# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

""" DESCRIPTION OF WORK"""
__author__ = "linpingta"

import os
import sys
import logging
import argparse
import re
import pandas as pd
import datetime
import copy
import time
from collections import defaultdict


def generate_base_info_dict(key, df, logger):
    base_info_dict = {}
    cur_data_info_list = df.T.to_dict().values()
    for cur_data_info in cur_data_info_list:
        hhid = cur_data_info["hhid"]
        cur_data_info_t = cur_data_info
        cur_data_info_t["online_time"] = key
        base_info_dict[hhid] = cur_data_info_t

    logger.info("base key[%s] generate req_num[%s]" % (key, len(base_info_dict)))
    return base_info_dict


def update_base_info_df(new_key, new_df, pre_key, base_dict, logger):
    """ change will be three types:
    1. same hhid but different price
    2. new hhid not exists in old
    3. old hhid not exists in new
    """
    pre_key_date = datetime.datetime.strptime(pre_key, "%Y%m%d")
    new_key_date = datetime.datetime.strptime(new_key, "%Y%m%d")
    new_pre_day_range = (new_key_date - pre_key_date).days

    old_base_dict = copy.deepcopy(base_dict)
    info_list = []
    info_stats_summary_dict = defaultdict(int)
    new_data_info_list = new_df.T.to_dict().values()
    for new_data_info in new_data_info_list:
        new_hhid = new_data_info["hhid"]
        community = new_data_info["community"]

        if new_hhid in base_dict: # existing hhid
            new_total_price = new_data_info["total_price"]
            old_total_price = base_dict[new_hhid]["total_price"]
            online_time = base_dict[new_hhid]["online_time"]
            info_dict = {
                "hhid": str(new_hhid),
                "pre_time": pre_key,
                "new_time": new_key,
                "community": community,
                "online_time": online_time,
                "new_pre_day_range": new_pre_day_range,
                "pre_data": old_total_price,
                "new_data": new_total_price
            }
            if new_total_price > old_total_price:
                info_dict["type"] = "increase_price"
                info_dict["info"] = new_total_price - old_total_price
                info_list.append(info_dict)
                info_stats_summary_dict["increase_price"] += 1
            elif new_total_price < old_total_price:
                info_dict["type"] = "decrease_price"
                info_dict["info"] = new_total_price - old_total_price
                info_list.append(info_dict)
                info_stats_summary_dict["decrease_price"] += 1

            # always update base_dict result
            base_dict[new_hhid]["total_price"] = new_total_price
            info_stats_summary_dict["existing_hhid_cnt"] += 1
        else: # new source updated
            new_data_info_t = new_data_info
            new_data_info_t["online_time"] = new_key
            base_dict[new_hhid] = new_data_info_t

            info_dict = {
                "hhid": str(new_hhid),
                "pre_time": -1,
                "new_time": new_key,
                "community": community,
                "online_time": new_key,
                "new_pre_day_range": new_pre_day_range,
                "type": "new_upload",
                "info": -1,
                "pre_data": -1,
                "new_data": -1
            }
            info_list.append(info_dict)
            info_stats_summary_dict["new_hhid_cnt"] += 1

    for old_hhid, old_data_info in old_base_dict.items():
        if old_hhid not in base_dict: # info remove
            online_time_date = datetime.datetime.strptime(base_dict[new_hhid]["online_time"], "%Y%m%d")
            new_online_day_range = (new_key_date - online_time_date).days
            community = old_data_info["community"]

            info_dict = {
                "hhid": str(old_hhid),
                "pre_time": pre_key,
                "new_time": new_key,
                "community": community,
                "online_time": old_data_info["online_time"],
                "new_pre_day_range": new_pre_day_range,
                "type": "down_online_less_equal_than",
                "info": new_online_day_range,
                "pre_data": online_time_date,
                "new_data": new_key_date
            }
            info_list.append(info_dict)
            info_stats_summary_dict["delete_hhid_cnt"] += 1

    logger.info("pre_key[%s] -> new_key[%s] generate req_num[%s]" % (pre_key, new_key, len(base_dict)))
    logger.info("pre_key[%s] -> new_key[%s] info_summary_dict: %s" % (pre_key, new_key, str(info_stats_summary_dict)))

    return base_dict, info_list


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
    parser.parse_args()

    date_df_dict = {}
    cnt = 0
    for cur_file in os.listdir("."):
        try:
            cur_date = re.search("eroom_time__(.*)_detail__(.*).csv", cur_file, re.IGNORECASE).group(1)
        except Exception as e:
            continue
        cur_df = pd.read_csv(cur_file)
        cur_df["cur_date"] = cur_date
        date_df_dict[cur_date] = cur_df

    base_info_dict = {}
    total_info_list = []
    pre_key = -1
    for idx, key in enumerate(sorted(date_df_dict)):
        if idx == 0:
            logger.info("key[%s]: generate base info" % key)
            base_info_dict = generate_base_info_dict(key, date_df_dict[key], logger)
        else:
            logger.info("pre_key[%s] -> key[%s]: update base info" % (pre_key, key))
            new_base_info_dict, info_list = update_base_info_df(key, date_df_dict[key], pre_key, base_info_dict, logger)
            base_info_dict = new_base_info_dict
            total_info_list.extend(info_list)

        pre_key = key

    # output final info
    total_info_df = pd.DataFrame(total_info_list)
    total_info_df.to_csv("stats_info_updated_%s.csv" % int(time.time()), encoding='utf-8-sig')


if __name__ == '__main__':
    main()
