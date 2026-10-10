import pathlib,hashlib,json
for d in pathlib.Path('corpus/homes').iterdir():
 if not (d/'metadata.json').exists() or (d/'dedup.done').exists():continue
 byhash={};replace={}
 for p in sorted(d.glob('**/*.png')):
  sha=hashlib.sha256(p.read_bytes()).digest()
  if sha in byhash:replace[p.relative_to(d).as_posix()]=byhash[sha].relative_to(d).as_posix();p.unlink()
  else:byhash[sha]=p
 for n in ['scene.gltf','source_properties.json']:
  p=d/n;x=json.load(open(p))
  def walk(v):
   if isinstance(v,dict):return {k:walk(vv) for k,vv in v.items()}
   if isinstance(v,list):return [walk(vv) for vv in v]
   if isinstance(v,str):return replace.get(v,v)
   return v
  p.write_text(json.dumps(walk(x),separators=(',',':')))
 (d/'dedup.done').write_text(str(len(replace)));print(d.name,len(replace),flush=True)
