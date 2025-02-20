import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv('lianjia_ershoufang_20250220_112515.csv')

# 数据预处理
df['总价（万）'] = pd.to_numeric(df['总价（万）'], errors='coerce')
df['面积（㎡）'] = df['面积（㎡）'].str.replace('㎡', '').astype(float)
df['单价（元/㎡）'] = pd.to_numeric(df['单价（元/㎡）'], errors='coerce')

# 按区域计算平均总价和房源数量
region_group = df.groupby('区域').agg({'总价（万）': 'mean', '标题': 'count'}).rename(columns={'标题': '房源数量'}).reset_index()

# 按面积段计算平均总价和房源数量
bins = [0, 50, 100, 150, 200, 250, 300]
labels = ['0-50㎡', '50-100㎡', '100-150㎡', '150-200㎡', '200-250㎡', '250-300㎡']
df['面积段'] = pd.cut(df['面积（㎡）'], bins=bins, labels=labels, right=False)
area_group = df.groupby('面积段').agg({'总价（万）': 'mean', '标题': 'count'}).rename(columns={'标题': '房源数量'}).reset_index()

# 可视化
plt.figure(figsize=(14, 6))

# 区域平均总价
plt.subplot(1, 2, 1)
plt.bar(region_group['区域'], region_group['总价（万）'])
plt.xlabel('区域')
plt.ylabel('平均总价（万）')
plt.title('各区域二手房平均总价')
plt.xticks(rotation=45)

# 面积段房源数量
plt.subplot(1, 2, 2)
plt.bar(area_group['面积段'], area_group['房源数量'])
plt.xlabel('面积段')
plt.ylabel('房源数量')
plt.title('不同面积段二手房源数量')

plt.tight_layout()
plt.show()
