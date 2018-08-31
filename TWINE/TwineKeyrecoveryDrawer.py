
from CPMITM import *
from MITMTWINE import *
LM= [5,0, 1, 4, 7, 12, 3 ,8, 13, 6, 9, 2, 15, 10, 11, 14]

class DrawKeyrecovery():
    def __init__(self,solutionFile, totalRounds, backwardRounds, forwardRounds):
        print('in init()')
        solFile = open(solutionFile,'r')
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
        _X = BasicTools.typeX
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ
        
        TWINE = MITM_TWINE("TWINE", 4, 64, self.TR, 4, 80)
        
        Solution = self.var_value_map
        fid = open(outputfile,'w')
        fid.write('\\documentclass{standalone}'+'\n'+'\\usepackage{tikz}'+'\n'+'\\usepackage{calc}'+'\n'+'\\usepackage{pgffor}'+'\n'+'\\usetikzlibrary{patterns}'+'\n'+'\\begin{document}'+'\n'+'\\begin{tikzpicture}[scale=0.35]'+'\n')
        fid.write('\\foreach \z in {0')
        for i in range(1,self.BR):
            fid.write(','+str(i))
        fid.write('}{'+'\n')
        fid.write('\\begin{scope}[yshift = -\\z* 5 cm]'+'\n')
        fid.write('\\node[left] at (0,0.5) {\\tiny Round \z};'+'\n')
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
        for i in range(1,self.BR):
            fid.write(','+str(i))
        fid.write('}{'+'\n')
        fid.write('\\begin{scope}[yshift = -\\z* 5 cm]'+'\n')
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

        fid.write('\\begin{scope}[yshift = -'+str(self.BR*5)+'cm]'+'\n')
        fid.write('\\foreach \\x  in {0,1,...,7}'+'\n'+'{'+'\n')
        fid.write('\\begin{scope}[xshift = \\x*7 cm]'+'\n')
        fid.write('\\draw (0,0) grid +(1,1);'+'\n')
        fid.write('\\draw (4,0) grid +(1,1);'+'\n')
        fid.write('\\end{scope}'+'\n')
        fid.write('}'+'\n'+'\n')
        fid.write('\\node[left] at (0,0.5) {\\tiny Round '+str(self.BR)+'};'+'\n')
        fid.write('\\end{scope}'+'\n')

        fid.write('\\begin{scope}[yshift = -'+str(self.BR*5)+'cm]'+'\n')
        fid.write('\\draw[dashed] (-0.2,1.2) rectangle node{\\scriptsize 11-round Distinguisher} +(54.4,-6.4);'+'\n')
        fid.write('\\end{scope}'+'\n'+'\n')
#above is the figure of  structure before the distinguisher.


        fid.write('\\foreach \\z in {'+str(self.BR+1))
        for i in range(1,self.FR):
            fid.write(','+str(i+self.BR+1))
        fid.write('}{'+'\n')
        fid.write('\\begin{scope}[yshift = -\\z* 5 cm]'+'\n')
        fid.write('\\node[left] at (0,0.5) {\\tiny Round' +'\pgfmathparse{int((\z-1)+'+str(self.TR)+')}\pgfmathresult'+'};'+'\n')
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

        fid.write('\\foreach \\z in {'+str(self.BR+1))
        for i in range(1,self.FR):
            fid.write(','+str(i+self.BR+1))
        fid.write('}{'+'\n')
        fid.write('\\begin{scope}[yshift = -\\z* 5 cm]'+'\n')
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

        fid.write('\\begin{scope}[yshift = -'+str((self.BR+1+self.FR)*5)+'cm]'+'\n')
        fid.write('\\foreach \\x  in {0,1,...,7}'+'\n'+'{'+'\n')
        fid.write('\\begin{scope}[ xshift = \\x*7 cm]'+'\n')
        fid.write('\\draw (0,0) grid +(1,1);'+'\n')
        fid.write('\\draw (4,0) grid +(1,1);'+'\n')
        fid.write('\\end{scope}'+'\n')
        fid.write('}'+'\n'+'\n')
        fid.write('\\node[left] at (0,0.5) {\\tiny Round '+str(self.BR+self.TR+self.FR)+'};'+'\n')
        fid.write('\\end{scope}'+'\n')
