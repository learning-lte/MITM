

from CPMITM import *
from MITMSKINNY import *
MC = [[1,0,1,1],[1,0,0,0],[0,1,1,0],[1,0,1,0]]
Inv_MC = [[0,1,0,0],[0,1,1,1],[0,1,0,1],[1,0,0,1]] #inverse of MC

class DrawDistinguisher():
    def __init__(self,solutionFile,totalRounds):
        print('in init()')
        solFile = open(solutionFile,'r')
        self.Round= totalRounds
        self.var_value_map = dict()
        for line in solFile:
            if line[0] != '#':
                temp = line
                temp = temp.replace('-', ' ')
                temp = temp.split()
                self.var_value_map[temp[0]] = int(temp[1])

    def draw(self,outputfile):
        Solution = self.var_value_map
        fid = open(outputfile,'w')
        fid.write('\\documentclass{standalone}'+'\n'+'\\usepackage{tikz}'+'\n'+'\\usepackage{calc}'+'\n'+'\\usepackage{pgffor}'+'\n'+'\\usetikzlibrary{patterns}'+'\n'+'\\begin{document}'+'\n'+'\\begin{tikzpicture}[scale=0.35]'+'\n')
        SKINNY = MITM_SKINNY("SKINNY", 8, 128, self.Round, 8, 128)
        _X = BasicTools.typeX
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ
        for i in range(1,self.Round//2):
            for j in range(2):
                if i !=0 or j !=0:
                    GState = _Z(SKINNY.genVars_input_of_round(2*i+j))

                    pu1 = SKINNY.genVars_cutting1(2*i+j-1)
                    pu2 = SKINNY.genVars_cutting2(2*i+j-1)

                    fid.write('\\begin{scope}[yshift ='+str(- i* 8)+' cm, xshift =' +str(j*14)+' cm]'+'\n')


                    for g in range(16):
                        row = 3-g//4
                        col = g%4
                        if Solution[GState[g]] ==1:
                            fid.write('\\fill[red]('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    for p in range(4):
                        if Solution[pu1[p]] == 1:
                            #print(pu1[p],Solution[pu1[p]])
                            fid.write('\\fill[blue]('+str(p)+','+str(3-1)+') rectangle +(1,1);'+'\n')
                        if Solution[pu2[p]] == 1:
                            #print(pu2[p],Solution[pu2[p]])
                            fid.write('\\fill[blue]('+str(p)+','+str(3-0)+') rectangle +(1,1);'+'\n')
                    fid.write('\n'+'\\end{scope}'+'\n')

        fid.write('\\foreach \z in {0')
        for i in range(1,self.Round//2):
            fid.write(','+str(i))
        fid.write('}{'+'\n')
        fid.write('\\begin{scope}[yshift = -\z* 8 cm]'+'\n')
        fid.write('\\foreach \\x  in {0,8,14,22}'+'\n'+'\\draw[step = 1] (\\x,0) grid + (4,4);'+'\n')
        fid.write('\\foreach \\x in {0,14}'+'\n'+'{\\draw[->] (\\x+4,2) --node[above]{\scriptsize $SB,AC$}+(4,0);'+ '\n'+'\\node[below] at (\\x+6,2) {\\scriptsize $AK,SR$};'+'\n'+'\\draw[->] (\\x+12,2) --node[above] {\\scriptsize $MC$}+(2,0);}'+'\n')
        fid.write('\\draw (2,4) node[above] {\\scriptsize Round \pgfmathparse{int(\\z*2)}\pgfmathresult };'+'\n'+ '\\draw (16,4) node[above] {\\scriptsize Round  \pgfmathparse{int(\\z*2+1)}\\pgfmathresult};'+'\n')
        fid.write('\\draw (28,2) |- ++(-30,-4);'+'\draw[->] (-2,-2)|-+(2,-4);'+'\n'+'\\end{scope}')
        fid.write('\n'+'}'+'\n')




        for i in range(self.Round//2):
            for j in range(2):
                State = _X(SKINNY.genVars_input_of_round(2*i+j))
                Rtate = _X(SKINNY.genVars_input_of_MixColumn(2*i+j))
                DState = _Y(SKINNY.genVars_input_of_round(2*i+j))
                DRtate = _Y(SKINNY.genVars_input_of_MixColumn(2*i+j))

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
        if self.Round%2 == 1:
            for i in [self.Round//2]:
                fid.write('\\begin{scope}[yshift ='+str(- i* 8)+' cm]'+'\n')
                fid.write('\\foreach \\x  in {0,8,14,22}'+'\n'+'\\draw[step = 1] (\\x,0) grid + (4,4);'+'\n')
                fid.write('\\foreach \\x in {0,14}'+'\n'+'{\\draw[->] (\\x+4,2) --node[above]{\scriptsize $SB,AC$}+(4,0);'+ '\n'+'\\node[below] at (\\x+6,2) {\\scriptsize $AK,SR$};'+'\n')
                fid.write('\\draw[->] (12,2) --node[above] {\\scriptsize $MC$}+(2,0);}'+'\n')
                fid.write('\\draw (2,4) node[above] {\\scriptsize Round '+str(2*i)+' };'+'\n'+ '\\draw (16,4) node[above] {\\scriptsize Round'+str(2*i+1)+'};'+'\n')
                fid.write('\end{scope}'+'\n')
        if self.Round%2 == 0:
            for i in [self.Round//2]:
                fid.write('\\begin{scope}[yshift ='+str(- i* 8)+' cm]'+'\n')
                fid.write('\\foreach \\x  in {0,8}'+'\n'+'\\draw[step = 1] (\\x,0) grid + (4,4);'+'\n')
                fid.write('\\foreach \\x in {0}'+'\n'+'{\\draw[->] (\\x+4,2) --node[above]{\scriptsize $SB,AC$}+(4,0);'+ '\n'+'\\node[below] at (\\x+6,2) {\\scriptsize $AK,SR$};}'+'\n')
                fid.write('\\draw (2,4) node[above] {\\scriptsize Round '+str(2*i)+' };'+'\n')
                fid.write('\end{scope}'+'\n')

        for i in [self.Round//2]:
            if self.Round%2 == 1:
                Cols = [0,1]
            else:
                Cols = [0]
            for j in Cols:
                GState = _Z(SKINNY.genVars_input_of_round(2*i+j))
                pu1 = SKINNY.genVars_cutting1(2*i+j)
                pu2 = SKINNY.genVars_cutting2(2*i+j)
                fid.write('\\begin{scope}[yshift ='+str(- i* 8)+' cm, xshift =' +str(j*14)+' cm]'+'\n')

                for g in range(16):
                    row = 3-g//4
                    col = g%4
                    if Solution[GState[g]] == 1:
                        fid.write('\\fill[red]('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')

                fid.write('\n'+'\\end{scope}'+'\n')


        for i in [self.Round//2]:
            if self.Round%2 == 1:
                Cols = [0,1]
            else:
                Cols = [0]
            for j in Cols:
                State = _X(SKINNY.genVars_input_of_round(2*i+j))
                DState = _Y(SKINNY.genVars_input_of_round(2*i+j))


                fid.write('\\begin{scope}[yshift ='+str(- i* 8)+' cm, xshift =' +str(j*14)+' cm]'+'\n')
                for g in range(16):
                    row = 3-g//4
                    col = g%4
                    if Solution[State[g]] ==1:
                        fid.write('\\fill[pattern = north east lines]('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                        fid.write('\\fill[pattern = north east lines]('+str((col+g//4)%4+8)+','+str(row)+') rectangle +(1,1);'+'\n')
                    if Solution[DState[g]] ==1:
                        fid.write('\\fill[pattern = north west lines]('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                        fid.write('\\fill[pattern = north west lines]('+str((col+g//4)%4+8)+','+str(row)+') rectangle +(1,1);'+'\n')
                fid.write('\n'+'\\end{scope}'+'\n')

##        if self.Round %2==0:
##            fid.write('\\begin{scope}[yshift ='+str(-(self.Round//2)* 8)+' cm]'+'\n')
##            fid.write('\\draw[step = 1] (0,0) grid + (4,4);'+'\n')
##            fid.write('\draw (2,4) node[above] {\\scriptsize Round '+str(self.Round+1) +'};'+'\n')
##            fid.write('\draw[->] (4,2) --node[above]{\\scriptsize $SB,AC$}+(4,0);'+'\n')
##            fid.write('\\node[below] at (6,2) {\\scriptsize $AK,SR$};'+'\n')
##            fid.write('\\draw (8,0) grid +(4,4);'+'\n')
##            #fid.write('\\node[below] at (10,0) {\\scriptsize Objval:'+str(Solution['objval'])+'};'+'\n')
##            fid.write('\\end{scope}')


        fid.write('\n'+'\\end{tikzpicture}'+'\n'+'\\end{document}')
        fid.close()








