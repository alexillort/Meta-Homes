import os,json,pathlib,hashlib,zipfile,subprocess,urllib.parse,struct,csv,concurrent.futures
root=pathlib.Path('corpus');cat=json.load(open('Official-Home-Library-Root-Catalog.json'))
def extract(h):
 existing=root/'homes'/h['id']/'metadata.json'
 if existing.exists():return json.load(open(existing))['extraction']
 p=root/'apks'/h['assetName'];sha=hashlib.sha256(p.read_bytes()).hexdigest();assert sha.upper()==h['apkSha256']
 out=root/'homes'/h['id'];out.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(p) as z:
  raw=z.read('assets/scene.zip');assert hashlib.sha256(raw).hexdigest().upper()==h['cookedSceneSha256']
  (out/'source_scene.zip').write_bytes(raw)
 env=os.environ.copy()
 if h['id'] in ['oceanarium','storybook']:env['MQH_TEXCAP']='1024'
 with open(out/'extraction.log','w') as log:r=subprocess.run(['build/extract',str(p),str(out)],stdout=log,stderr=log,env=env)
 if r.returncode: return {'home':h['displayName'],'status':'failed','code':r.returncode}
 g=json.load(open(out/'scene.gltf'));props=json.load(open(out/'source_properties.json'));assert len(g['meshes'])==len(props)
 b=bytearray((out/'scene.bin').read_bytes())
 for mi,pr in enumerate(props):
  m=g['materials'][mi];m.update({k:pr[k] for k in ['alphaMode','doubleSided']})
  if pr['alphaMode']=='MASK':m['alphaCutoff']=pr['alphaCutoff']
  m['pbrMetallicRoughness']['baseColorFactor']=pr['tint'];m['extensions']={'KHR_materials_unlit':{}}
  m['extras']={'sourceShader':pr['shader'],'additive':pr['additive'],'overlayKind':pr['overlayKind']}
  if 'lightmap' in pr:m['extras']['lightmapFile']=pr['lightmap']
  if 'orm' in pr:m['extras']['packedTextureFile']=pr['orm']
  if 'uv1' in pr:
   data=(out/pr['uv1']).read_bytes()
   while len(b)%4:b.append(0)
   bv=len(g['bufferViews']);g['bufferViews'].append({'buffer':0,'byteOffset':len(b),'byteLength':len(data),'target':34962});b.extend(data)
   ai=len(g['accessors']);g['accessors'].append({'bufferView':bv,'componentType':5126,'count':len(data)//8,'type':'VEC2'});g['meshes'][mi]['primitives'][0]['attributes']['TEXCOORD_1']=ai
 g['extensionsUsed']=list(set(g.get('extensionsUsed',[])+['KHR_materials_unlit']));g['buffers'][0]['byteLength']=len(b)
 (out/'scene.bin').write_bytes(b);(out/'scene.gltf').write_text(json.dumps(g,separators=(',',':')))
 # Check all referenced files, accessor bounds, finite coordinates, and index range.
 nv=nt=0;mins=[float('inf')]*3;maxs=[float('-inf')]*3
 for im in g.get('images',[]):assert (out/urllib.parse.unquote(im['uri'])).is_file()
 for a in g['accessors']:
  v=g['bufferViews'][a['bufferView']];size={5121:1,5123:2,5125:4,5126:4}[a['componentType']]*{'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]*a['count'];assert a.get('byteOffset',0)+size<=v['byteLength'];assert v.get('byteOffset',0)+v['byteLength']<=len(b)
 for mi,mesh in enumerate(g['meshes']):
  pr=mesh['primitives'][0];a=g['accessors'][pr['attributes']['POSITION']];v=g['bufferViews'][a['bufferView']];nv+=a['count']
  aidx=g['accessors'][pr['indices']];vidx=g['bufferViews'][aidx['bufferView']];indices=struct.unpack_from('<'+'I'*aidx['count'],b,vidx['byteOffset']);assert max(indices)<a['count'];assert len(indices)%3==0;nt+=len(indices)//3
  tr=g['nodes'][mi].get('translation',[0,0,0])
  for k in range(3):mins[k]=min(mins[k],a['min'][k]+tr[k]);maxs[k]=max(maxs[k],a['max'][k]+tr[k])
 row={'home':h['displayName'],'id':h['id'],'package':h['packageName'],'status':'extracted_static','meshes':len(g['meshes']),'vertices':nv,'triangles':nt,'materials':len(g['materials']),'images':len(g.get('images',[])),'apk_sha256':sha,'source_scene_sha256':hashlib.sha256(raw).hexdigest(),'bounds_min':mins,'bounds_max':maxs,'animation_export':'not_converted; preserved in source_scene.zip','historical_original':False}
 row['texture_max_dimension']=int(env['MQH_TEXCAP']) if 'MQH_TEXCAP' in env else None
 (out/'metadata.json').write_text(json.dumps({'catalog':h,'extraction':row},indent=2));print(h['displayName'],len(g['meshes']),nt,flush=True);return row
with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:rows=list(pool.map(extract,cat['homes']))
pathlib.Path('deliverables/catalog_and_metrics.json').write_text(json.dumps(rows,indent=2))
with open('deliverables/catalog_and_metrics.csv','w') as f:w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
