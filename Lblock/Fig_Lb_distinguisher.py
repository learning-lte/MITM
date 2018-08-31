from CPMITM import *
from MITMLBlock import *

linearM = [2,0,3,1,6,4,7,5]


class DrawDistinguisher():
    def __init__(self,solutionFile, totalRounds):
        print('in init()')
        solFile = open(solutionFile,'r')
        self.TR = totalRounds
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
        Solution = self.var_value_map
        
        fid = open(outputfile,'w')
        fid.write('\\documentclass{standalone}'+'\n'+'\\usepackage{tikz}'+'\n'+'\\usepackage{amssymb}'+'\n'+'\\usepackage{calc}'+'\n'+'\\usepackage{pgffor}'+'\n'+'\\usetikzlibrary{patterns}'+'\n'+'\\begin{document}'+'\n'+'\\begin{tikzpicture}[scale=0.35]'+'\n')
        Blockcipher = MITM_Lblock("Lblock", 4, 64, self.TR, 4, 80)
        for i in range(6):
            GL = _Z(Blockcipher.genVars_input_left(i))
            GR = _Z(Blockcipher.genVars_input_right(i))
            GOL = _Z(Blockcipher.genVars_output_F(i))
            GIF = _Z(Blockcipher.genVars_input_F(i))
            Inde = i
            fid.write('\\begin{scope}[yshift = '+str(-Inde*13)+' cm]'+'\n')
            for j in range(8):
                if Solution[GIF[j]] ==1:
                    fid.write('\\fill[red] (9,'+str(-1-j)+')rectangle +(1,1);'+'\n')
            fid.write('\end{scope}'+'\n')

        for i in range(6,self.TR):
            GL = _Z(Blockcipher.genVars_input_left(i))
            GR = _Z(Blockcipher.genVars_input_right(i))
            GOL = _Z(Blockcipher.genVars_output_F(i))
            GIF = _Z(Blockcipher.genVars_input_F(i))
            Inde = i-6
            fid.write('\\begin{scope}[yshift = '+str(-Inde*13)+' cm, xshift = 25cm]'+'\n')
            #fid.write('\\node[left] at (4,-4) {\\tiny Round '+str(i)+'};'+'\n')
            for j in range(8):

                if Solution[GIF[j]] ==1:
                    fid.write('\\fill[red] (9,'+str(-1-j)+')rectangle +(1,1);'+'\n')
            fid.write('\end{scope}'+'\n')
#above is the fill guessed bytes

        fid.write('\\foreach \\x in {0')
        for i in range(1,6):
            fid.write(','+str(i))
        fid.write('}{'+'\n')

        fid.write('\\begin{scope}[yshift = -\\x*13 cm]'+'\n')
        fid.write('\\draw (0,0) node[left=20pt,above]{\\tiny Round $\\x$} grid +(8,1);'+'\n')
        #fid.write('\\draw (0,0) grid +(8,1);'+'\n')
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
        fid.write('\\draw[->](6.5,-5.5) -- node[below=5pt]{\\tiny $SK$} + (0,1);'+'\n')
        fid.write('\\draw (6.5,-3.5)--+(0,-1);'+'\n')
        fid.write('\\draw (19,-4.5)--++(0,-3.5)--++(-15,-2);'+'\n')
        fid.write('\\draw[->] (4,-10)--+(0,-2);'+'\n')
        fid.write('\\draw (4,-4)--++(0,-4)--+(15,-2);'+'\n')
        fid.write('\\draw[->](19,-10)--+(0,-2);'+'\n')
        #fid.write('\\node[left] at (4,-4) {\\tiny Round \\x};'+'\n')
        fid.write('\end{scope}'+'\n')
        fid.write('\n'+'}'+'\n'+'\n')
#above is the structure of the leftpart


        fid.write('\\foreach \\y in {0')
        for i in range(1,self.TR-6):
            fid.write(','+str(i))
        fid.write('}{'+'\n')

        fid.write('\\begin{scope}[yshift = -\\y*13 cm, xshift = 25 cm]'+'\n')
        fid.write('\\node[right=20pt,above] at (23,0) {\\tiny Round \\pgfmathparse{int(\y+6)}\\pgfmathresult};'+'\n')
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
#        fid.write('\\draw[->](6.5,-1) -- node[left]{\\tiny $SK_{6+\\y}$} + (0,-2.5);'+'\n')
        fid.write('\\draw[->](6.5,-5.5) -- node[below=5pt]{\\tiny $SK$} + (0,1);'+'\n')
        fid.write('\\draw (6.5,-3.5)--+(0,-1);'+'\n')
        fid.write('\\draw (19,-4.5)--++(0,-3.5)--++(-15,-2);'+'\n')
        fid.write('\\draw[->] (4,-10)--+(0,-2);'+'\n')
        fid.write('\\draw (4,-4)--++(0,-4)--+(15,-2);'+'\n')
        fid.write('\\draw[->](19,-10)--+(0,-2);'+'\n')
        fid.write('\end{scope}'+'\n')
        fid.write('\n'+'}'+'\n'+'\n')

