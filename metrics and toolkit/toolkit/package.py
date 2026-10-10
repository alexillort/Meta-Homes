import pathlib,json,struct,urllib.parse,zipfile,hashlib,csv
root=pathlib.Path('corpus/homes');out=pathlib.Path('deliverables')
rows=[]
for d in sorted(root.iterdir()):
 if not (d/'metadata.json').exists():continue
 g=json.load(open(d/'scene.gltf'));b=bytearray((d/'scene.bin').read_bytes());cache={}
 for im in g.get('images',[]):
  uri=im.pop('uri');p=d/urllib.parse.unquote(uri)
  if uri not in cache:
   while len(b)%4:b.append(0)
   data=p.read_bytes();vi=len(g['bufferViews']);g['bufferViews'].append({'buffer':0,'byteOffset':len(b),'byteLength':len(data)});b.extend(data);cache[uri]=vi
  im.update({'bufferView':cache[uri],'mimeType':'image/png'})
 g['buffers']=[{'byteLength':len(b)}]
 while len(b)%4:b.append(0)
 js=json.dumps(g,separators=(',',':')).encode()
 while len(js)%4:js+=b' '
 p=d/'scene.glb'
 with open(p,'wb') as f:f.write(struct.pack('<III',0x46546c67,2,12+8+len(js)+8+len(b)));f.write(struct.pack('<II',len(js),0x4e4f534a));f.write(js);f.write(struct.pack('<II',len(b),0x004e4942));f.write(b)
 assert struct.unpack_from('<I',p.read_bytes(),8)[0]==p.stat().st_size
 row=json.load(open(d/'metadata.json'))['extraction'];row['unique_png_files']=len(list(d.glob('**/*.png')));row['glb_bytes']=p.stat().st_size;row['glb_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();row['load_report']=(d/'extraction.log').read_text();rows.append(row)
 print('GLB',d.name,p.stat().st_size,flush=True)
(out/'catalog_and_metrics.json').write_text(json.dumps(rows,indent=2));fields=list(dict.fromkeys(k for r in rows for k in r))
with open(out/'catalog_and_metrics.csv','w') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
print('Packaged',len(rows),'homes',flush=True)
