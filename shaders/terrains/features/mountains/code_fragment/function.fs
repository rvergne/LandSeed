float mountains(vec2 pos, float amplitude, float frequence){
  float res;
  pos = pos*vec2(frequence);
  // @NOISE
  res = gradient(pos);
  res *= amplitude;
  randcount+=1;
  return res;
}