#above is the sturcture of the rightpart



        for i in range(6):
            L = _X(Blockcipher.genVars_input_left(i))
            R = _X(Blockcipher.genVars_input_right(i))
            OL = _X(Blockcipher.genVars_output_F(i))
            IF = _X(Blockcipher.genVars_input_F(i))
            DL = _Y(Blockcipher.genVars_input_left(i))
            DR = _Y(Blockcipher.genVars_input_right(i))
            DOL = _Y(Blockcipher.genVars_output_F(i))
            DIF = _Y(Blockcipher.genVars_input_F(i))
            Inde = i
            fid.write('\\begin{scope}[yshift = '+str(-Inde*13)+' cm]'+'\n')
            for j in range(8):
                if Solution[L[j]] == 1:
                    fid.write('\\fill[pattern = north east lines] ('+str(j)+',0)rectangle +(1,1);'+'\n')
                if Solution[R[j]] ==1:
                    fid.write('\\fill[pattern = north east lines] ('+str(j+15)+',0)rectangle +(1,1);'+'\n')
                if Solution[OL[j]] == 1:
                    fid.write('\\fill[pattern = north east lines] (13,'+str(-1-j)+')rectangle +(1,1);'+'\n')
                if Solution[IF[j]] ==1:
                    fid.write('\\fill[pattern = north east lines] (9,'+str(-1-j)+')rectangle +(1,1);'+'\n')
                if Solution[DL[j]] == 1:
                    fid.write('\\fill[pattern = north west lines] ('+str(j)+',0)rectangle +(1,1);'+'\n')
                if Solution[DR[j]] ==1:
                    fid.write('\\fill[pattern = north west lines] ('+str(j+15)+',0)rectangle +(1,1);'+'\n')
                if Solution[DOL[j]] == 1:
                    fid.write('\\fill[pattern = north west lines] (13,'+str(-1-j)+')rectangle +(1,1);'+'\n')
                if Solution[DIF[j]] ==1:
                    fid.write('\\fill[pattern = north west lines] (9,'+str(-1-j)+')rectangle +(1,1);'+'\n')

            fid.write('\end{scope}'+'\n')

        for i in range(6,self.TR):
            L = _X(Blockcipher.genVars_input_left(i))
            R = _X(Blockcipher.genVars_input_right(i))
            OL = _X(Blockcipher.genVars_output_F(i))
            IF = _X(Blockcipher.genVars_input_F(i))
            DL = _Y(Blockcipher.genVars_input_left(i))
            DR = _Y(Blockcipher.genVars_input_right(i))
            DOL = _Y(Blockcipher.genVars_output_F(i))
            DIF = _Y(Blockcipher.genVars_input_F(i))
            Inde = i-6
            fid.write('\\begin{scope}[yshift = '+str(-Inde*13)+' cm, xshift = 25cm]'+'\n')
            for j in range(8):
                if Solution[L[j]] == 1:
                    fid.write('\\fill[pattern = north east lines] ('+str(j)+',0)rectangle +(1,1);'+'\n')
                if Solution[R[j]] ==1:
                    fid.write('\\fill[pattern = north east lines] ('+str(j+15)+',0)rectangle +(1,1);'+'\n')
                if Solution[OL[j]] == 1:
                    fid.write('\\fill[pattern = north east lines] (13,'+str(-1-j)+')rectangle +(1,1);'+'\n')
                if Solution[IF[j]] ==1:
                    fid.write('\\fill[pattern = north east lines] (9,'+str(-1-j)+')rectangle +(1,1);'+'\n')
                if Solution[DL[j]] == 1:
                    fid.write('\\fill[pattern = north west lines] ('+str(j)+',0)rectangle +(1,1);'+'\n')
                if Solution[DR[j]] ==1:
                    fid.write('\\fill[pattern = north west lines] ('+str(j+15)+',0)rectangle +(1,1);'+'\n')
                if Solution[DOL[j]] == 1:
                    fid.write('\\fill[pattern = north west lines] (13,'+str(-1-j)+')rectangle +(1,1);'+'\n')
                if Solution[DIF[j]] ==1:
                    fid.write('\\fill[pattern = north west lines] (9,'+str(-1-j)+')rectangle +(1,1);'+'\n')
            fid.write('\end{scope}'+'\n')
        fid.write('\\begin{scope}[yshift = '+str(-(self.TR-6)*13)+' cm, xshift = 25cm]'+'\n')
        L = _X(Blockcipher.genVars_input_left(self.TR))
        R = _X(Blockcipher.genVars_input_right(self.TR))
        DL = _Y(Blockcipher.genVars_input_left(self.TR))
        DR = _Y(Blockcipher.genVars_input_right(self.TR))
        fid.write('\\draw (0,0) grid +(8,1);'+'\n')
        fid.write('\\draw (15,0) grid +(8,1);'+'\n')
        fid.write('\\node[right=20pt,above] at (23,0) {\\tiny Round '+str(self.TR)+'};'+'\n')
        for j in range(8):
            if Solution[L[j]] == 1:
                fid.write('\\fill[pattern = north east lines] ('+str(j)+',0)rectangle +(1,1);'+'\n')
            if Solution[R[j]] ==1:
                fid.write('\\fill[pattern = north east lines] ('+str(j+15)+',0)rectangle +(1,1);'+'\n')
            if Solution[DL[j]] == 1:
                fid.write('\\fill[pattern = north west lines] ('+str(j)+',0)rectangle +(1,1);'+'\n')
            if Solution[DR[j]] ==1:
                fid.write('\\fill[pattern = north west lines] ('+str(j+15)+',0)rectangle +(1,1);'+'\n')

        fid.write('\end{scope}'+'\n')

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







