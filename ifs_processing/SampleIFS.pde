class SampleIFS {  
  class SierpinskiTriangle extends IteratedFunctionSystem {    
    SierpinskiTriangle() {
      super(new AffineTransformation[]{
        new AffineTransformation(0.5, 0, 0, 0.5, 0, 0),
        new AffineTransformation(0.5, 0, 0, 0.5, 0, 50),
        new AffineTransformation(0.5, 0, 0, 0.5, 50, 50)
      }, new float[]{1.0 / 3, 1.0 / 3, 1.0 / 3});
    }
  }
  
  class Square extends IteratedFunctionSystem {
    Square() {
      super(new AffineTransformation[]{
        new AffineTransformation(0.5, 0, 0, 0.5, 0, 0),
        new AffineTransformation(0.5, 0, 0, 0.5, 0, 50),
        new AffineTransformation(0.5, 0, 0, 0.5, 50, 50),
        new AffineTransformation(0.5, 0, 0, 0.5, 50, 0)
      }, new float[]{0.25, 0.25, 0.25, 0.25});
    }
  }
  
  class BarnsleyFern extends IteratedFunctionSystem {
    BarnsleyFern() {
      super(new AffineTransformation[]{
        new AffineTransformation(0, 0, 0, 0.16, 0, 0),
        new AffineTransformation(0.85, 0.04, -0.04, 0.85, 0, 1.6),
        new AffineTransformation(0.2, -0.26, 0.23, 0.22, 0, 1.6),
        new AffineTransformation(-0.15, 0.28, 0.26, 0.24, 0, 0.44)
      }, new float[]{0.01, 0.85, 0.07, 0.07});
    }
  }
  
  class FractalTree extends IteratedFunctionSystem {
    FractalTree() {
      super(new AffineTransformation[]{
        new AffineTransformation(0, 0, 0, 0.5, 0, 0),
        new AffineTransformation(0.42, -0.42, 0.42, 0.42, 0, 0.2),
        new AffineTransformation(0.42, 0.42, -0.42, 0.42, 0, 0.2),
        new AffineTransformation(0.1, 0, 0, 0.1, 0, 0.2)
      }, new float[]{0.05, 0.4, 0.4, 0.15});
    }
  }
  
  class MUSAFractal extends IteratedFunctionSystem {
    int previousTransformationIndex = 0;
    
    MUSAFractal() {
      super(new AffineTransformation(0, 0, 0, 0, 0, 0).nFlakeMidpointTransformations(6, width/2, 0.5),
            new float[]{0.25, 0.25, 0.25, 0.25, 0.25, 0.25});
            
      size = 4;
    }
    
    @Override
    Coordinate2D nextStage(Coordinate2D currentCoord, int transformationIndex) { //<>// //<>//
      int[] validIndices = new int[4];
      int count = 0;
      for (int i = 0; i < 6; i++) {
        if (i % 3 != previousTransformationIndex % 3) {
          validIndices[count] = i;
          count++;
        }
      }
      previousTransformationIndex = validIndices[transformationIndex];
      Coordinate2D result = transformations[previousTransformationIndex].transform(currentCoord);
      result.transformation = previousTransformationIndex;
      return result;
    }
    
    @Override
    Coordinate2D nextStageRandom(Coordinate2D currentCoord) {
       int transformationIndex = int(random(4));
       return nextStage(currentCoord, transformationIndex);
    }
  }
}
