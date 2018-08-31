from MITMLBlock import *




LB = MITM_Lblock("LB", 4, 64, 11,4,80)
LB.genModel_keyrecovery(".\Solution\LB_r5_r11_r5.lp", 5, 5, 2)
LB.genModel(".\Solution\LB_r11.lp", 11)



from LblockDistinguisherDrawer import *
from LblockKeyrecoveryDrawer import *
from LblockKeyscheduleDrawer import *
FigDistinguisher = DrawDistinguisher(".\Solution\LB_r5_r11_r5.sol", 11)
FigDistinguisher.draw(".\Figure\Distinguisher_LB.tex")

FigKeyrecovery = DrawKeyrecovery(".\Solution\LB_r5_r11_r5.sol", 11, 5, 5)
FigKeyrecovery.draw(".\Figure\Keyrecovey_LB.tex")
FigKeyrecovery.drawGuessedValue(".\Figure\GuessedValue_LB.tex")

FigKeyschedule = DrawKeyschedule(".\Solution\LB_r5_r11_r5.sol", 11, 5, 5, 2)
FigKeyschedule.draw(".\Figure\Keyschedule_LB.tex")

