# Programming the DS-MITM Attack with Constraints

These tools are part of the paper [Programming the DS-MITM Attack with Constraints](https://github.com/siweisun/MITM/blob/master/Programming%20the%20DS-MITM%20Attack.pdf) by Danping Shi, Siwei Sun, Patrick Derbez, Yosuke Todo, Bing Sun, and Lei Hu, which was accepted to [Asiacrypt 2018](https://asiacrypt.iacr.org/2018/).

## Dependencies

Our codes generate MILP models in the `*.lp` format, which are solved using [Gurobi](http://www.gurobi.com/), and the solutions are given in `*.sol` files. For a given model, we may want to list all feasible solutions. This can be done by the [SCIP](http://scip.zib.de/) solver with the following commands:

```
SCIP> read "model.lp"
SCIP> set constraints countsols collect TRUE
SCIP> count
SCIP> write allsolutions "solutions.txt"
```

Note that the file formats of the solution files generated by SCIP and Gurobi are different. We can convert the file format of the solution files of SCIP into the `*.sol` format with the routine `SCIP2Sol()` provided in `CPMITM.py`. Then the solution files `*.sol` can be parsed by the `SolFileParser` in `CPMITM.py`. 



## CPMITM.py

`CPMITM.py` is the main library that provides common functionalities for modelling the DS-MITM attack. When we are given a new cipher, we develop a new python module to generate MILP models by using the functionalities offered in `CPMITM.py`.  The class `MITMConstraints` contains the methods which output a list of constraints when given the the operation and its input / output variables. The most important methods are listed in the following.

- `ForwardDiff_LinearLayer(M, V_in, V_out):`
  - Input: the binary representation of a matrix M; the input variable list V_in; the output variable list V_out

  - Output: a list of constraints such that any binary solution corresponds to a valid forward differential propagation pattern.

  - Example:

    ```python
    >>> M = [[1,0,1,1],[1,0,0,0],[0,1,1,0],[1,0,1,0]]
    >>> a = ['a0', 'a1', 'a2', 'a3']
    >>> b = ['b0', 'b1', 'b2', 'b3']
    >>>
    >>> for c in MITMConstraints.ForwardDiff_LinearLayer(M, a, b): print(c)
    ...
    3 b0 -  a0 - a2 - a3 >= 0
    a0 + a2 + a3 - b0 >= 0
    1 b1 -  a0 >= 0
    a0 - b1 >= 0
    2 b2 -  a1 - a2 >= 0
    a1 + a2 - b2 >= 0
    2 b3 -  a0 - a2 >= 0
    a0 + a2 - b3 >= 0
    ```


- `ForwardDiff_XOR(V_in, b)`

  - Input: a list of  input variables to the XOR operation, and the output bit b

  - Output: a list of constraints describing how the forward differential propagate against the XOR operation

  - Example:

    ```python
    >>>a = ['a0','a1','a2']
    >>>b = 'b'
    >>>for c in MITMConstraints.ForwardDiff_XOR(a,b):print(c)
    a0 + a1 + a2 - b >= 0
    3 b - a0 - a1 - a2 >= 0
    ```

- `ForwardDiff_Branch(a, V_out)`

  - Input: the input bit a, and a list of variables V_out which contains the branches of a

  - Output: a list of constraints describing how the forward differential propagate against the branch operation

  - Example:V_out

    ```python
    >>>a = 'a'
    >>>b = ['b0', 'b1', 'b2']
    >>>for c in MITMConstraints.ForwardDiff_Branch(a,b):print(c)
    a - b0 = 0
    a - b1 = 0
    a - b2 = 0
    ```

- Then we have the methods `BackwardDet_LinearLayer`, `BackwardDet_XOR`, and `BackwardDet_Branch` for describing the backward determination for all the above operations.

- `relationXYZ(x, y, z)`

- - Input: the lists of X-type, Y-type and Z-type variables

  - Output: a list of constraints such that z[i] = 1 if and only if x[i] = y[i] = 1

  - Example:

    ```python
    >>> a = ['a0', 'a1', 'a2', 'a3']
    >>> b = ['b0', 'b1', 'b2', 'b3']
    >>> c = ['c0', 'c1', 'c2', 'c3']
    >>> MITMConstraints.relationXYZ(a, b, c)
    ['a0 - c0 >= 0',
     'b0 - c0 >= 0',
     'c0 - a0 - b0 >= -1',
     'a1 - c1 >= 0',
     'b1 - c1 >= 0',
     'c1 - a1 - b1 >= -1',
     'a2 - c2 >= 0',
     'b2 - c2 >= 0',
     'c2 - a2 - b2 >= -1',
     'a3 - c3 >= 0',
     'b3 - c3 >= 0',
     'c3 - a3 - b3 >= -1']
    ```



## A Toy Example

Here by we give an example of how to use `CPMITM.py` to analyze a toy cipher. The block size of the toy cipher is 32-bit (4-byte). The round function consists of AddRoundKey, a layer of 4 8-bit S-boxes, and the linear transformation MC, where 4 bytes (x_0, x_1, x_2, x_3) are transformed to (x_1 + x_2 + x_3, x_0 + x_2 + x_3, x_0 + x_1 + x_3, x_0 + x_1 + x_2).

First, let import `CPMITM.py`, define some cipher specific parameters, and derive a  new class from the abstract base class `Cipher`.

```python
from CPMITM import *

MC = [[0,1,1,1], [1,0,1,1], [1,1,0,1], [1,1,1,0]]
inv_MC = MC

class MITM_Toy(Cipher):
    pass
```

Then, we shoud be clear wich variables matters. Since the input and output variables of S-box are always equal, we only need to care about the input variables of the S-box layer and the input variables of the MC for each round.

```python
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
```

Note that the cipher is divided into three parts: E_0, E_1, E_2, where E_1 is the distinguisher part and E_0 and E_2 are the outter rounds from which some secret-key info is extracted by the attack. The tag `_r_minus` indicates round in E_0.

Therefore, if we target a cipher with 1-round E_0, 3-round E_1 and 2-round E_2, the following lists of variables are considered.

```python
['S_0_r_minus2', 'S_1_r_minus2', 'S_2_r_minus2', 'S_3_r_minus2'] # <-- input to E_0
['V_0_r_minus2', 'V_1_r_minus2', 'V_2_r_minus2', 'V_3_r_minus2']
['S_0_r_minus1', 'S_1_r_minus1', 'S_2_r_minus1', 'S_3_r_minus1']
['V_0_r_minus1', 'V_1_r_minus1', 'V_2_r_minus1', 'V_3_r_minus1']
['S_0_r0', 'S_1_r0', 'S_2_r0', 'S_3_r0']  # <-- Output of E_0 and input to E_1
['V_0_r0', 'V_1_r0', 'V_2_r0', 'V_3_r0']
...
['S_0_r2', 'S_1_r2', 'S_2_r2', 'S_3_r2']
['V_0_r2', 'V_1_r2', 'V_2_r2', 'V_3_r2']
['S_0_r3', 'S_1_r3', 'S_2_r3', 'S_3_r3']  # <-- Output of E_1 and input to E_2
['V_0_r3', 'V_1_r3', 'V_2_r3', 'V_3_r3']
['S_0_r4', 'S_1_r4', 'S_2_r4', 'S_3_r4']  # <-- Output of E_2
```

For the sake of simplicity, we start with showing how to model each round the distinguisher part.

```python
def genConstraints_of_Round(self, r):
        # 1. generate constraints of foward differential of the S-box layer and MC (X-type vars)
        # 2. generate constraints of backward determination of the S-box layer and MC (Y-type vars)
        # 3. generate constraints of the relationship of type X and type Y vars (Z-type vars)
```

Next, we prepare the objective function `genObjectiveFun_to_Round()` and add additional constraints `genConstraints_Additional()` to rule out trival and invalid solutions. We are now ready to generate a model whose feasible solutions constitute the set of all DS-MITM distinguishers.

```python
from MITMToy import *

# Name = "Toy", Wordsize = 8-bit, Blocksize = 32-bit, 
# R = 3,  word_keysize = 8, keysize = 128
Toy = MITM_Toy("Toy", 8, 32, 3, 8, 128) 
Toy.genModel(".\Solution\Toy_r3.lp", 3)
```

Note that `genModel()` only consider the distinguisher part. Hence the number of round is 3. After Toy_r3.lp is generated,
it can be solved by Gurobi. Let us move on to the model of the key-recovery part. 

First we consider the backward differential of E_0

```python
def genConstraints_backwardkeyrecovery(self, r): #backward differential, r < 0
        assert r < 0
        _X = BasicTools.typeX

        Input_round = self.genVars_input_of_round(r)
        Input_MC = self.genVars_input_of_MixColumn(r)
        Output_round = self.genVars_input_of_round(r+1)

        Constr = []
        
        Constr = Constr + MITMConstraints.ForwardDiff_LinearLayer(inv_MC, _X(Output_round), _X(Input_MC))
        Constr = Constr + MITMConstraints.equalConstraints(_X(Input_round), _X(Input_MC))

        return Constr
```

Note that the variables involved in E_0 should contain Type-X and Type-M variables, but when coding we only use Type-X variables since they can be distinguished by their round numbers. In this way we can ommit the constraints for the Type-X and Type-M variables for the input state of E_1 (they should be equal).

Next we need to know which words of the internal states of E_0 should be involved to construct the \delta set input to E_1.

```python
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
```

Similarly, models for E_2 are produced by `genConstraints_forwardkeyrecovery()`, and `genConstraints_GuessedKey_forwardkeyrecovery()`. All these information should be converted to the knowledge of what subkey words should be guessed

```python
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
```

After adding some additional constraints which, for example, limit the data complexity of the attack and preparing the objective function (e.g., minimize the number of subkey words guessed), we can generated the model of key recovery attack

```python
Toy.genModel_keyrecovery(".\Solution\Toy_r1_r3_r2.lp", 1, 2)
```

We the naming convention of the file name `r1_r3_r2` indicates that we are targeting a cipher E with 1-round E_0, 3-round E_0, and 2-round E_2. We solve `Toy_r1_r3_r2.lp` and the solution is written into `Toy_r1_r3_r2.sol`, which which we can produce the figures describing the distinguisher and the attack based on a Latex template of the diagram of the cipher

```python
FigDisginguisher = DrawDistinguisher(".\Solution\Toy_r1_r3_r2.sol", 3)
FigDisginguisher.draw(".\Figure\Distinguisher_Toy.tex")

FigKeyrecovery = DrawKeyrecovery(".\Solution\Toy_r1_r3_r2.sol", 3, 1, 2)
FigKeyrecovery.draw(".\Figure\Kerecovery_Toy.tex")

```

# DS-MITM Attack on TWINE

The `MITMTWINE.py` contains the class `MITM_TWINE` for generating the MILP models of TWINE. Before we look into the details of `MITMWINE`, let us see how to use it with the script `cmd_TW.py`. Firstly, we import the required scripts and build the class instance

```python
from MITMTWINE import *
from CPMITM import *

TW80 = MITM_TWINE("TW", 4, 64, 11, 4, 80)
```

If we are only interested in the distinguisher, we can generate the model as follows

```python
TW80.genModel("./Solution/TW80_r11.lp", 11)
```

Then the set of feasible solutions of `./Solution/TW80_r11.lp` corresponds to all 11-round DS-MITM distinguishers of TWINE80. To build a model involving the key-recovery part, we call the function `genModel_keyrecovery`

```python
TW80.genModel_keyrecovery("./Solution/TW80_r4_r11_r5.lp", 4, 5, 18)
```

We can find all solutions with the SCIP solver whose output is stored in `./Solution/All_TW80_r4_r11_r5.txt`. Then we convert it to the `*.sol` format of Gurobi

```python
BasicTools.SCIP2Sol("./Solution/All_TW80_r4_r11_r5.txt","./Solution/TW80_r4_r11_r5_")
```

Finally, we can draw the figures illustrating the distinguishers and attacks according to the solution files.  *The readers may ignore this part since it makes the code complicated*.

```python
from TwineDistinguisherDrawer import *
from TwineKeyrecoveryDrawer import *
from TwineKeyscheduleDrawer import *

FigDistinguisher = DrawDistinguisher("./Solution/TW80_r4_r11_r5_2.sol", 11)
FigDistinguisher.draw("./Figure/Distinguisher_TW80.tex")

FigKeyrecovery = DrawKeyrecovery("./Solution/TW80_r4_r11_r5_2.sol", 11, 4, 5)
FigKeyrecovery.draw("./Figure/Keyrecovery_TW80.tex")
FigKeyrecovery.drawGuessedValue("./Figure/GuessedValue_TW80.tex")

FigKeyschedule = DrawKeyschedule("./Solution/TW80_r4_r11_r5_2.sol", 11, 4, 5, 18, 20)
FigKeyschedule.draw("./Figure/Keyschedule_TW80.tex")
```



## Let us see how `MITMTWINE.py` works

First we define a new class `MITM_TWINE` by extending the abstract base class `Cipher` in `CPMITM.py`, and specify the state variables we care about. Note that variables with `_r_minus_` tag are used for rounds appended before the distinguisher.

```python
def genVars_input(self, r):
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
```

Then we define the method `genConstraints_of_Round(self, r)` for generating all constraints for a single round of the distinguisher part.  

```python
def genConstraints_of_Round(self, r):
    # 1. generate constraints for all Type-X variables: forward differential 
    # 2. generate constraints for all Type-Y variables: backward determination
    # 3. generate constraints for all Type-Z variables: z = 1 if and only if x = y = 1
```

Then after define additional constraints and the objective function in `genConstraints_Additional()` and `genObjectiveFun_to_Round()`, we are ready to call the `genModel()` method defined in the abstract base class to produce MILP models of the distinguisher part. Basically, in the derived class, we only need to specify the variables and constraints. Then abstract base class will know how to use this knowledge to produce the model for the distinguisher part. If we also need to model the key-recovery part, more work is required.

Basically, we need to define the methods for generating the constraints of the Type-M variables defined in $E_0$ (backward differential),  and the Type-W variables defined in $E_2$ 

```python
def genConstraints_backwardkeyrecovery(self, r):
    pass

def genConstraints_forwardkeyrecovery(self, r):
    pass
```

Next, we identify the information that should be guessed in our attack

```python
def genConstraints_guessedValue_backwardkeyrecovery(self, r):
    pass
    
def genConstraints_guessedValue_forwardkeyrecovery(self, r):
    pass
```

Subsequently, all such guessed information should be converted to subkey info

```python
def genConstraints_guessedValue_forwardkeyrecovery(self, r):
    pass

def genVars_subkey(self, r):
    pass

def genConstraints_guessedkey_IS(self, backwardRounds, forwardRounds):
    pass

def genConstraints_keyschedule(self, backwardRounds, forwardRounds, MR):
    pass
```

Finally, after introducing additional constraints and the objective function, we define in `genModel_keyrecovery()` how to generate the key-recovery model. Note that , in contrast to the distinguisher part, we do not provide a `genModel_keyrecovery()` method in the abstract base class, since the key-recovery process is more complicated and ad-hoc. We rely on the user to control the logic to generate the model.

# Remarks

From the above examples, we can see that modelling the DS-MITM attack against different ciphers with general constraint programming follows a fairly similar approach. However, we should emphasize that the DS-MITM attack cannot be automated completely. For example, the key-recover part is too flexible to be encoded into an abstract base class, and in many situations we may add cipher specific constraints which are derived from manual analysis (like the case of SKINNY and AES). Therefore, such tool should be regarded as an asistant tool for crypanalysts.









