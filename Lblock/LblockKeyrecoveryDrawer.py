

from CPMITM import *
from MITMLBlock import *

linearM = [2,0,3,1,6,4,7,5]

class DrawKeyrecovery():
    def __init__(self,solutionFile, totalRounds, backwardRounds, forwardRounds):
        print('in init()')
        solFile = open(solutionFile,'r')
        self.BR = backwardRounds
        self.FR = forwardRounds
        self.TR = totalRounds
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
        fid.write('\\documentclass{standalone}'+'\n'+'\\usepackage{tikz}'+'\n'+'\\usepackage{amssymb}'+'\n'+'\\usepackage{calc}'+'\n'+'\\usepackage{pgffor}'+'\n'+'\\usetikzlibrary{patterns}'+'\n'+'\\begin{document}'+'\n'+'\\begin{tikzpicture}[scale=0.35]'+'\n')
        _X = BasicTools.typeX
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ 

        Blockcipher = MITM_Lblock("Lblock", 4, 64, self.TR, 4, 80)
        for i in range(1,self.BR+1):
            KDL = _X(Blockcipher.genVars_input_left(-i))
            KDR = _X(Blockcipher.genVars_input_right(-i))
            KOL = _X(Blockcipher.genVars_output_F(-i))
            KIF = _X(Blockcipher.genVars_input_F(-i))
            Inde = self.BR -i
            fid.write('\\begin{scope}[yshift = '+str(-Inde*13)+' cm]'+'\n')
            for j in range(8):
                if Solution[KDL[j]] == 1:
                    fid.write('\\fill[red] ('+str(j)+',0)rectangle +(1,1);'+'\n')
                if Solution[KDR[j]] ==1:
                    fid.write('\\fill[red] ('+str(j+15)+',0)rectangle +(1,1);'+'\n')
                if Solution[KOL[j]] == 1:
                    fid.write('\\fill[red] (13,'+str(-1-j)+')rectangle +(1,1);'+'\n')
                if Solution[KIF[j]] ==1:
                    fid.write('\\fill[red] (9,'+str(-1-j)+')rectangle +(1,1);'+'\n')
            fid.write('\end{scope}'+'\n')

        KDL = _X(Blockcipher.genVars_input_left(0))
        KDR = _X(Blockcipher.genVars_input_right(0))
        Inde = self.BR
        fid.write('\\begin{scope}[yshift = '+str(-Inde*13)+' cm]'+'\n')
        for j in range(8):
            if Solution[KDL[j]] == 1:
                fid.write('\\fill[red] ('+str(j)+',0)rectangle +(1,1);'+'\n')
            if Solution[KDR[j]] ==1:
                fid.write('\\fill[red] ('+str(j+15)+',0)rectangle +(1,1);'+'\n')
        fid.write('\\draw (0,0) grid +(8,1);'+'\n')
        fid.write('\\draw (15,0) grid +(8,1);'+'\n')
        fid.write('\\node[left=20pt,above] at (0,0) {\\tiny Round '+str(self.BR)+'};'+'\n')
        fid.write('\\node[below,align = center] at(11.5,0.5) {$\\vdots$\\\ 11-round Distinguisher\\\$\\vdots$};'+'\n')
        fid.write('\end{scope}'+'\n')
#above is the fillment leftpart

        fid.write('\\foreach \\x in {0')
        for i in range(1,self.BR):
            fid.write(','+str(i))
        fid.write('}{'+'\n')
        fid.write('\\begin{scope}[yshift = -\\x*13 cm]'+'\n')
        fid.write('\\draw (0,0) node[left=20pt,above]{\\tiny Round $\\x$} grid +(8,1);'+'\n')
        fid.write('\\draw (15,0) grid +(8,1);'+'\n')
        fid.write('\\draw[->](4,0)|-+(2,-4);'+'\n')
        fid.write('\\draw[->] (6,-4)--+(3,0);'+'\n')
        fid.write('\\draw (9,-8) grid +(1,8);'+'\n')
        fid.write('\\draw[->] (10,-4)--node[above]{\\tiny $SB,LN$} +(3,0);'+'\n')
        fid.write('\\draw (13,-8) grid +(1,8);'+'\n')
        fid.write('\\draw[->](13,-4)--+(5.5,0);'+'\n')
        fid.write('\\draw(19,0)--+(0,-1);'+'\n')
        fid.write('\\draw (19,-0.6) node[below = 1pt]{\\scriptsize $\\lll 8$};'+'\n')
        fid.write('\\draw[->] (19,-2)--+(0,-1.5);'+'\n')
        fid.write('\\draw (19,-4) circle (0.5);'+'\n')
        fid.write('\\draw (18.5,-4)--+(1,0);'+'\n')
        fid.write('\\draw(19,-3.5)--+(0,-1);'+'\n')
        fid.write('\\draw (6.5,-4) circle (0.5);'+'\n')
        fid.write('\\draw[->](6.5,-5.5) -- node[below=5pt]{\\tiny $SK$} + (0,1);'+'\n')
        fid.write('\\draw (6.5,-3.5)--+(0,-1);'+'\n')
        fid.write('\\draw (19,-4.5)--++(0,-3.5)--++(-15,-2);'+'\n')
        fid.write('\\draw[->] (4,-10)--+(0,-2);'+'\n')
        fid.write('\\draw (4,-4)--++(0,-4)--+(15,-2);'+'\n')
        fid.write('\\draw[->](19,-10)--+(0,-2);'+'\n')
        fid.write('\end{scope}'+'\n')
        fid.write('\n'+'}'+'\n'+'\n')
