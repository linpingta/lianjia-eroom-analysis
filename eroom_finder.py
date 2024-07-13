# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

""" DESCRIPTION OF WORK"""
__author__ = "linpingta"

import argparse
import logging
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import math
import requests
import lxml
import re
import time
import datetime
import traceback


def re_match(re_pattern, string, errif=None):
    try:
        return re.findall(re_pattern, string)[0].strip()
    except IndexError:
        return errif


def get_house_info(start_url, sess, headers):
    html = sess.get(start_url, headers=headers, allow_redirects=True, timeout=3).text
    house_num = re.findall('共找到<span> (.*?) </span>套.*二手房', html)[0].strip()
    return house_num


def get_info_dic(info, area, city_name):
    info_dic = {
        'area': area,
        'title': re_match('target="_blank">(.*?)</a><!--', str(info)),
        'community': re_match('xiaoqu.*?target="_blank">(.*?)</a>', str(info)),
        'position': re_match('<a href.*?target="_blank">(.*?)</a>.*?class="address">', str(info)),
        'tax': re_match('class="taxfree">(.*?)</span>', str(info)),
        'total_price': float(re_match('class="totalPrice totalPrice2"><i> </i><span class="">(.*?)</span><i>万', str(info))),
        'unit_price': float(re_match('data-price="(.*?)"', str(info))),
    }
    hhid = re.findall('data-housecode="(.*?)"', str(info))[0]
    info_dic.update({
        'hhid': hhid,
        'link': f'https://{city_name}.lianjia.com/ershoufang/{hhid}.html',
    })
    icons = re.findall('class="houseIcon"></span>(.*?)</div>', str(info))[0].strip().split('|')
    info_dic.update({
        'hourseType': icons[0].strip(),
        'hourseSize': float(icons[1].replace('平米', '')),
        'direction': icons[2].strip(),
        'fitment': icons[3].strip(),
        'level': icons[4].strip(),
        'buildTime': icons[5].strip(),
    })
    return info_dic


def crawl_data(sess, real_dict, city_name, headers):
    total_num = 0
    err_num = 0
    data_info_list = []
    url = 'https://%s.lianjia.com/ershoufang/{}/pg{}/' % city_name

    for key_, value_ in real_dict.items():
        start_url = ('https://%s.lianjia.com/ershoufang/{}/' % city_name).format(value_)
        house_num = get_house_info(start_url, sess, headers)
        print('{}: 二手房源共计「{}」套'.format(key_, house_num))
        time.sleep(2)
        total_page = int(math.ceil(min(3000, int(house_num)) / 30.0))
        for i in tqdm(range(total_page), desc=key_):
            html = sess.get(url.format(value_, i+1), headers=headers, allow_redirects=True, timeout=3).text
            soup = BeautifulSoup(html, 'lxml')
            info_collect = soup.find_all(class_="info clear")
            for info in info_collect:
                try:
                    info_dic = get_info_dic(info, key_, city_name)
                    data_info_list.append(info_dic)
                except Exception as e:
                    traceback.print_exc()
                    print("icons <= 5 means not house, but car position")
                    err_num += 1
                total_num += 1
    print("after crawl, total_num[%s] err_num[%s]" % (total_num, err_num))
    return data_info_list


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(filename)s:%(lineno)s - %(funcName)s %(asctime)s;%(levelname)s] %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S'
    )
    logger = logging.getLogger(__file__)

    example_word = """
        DESCRIBE ARGUMENT USAGE HERE
        python main.py --help
    """

    parser = argparse.ArgumentParser(prog=__file__, description='code description', epilog=example_word,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    # add parameter if needed
    parser.add_argument('-v', '--version', help='version of code', action='version', version='%(prog)s 1.0')
    parser.add_argument('--area_name', help='area to fetch', type=str, default='all')
    parser.add_argument('--city_name', help='city to fetch', type=str, default='bj')

    args = parser.parse_args()

    city_name = args.city_name

    area_dic = {}
    area_dic_small = {}
    if city_name == "bj":
        # all beijing
        area_dic = {'朝阳区': 'chaoyang',
                    '海淀区': 'haidian',
                    '西城区': 'xicheng'
        }
        area_dic_small = {
            '五道口': 'wudaokou',
        }
    elif city_name == "hz":
        area_dic = {
            '钱塘区': 'qiantangqu'
                    }
        area_dic_small = {
            # define as real need
        }
    else:
        print("no area dic defined in city:%s, fill it first" % city_name)
        exit(1)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
        'Referer': 'https://%s.lianjia.com/ershoufang/' % city_name}
    sess = requests.session()
    sess.get('https://%s.lianjia.com/ershoufang/' % city_name, headers=headers)

    real_dict = area_dic
    if args.area_name == 'small':
        real_dict = area_dic_small

    data_info_list = crawl_data(sess, real_dict, city_name, headers)
    data = pd.DataFrame(data_info_list)
    data.to_csv("eroom_time__%s_detail__%s__area_%s.csv" % (datetime.datetime.now().strftime('%Y%m%d'), int(time.time()), len(area_dic.values())), encoding='utf-8-sig')


if __name__ == '__main__':
    main()
