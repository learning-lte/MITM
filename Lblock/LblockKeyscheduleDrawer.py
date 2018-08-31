from CPMITM import *
from MITMLBlock import *


linearM = [2,0,3,1,6,4,7,5]


class DrawKeyschedule():

    def __init__(self,solutionFile, totalRounds, backwardRounds, forwardRounds, MR):
        print('in init()')
        solFile = open(solutionFile,'r')
        self.var_value_map = dict()
        self.TR = totalRounds
        self.BR = backwardRounds
        self.FR = forwardRounds
        self.MR = MR
        for line in solFile:
            if line[0] != '#':
                temp = line
                temp = temp.replace('-', ' ')
                temp = temp.split()
                self.var_value_map[temp[0]] = int(temp[1])
    def draw(self,outputfile):
        Blockcipher = MITM_Lblock("Lblock", 4, 64, self.TR, 4, 80)
        Solution = self.var_value_map
        KRound = self.TR + self.BR + self.FR
        Lab = [j for j in range(80)]
        fid = open(outputfile,'w')
        fid.write('\\documentclass{standalone}'+'\n'+'\\usepackage{tikz}'+'\n'+'\\usepackage{amssymb}'+'\n'+'\\usepackage{calc}'+'\n'+'\\usepackage{pgffor}'+'\n'+'\\usetikzlibrary{patterns}'+'\n'+'\\begin{document}'+'\n'+'\\begin{tikzpicture}[scale=0.35]'+'\n')
        fid.write('\\foreach \\x in {0')
        for i in range(1, KRound-1):
            fid.write(','+str(i))
        fid.write('}{'+'\n')
        fid.write('\\begin{scope}[yshift = -\\x*6 cm]'+'\n')
        for j in range(8):
            fid.write('\\draw[->] ('+str(j+0.5)+',0)  --+(0,-1);'+'\n')
            fid.write('\\draw[->] ('+str(j+0.5)+',-2)  --+(0,-1);'+'\n')
            fid.write('\\draw[->] ('+str(j+0.5)+',-4)  --+(0,-1);'+'\n')
            #fid.write('\\draw ('+str(j+0.5)+',-3)-- ('+str((j-29)%80 + 0.5)+',-5);'+'\n')
        for j in range(8,80):
            fid.write('\\draw[->] ('+str(j+0.5)+',-2)  --+(0,-3);'+'\n')
            fid.write('\\draw[->] ('+str(j+0.5)+',0)  --+(0,-1);'+'\n')
            #fid.write('\\draw ('+str(j+0.5)+',-3)-- ('+str((j-29)%80 + 0.5)+',-5);'+'\n')
        fid.write('\\draw (0,-2) rectangle node{\\tiny Shift to the left by 29-bit}+(80,1);'+'\n')
        fid.write('\\draw (0,-4) rectangle node{S} +(4,1);'+'\n')
        fid.write('\\draw (4,-4) rectangle node{S} +(4,1);'+'\n')
        fid.write('\end{scope}'+'\n')
        fid.write('\n'+'}'+'\n'+'\n')


        for i in range(0, KRound):
             fid.write('\\begin{scope}[yshift = '+str(-i*6)+' cm]'+'\n')
             Sk = Blockcipher.genVars_subkey(i)
             for j in range(80):
                 if j%4 ==0:
                     fid.write('\\node[above] at ('+str(j)+',1) {\\tiny{'+str(j//4)+'}};'+'\n')
                 if Solution[Sk[j]] ==1:
                    if i == self.MR:
                        fid.write('\\fill[red] ('+str(j)+',0) rectangle +(1,1);'+'\n')
                    else:
                        fid.write('\\fill[green] ('+str(j)+',0) rectangle +(1,1);'+'\n')
                 fid.write('\\draw ('+str(j)+',0) rectangle node{\\tiny '+str(Lab[j])+'}+(1,1);'+'\n')
                 fid.write('\\node[left] at (0,0.5) {\\tiny {Round '+str(i)+'}};'+'\n')
             Lab = [Lab[(j+29)%80] for j in range(80)]

             fid.write('\\end{scope}'+'\n')

        fid.write('\n'+'\\end{tikzpicture}'+'\n'+'\\end{document}')
        fid.close()








