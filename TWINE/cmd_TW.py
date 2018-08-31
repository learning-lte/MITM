from MITMTWINE import *
from CPMITM import *




TW80 = MITM_TWINE("TW", 4, 64, 11,4,80)
TW80.genModel(".\Solution\TW80_r11.lp", 11)
TW80.genModel_keyrecovery(".\Solution\TW80_r4_r11_r5.lp", 4, 5, 18)



TW128 = MITM_TWINE("TW", 4, 64, 11,4,128)
TW128.genModel(".\Solution\TW128_r11.lp", 11)
TW128.genModel_keyrecovery(".\Solution\TW128_r5_r11_r9.lp", 5, 9, 6)


BasicTools.SCIP2Sol(".\Solution\All_TW80_r4_r11_r5.txt",".\Solution\TW80_r4_r11_r5_")
BasicTools.SCIP2Sol(".\Solution\All_TW128_r5_r11_r9.txt",".\Solution\TW128_r5_r11_r9_")

from TwineDistinguisherDrawer import *
from TwineKeyrecoveryDrawer import *
from TwineKeyscheduleDrawer import *
FigDistinguisher = DrawDistinguisher(".\Solution\TW80_r4_r11_r5.sol", 11)
FigDistinguisher.draw(".\Figure\Distinguisher_TW80.tex")

FigKeyrecovery = DrawKeyrecovery(".\Solution/TW80_r4_r11_r5.sol", 11, 4, 5)
FigKeyrecovery.draw(".\Figure\Keyrecovery_TW80.tex")
FigKeyrecovery.drawGuessedValue(".\Figure\GuessedValue_TW80.tex")

FigKeyschedule = DrawKeyschedule(".\Solution\TW80_r4_r11_r5.sol", 11, 4, 5, 18, 20)
FigKeyschedule.draw(".\Figure\Keyschedule_TW80.tex")


FigDistinguisher = DrawDistinguisher(".\Solution\TW128_r5_r11_r9.sol", 11)
FigDistinguisher.draw(".\Figure\Distinguisher_TW128.tex")

FigKeyrecovery = DrawKeyrecovery(".\Solution\TW128_r5_r11_r9.sol", 11, 5, 9)
FigKeyrecovery.draw(".\Figure\Keyrecovery_TW128.tex")
FigKeyrecovery.drawGuessedValue(".\Figure\GuessedValue_TW128.tex")

FigKeyschedule = DrawKeyschedule(".\Solution\TW128_r5_r11_r9.sol", 11, 5, 9, 6, 32)
FigKeyschedule.draw(".\Figure\Keyschedule_TW128.tex")


