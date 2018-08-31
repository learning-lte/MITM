
from CPMITM import *
MC = [[1,0,1,1],[1,0,0,0],[0,1,1,0],[1,0,1,0]]
Inv_MC = [[0,1,0,0],[0,1,1,1],[0,1,0,1],[1,0,0,1]] #inverse of MC



class MITM_SKINNY(Cipher):
    
    def genVars_input_of_round(self, r):#input state of r-th round
        if r >= 0:
            return ['S_'+ str(j)+'_r'+str(r) for j in range(0, self.wc)]
        else:
            return ['S_'+ str(j)+'_r_minus_'+str(-r) for j in range(0, self.wc)]
        
    def genVars_input_of_MixColumn(self, r):
        if r >= 0:
            return ['R_'+str(j)+'_r'+str(r) for j in range(0, self.wc)]
        else:
            return ['R_'+str(j)+'_r_minus_'+str(-r) for j in range(0, self.wc)]
        
    def genVars_cutting1(self, r):
        return ['phi_'+str(j)+'_r'+str(r) for j in range(0, 4)]
    
    def genVars_cutting2(self, r):
        return ['psi_'+str(j)+'_r'+str(r) for j in range(0, 4)]

    def subfunction_cutting(self,a,b,c,d):
        C =[]
        C = C + [a+' - '+ d +' >= 0']
        C = C + [b+' - '+ d + ' >= 0']
        C = C + [c+' - '+ d+' >= 0']
        C = C + [' - '+a+' - '+b+' - '+ c+' + '+d+' >= -2']
        return C

    # the paticular property of SKINNY: 8 byte subkeys are added to the state.
    def genConstraints_Cutting(self, r): 
        _Z = BasicTools.typeZ 
        R = self.genVars_input_of_MixColumn(r)
        S = self.genVars_input_of_round(r+1)
        pu1 = self.genVars_cutting1(r)
        pu2 = self.genVars_cutting2(r)
        C = []
        for j in range(4):
            a1 = _Z(R)[2*4+j]
            a2 = _Z(R)[3*4+j]
            b1 = _Z(S)[1*4+j]
            b2 = _Z(S)[0*4+j]
            c =  _Z(S)[3*4 + j]
            C = C + self.subfunction_cutting(a1, b1, c, pu1[j])
            C = C + self.subfunction_cutting(a2, b2, c, pu2[j])
        return C

    
    def genConstraints_of_Round(self, r):
        _X = BasicTools.typeX
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ

        Input_round = self.genVars_input_of_round(r)
        Input_MC = self.genVars_input_of_MixColumn(r)
        Output_round = self.genVars_input_of_round(r+1)

        constr =[]

        # 1. Constraints of Foward Differential
        constr = constr + MITMConstraints.equalConstraints(_X(ShiftRow(Input_round)), _X(Input_MC)) # - Constraints for S-box and ShiftRow
        for j in range(0, 4): # - Constraints for MixCols
            constr = constr + MITMConstraints.ForwardDiff_LinearLayer(MC, _X(column(Input_MC, j)), _X(column(Output_round, j)))

        # 2. Constraints of Backward Determination
        constr = constr + MITMConstraints.equalConstraints(_Y(ShiftRow(Input_round)), _Y(Input_MC))
        for j in range(0, 4): # - Constraints for MixCols
            constr = constr + MITMConstraints.BackwardDet_LinearLayer(MC, _Y(column(Input_MC, j)), _Y(column(Output_round, j)))

        # 3. Constraints of the relationship of type X and type Y vars
        constr = constr + MITMConstraints.relationXYZ(_X(Input_round), _Y(Input_round), _Z(Input_round))
        constr = constr + MITMConstraints.relationXYZ(_X(Input_MC), _Y(Input_MC), _Z(Input_MC))
        constr = constr + MITMConstraints.relationXYZ(_X(Output_round), _Y(Output_round), _Z(Output_round))
        
        constr = constr + self.genConstraints_Cutting(r)
        return constr 
     


    def genConstraints_Additional(self):
        Constr = []
        _X = BasicTools.typeX
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ 
        
        plaintext = self.genVars_input_of_round(0)
        ciphertext = self.genVars_input_of_round(self.totalRounds)

        Constr = []
        Constr = Constr +  MITMConstraints.relationXYZ(_X(ciphertext),_Y(ciphertext),_Z(ciphertext))
        
        Constr = Constr + [BasicTools.plusTerm(_X(plaintext)) + ' >= 1']
        Constr = Constr + [BasicTools.plusTerm(_Y(ciphertext)) + ' >= 1 ']
        
        Constr = Constr + [self.genObjectiveFun_to_Round(self.totalRounds) + ' <= ' + str(self.wc_key - 1)]
        #the bound of the distinguisher is set to 40 for searching best key recovery attack.
                
        Input_round1 = self.genVars_input_of_round(1)
        Input1 = ['2 '+ _Z(Input_round1)[j] for j in range(16)]
        Constr = Constr + [BasicTools.plusTerm(_Z(Input_round1)) + ' + 16 Ad1 <= 17']
        Constr = Constr + [BasicTools.plusTerm(Input1) + ' + Ad1 >= 3']
        return Constr        



    def genObjectiveFun_to_Round(self, i):
        _Z = BasicTools.typeZ
        terms = []
        cut_terms = []

        for j in range(1, i):
            terms = terms + _Z(self.genVars_input_of_round(j))
            cut_terms =  cut_terms + self.genVars_cutting1(j)
            cut_terms =  cut_terms + self.genVars_cutting2(j)
        terms = terms + _Z(self.genVars_input_of_round(i))
        return BasicTools.plusTerm(terms)+ ' - '+ BasicTools.MinusTerm(cut_terms) + ' - Ad1' 
    
    
     #following is the key recovery process
     #backward differential process, r < 0
    def genConstraints_backwardkeyrecovery(self, r): 
        assert r < 0
        _X = BasicTools.typeX  
    
        Input_round = self.genVars_input_of_round(r)
        Input_MC = self.genVars_input_of_MixColumn(r)
        Output_round = self.genVars_input_of_round(r+1)
     
        Constr = []
        for j in range(4):
            Constr = Constr + MITMConstraints.ForwardDiff_LinearLayer(Inv_MC, _X(column(Output_round,j)), _X(column(Input_MC,j)))
        Constr = Constr + MITMConstraints.equalConstraints(_X(ShiftRow(Input_round)), _X(Input_MC))
        
        return Constr

       

    def genConstraints_GuessedKey_backwardkeyrecovery(self, r):
        assert r < 0
        _X = BasicTools.typeX
        _Z = BasicTools.typeZ

        Input_round = self.genVars_input_of_round(r)
        Input_MC = self.genVars_input_of_MixColumn(r)
        Output_round = self.genVars_input_of_round(r+1)        
         
        Constr = []
        if r == -1:
            Constr = Constr + MITMConstraints.equalConstraints(_X(Input_round), _Z(Input_round))            
            for j in range(16):
                Constr = Constr + [_Z(Input_MC)[j] + ' = 0']
                
        else:
            for j in range(4):
                Constr = Constr + MITMConstraints.BackwardDet_LinearLayer(MC,_Z(column(Input_MC,j)), _Z(column(Output_round, j)))
            
            for i in range(4):
                for j in range(4):
                    Constr = Constr + MITMConstraints.BackwardDet_Branch(_Z(Input_round)[4*i+j], [_X(Input_round)[4*i+j], _Z(Input_MC)[4*i+((j+i)%4)]])
            
        return Constr
 
    #forward determination: added rounds after the distinguisher
    def genConstraints_forwardkeyrecovery(self, r):  
        _Y = BasicTools.typeY
 
        Input_round = self.genVars_input_of_round(r)
        Input_MC = self.genVars_input_of_MixColumn(r)
        Output_round = self.genVars_input_of_round(r+1)
        Constr = []
        
        Constr = Constr + MITMConstraints.equalConstraints(_Y(ShiftRow(Input_round)), _Y(Input_MC))
        for j in range(4):
            Constr = Constr + MITMConstraints.BackwardDet_LinearLayer(Inv_MC, _Y(column(Output_round,j)), _Y(column(Input_MC,j)))
        return Constr
              
        
    def genConstraints_GuessedKey_forwardkeyrecovery(self, r):
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ
        Input_round = self.genVars_input_of_round(r)
        Constr = []
        Constr = Constr + MITMConstraints.equalConstraints(_Y(Input_round), _Z(Input_round))
        return Constr
            
    def genVars_subkey(self, r):
        return ['SK_' + str(j) + '_r' + str(r) for j in range(8)]
    
    def genConstraints_guessedkey_IS(self, backwardRounds, forwardRounds):#guessed subkeys
        Constr = []
        _Z = BasicTools.typeZ
        for i in range(1, backwardRounds + 1):
            SK = self.genVars_subkey(backwardRounds - i)
            Input_MC = self.genVars_input_of_MixColumn(-i)
            for row in range(2):
                for col in range(4):
                    Constr = Constr + [SK[4*row + col]+ ' - '+ _Z(Input_MC)[4*row + ((col + row)%4)] + ' = 0']
            
        for i in range(0, forwardRounds):
            SK = self.genVars_subkey(backwardRounds + self.totalRounds + i)
            Input_round = self.genVars_input_of_round(self.totalRounds + i)
            for j in range(0, 8):
                    Constr = Constr + [SK[j] + ' - ' + _Z(Input_round)[j] + ' = 0']
        return Constr


       
    def genConstraints_of_keyrecovery(self, backwardRounds, forwardRounds):
        Constr = []
        #constraints of distinguisher
        Constr = Constr + self.genConstraints_Additional()
        for i in range(0, self.totalRounds):
            Constr = Constr + self.genConstraints_of_Round(i)
            
        #constraints of keyrecovery process
        for i in range(1, backwardRounds + 1):
            Constr = Constr + self.genConstraints_backwardkeyrecovery(-i)
            Constr = Constr + self.genConstraints_GuessedKey_backwardkeyrecovery(-i)
        for i in range(0, forwardRounds):
            Constr = Constr + self.genConstraints_forwardkeyrecovery(self.totalRounds + i)
            Constr = Constr + self.genConstraints_GuessedKey_forwardkeyrecovery(self.totalRounds + i)
        
        Constr = Constr + self.genConstraints_guessedkey_IS(backwardRounds, forwardRounds)
        return Constr

    def genConstraints_additional_keyrecovery(self, backwardRounds):
        _X = BasicTools.typeX
        Input_round = self.genVars_input_of_round(-backwardRounds)
        Constr = [BasicTools.plusTerm(_X(Input_round)) + ' <= ' + str(self.wc - 1)] #limits of the data complexity
        return Constr
    
    def genObjective_keyrecovery(self, backwardRounds, forwardRounds):
        _Z = BasicTools.typeZ
        GK = []
        for i in range(0, backwardRounds):
            GK = GK + self.genVars_subkey(i)
        for i in range(0, forwardRounds):
            GK = GK + self.genVars_subkey(backwardRounds + self.totalRounds + i)
        return BasicTools.plusTerm(GK)

