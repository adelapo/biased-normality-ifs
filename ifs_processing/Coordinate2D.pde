class Coordinate2D {
  float x;
  float y;
  
  int transformation;
   
  Coordinate2D(float x, float y, int transformation) {
    this.x = x;
    this.y = y;
    
    this.transformation = transformation;
  }
  
  Coordinate2D(float x, float y) {
    this(x, y, -1);
  }
  
  Coordinate2D generalMidpoint(Coordinate2D coord1, Coordinate2D coord2, float fraction) {
    float newX = coord1.x + (fraction * (coord2.x - coord1.x));
    float newY = coord1.y + (fraction * (coord2.y - coord1.y));
    
    return new Coordinate2D(newX, newY);
  }
  
  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (!(o instanceof Coordinate2D)) {
      return false;
    }
    
    Coordinate2D other = (Coordinate2D) o;
    
    return x == other.x && y == other.y;  
  }
}
