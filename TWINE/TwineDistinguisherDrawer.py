

LM= [5,0, 1, 4, 7, 12, 3 ,8, 13, 6, 9, 2, 15, 10, 11, 14]

from CPMITM import *
from MITMTWINE import *

class DrawDistinguisher():
    def __init__(self, solutionFile, Round):
        print('in init()')
        solFile = open(solutionFile,'r')
        self.Round = Round
        self.var_value_map = dict()
        for line in solFile:
            if line[0] != '#':
                temp = line
                temp = temp.replace('-', ' ')
                temp = temp.split()
                self.var_value_map[temp[0]] = int(temp[1])

    def draw(self,outputfile):
        
        _X = BasicTools.typeX
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ
        TWINE = MITM_TWINE("TWINE", 4, 64, self.Round, 4, 80)
        Solution = self.var_value_map
        fid = open(outputfile,'w')
        fid.write('\\documentclass{standalone}'+'\n'+'\\usepackage{tikz}'+'\n'+'\\usepackage{calc}'+'\n'+'\\usepackage{pgffor}'+'\n'+'\\usetikzlibrary{patterns}'+'\n'+'\\begin{document}'+'\n'+'\\begin{tikzpicture}[scale=0.35]'+'\n')
        fid.write('\\foreach \z in {0')
        for i in range(1,self.Round):
            fid.write(','+str(i))
        fid.write('}{'+'\n')
        fid.write('\\begin{scope}[yshift = -\\z* 5 cm]'+'\n')
        fid.write('\\foreach \\x  in {0,1,...,7}'+'\n'+'{'+'\n')
        fid.write('\\begin{scope}[xshift = \\x*7 cm]'+'\n')
        fid.write('\\draw (0,0) grid +(1,1);'+'\n')
        fid.write('\\draw[->] (0.5,0)|- +(1,-1.5);'+'\n')
        fid.write('\\draw (4,0) grid +(1,1);'+'\n')
        fid.write('\\draw (1.75,-1.5) circle (0.25);'+'\n')
        fid.write('\\draw (1.75,-1.25) --+(0,-0.5);'+'\n')
        fid.write('\\draw[->] (1.5,-1.5) --(2.5,-1.5);'+'\n')
        fid.write('\\draw (2.5,-1.75) rectangle + (1,0.5);'+'\n')
        fid.write('\\draw[->](3.5,-1.5)--(4.25,-1.5);'+'\n')
        fid.write('\\draw (4.5,-1.5) circle (0.25);'+'\n')
        fid.write('\\draw (4.25,-1.5) -- +(0.5,0);'+'\n')
        fid.write('\\draw (4.5,0)--+(0,-2);'+'\n')
        fid.write('\\draw[->](0.5,-3)--+(0,-1);'+'\n')
        fid.write('\\draw[->](4.5,-3)--+(0,-1);'+'\n')
        fid.write('\\draw (0.5,-1.5)--+(0,-0.5);'+'\n')
        fid.write('\\draw[->] (1.75,-0.5) node[above]{\\tiny{RK}} --(1.75,-1.25);'+'\n')
        fid.write('\\end{scope}'+'\n')
        fid.write('\n'+'}')
        fid.write('\n'+'\\end{scope}')
        fid.write('\n'+'}'+'\n'+'\n')

        fid.write('\\foreach \z in {0')
        for i in range(1,self.Round):
            fid.write(','+str(i))
        fid.write('}{'+'\n')
        fid.write('\\begin{scope}[yshift = -\\z* 5 cm]'+'\n')
        fid.write('\\node[left] at (0,0.5) {\\tiny Round \z};'+'\n')
        for i in range(16):
            if i % 2 == 0:
                x1 = (i//2)*7 +0.5
            if LM[i] % 2 ==0:
                x2 = (LM[i]//2)*7 + 0.5
            if i %2 ==1:
                x1 = (i//2)*7+4.5
            if LM[i]%2 ==1:
                x2 = (LM[i]//2)*7+4.5
            fid.write('\\draw ('+str(x1)+',-2)--('+str(x2)+',-3);'+'\n')
        fid.write('\\end{scope}'+'\n')
        fid.write('}'+'\n'+'\n')

        fid.write('\\begin{scope}[yshift = -'+str(self.Round*5)+'cm]'+'\n')
        fid.write('\\node[left] at (0,0.5) {\\tiny Round '+str(self.Round)+'};'+'\n')
        fid.write('\\foreach \\x  in {0,1,...,7}'+'\n'+'{'+'\n')
        fid.write('\\begin{scope}[ xshift = \\x*7 cm]'+'\n')
        fid.write('\\draw (0,0) grid +(1,1);'+'\n')
        fid.write('\\draw (4,0) grid +(1,1);'+'\n')
        fid.write('\\end{scope}'+'\n')
        fid.write('}'+'\n'+'\n')
        fid.write('\\end{scope}'+'\n')
        
        

        
        for i in range(self.Round):
            GIS = _Z(TWINE.genVars_inputSbox(i))
            fid.write('\\begin{scope}[yshift = -'+str(i*5)+'cm]'+'\n')
            for j in range(8):
                if self.var_value_map[GIS[j]] == 1:
                    fid.write('\\fill[red] ('+str(7*j+2.5)+',-1.75) rectangle+(1,0.5);'+'\n')
            fid.write('\\end{scope}'+'\n'+'\n')

        for i in range(self.Round):
            IP = _X(TWINE.genVars_input(i))
            IS = _X(TWINE.genVars_inputSbox(i))
            DIP = _Y(TWINE.genVars_input(i))
            DIS = _Y(TWINE.genVars_inputSbox(i))
            fid.write('\\begin{scope}[yshift = -'+str(i*5)+'cm]'+'\n')
            for j in range(16):
                if self.var_value_map[IP[j]] == 1:
                    if j % 2 == 0:
                        x = 7*(j//2)
                    if j % 2 == 1:
                        x = 4 + 7*(j//2)
                    fid.write('\\fill[pattern = north east lines] ('+str(x)+',0) rectangle+(1,1);'+'\n')
                if self.var_value_map[DIP[j]] == 1:
                    if j % 2 == 0:
                        x = 7*(j//2)
                    if j % 2 == 1:
                        x = 4 + 7*(j//2)
                    fid.write('\\fill[pattern = north west lines] ('+str(x)+',0) rectangle+(1,1);'+'\n')
            for j in range(8):
                if self.var_value_map[IS[j]] == 1:
                    fid.write('\\fill[pattern = north east lines] ('+str(7*j+2.5)+',-1.75) rectangle+(1,0.5);'+'\n')
                if self.var_value_map[DIS[j]] == 1:
                    fid.write('\\fill[pattern = north west lines] ('+str(7*j+2.5)+',-1.75) rectangle+(1,0.5);'+'\n')
            fid.write('\\end{scope}'+'\n'+'\n')

        for i in [self.Round]:
            IP = _X(TWINE.genVars_input(i))
            DIP = _Y(TWINE.genVars_input(i))
            fid.write('\\begin{scope}[yshift = -'+str(i*5)+'cm]'+'\n')
            for j in range(16):
                if self.var_value_map[IP[j]] == 1:
                    if j % 2 == 0:
                        x = 7*(j//2)
                    if j % 2 == 1:
                        x = 4 + 7*(j//2)
                    fid.write('\\fill[pattern = north east lines] ('+str(x)+',0) rectangle+(1,1);'+'\n')
                if self.var_value_map[DIP[j]] == 1:
                    if j % 2 == 0:
                        x = 7*(j//2)
                    if j % 2 == 1:
                        x = 4 + 7*(j//2)
                    fid.write('\\fill[pattern = north west lines] ('+str(x)+',0) rectangle+(1,1);'+'\n')
            fid.write('\\end{scope}'+'\n'+'\n')
        fid.write('\n'+'\\end{tikzpicture}'+'\n'+'\\end{document}')
        fid.close()