#above is the left structure


        for i in range(self.FR):
            DL = _Y(Blockcipher.genVars_input_left(i+self.TR))
            DR = _Y(Blockcipher.genVars_input_right(i+self.TR))
            OL = _Y(Blockcipher.genVars_output_F(i+self.TR))
            IF = _Y(Blockcipher.genVars_input_F(i+self.TR))
            Inde = i
            fid.write('\\begin{scope}[yshift = '+str(-Inde*13)+' cm, xshift = 25 cm]'+'\n')
            for j in range(8):
                if Solution[DL[j]] == 1:
                    fid.write('\\fill[red] ('+str(j)+',0)rectangle +(1,1);'+'\n')
                if Solution[DR[j]] ==1:
                    fid.write('\\fill[red] ('+str(j+15)+',0)rectangle +(1,1);'+'\n')
                if Solution[OL[j]] == 1:
                    fid.write('\\fill[red] (13,'+str(-1-j)+')rectangle +(1,1);'+'\n')
                if Solution[IF[j]] ==1:
                    fid.write('\\fill[red] (9,'+str(-1-j)+')rectangle +(1,1);'+'\n')
            fid.write('\end{scope}'+'\n')

        DL = _Y(Blockcipher.genVars_input_left(self.FR+self.TR))
        DR = _Y(Blockcipher.genVars_input_right(self.FR+self.TR))

        fid.write('\\begin{scope}[yshift = '+str(-self.FR*13)+' cm, xshift = 25 cm]'+'\n')
        for j in range(8):
            if Solution[DL[j]] == 1:
                fid.write('\\fill[red] ('+str(j)+',0)rectangle +(1,1);'+'\n')
            if Solution[DR[j]] ==1:
                fid.write('\\fill[red] ('+str(j+15)+',0)rectangle +(1,1);'+'\n')
        fid.write('\\draw (0,0) grid +(8,1);'+'\n')
        fid.write('\\draw (15,0) grid +(8,1);'+'\n')
        fid.write('\\node[right=20pt,above] at (23,0) {\\tiny Round '+str(self.BR+self.FR+self.TR)+'};'+'\n')
        fid.write('\end{scope}'+'\n')

