
from CPMITM import *

Pi = [5,0,1,4,7,12,3,8,13,6,9,2,15,10,11,14]


class MITM_TWINE(Cipher):
    def genVars_input(self,r):
        if r >= 0:
            return ['Input_'+str(j)+'_r'+str(r) for j in range(0, self.wc)]
        else:
            return ['Input_'+str(j)+'_r_minus_'+str(-r) for j in range(0, self.wc)]

    def genVars_inputSbox(self,r):
        if r >= 0:
            return ['IS_'+str(j)+'_r'+str(r) for j in range(0, self.wc//2)]
        else:
            return ['IS_'+str(j)+'_r_minus_'+str(-r) for j in range(0, self.wc//2)]

    def genVars_inputPerm(self,r):
        if r >= 0:
            return ['IPerm_'+str(j)+'_r'+str(r) for j in range(0, self.wc)]
        else:
            return ['IPerm_'+str(j)+'_r_minus_'+str(-r) for j in range(0, self.wc)]
    

    def genConstraints_of_Round(self, r):
        _X = BasicTools.typeX
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ
        
        Input = self.genVars_input(r)
        IS = self.genVars_inputSbox(r)
        Input_Perm = self.genVars_inputPerm(r)
        Output  = self.genVars_input(r+1)
        
        Input_left = [Input[2*j] for j in range(8)]
        Input_right = [Input[2*j+1] for j in range(8)]
        Input_Perm_left = [Input_Perm[2*j] for j in range(8)]
        Input_Perm_right = [Input_Perm[2*j+1] for j in range(8)]
        
        Constr = []
        
        #1. constraints for forward differential
        #3-branch structure
        for j in range(8):
            Constr = Constr + MITMConstraints.ForwardDiff_Branch(_X(Input_left)[j],[_X(IS)[j],_X(Input_Perm_left)[j]])        
        #XOR operation          
        for j in range(8):
            Constr = Constr + MITMConstraints.ForwardDiff_XOR([_X(IS)[j],_X(Input_right)[j]],_X(Input_Perm_right)[j])
        #permutation
        Constr = Constr + MITMConstraints.PermConstraints(Pi,_X(Input_Perm),_X(Output))
        
        #2. constraints for backward determination
       
        for j in range(8):
            Constr = Constr + MITMConstraints.BackwardDet_Branch(_Y(Input_left)[j],[_Y(IS)[j],_Y(Input_Perm_left)[j]])
           
        for j in range(8):
            Constr = Constr + MITMConstraints.BackwardDet_XOR([_Y(IS)[j],_Y(Input_right)[j]],_Y(Input_Perm_right)[j])
         
        Constr = Constr + MITMConstraints.PermConstraints(Pi,_Y(Input_Perm),_Y(Output))
        
        
        # 3. Constraints of the relationship of type X and type Y vars
        Constr = Constr +  MITMConstraints.relationXYZ(_X(Input),_Y(Input),_Z(Input))
        Constr = Constr +  MITMConstraints.relationXYZ(_X(IS),_Y(IS),_Z(IS))
        Constr = Constr +  MITMConstraints.relationXYZ(_X(Input_Perm),_Y(Input_Perm),_Z(Input_Perm))
        return Constr

    def genConstraints_Additional(self):
        _X = BasicTools.typeX
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ
        
        Constr = []
        plaintext = self.genVars_input(0)
        ciphertext = self.genVars_input(self.totalRounds)
        A = BasicTools.typeX(plaintext)
        B = BasicTools.typeY(ciphertext)

        Constr = []
        Constr = Constr +  MITMConstraints.relationXYZ(_X(ciphertext), _Y(ciphertext), _Z(ciphertext))
        Constr = Constr + [BasicTools.plusTerm(A) + ' >= 1']
        Constr = Constr + [BasicTools.plusTerm(B) + ' >= 1']
        Constr = Constr + [self.genObjectiveFun_to_Round(self.totalRounds) + ' <= '+ str(self.wc_key - 1)]
        
        A1 = [str(self.wc_key) + ' ' + A[j] for j in range(0, self.wc)]
        B1 = ['15 ' + B[j] for j in range(0, self.wc)]
        Constr = Constr + [self.genObjectiveFun_to_Round(self.totalRounds) + ' - ' + BasicTools.MinusTerm(A1) + ' - ' + BasicTools.MinusTerm(B1) + ' <= ' + str(-self.wc_key-1)]

        return Constr

    def genObjectiveFun_to_Round(self,i):
        terms = []
        for j in range(i):
            terms = terms + self.genVars_inputSbox(j)
        return BasicTools.plusTerm(BasicTools.typeZ(terms))




        
     #following is the key-recovery process
      #backward differential process, r < 0
    def genConstraints_backwardkeyrecovery(self, r):
        assert r < 0
        _X = BasicTools.typeX
        
        Input = self.genVars_input(r)
        IS = self.genVars_inputSbox(r)
        Iperm = self.genVars_inputPerm(r)
        Output  = self.genVars_input(r+1)
        
      
        Input_left = [Input[2*j] for j in range(8)]
        Input_right = [Input[2*j+1] for j in range(8)]
        Iperm_left = [Iperm[2*j] for j in range(8)]
        Iperm_right = [Iperm[2*j+1] for j in range(8)]
        Constr = []
        #permutation
        Constr = Constr + MITMConstraints.PermConstraints(Pi, _X(Iperm), _X(Output))       
        #3-branch structure
        for j in range(8):
            Constr = Constr + MITMConstraints.ForwardDiff_Branch(_X(Iperm_left)[j], [_X(Input_left)[j], _X(IS)[j]])
        # XOR
        for j in range(8):
            Constr = Constr + MITMConstraints.ForwardDiff_XOR([_X(IS)[j], _X(Iperm_right)[j]], _X(Input_right)[j])
        return Constr
    
    #we let r < 0 for the added rounds before the distinguisher.
    def genConstraints_guessedValue_backwardkeyrecovery(self, r):
        assert r < 0
        _Z = BasicTools.typeZ
        _X = BasicTools.typeX

        Input = self.genVars_input(r)
        IS = self.genVars_inputSbox(r)
        Iperm = self.genVars_inputPerm(r)
        Output  = self.genVars_input(r+1)
        
        Input_left = [Input[2*j] for j in range(8)]
        Input_right = [Input[2*j+1] for j in range(8)]
        Iperm_left = [Iperm[2*j] for j in range(8)]
        Iperm_right = [Iperm[2*j+1] for j in range(8)]
        Constr = []
        
        #initialization
        if r == -1:
            Constr = Constr + MITMConstraints.equalConstraints(_Z(Input_left), _Z(IS))
            Constr = Constr + MITMConstraints.equalConstraints(_Z(IS), _X(IS))

            for j in range(8):
                Constr = Constr + [_Z(Input_right)[j] + ' = 0']
                
        else:
        #permutation
            Constr = Constr + MITMConstraints.PermConstraints(Pi,_Z(Iperm), _Z(Output))
            #XOR,SBox
            Constr = Constr + MITMConstraints.equalConstraints(_Z(Input_right), _Z(Iperm_right))
            for j in range(8): #which is similar to BackwardDet_Branch
                Constr = Constr + MITMConstraints.BackwardDet_Branch(_Z(IS)[j], [_Z(Iperm_right)[j], _X(IS)[j]])
            #3-branch
            for j in range(8):
                Constr = Constr + MITMConstraints.BackwardDet_Branch(_Z(Input_left)[j], [_Z(Iperm_left)[j], _Z(IS)[j]])
        return Constr
    
    
    def genConstraints_forwardkeyrecovery(self, r):#forward determination       
        _Y = BasicTools.typeY
        Input = self.genVars_input(r)
        IS = self.genVars_inputSbox(r)
        Input_Perm = self.genVars_inputPerm(r)
        Output  = self.genVars_input(r+1)

        Input_left = [Input[2*j] for j in range(8)]
        Input_right = [Input[2*j+1] for j in range(8)]
        Input_Perm_left = [Input_Perm[2*j] for j in range(8)]
        Input_Perm_right = [Input_Perm[2*j+1] for j in range(8)]
                    
        Constr = []
        #3-branch structure
        for j in range(8):
            Constr = Constr + MITMConstraints.BackwardDet_Branch(_Y(Input_Perm_left)[j],[_Y(Input_left)[j],_Y(IS)[j]])
        #XOR
        for j in range(8):
            Constr = Constr + MITMConstraints.BackwardDet_XOR([_Y(IS)[j],_Y(Input_Perm_right)[j]],_Y(Input_right)[j])
        #permutation
        Constr = Constr + MITMConstraints.PermConstraints(Pi,_Y(Input_Perm),_Y(Output))
        return Constr

    def genConstraints_guessedValue_forwardkeyrecovery(self, r):
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ
        IS = self.genVars_inputSbox(r)
        Constr = MITMConstraints.equalConstraints(_Y(IS), _Z(IS))
        return Constr

    def genVars_subkey(self, r):
        return ['SK_'+str(j)+'_r'+str(r) for j in range(0, self.wc_key)]
    
    def genConstraints_guessedkey_IS(self, backwardRounds, forwardRounds):
        _Z = BasicTools.typeZ
        Constr = []
        if self.wc_key == 32:
            CK = [2,3,12,15,17,18,28,31] #extract positons of round subkey
        if self.wc_key == 20:
            CK = [1,3,4,6,13,14,15,16]
        for i in range(1, backwardRounds + 1):
            SK = self.genVars_subkey(backwardRounds - i)
            IS = self.genVars_inputSbox(-i)
            for j in range(len(CK)):
                Constr = Constr + [SK[CK[j]] + ' - ' + _Z(IS)[j] + ' >= 0']
        for i in range(forwardRounds):
            SK = self.genVars_subkey(backwardRounds + self.totalRounds + i)
            IS = self.genVars_inputSbox(self.totalRounds + i)
            for j in range(len(CK)):
                Constr = Constr + [SK[CK[j]]+' - '+ _Z(IS)[j]+' >= 0']
        return Constr

  

    #we guessed keys of MR-th round subkey instead of masterkey.
    def genConstraints_keyschedule(self, backwardRounds, forwardRounds, MR):

        assert MR < self.totalRounds + backwardRounds + forwardRounds
        T = self.totalRounds + backwardRounds + forwardRounds
        Constr = []
        if self.wc_key == 32:
            LLL = [1,4,23]
            CLL = [0,16,30]
            CK = [2,3,12,15,17,18,28,31]
            KPI = [31,28,29,30] + [j for j in range(0, self.wc_key)]
        else:
            LLL = [1,4]
            CLL = [0,16]
            CK = [1,3,4,6,13,14,15,16]
            KPI = [19,16,17,18] + [j for j in range(0, self.wc_key)]
        SLL = set([j for j in range(0, self.wc_key)]) - set(LLL)


        for i in range(0, MR):
            RK_0 = self.genVars_subkey(i)
            RK_1 = self.genVars_subkey(i+1)
            for j in SLL:
                Constr = Constr + [RK_0[j] + ' - ' + RK_1[KPI[j]] + ' = 0']
            for j in range(len(LLL)):
                Constr = Constr + MITMConstraints.zeroprop([RK_1[KPI[CLL[j]]], RK_1[KPI[LLL[j]]]], RK_0[LLL[j]])

        for i in range(MR, T-1):
            RK_0 = self.genVars_subkey(i)
            RK_1 = self.genVars_subkey(i+1)
            for j in SLL:
                Constr = Constr + [RK_0[j] + ' - ' + RK_1[KPI[j]] + ' = 0']
            for j in range(len(LLL)):
                Constr = Constr + MITMConstraints.zeroprop([RK_0[LLL[j]], RK_0[CLL[j]]], RK_1[KPI[LLL[j]]])
        return Constr
    
    #we guessed keys of MR-th round subkey instead of masterkey.
    def genConstraints_of_keyrecovery(self, backwardRounds, forwardRounds, MR):
        Constr = []
        #constraints of distinguisher
        Constr = Constr + self.genConstraints_Additional()
        for i in range(0, self.totalRounds):
            Constr = Constr + self.genConstraints_of_Round(i)
            
        #constraints of keyrecovery process
        for i in range(1, backwardRounds + 1):
            Constr = Constr + self.genConstraints_backwardkeyrecovery(-i)
            Constr = Constr + self.genConstraints_guessedValue_backwardkeyrecovery(-i)
        for i in range(0, forwardRounds):
            Constr = Constr + self.genConstraints_forwardkeyrecovery(self.totalRounds + i)
            Constr = Constr + self.genConstraints_guessedValue_forwardkeyrecovery(self.totalRounds + i)
        #constraints of key-schedule
        Constr = Constr + self.genConstraints_guessedkey_IS(backwardRounds, forwardRounds)
        Constr = Constr + self.genConstraints_keyschedule(backwardRounds, forwardRounds, MR)
        return Constr
    
    #we guessed keys of MR-th round subkey instead of masterkey.
    def genObjectiveFun_keyrecovery(self, MR):
        guessedkey = self.genVars_subkey(MR)
        return BasicTools.plusTerm(guessedkey)    
    
    #we guessed keys of MR-th round subkey instead of masterkey.
    def genConstraints_additional_keyrecovery(self, backwardRounds, MR):
        _X = BasicTools.typeX 
        plaintext = self.genVars_input(-backwardRounds)
        Constr = [BasicTools.plusTerm(_X(plaintext)) + ' <= ' + str(self.wc - 1)]
        Constr = Constr + [self.genObjectiveFun_keyrecovery(MR) + ' <= ' + str(self.wc_key - 1)]
        return Constr
        
        
     #we guessed keys of MR-th round subkey instead of masterkey.   
    def genModel_keyrecovery(self, file, backwardRounds, forwardRounds, MR):

        V = set([])
        Constr = list([])
       
        Constr = Constr + self.genConstraints_additional_keyrecovery(backwardRounds, MR)
        Constr = Constr + self.genConstraints_of_keyrecovery(backwardRounds, forwardRounds, MR)



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













