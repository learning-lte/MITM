
from MITMAES import * 


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
        
        AES = MITM_AES("AES", 8, 128, self.Round, 8, 128)
        Solution = self.var_value_map
        fid = open(outputfile,'w')
        fid.write('\\documentclass{standalone}'+'\n'+'\\usepackage{tikz}'+'\n'+'\\usepackage{calc}'+'\n'+'\\usepackage{pgffor}'+'\n'+'\\usetikzlibrary{patterns}'+'\n'+'\\begin{document}'+'\n'+'\\begin{tikzpicture}[scale=0.35]'+'\n')

        for i in range(self.Round//2):
            for j in range(2):
                if i !=0 or j !=0:
                    GState = _Z(AES.genVars_input_of_round(2*i+j))

                    fid.write('\\begin{scope}[yshift ='+str(- i* 8)+' cm, xshift =' +str(j*14)+' cm]'+'\n')
                    for g in range(16):
                        row = 3-g//4
                        col = g%4
                        if Solution[GState[g]] ==1:
                            fid.write('\\fill[red]('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')

                    fid.write('\n'+'\\end{scope}'+'\n')
                    
                    
        if self.Round%2 == 1:
            
            for i in [self.Round//2]:
                for j in [0]:
                    GState = _Z(AES.genVars_input_of_round(2*i+j))
                    fid.write('\\begin{scope}[yshift ='+str(- i* 8)+' cm, xshift =' +str(j*14)+' cm]'+'\n')
                    for g in range(16):
                        row = 3-g//4
                        col = g%4
                        if Solution[GState[g]] ==1:
                            fid.write('\\fill[red]('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')

                    fid.write('\n'+'\\end{scope}'+'\n')
            

        for i in range(self.Round//2):
            for j in range(2):
                State = _X(AES.genVars_input_of_round(2*i+j))
                Rtate = _X(AES.genVars_input_of_MixColumn(2*i+j))
                DState = _Y(AES.genVars_input_of_round(2*i+j))
                DRtate = _Y(AES.genVars_input_of_MixColumn(2*i+j))

                fid.write('\\begin{scope}[yshift ='+str(- i* 8)+' cm, xshift =' +str(j*14)+' cm]'+'\n')
                for g in range(16):
                    row = 3-g//4
                    col = g%4
                    if Solution[State[g]] ==1:
                        fid.write('\\fill[pattern = north east lines]('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    if Solution[Rtate[g]] == 1:
                        fid.write('\\fill[pattern = north east lines]('+str(col+8)+','+str(row)+') rectangle +(1,1);'+'\n')
                    if Solution[DState[g]] ==1:
                        fid.write('\\fill[pattern = north west lines]('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    if Solution[DRtate[g]] == 1:
                        fid.write('\\fill[pattern = north west lines]('+str(col+8)+','+str(row)+') rectangle +(1,1);'+'\n')
                fid.write('\n'+'\\end{scope}'+'\n')


        
        for i in [self.Round//2]:
            for j in range(self.Round%2 + 1):
                State = _X(AES.genVars_input_of_round(2*i+j))
                DState = _Y(AES.genVars_input_of_round(2*i+j))


                fid.write('\\begin{scope}[yshift ='+str(- i* 8)+' cm, xshift =' +str(j*14)+' cm]'+'\n')
                for g in range(16):
                    row = 3-g//4
                    col = g%4
                    if Solution[State[g]] ==1:
                        fid.write('\\fill[pattern = north east lines]('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')

                    if Solution[DState[g]] ==1:
                        fid.write('\\fill[pattern = north west lines]('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                if self.Round%2 == 1 and j == 0:
                    Rtate = _X(AES.genVars_input_of_MixColumn(2*i+j))
                    DRtate = _Y(AES.genVars_input_of_MixColumn(2*i+j))
                    for g in range(16):
                        row = 3-g//4
                        col = g%4
                        if Solution[Rtate[g]] ==1:
                            fid.write('\\fill[pattern = north east lines]('+str(col + 8)+','+str(row)+') rectangle +(1,1);'+'\n')

                        if Solution[DRtate[g]] ==1:
                            fid.write('\\fill[pattern = north west lines]('+str(col + 8)+','+str(row)+') rectangle +(1,1);'+'\n')                    
                        

                fid.write('\n'+'\\end{scope}'+'\n')

##        fid.write('\\begin{scope}[yshift ='+str(-(self.Round//2)* 8)+' cm]'+'\n')
##        fid.write('\\draw[step = 1] (0,0) grid + (4,4);'+'\n')
##        fid.write('\draw (2,4) node[above] {\\scriptsize Round '+str(self.Round) +'};'+'\n')
##
##        fid.write('\\end{scope}')


        fid.write('\\foreach \z in {0')
        for i in range(1,self.Round//2):
            fid.write(','+str(i))
        fid.write('}{'+'\n')
        fid.write('\\begin{scope}[yshift = -\z* 8 cm]'+'\n')
        fid.write('\\foreach \\x  in {0,8,14,22}'+'\n'+'\\draw[step = 1] (\\x,0) grid + (4,4);'+'\n')
        fid.write('\\foreach \\x in {0,14}'+'\n'+'{\\draw[->] (\\x+4,2) --node[above]{\scriptsize $SB,SR$}+(4,0);'+ '\n'+'\\node[below] at (\\x+6,2) {\\scriptsize $AK$};'+'\n'+'\\draw[->] (\\x+12,2) --node[above] {\\scriptsize $MC$}+(2,0);}'+'\n')
        fid.write('\\draw (2,4) node[above] {\\scriptsize Round \pgfmathparse{int(\\z*2)}\pgfmathresult };'+'\n'+ '\\draw (16,4) node[above] {\\scriptsize Round  \pgfmathparse{int(\\z*2+1)}\\pgfmathresult};'+'\n')
        fid.write('\\draw (28,2) |- ++(-30,-4);'+'\draw[->] (-2,-2)|-+(2,-4);'+'\n'+'\\end{scope}')
        fid.write('\n'+'}'+'\n')

        if self.Round%2 == 0:
            for i in [self.Round//2]:
                fid.write('\\begin{scope}[yshift ='+ str(-(i)* 8) +'cm]'+'\n')
                fid.write('\\draw (2,4) node[above] {\\scriptsize Round '+str(2*i)+'};'+'\n')
                fid.write('\\foreach \\x  in {0}'+'\n'+'\\draw[step = 1] (\\x,0) grid + (4,4);'+'\n')
                fid.write('\n'+'\\end{scope}')
        if self.Round%2 == 1:
            for i in [self.Round//2]:
                fid.write('\\begin{scope}[yshift ='+ str(-(i)* 8) +'cm]'+'\n')
                fid.write('\\draw (2,4) node[above] {\\scriptsize Round '+str(2*i)+'};'+'\n')
                fid.write('\\foreach \\x  in {0,8,14}'+'\n'+'\\draw[step = 1] (\\x,0) grid + (4,4);'+'\n')
                fid.write('\\foreach \\x in {0}'+'\n'+'{\\draw[->] (\\x+4,2) --node[above]{\scriptsize $SB,SR$}+(4,0);'+ '\n'+'\\node[below] at (\\x+6,2) {\\scriptsize $AK$};'+'\n')
                fid.write('\\draw[->] (\\x+12,2) --node[above] {\\scriptsize $MC$}+(2,0);}'+'\n')
                fid.write('\\draw (2,4) node[above] {\\scriptsize Round '+str(2*i)+'};'+'\n'+ '\\draw (16,4) node[above] {\\scriptsize Round '+str(2*i+1)+'};'+'\n')
                fid.write('\n'+'\\end{scope}')


        fid.write('\\end{tikzpicture}'+'\n'+'\\end{document}')
        fid.close()







