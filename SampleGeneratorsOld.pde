//class SampleGenerators {
//  class UniformRandomGenerator extends Generator {
//    UniformRandomGenerator(int base, int len) {
//      super(base, len);
//    }
    
//    String compute() {
//      StringBuilder result = new StringBuilder();
      
//      for (int i = 0; i < len; i++) {
//        result.append(int(random(base)));
//      }
       
//      string = result.toString();
//      return string;
//    }
//  }
  
//  class ChampernowneIterator extends GeneratorIterator {
//    int base;
//    int currentNum;
//    String currentNumStr;
//    int currentNumIndex;
    
//    ChampernowneIterator(int base) {
//      super();
//      this.base = base;
//      this.currentNum = 0;
//      this.currentNumIndex = 0;
      
//      this.currentNumStr = Integer.toString(currentNum, base);
//    }
    
//    String next() {
//      if (currentNumIndex >= currentNumStr.length()) {
//        currentNum++;
//        currentNumIndex = 0;
//        currentNumStr = Integer.toString(currentNum, base);
//      }
      
//      String nextString = Character.toString(currentNumStr.charAt(currentNumIndex));
//      currentNumIndex++;
      
//      return nextString;
//    }
//  }
  
//  class RandomGenerator extends Generator {
//    float[] biases;
    
//    RandomGenerator(float[] biases, int len) {
//      super(biases.length, len);
//      this.biases = biases;
//    }
    
//    String compute() {
//      StringBuilder result = new StringBuilder();
      
//      while (result.length() < len) {
//        result.append(biasedRandom());
//      }
      
//      string = result.toString();
      
//      return string;
//    }
    
//    String biasedRandom() {
//      float prob = 0.0;
//      float randomNumber = random(1.0);
      
//      for (int i = 0; i < biases.length; i++) {
//        prob += biases[i];
//        if (randomNumber < prob) {
//          return Integer.toString(i, biases.length);
//        }
//      }
      
//      return Integer.toString(biases.length - 1);
//    }
//  }
  
//  class Champernowne extends Generator {
//    Champernowne(int base, int len) {
//      super(base, len); 
//    }
    
//    String compute() {
//      StringBuilder result = new StringBuilder();
//      int i = 0;
//      while (result.length() < len) {
//        result.append(dec2base(i, base));
//        i++;
//      }
      
//      string = result.toString();
//      return string;
//    }
//  }
  
//  class LimitedChampernowne extends Generator {
//    int limit;
    
//    LimitedChampernowne(int base, int len, int limit) {
//      super(base, len);
//      this.limit = limit;
//    }
    
//    String compute() {
//      StringBuilder result = new StringBuilder();
//      int i = 0;
//      StringBuilder currentSequence;
      
//      while (result.length() < len) {
//        currentSequence = new StringBuilder();
//        currentSequence.append(dec2base(i, base));
        
//        if (currentSequence.length() > limit) {
//          i = 0;
//          currentSequence = new StringBuilder();
//          currentSequence.append(dec2base(i, base));
//        }
        
//        //while (currentSequence.length() < limit) {
//        //  currentSequence.insert(0, "0");
//        //}
        
//        result.append(currentSequence);
//        i++;
//      }
      
//      string = result.toString();
//      return string;
//    }
//  }
  
//  class CopelandErdos extends Generator {
//    CopelandErdos(int base, int len) {
//      super(base, len); 
//    }
    
//    boolean isPrime(int n) {
//      for (int i = 2; i < sqrt(n); i++) {
//        if (n % i == 0) {
//          return false; 
//        }
//      }
//      return true;
//    }
    
//    String compute() {
//      StringBuilder result = new StringBuilder();
      
//      int i = 2;
      
//      while (result.length() < len) {
//         if (isPrime(i)) {
//           result.append(dec2base(i, base)); 
//         }
//         i++;
//      }
      
//      string = result.toString();      
//      return string;
//    }
//  }
  
  
//  class BiasedNormal extends Generator {
//    // Uses Champernowne's sequence to produce a biased normal sequence
//    int[] probNumerators;
//    int[] probDenominators;
    
//    BiasedNormal(int[] probNumerators, int[] probDenominators, int len) {
//      super(probNumerators.length, len);
            
//      this.probNumerators = probNumerators;
//      this.probDenominators = probDenominators;
//    }
    
//    String compute() {
//      int d = lowestCommonMultiple(probDenominators);
      
//      StringBuilder result = new StringBuilder();
      
//      StringBuilder gBuilder = new StringBuilder();
      
//      Generator c_d = new SampleGenerators.CopelandErdos(d, len);
//      c_d.compute();
      
//      for (int i = 0; i < probNumerators.length; i++) {
//        for (int j = 0; j < probNumerators[i] * (d / probDenominators[i]); j++) {
//          gBuilder.append(Integer.toString(i, probNumerators.length)); 
//        }
//      }
      
//      String g = gBuilder.toString();
//      println("g = " + g);
      
//      for (int i = 0; i < len; i++) {
//        String champernowneIndexStr = Character.toString(c_d.string.charAt(i));
//        int champernowneIndex = Integer.parseInt(champernowneIndexStr, d);
//        String gAtIndex = Character.toString(g.charAt(champernowneIndex));
        
//        //result.append(Character.toString(g.charAt(Integer.parseInt(Character.toString(c_d.string.charAt(i)), d))));
        
//        result.append(gAtIndex);
//      }
      
//      string = result.toString();
//      return string;
//    }
    
//    int lowestCommonMultiple(int[] numbers) {
//      // First, find max
//      int maxNum = numbers[0];
      
//      for (int number : numbers) {
//        if (number > maxNum) {
//          maxNum = number; 
//        }
//      }
      
//      boolean allDivide;
      
//      int ans = maxNum;
      
//      while (true) {
//         allDivide = true;
//         for (int number : numbers) {
//           allDivide = allDivide && (ans % number == 0);
//         }
         
//         if (allDivide) {
//           return ans; 
//         }

//         ans += maxNum;
//      }
//    }
//  }
//}
