from MITMToy import *




Toy = MITM_Toy("Toy", 8, 32, 3, 8, 128)
Toy.genModel(".\Solution\Toy_r3.lp", 3)
Toy.genModel_keyrecovery(".\Solution\Toy_r1_r3_r2.lp", 1, 2)


from ToyDistinguisherDrawer import *
from ToyKeyrecoveryDrawer import *


FigDisginguisher = DrawDistinguisher(".\Solution\Toy_r1_r3_r2.sol", 3)
FigDisginguisher.draw(".\Figure\Distinguisher_Toy.tex")

FigKeyrecovery = DrawKeyrecovery(".\Solution\Toy_r1_r3_r2.sol", 3, 1, 2)
FigKeyrecovery.draw(".\Figure\Kerecovery_Toy.tex")


