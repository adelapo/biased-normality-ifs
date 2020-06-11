import java.util.Iterator;

abstract class Generator implements Iterator<String> {
  int base;
  
  int currentNumber;
  int currentNumberIndex;
  String currentNumberString;
   
  Generator(int base) {
    this.base = base;
    
    currentNumber = 0;
    currentNumberIndex = 0;
    currentNumberString = "0";
  }
  
  boolean hasNext() {
    return true; 
  }
  
  String next() {
    String nextString = Character.toString(currentNumberString.charAt(currentNumberIndex));
    
    currentNumberIndex++;
    
    if (currentNumberIndex >= currentNumberString.length()) {
      currentNumberIndex = 0;
      currentNumber = nextNumber();
      currentNumberString = Integer.toString(currentNumber, base);
    }
    
    return nextString;
  }
  
  abstract int nextNumber();
}

//abstract class GeneratorIterator implements Iterator<String> {  
//  boolean hasNext() {
//    return true;
//  }
//}
