import java.util.Map;
import java.util.Collections;

IteratedFunctionSystem IFS;
SampleIFS samples;
Coordinate2D coord;

ArrayList<Coordinate2D> fractal;

IntList fractalXcoords;
IntList fractalYcoords;

PImage fractalImage;
PImage measureImage;

int numIterations = 1000000;

boolean useGenerator = true;

// Pan and zoom variables
float zoomScale = 1;
float xPan;
float yPan;

float initialMouseX;
float initialMouseY;

int fractalImageWidth;
int fractalImageHeight;

color backgroundColor;

boolean drawMeasure;

void setup() {
  size(800, 800);
  stroke(0, 255, 0);
  colorMode(HSB, 360, 100, 100);
  
  xPan = width / 2;
  yPan = height / 2;
  
  drawMeasure = false;
  
  initialMouseX = 0;
  initialMouseY = 0;
  
  backgroundColor = color(0, 0, 0);
  
  background(backgroundColor);  
  imageMode(CENTER);
  
  SampleIFS sampleIFS = new SampleIFS();
  SampleGenerators generators = new SampleGenerators();
  
  // Set the iterated function system here
  IFS = sampleIFS.new Square();
  
  // Set the generator here (used only when useGenerator is true)
  Generator generator = generators.new CopelandErdos(IFS.size); //<>//
  
  print("Computing fractal... ");
  
  if (useGenerator) {  // Set this flag at top of this file
    fractal = runIFSwithGenerator(IFS, generator);
  } else {
    fractal = runIFSwithProbabilities(IFS); 
  }
  
  println("done.");
  
  print("Creating image... ");
  fractalImage = fractal2Image(fractal, IFS.size);
  
  fractalImageWidth = fractalImage.width;
  fractalImageHeight = fractalImage.height;
  
  println("done.");
  
  print("Creating measure viualization... ");
  measureImage = measureVisualization(fractal);
  
  println("done.");
  
  print("Fitting fractal width to screen width... ");
  
  if (fractalImage.width > fractalImage.height) {
    zoom(width / fractalImage.width);
  } else {
    zoom(height / fractalImage.height);
  }
    
  println("done.");
}

void draw() {
  background(backgroundColor);
  
  if (drawMeasure) {
    image(measureImage, xPan, yPan);
  } else {
    image(fractalImage, xPan, yPan);
  }
}

void mousePressed() {
  initialMouseX = mouseX;
  initialMouseY = mouseY;
}

void mouseDragged() {
  xPan += mouseX - initialMouseX;
  yPan += mouseY - initialMouseY;
  
  initialMouseX = mouseX;
  initialMouseY = mouseY;
}

void mouseWheel(MouseEvent event) {
  float scrollDirection = event.getCount();  // -1 = UP, +1 = DOWN
  
  if (scrollDirection > 0) {
    zoom(2.0 / 3);
  } else {
    zoom(1.5);
  }
}

void keyPressed() {
  if (key == 's' || key == 'f' || key == 'g') {
    int[] times = new int[]{year(), month(), day(), hour(), minute(), second()};
    String[] timesStr = new String[6];
    for (int i = 0; i < times.length; i++) {
      timesStr[i] = Integer.toString(times[i]);
      if (timesStr[i].length() < 2) {
        timesStr[i] = "0" + timesStr[i];
      }
    }
    if (key == 's') {
      String fileName = "screenshots/screenshot_" + times[0] + times[1] + times[2] + "_" + times[3] + times[4] + times[5] + ".png";
      println("Saved screenshot as " + fileName);
      saveFrame(fileName);
    } else if (key == 'f') {
      String fileName = "screenshots/fractal_" + times[0] + times[1] + times[2] + "_" + times[3] + times[4] + times[5] + ".png";
      println("Saved fractal as " + fileName);
      fractalImage.save(fileName);
    } else if (key == 'g') {
      String fileName = "screenshots/measure_" + times[0] + times[1] + times[2] + "_" + times[3] + times[4] + times[5] + ".png";
      println("Saved measure as " + fileName);
      measureImage.save(fileName);
    }
  }
  
  if (keyCode == UP) {
    zoom(1.5);
  }
  if (keyCode == DOWN) {
    zoom(2.0 / 3); 
  }
  
  if (key == 'm') {
    drawMeasure = true; 
  }

}

void keyReleased() {
  if (key == 'm') {
    drawMeasure = false; 
  }
}

void zoom(float scale) {
  zoomScale *= scale;
  
  for (Coordinate2D coord : fractal) {
    coord.x *= scale;
    coord.y *= scale;
  }
  
  fractalImage = fractal2Image(fractal, IFS.size);
  measureImage = measureVisualization(fractal);
}


void drawCoord(Coordinate2D coord) {
   point(coord.x, coord.y);
}

ArrayList<Coordinate2D> runIFSwithProbabilities(IteratedFunctionSystem ifs) {
  ArrayList<Coordinate2D> result = new ArrayList();
  
  // Coordinate2D coord = new Coordinate2D(random(width), random(height));
  Coordinate2D coord = new Coordinate2D(0, 0);
  
  for (int i = 0; i < numIterations; i++) {
    coord = ifs.nextStageRandom(coord);    
    result.add(coord);
  }
  
  return result;
}