#above is the fillment of rightpart
        fid.write('\\begin{scope}[yshift = -0 cm, xshift = 25 cm]'+'\n')
        fid.write('\\node[above,align = center] at(11.5,0.5) {$\\vdots$\\\Distinguisher\\\ $\\vdots$};'+'\n')
        fid.write('\end{scope}'+'\n')

        fid.write('\\foreach \\y in {0')
        for i in range(1,self.FR):
            fid.write(','+str(i))
        fid.write('}{'+'\n')
        fid.write('\\begin{scope}[yshift = -\\y*13 cm, xshift = 25 cm]'+'\n')
        fid.write('\\draw (0,0) grid +(8,1);'+'\n')
        fid.write('\\node[right=20pt,above] at (23,0) {\\tiny Round \\pgfmathparse{int(\y+'+str(self.BR+self.TR)+')}\\pgfmathresult};'+'\n')
        fid.write('\\draw (15,0) grid +(8,1);'+'\n')
        fid.write('\\draw[->](4,0)|-+(2,-4);'+'\n')
        fid.write('\\draw[->] (6,-4)--+(3,0);'+'\n')
        fid.write('\\draw (9,-8) grid +(1,8);'+'\n')
        fid.write('\\draw[->] (10,-4)--node[above]{\\tiny $SB,LN$} +(3,0);'+'\n')
        fid.write('\\draw (13,-8) grid +(1,8);'+'\n')
        fid.write('\\draw[->](13,-4)--+(5.5,0);'+'\n')
        fid.write('\\draw(19,0)--+(0,-1);'+'\n')
        fid.write('\\draw (19,-0.6) node[below = 1pt]{\\scriptsize $\\lll 8$};'+'\n')
        fid.write('\\draw[->] (19,-2)--+(0,-1.5);'+'\n')
        fid.write('\\draw (19,-4) circle (0.5);'+'\n')
        fid.write('\\draw (18.5,-4)--+(1,0);'+'\n')
        fid.write('\\draw(19,-3.5)--+(0,-1);'+'\n')
        fid.write('\\draw (6.5,-4) circle (0.5);'+'\n')
        fid.write('\\draw[->](6.5,-5.5) -- node[below=5pt]{\\tiny $SK$} + (0,1);'+'\n')
        fid.write('\\draw (6.5,-3.5)--+(0,-1);'+'\n')
        fid.write('\\draw (19,-4.5)--++(0,-3.5)--++(-15,-2);'+'\n')
        fid.write('\\draw[->] (4,-10)--+(0,-2);'+'\n')
        fid.write('\\draw (4,-4)--++(0,-4)--+(15,-2);'+'\n')
        fid.write('\\draw[->](19,-10)--+(0,-2);'+'\n')

        fid.write('\end{scope}'+'\n')
        fid.write('\n'+'}'+'\n'+'\n')
#above is the right structure


        fid.write('\n'+'\\end{tikzpicture}'+'\n'+'\\end{document}')
        fid.close()

    def drawGuessedValue(self,outputfile):
        _X = BasicTools.typeX
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ 
        Solution = self.var_value_map
        fid = open(outputfile,'w')
        fid.write('\\documentclass{standalone}'+'\n'+'\\usepackage{tikz}'+'\n'+'\\usepackage{amssymb}'+'\n'+'\\usepackage{calc}'+'\n'+'\\usepackage{pgffor}'+'\n'+'\\usetikzlibrary{patterns}'+'\n'+'\\begin{document}'+'\n'+'\\begin{tikzpicture}[scale=0.35]'+'\n')

        Blockcipher = MITM_Lblock("Lblock", 4, 64, self.TR, 4, 80)
        for i in range(1,self.BR+1):
            VL = _Z(Blockcipher.genVars_input_left(-i))
            VR = _Z(Blockcipher.genVars_input_right(-i))
            VIF = _Z(Blockcipher.genVars_input_F(-i))
            VOL = _Z(Blockcipher.genVars_output_F(-i))

            Inde = self.BR -i
            fid.write('\\begin{scope}[yshift = '+str(-Inde*13)+' cm]'+'\n')
            for j in range(8):
                if Solution[VL[j]] == 1:
                    fid.write('\\fill[orange] ('+str(j)+',0)rectangle +(1,1);'+'\n')
                if Solution[VR[j]] ==1:
                    fid.write('\\fill[orange] ('+str(j+15)+',0)rectangle +(1,1);'+'\n')
                if Solution[VOL[j]] == 1:
                    fid.write('\\fill[orange] (13,'+str(-1-j)+')rectangle +(1,1);'+'\n')
                if Solution[VIF[j]] ==1:
                    fid.write('\\fill[orange] (9,'+str(-1-j)+')rectangle +(1,1);'+'\n')
                    fid.write('\\fill[orange] (0,'+str(-2-j)+')rectangle +(1,1);'+'\n')
            fid.write('\end{scope}'+'\n')


        KDL = _Z(Blockcipher.genVars_input_left(0))
        KDR = _Z(Blockcipher.genVars_input_right(0))
        Inde = self.BR
        fid.write('\\begin{scope}[yshift = '+str(-Inde*13)+' cm]'+'\n')
        for j in range(8):
            if Solution[KDL[j]] == 1:
                fid.write('\\fill[orange] ('+str(j)+',0)rectangle +(1,1);'+'\n')
            if Solution[KDR[j]] ==1:
                fid.write('\\fill[orange] ('+str(j+15)+',0)rectangle +(1,1);'+'\n')
        fid.write('\\node[left=20pt,above] at (0,0) {\\tiny Round '+str(self.BR)+'};'+'\n')
        fid.write('\\draw (0,0) grid +(8,1);'+'\n')
        fid.write('\\draw (15,0) grid +(8,1);'+'\n')
        fid.write('\\node[below,align = center] at(11.5,0.5) {$\\vdots$\\\ 11-round Distinguisher\\\$\\vdots$};'+'\n')

        fid.write('\end{scope}'+'\n')
