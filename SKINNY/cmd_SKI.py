from MITMSKINNY import *
from Count_guessedKey import *



SKI = MITM_SKINNY("SKINNY", 8, 128, 10, 8, 384)
SKI.genModel(".\Solution\SKI_r10.lp", 10)
#find all solutions with added constraints that the bound of the distinguisher equals 40
SKI.genModel_keyrecovery(".\Solution\SKI_r3_r10_r9.lp", 3, 9)


BasicTools.SCIP2Sol(".\Solution\All_SKI_r3_r10_r9.txt",".\Solution\SKI_r3_r10_r9_")

from SkinnyDistinguisherDrawer import *
from SkinnyKeyrecoveryDrawer import *
from SkinnyKeyscheduleDrawer import *

FigDisginguisher = DrawDistinguisher(".\Solution\SKI_r3_r10_r9.sol", 10)
FigDisginguisher.draw(".\Figure\Distinguisher_SKI.tex")

FigKeyrecovery = DrawKeyrecovery(".\Solution\SKI_r3_r10_r9.sol", 10, 3, 9)
FigKeyrecovery.draw(".\Figure\Kerecovery_SKI.tex")
FigKeyrecovery.drawGuessedValue(".\Figure\GuessedValue_SKI.tex")

FigKeyschedule = DrawKeyschedule(".\Solution\SKI_r3_r10_r9.sol", 10, 3,9)
FigKeyschedule.draw(".\Figure\Keyschedule_SKI.tex")

Num_GuessedKey = Count_guessedkey(".\Solution\SKI_r3_r10_r9.sol", 10, 3, 9)
print(Num_GuessedKey .Count()[1])

