# 邏輯設計期末專題 - Petrick's method
# 作者: [1130727 姚妮廷]
# 日期: 2025/06/13

# --- 模組匯入 ---
# 從 sympy 函式庫匯入需要的函數：symbols 用於創建符號變數, Or/And 用於邏輯運算, to_dnf 用於轉換為SOP形式
from sympy import symbols, Or, And, to_dnf
# 從 itertools 模組匯入 product 函數，用於計算笛卡兒積，找出所有可能的解組合
from itertools import product

# 系統輸入

# 初始化函數相關變數
function_index = 1  # 用於顯示當前輸入的是第幾個函數 (f1, f2, ...)
minterm_functions = []  # 建立一個空列表，用來儲存使用者輸入的每一個函數的最小項

# 提示使用者開始輸入
print("請逐一輸入每個函數的最小項（以逗號分隔），輸入完成後直接按 Enter 結束。")
# 使用 while 無窮迴圈，讓使用者可以連續輸入多個函數
while True:
    # 接收使用者輸入，並顯示提示訊息，例如 "請輸入 f1 的最小項編號："
    function_input = input(f"請輸入 f{function_index} 的最小項編號：\n")
    # 判斷使用者是否直接按 Enter (輸入空字串)，若是則結束輸入
    if not function_input:
        break  # 跳出迴圈
    # 如果有輸入，使用 split(',') 將字串分割成最小項列表，並加入到 minterm_functions 中
    minterm_functions.append(function_input.split(','))
    # 函數編號加一，為下一次輸入做準備
    function_index += 1

# 初始化質詢項 (Prime Implicant, PI) 相關變數
pi_global_counter = 1  # 全域的 PI 計數器，確保每個 PI (包含共享和非共享) 都有獨一無二的編號
shared_term_count = 0  # 計算共享項的數量
shared_terms = []  # 建立一個空列表，用來儲存所有共享項

# 讓使用者輸入共享項 (Shared Term)
print("\n請輸入所有函數共用的共享項（以逗號分隔），輸入完成後直接按 Enter 結束。")
# 使用 while 無窮迴圈，讓使用者可以連續輸入多個共享項
while True:
    # 接收使用者輸入，並提示是第幾個共享項 P
    shared_term_input = input(f"請輸入共享項 P{pi_global_counter}：")
    # 判斷使用者是否直接按 Enter，若是則結束輸入
    if not shared_term_input:
        break  # 跳出迴圈
    # 將輸入的共享項字串分割成列表，並加入 shared_terms
    shared_terms.append(shared_term_input.split(','))
    # 全域 PI 計數器加一
    pi_global_counter += 1
    # 共享項數量計數器加一
    shared_term_count += 1

# 讓使用者為每個函數輸入其餘的、非共享的質詢項
prime_implicants_dict = {}  # 建立一個空字典，key 是函數名 (f1)，value 是該函數獨有的 PI 列表
all_pis_list = list(shared_terms)  # 建立一個包含所有 PI 的總列表，先將共享項放進去

# 遍歷之前輸入的每個函數，來接收其獨有的 PI
for i, func in enumerate(minterm_functions, 1):
    current_function_pis = []  # 暫存當前這個函數的 PI
    # 提示使用者現在要為哪個函數輸入 PI
    print(f"\n請輸入 f{i} 的質詢項（不含共享項），輸入完成後直接按 Enter 結束。")
    # 使用 while 迴圈連續輸入
    while True:
        # 接收使用者輸入，並提示 PI 的全域編號
        pi_input = input(f"請輸入 f{i} 的下一個質詢項 P{pi_global_counter}（以逗號分隔）：")
        # 判斷使用者是否結束輸入
        if not pi_input:
            break  # 跳出迴圈
        # 將輸入的 PI 字串分割成列表
        pi_input_list = pi_input.split(',')
        # 將這個 PI 列表加入到"當前函數的 PI 列表"中
        current_function_pis.append(pi_input_list)
        # 同時也將這個 PI 加入到"所有 PI 的總列表"中，以方便後續統一定位和索引
        all_pis_list.append(pi_input_list)
        # 全域 PI 計數器加一
        pi_global_counter += 1
    # 將"當前函數的 PI 列表"存入字典，鍵為函數名
    prime_implicants_dict[f"f{i}"] = current_function_pis

# Petrick's method 演算