#above is fillment of leftpart


        fid.write('\\foreach \\x in {0')
        for i in range(1,self.BR):
            fid.write(','+str(i))
        fid.write('}{'+'\n')

        fid.write('\\begin{scope}[yshift = -\\x*13 cm]'+'\n')

        fid.write('\\draw (0,0) node[left=20pt,above]{\\tiny Round $\\x$} grid +(8,1);'+'\n')
        fid.write('\\draw (15,0) grid +(8,1);'+'\n')
        fid.write('\\draw[->](4,0)|-+(2,-4);'+'\n')
        fid.write('\\draw[->] (6,-4)--+(3,0);'+'\n')
        fid.write('\\draw (9,-8) grid +(1,8);'+'\n')
        fid.write('\\draw[->] (10,-4)--node[above]{\\tiny $SB,LN$} +(3,0);'+'\n')
        fid.write('\\draw (13,-8) grid +(1,8);'+'\n')
        fid.write('\\draw[->](13,-4)--+(5.5,0);'+'\n')
        fid.write('\\draw(19,0)--+(0,-1);'+'\n')
        fid.write('\\draw (19,-0.6) node[below = 1pt]{\\scriptsize $\\lll 8$};'+'\n')
        fid.write('\\draw[->] (19,-2)--+(0,-1.5);'+'\n')
        fid.write('\\draw (19,-4) circle (0.5);'+'\n')
        fid.write('\\draw (18.5,-4)--+(1,0);'+'\n')
        fid.write('\\draw(19,-3.5)--+(0,-1);'+'\n')
        fid.write('\\draw (6.5,-4) circle (0.5);'+'\n')
#        fid.write('\\draw[->](6.5,-1) -- node[left]{\\tiny $SK_{\\x}$} + (0,-2.5);'+'\n')
        fid.write('\\draw[->](1,-5) -|  (6.5,-4.5);'+'\n')
        fid.write('\\draw (0,-9) grid +(1,8);'+'\n')
        fid.write('\\node[below] at (6.5,-5) {\\tiny $SK$};'+'\n')

        fid.write('\\draw (6.5,-3.5)--+(0,-1);'+'\n')
        fid.write('\\draw (19,-4.5)--++(0,-3.5)--++(-15,-2);'+'\n')
        fid.write('\\draw[->] (4,-10)--+(0,-2);'+'\n')
        fid.write('\\draw (4,-4)--++(0,-4)--+(15,-2);'+'\n')
        fid.write('\\draw[->](19,-10)--+(0,-2);'+'\n')

        fid.write('\end{scope}'+'\n')
        fid.write('\n'+'}'+'\n'+'\n')

#above is the structure of leftpart


        for i in range(self.FR):
            DL = _Y(Blockcipher.genVars_input_left(i+self.TR))
            DR = _Y(Blockcipher.genVars_input_right(i+self.TR))
            OL = _Y(Blockcipher.genVars_output_F(i+self.TR))
            IF = _Z(Blockcipher.genVars_input_F(i+self.TR))
            Inde = i
            fid.write('\\begin{scope}[yshift = '+str(-Inde*13)+' cm, xshift = 25 cm]'+'\n')

            for j in range(8):
                if Solution[DL[j]] == 1:
                    fid.write('\\fill[orange] ('+str(j)+',0)rectangle +(1,1);'+'\n')
                if Solution[DR[j]] ==1:
                    fid.write('\\fill[orange] ('+str(j+15)+',0)rectangle +(1,1);'+'\n')
                if Solution[OL[j]] == 1:
                    fid.write('\\fill[orange] (13,'+str(-1-j)+')rectangle +(1,1);'+'\n')
                if Solution[IF[j]] ==1:
                    fid.write('\\fill[orange] (9,'+str(-1-j)+')rectangle +(1,1);'+'\n')
                    fid.write('\\fill[orange] (0,'+str(-2-j)+')rectangle +(1,1);'+'\n')
            fid.write('\end{scope}'+'\n')

        DL = _Y(Blockcipher.genVars_input_left(self.FR+self.TR))
        DR = _Y(Blockcipher.genVars_input_right(self.FR+self.TR))
        Inde = self.FR
        fid.write('\\begin{scope}[yshift = '+str(-Inde*13)+' cm, xshift = 25 cm]'+'\n')
        for j in range(8):
            if Solution[DL[j]] == 1:
                fid.write('\\fill[orange] ('+str(j)+',0)rectangle +(1,1);'+'\n')
            if Solution[DR[j]] ==1:
                fid.write('\\fill[orange] ('+str(j+15)+',0)rectangle +(1,1);'+'\n')
        fid.write('\\node[right=20pt,above] at (23,0) {\\tiny Round '+str(self.BR+self.FR+self.TR)+'};'+'\n')
        fid.write('\\draw (0,0) grid +(8,1);'+'\n')
        fid.write('\\draw (15,0) grid +(8,1);'+'\n')

        fid.write('\end{scope}'+'\n')

