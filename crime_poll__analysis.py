# %% [1] 匯入套件與設定
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 設定圖表風格
sns.set_style("whitegrid")
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False 

# %% [2] 資料讀取與前處理
filename = 'Data.csv'

if os.path.exists(filename):
    # 讀取資料
    df = pd.read_csv(filename)
    
    # 1. 移除無效的空行 (Drop Empty Rows)
    # 檢查 year 或 month 為空值的列並刪除
    df = df.dropna(subset=['year', 'month'])
    
    # 2. 建立時間序列 (Convert to Datetime)
    df['date'] = pd.to_datetime({'year': df['year'], 'month': df['month'], 'day': 1})
    
    # 3. 處理缺值 (Handle Missing Values) - 使用線性插值 + 前後填補
    # 定義需要修補的數值欄位
    target_cols = ['crime_rate', 'violent_crime_rate', 'fraud_rate', 
                   'president_approval', 'ruling_party_approval']
    
    # interpolate(): 填補中間的缺口 (根據時間趨勢連線)
    # bfill(): 如果第一筆是空的，用後面那一筆來補 (Back Fill)
    df[target_cols] = df[target_cols].interpolate(method='linear').bfill()

    print(f"資料處理完成！有效筆數: {len(df)} 筆")
    print("缺值已自動修補。")
    
else:
    print(f"找不到檔案: {filename}")
    exit()

# %% [3] 定義分析目標
crime_map = {
    'crime_rate': '刑案犯罪率',
    'violent_crime_rate': '暴力犯罪率',
    'fraud_rate': '詐欺犯罪率'
}

poll_map = {
    'president_approval': '總統滿意度',
    'ruling_party_approval': '執政黨信任度' 
}
print(f"X / Y 軸 設定完成")

# %% [4] 畫圖：雙軸折線圖 (Time Series)
print("\n" + "="*50)
print(f"{'犯罪指標':<10} vs {'民調指標':<10} | {'相關係數 (r)':<8} | {'解讀'}")
print("-" * 50)

# 雙重迴圈：遍歷 [所有犯罪指標] x [所有民調指標]
for poll_col, poll_label in poll_map.items():
    for crime_col, crime_label in crime_map.items():
        
        # 1. 計算相關係數
        corr = df[crime_col].corr(df[poll_col])
        
        # 統計解讀
        strength = "高度" if abs(corr) > 0.7 else "中度" if abs(corr) > 0.3 else "低度"
        relation = "正相關" if corr > 0 else "負相關"
        
        print(f"{crime_label:<10} vs {poll_label:<10} | {corr:8.4f}   | {strength}{relation}")

        # 2. 繪製圖表
        fig, ax1 = plt.subplots(figsize=(10, 5))

        # 左軸：犯罪數據
        color_1 = 'tab:red'
        ax1.set_xlabel('時間 (Date)')
        ax1.set_ylabel(f'{crime_label} (件/十萬人口)', color=color_1, fontweight='bold')
        ax1.plot(df['date'], df[crime_col], color=color_1, marker='o', alpha=0.8, label=crime_label)
        ax1.tick_params(axis='y', labelcolor=color_1)
        ax1.grid(True, alpha=0.3)

        # 右軸：民調數據
        ax2 = ax1.twinx()
        color_2 = 'tab:blue' if poll_col == 'president_approval' else 'tab:green' # 不同指標用不同色
        ax2.set_ylabel(f'{poll_label} (%)', color=color_2, fontweight='bold')
        ax2.plot(df['date'], df[poll_col], color=color_2, marker='s', linestyle='--', alpha=0.8, label=poll_label)
        ax2.tick_params(axis='y', labelcolor=color_2)

        plt.title(f'趨勢分析：{crime_label} vs {poll_label} (r={corr:.2f})')
        plt.tight_layout()
        plt.show()

print("="*50)

# %% [5] 散佈圖與迴歸線

print("\n" + "="*50)
print("正在生成散佈圖...")

for poll_col, poll_label in poll_map.items():
    for crime_col, crime_label in crime_map.items():
        
        plt.figure(figsize=(8, 6))
        
        # 1. 設定顏色：總統用紫色，執政黨用綠色
        color_code = 'purple' if poll_col == 'president_approval' else 'seagreen'
        
        # 2. 畫散佈圖 + 迴歸直線
        # ci=None: 不顯示信賴區間陰影 (讓圖面比較乾淨)
        # scatter_kws: 設定點的透明度，避免點重疊時看不清楚
        sns.regplot(x=crime_col, y=poll_col, data=df, 
                    color=color_code, ci=None, 
                    scatter_kws={'alpha': 0.6, 's': 60})
        
        # 3. 計算相關係數 (放在標題)
        corr = df[crime_col].corr(df[poll_col])
        
        plt.title(f'散佈圖分析：{crime_label} vs {poll_label} (r={corr:.2f})', fontsize=14)
        plt.xlabel(f'{crime_label} (件/十萬人口)', fontsize=12)
        plt.ylabel(f'{poll_label} (%)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

print("所有散佈圖繪製完成。")
# %%
