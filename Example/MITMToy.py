
from CPMITM import *

MC = [[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]]
inv_MC = MC

class MITM_Toy(Cipher):
    def genVars_input_of_round(self,r):
        if r >= 0:
            return ['S_'+ str(j)+'_r'+str(r) for j in range(4)]
        else:
            return ['S_'+ str(j)+'_r_minus'+str(-r) for j in range(4)]

    def genVars_input_of_MixColumn(self,r):
        if r >= 0:
            return ['V_'+str(j)+'_r'+str(r) for j in range(4)]
        else:
            return ['V_'+str(j)+'_r_minus'+str(-r) for j in range(4)]



    def genConstraints_of_Round(self, r):
        _X = BasicTools.typeX
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ

        Input_round = self.genVars_input_of_round(r)
        Input_MC = self.genVars_input_of_MixColumn(r)
        Output_round = self.genVars_input_of_round(r+1)

        constr =[]

        # 1. Constraints of Foward Differential
        constr = constr + MITMConstraints.equalConstraints(_X(Input_round), _X(Input_MC)) # - Constraints for S-box and ShiftRow
        # - Constraints for MixCols
        constr = constr + MITMConstraints.ForwardDiff_LinearLayer(MC, _X(Input_MC), _X(Output_round))

        # 2. Constraints of Backward Determination
        constr = constr + MITMConstraints.equalConstraints(_Y(Input_round), _Y(Input_MC))
        # - Constraints for MixCols
        constr = constr + MITMConstraints.BackwardDet_LinearLayer(MC, _Y(Input_MC), _Y(Output_round))

        # 3. Constraints of the relationship of type X and type Y vars
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

        Constr = Constr + [self.genObjectiveFun_to_Round(self.totalRounds) + ' <= ' + str(self.wc_key - 1)]
        return Constr


#keyrecovery process
    def genConstraints_backwardkeyrecovery(self, r): #backward differential process, r < 0
        assert r < 0
        _X = BasicTools.typeX

        Input_round = self.genVars_input_of_round(r)
        Input_MC = self.genVars_input_of_MixColumn(r)
        Output_round = self.genVars_input_of_round(r+1)

        Constr = []
        for j in range(4):
            Constr = Constr + MITMConstraints.ForwardDiff_LinearLayer(inv_MC, _X(Output_round), _X(Input_MC))
        Constr = Constr + MITMConstraints.equalConstraints(_X(Input_round), _X(Input_MC))

        return Constr



    def genConstraints_GuessedKey_backwardkeyrecovery(self, r):
        assert r < 0
        _X = BasicTools.typeX
        _Z = BasicTools.typeZ

        Input_round = self.genVars_input_of_round(r)
        Input_MC = self.genVars_input_of_MixColumn(r)
        Output_round = self.genVars_input_of_round(r+1)

        Constr = []
        Constr = Constr + MITMConstraints.BackwardDet_LinearLayer(MC, _Z(Input_MC), _Z(Output_round))

        for j in range(4):
            Constr = Constr + MITMConstraints.BackwardDet_Branch(_Z(Input_round)[j], [_X(Input_round)[j], _Z(Input_MC)[j]])

        return Constr


    def genConstraints_forwardkeyrecovery(self, r):#forward determination
        _Y = BasicTools.typeY

        Input_round = self.genVars_input_of_round(r)
        Input_MC = self.genVars_input_of_MixColumn(r)
        Output_round = self.genVars_input_of_round(r+1)
        Constr = []

        Constr = Constr + MITMConstraints.equalConstraints(_Y(Input_round), _Y(Input_MC))
        Constr = Constr + MITMConstraints.BackwardDet_LinearLayer(inv_MC, _Y(Output_round), _Y(Input_MC))
        return Constr


    def genConstraints_GuessedKey_forwardkeyrecovery(self, r):
        _Y = BasicTools.typeY
        _Z = BasicTools.typeZ
        Input_MC = self.genVars_input_of_MixColumn(r)
        Input_round = self.genVars_input_of_round(r)
        Constr = []
        Constr = Constr + MITMConstraints.equalConstraints(_Y(Input_MC), _Z(Input_MC))
        Constr = Constr + MITMConstraints.equalConstraints(_Y(Input_round), _Z(Input_round))
        return Constr

    def genVars_subkey(self, r):
        return ['SK_' + str(j) + '_r' + str(r) for j in range(4)]

    def genConstraints_guessedkey_IS(self, backwardRounds, forwardRounds):#guessed subkeys
        Constr = []
        _Z = BasicTools.typeZ
        for i in range(0, backwardRounds):
            SK = self.genVars_subkey(i)
            Input_round = self.genVars_input_of_round(-(backwardRounds - i))
            for j in range(self.wc):
                Constr = Constr + [SK[j] + ' - ' + _Z(Input_round)[j] + ' >= 0']

        for i in range(0, forwardRounds):
            SK = self.genVars_subkey(1 + backwardRounds + self.totalRounds + i)
            Input_MC = self.genVars_input_of_MixColumn(self.totalRounds + i)
            for j in range(0, self.wc):
                    Constr = Constr + [SK[j] + ' - ' + _Z(Input_MC)[j] + ' >= 0']
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
        GK = []
        for i in range(backwardRounds):
            GK = GK + self.genVars_subkey(i)
        for i in range(forwardRounds):
            GK = GK + self.genVars_subkey(1 + backwardRounds + self.totalRounds + i)

        return BasicTools.plusTerm(GK)


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