# 為每個最小項尋找能覆蓋它的所有質詢項 (PI)
minterm_coverage_groups = {}  # 建立空字典，用來儲存每個函數的覆蓋情況
# 遍歷所有已輸入的函數及其最小項
for i, func_minterms in enumerate(minterm_functions, 1):
    function_key = f"f{i}"  # 產生字典鍵，例如 "f1"
    groups_for_function = []  # 建立列表，儲存這個函數中，每個最小項其對應的覆蓋選項
    
    # 根據 PI 的總數量，一次性創建所有需要的符號變數 
    p_symbols = symbols(f'P1:{pi_global_counter}')

    # 遍歷當前函數的每一個最小項
    for minterm in func_minterms:
        covering_pis = []  # 建立列表，用來儲存能覆蓋"這一個"最小項的所有 PI 符號
        # 首先，檢查共享項是否覆蓋此最小項
        for j, shared in enumerate(shared_terms):
            if minterm in shared:  # 如果最小項存在於某個共享項中
                covering_pis.append(p_symbols[j])  # 將對應的 PI 符號加入列表
        
        # 接著，檢查該函數自己獨有的質詢項
        individual_pis = prime_implicants_dict[function_key]  # 從字典中取出此函數的 PI
        for pi in individual_pis:
            if minterm in pi:  # 如果最小項存在於某個 PI 中
                # 在 all_pis_list (所有PI的總列表) 中找到這個 PI 的索引
                pi_index = all_pis_list.index(pi)
                # 根據這個總索引，將對應的 PI 符號加入列表
                covering_pis.append(p_symbols[pi_index])
        
        # 將這個最小項的所有覆蓋選項 (covering_pis) 加入到此函數的總覆蓋列表 (groups_for_function)
        groups_for_function.append(covering_pis)
    # 將整理好的單一函數覆蓋列表存入總字典
    minterm_coverage_groups[function_key] = groups_for_function

# 輸出每個最小項的覆蓋情況，方便檢查
print("\n--- 各函數最小項的覆蓋情況 ---")
for func_name, groups in minterm_coverage_groups.items():
    print(f"{func_name}: {groups}")  # 格式化輸出

# --- 3. 計算並找出最簡解 ---

# 計算每個P-function 並化簡為 SOP 形式
all_sop_solutions = {}  # 建立空字典，儲存每個函數化簡後的解 (SOP形式)
print("\n--- 各函數的P-function化簡結果 (SOP) ---")
# 遍歷每個函數的覆蓋情況
for func_name, groups in minterm_coverage_groups.items():
    # 如果某個函數沒有最小項，則跳過
    if not groups:
        continue
    
    # 對於每個最小項，其所有的覆蓋選項 (PI) 之間是 "OR" 關係
    pos_clauses = [Or(*term_options) for term_options in groups]
    
    # 所有最小項的 "OR" 子句之間是 "AND" 關係，形成 POS (Product of Sums) 形式的佩特里克函數
    petrick_function_pos = And(*pos_clauses)
    
    # 使用 to_dnf (disjunctive normal form) 函數，透過分配律將 POS 形式展開為 SOP (Sum of Products) 形式
    sop_result = to_dnf(petrick_function_pos, simplify=True)
    
    # 輸出化簡結果
    print(f"{func_name} 的解: \n{sop_result}")
    
    # 將 sympy 物件轉換為字串，並用 ' | ' (OR) 分割成列表，儲存到字典中
    all_sop_solutions[func_name] = str(sop_result).split(' | ')

# 透過窮舉所有組合，尋找多函數輸出的總體最簡解
if all_sop_solutions:  # 確保有解才進行下一步
    # 使用 itertools.product 計算所有函數解的笛卡兒積，得到所有可能的解組合
    solution_combinations = list(product(*all_sop_solutions.values()))
    
    # 初始化變數以尋找最低成本解
    min_cost = float('inf')  # 將初始最低成本設為無限大
    best_solution_combos = []  # 建立列表，用來儲存成本最低的一個或多個解組合

    # 遍歷每一個可能的解組合
    for combo in solution_combinations:
        used_pis_set = set()  # 使用集合 (set) 來儲存該組合用到的所有 PI，集合特性可自動處理重複項
        # 遍歷組合中的每一個函數解表達式
        for solution_expression in combo:
            # 將 "P1 & P2" 這樣的字串用 '&' 分割成 PI 列表
            p_terms = [p.strip() for p in solution_expression.split('&')]
            # 使用 update 方法將列表中的所有 PI 加入集合
            used_pis_set.update(p_terms)
        
        # 計算此組合的總成本，即使用到的不重複 PI 的數量
        current_cost = len(used_pis_set)
        
        # 比較成本
        if current_cost < min_cost:  # 如果當前成本更低
            min_cost = current_cost  # 更新最低成本
            best_solution_combos = [combo]  # 重置最佳解列表，只保留當前這一個
        elif current_cost == min_cost: # 如果成本與當前最低相同
            best_solution_combos.append(combo)  # 將此組合也加入最佳解列表

    # 輸出最終結果
    print("\n--- 成本最低的最佳解組合 ---")
    # 輸出最終找到的最低成本值
    print(f"最低成本 (使用的總質詢項數量): {min_cost}")
    # 遍歷所有最佳解組合並輸出
    for i, final_combo in enumerate(best_solution_combos, 1):
        print(f"\n組合 {i}:")  # 輸出組合編號
        # 使用 zip 將函數名和對應的解配對起來
        for func_name, expression in zip(all_sop_solutions.keys(), final_combo):
            # 將 sympy 邏輯運算的 '&' 符號替換成電路設計中更常用的 '+'，使其更易讀
            formatted_expression = expression.replace(' & ', ' + ')
            # 輸出每個函數的最終化簡式
            print(f"  {func_name} = {formatted_expression}")