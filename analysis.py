# %%
import pandas as pd
import os

# --- 這是給 C++ 背景的你的特別說明 ---
# Python 腳本執行的「當前路徑 (CWD)」通常是 VS Code 開啟的根目錄
# 所以讀取檔案時，建議包含資料夾名稱，或者使用絕對路徑
# 你的檔案結構是： 根目錄 -> 統計學習 -> Data.csv

csv_path = 'Data.csv' 

# 為了保險起見，我們先檢查檔案在不在
if os.path.exists(csv_path):
    print(f"找到檔案了：{csv_path}")
    df = pd.read_csv(csv_path)
    print(df.head()) # 印出前五行
else:
    print(f"找不到檔案！請確認路徑。當前路徑是: {os.getcwd()}")
# %%
