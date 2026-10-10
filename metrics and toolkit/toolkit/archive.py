import pathlib,json,zipfile
root=pathlib.Path('corpus/homes');out=pathlib.Path('deliverables')
with zipfile.ZipFile(out/'Meta_Homes_22_GLB.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as z:
 for d in sorted(root.iterdir()):
  assert (d/'scene.glb').is_file(),d
  files={d/n for n in ['scene.glb','source_properties.json','scene.blendmeta.json','metadata.json','extraction.log']}
  for prop in json.load(open(d/'source_properties.json')):
   for k in ['lightmap','orm','uv1']:
    if k in prop:files.add(d/prop[k])
  for p in sorted(files):assert p.is_file(),p;z.write(p,d.name+'/'+p.relative_to(d).as_posix())
 z.write(out/'README.txt','README.txt');z.write(out/'catalog_and_metrics.json','catalog_and_metrics.json')
print('Models ZIP', (out/'Meta_Homes_22_GLB.zip').stat().st_size,flush=True)
with zipfile.ZipFile(out/'Meta_Homes_Source_Scenes.zip','w',compression=zipfile.ZIP_STORED,allowZip64=True) as z:
 for d in sorted(root.iterdir()):
  z.write(d/'source_scene.zip',d.name+'/source_scene.zip')
  for p in sorted(d.glob('apk_assets/**/*')):
   if p.is_file():z.write(p,d.name+'/'+p.relative_to(d).as_posix())
 z.write('Official-Home-Library-Root-Catalog.json','Official-Home-Library-Root-Catalog.json');z.write(out/'README.txt','README.txt')
print('Sources ZIP', (out/'Meta_Homes_Source_Scenes.zip').stat().st_size,flush=True)
with zipfile.ZipFile(out/'Meta_Homes_Metrics_and_Toolkit.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n in ['README.txt','catalog_and_metrics.json','catalog_and_metrics.csv','extractor_fixes.patch']:z.write(out/n,n)
 for p in sorted((out/'toolkit').iterdir()):z.write(p,'toolkit/'+p.name)
print('Toolkit saved',flush=True)
