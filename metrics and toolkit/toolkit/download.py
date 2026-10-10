import json,pathlib,urllib.request,hashlib
cat=json.load(open('Official-Home-Library-Root-Catalog.json'))
d=pathlib.Path('corpus/apks');d.mkdir(parents=True,exist_ok=True)
for h in cat['homes']:
 p=d/h['assetName'];u='https://github.com/nikitat21/Quest-Home-Switcher/releases/download/homes-v2.0.0/'+h['assetName']
 if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest().upper()!=h['apkSha256']:urllib.request.urlretrieve(u,p)
 assert hashlib.sha256(p.read_bytes()).hexdigest().upper()==h['apkSha256']
 print(h['displayName'], 'verified')
