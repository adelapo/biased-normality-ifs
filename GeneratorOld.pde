//import java.util.Iterator;

abstract class GeneratorOld {
  int base;
  int len;
  String string;
   
  GeneratorOld(int base, int len) {
    this.len = len;
    this.base = base;
    
    // string = compute();
  }
  
  abstract String compute();
  
  String get(int index) {
    return str(string.charAt(index));
  }
}
