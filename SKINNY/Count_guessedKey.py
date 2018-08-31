from MITMSKINNY import *
KPT = [9,15,8,13,10,14,12,11,0,1,2,3,4,5,6,7]
KT = [8,9,10,11,12,13,14,15,2,0,4,7,6,3,5,1]
class Count_guessedkey():
    def __init__(self,solutionFile, totalRounds, backwardRounds, forwardRounds):
##        print('in init()')
        solFile = open(solutionFile,'r')
        self.Round = totalRounds + forwardRounds + backwardRounds
        self.TR = totalRounds
        self.BR = backwardRounds
        self.FR = forwardRounds
        self.var_value_map = dict()
        for line in solFile:
            if line[0] != '#':
                temp = line
                temp = temp.replace('-', ' ')
                temp = temp.split()
                self.var_value_map[temp[0]] = int(temp[1])
    def Count(self):
        SKINNY = MITM_SKINNY("SKINNY", 8, 128, 10, 8, 384)
        Solution = self.var_value_map
        T = [0 for j in range(16)]
        guessN = 0
        MK = [j for j in range(16)]
        for i in range(self.BR):
            SK = SKINNY.genVars_subkey(i)
            for j in range(8):
                if Solution[SK[j]] == 1:
                    T[MK[j]] = T[MK[j]] + 1
            MK = [KPT[MK[j]] for j in range(16)]
            #print(T)
        for i in range(self.BR, self.BR + self.TR + 1):
            MK = [KPT[MK[j]] for j in range(16)]
        for i in range(self.BR + self.TR + 1, self.BR + self.TR + self.FR):
            SK = SKINNY.genVars_subkey(i)
            for j in range(8):
                if Solution[SK[j]] ==1:
                    T[MK[j]] = T[MK[j]] + 1
            MK = [KPT[MK[j]] for j in range(16)]
            #print(T)
        for j in range(16):
            if T[j] >= 3:
                guessN = guessN + 3
            else:
                guessN = guessN + T[j]

        return [T,guessN]
