import bpy,sys,json,math,pathlib
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:];home=args[0];root=pathlib.Path(args[1]).resolve();d=root/'assets'/home;out=root/'images'/home;out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(d/'preview.glb'))
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=8;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=6
scene.render.resolution_x=1280;scene.render.resolution_y=800;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
scene.world=bpy.data.worlds.new('Backdrop');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(0.055,0.065,0.08,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=0.8
props=json.load(open(d/'source_properties.json'));names={p['name'].lower():p for p in props}
meshes=[o for o in scene.objects if o.type=='MESH'];sky=[];points=[]
for o in meshes:
 n=o.name.lower();pr=names.get(n) or names.get(n.rsplit('.',1)[0],{});corners=[o.matrix_world@Vector(c) for c in o.bound_box];span=max(max(p[k] for p in corners)-min(p[k] for p in corners) for k in range(3))
 if pr.get('overlayKind',0)>0 or any(x in n for x in ['navmesh','chairicon','chair_icon','collision']):o.hide_render=True;continue
 if any(x in n for x in ['skybox','skydome','sky_dome']):sky.append(o);continue
 if span>1000:
  import numpy as np
  co=np.array([tuple(o.matrix_world@v.co) for v in o.data.vertices]);bad=np.max(np.abs(co),axis=1)>1000
  if 0<bad.mean()<0.1:
   import bmesh
   bm=bmesh.new();bm.from_mesh(o.data);bm.verts.ensure_lookup_table();remove=[bm.verts[i] for i in np.flatnonzero(bad)];bmesh.ops.delete(bm,geom=remove,context='VERTS');bm.to_mesh(o.data);bm.free();o.data.update();bpy.context.view_layer.update()
   corners=[o.matrix_world@v.co for v in o.data.vertices];span=max(max(p[k] for p in corners)-min(p[k] for p in corners) for k in range(3))
  if span>1000:sky.append(o);continue
 if span>180:sky.append(o);continue
 if span<150:
  for p in corners:
   if abs(p.x)<60 and abs(p.y)<60 and -10<p.z<45:points.append(p)
if not points:points=[p for o in meshes for p in [o.matrix_world@Vector(c) for c in o.bound_box] if max(abs(p.x),abs(p.y),abs(p.z))<150]
import numpy as np
arr=np.array([tuple(p) for p in points]);low=np.percentile(arr,5,axis=0);high=np.percentile(arr,95,axis=0);center=Vector((low+high)/2);size=max(high-low);size=max(12,min(size,100));center.z=max(1.0,min(center.z,8.0))
camdata=bpy.data.cameras.new('Camera');cam=bpy.data.objects.new('Camera',camdata);scene.collection.objects.link(cam);scene.camera=cam;camdata.clip_start=0.03;camdata.clip_end=500000
camdata.lens=22
cam.location=(0,0,1.65);target=Vector((8,0,1.65)) if home=='desert-terrace' else (Vector((0,-8,1.65)) if home=='winter-lodge' else Vector((0,8,1.65)));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(out/'inside.png');bpy.ops.render.render(write_still=True)
for o in sky:o.hide_render=True
if home=='studio':
 for o in meshes:
  if '.bg_' in o.name.lower():o.hide_render=True
if home=='storybook':
 for o in meshes:
  if any(k in o.name.lower() for k in ['sky','backdrop','background','cloud']):o.hide_render=True
camdata.lens=45;distance_scale=3 if home in ['cyber-city','storybook'] else (2 if home in ['studio','crystal-atrium','winter-lodge'] else 1)
cam.location=center+Vector((size*0.85,-size*1.1,size*0.8))*distance_scale;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(out/'outside.png');bpy.ops.render.render(write_still=True)
hit=scene.ray_cast(bpy.context.evaluated_depsgraph_get(),cam.location,(center-cam.location).normalized());print('CENTER_HIT',hit[0],hit[4].name if hit[0] else None,tuple(hit[1]),flush=True)
(out/'camera.json').write_text(json.dumps({'inside_position':[0,0,1.65],'inside_target':[0,8,1.65],'outside_position':list(cam.location),'outside_target':list(center),'hidden_skyboxes':[o.name for o in sky],'preview_texture_max_dimension':512},indent=2))
print('DONE',home,flush=True)