#    def genObjective_keyrecovery(self, backwardRounds, forwardRounds):
#        _X = BasicTools.typeX
#        _Y = BasicTools.typeY
#        GV = []
#        for i in range(1, backwardRounds):
#            GV = GV + _X(self.genVars_input_of_round(-i))
#        for i in range(0, forwardRounds):
#            GV = GV + _Y(self.genVars_input_of_round(self.totalRounds + i))[0:8]
#        return BasicTools.plusTerm(GV)
#        
        
    #backwardRounds (forwardRounds) is the added rounds before (resp. after) the distinguisher.                
    def genModel_keyrecovery(self, file, backwardRounds, forwardRounds):

        V = set([])
        Constr = list([])     
        Constr = Constr + self.genConstraints_additional_keyrecovery(backwardRounds)
        Constr = Constr + self.genConstraints_of_keyrecovery(backwardRounds, forwardRounds)

        V = BasicTools.getVariables_From_Constraints(Constr)

        myfile=open(file,'w')
        print('Minimize', file = myfile)
        print(self.genObjective_keyrecovery(backwardRounds, forwardRounds), file = myfile)
        print('\n', file = myfile)
        print('Subject To', file = myfile)
        for c in Constr:
            print(c, file = myfile)

        print('\n', file = myfile)
        print('Binary', file = myfile)
        for v in V:
            print(v, file = myfile)
        myfile.close()
   










