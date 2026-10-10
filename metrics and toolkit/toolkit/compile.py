import subprocess,pathlib
src=[str(p) for p in pathlib.Path('astc/Source').glob('astcenc_*.cpp')]
incs=['astc/Source','editor/QuestHomeEditor/src','editor/QuestHomeEditor/third_party/miniz','editor/QuestHomeEditor/third_party/stb','editor/QuestHomeEditor/third_party/acl/includes','editor/QuestHomeEditor/third_party/rtm/includes']
cmd=['g++','-std=c++17','-O1','-pthread','-DASTCENC_SSE=41','-DASTCENC_AVX=0','-DASTCENC_NEON=0','-DASTCENC_POPCNT=0','-DASTCENC_F16C=0','-msse4.1']+['-I'+s for s in incs]+['build/extract.cpp','editor/QuestHomeEditor/src/cook/hzanim_acl.cpp']+src+[str(p) for p in pathlib.Path('editor/QuestHomeEditor/third_party/miniz').glob('*.c')]+['editor/QuestHomeEditor/src/impl/stb_image_impl.c','-o','build/extract']
with open('build/compile.log','w') as f:r=subprocess.run(cmd,stdout=f,stderr=f)
print(r.returncode)
