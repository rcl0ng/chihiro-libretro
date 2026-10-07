#!/usr/bin/env python3
"""ChihiroPack: build and independently verify FATX package images. MIT license."""
from __future__ import annotations
import argparse, contextlib, hashlib, json, math, os, shutil, struct, subprocess
import sys, tempfile
from pathlib import Path, PurePosixPath

VERSION = "1.0"
IMAGE_BYTES = 496 * 1024 * 1024
CLUSTER = 4096
END = 0xFFFFFFFF
BASE = Path(__file__).resolve().parent

class PackError(Exception): pass

def log(message): print(message, flush=True)

def name_bytes(name):
    try: value = name.encode("ascii")
    except UnicodeEncodeError: raise PackError(f"FATX needs ASCII names: {name!r}")
    if not 1 <= len(value) <= 42 or name in (".", "..") or any(c < 32 or c >= 127 or chr(c) in '\"*/:<>?\\|' for c in value):
        raise PackError(f"Invalid FATX name (maximum 42 ASCII bytes): {name!r}")
    return value

def geometry(size=IMAGE_BYTES):
    if size != IMAGE_BYTES: raise PackError("This tool uses a 496 MiB Chihiro image")
    # Select a FAT large enough without a potentially oscillating fixed point.
    fat_size = math.ceil((size // CLUSTER + 1) * 4 / 4096) * 4096
    data_start = 4096 + fat_size
    return fat_size, data_start, (size - data_start) // CLUSTER

def sevenzip():
    candidates = [BASE / "7za.exe"] if os.name == "nt" else [BASE / "7zip-linux/7zz"]
    for p in candidates:
        if p.is_file(): return str(p)
    for exe in ("7zz", "7z", "7za"):
        if p := shutil.which(exe): return p
    raise PackError("ZIP/7z input needs the bundled 7za.exe; keep the portable folder together")

def archive_command(args):
    result = subprocess.run([sevenzip(), *args], stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            encoding="utf-8", errors="replace")
    if result.returncode: raise PackError("Archive operation failed:\n" + result.stdout[-3500:])
    return result.stdout

def safe_archive(path):
    listing = archive_command(["l", "-slt", "-ba", "-sccUTF-8", "--", str(path)])
    seen = set()
    total = 0
    for block in listing.split("\n\n"):
        fields = dict(line.split(" = ", 1) for line in block.splitlines() if " = " in line)
        if "Path" not in fields: continue
        name = fields["Path"].replace("\\", "/")
        parts = PurePosixPath(name).parts
        if not parts or name.startswith("/") or any(p in (".", "..") or ":" in p or any(ord(c)<32 for c in p) for p in parts):
            raise PackError(f"Unsafe archive path: {name!r}")
        if any(p.endswith((" ", ".")) or p.split(".")[0].upper() in {"CON","PRN","AUX","NUL",*(f"COM{i}" for i in range(1,10)),*(f"LPT{i}" for i in range(1,10))} for p in parts):
            raise PackError(f"Unsupported Windows archive path: {name!r}")
        if any(k in fields for k in ("Symbolic Link", "Hard Link")) or any(token.startswith("l") for token in (fields.get("Attributes", "") + " " + fields.get("Mode", "")).split()):
            raise PackError(f"Archive links are unsupported: {name!r}")
        key = name.casefold().rstrip("/")
        if key in seen: raise PackError(f"Case-insensitive duplicate archive path: {name}")
        seen.add(key)
        total += int(fields.get("Size", "0"))
    if not seen: raise PackError("Empty or unreadable archive")
    if total > IMAGE_BYTES: raise PackError(f"Package expands to {total:,} bytes: exceeds Chihiro image capacity")

@contextlib.contextmanager
def package(source):
    source = source.resolve()
    if source.is_dir(): yield source; return
    if source.suffix.lower() not in (".zip", ".7z"): raise PackError("Input must be a game directory, ZIP or 7z")
    safe_archive(source)
    with tempfile.TemporaryDirectory(prefix="chihiropack-") as temporary:
        log("Extracting package and checking archive CRCs...")
        archive_command(["x", "-y", "-sccUTF-8", "-o"+temporary, "--", str(source)])
        root = Path(temporary).resolve()
        for p in root.rglob("*"):
            if p.is_symlink() or not p.resolve().is_relative_to(root): raise PackError("Archive contains a link outside the package")
        yield root

def game_root(root):
    boots = [p for p in root.rglob("*") if p.name.lower()=="boot.id" and p.is_file()]
    if len(boots) != 1: raise PackError(f"Expected one boot.id; found {len(boots)}. Select one game package.")
    root = boots[0].parent
    bid = boots[0].read_bytes()
    if len(bid)!=480 or bid[:4]!=b"BTID" or bid[32:36]!=b"XBAM": raise PackError("Invalid Chihiro boot.id (expected 480-byte BTID/XBAM header)")
    try: entry = bid[160:191].split(b"\0",1)[0].decode("ascii").replace("\\","/").lstrip("/")
    except UnicodeDecodeError: raise PackError("Invalid executable name in boot.id")
    if not entry or any(p in (".","..") for p in entry.split("/")): raise PackError("Unsafe executable name in boot.id")
    files = {p.relative_to(root).as_posix().casefold():p for p in root.rglob("*") if p.is_file()}
    if entry.casefold() not in files: raise PackError(f"boot.id executable missing: {entry}")
    with files[entry.casefold()].open("rb") as f:
        if f.read(4)!=b"XBEH": raise PackError(f"Not a valid XBE executable: {entry}")
    title = bid[128:160].split(b"\0",1)[0].decode("ascii", "replace")
    return root, title, entry

def scan(root):
    nodes = {"": {"path":root,"directory":True,"size":0}}
    for p in sorted(root.rglob("*"),key=lambda p:p.relative_to(root).as_posix().casefold()):
        if p.is_symlink() or not p.resolve().is_relative_to(root.resolve()): raise PackError(f"Links unsupported: {p}")
        if not p.is_dir() and not p.is_file(): raise PackError(f"Special files unsupported: {p}")
        rel = p.relative_to(root).as_posix()
        name_bytes(p.name)
        if any(k.casefold()==rel.casefold() for k in nodes): raise PackError(f"Case-insensitive name collision: {rel}")
        nodes[rel] = {"path":p,"directory":p.is_dir(),"size":0 if p.is_dir() else p.stat().st_size}
    for rel,n in nodes.items():
        if n["directory"]:
            n["children"] = [k for k in nodes if k and str(PurePosixPath(k).parent).replace(".","",1)==rel] if not rel else [k for k in nodes if k and str(PurePosixPath(k).parent)==rel]
            if not rel:n["children"].sort(key=lambda name:(PurePosixPath(name).name.lower()!="boot.id",name.casefold()))
            n["count"] = max(1, math.ceil((len(n["children"])+1)*64/CLUSTER))
        else: n["count"] = math.ceil(n["size"]/CLUSTER)
    return nodes

def verify(image, expected=None):
    size = image.stat().st_size
    fat_size,data_start,capacity = geometry(size)
    used = set(); files = {}; directories = []
    with image.open("rb") as f:
        header=f.read(4096)
        if header[:4]!=b"FATX" or struct.unpack_from("<II",header,8)!=(8,1): raise PackError("Unexpected FATX header")
        fat=struct.unpack("<"+"I"*(fat_size//4),f.read(fat_size))
        def chain(first):
            out=[]; c=first
            while c!=END:
                if c<1 or c>capacity or c in used: raise PackError("Invalid, shared or looping FATX cluster chain")
                used.add(c);out.append(c);c=fat[c]
                if len(out)>capacity: raise PackError("FATX chain too long")
            return out
        def read_cluster(c):
            f.seek(data_start+(c-1)*CLUSTER);data=f.read(CLUSTER)
            if len(data)!=CLUSTER: raise PackError("Truncated FATX data")
            return data
        def walk(first,parent,depth=0):
            if depth>128: raise PackError("Directory nesting too deep")
            data=b"".join(read_cluster(c) for c in chain(first));seen=set()
            for pos in range(0,len(data),64):
                entry=data[pos:pos+64];length=entry[0]
                if length in (0,255): break
                if length>42: raise PackError("Invalid FATX directory entry")
                try: name=entry[2:2+length].decode("ascii")
                except UnicodeDecodeError: raise PackError("Non-ASCII FATX entry")
                name_bytes(name)
                if name.casefold() in seen: raise PackError("Duplicate FATX name")
                seen.add(name.casefold());rel=parent+name
                start,length_bytes=struct.unpack_from("<II",entry,44)
                if entry[1]&16: directories.append(rel);walk(start,rel+"/",depth+1)
                else:
                    blocks=chain(start) if length_bytes else []
                    if len(blocks)!=math.ceil(length_bytes/CLUSTER): raise PackError("File allocation/length mismatch")
                    digest=hashlib.sha256();remaining=length_bytes
                    for c in blocks:
                        chunk=read_cluster(c)[:min(remaining,CLUSTER)];digest.update(chunk);remaining-=len(chunk)
                    files[rel]={"size":length_bytes,"sha256":digest.hexdigest()}
        walk(1,"")
    if expected is not None and files!=expected: raise PackError("Readback files do not match source package")
    return {"image":image.name,"image_bytes":size,"image_sha256":hashlib.file_digest(image.open("rb"),"sha256").hexdigest(),"files_verified":len(files),"directories_verified":len(directories),"status":"PASS: FATX structure and file payloads verified" if expected is not None else "PASS: FATX structure read; compare to a source package or report to verify original payloads","files":files}

def create(source,output):
    output=output.resolve();report=output.with_suffix(output.suffix+".verification.json")
    if output.exists() or report.exists(): raise PackError(f"Output already exists: {output}. Choose a new output filename.")
    with package(source) as extracted:
        root,title,entry=game_root(extracted)
        if output.is_relative_to(root): raise PackError("Output must be outside the source game directory")
        nodes=scan(root);fat_size,data_start,capacity=geometry()
        required=sum(n["count"] for n in nodes.values())
        if required>capacity: raise PackError(f"Needs {required} clusters; image holds {capacity}. Game package is too large.")
        log(f"Game: {title}; executable: {entry}; {sum(not n['directory'] for n in nodes.values())} files")
        output.parent.mkdir(parents=True,exist_ok=True)
        fat=[0]*(fat_size//4);fat[0]=0xFFFFFFF8;next_cluster=1
        for n in nodes.values():
            count=n["count"];n["first"]=next_cluster if count else 0
            for c in range(next_cluster,next_cluster+count):fat[c]=c+1 if c+1<next_cluster+count else END
            next_cluster+=count
        expected={}
        fd,part=tempfile.mkstemp(prefix=output.name+".",suffix=".partial",dir=output.parent);os.close(fd);part=Path(part)
        try:
            with part.open("w+b") as f:
                f.truncate(IMAGE_BYTES);header=bytearray(4096);struct.pack_into("<4sIII",header,0,b"FATX",0x524F4E31,8,1);f.write(header);f.write(struct.pack("<"+"I"*len(fat),*fat))
                for rel,n in nodes.items():
                    if n["directory"]:
                        data=bytearray(b"\xff"*(n["count"]*CLUSTER))
                        for i,child in enumerate(n["children"]):
                            c=nodes[child];name=name_bytes(PurePosixPath(child).name);record=bytearray(64);record[0]=len(name);record[1]=16 if c["directory"] else 32;record[2:2+len(name)]=name
                            struct.pack_into("<II",record,44,c["first"],c["size"]);data[i*64:(i+1)*64]=record
                        f.seek(data_start+(n["first"]-1)*CLUSTER);f.write(data)
                    else:
                        if n["count"]: f.seek(data_start+(n["first"]-1)*CLUSTER)
                        digest=hashlib.sha256();written=0
                        with n["path"].open("rb") as src:
                            while chunk:=src.read(1024*1024):f.write(chunk);digest.update(chunk);written+=len(chunk)
                        if written!=n["size"]: raise PackError(f"Source file changed during conversion: {rel}")
                        expected[rel]={"size":written,"sha256":digest.hexdigest()}
                f.flush();os.fsync(f.fileno())
            log("Reading image back and verifying every file...")
            validation=verify(part,expected);validation.update(image=output.name,title=title,executable=entry,tool_version=VERSION,source_files=sum(n["size"] for n in nodes.values()))
            # Preserve all source payloads, including original boot.id and XBE bytes.
            # Never overwrite an existing image, even if another process raced us.
            try:
                os.link(part,output)
            except FileExistsError:
                raise PackError(f"Output already exists: {output}")
            except OSError:
                owned=False
                try:
                    with output.open("xb") as dst,part.open("rb") as src:
                        owned=True;shutil.copyfileobj(src,dst,1024*1024);dst.flush();os.fsync(dst.fileno())
                except Exception:
                    if owned:output.unlink(missing_ok=True)
                    raise
            report.write_text(json.dumps(validation,indent=2)+"\n",encoding="utf-8")
            log(f"PASS: {validation['files_verified']} files verified.\nBIN: {output}\nReport: {report}")
        except Exception:
            # Existing user outputs are never removed; our own failed copy is cleaned.
            raise
        finally: part.unlink(missing_ok=True)

def main():
    args=sys.argv[1:];pause="--pause" in args
    if pause:args.remove("--pause")
    if not args:
        log(f"ChihiroPack {VERSION}: drop a game folder, ZIP or 7z onto ChihiroPack.exe.")
        text=input("Or enter a game package path: ").strip().strip('"')
        if not text:return 0
        args=[text]
    if args[0] not in ("create","verify","--help","-h","--version"):args.insert(0,"create")
    p=argparse.ArgumentParser(description="Package complete Chihiro XBE games into verified FATX BIN images")
    p.add_argument("--version",action="version",version=VERSION)
    sub=p.add_subparsers(dest="command",required=True)
    c=sub.add_parser("create",help="Convert game directories, ZIPs or 7z archives")
    c.add_argument("inputs",nargs="+",type=Path);c.add_argument("-o","--output",type=Path);c.add_argument("--output-dir",type=Path);c.add_argument("--batch",action="store_true",help="Convert immediate game folders/archives inside the input directory")
    v=sub.add_parser("verify",help="Read a BIN and compare payloads to its conversion report")
    v.add_argument("image",type=Path);v.add_argument("--report",type=Path)
    code=0
    try:
        a=p.parse_args(args)
        if a.command=="verify":
            report=a.report or a.image.with_suffix(a.image.suffix+".verification.json")
            expected=json.loads(report.read_text(encoding="utf-8"))["files"] if report.exists() else None
            result=verify(a.image,expected)
            if expected is not None:
                saved=json.loads(report.read_text(encoding="utf-8"))
                if result["image_sha256"]!=saved["image_sha256"]:raise PackError("Image hash differs from conversion report")
            log(result["status"]+f"; {result['files_verified']} files")
        else:
            inputs=a.inputs
            if a.batch:
                if len(inputs)!=1 or not inputs[0].is_dir():raise PackError("--batch needs one directory containing game folders/archives")
                inputs=sorted(x for x in inputs[0].iterdir() if x.is_dir() or x.suffix.lower() in (".zip",".7z"))
            if not inputs:raise PackError("No game packages found")
            if a.output and len(inputs)!=1:raise PackError("--output is for one input; use --output-dir for a batch")
            if a.output and a.output_dir:raise PackError("Choose --output or --output-dir, not both")
            for source in inputs:
                stem=source.name if source.is_dir() else source.stem
                if stem.lower().endswith(".game"):stem=stem[:-5]
                output=a.output or (a.output_dir or source.resolve().parent)/f"{stem}.bin"
                try:create(source,output)
                except (PackError,OSError,ValueError,KeyError) as e:log(f"ERROR [{source.name}]: {e}");code=1
    except (PackError,OSError,ValueError,KeyError) as e:log(f"ERROR: {e}");code=1
    except KeyboardInterrupt:log("Cancelled.");code=130
    finally:
        if pause:
            try:input("Press Enter to close...")
            except (EOFError,KeyboardInterrupt):pass
    return code

if __name__=="__main__":sys.exit(main())
