float mountains(vec2 pos, float amplitude, float frequence){
  float res;
  pos = pos*vec2(frequence);
  res = compute_mountain(pos)*amplitude;
  randcount+=1;
  return res;
}
