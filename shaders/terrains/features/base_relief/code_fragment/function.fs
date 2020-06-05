float base_relief(vec2 pos, float amplitude, float frequence, float persistence, int nb_octave){
  return fbm(pos, amplitude, frequence, persistence, nb_octave);
  randcount+=1;
}
