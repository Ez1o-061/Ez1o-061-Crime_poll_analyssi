# %% [1] 匯入套件與設定
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 設定圖表風格
sns.set_style("whitegrid")
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False 

# %% [2] 讀取 CSV 檔案
# 設定檔案名稱
filename = 'Data.csv'

# 檢查檔案是否存在，避免報錯
if os.path.exists(filename):
    try:
        # 讀取 CSV
        df = pd.read_csv(filename)
        print(f"成功讀取檔案: {filename}")
        print(f"資料筆數: {len(df)} 筆")
    except Exception as e:
        print(f"讀取檔案發生錯誤: {e}")
else:
    print(f"找不到檔案: {filename}")
    # 這裡停止後續執行，因為沒有資料無法畫圖
    df = None

# %% [3] 資料清整與相關係數分析
if df is not None:
    # 1. 建立時間序列 (Datetime) 讓 X 軸正確排序
    try:
        df['date'] = pd.to_datetime({'year': df['year'], 'month': df['month'], 'day': 1})
        print("\n時間欄位處理完成。")
    except KeyError as e:
        print(f"\n錯誤: CSV 檔案中缺少必要的欄位 {e}")

    # 2. 計算相關係數
    # 確保 CSV 裡有 'crime_rate' 和 'president_approval'
    if 'crime_rate' in df.columns and 'president_approval' in df.columns:
        corr = df['crime_rate'].corr(df['president_approval'])
        print("-" * 30)
        print(f"犯罪率 vs 滿意度 相關係數 (r): {corr:.4f}")
        print("-" * 30)

        # 簡單解讀
        if abs(corr) > 0.7:
            strength = "高度相關"
        elif abs(corr) > 0.3:
            strength = "中度相關"
        else:
            strength = "低度相關"
        
        relation = "正相關" if corr > 0 else "負相關"
        print(f"統計解讀: 兩者呈現 {strength} ({relation})")
    else:
        print("錯誤: CSV 中找不到 'crime_rate' 或 'president_approval' 欄位。")

# %% [4] 畫圖：雙軸折線圖 (Time Series)
if df is not None:
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # 左軸：犯罪率
    color_1 = 'tab:red'
    ax1.set_xlabel('時間 (Year-Month)', fontsize=12)
    ax1.set_ylabel('刑案犯罪率 (件/十萬人口)', color=color_1, fontsize=12, fontweight='bold')
    ax1.plot(df['date'], df['crime_rate'], color=color_1, marker='o', linewidth=2, label='犯罪率')
    ax1.tick_params(axis='y', labelcolor=color_1)
    ax1.grid(True, alpha=0.3)

    # 右軸：滿意度
    ax2 = ax1.twinx()
    color_2 = 'tab:blue'
    ax2.set_ylabel('總統執政滿意度 (%)', color=color_2, fontsize=12, fontweight='bold')
    ax2.plot(df['date'], df['president_approval'], color=color_2, marker='s', linestyle='--', linewidth=2, label='滿意度')
    ax2.tick_params(axis='y', labelcolor=color_2)

    plt.title(f'犯罪率 vs 民調滿意度趨勢分析 (r={corr:.2f})', fontsize=16)
    plt.tight_layout()
    plt.show()

# %% [5] 畫圖：散佈圖與迴歸線
if df is not None:
    plt.figure(figsize=(8, 6))
    
    # ci=None 代表不畫信賴區間，若資料量大(>30筆)可以拿掉 ci=None 看看效果
    sns.regplot(x='crime_rate', y='president_approval', data=df, color='purple', ci=None)
    
    plt.title('散佈圖：犯罪率對滿意度的影響', fontsize=14)
    plt.xlabel('刑案犯罪率 (件/十萬人口)', fontsize=12)
    plt.ylabel('總統滿意度 (%)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.show()
# %%