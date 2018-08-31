
from MITMToy import * 


class DrawKeyrecovery():
    def __init__(self, solutionFile, totalRounds, backwardRounds, forwardRounds):
        print('in init()')
        solFile = open(solutionFile,'r')
        self.Round = totalRounds
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
        
        Toy = MITM_Toy("Toy", 8, 32, self.Round, 8, 128)
        Solution = self.var_value_map
        fid = open(outputfile,'w')
        fid.write('\\documentclass{standalone}'+'\n'+'\\usepackage{tikz}'+'\n'+'\\usepackage{calc}'+'\n'+'\\usepackage{pgffor}'+'\n'+'\\usetikzlibrary{patterns}'+'\n'+'\\begin{document}'+'\n'+'\\begin{tikzpicture}[scale=0.35]'+'\n')
        
        for i in range(0, self.BR + 1):
            S = _X(Toy.genVars_input_of_round(-i))   
                 
            fid.write('\\begin{scope}[yshift = '+str(-(-i+1)*5)+'cm]'+'\n')
            for j in range(4):
                if Solution[S[j]] == 1:
                    fid.write('\\fill[orange]('+str(j)+',0) rectangle+(1,1);'+'\n')
                
            fid.write('\\end{scope}'+'\n')        
        
        for i in range(self.FR+1):
              
            DS = _Y(Toy.genVars_input_of_round(self.Round + i))            
            fid.write('\\begin{scope}[yshift = '+str(-(i +  self.BR)*5 - 2)+'cm]'+'\n')
            for j in range(4):

                if Solution[DS[j]] == 1:
                    fid.write('\\fill[orange]('+str(j)+',0) rectangle+(1,1);'+'\n')
            fid.write('\\end{scope}'+'\n')


        for i in [0]:
            fid.write('\\begin{scope}[yshift ='+str(-i*5)+' cm]'+'\n')
            fid.write('\\draw (0,0) grid +(4,1);'+ '\n')
            fid.write('\\foreach \y in {0,1,2,3}{')
            fid.write('\\draw[->](2,0)--+(0,-0.5);'+'\n')
            fid.write('\\draw(\y,-1.5) rectangle node{\\tiny{$S$}} +(1,1);'+'\n')
            fid.write('}'+'\n')
            fid.write('\\draw (0,-2.5) rectangle node{\\tiny{MC}} +(4,1);'+'\n')
            fid.write('\\draw[->] (2,-2.5)--+(0,-0.5);'+'\n')
            fid.write('\\draw (1.75,-3.25)--+(0.5,0);'+ '\n')
            fid.write('\\draw (2,-3.25) circle (0.25);' +'\n')
            fid.write('\\draw (4,-3.25) --(2.25,-3.25);'+'\n')
            fid.write('\\node[right] at (4,-3.25) {\\tiny{$K_0$}};'+'\n')
            fid.write('\\draw[->](2,-3)--+(0,-1);'+'\n')           
            fid.write('\\end{scope}' + '\n')     
        fid.write('\\draw(0,-5) grid +(4,1);' + '\n')
        fid.write('\\node at (2,-5.5){\\tiny{Distinguisher}};'+'\n')
        for i in [1,2]:
            fid.write('\\begin{scope}[yshift ='+str(-i*5-2)+' cm]'+'\n')
            fid.write('\\draw (0,0) grid +(4,1);'+ '\n')
            fid.write('\\foreach \y in {0,1,2,3}{')
            fid.write('\\draw[->](2,0)--+(0,-0.5);'+'\n')
            fid.write('\\draw(\y,-1.5) rectangle node{\\tiny{$S$}} +(1,1);'+'\n')
            fid.write('}'+'\n')
            fid.write('\\draw (0,-2.5) rectangle node{\\tiny{MC}} +(4,1);'+'\n')
            fid.write('\\draw[->] (2,-2.5)--+(0,-0.5);'+'\n')
            fid.write('\\draw (1.75,-3.25)--+(0.5,0);'+ '\n')
            fid.write('\\draw (2,-3.25) circle (0.25);' +'\n')
            fid.write('\\draw (4,-3.25) --(2.25,-3.25);'+'\n')
            fid.write('\\node[right] at (4,-3.25) {\\tiny{$K_'+str(3+i)+'$}};'+'\n')
            fid.write('\\draw[->](2,-3)--+(0,-1);'+'\n')           
            fid.write('\\end{scope}' + '\n')
        fid.write('\\draw (0,-17) grid +(4,1);'+ '\n')     
        


        fid.write('\\end{tikzpicture}'+'\n'+'\\end{document}')
        fid.close()








