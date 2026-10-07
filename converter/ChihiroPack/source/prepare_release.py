"""Download pinned official dependencies and assemble the portable folder. MIT."""
from pathlib import Path
import argparse,hashlib,shutil,subprocess,urllib.request,zipfile,json
ROOT=Path(__file__).resolve().parent
SOURCES={
 '7z-source.7z':('https://www.7-zip.org/a/7z2603-src.7z','41e2a7c0e9f838351c625e01f0f581a2188bb3dda10c8e0b4a852da26546ffe2'),
 'python-embed.zip':('https://www.python.org/ftp/python/3.13.7/python-3.13.7-embed-amd64.zip','f6cca216a359be84797cabb54149ce5e062afb16cc7567eb7fc51cacb2d86b65'),
 '7z-extra.7z':('https://www.7-zip.org/a/7z2603-extra.7z','191894e6acb3647ffb69ce630479ff318523b2e2b9890aa7f05c1127c2e59b8f'),
}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--sevenzip',default=shutil.which('7z') or shutil.which('7zz') or r'C:\Program Files\7-Zip\7z.exe');ap.add_argument('--output',type=Path,default=ROOT/'dist/ChihiroPack');a=ap.parse_args()
 cache=ROOT/'dependency-cache';cache.mkdir(exist_ok=True);dest=a.output;dest.mkdir(parents=True,exist_ok=True)
 for name,(url,expected) in SOURCES.items():
  p=cache/name
  if not p.exists():
   with urllib.request.urlopen(url,timeout=90) as src,p.open('wb') as dst:shutil.copyfileobj(src,dst)
  actual=hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
  if actual!=expected:raise RuntimeError('Dependency checksum mismatch: '+name)
 with zipfile.ZipFile(cache/'python-embed.zip') as z:z.extractall(dest/'runtime')
 (dest/'runtime/python313._pth').write_text('python313.zip\n.\n')
 extra=cache/'7zip-extra';extra.mkdir(exist_ok=True)
 subprocess.run([a.sevenzip,'x','-y','-o'+str(extra),str(cache/'7z-extra.7z')],check=True)
 shutil.copy2(extra/'x64/7za.exe',dest/'7za.exe')
 licenses=dest/'licenses';licenses.mkdir(exist_ok=True)
 shutil.copy2(extra/'License.txt',licenses/'7zip-LICENSE.txt');shutil.copy2(dest/'runtime/LICENSE.txt',licenses/'Python-LICENSE.txt')
 for name in ['ChihiroPack.exe','chihiro_pack.py','Convert_All_Packages.bat','README.md','LICENSE']:
  shutil.copy2(ROOT/name,dest/name)
 for name in ['input','output']:(dest/name).mkdir(exist_ok=True)
 third=dest/'third_party/7zip';third.mkdir(parents=True,exist_ok=True)
 shutil.copy2(cache/'7z-source.7z',third/'7z2603-src.7z')
 (dest/'dependency-checksums.json').write_text(json.dumps({k:{'url':v[0],'sha256':v[1]} for k,v in SOURCES.items()},indent=2)+'\n')
 print('Portable release:',dest)
if __name__=='__main__':main()
