from abc import ABCMeta, abstractmethod
from functools import reduce
import math
import random


class BasicTools:
    #the function of leting the SCIP file to each solution file
    def SCIP2Sol(solutionFile, outputfile):
        solFile = open(solutionFile,'r')
        goodFormat = list()
        variable_format=list()
        j=1
        for line in solFile:
            temp = line
            temp = temp.replace(',', ' ')

            temp = temp.split()
            print(temp[0])
            if line[0] == '#':
                variable_format = temp
            else:

                f = open(outputfile + str(j) + '.sol','w')
                for i in range(0, len(variable_format)):
                    f.write(variable_format[i] + ' ' + temp[i] + '\n')
                f.close()
                j=j+1
        solFile.close()

    
    @staticmethod
    def typeX(V):
        return [v + '_TypeX' for v in V]

    @staticmethod
    def typeY(V):
        return [v + '_TypeY' for v in V]

    @staticmethod
    def typeZ(V):
        return [v + '_TypeZ' for v in V]


    @staticmethod
    def transpose(M):
        """
        Transpose the matrix M
        >>> M = [[1,0,1,1],[1,0,0,0],[0,1,1,0],[1,0,1,0]]
        >>>
        >>> BasicTools.transpose(M)
        [[1, 1, 0, 1], [0, 0, 1, 0], [1, 0, 1, 1], [1, 0, 0, 0]]
        >>>
        >>>
        """
        m = len(M)
        n = len(M[0])

        Mt = []
        for i in range(0, n):
            row = [M[k][i] for k in range(0, m)]
            Mt.append(row)

        return Mt

    @staticmethod
    def plusTerm(in_vars):
        """
        >>> BasicTools.plusTerm(['x','y','z'])
        'x + y + z'
        >>> BasicTools.plusTerm(['x','y'])
        'x + y'
        >>> BasicTools.plusTerm(['x','y','z','a','b'])
        'x + y + z + a + b'
        >>>
        """
        t = ''
        for v in in_vars:
            t = t + v + ' + '

        return t[0:-3]

    @staticmethod
    def MinusTerm(in_vars):
        """
        >>> BasicTools.plusTerm(['x','y','z'])
        'x + y + z'
        >>> BasicTools.plusTerm(['x','y'])
        'x + y'
        >>> BasicTools.plusTerm(['x','y','z','a','b'])
        'x + y + z + a + b'
        >>>
        """
        t = ''
        for v in in_vars:
            t = t + v + ' - '

        return t[0:-3]

    @staticmethod
    def generalizedPermutation(in_vars, permTable):
        """
        Example:
            >>> BasicTools.generalizedPermutation(['x0','x1','x2'], [2,2,0,0,1,1])
            ['x2', 'x2', 'x0', 'x0', 'x1', 'x1']
            >>>
        """
        out = [None for i in range(0, len(permTable))]
        for j in range(0, len(permTable)):
            assert permTable[j] in range(0, len(in_vars)), "index value is not compatible with in variables!"
            out[j] = in_vars[permTable[j]]
        return out

    @staticmethod
    def leftRotation(in_vars, offset):
        assert offset < len(in_vars), "Are you rotating too much?"
        out = [None for i in range(0, len(in_vars))]
        if offset == 0:
            out[0:] = in_vars[0:]
        else:
            out[0:-offset] = in_vars[offset:]
        return out

    @staticmethod
    def rightRotation(in_vars, offset):
        assert offset < len(in_vars), "Are you rotating too much?"
        out = [None for i in range(0, len(in_vars))]
        if offset == 0:
            out[0:] = in_vars[0:]
        else:
            out[offset:] = in_vars[0:-offset]
        return out

    @staticmethod
    def leftCyclicRotation(in_vars, offset):
        out = [None for i in range(0, len(in_vars))]
        for i in range(0, len(in_vars)):
            out[i] = in_vars[(i+offset) % len(in_vars)]

        return out

    @staticmethod
    def rightCyclicRotation(in_vars, offset):
        out = [None for i in range(0, len(in_vars))]
        for i in range(0, len(in_vars)):
            out[i] = in_vars[(i-offset) % len(in_vars)]

        return out


    @staticmethod
    def dotProduct(x, y, size):
        """
        comput the dot product of to binary strings:
        dotProduct(0101, 1100, 4) = 0*1 + 1*1 + 0*0 + 1*0 = 1

        Example:
            >>> bin(15)
            '0b1111'
            >>> bin(11)
            '0b1011'
            >>> BasicTools.dotProduct(15, 11, 4)
            1
        """
        a = bin(x)[2:].zfill(size)
        b = bin(y)[2:].zfill(size)
        t = [int(a[i])&int(b[i]) for i in range(0, size)]
        return reduce((lambda x,y: x^y), t)



    @staticmethod
    def wordToBinaryString(word, size):
        """
        Example:
            >>> BasicTools.wordToBinaryString(0xF1, 8)
            '11110001'
        """
        return bin(word)[2:].zfill(size)

    @staticmethod
    def allVectorsOfDim(d):
        """
        compute the set of all vectors in space {0,1}^d
        Example:
            >>> BasicTools.allVectorsOfDim(3)
            {(0, 0, 0),
             (0, 0, 1),
             (0, 1, 0),
             (0, 1, 1),
             (1, 0, 0),
             (1, 0, 1),
             (1, 1, 0),
             (1, 1, 1)}
        """
        out = set({})
        for i in range(0, 2**d):
            s = bin(i)[2:].zfill(d)
            v = tuple([int(s[j]) for j in range(0, len(s))])
            out.add(v)

        return out

    @staticmethod
    def nonzeroVectorsOfDim(d):
        """
        Example:
            >>> BasicTools.nonzeroVectorsOfDim(3)
            {(0, 1, 1),
            (1, 1, 0),
            (1, 0, 0),
            (0, 0, 1),
            (1, 0, 1),
            (0, 1, 0),
            (1, 1, 1)}
        """
        return BasicTools.allVectorsOfDim(d) -{tuple(0 for i in range(0,d))}
    @staticmethod
    def zeroIn_NonzeroOut_Patterns(in_size, out_size):
        out = set({})
        for v in BasicTools.nonzeroVectorsOfDim(out_size):
            out.add(tuple([0 for i in range(0,in_size)] + list(v)))

        return out

    @staticmethod
    def nozeroIn_ZeroOut_Or_ZeroIn_NonzeroOut_Patterns(in_size, out_size):
        """
        Example:
            >>> BasicTools.nozeroIn_ZeroOut_Or_ZeroIn_NonzeroOut_Patterns(2,3)
            {(0, 0, 0, 0, 1),
             (0, 0, 0, 1, 0),
             (0, 0, 0, 1, 1),
             (0, 0, 1, 0, 0),
             (0, 0, 1, 0, 1),
             (0, 0, 1, 1, 0),
             (0, 0, 1, 1, 1),
             (0, 1, 0, 0, 0),
             (1, 0, 0, 0, 0),
             (1, 1, 0, 0, 0)}
        """
        out = set({})

        for v in BasicTools.nonzeroVectorsOfDim(in_size):
            out.add(tuple(list(v)+list(tuple(0 for i in range(0,out_size)))))

        for v in BasicTools.nonzeroVectorsOfDim(out_size):
            out.add(tuple([0 for i in range(0,in_size)] + list(v)))

        return out

    @staticmethod
    def interestedSpace(m, n):
        return (BasicTools.allVectorsOfDim(m+n) - BasicTools.nozeroIn_ZeroOut_Or_ZeroIn_NonzeroOut_Patterns(m,n) - {(0,0,0,0,0,0,0,0)})

    @staticmethod
    def differential_patterns_with_freq(sbox, f):
        """
        Compute the set of all possible differential patterns with a given probability f.
        """
        DDT = BasicTools.differential_Distribution_Table(sbox)
        out = set({})
        for dx in range(0, len(sbox.table)):
            for dy in range(0, len(sbox.table)):
                if DDT[dx][dy] == f:
                    out.add(BasicTools._differentialVector(dx, dy, sbox.size))

        return out


    @staticmethod
    def linear_patterns_with_freq(sbox, f):
        """
        Compute the set of all possible differential patterns with a given probability f.
        """
        DDT = BasicTools.differential_Distribution_Table(sbox)
        out = set({})
        for dx in range(0, len(sbox.table)):
            for dy in range(0, len(sbox.table)):
                if DDT[dx][dy] == f:
                    out.add(BasicTools._differentialVector(dx, dy, sbox.size))

        return out

    @staticmethod
    def getVariables_From_Constraints(C):
        V = set([])
        for s in C:
            temp = s.strip()
            temp = temp.replace('+', ' ')
            temp = temp.replace('-', ' ')
            temp = temp.replace('>=', ' ')
            temp = temp.replace('<=', ' ')
            temp = temp.replace('=', ' ')
            temp = temp.split()
            for v in temp:
                if not v.isdecimal():
                    V.add(v)

        return V