#above is the fillment of rightpart

        fid.write('\\begin{scope}[yshift = -0 cm, xshift = 25 cm]'+'\n')
        fid.write('\\node[above,align = center] at(11.5,0.5) {$\\vdots$\\\Distinguisher\\\ $\\vdots$};'+'\n')
        fid.write('\end{scope}'+'\n')

        fid.write('\\foreach \\y in {0')
        for i in range(1,self.FR):
            fid.write(','+str(i))
        fid.write('}{'+'\n')

        fid.write('\\begin{scope}[yshift = -\\y*13 cm, xshift = 25 cm]'+'\n')

        fid.write('\\node[right=20pt,above] at (23,0) {\\tiny Round \\pgfmathparse{int(\y+'+str(self.BR+self.TR)+')}\\pgfmathresult};'+'\n')
        fid.write('\\draw (0,0) grid +(8,1);'+'\n')
        fid.write('\\draw (15,0) grid +(8,1);'+'\n')
        fid.write('\\draw[->](4,0)|-+(2,-4);'+'\n')
        fid.write('\\draw[->] (6,-4)--+(3,0);'+'\n')
        fid.write('\\draw (9,-8) grid +(1,8);'+'\n')
        fid.write('\\draw[->] (10,-4)--node[above]{\\tiny $SB,LN$} +(3,0);'+'\n')
        fid.write('\\draw (13,-8) grid +(1,8);'+'\n')
        fid.write('\\draw[->](13,-4)--+(5.5,0);'+'\n')
        fid.write('\\draw(19,0)--+(0,-1);'+'\n')
        fid.write('\\draw (19,-0.6) node[below = 1pt]{\\scriptsize $\\lll 8$};'+'\n')
        fid.write('\\draw[->] (19,-2)--+(0,-1.5);'+'\n')
        fid.write('\\draw (19,-4) circle (0.5);'+'\n')
        fid.write('\\draw (18.5,-4)--+(1,0);'+'\n')
        fid.write('\\draw(19,-3.5)--+(0,-1);'+'\n')
        fid.write('\\draw (6.5,-4) circle (0.5);'+'\n')
        #fid.write('\\draw[->](6.5,-1) -- node[left]{\\tiny $SK_{\\y}$} + (0,-2.5);'+'\n')
        fid.write('\\draw[->](1,-5) -|  (6.5,-4.5);'+'\n')
        fid.write('\\draw (0,-9) grid +(1,8);'+'\n')
        fid.write('\\node[below] at (6.5,-5) {\\tiny $SK$};'+'\n')

        fid.write('\\draw (6.5,-3.5)--+(0,-1);'+'\n')
        fid.write('\\draw (19,-4.5)--++(0,-3.5)--++(-15,-2);'+'\n')
        fid.write('\\draw[->] (4,-10)--+(0,-2);'+'\n')
        fid.write('\\draw (4,-4)--++(0,-4)--+(15,-2);'+'\n')
        fid.write('\\draw[->](19,-10)--+(0,-2);'+'\n')

        fid.write('\end{scope}'+'\n')
        fid.write('\n'+'}'+'\n'+'\n')


#above is the structure of rightpart
        fid.write('\n'+'\\end{tikzpicture}'+'\n'+'\\end{document}')
        fid.close()

def main():
    a = print_function('Sh_TW_keylen20_r11_4_5_MR18.sol',11)
    a.Code('Sh_TW_keylen20_r11_4_5_MR18_dis.tex')
##    value = [40,42,43,44,45,46,47,48]
##    num =[4,4,4,12,16,8,12,24]
##    fff= open('SCIPfigure/cmd.txt','a')
##    for j in range(8):
##        for j1 in range(1,num[j]+1):
##            x = print_function('SCIP/val_'+str(value[j])+'myfile'+str(j1)+'.txt',10)
##            x.Code('SCIPfigure/val_'+str(value[j])+'myfigure'+str(j1)+'.tex')
##            fff.write('pdflatex val_'+str(value[j])+'myfigure'+str(j1)+'.tex'+'\n')
##    fff.close()

def print_cmd():
    for j in range(1,85):
        print('pdflatex myfigure'+str(j)+'.tex')







