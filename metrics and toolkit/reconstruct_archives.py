import json,pathlib,hashlib,os
root=pathlib.Path(__file__).resolve().parent
for archive in json.load(open(root/'archive_parts_manifest.json')):
 target=root/archive['archive'];tmp=target.with_suffix(target.suffix+'.rebuild')
 with tmp.open('wb') as out:
  for part in archive['parts']:
   sha=hashlib.sha256();count=0
   with (root/part['name']).open('rb') as f:
    while data:=f.read(1024*1024):out.write(data);sha.update(data);count+=len(data)
   if count!=part['size'] or sha.hexdigest()!=part['sha256']:raise ValueError('Invalid part: '+part['name'])
 os.replace(tmp,target);print('Reconstructed:',target.name)