#above is the figure of structure following the distinguisher


        for i in range(self.BR):
            GIS = _X(TWINE.genVars_inputSbox(-(self.BR-i)))
            X = _X(TWINE.genVars_input(-(self.BR-i)))
            fid.write('\\begin{scope}[yshift = -'+str(i*5)+'cm]'+'\n')
            for j in range(8):
                if self.var_value_map[GIS[j]] == 1:
                    fid.write('\\fill[blue] ('+str(7*j+2.5)+',-1.75) rectangle+(1,0.5);'+'\n')
            for j in range(16):
                if self.var_value_map[X[j]] == 1:
                    if j % 2 == 0:
                        x = 7*(j//2)
                    if j % 2 == 1:
                        x = 4 + 7*(j//2)
                    fid.write('\\fill[blue] ('+str(x)+',0) rectangle+(1,1);'+'\n')
            fid.write('\\end{scope}'+'\n'+'\n')

        for i in [self.BR]:
            X = _X(TWINE.genVars_input(0))
            fid.write('\\begin{scope}[yshift = -'+str(i*5)+'cm]'+'\n')
            for j in range(16):
                if self.var_value_map[X[j]] == 1:
                    if j % 2 == 0:
                        x = 7*(j//2)
                    if j % 2 == 1:
                        x = 4 + 7*(j//2)
                    fid.write('\\fill[blue] ('+str(x)+',0) rectangle+(1,1);'+'\n')
            fid.write('\\end{scope}'+'\n'+'\n')
#above is the fillment before the distinguisher


        for i in range(self.FR):
            GIS = _Y(TWINE.genVars_inputSbox(i+self.TR))
            X = _Y(TWINE.genVars_input(i+self.TR))
            fid.write('\\begin{scope}[yshift = -'+str((i+self.BR+1)*5)+'cm]'+'\n')
            for j in range(8):
                if self.var_value_map[GIS[j]] == 1:
                    fid.write('\\fill[blue] ('+str(7*j+2.5)+',-1.75) rectangle+(1,0.5);'+'\n')
            for j in range(16):
                if self.var_value_map[X[j]] == 1:
                    if j % 2 == 0:
                        x = 7*(j//2)
                    if j % 2 == 1:
                        x = 4 + 7*(j//2)
                    fid.write('\\fill[blue] ('+str(x)+',0) rectangle+(1,1);'+'\n')
            fid.write('\\end{scope}'+'\n'+'\n')

        for i in [self.FR]:
            X = _Y(TWINE.genVars_input(i+self.TR))
            fid.write('\\begin{scope}[yshift = -'+str((i+self.BR+1)*5)+'cm]'+'\n')
            for j in range(16):
                if self.var_value_map[X[j]] == 1:
                    if j % 2 == 0:
                        x = 7*(j//2)
                    if j % 2 == 1:
                        x = 4 + 7*(j//2)
                    fid.write('\\fill[blue] ('+str(x)+',0) rectangle+(1,1);'+'\n')
            fid.write('\\end{scope}'+'\n'+'\n')
        fid.write('\n'+'\\end{tikzpicture}'+'\n'+'\\end{document}')
        fid.close()


    def drawGuessedValue(self,outputfile):
        
        _X = BasicTools.typeX
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ        
        TWINE = MITM_TWINE("TWINE", 4, 64, self.TR, 4, 80)
        
        Solution = self.var_value_map
        fid = open(outputfile,'w')
        fid.write('\\documentclass{standalone}'+'\n'+'\\usepackage{tikz}'+'\n'+'\\usepackage{calc}'+'\n'+'\\usepackage{pgffor}'+'\n'+'\\usetikzlibrary{patterns}'+'\n'+'\\begin{document}'+'\n'+'\\begin{tikzpicture}[scale=0.35]'+'\n')
        fid.write('\\foreach \z in {0')
        for i in range(1,self.BR):
            fid.write(','+str(i))
        fid.write('}{'+'\n')
        fid.write('\\begin{scope}[yshift = -\\z* 5 cm]'+'\n')
        fid.write('\\node[left] at (0,0.5) {\\tiny Round \z};'+'\n')
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

#        fid.write('\\draw[->] (1.75,-0.5) node[above]{\\tiny{RK}} --(1.75,-1.25);'+'\n')
        fid.write('\\draw (-1,-0.75) rectangle node[left=5pt]{\\tiny{RK}} +(1,0.5);'+'\n')
        fid.write('\\draw[->]  (0,-0.5) -|(1.75,-1.25);'+'\n')
        fid.write('\\draw[->] (1.75,-0.5)  --(1.75,-1.25);'+'\n')

        fid.write('\\end{scope}'+'\n')
        fid.write('\n'+'}')
        fid.write('\n'+'\\end{scope}')
        fid.write('\n'+'}'+'\n'+'\n')

        fid.write('\\foreach \z in {0')
        for i in range(1,self.BR):
            fid.write(','+str(i))
        fid.write('}{'+'\n')
        fid.write('\\begin{scope}[yshift = -\\z* 5 cm]'+'\n')
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

        fid.write('\\begin{scope}[yshift = -'+str(self.BR*5)+'cm]'+'\n')
        fid.write('\\foreach \\x  in {0,1,...,7}'+'\n'+'{'+'\n')
        fid.write('\\begin{scope}[xshift = \\x*7 cm]'+'\n')
        fid.write('\\draw (0,0) grid +(1,1);'+'\n')
        fid.write('\\draw (4,0) grid +(1,1);'+'\n')
        fid.write('\\end{scope}'+'\n')
        fid.write('}'+'\n'+'\n')
        fid.write('\\node[left] at (0,0.5) {\\tiny Round '+str(self.BR)+'};'+'\n')
        fid.write('\\end{scope}'+'\n')

        fid.write('\\begin{scope}[yshift = -'+str(self.BR*5)+'cm]'+'\n')
        fid.write('\\draw[dashed] (-0.2,1.2) rectangle node{\\scriptsize 11-round Distinguisher} +(54.4,-6.4);'+'\n')
        fid.write('\\end{scope}'+'\n'+'\n')
#above is the figure of  structure before the distinguisher.


        fid.write('\\foreach \\z in {'+str(self.BR+1))
        for i in range(1,self.FR):
            fid.write(','+str(i+self.BR+1))
        fid.write('}{'+'\n')
        fid.write('\\begin{scope}[yshift = -\\z* 5 cm]'+'\n')
        fid.write('\\node[left] at (0,0.5) {\\tiny Round' +'\pgfmathparse{int((\z-1)+'+str(self.TR)+')}\pgfmathresult'+'};'+'\n')
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

#        fid.write('\\draw[->] (1.75,-0.5) node[above]{\\tiny{RK}} --(1.75,-1.25);'+'\n')
        fid.write('\\draw (-1,-0.75) rectangle node[left=5pt]{\\tiny{RK}} +(1,0.5);'+'\n')
        fid.write('\\draw[->]  (0,-0.5) -|(1.75,-1.25);'+'\n')
        fid.write('\\draw[->] (1.75,-0.5)  --(1.75,-1.25);'+'\n')


        fid.write('\\end{scope}'+'\n')
        fid.write('\n'+'}')
        fid.write('\n'+'\\end{scope}')
        fid.write('\n'+'}'+'\n'+'\n')

        fid.write('\\foreach \\z in {'+str(self.BR+1))
        for i in range(1,self.FR):
            fid.write(','+str(i+self.BR+1))
        fid.write('}{'+'\n')
        fid.write('\\begin{scope}[yshift = -\\z* 5 cm]'+'\n')
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

        fid.write('\\begin{scope}[yshift = -'+str((self.BR+1+self.FR)*5)+'cm]'+'\n')
        fid.write('\\foreach \\x  in {0,1,...,7}'+'\n'+'{'+'\n')
        fid.write('\\begin{scope}[ xshift = \\x*7 cm]'+'\n')
        fid.write('\\draw (0,0) grid +(1,1);'+'\n')
        fid.write('\\draw (4,0) grid +(1,1);'+'\n')
        fid.write('\\end{scope}'+'\n')
        fid.write('}'+'\n'+'\n')
        fid.write('\\node[left] at (0,0.5) {\\tiny Round '+str(self.BR+self.TR+self.FR)+'};'+'\n')
        fid.write('\\end{scope}'+'\n')
#above is the figure of structure following the distinguisher


        for i in range(self.BR):
            VIS = _Z(TWINE.genVars_inputSbox(-(self.BR-i)))
            VX =  _Z(TWINE.genVars_input(-(self.BR-i)))

            fid.write('\\begin{scope}[yshift = -'+str(i*5)+'cm]'+'\n')
            for j in range(8):
                if self.var_value_map[VIS[j]] == 1:
                    fid.write('\\fill[orange] ('+str(7*j+2.5)+',-1.75) rectangle+(1,0.5);'+'\n')
                    fid.write('\\fill[orange] ('+str(7*j-1)+',-0.75) rectangle+(1,0.5);'+'\n')
            for j in range(16):
                if self.var_value_map[VX[j]] == 1:
                    if j % 2 == 0:
                        x = 7*(j//2)
                    if j % 2 == 1:
                        x = 4 + 7*(j//2)
                    fid.write('\\fill[orange] ('+str(x)+',0) rectangle+(1,1);'+'\n')
            fid.write('\\end{scope}'+'\n'+'\n')

        for i in [self.BR]:
            X = _Z(TWINE.genVars_input(0))
            fid.write('\\begin{scope}[yshift = -'+str(i*5)+'cm]'+'\n')
            for j in range(16):
                if self.var_value_map[X[j]] == 1:
                    if j % 2 == 0:
                        x = 7*(j//2)
                    if j % 2 == 1:
                        x = 4 + 7*(j//2)
                    fid.write('\\fill[orange] ('+str(x)+',0) rectangle+(1,1);'+'\n')
            fid.write('\\end{scope}'+'\n'+'\n')
#fill before the distinguisher


        for i in range(self.FR):
            GIS = _Z(TWINE.genVars_inputSbox(i+self.TR))
            X = _Y(TWINE.genVars_input(i+self.TR))
            fid.write('\\begin{scope}[yshift = -'+str((i+self.BR+1)*5)+'cm]'+'\n')
            for j in range(8):
                if self.var_value_map[GIS[j]] == 1:
                    fid.write('\\fill[orange] ('+str(7*j+2.5)+',-1.75) rectangle+(1,0.5);'+'\n')
                    fid.write('\\fill[orange] ('+str(7*j-1)+',-0.75) rectangle+(1,0.5);'+'\n')
            for j in range(16):
                if self.var_value_map[X[j]] == 1:
                    if j % 2 == 0:
                        x = 7*(j//2)
                    if j % 2 == 1:
                        x = 4 + 7*(j//2)
                    fid.write('\\fill[orange] ('+str(x)+',0) rectangle+(1,1);'+'\n')
            fid.write('\\end{scope}'+'\n'+'\n')

        for i in [self.FR]:
            X = _Y(TWINE.genVars_input(i+self.TR))
            fid.write('\\begin{scope}[yshift = -'+str((i+self.BR+1)*5)+'cm]'+'\n')
            for j in range(16):
                if self.var_value_map[X[j]] == 1:
                    if j % 2 == 0:
                        x = 7*(j//2)
                    if j % 2 == 1:
                        x = 4 + 7*(j//2)
                    fid.write('\\fill[orange] ('+str(x)+',0) rectangle+(1,1);'+'\n')
            fid.write('\\end{scope}'+'\n'+'\n')
        fid.write('\n'+'\\end{tikzpicture}'+'\n'+'\\end{document}')
        fid.close()











