import java.io.*;
import java.util.*;

public class Solution {
    
    static boolean isWeirdEqual(int[] a, int[] b){
        /*
         Your recusive solution goes here.   
         */
		int n = a.length;                                       
        if (n%2 != 0) {                                         
            return Arrays.equals(a,b);                         
        } 
        int[] A1 = Arrays.copyOfRange(a,0, n/2);           
        int[] B1 = Arrays.copyOfRange(b, 0, n/2);        
        int[] A2 = Arrays.copyOfRange(a, n/2, n);             
        int[] B2 = Arrays.copyOfRange(b, n/2, n);   
        
        boolean A2_B2 = isWeirdEqual(A2, B2);
    
        return (isWeirdEqual(A1, B1) && (A2_B2 || isWeirdEqual(A1, B2))) || (A2_B2 && (isWeirdEqual(A2,B1)));
    }
    

    public static void main(String[] args) {
        /* Read input from STDIN. Print output to STDOUT. Your class should be named Solution. 

	You should be able to compile your program with the command:
   
		javac Solution.java
	
   	To conveniently test your algorithm, you can run your solution with any of the tester input files using:
   
		java Solution inputXX.txt
	
	where XX is 00, 01, ..., 13.
	*/

   	Scanner s;
	if (args.length > 0){
		try{
			s = new Scanner(new File(args[0]));
		} catch(java.io.FileNotFoundException e){
			System.out.printf("Unable to open %s\n",args[0]);
			return;
		}
		System.out.printf("Reading input values from %s.\n",args[0]);
	}else{
		s = new Scanner(System.in);
		System.out.printf("Reading input values from stdin.\n");
	}     
  
        int n = s.nextInt();
        int[] a = new int[n];
        int[] b = new int[n];
        
        for(int j = 0; j < n; j++){
            a[j] = s.nextInt();
        }
        
        for(int j = 0; j < n; j++){
            b[j] = s.nextInt();
        }
        
        System.out.println((isWeirdEqual(a, b) ? "YES" : "NO"));
    }
}