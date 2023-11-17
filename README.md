# lianjia-eroom-crawler
Crawler / Analysis of eroom data (链家爬虫/数据分析; 2017年前成交价)

### 更新
2023-10-25: 为方便数据管理，原先eroom_xxxx_.csv等历史报价快照，被分别移入bj_data(beijing 北京), hz_data(hangzhou 杭州), sh_data(shanghai 上海), sz_data(shenzhen 深圳), gz_data(guangzhou 广州)等目录，历史数据持续提供中

[![GitHub stars](https://img.shields.io/github/stars/linpingta/lianjia-eroom-crawler.svg?style=social&label=Star)](https://github.com/linpingta/lianjia-eroom-crawler/stargazers)
[![Fork](https://img.shields.io/badge/-Fork-green?logo=github&style=for-the-badge)](https://github.com/linpingta/lianjia-eroom-crawler/fork)
[![Clone](https://img.shields.io/badge/Clone-HTTPS-blue.svg)](https://github.com/linpingta/lianjia-eroom-crawler.git)

## 链家房价爬虫和数据分析
这是一个使用Python编写的链家房价爬虫和数据分析脚本。通过这个脚本，您可以爬取链家网站上的房屋信息，并进行数据分析和可视化。

### 项目背景
因为前两年在关注北京二手房市场，但搜索发现的一些链家爬虫已经几年没有更新过，也不支持数据分析的功能，因此开发了这个项目。
相比其它lianjia爬虫，目前看它的一个重要优点在于仍然可用（咳咳，但这确实是一个优点）。
而且在我看来，lianjia爬虫并不困难，但lianjia爬虫只能获取最新的数据，某种程度来说，我们只知道一个状态。但在实际问题里，我们更关心的是相比前两年，房价跌了还是涨了，挂牌多了还是少了，这些信息不仅需要最新的数据，更需要对历史数据的维护。本项目不仅提供了爬虫功能，也持续更新历史数据，方便参考。

## 功能特点

https://zhuanlan.zhihu.com/p/637813923

### 爬取功能
链家网站上的房屋信息，包括房屋价格、面积、所在区域、房型等

可以根据用户的需求自定义爬取的区域等参数。

<img width="1311" alt="image" src="https://github.com/linpingta/lianjia-eroom-crawler/assets/2771082/09117727-c8af-4633-897c-6434883fff95">


### 分析功能
提供了多种数据分析功能，例如计算平均房价、绘制房价分布直方图等。

提供基于多组房价数据的挂牌价格变化查找分析功能

提供小区级别平均价格变化分析功能

支持数据导出为 CSV 文件，方便后续处理和分析。
<img width="926" alt="image" src="https://github.com/linpingta/lianjia-eroom-crawler/assets/2771082/9f6a2ba4-3772-40d8-9dd9-03f0191eb7f4">


### 适用范围
本项目默认行为对北京链家数据爬虫，但很容易修改后支持其它地区，如**杭州**，武汉，深圳等地区爬虫（上海相对特殊一点，需要一些小改动），例如 "hangzhou_eroom_time__20220115_detail__1642235044__area_1.csv".
简单修改代码里的:
```
'https://bj.lianjia.com/ershoufang/' -> 'https://hz.lianjia.com/ershoufang/'
```

## 重要：原始历史数据
相信对于很多人而言，爬虫本身并不是困难的问题，但爬虫只能获取最新挂牌价格信息，并不能直接获取历史信息。本项目不仅提供了获取最新信息的方式，也提供了历史报价信息，方便使用者参考.
参见项目目录里 "_20220128_" 等。

```
bj_data/eroom_xxx_.csv :  北京历史报价快照
hz_data/eroom_xxx_.csv :  北京历史报价快照
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


## 历史成交价

数据可见web_old_eroom_chengjiao_before_2018_new.csv

<img width="1277" alt="image" src="https://github.com/linpingta/lianjia-eroom-crawler/assets/2771082/67ed939c-e1fa-45b9-be27-49628d06c76c">


免责声明：本项目并不能保证历史成交价的准确性，希望帮助到有相关需要的人，所以会在力所能及范围内保证准确，但作为一个免费项目，不会对数据准确性承担法律或相关的任何责任，如需使用请自行甄别验证，最好对多个数据来源相互印证。


## 注意事项
请尊重链家网站的使用规则，避免过于频繁地进行爬取操作。
由于网站结构可能会发生变化，脚本在未来的某些时刻可能需要进行适当的修改以适应新的页面布局。

## 贡献
欢迎对本项目提出改进建议和提交贡献代码。如果您发现了 bug 或者有新功能的想法，请在 GitHub 上提交 issue，或者发送邮件到linpingta@163.com


