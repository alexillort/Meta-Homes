from PIL import Image,ImageDraw,ImageFont
import json,pathlib,zipfile
root=pathlib.Path('previews');out=root/'gallery';out.mkdir(exist_ok=True)
rows={r['id']:r for r in json.load(open('deliverables/catalog_and_metrics.json'))}
groups=[['classic-home','cyber-city','winter-lodge','desert-terrace','space-station','quest-dome'],['mogu-hall','crystal-atrium','mountain-study','studio','blue-hill-gold-mine','cascadia'],['futurescape','lakeside-peak','oceanarium','paradiso','polar-village','storybook'],['abstraction','bubbles','rockquarry','meta-horizon-terrace']]
assert set(sum(groups,[]))==set(rows)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';title=ImageFont.truetype(font,30);label=ImageFont.truetype(font,25);small=ImageFont.truetype(font,18)
for i,names in enumerate(groups,1):
 im=Image.new('RGB',(1312,100+len(names)*462),(18,23,30));draw=ImageDraw.Draw(im);draw.text((24,18),'INTERIOR',font=title,fill='#e7eef7');draw.text((676,18),'EXTERIOR DEL MODELO',font=title,fill='#e7eef7');draw.text((24,60),'Renders estáticos · Blender · fondos envolventes ocultos en el exterior',font=small,fill='#a9b8ca')
 for j,n in enumerate(names):
  y=100+j*462;draw.text((24,y),rows[n]['home'],font=label,fill='#ffffff')
  for k,v in enumerate(['inside','outside']):
   p=root/'images'/n/(v+'.png');image=Image.open(p).convert('RGB').resize((640,400),Image.Resampling.LANCZOS);im.paste(image,(16+k*656,y+42))
 im.save(out/f'Meta_Homes_Views_{i:02}.jpg',quality=93,subsampling=0)
readme='22 Homes del catálogo de ports de Meta/Oculus. 44 renders estáticos (interior + exterior), 1280 × 800.\nNo son capturas del visor. Materiales aproximados a partir de los GLB extraídos; texturas de previsualización de hasta 512 px. Animaciones, niebla y shaders propietarios no se reproducen. Las vistas exteriores ocultan fondos envolventes y geometría de fondo de gran escala para revelar la construcción del entorno. Vértices guía extremos de algunas mallas animadas se omiten en estas previsualizaciones. Cámara interior aproximada; no se valida como punto de spawn oficial.\n'
(out/'README.txt').write_text(readme)
with zipfile.ZipFile(out/'Meta_Homes_44_Views.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=1) as z:
 for n in rows:
  for p in sorted((root/'images'/n).iterdir()):z.write(p,n+'/'+p.name)
 for p in sorted(out.glob('Meta_Homes_Views_*.jpg')):z.write(p,p.name)
 z.write(out/'README.txt','README.txt')
print('Gallery created',flush=True)
