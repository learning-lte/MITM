
from CPMITM import *

MC = [[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]
inv_MC = MC

class MITM_AES(Cipher):
    def genVars_input_of_round(self,r):
        if r >= 0:
            return ['S_'+ str(j)+'_r'+str(r) for j in range(16)]
        else:
            return ['S_'+ str(j)+'_r_minus'+str(-r) for j in range(16)]
    
    def genVars_input_of_MixColumn(self,r):
        if r >= 0:
            return ['V_'+str(j)+'_r'+str(r) for j in range(16)]
        else:
            return ['V_'+str(j)+'_r_minus'+str(-r) for j in range(16)]

    def genVars_added(self,r):
        if r >= 0:
            return ['Add_'+ str(j)+'_r'+str(r) for j in range(4)]
        else:
            return ['Add_'+ str(j)+'_r_minus'+str(-r) for j in range(4)]


    def genConstraints_of_Round(self, r):
        _X = BasicTools.typeX
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ

        Input_round = self.genVars_input_of_round(r)
        Input_MC = self.genVars_input_of_MixColumn(r)
        Output_round = self.genVars_input_of_round(r+1)
        Added_var = self.genVars_added(r)

        constr =[]

        # 1. Constraints of Foward Differential
        # - Constraints for S-box and ShiftRow
        constr = constr + MITMConstraints.equalConstraints(_X(ShiftRow_AES(Input_round)), _X(Input_MC))
        # - Constraints for MixCols
        if r == 0:
            for j in range(0, 4):
                constr = constr + MITMConstraints.FowrwardDiff_TruncatedDiff_AESMixColumn(_X(column(Input_MC, j)), _X(column(Output_round, j)), _X(Added_var)[j])
        else:
            for j in range(0, 4):
                constr = constr + MITMConstraints.ForwardDiff_LinearLayer(MC, _X(column(Input_MC, j)), _X(column(Output_round, j)))

        # 2. Constraints of Backward Determination
        # - Constraints for S-box and ShiftRow
        constr = constr + MITMConstraints.equalConstraints(_Y(ShiftRow_AES(Input_round)), _Y(Input_MC))
        # - Constraints for MixCols
        if r == self.totalRounds - 1:
            for j in range(0, 4):
                constr = constr + MITMConstraints.BackwardDet_TruncatedDiff_AESMixColumn(_Y(column(Input_MC, j)), _Y(column(Output_round, j)), _Y(Added_var)[j])
        else:
            for j in range(0, 4):
                constr = constr + MITMConstraints.BackwardDet_LinearLayer(MC, _Y(column(Input_MC, j)), _Y(column(Output_round, j)))

        # 3. Constraints of the relationship of type X,type Y and type Z vars
        constr = constr + MITMConstraints.relationXYZ(_X(Input_round), _Y(Input_round), _Z(Input_round))
        constr = constr + MITMConstraints.relationXYZ(_X(Input_MC), _Y(Input_MC), _Z(Input_MC))


        return constr


    def genObjectiveFun_to_Round(self, i):
        _Z = BasicTools.typeZ
        terms = []
        cut_terms = []

        for j in range(1, i):
            terms = terms + _Z(self.genVars_input_of_round(j))

        return BasicTools.plusTerm(terms)

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
        #complexity bound
        Constr = Constr + [self.genObjectiveFun_to_Round(self.totalRounds) + ' <= ' + str(self.wc_key - 1 + 16)]
        return Constr



    #keyrecovery process
    #backward differential, similar to forward differential.
    def genConstraints_backwardkeyrecovery(self, r): 
        assert r < 0
        _X = BasicTools.typeX

        Input_round = self.genVars_input_of_round(r)
        Input_MC = self.genVars_input_of_MixColumn(r)
        Output_round = self.genVars_input_of_round(r+1)

        Constr = []
        #Constraints for inverse of MixColumn
        for j in range(4):
            Constr = Constr + MITMConstraints.ForwardDiff_LinearLayer(inv_MC, _X(column(Output_round,j)), _X(column(Input_MC,j)))
        #Constraints for the shiftrow and Sbox
        Constr = Constr + MITMConstraints.equalConstraints(_X(ShiftRow_AES(Input_round)), _X(Input_MC))

        return Constr


    #translate to plaintexts and value and subkeys, which is a backward determination process.
    def genConstraints_GuessedKey_backwardkeyrecovery(self, r):
        assert r < 0
        _X = BasicTools.typeX
        _Z = BasicTools.typeZ

        Input_round = self.genVars_input_of_round(r)
        Input_MC = self.genVars_input_of_MixColumn(r)
        Output_round = self.genVars_input_of_round(r+1)

        Constr = []

        for j in range(4):
            Constr = Constr + MITMConstraints.BackwardDet_LinearLayer(MC,_Z(column(Input_MC,j)), _Z(column(Output_round, j)))

        for i in range(4):
            for j in range(4):
                Constr = Constr + MITMConstraints.BackwardDet_Branch(_Z(Input_round)[4*i+j], [_X(Input_round)[4*i+j], _Z(Input_MC)[4*i+((j-i)%4)]])

        return Constr

    #forward determination: tranlate to the ciphertext and subkeys
    def genConstraints_forwardkeyrecovery(self, r):
        _Y = BasicTools.typeY

        Input_round = self.genVars_input_of_round(r)
        Input_MC = self.genVars_input_of_MixColumn(r)
        Output_round = self.genVars_input_of_round(r+1)
        Constr = []

        Constr = Constr + MITMConstraints.equalConstraints(_Y(ShiftRow_AES(Input_round)), _Y(Input_MC))
        for j in range(4):
            Constr = Constr + MITMConstraints.BackwardDet_LinearLayer(MC, _Y(column(Output_round,j)), _Y(column(Input_MC,j)))
        return Constr


    def genConstraints_GuessedKey_forwardkeyrecovery(self, r):
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ
        Input_MC = self.genVars_input_of_MixColumn(r)
        Constr = []
        Constr = Constr + MITMConstraints.equalConstraints(_Y(Input_MC), _Z(Input_MC))
        return Constr

    def genVars_subkey(self, r):
        return ['SK_' + str(j) + '_r' + str(r) for j in range(16)]
 
    #mark the guessed subkeys
    def genConstraints_guessedkey_IS(self, backwardRounds, forwardRounds):
        Constr = []
        _Z = BasicTools.typeZ
        for i in range(0, backwardRounds + 1):
            SK = self.genVars_subkey(i)
            Input_round = self.genVars_input_of_round(-(backwardRounds - i))
            for j in range(16):
                Constr = Constr + [SK[j] + ' - ' + _Z(Input_round)[j] + ' >= 0']

        for i in range(0, forwardRounds):
            SK = self.genVars_subkey(1 + backwardRounds + self.totalRounds + i)
            Input_MC = self.genVars_input_of_MixColumn(self.totalRounds + i)
            for j in range(0, 16):
                    Constr = Constr + [SK[j] + ' - ' + _Z(Input_MC)[j] + ' >= 0']
        return Constr

    #key bridging technique
    def genVars_cutting_guessed_subkey(self, r):
        return ['CSK_'+ str(j) + '_r' + str(r) for j in range(16)]


    #sk = [k1,k2,k3],ck, any two elements of sk can deduce the other one.
    #Thus if k1 = k2 = k3 = 1, we let ck = 1, reducing one guess.
    def gensubConstraints_cutting_guessed_subkey(self, sk, ck):
        C = []
        C = C + [BasicTools.plusTerm(sk) + ' - 3 '+ ck + ' >= 0']
        C = C + [BasicTools.plusTerm(sk) + ' - 2 '+ ck + ' <= 2']
        return C

    def genConstraints_cutting_guessed_subkey(self, backwardRounds, forwardRounds):
        NK = self.wc_key // 4
        Constr = []

        GuessedK_backward = []
        CK_column_backward = []
        for i in range(0, 1 + backwardRounds):
            SK = self.genVars_subkey(i)
            CK = self.genVars_cutting_guessed_subkey(i)

            for col in range(4):
                GuessedK_backward.append([SK[4*row + col] for row in range(4)])
                CK_column_backward.append([CK[4*row + col] for row in range(4)])

        for j in range(min(NK, len(GuessedK_backward))):
            for h in range(4):
                Constr = Constr + [CK_column_backward[j][h] + ' = 0']

        if len(GuessedK_backward) > NK:
            for j in range(NK, len(GuessedK_backward)):
                ck = CK_column_backward[j]
                sk = GuessedK_backward[j]
                sk_1 = GuessedK_backward[j-1]
                sk_NK = GuessedK_backward[j-NK]

                if j % NK == 0:

                    for h in range(4):
                        Constr = Constr + self.gensubConstraints_cutting_guessed_subkey([sk_1[(h+1)%4],sk_NK[h],sk[h]],ck[h])
                        
                else:
                    for h in range(4):
                            Constr = Constr + self.gensubConstraints_cutting_guessed_subkey([sk_1[h],sk_NK[h],sk[h]],ck[h])

        GuessedK_forward = []
        CK_column_forward = []
        
        for i in range(forwardRounds):
            SK = self.genVars_subkey(1 + backwardRounds + self.totalRounds + i)
            CK = self.genVars_cutting_guessed_subkey(1 + backwardRounds + self.totalRounds + i)
            for col in range(4):
                GuessedK_forward.append([SK[4*row + col] for row in range(4)])
                CK_column_forward.append([CK[4*row + col] for row in range(4)])

        for j in range(min(NK, len(GuessedK_forward))):
            for h in range(4):
                Constr = Constr + [CK_column_forward[j][h] + ' = 0']

        if len(GuessedK_forward) > NK:
            startCol = 4*(1 + backwardRounds + self.totalRounds)
            for j in range(NK, len(GuessedK_forward)):
                ck = CK_column_forward[j]
                sk = GuessedK_forward[j]
                sk_1 = GuessedK_forward[j - 1]
                sk_NK = GuessedK_forward[j - NK]

                if (startCol + j) % NK == 0 or (NK > 6 and (startCol + j) % NK == 4):
                    for h in range(4):
                        Constr = Constr +  [ck[h] + ' = 0']
                else:
                    for h in range(4):
                        Constr = Constr + self.gensubConstraints_cutting_guessed_subkey([sk[h], sk_1[h], sk_NK[h]], ck[h])
        return Constr
    #special property of AES
    def genConstraints_zeroR_keyrecovery(self, backwardRounds):
        sk = self.genVars_subkey(backwardRounds)
        sk1 = ['2 '+ sk[j] for j in range(16)]
        Constr = []
        Constr = Constr + [BasicTools.plusTerm(sk) + ' + 16 Ad0 <= 17']
        Constr = Constr + [BasicTools.plusTerm(sk1) + ' + Ad0 >= 3']
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

        #constraints of keybridging techniques
        Constr = Constr + self.genConstraints_cutting_guessed_subkey(backwardRounds, forwardRounds)

        return Constr


    def genConstraints_additional_keyrecovery(self, backwardRounds):
        _X = BasicTools.typeX
        Input_round = self.genVars_input_of_round(-backwardRounds)
        Constr = [BasicTools.plusTerm(_X(Input_round)) + ' <= ' + str(self.wc - 1)] #limits of the data complexity
        Constr = Constr + self.genConstraints_zeroR_keyrecovery(backwardRounds)
        return Constr

    def genObjective_keyrecovery(self, backwardRounds, forwardRounds):
        GK = []
        CK = []

        for i in range(0, backwardRounds + 1):
            GK = GK + self.genVars_subkey(i)
            CK = CK + self.genVars_cutting_guessed_subkey(i)
        for i in range(forwardRounds):
            GK = GK + self.genVars_subkey(1 + backwardRounds + self.totalRounds + i)
            CK = CK + self.genVars_cutting_guessed_subkey(1 + backwardRounds + self.totalRounds + i)
        Obj = BasicTools.plusTerm(GK) + ' - ' + BasicTools.MinusTerm(CK)+ ' - Ad0'
        return Obj


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
        print(self.genObjective_keyrecovery(backwardRounds, forwardRounds) +' <= '+str(self.wc_key - 1),file = myfile)
        for c in Constr:
            print(c, file = myfile)

        print('\n', file = myfile)
        print('Binary', file = myfile)
        for v in V:
            print(v, file = myfile)
        myfile.close()
