Minimize
S_0_r1_TypeZ + S_1_r1_TypeZ + S_2_r1_TypeZ + S_3_r1_TypeZ + S_0_r2_TypeZ + S_1_r2_TypeZ + S_2_r2_TypeZ + S_3_r2_TypeZ


Subject To
S_0_r0_TypeX - V_0_r0_TypeX = 0
S_1_r0_TypeX - V_1_r0_TypeX = 0
S_2_r0_TypeX - V_2_r0_TypeX = 0
S_3_r0_TypeX - V_3_r0_TypeX = 0
3 S_0_r1_TypeX -  V_1_r0_TypeX - V_2_r0_TypeX - V_3_r0_TypeX >= 0
V_1_r0_TypeX + V_2_r0_TypeX + V_3_r0_TypeX - S_0_r1_TypeX >= 0
3 S_1_r1_TypeX -  V_0_r0_TypeX - V_2_r0_TypeX - V_3_r0_TypeX >= 0
V_0_r0_TypeX + V_2_r0_TypeX + V_3_r0_TypeX - S_1_r1_TypeX >= 0
3 S_2_r1_TypeX -  V_0_r0_TypeX - V_1_r0_TypeX - V_3_r0_TypeX >= 0
V_0_r0_TypeX + V_1_r0_TypeX + V_3_r0_TypeX - S_2_r1_TypeX >= 0
3 S_3_r1_TypeX -  V_0_r0_TypeX - V_1_r0_TypeX - V_2_r0_TypeX >= 0
V_0_r0_TypeX + V_1_r0_TypeX + V_2_r0_TypeX - S_3_r1_TypeX >= 0
S_0_r0_TypeY - V_0_r0_TypeY = 0
S_1_r0_TypeY - V_1_r0_TypeY = 0
S_2_r0_TypeY - V_2_r0_TypeY = 0
S_3_r0_TypeY - V_3_r0_TypeY = 0
3 V_0_r0_TypeY -  S_1_r1_TypeY - S_2_r1_TypeY - S_3_r1_TypeY >= 0
S_1_r1_TypeY + S_2_r1_TypeY + S_3_r1_TypeY - V_0_r0_TypeY >= 0
3 V_1_r0_TypeY -  S_0_r1_TypeY - S_2_r1_TypeY - S_3_r1_TypeY >= 0
S_0_r1_TypeY + S_2_r1_TypeY + S_3_r1_TypeY - V_1_r0_TypeY >= 0
3 V_2_r0_TypeY -  S_0_r1_TypeY - S_1_r1_TypeY - S_3_r1_TypeY >= 0
S_0_r1_TypeY + S_1_r1_TypeY + S_3_r1_TypeY - V_2_r0_TypeY >= 0
3 V_3_r0_TypeY -  S_0_r1_TypeY - S_1_r1_TypeY - S_2_r1_TypeY >= 0
S_0_r1_TypeY + S_1_r1_TypeY + S_2_r1_TypeY - V_3_r0_TypeY >= 0
S_0_r0_TypeX - S_0_r0_TypeZ >= 0
S_0_r0_TypeY - S_0_r0_TypeZ >= 0
S_0_r0_TypeZ - S_0_r0_TypeX - S_0_r0_TypeY >= -1
S_1_r0_TypeX - S_1_r0_TypeZ >= 0
S_1_r0_TypeY - S_1_r0_TypeZ >= 0
S_1_r0_TypeZ - S_1_r0_TypeX - S_1_r0_TypeY >= -1
S_2_r0_TypeX - S_2_r0_TypeZ >= 0
S_2_r0_TypeY - S_2_r0_TypeZ >= 0
S_2_r0_TypeZ - S_2_r0_TypeX - S_2_r0_TypeY >= -1
S_3_r0_TypeX - S_3_r0_TypeZ >= 0
S_3_r0_TypeY - S_3_r0_TypeZ >= 0
S_3_r0_TypeZ - S_3_r0_TypeX - S_3_r0_TypeY >= -1
V_0_r0_TypeX - V_0_r0_TypeZ >= 0
V_0_r0_TypeY - V_0_r0_TypeZ >= 0
V_0_r0_TypeZ - V_0_r0_TypeX - V_0_r0_TypeY >= -1
V_1_r0_TypeX - V_1_r0_TypeZ >= 0
V_1_r0_TypeY - V_1_r0_TypeZ >= 0
V_1_r0_TypeZ - V_1_r0_TypeX - V_1_r0_TypeY >= -1
V_2_r0_TypeX - V_2_r0_TypeZ >= 0
V_2_r0_TypeY - V_2_r0_TypeZ >= 0
V_2_r0_TypeZ - V_2_r0_TypeX - V_2_r0_TypeY >= -1
V_3_r0_TypeX - V_3_r0_TypeZ >= 0
V_3_r0_TypeY - V_3_r0_TypeZ >= 0
V_3_r0_TypeZ - V_3_r0_TypeX - V_3_r0_TypeY >= -1
S_0_r1_TypeX - V_0_r1_TypeX = 0
S_1_r1_TypeX - V_1_r1_TypeX = 0
S_2_r1_TypeX - V_2_r1_TypeX = 0
S_3_r1_TypeX - V_3_r1_TypeX = 0
3 S_0_r2_TypeX -  V_1_r1_TypeX - V_2_r1_TypeX - V_3_r1_TypeX >= 0
V_1_r1_TypeX + V_2_r1_TypeX + V_3_r1_TypeX - S_0_r2_TypeX >= 0
3 S_1_r2_TypeX -  V_0_r1_TypeX - V_2_r1_TypeX - V_3_r1_TypeX >= 0
V_0_r1_TypeX + V_2_r1_TypeX + V_3_r1_TypeX - S_1_r2_TypeX >= 0
3 S_2_r2_TypeX -  V_0_r1_TypeX - V_1_r1_TypeX - V_3_r1_TypeX >= 0
V_0_r1_TypeX + V_1_r1_TypeX + V_3_r1_TypeX - S_2_r2_TypeX >= 0
3 S_3_r2_TypeX -  V_0_r1_TypeX - V_1_r1_TypeX - V_2_r1_TypeX >= 0
V_0_r1_TypeX + V_1_r1_TypeX + V_2_r1_TypeX - S_3_r2_TypeX >= 0
S_0_r1_TypeY - V_0_r1_TypeY = 0
S_1_r1_TypeY - V_1_r1_TypeY = 0
S_2_r1_TypeY - V_2_r1_TypeY = 0
S_3_r1_TypeY - V_3_r1_TypeY = 0
3 V_0_r1_TypeY -  S_1_r2_TypeY - S_2_r2_TypeY - S_3_r2_TypeY >= 0
S_1_r2_TypeY + S_2_r2_TypeY + S_3_r2_TypeY - V_0_r1_TypeY >= 0
3 V_1_r1_TypeY -  S_0_r2_TypeY - S_2_r2_TypeY - S_3_r2_TypeY >= 0
S_0_r2_TypeY + S_2_r2_TypeY + S_3_r2_TypeY - V_1_r1_TypeY >= 0
3 V_2_r1_TypeY -  S_0_r2_TypeY - S_1_r2_TypeY - S_3_r2_TypeY >= 0
S_0_r2_TypeY + S_1_r2_TypeY + S_3_r2_TypeY - V_2_r1_TypeY >= 0
3 V_3_r1_TypeY -  S_0_r2_TypeY - S_1_r2_TypeY - S_2_r2_TypeY >= 0
S_0_r2_TypeY + S_1_r2_TypeY + S_2_r2_TypeY - V_3_r1_TypeY >= 0
S_0_r1_TypeX - S_0_r1_TypeZ >= 0
S_0_r1_TypeY - S_0_r1_TypeZ >= 0
S_0_r1_TypeZ - S_0_r1_TypeX - S_0_r1_TypeY >= -1
S_1_r1_TypeX - S_1_r1_TypeZ >= 0
S_1_r1_TypeY - S_1_r1_TypeZ >= 0
S_1_r1_TypeZ - S_1_r1_TypeX - S_1_r1_TypeY >= -1
S_2_r1_TypeX - S_2_r1_TypeZ >= 0
S_2_r1_TypeY - S_2_r1_TypeZ >= 0
S_2_r1_TypeZ - S_2_r1_TypeX - S_2_r1_TypeY >= -1
S_3_r1_TypeX - S_3_r1_TypeZ >= 0
S_3_r1_TypeY - S_3_r1_TypeZ >= 0
S_3_r1_TypeZ - S_3_r1_TypeX - S_3_r1_TypeY >= -1
V_0_r1_TypeX - V_0_r1_TypeZ >= 0
V_0_r1_TypeY - V_0_r1_TypeZ >= 0
V_0_r1_TypeZ - V_0_r1_TypeX - V_0_r1_TypeY >= -1
V_1_r1_TypeX - V_1_r1_TypeZ >= 0
V_1_r1_TypeY - V_1_r1_TypeZ >= 0
V_1_r1_TypeZ - V_1_r1_TypeX - V_1_r1_TypeY >= -1
V_2_r1_TypeX - V_2_r1_TypeZ >= 0
V_2_r1_TypeY - V_2_r1_TypeZ >= 0
V_2_r1_TypeZ - V_2_r1_TypeX - V_2_r1_TypeY >= -1
V_3_r1_TypeX - V_3_r1_TypeZ >= 0
V_3_r1_TypeY - V_3_r1_TypeZ >= 0
V_3_r1_TypeZ - V_3_r1_TypeX - V_3_r1_TypeY >= -1
S_0_r2_TypeX - V_0_r2_TypeX = 0
S_1_r2_TypeX - V_1_r2_TypeX = 0
S_2_r2_TypeX - V_2_r2_TypeX = 0
S_3_r2_TypeX - V_3_r2_TypeX = 0
3 S_0_r3_TypeX -  V_1_r2_TypeX - V_2_r2_TypeX - V_3_r2_TypeX >= 0
V_1_r2_TypeX + V_2_r2_TypeX + V_3_r2_TypeX - S_0_r3_TypeX >= 0
3 S_1_r3_TypeX -  V_0_r2_TypeX - V_2_r2_TypeX - V_3_r2_TypeX >= 0
V_0_r2_TypeX + V_2_r2_TypeX + V_3_r2_TypeX - S_1_r3_TypeX >= 0
3 S_2_r3_TypeX -  V_0_r2_TypeX - V_1_r2_TypeX - V_3_r2_TypeX >= 0
V_0_r2_TypeX + V_1_r2_TypeX + V_3_r2_TypeX - S_2_r3_TypeX >= 0
3 S_3_r3_TypeX -  V_0_r2_TypeX - V_1_r2_TypeX - V_2_r2_TypeX >= 0
V_0_r2_TypeX + V_1_r2_TypeX + V_2_r2_TypeX - S_3_r3_TypeX >= 0
S_0_r2_TypeY - V_0_r2_TypeY = 0
S_1_r2_TypeY - V_1_r2_TypeY = 0
S_2_r2_TypeY - V_2_r2_TypeY = 0
S_3_r2_TypeY - V_3_r2_TypeY = 0
3 V_0_r2_TypeY -  S_1_r3_TypeY - S_2_r3_TypeY - S_3_r3_TypeY >= 0
S_1_r3_TypeY + S_2_r3_TypeY + S_3_r3_TypeY - V_0_r2_TypeY >= 0
3 V_1_r2_TypeY -  S_0_r3_TypeY - S_2_r3_TypeY - S_3_r3_TypeY >= 0
S_0_r3_TypeY + S_2_r3_TypeY + S_3_r3_TypeY - V_1_r2_TypeY >= 0
3 V_2_r2_TypeY -  S_0_r3_TypeY - S_1_r3_TypeY - S_3_r3_TypeY >= 0
S_0_r3_TypeY + S_1_r3_TypeY + S_3_r3_TypeY - V_2_r2_TypeY >= 0
3 V_3_r2_TypeY -  S_0_r3_TypeY - S_1_r3_TypeY - S_2_r3_TypeY >= 0
S_0_r3_TypeY + S_1_r3_TypeY + S_2_r3_TypeY - V_3_r2_TypeY >= 0
S_0_r2_TypeX - S_0_r2_TypeZ >= 0
S_0_r2_TypeY - S_0_r2_TypeZ >= 0
S_0_r2_TypeZ - S_0_r2_TypeX - S_0_r2_TypeY >= -1
S_1_r2_TypeX - S_1_r2_TypeZ >= 0
S_1_r2_TypeY - S_1_r2_TypeZ >= 0
S_1_r2_TypeZ - S_1_r2_TypeX - S_1_r2_TypeY >= -1
S_2_r2_TypeX - S_2_r2_TypeZ >= 0
S_2_r2_TypeY - S_2_r2_TypeZ >= 0
S_2_r2_TypeZ - S_2_r2_TypeX - S_2_r2_TypeY >= -1
S_3_r2_TypeX - S_3_r2_TypeZ >= 0
S_3_r2_TypeY - S_3_r2_TypeZ >= 0
S_3_r2_TypeZ - S_3_r2_TypeX - S_3_r2_TypeY >= -1
V_0_r2_TypeX - V_0_r2_TypeZ >= 0
V_0_r2_TypeY - V_0_r2_TypeZ >= 0
V_0_r2_TypeZ - V_0_r2_TypeX - V_0_r2_TypeY >= -1
V_1_r2_TypeX - V_1_r2_TypeZ >= 0
V_1_r2_TypeY - V_1_r2_TypeZ >= 0
V_1_r2_TypeZ - V_1_r2_TypeX - V_1_r2_TypeY >= -1
V_2_r2_TypeX - V_2_r2_TypeZ >= 0
V_2_r2_TypeY - V_2_r2_TypeZ >= 0
V_2_r2_TypeZ - V_2_r2_TypeX - V_2_r2_TypeY >= -1
V_3_r2_TypeX - V_3_r2_TypeZ >= 0
V_3_r2_TypeY - V_3_r2_TypeZ >= 0
V_3_r2_TypeZ - V_3_r2_TypeX - V_3_r2_TypeY >= -1
S_0_r3_TypeX - S_0_r3_TypeZ >= 0
S_0_r3_TypeY - S_0_r3_TypeZ >= 0
S_0_r3_TypeZ - S_0_r3_TypeX - S_0_r3_TypeY >= -1
S_1_r3_TypeX - S_1_r3_TypeZ >= 0
S_1_r3_TypeY - S_1_r3_TypeZ >= 0
S_1_r3_TypeZ - S_1_r3_TypeX - S_1_r3_TypeY >= -1
S_2_r3_TypeX - S_2_r3_TypeZ >= 0
S_2_r3_TypeY - S_2_r3_TypeZ >= 0
S_2_r3_TypeZ - S_2_r3_TypeX - S_2_r3_TypeY >= -1
S_3_r3_TypeX - S_3_r3_TypeZ >= 0
S_3_r3_TypeY - S_3_r3_TypeZ >= 0
S_3_r3_TypeZ - S_3_r3_TypeX - S_3_r3_TypeY >= -1
S_0_r0_TypeX + S_1_r0_TypeX + S_2_r0_TypeX + S_3_r0_TypeX >= 1
S_0_r3_TypeY + S_1_r3_TypeY + S_2_r3_TypeY + S_3_r3_TypeY >= 1 
S_0_r1_TypeZ + S_1_r1_TypeZ + S_2_r1_TypeZ + S_3_r1_TypeZ + S_0_r2_TypeZ + S_1_r2_TypeZ + S_2_r2_TypeZ + S_3_r2_TypeZ <= 15


