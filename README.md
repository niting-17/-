## 題目
1.實作 Patrick Method，程式語言種類不限，程式碼須包含註解。   
2.實現 single output problem 以及 multiple output problem。   
3.系統輸入：所有的PI，如為 multiple output problem 則須包含可能的  shared terms。  
4.系統輸出：所有的 minimum SOP。 

## 主要邏輯流程
1. 系統輸入： 程式首先引導使用者逐一輸入每個函數的最小項，並支援多
個函數輸入。接著，使用者需輸入所有函數共用的共享項，這些共享項
會被賦予獨一無二的全域 PI 編號。最後，針對每個函數，程式會引導
使用者輸入其獨有的非共享質詢項，並同樣賦予全域 PI 編號。 
2. Petrick's Method 演算法：  
o 最小項覆蓋分析： 程式會為每個函數的每一個最小項，尋找能夠
覆蓋它的所有質詢項 (包含共享項和該函數獨有的 PI) 。這些能
覆蓋特定最小項的 PI 會被儲存在一個列表中，形成該最小項的
覆蓋選項組。 
o 建立 P-function： 對於每個函數，其所有的最小項覆蓋選項組
會被轉換為邏輯表示式。在每個覆蓋選項組內部，PI 之間是邏輯 
OR 關係。而所有最小項的這些 OR 子句之間，則以邏輯 AND 
關係連接起來，形成積之和 (POS) 形式的 P-function 。 
3. 計算並找出minimum solution：  
轉換為 SOP： 利用 SymPy 模組的 to_dnf 函數，將 POS 形式
的 P-function 透過分配律展開並化簡為 SOP 形式。 
多重輸出： 對於多重輸出問題，由於「整體最優解不一定是單一
最優解」，程式會使用 itertools.product 計算所有函數 SOP 解
的笛卡兒積，以窮舉所有可能的解組合 。 
成本計算與篩選： 對於每一個可能的解組合，程式會計算其總成
本，即該組合中所有函數解所使用的不重複 PI 的數量 。最終，
程式將選出成本最低的一個或多個解組合作為最終的解，並將 
SymPy 的 & 符號替換為 + 符號提高可讀性。

[程式執行檔](https://drive.google.com/file/d/1bWzEWKxL2QwkTbq2naDkin0ngDuh8Cny/view?usp=sharing)
