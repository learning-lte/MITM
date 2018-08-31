from CPMITM import *
from MITMTWINE import *


class DrawKeyschedule():
    def __init__(self,solutionFile, totalRounds, backwardRounds, forwardRounds, MR,  keylen):
        print('in init()')
        solFile = open(solutionFile,'r')
        self.fullRounds = totalRounds + backwardRounds + forwardRounds
        self.TR = totalRounds
        self.keylen = keylen
        self.MR = MR
        self.var_value_map = dict()
        for line in solFile:
            if line[0] != '#':
                temp = line
                temp = temp.replace('-', ' ')
                temp = temp.split()
                self.var_value_map[temp[0]] = int(temp[1])

    def draw(self,outputfile):
        TWINE = MITM_TWINE("TWINE", 4, 64, self.TR, 4, 4*self.keylen)
        if self.keylen == 32:
            LLL = [1,4,23]
            CLL = [0,16,30]
            CK = [2,3,12,15,17,18,28,31]
            KPI = [31,28,29,30] + [j for j in range(self.keylen-4)]
            MPT = [j+4 for j in range(self.keylen-4)]+[1,2,3,0]
            Mark = [j for j in range(self.keylen)]
            
        else:
            LLL = [1,4]
            CLL = [0,16]
            CK = [1,3,4,6,13,14,15,16]
            KPI = [19,16,17,18] + [j for j in range(self.keylen-4)]
            MPT = [j+4 for j in range(self.keylen-4)]+[1,2,3,0]
            Mark = [j for j in range(self.keylen)]
        #SLL = set([j for j in range(self.keylen)])-set(LLL)
        Solution = self.var_value_map
        fid = open(outputfile,'w')
        fid.write('\\documentclass{standalone}'+'\n'+'\\usepackage{tikz}'+'\n'+'\\usepackage{calc}'+'\n'+'\\usepackage{pgffor}'+'\n'+'\\usetikzlibrary{patterns}'+'\n'+'\\begin{document}'+'\n'+'\\begin{tikzpicture}[scale=0.35]'+'\n')
        
        for i in range(self.fullRounds - 1):
            RK = TWINE.genVars_subkey(i)
            fid.write('\\begin{scope}[yshift = '+str(-i* 7)+' cm]'+'\n')
            for j in range(self.keylen):
                if self.var_value_map[RK[j]] == 1:
                    if i == self.MR:
                        fid.write('\\fill[red] ('+str(j*4)+',0) rectangle + (1,1);'+'\n')
                    else:
                        fid.write('\\fill[green] ('+str(j*4)+',0) rectangle + (1,1);'+'\n')
                fid.write('\\node[above] at('+str(4*j+0.5)+',0){\\tiny '+str(Mark[j])+' };'+'\n')
            Mark = [Mark[MPT[j]] for j in range(self.keylen)]
            fid.write('\n'+'\\end{scope}')


        fid.write('\\foreach \z in {0')
        for i in range(1,self.fullRounds - 1):
            fid.write(','+str(i))
        fid.write('}{'+'\n')
        fid.write('\\begin{scope}[yshift = -\\z* 7 cm]'+'\n')
        fid.write('\\node[left] at(0,0.5) {\\tiny Round \\z};'+'\n')
        fid.write('\\foreach \\x  in {0,1,...,'+str(self.keylen-1)+'}'+'\n'+'{'+'\n')
        fid.write('\\begin{scope}[xshift = \\x*4 cm]'+'\n')
        fid.write('\\draw (0,0) rectangle +(1,1);'+'\n')
#        fid.write('\\node[above] at(0.5,0){\\tiny{\\x}};'+'\n')
        fid.write('\\draw[->] (0.5,0) -- +(0,-2);'+'\n')
        fid.write('\\draw[->] (0.5,-5)--+(0,-1);'+'\n')
        fid.write('\\end{scope}'+'\n')
        fid.write('\n'+'}')


        x1 = CLL[0]*4+0.5
        x2 = LLL[0]*4+0.25
        fid.write('\\draw[->] ('+str(x1)+',-1)--+(1.5,0);'+'\n')
        fid.write('\\draw ('+str(x1+1.5)+',-1.25) rectangle node{\\tiny{S}} +(1,0.5);'+'\n')
        fid.write('\\draw[->] ('+str(x1+2.5)+',-1)--('+str(x2)+',-1);'+'\n')
        for j in range(1,len(CLL)):
            x1 = CLL[j]*4+0.5
            x2 = LLL[j]*4+0.75
            fid.write('\\draw[->] ('+str(x1)+',-1)--+(-1.5,0);'+'\n')
            fid.write('\\draw ('+str(x1-1.5)+',-1.25) rectangle node{\\tiny{S}} +(-1,0.5);'+'\n')
            fid.write('\\draw[->] ('+str(x1-2.5)+',-1)--('+str(x2)+',-1);'+'\n')
        for j in range(len(LLL)):
            x1 = LLL[j]*4+0.5
            fid.write('\\draw ('+str(x1)+',-1) circle (0.25);'+'\n')
            fid.write('\\draw('+str(x1-0.25)+',-1)--+(0.5,0);'+'\n')
        for j in range(self.keylen):
            x1 = j*4+0.5
            x2 = KPI[j]*4+0.5
            fid.write('\\draw ('+str(x1)+',-2)--('+str(x2)+',-5);'+'\n')

        fid.write('\n'+'\\end{scope}')
        fid.write('\n'+'}'+'\n'+'\n')


        for i in [self.fullRounds - 1]:
            RK = TWINE.genVars_subkey(i)
            fid.write('\\begin{scope}[yshift = '+str(-i* 7)+' cm]'+'\n')
            for j in range(self.keylen):
                if self.var_value_map[RK[j]] == 1:
                    fid.write('\\fill[green] ('+str(j*4)+',0) rectangle + (1,1);'+'\n')
                fid.write('\\node[above] at('+str(4*j+0.5)+',0){\\tiny '+str(Mark[j])+' };'+'\n')
            Mark = [Mark[MPT[j]] for j in range(self.keylen)]
            fid.write('\\node[left] at(0,0.5) {\\tiny Round '+str(i)+'};'+'\n')
            fid.write('\\foreach \\x  in {0,1,...,'+str(self.keylen-1)+'}'+'\n'+'{'+'\n')
            fid.write('\\begin{scope}[xshift = \\x*4 cm]'+'\n')
            fid.write('\\draw (0,0) rectangle +(1,1);'+'\n')
            fid.write('\\end{scope}'+'\n')
            fid.write('\n'+'}')
            fid.write('\n'+'\\end{scope}')


        fid.write('\n'+'\\end{tikzpicture}'+'\n'+'\\end{document}')
        fid.close()