Binary
S_1_r2_TypeX
S_0_r3_TypeX
V_3_r1_TypeX
V_0_r2_TypeZ
V_2_r2_TypeX
V_2_r2_TypeY
S_2_r2_TypeZ
S_0_r3_TypeZ
S_3_r3_TypeZ
S_3_r2_TypeY
S_0_r0_TypeZ
V_2_r1_TypeX
S_0_r0_TypeX
S_1_r3_TypeZ
S_2_r2_TypeX
S_2_r2_TypeY
S_0_r0_TypeY
V_2_r1_TypeY
S_3_r1_TypeZ
S_3_r3_TypeX
S_2_r3_TypeZ
S_0_r2_TypeY
V_2_r0_TypeZ
S_1_r2_TypeZ
V_0_r0_TypeZ
V_1_r1_TypeX
V_1_r1_TypeY
V_0_r1_TypeX
S_1_r3_TypeY
S_2_r1_TypeZ
S_1_r0_TypeX
S_1_r0_TypeY
V_0_r2_TypeX
V_2_r1_TypeZ
S_3_r2_TypeX
V_0_r1_TypeY
V_2_r2_TypeZ
V_3_r2_TypeY
S_1_r1_TypeY
S_3_r1_TypeX
S_0_r2_TypeZ
V_2_r0_TypeX
S_3_r0_TypeZ
V_2_r0_TypeY
V_1_r0_TypeX
V_3_r0_TypeY
S_0_r1_TypeY
V_1_r0_TypeZ
S_0_r3_TypeY
V_0_r0_TypeY
V_1_r2_TypeY
S_0_r2_TypeX
V_3_r0_TypeZ
S_1_r3_TypeX
S_0_r1_TypeZ
V_3_r1_TypeZ
V_0_r0_TypeX
S_3_r0_TypeY
S_1_r0_TypeZ
S_1_r1_TypeZ
V_1_r2_TypeZ
S_2_r1_TypeX
S_2_r3_TypeY
S_3_r3_TypeY
V_3_r2_TypeZ
V_0_r2_TypeY
S_2_r1_TypeY
V_1_r2_TypeX
V_1_r0_TypeY
S_1_r1_TypeX
S_2_r0_TypeY
S_3_r1_TypeY
S_3_r0_TypeX
V_0_r1_TypeZ
V_3_r1_TypeY
V_3_r2_TypeX
S_0_r1_TypeX
S_2_r0_TypeZ
S_1_r2_TypeY
V_1_r1_TypeZ
S_2_r3_TypeX
S_3_r2_TypeZ
S_2_r0_TypeX
V_3_r0_TypeX
