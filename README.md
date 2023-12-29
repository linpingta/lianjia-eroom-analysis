# eroom-analysis
Analysis of eroom data 数据分析

### 更新

2023-12-08: 基于提供数据，可以分析北京22/23年房价变化

2023-10-25: 为方便数据管理，原先eroom_xxxx_.csv等历史报价快照，被分别移入bj_data(beijing 北京), hz_data(hangzhou 杭州), sh_data(shanghai 上海), sz_data(shenzhen 深圳), gz_data(guangzhou 广州)等目录，历史数据持续提供中

[![GitHub stars](https://img.shields.io/github/stars/linpingta/lianjia-eroom-crawler.svg?style=social&label=Star)](https://github.com/linpingta/lianjia-eroom-crawler/stargazers)
[![Fork](https://img.shields.io/badge/-Fork-green?logo=github&style=for-the-badge)](https://github.com/linpingta/lianjia-eroom-crawler/fork)
[![Clone](https://img.shields.io/badge/Clone-HTTPS-blue.svg)](https://github.com/linpingta/lianjia-eroom-crawler.git)

## 链家房价爬虫和数据分析
这是一个使用Python编写的链家房价爬虫和数据分析脚本。通过这个脚本，您可以爬取链家网站上公开的房屋信息，并进行数据分析和可视化。

### 项目背景
因为前两年在关注北京二手房市场，但搜索发现的一些链家爬虫缺少更新，也不支持数据分析的功能，因此开发了这个项目。我们可以看到相比前两年，房价跌了还是涨了，挂牌多了还是少了，有效帮助购房人。

### 爬取功能
链家网站上的公开房屋信息，包括房屋价格、面积、所在区域、房型等

可以根据用户的需求自定义爬取的区域等参数。

<img width="1311" alt="image" src="https://github.com/linpingta/lianjia-eroom-crawler/assets/2771082/09117727-c8af-4633-897c-6434883fff95">


### 分析功能
提供了多种数据分析功能，例如计算平均房价、绘制房价分布直方图等。

提供基于多组房价数据的挂牌价格变化查找分析功能

提供小区级别平均价格变化分析功能

支持数据导出为 CSV 文件，方便后续处理和分析。
<img width="926" alt="image" src="https://github.com/linpingta/lianjia-eroom-crawler/assets/2771082/9f6a2ba4-3772-40d8-9dd9-03f0191eb7f4">


### 适用范围
本项目默认行为对北京链家数据爬虫（其它城市仅示例），可修改后支持其它地区，如**杭州**，武汉，深圳等地区爬虫（上海相对特殊一点，需要一些小改动）
简单修改代码如:
```
'https://bj.lianjia.com/ershoufang/' -> 'https://hz.lianjia.com/ershoufang/'
```

## 使用方法

1. 安装所需的依赖库。

```
pip install pandas
pip install lxml
pip install bs4

```

2. 运行爬虫

无参数运行，默认处理beijing，各个区数据，比如东城区
```
python eroom_finder.py --city_name bj
```

指定参数运行：
(1) 指定其它城市
(2) 指定特定区域（比如四惠）
```
python eroom_finder.py --city_name bj --area_name small
```
之后你会看到结果如eroom_time__20221227_detail__1672138021__*.csv


3. 运行数据分析：小区平均价格统计

```
python eroom_price_adjust_tracker.py
```
脚本将会将爬取的数据保存为 final_community_eroom_stats_size_*.csv 文件， *为软件运行的YYYYMMDD。

基于结果进行进一步的可视化分析，如

<img width="730" alt="image" src="https://github.com/linpingta/lianjia-eroom-crawler/assets/2771082/8903e445-39c0-4086-9a1b-3c71315bd06d">


4. 运行数据分析：房价变化统计

```
python eroom_district_comparer.py
```
脚本将会将爬取的数据保存为 stats_info_updated_*.csv 文件。

基于历史数据，可以方便分析出特定房源的挂牌价变化情况，挂牌上架下架（重新上架）时间

<img width="717" alt="image" src="https://github.com/linpingta/lianjia-eroom-crawler/assets/2771082/48ebcadd-acb8-488e-af25-46fb9f908c9c">


## 免责声明
本项目永远作为一个免费项目使用，仅用于学习交流使用，使用者不得用于谋利或访问非公开数据

本项目并不保证历史数据的准确性，希望帮助到有相关需要的购房人，不对数据准确性/一致性承担法律或相关任何责任，使用者请自行甄别判断。

## 注意事项 ！！注意事项 ！！
请尊重链家网站的使用规则，本程序只可用于适度访问公开数据，严禁修改本程序访过于频繁地进行访问，严禁修改本程序访问任何非公开数据。

数据只能用于个人使用，不支持数据共享，不能用于任何商业用途，请遵守中国相关法律

## 贡献
欢迎对本项目提出改进建议和提交贡献代码。如果您发现了 bug，请在 GitHub 上提交 issue


