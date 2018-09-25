\ Model Dominating_Set
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
 
Subject To
 R0: y_0 + y_1 + y_2 + y_3 + y_4 + y_5 <= 2
 C_0: y_0 + y_1 + y_5 >= 1
 C_1: y_0 + y_1 + y_2 >= 1
 C_2: y_1 + y_2 + y_3 >= 1
 C_3: y_2 + y_3 + y_4 >= 1
 C_4: y_3 + y_4 + y_5 >= 1
 C_5: y_0 + y_4 + y_5 >= 1
Bounds
Binaries
 y_0 y_1 y_2 y_3 y_4 y_5
End
