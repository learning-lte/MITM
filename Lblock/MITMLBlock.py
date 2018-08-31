
from CPMITM import *

linearM = [2,0,3,1,6,4,7,5]



class MITM_Lblock(Cipher):
    
    def genVars_input_left(self, r):
        if r >= 0:
            return ['L_'+ str(j)+'_r'+str(r) for j in range(0, self.wc//2)]
        else:
            return ['L_'+ str(j)+'_r_minus_'+str(-r) for j in range(0, self.wc//2)]
    def genVars_input_right(self, r):
        if r >= 0:
            return ['R_'+ str(j)+'_r'+str(r) for j in range(0, self.wc//2)]
        else:
            return ['R_'+ str(j)+'_r_minus_'+str(-r) for j in range(0, self.wc//2)]
    def genVars_input_F(self, r):
        if r >= 0:
            return ['IF_'+ str(j)+'_r'+str(r) for j in range(0, self.wc//2)]
        else:
            return ['IF_'+ str(j)+'_r_minus_'+str(-r) for j in range(0, self.wc//2)]
    def genVars_output_F(self, r):
        if r >= 0:
            return ['OL_'+ str(j)+'_r'+str(r) for j in range(0, self.wc//2)]
        else:
            return ['OL_'+ str(j)+'_r_minus_'+str(-r) for j in range(0, self.wc//2)]
            
    
    def genConstraints_of_Round(self, r):
         
        _X = BasicTools.typeX
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ   
    
        Input_L= self.genVars_input_left(r)
        Input_R = self.genVars_input_right(r)
        Input_F = self.genVars_input_F(r)
        Output_F = self.genVars_output_F(r) 
        Output_L = self.genVars_input_left(r+1)
        Output_R = self.genVars_input_right(r+1)
        
        Constr = []
        #1. constraints for forward differential
        #constraints for 3-branch
        for j in range(8):
            Constr = Constr + MITMConstraints.ForwardDiff_Branch(_X(Input_L)[j], [_X(Input_F)[j], _X(Output_R)[j]])
        #constraints  for linear permutation
        Constr = Constr + MITMConstraints.PermConstraints(linearM,_X(Input_F), _X(Output_F))
        #constraints for XOR
        for j in range(8):
            Constr = Constr + MITMConstraints.ForwardDiff_XOR([_X(Output_F)[j], _X(Input_R)[(j+2)%8]], _X(Output_L)[j])
   
        #2. constraints for backward determination
        for j in range(8):
            Constr = Constr + MITMConstraints.BackwardDet_Branch(_Y(Input_L)[j], [_Y(Input_F)[j], _Y(Output_R)[j]])
        Constr = Constr + MITMConstraints.PermConstraints(linearM,_Y(Input_F), _Y(Output_F))
        for j in range(8):
            Constr = Constr + MITMConstraints.BackwardDet_XOR([_Y(Output_F)[j], _Y(Input_R)[(j+2)%8]], _Y(Output_L)[j])
            
        # 3. Constraints of the relationship of type X and type Y vars
        Constr = Constr + MITMConstraints.relationXYZ(_X(Input_L), _Y(Input_L), _Z(Input_L))
        Constr = Constr + MITMConstraints.relationXYZ(_X(Input_R), _Y(Input_R), _Z(Input_R))
        Constr = Constr + MITMConstraints.relationXYZ(_X(Input_F), _Y(Input_F), _Z(Input_F))
        Constr = Constr + MITMConstraints.relationXYZ(_X(Output_F), _Y(Output_F), _Z(Output_F))
        return Constr



    def genConstraints_Additional(self):
        Constr = []
        _X = BasicTools.typeX
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ 
        
        plaintext_L= self.genVars_input_left(0)
        plaintext_R = self.genVars_input_right(0)
        ciphertext_L = self.genVars_input_left(self.totalRounds)
        ciphertext_R = self.genVars_input_right(self.totalRounds)
        
        A = BasicTools.typeX(plaintext_L + plaintext_R)
        B = BasicTools.typeY(ciphertext_L + ciphertext_R)

        Constr = []
        Constr = Constr +  MITMConstraints.relationXYZ(_X(ciphertext_L + ciphertext_R), _Y(ciphertext_L + ciphertext_R),_Z(ciphertext_L + ciphertext_R))
        Constr = Constr + [BasicTools.plusTerm(A) + ' >= 1']
        Constr = Constr + [BasicTools.plusTerm(B) + ' >= 1']
        Constr = Constr + [self.genObjectiveFun_to_Round(self.totalRounds) + ' <= ' + str(self.wc_key - 1)]
        
        A1 = ['7 ' + A[j] for j in range(0, self.wc)]
        B1 = ['7 ' + B[j] for j in range(0, self.wc)]
        Constr = Constr + [self.genObjectiveFun_to_Round(self.totalRounds) + ' - ' + BasicTools.MinusTerm(A1) + ' - ' + BasicTools.MinusTerm(B1) + ' <= 0']
        return Constr

    def genObjectiveFun_to_Round(self, i):
        terms = []
        for j in range(i):
            terms = terms + self.genVars_input_F(j)
        return BasicTools.plusTerm(BasicTools.typeZ(terms))




    #following is the key recovery process
    def genContraints_backwardkeyrecovery(self, r): #backward differential process, r < 0
        assert r < 0
        _X = BasicTools.typeX  
    
        Input_left = self.genVars_input_left(r)
        Input_right = self.genVars_input_right(r)
        Input_F = self.genVars_input_F(r)
        Ouput_F = self.genVars_output_F(r) 
        Ouput_left = self.genVars_input_left(r+1)
        Output_right = self.genVars_input_right(r+1) 
        #constraints for 3-branch 
        Constr = []
        for j in range(0, 8):
            Constr = Constr + MITMConstraints.ForwardDiff_Branch(_X(Output_right)[j], [_X(Input_left)[j], _X(Input_F)[j]])
         #constraints  for linear permutation 
        Constr = Constr + MITMConstraints.PermConstraints(linearM,_X(Input_F), _X(Ouput_F))        
        #constraints for XOR
        for j in range(0, 8):
            Constr = Constr + MITMConstraints.ForwardDiff_XOR([_X(Ouput_left)[j], _X(Ouput_F)[j]], _X(Input_right)[(j+2)%8])
        return Constr

       

    def genContraints_guessedValue_backwardkeyrecovery(self, r):
        assert r < 0
        _X = BasicTools.typeX
        _Z = BasicTools.typeZ
        
        Input_left = self.genVars_input_left(r)
        Input_right = self.genVars_input_right(r)
        Input_F = self.genVars_input_F(r)
        Ouput_F = self.genVars_output_F(r) 
        Output_left = self.genVars_input_left(r+1)
        Output_right = self.genVars_input_right(r+1)        
        Constr = []
        if r == -1:
            Constr = Constr + MITMConstraints.equalConstraints(_X(Input_F), _Z(Input_F))
            Constr = Constr + MITMConstraints.equalConstraints(_Z(Input_left), _Z(Input_F))
            for j in range(8):
                Constr = Constr + [_Z(Input_right)[j] + ' = 0']
                Constr = Constr + [_Z(Ouput_F)[j] + ' = 0']
        else:
            #3-branch
            for j in range(8):
                 Constr = Constr + MITMConstraints.BackwardDet_Branch(_Z(Input_left)[j], [_Z(Input_F)[j], _Z(Output_right)[j]])
            #XOR
            for j in range(8):
                Constr = Constr + MITMConstraints.BackwardDet_XOR([_Z(Ouput_F)[j], _Z(Input_right)[(j+2)%8]], _Z(Output_left)[j])
            #linear permutation,SBOX
            for j in range(8):
                Constr = Constr + MITMConstraints.BackwardDet_Branch(_Z(Input_F)[j], [_X(Input_F)[j], _Z(Ouput_F)[linearM[j]]])
        return Constr
    
    #forward determination
    def genContraints_forwardkeyrecovery(self, r):  
        _Y = BasicTools.typeY
        Input_left = self.genVars_input_left(r)
        Input_right = self.genVars_input_right(r)
        Input_F = self.genVars_input_F(r)
        Output_F = self.genVars_output_F(r) 
        Output_left = self.genVars_input_left(r+1)
        Output_right = self.genVars_input_right(r+1)
        Constr = []
        #3-Branch
        for j in range(8):
            Constr = Constr + MITMConstraints.BackwardDet_Branch(_Y(Output_right)[j], [_Y(Input_left)[j], _Y(Input_F)[j]])
        #XOR
        for j in range(8):
            Constr = Constr + MITMConstraints.BackwardDet_XOR([_Y(Output_left)[j], _Y(Output_F)[j]], _Y(Input_right)[(j+2)%8])
        #linear permutation
        Constr = Constr + MITMConstraints.PermConstraints(linearM, _Y(Input_F), _Y(Output_F))
        return Constr
              
        
    def genContraints_guessedValue_forwardkeyrecovery(self, r):
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ
        Input_F = self.genVars_input_F(r)
        Constr = []
        Constr = Constr + MITMConstraints.equalConstraints(_Y(Input_F), _Z(Input_F))
        return Constr
            
    def genVars_subkey(self, r):
        return ['SK_'+str(j)+'_r'+str(r) for j in range(self.keysize)]
    
    def genContraints_guessedkey_IS(self, backwardRounds, forwardRounds):
        Constr = []
        _Z = BasicTools.typeZ
        for i in range(1, backwardRounds+1):
            SK = self.genVars_subkey(backwardRounds - i)
            Input_F = self.genVars_input_F(-i)
            for j in range(8):
                for l in range(4):
                    Constr = Constr + [SK[4*j + l] + ' - ' + _Z(Input_F)[j] + ' >= 0']
        for i in range(forwardRounds):
            SK = self.genVars_subkey(backwardRounds + self.totalRounds + i)
            Input_F = self.genVars_input_F(self.totalRounds + i)
            for j in range(8):
                for l in range(4):
                    Constr = Constr + [SK[4*j + l] +' - '+_Z(Input_F)[j]+' >= 0']
        return Constr
 
    #keybridging techniques, we guessed subkeys of MR-th round instead masterkey for lblcok . 
    def genContraints_keyschedule(self, backwardRounds , forwardRounds, MR):

        assert MR < self.totalRounds + backwardRounds + forwardRounds
        T = self.totalRounds + backwardRounds + forwardRounds
        Constr = []
        for i in range(MR):
            RK_0 = self.genVars_subkey(i)
            RK_1 = self.genVars_subkey(i+1)
            for j in range(2, 20):
                for j1 in range(0, 4):
                    Constr = Constr + [RK_0[(4*j+j1 +29)%80] + ' - ' + RK_1[4*j+j1] + ' = 0']
            for j in range(0, 2):
                for j1 in range(0, 4):
                    Constr = Constr + MITMConstraints.zeroprop([RK_1[4*j], RK_1[4*j+1], RK_1[j*4+2], RK_1[4*j+3]], RK_0[(4*j+j1+29)%80])

        for i in range(MR, T-1):
            RK_0 = self.genVars_subkey(i)
            RK_1 = self.genVars_subkey(i+1)
            for j in range(2,20):
                for j1 in range(0, 4):
                    Constr = Constr + [RK_0[(4*j + j1 + 29)%80] + ' - '+RK_1[4*j+j1] + ' = 0']
            for j in range(2):
                for j1 in range(4):
                    Constr = Constr + MITMConstraints.zeroprop([RK_0[(4*j+29)%80], RK_0[(4*j+1+29)%80], RK_0[(4*j+2+29)%80], RK_0[(4*j+3+29)%80]], RK_1[4*j+j1])
        return Constr

       
    def getTotalConstraints_of_keyrecovery(self, backwardRounds, forwardRounds, MR):
        Constr = []
        #constraints of distinguisher
        Constr = Constr + self.genConstraints_Additional()
        for i in range(self.totalRounds):
            Constr = Constr + self.genConstraints_of_Round(i)
            
        #constraints of keyrecovery process
        for i in range(1, backwardRounds + 1):
            Constr = Constr + self.genContraints_backwardkeyrecovery(-i)
            Constr = Constr + self.genContraints_guessedValue_backwardkeyrecovery(-i)
        for i in range(forwardRounds):
            Constr = Constr + self.genContraints_forwardkeyrecovery(self.totalRounds + i)
            Constr = Constr + self.genContraints_guessedValue_forwardkeyrecovery(self.totalRounds + i)
            
        #constraints of key-schedule
        Constr = Constr + self.genContraints_guessedkey_IS(backwardRounds, forwardRounds)
        Constr = Constr + self.genContraints_keyschedule(backwardRounds , forwardRounds, MR)
        return Constr

    def genObjectiveFun_keyrecovery(self, MR):
        guessedkey = self.genVars_subkey(MR)
        return BasicTools.plusTerm(guessedkey)
    
    #we guessed subkeys of MR-th round.
    def genContraints_additional_keyrecovery(self, backwardRounds, MR):
        _X = BasicTools.typeX
        plaintext = self.genVars_input_left(-backwardRounds) + self.genVars_input_right(-backwardRounds)
        Constr = [BasicTools.plusTerm(_X(plaintext)) + ' <= ' + str(self.wc - 1)]
        Constr = Constr + [self.genObjectiveFun_keyrecovery(MR) + ' <= ' + str(self.keysize - 1)]
        return Constr
    
    
    #backwardRounds(forwardRounds) are the added rounds before(resp. after) the distinguisher.
    #we guessed the subkeys of MR-th round.
    def genModel_keyrecovery(self, file, backwardRounds, forwardRounds, MR):

        V = set([])
        Constr = list([])
       
        Constr = Constr + self.genContraints_additional_keyrecovery(backwardRounds, MR)
        Constr = Constr + self.getTotalConstraints_of_keyrecovery(backwardRounds, forwardRounds, MR)

        

        V = BasicTools.getVariables_From_Constraints(Constr)

        myfile=open(file,'w')
        print('Minimize', file = myfile)
        print(self.genObjectiveFun_keyrecovery(MR), file = myfile)
        print('\n', file = myfile)
        print('Subject To', file = myfile)

        for c in Constr:
            print(c, file = myfile)

        print('\n', file = myfile)
        print('Binary', file = myfile)
        for v in V:
            print(v, file = myfile)
        myfile.close()





