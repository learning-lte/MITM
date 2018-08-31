from MITMAES import *



###added constraint with data complexity is less than 2^8
##AES = MITM_AES("AES", 8, 128, 4, 8,128)
##AES.genModel_keyrecovery(".\Solution\AES128_r0_r4_r2.lp", 0, 2)





#added constraints that the bound of the distinguisher is added by 16
AES = MITM_AES("AES", 8, 128, 4, 8,128)
AES.genModel_keyrecovery(".\Solution\AES128_r1_r4_r2.lp", 1, 2)

AES = MITM_AES("AES192", 8, 128, 4, 8,192)
AES.genModel_keyrecovery(".\Solution\AES192_r1_r4_r3.lp", 1, 3)


AES = MITM_AES("AES", 8, 128, 5, 8,256)
AES.genModel_keyrecovery(".\Solution\AES256_r1_r5_r3.lp", 1, 3) 




from AESDistinguisherDrawer import *
from AESKeyrecoveryDrawer import *

FigDistinguisher = DrawDistinguisher(".\Solution\AES128_r0_r4_r2.sol", 4)
FigDistinguisher.draw(".\Figure\Distinguisher_AES128_r0_r4_r2.tex")

FigKeyrecovery = DrawKeyrecovery(".\Solution\AES128_r0_r4_r2.sol", 4, 0, 2)
FigKeyrecovery.draw(".\Figure\Keyrecovery_AES128_r0_r4_r2.tex")
FigKeyrecovery.drawGuessedValue(".\Figure\GuessedValue_AES128_r0_r4_r2.tex")



FigDistinguisher = DrawDistinguisher(".\Solution\AES128_r1_r4_r2.sol", 4)
FigDistinguisher.draw(".\Figure\Distinguisher_AES128_r1_r4_r2.tex")

FigKeyrecovery = DrawKeyrecovery(".\Solution\AES128_r1_r4_r2.sol", 4, 1, 2)
FigKeyrecovery.draw(".\Figure\Keyrecovery_AES128_r1_r4_r2.tex")
FigKeyrecovery.drawGuessedValue(".\Figure\GuessedValue_AES128_r1_r4_r2.tex")

FigDistinguisher = DrawDistinguisher(".\Solution\AES192_r1_r4_r3.sol", 4)
FigDistinguisher.draw(".\Figure\Distinguisher_AES192_r1_r4_r3.tex")

FigKeyrecovery = DrawKeyrecovery(".\Solution\AES192_r1_r4_r3.sol", 4, 1, 3)
FigKeyrecovery.draw(".\Figure\Keyrecovery_AES192_r1_r4_r3.tex")
FigKeyrecovery.drawGuessedValue(".\Figure\GuessedValue_AES192_r1_r4_r3.tex")


FigDistinguisher = DrawDistinguisher(".\Solution\AES256_r1_r5_r3.sol", 5)
FigDistinguisher.draw(".\Figure\Distinguisher_AES256_r1_r5_r3.tex")

FigKeyrecovery = DrawKeyrecovery(".\Solution\AES256_r1_r5_r3.sol", 5, 1, 3)
FigKeyrecovery.draw(".\Figure\Keyrecovery_AES256_r1_r5_r3.tex")
FigKeyrecovery.drawGuessedValue(".\Figure\GuessedValue_AES256_r1_r5_r3.tex")
