
from MITMAES import * 


class DrawKeyrecovery():
    def __init__(self, solutionFile, totalRounds, backwardRounds, forwardRounds):
        print('in init()')
        solFile = open(solutionFile,'r')
        self.TR = totalRounds
        self.FR = forwardRounds
        self.BR = backwardRounds
        self.var_value_map = dict()
        for line in solFile:
            if line[0] != '#':
                temp = line
                temp = temp.replace('-', ' ')
                temp = temp.split()
                self.var_value_map[temp[0]] = int(temp[1])

    def draw(self,outputfile):
        Solution = self.var_value_map
        
        _X = BasicTools.typeX
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ
        
        AES = MITM_AES("AES", 8, 128, self.TR, 8, 128)
        
        fid = open(outputfile,'w')
        fid.write('\\documentclass{standalone}'+'\n'+'\\usepackage{tikz}'+'\n'+'\\usepackage{calc}'+'\n'+'\\usepackage{pgffor}'+'\n'+'\\usetikzlibrary{patterns}'+'\n'+'\\begin{document}'+'\n'+'\\begin{tikzpicture}[scale=0.35]'+'\n')
              
        
        for i in range(self.BR//2):
            for j in range(2):
                FGR = _X(AES.genVars_input_of_MixColumn(-(self.BR - (2*i+j))))
                FGS = _X(AES.genVars_input_of_round(-(self.BR - (2*i+j))))


                fid.write('\\begin{scope}[yshift ='+str(- i* 8)+' cm, xshift =' +str(j*14)+' cm]'+'\n')
                for g in range(16):
                    row = 3-g//4
                    col = g%4
                    if Solution[FGS[g]] ==1:
                        fid.write('\\fill[red]('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    if Solution[FGR[g]] == 1:
                        fid.write('\\fill[red]('+str(col+8)+','+str(row)+') rectangle +(1,1);'+'\n')

                fid.write('\n'+'\\end{scope}'+'\n')


        for i in [self.BR//2]:
            if self.BR%2 == 1:
                Cols = [0,1]
            else:
                Cols = [0]
            for j in Cols:

                FGS = _X(AES.genVars_input_of_round(-(self.BR - (2*i+j))))


                fid.write('\\begin{scope}[yshift ='+str(- i* 8)+' cm, xshift =' +str(j*14)+' cm]'+'\n')
                for g in range(16):
                    row = 3-g//4
                    col = g%4
                    if Solution[FGS[g]] ==1:
                        fid.write('\\fill[red]('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    if self.BR%2 == 1 and j == 0:
                        FGR = _X(AES.genVars_input_of_MixColumn(-(self.BR - (2*i+j))))
                        
                        if Solution[FGR[g]] ==1:
                            fid.write('\\fill[red]('+str(col+8)+','+str(row)+') rectangle +(1,1);'+'\n')
                fid.write('\n'+'\\end{scope}'+'\n') 
#above is the fillment of the backward differential

       
#following is the structure of backward keyrecovery  
        if self.BR//2 >= 1:
            
            fid.write('\\foreach \z in {0')
            for i in range(1, self.BR//2):
                fid.write(','+str(i))
            fid.write('}{'+'\n')
            fid.write('\\begin{scope}[yshift = -\z* 8 cm]'+'\n')
            fid.write('\\foreach \\x  in {0,8,14,22}'+'\n'+'\\draw[step = 1] (\\x,0) grid + (4,4);'+'\n')
            fid.write('\\foreach \\x in {0,14}'+'\n'+'{\\draw[->] (\\x+4,2) --node[above]{\scriptsize $SB,SR$}+(4,0);'+'\n'+'\\draw[->] (\\x+12,2) --node[above] {\\scriptsize $MC$}+(2,0);}'+'\n')

            fid.write('\\node[below] at (\\x+13,2) {\\scriptsize $AK$};'+'\n')
            fid.write('\\draw (2,4) node[above] {\\scriptsize Round \pgfmathparse{int(\\z*2)}\pgfmathresult };'+'\n'+ '\\draw (16,4) node[above] {\\scriptsize Round  \pgfmathparse{int(\\z*2+1)}\\pgfmathresult};'+'\n')
            fid.write('\\draw (28,2) |- ++(-30,-4);'+'\draw[->] (-2,-2)|-+(2,-4);'+'\n'+'\\end{scope}')
            fid.write('\n'+'}'+'\n')

        if self.BR%2 == 1:
            for i in [self.BR//2]:
                fid.write('\\begin{scope}[yshift ='+str(- i* 8)+' cm]'+'\n')
                fid.write('\\foreach \\x  in {0,8,14}'+'\n'+'\\draw[step = 1] (\\x,0) grid + (4,4);'+'\n')
                fid.write('\\foreach \\x in {0}'+'\n'+'{\\draw[->] (\\x+4,2) --node[above]{\scriptsize $SB,SR$}+(4,0);'+ '\n')
                fid.write('\\draw[->] (\\x+12,2) --node[above] {\\scriptsize $MC$}+(2,0);'+'\n')
                fid.write('\\node[below] at (\\x+13,2) {\\scriptsize $AK$};'+'\n')
                fid.write('}'+'\n')
                fid.write('\\draw (2,4) node[above] {\\scriptsize Round '+str(2*i)+' };'+'\n')
                fid.write('\\draw (16,4) node[above] {\\scriptsize Round'+str(2*i+1)+'};'+'\n')

                fid.write('\\draw (18,2)--(28,2);'+'\n')
                fid.write('\\draw (28,2) |- ++(-30,-4);'+'\n')
                fid.write('\\draw[->] (-2,-2)|-+(8,-4);'+'\n')

                fid.write('\end{scope}'+'\n')

        if self.BR%2 == 0:
            for i in [self.BR//2]:
                fid.write('\\begin{scope}[yshift ='+str(- i* 8)+' cm]'+'\n')
                fid.write('\\foreach \\x  in {0}'+'\n'+'\\draw[step = 1] (\\x,0) grid + (4,4);'+'\n')
                fid.write('\\draw (2,4) node[above] {\\scriptsize Round '+str(2*i)+' };'+'\n')

                fid.write('\\draw[->] (4,2)--+(2,0);'+'\n')

                fid.write('\end{scope}'+'\n')
#above is the structure of backward keyrecovery        
        
        
        if self.BR%2 == 0:
            ysh = self.BR//2
        else:
            ysh = self.BR//2 +1     
        
        
        for j in [self.TR]:
            GS = _Y(AES.genVars_input_of_round(self.TR))
        fid.write('\\begin{scope}[yshift = '+str(-ysh *8)+' cm];'+'\n')

        #fid.write('\\node[above] at (11,1.2){\\scripsize $\\cdots$ 11-round Distinguisher $\\cdots$};'+'\n')
        fid.write('\\draw[->] (18,2) --node[left=50pt]{\\scriptsize $\\cdots$  Distinguisher $\\cdots$} (28,2);'+'\n')

        fid.write('\\draw (28,2) |- ++(-30,-4);'+'\n')
        fid.write('\\draw[->] (-2,-2)|-+(2,-4);'+'\n')
        fid.write('\\end{scope}'+'\n')   
        
        
        for i in range((self.FR)//2):
            for j in range(2):
                GR = _Y(AES.genVars_input_of_MixColumn((2*i+j) + self.TR))
                GS = _Y(AES.genVars_input_of_round((2*i+j) + self.TR))

                fid.write('\\begin{scope}[yshift ='+str(- (i+ysh+1)* 8)+' cm, xshift =' +str(j*14)+' cm]'+'\n')
                fid.write('\\draw (2,4) node[above] {\\scriptsize Round '+str((2*i+j)+self.TR+self.BR)+' };'+'\n')
                for g in range(16):
                    row = 3-g//4
                    col = g%4
                    if Solution[GS[g]] ==1:
                        fid.write('\\fill[red]('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    if Solution[GR[g]] == 1:
                        fid.write('\\fill[red]('+str(col+8)+','+str(row)+') rectangle +(1,1);'+'\n')

                fid.write('\n'+'\\end{scope}'+'\n')


        for i in [(self.FR)//2]:
            if (self.FR)%2 == 1:
                Cols = [0,1]
            else:
                Cols = [0]
            for j in Cols:
                GS = _Y(AES.genVars_input_of_round((2*i+j) + self.TR))

                fid.write('\\begin{scope}[yshift ='+str(-(i+ysh+1)* 8)+' cm, xshift =' +str(j*14)+' cm]'+'\n')
                fid.write('\\draw (2,4) node[above] {\\scriptsize Round '+str((2*i+j)+self.TR+self.BR)+' };'+'\n')
                for g in range(16):
                    row = 3-g//4
                    col = g%4
                    if Solution[GS[g]] ==1:
                        fid.write('\\fill[red]('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    if (self.FR)%2 == 1 and j == 0:
                        GR = _Y(AES.genVars_input_of_MixColumn((2*i+j) + self.TR))
                        if Solution[GR[g]] ==1:
                            fid.write('\\fill[red]('+str(col+8)+','+str(row)+') rectangle +(1,1);'+'\n')
                fid.write('\n'+'\\end{scope}'+'\n')
#above is the fillment of backward

        fid.write('\\foreach \z in {'+str(ysh+1))
        for i in range(1,(self.FR)//2):
            fid.write(','+str(i+ysh+1))
        fid.write('}{'+'\n')
        fid.write('\\begin{scope}[yshift = -\z* 8 cm]'+'\n')
        fid.write('\\foreach \\x  in {0,8,14,22}'+'\n'+'\\draw[step = 1] (\\x,0) grid + (4,4);'+'\n')
        fid.write('\\foreach \\x in {0,14}'+'\n'+'{\\draw[->] (\\x+4,2) --node[above]{\scriptsize $SB,SR$}+(4,0);'+ '\n'+'\\node[below] at (\\x+6,2) {\\scriptsize $AK$};'+'\n'+'\\draw[->] (\\x+12,2) --node[above] {\\scriptsize $MC$}+(2,0);}'+'\n')

        fid.write('\\draw (28,2) |- ++(-30,-4);'+'\draw[->] (-2,-2)|-+(2,-4);'+'\n'+'\\end{scope}')
        fid.write('\n'+'}'+'\n')

        if (self.FR)%2 == 1:
            for i in [(self.FR)//2]:
                fid.write('\\begin{scope}[yshift ='+str(- (i+ysh+1)* 8)+' cm]'+'\n')
                fid.write('\\foreach \\x  in {0,8,14}'+'\n'+'\\draw[step = 1] (\\x,0) grid + (4,4);'+'\n')
                fid.write('\\foreach \\x in {0}'+'\n'+'{\\draw[->] (\\x+4,2) --node[above]{\scriptsize $SB,SR$}+(4,0);'+ '\n'+'\\node[below] at (\\x+6,2) {\\scriptsize $AK$};'+'\n')
                fid.write('\\draw[->] (\\x+12,2) --node[above] {\\scriptsize $MC$}+(2,0);'+'\n')
                fid.write('}'+'\n')

#                fid.write('\\draw (16,4) node[above] {\\scriptsize C};'+'\n')
                fid.write('\end{scope}'+'\n')

        if (self.FR)%2 == 0:
            for i in [(self.FR)//2]:
                fid.write('\\begin{scope}[yshift ='+str(- (i+ysh+1)* 8)+' cm]'+'\n')
                fid.write('\\foreach \\x  in {0}'+'\n'+'\\draw[step = 1] (\\x,0) grid + (4,4);'+'\n')
#                fid.write('\\draw (2,4) node[above] {\\scriptsize C };'+'\n')

                fid.write('\end{scope}'+'\n')

        fid.write('\n'+'\\end{tikzpicture}'+'\n'+'\\end{document}')
        fid.close()


    def drawGuessedValue(self, outputfile):

        Solution = self.var_value_map
        
        _X = BasicTools.typeX
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ
        
        AES = MITM_AES("AES", 8, 128, self.TR, 8, 128)
        
        fid = open(outputfile,'w')
        fid.write('\\documentclass{standalone}'+'\n'+'\\usepackage{tikz}'+'\n'+'\\usepackage{calc}'+'\n'+'\\usepackage{pgffor}'+'\n'+'\\usetikzlibrary{patterns}'+'\n'+'\\begin{document}'+'\n'+'\\begin{tikzpicture}[scale=0.35]'+'\n')
              
        
        for i in range(self.BR//2):
            for j in range(2):
                FSR = _Z(AES.genVars_input_of_MixColumn(-(self.BR - (2*i+j))))
                FS = _Z(AES.genVars_input_of_round(-(self.BR - (2*i+j))))


                fid.write('\\begin{scope}[yshift ='+str(- i* 8)+' cm, xshift =' +str(j*14)+' cm]'+'\n')
                for g in range(16):
                    row = 3-g//4
                    col = g%4
                    if Solution[FS[g]] ==1:
                        fid.write('\\fill[orange]('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    if Solution[FSR[g]] == 1:
                        fid.write('\\fill[orange]('+str(col+8)+','+str(row)+') rectangle +(1,1);'+'\n')
                fid.write('\n'+'\\end{scope}'+'\n')


                fid.write('\\begin{scope}[yshift ='+str(- i* 8)+' cm]'+'\n')
                for g in range(16):
                    row = 3-g//4
                    col = g%4
                    if Solution[FS[g]] ==1:
                        if j == 0:
                            fid.write('\\fill[orange]('+str(col-7)+','+str(row-2)+') rectangle +(1,1);'+'\n')
                        if j == 1:
                            fid.write('\\fill[orange]('+str(col+29)+','+str(row+3)+') rectangle +(1,1);'+'\n')
                fid.write('\n'+'\\end{scope}'+'\n')






        for i in [self.BR//2]:
            if self.BR%2 == 1:
                Cols = [0,1]
            else:
                Cols = [0]
            for j in Cols:

                FS = _Z(AES.genVars_input_of_round(-(self.BR - (2*i+j))))
                fid.write('\\begin{scope}[yshift ='+str(- i* 8)+' cm, xshift =' +str(j*14)+' cm]'+'\n')
                for g in range(16):
                    row = 3-g//4
                    col = g%4
                    if Solution[FS[g]] ==1:
                        fid.write('\\fill[orange]('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    if self.BR%2 == 1 and j == 0:
                        FSR = _Z(AES.genVars_input_of_MixColumn(-(self.BR - (2*i+j))))
                        
                        if Solution[FS[g]] ==1:
                            fid.write('\\fill[orange]('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                        if Solution[FSR[g]] ==1:
                            fid.write('\\fill[orange]('+str(col+8)+','+str(row)+') rectangle +(1,1);'+'\n')
                fid.write('\n'+'\\end{scope}'+'\n')

            if self.BR%2 == 1:
                FS = _Z(AES.genVars_input_of_round(-(self.BR - (2*i))))
                fid.write('\\begin{scope}[yshift ='+str(- i* 8)+' cm]'+'\n')
                for g in range(16):

                    row = 3-g//4
                    col = g%4
                    if Solution[FS[g]] ==1:
                        fid.write('\\fill[orange]('+str(col-7)+','+str(row-2)+') rectangle +(1,1);'+'\n')
                fid.write('\end{scope}'+'\n')  

#above is the fill backward process

        if self.BR//2 >= 1:
            
            fid.write('\\foreach \z in {0')
            for i in range(1, self.BR//2):
                fid.write(','+str(i))
            fid.write('}{'+'\n')
            fid.write('\\begin{scope}[yshift = -\z* 8 cm]'+'\n')
            fid.write('\\foreach \\x  in {0,8,14,22}'+'\n'+'\\draw[step = 1] (\\x,0) grid + (4,4);'+'\n')
            fid.write('\\foreach \\x in {0,14}'+'\n'+'{\\draw[->] (\\x+4,2) --node[above]{\scriptsize $SB,SR$}+(4,0);'+'\n'+'\\draw[->] (\\x+12,2) --node[above] {\\scriptsize $MC$}+(2,0);}'+'\n')
            fid.write('\\node[below] at (\\x+13,2) {\\scriptsize $AK$};'+'\n')
            fid.write('\\draw (2,4) node[above] {\\scriptsize Round \pgfmathparse{int(\\z*2)}\pgfmathresult };'+'\n'+ '\\draw (16,4) node[above] {\\scriptsize Round  \pgfmathparse{int(\\z*2+1)}\\pgfmathresult};'+'\n')
            fid.write('\\draw (28,2) |- ++(-30,-4);'+'\draw[->] (-2,-2)|-+(2,-4);'+'\n'+'\\end{scope}')
            fid.write('\n'+'}'+'\n')




            fid.write('\\draw[->] (6,1) |-+(-9,-2);'+ '\n')
            fid.write('\\draw[step = 1] (-7,-2) grid + (4,4);'+'\n')
            fid.write('\\draw[->] (13,3) |-+(16,2);'+ '\n')
            fid.write('\\draw[step = 1] (29,4) grid + (4,4);'+'\n')
    
            fid.write('\\draw (2,4) node[above] {\\scriptsize Round \pgfmathparse{int(\\z*2)}\pgfmathresult };'+'\n')
            fid.write( '\\draw (16,4) node[above] {\\scriptsize Round  \pgfmathparse{int(\\z*2+1)}\\pgfmathresult};'+'\n')
            fid.write('\\draw (28,2) |- ++(-30,-4);'+'\draw[->] (-2,-2)|-+(2,-4);'+'\n'+'\\end{scope}')
            fid.write('\n'+'}'+'\n')
                
                

        if self.BR%2 == 1:
            for i in [self.BR//2]:
                fid.write('\\begin{scope}[yshift ='+str(- i* 8)+' cm]'+'\n')
                fid.write('\\foreach \\x  in {0,8,14}'+'\n'+'\\draw[step = 1] (\\x,0) grid + (4,4);'+'\n')
                fid.write('\\foreach \\x in {0}'+'\n'+'{\\draw[->] (\\x+4,2) --node[above]{\scriptsize $SB,SR$}+(4,0);'+ '\n')
                fid.write('\\draw[->] (\\x+12,2) --node[above] {\\scriptsize $MC$}+(2,0);'+'\n')
                fid.write('\\node[below] at (\\x+13,2) {\\scriptsize $AK$};'+'\n')
                fid.write('}'+'\n')
                fid.write('\\draw (2,4) node[above] {\\scriptsize Round '+str(2*i)+' };'+'\n')
                fid.write('\\draw (16,4) node[above] {\\scriptsize Round'+str(2*i+1)+'};'+'\n')
                fid.write('\\draw (18,2)--(28,2);'+'\n')
                fid.write('\\draw (28,2) |- ++(-30,-4);'+'\n')
                fid.write('\\draw[->] (-2,-2)|-+(8,-4);'+'\n')

                fid.write('\\draw[-] (-1,2)--+(1,0);'+ '\n')
                fid.write('\\draw[->] (-1,2) |-+(-4,-2);'+ '\n')
                fid.write('\\draw[step = 1] (-7,-2) grid + (4,4);'+'\n')
                
                fid.write('\\draw[->] (13,3) |-+(16,2);'+ '\n')
                fid.write('\\draw[step = 1] (29,3) grid + (4,4);'+'\n')                
                    
                
                fid.write('\end{scope}'+'\n')

        if self.BR%2 == 0:
            for i in [self.BR//2]:
                fid.write('\\begin{scope}[yshift ='+str(- i* 8)+' cm]'+'\n')
                fid.write('\\foreach \\x  in {0}'+'\n'+'\\draw[step = 1] (\\x,0) grid + (4,4);'+'\n')
                fid.write('\\draw (2,4) node[above] {\\scriptsize Round '+str(2*i)+' };'+'\n')
                fid.write('\\draw[->] (4,2)--+(2,0);'+'\n')

                fid.write('\\draw[-] (-1,2)--+(1,0);'+ '\n')
                fid.write('\\draw[->] (-1,2) |-+(-4,-2);'+ '\n')
                fid.write('\\draw[step = 1] (-7,-2) grid + (4,4);'+'\n')
                fid.write('\end{scope}'+'\n')



#above is the structure of backward keyrecovery        
        
        
        if self.BR%2 == 0:
            ysh = self.BR//2
        else:
            ysh = self.BR//2 +1




        for i in range((self.FR)//2):
            for j in range(2):
                GR = _Y(AES.genVars_input_of_MixColumn((2*i+j) + self.TR))
                GS = _Y(AES.genVars_input_of_round((2*i+j) + self.TR))

                fid.write('\\begin{scope}[yshift ='+str(- (i+ysh+1)* 8)+' cm, xshift =' +str(j*14)+' cm]'+'\n')
                fid.write('\\draw (2,4) node[above] {\\scriptsize Round '+str((2*i+j)+self.TR+self.BR)+' };'+'\n')
                for g in range(16):
                    row = 3-g//4
                    col = g%4
                    if Solution[GS[g]] ==1:
                        fid.write('\\fill[orange]('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    if Solution[GR[g]] == 1:
                        fid.write('\\fill[orange]('+str(col+8)+','+str(row)+') rectangle +(1,1);'+'\n')
                fid.write('\n'+'\\end{scope}'+'\n')

                fid.write('\\begin{scope}[yshift ='+str(- (i+ysh+1)* 8)+' cm]'+'\n')
                for g in range(16):
                    row = 3-g//4
                    col = g%4
                    if Solution[GR[g]] ==1:
                        if j == 0:
                            fid.write('\\fill[orange]('+str(col-7)+','+str(row-3)+') rectangle +(1,1);'+'\n')
                        if j == 1:
                            fid.write('\\fill[orange]('+str(col+29)+','+str(row+3)+') rectangle +(1,1);'+'\n')
                fid.write('\n'+'\\end{scope}'+'\n')




        for i in [(self.FR)//2]:
            if (self.FR)%2 == 1:
                Cols = [0,1]
            else:
                Cols = [0]
            for j in Cols:

                GS = _Y(AES.genVars_input_of_round((2*i+j) + self.TR))
                fid.write('\\begin{scope}[yshift ='+str(-(i+ysh+1)* 8)+' cm, xshift =' +str(j*14)+' cm]'+'\n')
                fid.write('\\draw (2,4) node[above] {\\scriptsize Round '+str((2*i+j)+self.TR+self.BR)+' };'+'\n')
                for g in range(16):
                    row = 3-g//4
                    col = g%4
                    if Solution[GS[g]] ==1:
                        fid.write('\\fill[orange]('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    if (self.FR)%2 == 1 and j == 0:
                        GR = _Y(AES.genVars_input_of_MixColumn((2*i+j) + self.TR))
                        if Solution[GR[g]] ==1:
                            fid.write('\\fill[orange]('+str(col+8)+','+str(row)+') rectangle +(1,1);'+'\n')
                fid.write('\n'+'\\end{scope}'+'\n')

                if (self.FR)%2 == 1 and j == 0:
                    fid.write('\\begin{scope}[yshift ='+str(- (i+ysh+1)* 8)+' cm]'+'\n')
                    for g in range(16):
                        row = 3-g//4
                        col = g%4
                        if Solution[GR[g]] ==1:
                                fid.write('\\fill[orange]('+str(col-7)+','+str(row-3)+') rectangle +(1,1);'+'\n')

                    fid.write('\n'+'\\end{scope}'+'\n')
#above is the fillment forward keyrecovery


        fid.write('\\begin{scope}[yshift = '+str(-ysh *8)+' cm];'+'\n')
        fid.write('\\draw[->] (18,2) --node[left=50pt]{\\scriptsize $\\cdots$ Distinguisher $\\cdots$} (28,2);'+'\n')

        fid.write('\\draw (28,2) |- ++(-30,-4);'+'\n')
        fid.write('\\draw[->] (-2,-2)|-+(2,-4);'+'\n')
        fid.write('\\end{scope}'+'\n')
        
        

        fid.write('\\foreach \z in {'+str(ysh+1))
        for i in range(1,(self.FR)//2):
            fid.write(','+str(i+ysh+1))
        fid.write('}{'+'\n')
        fid.write('\\begin{scope}[yshift = -\z* 8 cm]'+'\n')
        fid.write('\\foreach \\x  in {0,8,14,22}'+'\n'+'\\draw[step = 1] (\\x,0) grid + (4,4);'+'\n')
        fid.write('\\foreach \\x in {0,14}'+'\n'+'{\\draw[->] (\\x+4,2) --node[above]{\scriptsize $SB,SR$}+(4,0);'+ '\n'+'\\node[below] at (\\x+6,2) {\\scriptsize $AK$};'+'\n'+'\\draw[->] (\\x+12,2) --node[above] {\\scriptsize $MC$}+(2,0);}'+'\n')
        fid.write('\\draw[->] (6,1) |-+(-9,-2);'+ '\n')        
        fid.write('\\draw[step = 1] (-7,-3) grid + (4,4);'+'\n')
        fid.write('\\draw[->] (20,3) |-+(9,2);'+ '\n')
        fid.write('\\draw[step = 1] (29,3) grid + (4,4);'+'\n')
        
        
        fid.write('\\draw (28,2) |- ++(-30,-4);'+'\draw[->] (-2,-2)|-+(2,-4);'+'\n'+'\\end{scope}')
        fid.write('\n'+'}'+'\n')

        if (self.FR)%2 == 1:
            for i in [(self.FR)//2]:
                fid.write('\\begin{scope}[yshift ='+str(- (i+ysh+1)* 8)+' cm]'+'\n')
                fid.write('\\foreach \\x  in {0,8,14}'+'\n'+'\\draw[step = 1] (\\x,0) grid + (4,4);'+'\n')
                fid.write('\\foreach \\x in {0}'+'\n'+'{\\draw[->] (\\x+4,2) --node[above]{\scriptsize $SB,SR$}+(4,0);'+ '\n'+'\\node[below] at (\\x+6,2) {\\scriptsize $AK$};'+'\n')
                fid.write('\\draw[->] (6,1) |-+(-9,-2);'+ '\n')
                fid.write('\\draw[step = 1] (-7,-3) grid + (4,4);'+'\n')
                fid.write('\\draw[->] (\\x+12,2) --node[above] {\\scriptsize $MC$}+(2,0);'+'\n')

                fid.write('}'+'\n')
#                fid.write('\\draw (16,4) node[above] {\\scriptsize C};'+'\n')
                fid.write('\end{scope}'+'\n')

        if (self.FR)%2 == 0:
            for i in [(self.FR)//2]:
                fid.write('\\begin{scope}[yshift ='+str(- (i+ysh+1)* 8)+' cm]'+'\n')
                fid.write('\\foreach \\x  in {0}'+'\n'+'\\draw[step = 1] (\\x,0) grid + (4,4);'+'\n')
#                fid.write('\\draw (2,4) node[above] {\\scriptsize C };'+'\n')

                fid.write('\end{scope}'+'\n')


        fid.write('\n'+'\\end{tikzpicture}'+'\n'+'\\end{document}')
        fid.close()