class MITMConstraints:

    @staticmethod
    def ForwardDiff_LinearLayer(M, V_in, V_out):
        """
        >>> M = [[1,0,1,1],[1,0,0,0],[0,1,1,0],[1,0,1,0]]
        >>> a = ['a0', 'a1', 'a2', 'a3']
        >>> b = ['b0', 'b1', 'b2', 'b3']
        >>>
        >>> for c in MITMConstraints.ForwardDiff_LinearLayer(M, a, b): print(c)
        ...
        3 b0 -  a0 - a2 - a3 >= 0
        a0 + a2 + a3 - b0 >= 0
        1 b1 -  a0 >= 0
        a0 - b1 >= 0
        2 b2 -  a1 - a2 >= 0
        a1 + a2 - b2 >= 0
        2 b3 -  a0 - a2 >= 0
        a0 + a2 - b3 >= 0
        >>>
        """
        assert len(M[0]) == len(V_in), "The input is not compatible with the matrix"
        assert len(M) == len(V_out), "The output is not compatible with the matrix"

        m = len(M)
        n = len(M[0])

        constr = []
        for i in range(0, m):
            s = sum(M[i]) # the number of 1s in row i
            terms = [V_in[j] for j in range(0, n) if M[i][j] == 1]
            constr = constr + [str(s) + ' ' + V_out[i] + ' - ' + ' ' + BasicTools.MinusTerm(terms) + ' >= 0']
            constr = constr + [BasicTools.plusTerm(terms) + ' - ' + V_out[i] + ' >= 0']

        return constr

    @staticmethod
    def ForwardDiff_XOR(a,b):#if one of a is active,then b is active; else b is nonactive
        """
        >>>a = ['a0','a1','a2']
        >>>b = 'b'
        >>>for c in MITMConstraints.ForwardDiff_XOR(a,b):print(c)
       
        a0 + a1 + a2 - b >= 0
        3 b - a0 - a1 - a2 >= 0
        """
        n = len(a)
        C = []
        C = C + [' + '.join(a)+' - '+b+' >= 0']
        C = C + [str(n)+' '+b+' - '+' - '.join(a)+' >= 0']
        return C
    
    @staticmethod
    def BackwardDet_XOR(a,b):
        """
        >>>a = ['a0','a1','a2']
        >>>b = 'b'
        >>>for c in MITMConstraints.ForwardDiff_XOR(a,b):print(c)
       a0 - b = 0
       a1 - b = 0
       a2 - b = 0
        """   
        
        n = len(a)
        C = []
        for j in range(n):
            C = C + [a[j] + ' - '+b +' = 0']
        return C
    
    @staticmethod
    def ForwardDiff_Branch(a,b):
        """
        >>>a = 'a'
        >>>b = ['b0', 'b1', 'b2']
        >>>for c in MITMConstraints.ForwardDiff_Branch(a,b):print(c)
        a - b0 = 0
        a - b1 = 0
        a - b2 = 0
        """        
        
        n = len(b)
        C = []
        for j in range(n):
            C = C + [a + ' - '+b[j] + ' = 0']
        return C
    
    @staticmethod
    def BackwardDet_Branch(a,b):
        """
        >>>a = 'a'
        >>>b = ['b0', 'b1', 'b2']
        >>>for c in MITMConstraints.ForwardDiff_Branch(a,b):print(c)
        b0 + b1 + b2 - a >= 0
        3 a - b0 - b1 - b2 >= 0
        """           
        
        n = len(b)
        C = []
        C = C + [' + '.join(b)+' - '+a+' >= 0']
        C = C + [str(n)+' '+a+' - '+' - '.join(b)+' >= 0']
        return C
    
    @staticmethod
    def BackwardDet_LinearLayer(M, V_in, V_out):
        """
        >>> M = [[1,0,1,1],[1,0,0,0],[0,1,1,0],[1,0,1,0]]
        >>> a = ['a0', 'a1', 'a2', 'a3']
        >>> b = ['b0', 'b1', 'b2', 'b3']
        >>> MITMConstraints.BackwardDet_LinearLayer(M, a, b)
        ['3 a0 -  b0 - b1 - b3 >= 0',
         'b0 + b1 + b3 - a0 >= 0',
         '1 a1 -  b2 >= 0',
         'b2 - a1 >= 0',
         '3 a2 -  b0 - b2 - b3 >= 0',
         'b0 + b2 + b3 - a2 >= 0',
         '1 a3 -  b0 >= 0',
         'b0 - a3 >= 0']
        >>>
        >>>
        """
        return MITMConstraints.ForwardDiff_LinearLayer(BasicTools.transpose(M), V_out, V_in)

    @staticmethod
    def equalConstraints(x, y):
        assert len(x) == len(y)
        c = []
        for i in range(0, len(x)):
            c = c + [x[i] + ' - ' + y[i] + ' = 0']

        return c
    
    @staticmethod
    def PermConstraints(Perm, x, y): # x[j] to y[Perm[j]]
        assert len(x) == len(y)
        c = []
        for i in range(0, len(x)):
            c = c + [x[i] + ' - ' + y[Perm[i]] + ' = 0']

        return c

    @staticmethod
    def relationXYZ(x, y, z):
        """
        >>> MITMConstraints.relationXYZ(a, b, c)
        ['a0 - c0 >= 0',
         'b0 - c0 >= 0',
         'c0 - a0 - b0 >= -1',
         'a1 - c1 >= 0',
         'b1 - c1 >= 0',
         'c1 - a1 - b1 >= -1',
         'a2 - c2 >= 0',
         'b2 - c2 >= 0',
         'c2 - a2 - b2 >= -1',
         'a3 - c3 >= 0',
         'b3 - c3 >= 0',
         'c3 - a3 - b3 >= -1']
        """
        assert len(x) == len(y) and len(y) == len(z)
        c = []
        for i in range(0, len(x)):
            c = c + [x[i] + ' - ' + z[i] + ' >= 0']
            c = c + [y[i] + ' - ' + z[i] + ' >= 0']
            c = c + [z[i] + ' - ' + x[i] + ' - ' + y[i] + ' >= -1']

        return c


    @staticmethod
    def zeroprop(a,b):#if one of a is zero, then b is zero, other than b is one.
        """
        >>>a = ['a0','a1','a2']
        >>>b = 'b'
        
        >>>for c in MITMConstraints.zeroprop(a,b):print(c)
        a0 + a1 + a2 - 3 b >= 0
        a0 + a1 + a2 - b <= 2
        
        """
        
        Constr = []
        n = len(a)
        Constr = Constr + [' + '.join(a)+' - '+str(n)+' '+b+' >= 0']
        Constr = Constr + [' + '.join(a)+' - '+b+' <= '+str(n-1)]
        return Constr
    
    @staticmethod
    def FowrwardDiff_TruncatedDiff_AESMixColumn(V_in, V_out, V_mid):
        """
        >>>V_in = ['a0','a1','a2','a3']
        >>>V_out = ['b0','b1', 'b2','b3']
        >>>V_mid = 'c'
        >>>for c in MITMConstraints.FowrwardDiff_TruncatedDiff_AESMixColumn(V_in, V_out, V_mid):print(c)
        a0 + a1 + a2 + a3 - c >= 0
        4 c - a0 - a1 - a2 - a3 >= 0
        4 c - b0 - b1 - b2 - b3 >= 0
        a0 + a1 + a2 + a3 + b0 + b1 + b2 + b3 - 5 c >= 0
        """             
        Constr = []
        Constr = Constr + [BasicTools.plusTerm(V_in) + ' - ' + V_mid + ' >= 0']
        Constr = Constr + ['4 ' + V_mid + ' - ' + BasicTools.MinusTerm(V_in) + ' >= 0']
        Constr = Constr + ['4 ' + V_mid + ' - ' + BasicTools.MinusTerm(V_out) + ' >= 0']
        Constr = Constr + [BasicTools.plusTerm(V_in) + ' + ' + BasicTools.plusTerm(V_out) + ' - 5 ' + V_mid + ' >= 0']
        return Constr

    @staticmethod
    def BackwardDet_TruncatedDiff_AESMixColumn(V_in, V_out, V_mid):
        """
        >>>V_in = ['a0','a1','a2','a3']
        >>>V_out = ['b0','b1', 'b2','b3']
        >>>V_mid = 'c'
        >>>for c in MITMConstraints.BackwardDet_TruncatedDiff_AESMixColumn(V_in, V_out, V_mid):print(c)
        b0 + b1 + b2 + b3 - c >= 0
        4 c - b0 - b1 - b2 - b3 >= 0
        4 c - a0 - a1 - a2 - a3 >= 0
        a0 + a1 + a2 + a3 + b0 + b1 + b2 + b3 - 5 c >= 0
        """
        
        Constr = []
        Constr = Constr + [BasicTools.plusTerm(V_out) + ' - ' + V_mid + ' >= 0']
        Constr = Constr + ['4 ' + V_mid + ' - ' + BasicTools.MinusTerm(V_out) + ' >= 0']
        Constr = Constr + ['4 ' + V_mid + ' - ' + BasicTools.MinusTerm(V_in) + ' >= 0']
        Constr = Constr + [BasicTools.plusTerm(V_in) + ' + ' + BasicTools.plusTerm(V_out) + ' - 5 ' + V_mid + ' >= 0']
        return Constr   
    


    
