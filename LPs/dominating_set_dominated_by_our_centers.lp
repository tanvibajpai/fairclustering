\ Model Dominating_Set
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
 
Subject To
 R0: y_0 + y_1 + y_2 + y_3 + y_4 + y_5 + y_6 + y_7 <= 5
 C_0: y_0 + y_1 + y_7 >= 1
 C_1: y_0 + y_1 + y_2 >= 1
 C_2: y_1 + y_2 + y_3 >= 1
 C_3: y_2 + y_3 + y_4 >= 1
 C_4: y_3 + y_4 + y_5 >= 1
 C_5: y_4 + y_5 + y_6 >= 1
 C_6: y_5 + y_6 + y_7 >= 1
 C_7: y_0 + y_6 + y_7 >= 1
 R9: y_3 = 0
 R10: y_4 = 0
 R11: y_5 = 0
 R12: y_6 = 0
 R13: y_7 = 0
Bounds
Binaries
 y_0 y_1 y_2 y_3 y_4 y_5 y_6 y_7
End
