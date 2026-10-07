"""Behavior tests for ChihiroPack (no copyrighted game data)."""
from pathlib import Path
import importlib.util,tempfile,zipfile,hashlib,struct,subprocess,sys,json
p=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('pack',p/'chihiro_pack.py');pack=importlib.util.module_from_spec(spec);spec.loader.exec_module(pack)
def fixture(root):
 root.mkdir(parents=True);b=bytearray(480);b[:4]=b'BTID';b[32:36]=b'XBAM';b[128:132]=b'TEST';b[160:169]=b'\\game.xbe';(root/'boot.id').write_bytes(b);(root/'game.xbe').write_bytes(b'XBEHfixture')
 (root/'assets').mkdir();(root/'assets/two-clusters').write_bytes(bytes(range(256))*33);(root/'empty').write_bytes(b'')
 for i in range(80):(root/f'a{i:03}').write_bytes(str(i).encode())
def rejected(fn):
 try:fn()
 except pack.PackError:return
 raise AssertionError('invalid input accepted')
with tempfile.TemporaryDirectory() as d:
 d=Path(d);root=d/'outer/game';fixture(root)
 image=d/'fixture.bin';pack.create(d/'outer',image)
 expected={x.relative_to(root).as_posix():{'size':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in root.rglob('*') if x.is_file()}
 assert pack.verify(image,expected)['files_verified']==84
 # Independently use the core's media-reader allocation formula, not geometry().
 with image.open('rb') as f:
  h=f.read(16);spc,start=struct.unpack_from('<II',h,8);cluster=spc*512;entries=image.stat().st_size//cluster+1;data=4096+((entries*4+4095)//4096)*4096
  f.seek(data+(start-1)*cluster);e=f.read(64);assert e[2:9]==b'boot.id'
  first=struct.unpack_from('<I',e,44)[0];f.seek(data+(first-1)*cluster);assert f.read(4)==b'BTID'
 old=hashlib.file_digest(image.open('rb'),'sha256').hexdigest();rejected(lambda:pack.create(root,image));assert hashlib.file_digest(image.open('rb'),'sha256').hexdigest()==old
 with image.open('r+b') as f:f.seek(data+(first-1)*cluster+100);f.write(b'BAD')
 rejected(lambda:pack.verify(image,expected))
 z=d/'fixture.zip'
 with zipfile.ZipFile(z,'w') as ar:
  for x in root.rglob('*'):
   if x.is_file():ar.write(x,x.relative_to(d/'outer'))
 pack.create(z,d/'zip.bin');assert pack.verify(d/'zip.bin',expected)['files_verified']==84
 slip=d/'slip.zip'
 with zipfile.ZipFile(slip,'w') as ar:ar.writestr('../outside','bad')
 rejected(lambda:pack.create(slip,d/'slip.bin'));assert not (d/'outside').exists()
 missing=d/'missing';missing.mkdir();rejected(lambda:pack.create(missing,d/'missing.bin'))
 (root/'GAME.XBE').write_bytes(b'XBEH');rejected(lambda:pack.create(root,d/'collision.bin'));(root/'GAME.XBE').unlink()
 (root/'game.xbe').unlink();rejected(lambda:pack.create(root,d/'missing-exe.bin'));(root/'game.xbe').write_bytes(b'XBEHfixture')
 with (root/'oversized').open('wb') as f:f.truncate(pack.IMAGE_BYTES)
 rejected(lambda:pack.create(root,d/'large.bin'));(root/'oversized').unlink()
 second=d/'other';fixture(second);rejected(lambda:pack.game_root(d))
 # Batch continues after a malformed package and reports a nonzero result.
 batch=d/'batch';batch.mkdir();shutil=__import__('shutil');shutil.copytree(root,batch/'good');(batch/'bad').mkdir()
 result=subprocess.run([sys.executable,str(p/'chihiro_pack.py'),'create',str(batch),'--batch','--output-dir',str(d/'batch-output')],capture_output=True,text=True)
 assert result.returncode==1 and (d/'batch-output/good.bin').exists() and 'ERROR [bad]' in result.stdout
 print('PASS: folder/ZIP conversion; nested root, empty files, multi-cluster files/directories; native reader layout; byte identity; corruption, collisions, traversal, missing executable, oversize, overwrite refusal; batch continuation')
