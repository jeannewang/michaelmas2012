import java.util.Random;
import java.io.*;
import java.math.BigInteger;
import java.util.HashSet;
import java.util.Iterator;
import java.nio.ByteBuffer;

class DESPrac
{
	public static byte[] toByteArray(double value) {
	    byte[] bytes = new byte[8];
	    ByteBuffer.wrap(bytes).putDouble(value);
	    return bytes;
	}
	
    public static void main(String[] args) throws IOException
    {
        long testP=0x1234567887654321L;
        long testK=0x33333333333333L;
        
        long testC=TwoRoundModifiedDES(testK,testP);
        System.out.println("c: 0x"+Long.toHexString(testC));
        
        long startTime=System.nanoTime();
        for (int i=0;i<1000;i++)
        {
        	TwoRoundModifiedDES(testK,testP);
        }
        long endTime=System.nanoTime();
        
        long time1000=(endTime-startTime);
        System.out.println("Time for 1000 iterations:"+time1000+"ns");
        
        BigInteger a= new BigInteger("2").pow(45);
        BigInteger b=new BigInteger("10").pow(9);
        BigInteger c=new BigInteger(toByteArray(d));
        System.out.println("Time for 2^55 iterations:" + a.multiply(new BigInteger(String.valueOf(time1000))).divide(b).divide(new BigInteger("31536000")) + " years");
        
    }

    static void differentialDistributionTable (int SBoxNumber)
    {
        // ...
    }

    // constants for &-ing with, to mask off everything but the bottom 32- or 48-bits of a long
    static long MASK32 = 0xffffffffL;
    static long MASK48 = 0xffffffffffffL;

    static long TwoRoundModifiedDES(long K, long P) // input is a 56-bit key "long" and a 64-bit plaintext "long", returns the ciphertext
    {
        long L0=(P>>32)&MASK32; // watch out for the sign extension!
        long R0=P&MASK32;
        long K1=K&MASK48;
        long K2=(K>>8)&MASK48;
        
        long L1=R0;
        long R1=L0^Feistel(R0, K1);

        long L2=R1;
        long R2=L1^Feistel(R1, K2);

        long C=L2<<32 | R2;

        return(C);
    }

    static long Feistel(long R, long K) // input is a 32-bit integer and 48-bit key, both stored in 64-bit signed "long"s; returns the output of the Feistel round
    {
        long K_=K&MASK32;
        long P=PBox(SBox((EBox(R)^K)));
        long F=P^K_;
        
    	return(F);
    }

    // NB: these differ from the tables in the DES standard because the latter are encoded in a strange order

    static final byte[] S1Table={
     3,  7,  5,  1, 12,  8,  2, 11, 10,  3, 15,  6,  7, 12,  8,  2,
    13,  0, 11,  4,  6,  5,  1, 14,  0, 10,  4, 13,  9, 15, 14,  9,
     4,  1,  2, 12, 11, 14, 15,  5, 14,  7,  8,  3,  1,  8,  5,  6,
     9, 15, 12, 10,  0, 11, 10,  0, 13,  4,  7,  9,  6,  2,  3, 11,
    };

    static final byte[] S2Table={
    13,  1,  2, 15,  8, 13,  4,  8,  6, 10, 15,  3, 11,  7,  1,  4,
    10, 12,  9,  5,  3,  6, 14, 11,  5,  0,  0, 14, 12,  9,  7,  2,
     7,  2, 11,  1,  4, 14,  1,  7,  9,  4, 12, 10, 14,  8,  2, 13,
     0, 15,  6, 12, 10,  9, 13,  0, 15,  3,  3,  5,  5,  6,  8, 11,
    };

    static final byte[] S3Table={
    14,  0,  4, 15, 13,  7,  1,  4,  2, 14, 15,  2, 11, 13,  8,  1,
     3, 10, 10,  6,  6, 12, 12, 11,  5,  9,  9,  5,  0,  3,  7,  8,
     4, 15,  1, 12, 14,  8,  8,  2, 13,  4,  6,  9,  2,  1, 11,  7,
    15,  5, 12, 11,  9,  3,  7, 14,  3, 10, 10,  0,  5,  6,  0, 13,
    };

    static final byte[] S4Table={
    10, 13,  0,  7,  9,  0, 14,  9,  6,  3,  3,  4, 15,  6,  5, 10,
     1,  2, 13,  8, 12,  5,  7, 14, 11, 12,  4, 11,  2, 15,  8,  1,
    13,  1,  6, 10,  4, 13,  9,  0,  8,  6, 15,  9,  3,  8,  0,  7,
    11,  4,  1, 15,  2, 14, 12,  3,  5, 11, 10,  5, 14,  2,  7, 12,
    };

    static final byte[] S5Table={
     7, 13, 13,  8, 14, 11,  3,  5,  0,  6,  6, 15,  9,  0, 10,  3,
     1,  4,  2,  7,  8,  2,  5, 12, 11,  1, 12, 10,  4, 14, 15,  9,
    10,  3,  6, 15,  9,  0,  0,  6, 12, 10, 11,  1,  7, 13, 13,  8,
    15,  9,  1,  4,  3,  5, 14, 11,  5, 12,  2,  7,  8,  2,  4, 14,
    };

