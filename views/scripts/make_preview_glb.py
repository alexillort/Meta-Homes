import zipfile,pathlib,json,struct,io,sys
from PIL import Image
name=sys.argv[1];out=pathlib.Path('previews/assets')/name;out.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile('deliverables/Meta_Homes_22_GLB.zip') as z:
 with z.open(name+'/scene.glb') as f:
  f.read(12);n,t=struct.unpack('<II',f.read(8));g=json.loads(f.read(n));f.read(8)
  imageviews=sorted(set(im['bufferView'] for im in g.get('images',[])),key=lambda i:g['bufferViews'][i]['byteOffset'])
  first=g['bufferViews'][imageviews[0]]['byteOffset'] if imageviews else g['buffers'][0]['byteLength'];buf=bytearray(f.read(first));at=first
  for vi in imageviews:
   v=g['bufferViews'][vi];skip=v['byteOffset']-at
   if skip:f.read(skip)
   b=f.read(v['byteLength']);assert len(b)==v['byteLength'];at=v['byteOffset']+v['byteLength']
   im=Image.open(io.BytesIO(b)).convert('RGBA');im.thumbnail((512,512),Image.Resampling.LANCZOS);stream=io.BytesIO();im.save(stream,format='PNG',compress_level=1);b=stream.getvalue()
   while len(buf)%4:buf.append(0)
   v['byteOffset']=len(buf);v['byteLength']=len(b);buf.extend(b)
 g['buffers']=[{'byteLength':len(buf)}]
 while len(buf)%4:buf.append(0)
 js=json.dumps(g,separators=(',',':')).encode()
 while len(js)%4:js+=b' '
 with (out/'preview.glb').open('wb') as f:
  f.write(struct.pack('<III',0x46546c67,2,12+8+len(js)+8+len(buf)));f.write(struct.pack('<II',len(js),0x4e4f534a));f.write(js);f.write(struct.pack('<II',len(buf),0x004e4942));f.write(buf)
 for fn in ['metadata.json','source_properties.json','scene.blendmeta.json']:(out/fn).write_bytes(z.read(name+'/'+fn))
print(name,len(buf),flush=True)