ArrayList<Coordinate2D> runIFSwithGenerator(IteratedFunctionSystem ifs, Generator gen) {
  int transformationIndex;
  
  ArrayList<Coordinate2D> result = new ArrayList();
  
  // Coordinate2D coord = new Coordinate2D(random(width), random(height));
  Coordinate2D coord = new Coordinate2D(0, 0);
  
  for (int i = 0; i < numIterations; i++) {
    transformationIndex = Integer.parseInt(gen.next());
    coord = ifs.nextStage(coord, transformationIndex);
    
    result.add(coord);
    
    if (i % 1000000 == 0) {
      println((100.0 * i / numIterations) + "% through runIFSwithGenerator"); 
    }
  }
  
  return result;
}

String dec2base(int num, int toBase) {
  return Integer.toString(num, toBase);
}

PImage fractal2Image(ArrayList<Coordinate2D> fractal, int numTransformations) {  
  IntList xCoords = new IntList();
  IntList yCoords = new IntList();
  
  for (Coordinate2D coord : fractal) {
    xCoords.append(int(coord.x));
    yCoords.append(int(coord.y));
  }
  
  int minX = xCoords.min();
  int maxX = xCoords.max();
  int minY = yCoords.min();
  int maxY = yCoords.max();
  
  int imageWidth = maxX - minX + 1;
  int imageHeight = maxY - minY + 1;
  
  PImage result = createImage(imageWidth, imageHeight, HSB);
  result.loadPixels();
  
  for (int i = 0; i < result.pixels.length; i++) {
    result.pixels[i] = backgroundColor;
  }
  
  result.updatePixels();
  
  result.loadPixels();
  
  int x, y;
  
  int pixelIndex;
  float pixelHue;
  
  for (Coordinate2D coord: fractal) {
    x = int(coord.x);
    y = int(coord.y);
    
    pixelIndex = ((y - minY) * imageWidth) + (x - minX);
    if (coord.transformation == -1) {
      result.pixels[pixelIndex] = color(120, 100, 100);
    } else {
      pixelHue = map(coord.transformation, 0, numTransformations, 0, 360);
      result.pixels[pixelIndex] = color(pixelHue, 100, 100);
    }
  }
  
  result.updatePixels();
  
  return result;
}

PImage measureVisualization(ArrayList<Coordinate2D> fractal) {
  IntList xCoords = new IntList();
  IntList yCoords = new IntList();
  
  for (Coordinate2D coord : fractal) {
    xCoords.append(int(coord.x));
    yCoords.append(int(coord.y));
  }
  
  int minX = xCoords.min();
  int maxX = xCoords.max();
  int minY = yCoords.min();
  int maxY = yCoords.max();
  
  int imageWidth = maxX - minX + 1;
  int imageHeight = maxY - minY + 1;
  
  PImage result = createImage(imageWidth, imageHeight, HSB);
  result.loadPixels();
  
  for (int i = 0; i < result.pixels.length; i++) {
    result.pixels[i] = backgroundColor;
  }
  
  result.updatePixels();
  
  result.loadPixels();
  
  int x, y;
  
  int pixelIndex;
  int pixelCount;
  
  float pixelHue;
  
  HashMap<Integer, Integer> pixelIndexMap = new HashMap<Integer, Integer>();
  
  for (Coordinate2D coord: fractal) {
    x = int(coord.x);
    y = int(coord.y);
    
    
    
    pixelIndex = ((y - minY) * imageWidth) + (x - minX);
    if (pixelIndexMap.containsKey(pixelIndex)) {
      pixelIndexMap.put(pixelIndex, pixelIndexMap.get(pixelIndex) + 1);
    } else {
      pixelIndexMap.put(pixelIndex, 1); 
    }
  }
  
  // Find max pixelCount  
  int maxPixelIndex = 0;
  int maxPixelCount = -1;
  
  int minPixelCount = numIterations + 1;
  
  for (Map.Entry<Integer, Integer> index : pixelIndexMap.entrySet()) {
    pixelIndex = index.getKey();
    pixelCount = index.getValue();
    
    if (pixelCount > maxPixelCount) {
      maxPixelCount = pixelCount;
      maxPixelIndex = pixelIndex;
    }
    
    if (pixelCount < minPixelCount) {
      minPixelCount = pixelCount; 
    }
  }
  
  println("\nminPixelCount: " + minPixelCount);
  println("maxPixelCount: " + maxPixelCount);
  println("pixelIndexMap.size(): " + pixelIndexMap.size());
  
  for (Map.Entry<Integer, Integer> index : pixelIndexMap.entrySet()) {
    pixelIndex = index.getKey();
    pixelCount = index.getValue();
    
    //pixelHue = map(pixelCount * zoomScale * zoomScale, 0, numIterations, 0, 360);
    pixelHue = map(pixelCount, minPixelCount, maxPixelCount, 0, 330);
    //if (pixelIndex < 10) {
    //  println("pixelHue: " + pixelHue);
    //}
    
    result.pixels[pixelIndex] = color(pixelHue, 100, 100);
  }
  
  result.updatePixels();
  
  return result;
}
