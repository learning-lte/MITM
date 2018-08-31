

PT = [9,15,8,13,10,14,12,11,0,1,2,3,4,5,6,7]
T = [8,9,10,11,12,13,14,15,2,0,4,7,6,3,5,1]
from MITMSKINNY import *

class DrawKeyschedule():
    def __init__(self,solutionFile, totalRounds, backwardRounds, forwardRounds):
##        print('in init()')
        solFile = open(solutionFile,'r')
        self.Round = totalRounds + backwardRounds + forwardRounds
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

    def draw(self,outputfile):
        Solution = self.var_value_map
        SKINNY = MITM_SKINNY("SKI",8,128,self.TR, 8, 384)
        fid = open(outputfile,'w')
        fid.write('\\documentclass{standalone}'+'\n'+'\\usepackage{tikz}'+'\n'+'\\usepackage{calc}'+'\n'+'\\usepackage{pgffor}'+'\n'+'\\usetikzlibrary{patterns}'+'\n'+'\\begin{document}'+'\n'+'\\begin{tikzpicture}[scale=0.35]'+'\n')
        fid.write('\\foreach \z in {0')
        for i in range(1,self.Round-1):
            fid.write(','+str(i))
        fid.write('}{'+'\n')
        fid.write('\\begin{scope}[yshift = -\\z* 4 cm]'+'\n')
        fid.write('\\foreach \\x  in {0,1,...,15}'+'\n'+'{'+'\n')
        fid.write('\\begin{scope}[xshift = \\x*3 cm]'+'\n')

        fid.write('\\draw (0,0) grid +(1,1);'+'\n')
        fid.write('\\draw (0.5,0) -- +(0,-1);'+'\n')
        fid.write('\\draw[->] (0.5,-2) -- +(0,-1);'+'\n')
        fid.write('\\end{scope}'+'\n')
        fid.write('\n'+'}'+'\n')
        fid.write('\\node[left] at(0,0.5){\\tiny{\\z}};'+'\n')
        for j in range(16):
            x = PT[j]*3 + 0.5
            y = j*3+0.5
            fid.write('\\draw ('+str(x)+',-1)--('+str(y)+',-2);'+'\n')
        fid.write('\n'+'\\end{scope}')
        fid.write('\n'+'}'+'\n'+'\n')

        for i in range(self.BR + self.TR + 1, self.BR + self.FR + self.TR):
            SK = SKINNY.genVars_subkey(i)
            fid.write('\\begin{scope}[yshift = '+str(-i* 4)+' cm]'+'\n')
            for j in range(8):
                if Solution[SK[j]] == 1:
                    fid.write('\\fill[green] ('+str(3*j)+',0) rectangle +(1,1);'+'\n')
            fid.write('\n'+'\\end{scope}')

        for i in range(self.BR):
            SK = SKINNY.genVars_subkey(i)
            fid.write('\\begin{scope}[yshift = '+str(-i* 4)+' cm]'+'\n')
            for j in range(8):
                if Solution[SK[j]] == 1:
                    fid.write('\\fill[green] ('+str(3*j)+',0) rectangle +(1,1);'+'\n')
            fid.write('\n'+'\\end{scope}')


        for j in range(16):
            sk = j
            fid.write('\\node[above] at('+str(sk*3+0.5)+',0) {\\tiny{'+str(j)+'}};'+'\n')
            for r in range(1,self.Round):
                sk = T[sk]
                ix = sk*3+0.5
                fid.write('\\begin{scope}[yshift ='+ str(-r* 4)+' cm]'+'\n')
                fid.write('\\node[above] at('+str(ix)+',0) {\\tiny{'+str(j)+'}};'+'\n')
                fid.write('\\end{scope}'+'\n')

        fid.write('\\foreach \\x  in {0,1,...,15}'+'\n'+'{'+'\n')
        fid.write('\\begin{scope}[yshift = -'+str((self.Round-1)*4)+'cm]'+'\n')
        fid.write('\\begin{scope}[xshift = \\x*3 cm]'+'\n')
        fid.write('\\draw (0,0) grid +(1,1);'+'\n')
        fid.write('\\end{scope}'+'\n')
        fid.write('\\node[left] at(0,0.5){\\tiny{'+str(self.Round-1)+'}};'+'\n')
        fid.write('\\end{scope}'+'\n')
        fid.write('}'+'\n'+'\n')

        fid.write('\n'+'\\end{tikzpicture}'+'\n'+'\\end{document}')
        fid.close()