    static final byte[] S6Table={
     2, 14, 12, 11,  4,  2,  1, 12,  7,  4, 10,  7, 11, 13,  6,  1,
     8,  5,  5,  0,  3, 15, 15, 10, 13,  3,  0,  9, 14,  8,  9,  6,
     4, 11,  2,  8,  1, 12, 11,  7, 10,  1, 13, 14,  7,  2,  8, 13,
    15,  6,  9, 15, 12,  0,  5,  9,  6, 10,  3,  4,  0,  5, 14,  3,
    };

    static final byte[] S7Table={
    12, 10,  1, 15, 10,  4, 15,  2,  9,  7,  2, 12,  6,  9,  8,  5,
     0,  6, 13,  1,  3, 13,  4, 14, 14,  0,  7, 11,  5,  3, 11,  8,
     9,  4, 14,  3, 15,  2,  5, 12,  2,  9,  8,  5, 12, 15,  3, 10,
     7, 11,  0, 14,  4,  1, 10,  7,  1,  6, 13,  0, 11,  8,  6, 13,
    };

    static final byte[] S8Table={
     4, 13, 11,  0,  2, 11, 14,  7, 15,  4,  0,  9,  8,  1, 13, 10,
     3, 14, 12,  3,  9,  5,  7, 12,  5,  2, 10, 15,  6,  8,  1,  6,
     1,  6,  4, 11, 11, 13, 13,  8, 12,  1,  3,  4,  7, 10, 14,  7,
    10,  9, 15,  5,  6,  0,  8, 15,  0, 14,  5,  2,  9,  3,  2, 12,
    };

    // STables[i-1][s] is the output for input s to S-box i
    static final byte[][] STables={S1Table, S2Table, S3Table, S4Table, S5Table, S6Table, S7Table, S8Table};

    static long SBox(long S) // input is a 48-bit integer stored in 64-bit signed "long"
    {
        // Split I into eight 6-bit chunks
        int Sa=(int)((S>>42));
        int Sb=(int)((S>>36)&63);
        int Sc=(int)((S>>30)&63);
        int Sd=(int)((S>>24)&63);
        int Se=(int)((S>>18)&63);
        int Sf=(int)((S>>12)&63);
        int Sg=(int)((S>>6)&63);
        int Sh=(int)(S&63);
        // Apply the S-boxes
        byte Oa=S1Table[Sa];
        byte Ob=S2Table[Sb];
        byte Oc=S3Table[Sc];
        byte Od=S4Table[Sd];
        byte Oe=S5Table[Se];
        byte Of=S6Table[Sf];
        byte Og=S7Table[Sg];
        byte Oh=S8Table[Sh];
        // Combine answers into 32-bit output stored in 64-bit signed "long"
        long O=(long)Oa<<28 | (long)Ob<<24 | (long)Oc<<20 | (long)Od<<16 | (long)Oe<<12 | (long)Of<<8 | (long)Og<<4 | (long)Oh;
        return(O);
    }

    static long EBox(long R) // input is a 32-bit integer stored in 64-bit signed "long"
    {
        // compute each 6-bit component
        long Ea=(R>>27)&31 | (R&1)<<5;
        long Eb=(R>>23)&63;
        long Ec=(R>>19)&63;
        long Ed=(R>>15)&63;
        long Ee=(R>>11)&63;
        long Ef=(R>>7)&63;
        long Eg=(R>>3)&63;
        long Eh=(R>>31)&1 | (R&31)<<1;
        // 48-bit output stored in 64-bit signed "long"
        long E=(long)Ea<<42 | (long)Eb<<36 | (long)Ec<<30 | (long)Ed<<24 | (long)Ee<<18 | (long)Ef<<12 | (long)Eg<<6 | (long)Eh;
        return(E);
    }

    static final int[] Pbits={
    16,  7, 20, 21,
    29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11,  4, 25
    };

    // this would have been a lot faster as fixed binary operations rather than a loop
    static long PBox(long O) // input is a 32-bit integer stored in 64-bit signed "long"
    {
        long P=0L;
        for(int i=0; i<32; i++)
        {
            P|=((O>>(32-Pbits[i]))&1) << (31-i);
        }
        return(P);
    }

    // a helper method to call the external programme "encrypt" in the current directory
    // the parameter is the 64-bit plaintext to encrypt, returns the ciphertext
    static long callEncrypt(long P) throws IOException
    {
        Process process = Runtime.getRuntime().exec("./encrypt "+Long.toHexString(P));
        String CString = (new BufferedReader(new InputStreamReader(process.getInputStream()))).readLine();

        // we have to go via BigInteger otherwise the signed longs cause incorrect parsing
        long C=new BigInteger(CString, 16).longValue();

        return(C);
    }

}
