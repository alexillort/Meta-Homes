#include "loaders/scene_loader.h"
#include "io/gltf_export.h"
#include <fstream>
int main(int argc,char**argv){if(argc!=3)return 2;SceneLoader l;l.verbose=(std::getenv("MQH_VERBOSE") != nullptr);if(!l.load(argv[1])||l.meshes.empty())return 3;
std::filesystem::create_directories(argv[2]);std::ofstream meta(std::string(argv[2])+"/source_properties.json");meta<<"[";bool first=true;
for(size_t i=0;i<l.meshes.size();++i){auto&m=l.meshes[i];if(m.positions.size()<9||m.indices.size()<3)continue;
float mat[16];if(m.hasWorldMatrix)memcpy(mat,m.worldMatrix,sizeof(mat));else trsToMat4(m.transform,mat);
for(size_t v=0;v<m.positions.size();v+=3){float x=m.positions[v],y=m.positions[v+1],z=m.positions[v+2];for(int k=0;k<3;++k)m.positions[v+k]=mat[k]*x+mat[4+k]*y+mat[8+k]*z+mat[12+k];}
if(!first)meta<<",";first=false;meta<<"{\"source_mesh\":"<<i<<",\"name\":\""<<gltfexport::jesc(m.name)<<"\",\"shader\":\""<<gltfexport::jesc(m.shaderPath)<<"\",\"alphaMode\":\""<<(m.alphaTest?"MASK":(m.useBlend?"BLEND":"OPAQUE"))<<"\",\"alphaCutoff\":"<<m.alphaCutoff<<",\"doubleSided\":"<<(m.doubleSided?"true":"false")<<",\"additive\":"<<(m.additive?"true":"false")<<",\"overlayKind\":"<<m.overlayKind<<",\"tint\":["<<m.tint[0]<<","<<m.tint[1]<<","<<m.tint[2]<<","<<m.tint[3]<<"],\"hasVat\":"<<(m.hasVat?"true":"false");
auto png=[&](const char* role,const std::vector<u8>& buf,u32 w,u32 h){if(buf.size()>=size_t(w)*h*4){std::string fn=std::string(role)+"_"+std::to_string(i)+".png";gltfexport::writePng(std::string(argv[2])+"/"+fn,buf.data(),w,h);meta<<",\""<<role<<"\":\""<<fn<<"\"";}};
if(m.hasLightmap)png("lightmap",m.lmRGBA,m.lmW,m.lmH);if(m.hasOrm)png("orm",m.ormRGBA,m.ormW,m.ormH);
if(m.uvs2.size()==m.positions.size()/3*2){std::string fn="uv1_"+std::to_string(i)+".bin";std::ofstream f(std::string(argv[2])+"/"+fn,std::ios::binary);f.write((const char*)m.uvs2.data(),m.uvs2.size()*4);meta<<",\"uv1\":\""<<fn<<"\"";}meta<<"}";}
meta<<"]";fprintf(stderr,"Loaded %zu meshes\n",l.meshes.size());return gltfexport::exportEnv(l.meshes,argv[2],"scene")?0:4;}
