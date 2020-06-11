class IteratedFunctionSystem {
  AffineTransformation[] transformations;
  float[] probabilities;
  
  int size;
  
  IteratedFunctionSystem(AffineTransformation[] transformations, float[] probabilities) {
    this.transformations = transformations;
    this.probabilities = probabilities;
    
    size = probabilities.length;
  }
  
  Coordinate2D nextStage(Coordinate2D currentCoord, int transformationIndex) {
    Coordinate2D result = transformations[transformationIndex].transform(currentCoord);
    result.transformation = transformationIndex;
    return result;
  }
  
  Coordinate2D nextStageRandom(Coordinate2D currentCoord) {
    float prob = 0.0;
    float randomNumber = random(1.0);
    for (int i = 0; i < size; i++) {
      prob += probabilities[i];
      
      if (randomNumber < prob) {
        return nextStage(currentCoord, i);
      }
    }
    return nextStage(currentCoord, size - 1);  // This should never happen
  }
}
