class SampleGenerators {
  class UniformRandomGenerator extends Generator {
    UniformRandomGenerator(int base) {
      super(base);
      currentNumber = int(random(base));
      currentNumberString = Integer.toString(currentNumber, base);
    }
    
    int nextNumber() {
      return int(random(base));
    }
  }
  
  class Champernowne extends Generator {
    Champernowne(int base) {
      super(base); 
    }
    
    int nextNumber() {
      return currentNumber + 1; 
    }
  }
  
  class RandomGenerator extends Generator {
    float[] biases;
    
    RandomGenerator(float[] biases) {
      super(biases.length);
      this.biases = biases;
    }
    
    int nextNumber() {
      float prob = 0.0;
      float randomNumber = random(1.0);
      
      for (int i = 0; i < biases.length; i++) {
        prob += biases[i];
        if (randomNumber < prob) {
          return i;
        }
      }
      
      return biases.length - 1;
    }
  }
  
  class LimitedChampernowne extends Generator {
    int limitLength;
    
    LimitedChampernowne(int base, int limitLength) {
      super(base);
      this.limitLength = limitLength;
    }
    
    int nextNumber() {
      int nextNum = currentNumber + 1;
      
      if (Integer.toString(nextNum, base).length() > limitLength) {
        nextNum = 0; 
      }
      
      return nextNum;
    } //<>//
  }
  
  class CopelandErdos extends Generator {
    CopelandErdos(int base) {
      super(base);
      
      currentNumber = 2;
      currentNumberString = Integer.toString(currentNumber, 2);
    }
    
    boolean isPrime(int n) {
      for (int i = 2; i < sqrt(n); i++) {
        if (n % i == 0) {
          return false; 
        }
      }
      return true;
    }
    
    int nextNumber() {
      int nextNum = currentNumber + 1;
      while (!isPrime(nextNum)) {
        nextNum++;
      }
      return nextNum;
    }
  }
  
  class BiasedNormal extends Generator {
    int[] probNumerators;
    int[] probDenominators;
    Generator normalGenerator;
    
    int d;
    
    String g;
    
    BiasedNormal(int[] probNumerators, int[] probDenominators) {
      super(probNumerators.length);
      this.probNumerators = probNumerators;
      this.probDenominators = probDenominators;
      
      d = lowestCommonMultiple(probDenominators);
      
      this.normalGenerator = new Champernowne(d);
      
      StringBuilder gBuilder = new StringBuilder();
      
      for (int i = 0; i < probNumerators.length; i++) {
        for (int j = 0; j < probNumerators[i] * (d / probDenominators[i]); j++) {
          gBuilder.append(Integer.toString(i, probNumerators.length)); 
        }
      }
      
      g = gBuilder.toString();
      println("g = " + g);
    }
    
    int nextNumber() {
      String nextInNormSeq = normalGenerator.next();     
      int index = Integer.parseInt(nextInNormSeq, d);      
      String gAtIndex = Character.toString(g.charAt(index));
     
      int nextNum = Integer.parseInt(gAtIndex, base);
      return nextNum;
    }
    
    int lowestCommonMultiple(int[] numbers) {
      // First, find max
      int maxNum = numbers[0];
      
      for (int number : numbers) {
        if (number > maxNum) {
          maxNum = number; 
        }
      }
      
      boolean allDivide;
      
      int ans = maxNum;
      
      while (true) {
         allDivide = true;
         for (int number : numbers) {
           allDivide = allDivide && (ans % number == 0);
         }
         
         if (allDivide) {
           return ans; 
         }

         ans += maxNum;
      }
    }
  }
}
