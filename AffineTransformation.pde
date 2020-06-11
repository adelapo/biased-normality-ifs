class AffineTransformation {
  // Barnsley, p. 86
  /* 
   _      _  _ _       _   _
  | a    b || x |     |  e  |
  |        ||   |  +  |     |
  | c    d || y |     |  f  |
   -      -  - -       -   -  
  */
  
  float a, b, c, d, e, f;
  
  AffineTransformation(float a, float b, float c, float d, float e, float f) {
    this.a = a;
    this.b = b;
    this.c = c;
    this.d = d;
    this.e = e;
    this.f = f;
  }
  
  Coordinate2D transform(Coordinate2D coord) {
    float u = a * coord.x + b * coord.y + e;
    float v = c * coord.x + d * coord.y + f;
    
    return new Coordinate2D(u, v);
  }
  
  AffineTransformation midpointTransform(Coordinate2D vertex, float r) {
    float a = 1 - r;
    float d = 1 - r;
    float e = r * vertex.x;
    float f = r * vertex.y;
    
    return new AffineTransformation(a, 0, 0, d, e, f);
  }
  
  AffineTransformation[] nFlakeMidpointTransformations(int n, float radius, float r) {
    AffineTransformation[] transformations = new AffineTransformation[n];
    
    float vertX;
    float vertY;
    
    for (int i = 0; i < n; i++) {
      vertX = width/2 + radius * cos(2 * PI * i / n);
      vertY = height/2 + radius * sin(2 * PI * i / n);
      transformations[i] = midpointTransform(new Coordinate2D(vertX, vertY), r);
    }
    
    return transformations;
  }
}
