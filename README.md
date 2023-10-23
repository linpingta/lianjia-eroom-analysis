# lianjia-eroom-crawler
Crawler / Analysis of eroom data (链家爬虫/数据分析; 2017年前成交价)

[![GitHub stars](https://img.shields.io/github/stars/linpingta/lianjia-eroom-crawler.svg?style=social&label=Star)](https://github.com/linpingta/lianjia-eroom-crawler/stargazers)
[![Fork](https://img.shields.io/badge/-Fork-green?logo=github&style=for-the-badge)](https://github.com/linpingta/lianjia-eroom-crawler/fork)
[![Clone](https://img.shields.io/badge/Clone-HTTPS-blue.svg)](https://github.com/linpingta/lianjia-eroom-crawler.git)

## 链家房价爬虫和数据分析
这是一个使用 Python 编写的链家房价爬虫和数据分析脚本。通过这个脚本，您可以爬取链家网站上的房屋信息，并进行数据分析和可视化。

## 功能特点
### 爬取功能
链家网站上的房屋信息，包括房屋价格、面积、所在区域、房型等

可以根据用户的需求自定义爬取的区域等参数。

### 分析功能
提供了多种数据分析功能，例如计算平均房价、绘制房价分布直方图等。

提供基于多组房价数据的挂牌价格变化查找分析功能

提供小区级别平均价格变化分析功能

支持数据导出为 CSV 文件，方便后续处理和分析。

### 适用范围
本项目默认行为对北京链家数据爬虫，但很容易修改后支持其它地区，如杭州，武汉等地区爬虫，

## 重要：原始历史数据
相信对于很多人而言，爬虫本身并不是困难的问题，但爬虫只能获取最新挂牌价格信息，并不能直接获取历史信息。本项目不仅提供了获取最新信息的方式，也提供了历史报价信息，方便使用者参考

## 使用方法

1. 安装所需的依赖库。

```
pip install pandas
pip install lxml
pip install bs4

```

2. 运行爬虫

```
python eroom_finder.py
```
之后你会看到结果如eroom_time__20221227_detail__1672138021__*.csv


3. 运行数据分析：平均价格统计

```
python eroom_analysis.py
```
脚本将会将爬取的数据保存为 final_community_eroom_stats_size_*.csv 文件， *为软件运行的YYYYMMDD。

4. 运行数据分析：房价变化统计

```
python eroom_analysis2.py
```
脚本将会将爬取的数据保存为 stats_info_updated_*.csv 文件。

## 历史成交价

数据可见web_old_eroom_chengjiao_before_2018_new.csv

免责声明：本项目并不能保证历史成交价的准确性，希望帮助到有相关需要的人，所以会在力所能及范围内保证准确，但作为一个免费项目，不会对数据准确性承担法律或相关的任何责任，如需使用请自行甄别验证，最好对多个数据来源相互印证。


## 注意事项
请尊重链家网站的使用规则，避免过于频繁地进行爬取操作。
由于网站结构可能会发生变化，脚本在未来的某些时刻可能需要进行适当的修改以适应新的页面布局。

## 贡献
欢迎对本项目提出改进建议和提交贡献代码。如果您发现了 bug 或者有新功能的想法，请在 GitHub 上提交 issue，或者发送邮件到linpingta@163.com