class SolFilePaser:
    def __init__(self, solutionFile):
        solFile = open(solutionFile,'r')
        self.var_value_map = dict()
        print('in init()')
        for line in solFile:
            if line[0] != '#':
                temp = line
                temp = temp.replace('-', ' ')
                temp = temp.split()
                self.var_value_map[temp[0]] = int(temp[1])

    def getSolutions(self):
        return self.var_value_map

    def getBitPatternsFrom(self, vars_sequence):
        pattern = ''
        for key in vars_sequence:
            assert key in self.var_value_map.keys()
            pattern = pattern + str(self.var_value_map[key])

        return pattern

class Cipher(metaclass = ABCMeta):
    def __init__(self, Name, W, Blocksize, R,  word_keysize, keysize):
        print("The wordsize of " + Name + " is " + str(W))
        self.name = Name
        self.wordsize = W
        self.blocksize = Blocksize
        self.wc = Blocksize//W
        self.totalRounds = R
        self.keysize = keysize
        self.wc_key = keysize // word_keysize
        

    @abstractmethod
    def genConstraints_of_Round(self, i):
        pass

    def genObjectiveFun_to_Round(self, i):
#        terms = []
#        for k in range(1, i):
#            terms = terms + [self.activeMarker + str(j) + '_r' + str(k) for j in range(0, self.sboxPerRoud)]
#        
#        return BasicTools.plusTerm(terms)
        pass

    @abstractmethod
    def genConstraints_Additional(self):
        pass

    def genModel(self, ofile, r):
        V = set([])
        C = list([])

        for i in range(r):
            C = C + self.genConstraints_of_Round(i)

        C = C + self.genConstraints_Additional()

        V = BasicTools.getVariables_From_Constraints(C)

        myfile=open(ofile,'w')
        print('Minimize', file = myfile)
        print(self.genObjectiveFun_to_Round(r), file = myfile)
        print('\n', file = myfile)
        print('Subject To', file = myfile)
        for c in C:
            print(c, file = myfile)

        print('\n', file = myfile)
        print('Binary', file = myfile)
        for v in V:
            print(v, file = myfile)
        myfile.close()

def column(A, j):
    return [A[j], A[j+4], A[j+8], A[j+12]]

def ShiftRow_AES(A):
    return [A[0], A[1], A[2], A[3],\
            A[5], A[6], A[7], A[4],\
            A[10],A[11],A[8], A[9],\
            A[15],A[12],A[13],A[14]]

def ShiftRow(A):
    return [A[0], A[1], A[2], A[3],\
            A[7], A[4], A[5], A[6],\
            A[10],A[11],A[8], A[9],\
            A[13],A[14],A[15],A[12]]

def prettyPrint(A):
    print(A[0:4])
    print(A[4:8])
    print(A[8:12])
    print(A[12:16])
    print('\n')


def main():
    pass

if __name__ == '__main__':
    main()
