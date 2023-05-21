# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

""" DESCRIPTION OF WORK"""
__author__ = "linpingta"

import os
import sys
import logging
import argparse
import re
import time

import pandas as pd


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

    community_dict = {}

    df_list = []
    for cur_file in os.listdir("data"):
        try:
            cur_date = re.search("eroom_time__(.*)_detail__(.*).csv", cur_file, re.IGNORECASE).group(1)
        except:
            continue
        cur_df = pd.read_csv("data/" + cur_file)
        cur_df["cur_date"] = cur_date
        avg_df = cur_df.groupby(["community", "position", "cur_date"]).agg({"unit_price": "mean", "hourseSize": "mean", "total_price": "mean", "hhid": "count"}).reset_index()
        df_list.append(avg_df)

        cur_data_info_list = avg_df.T.to_dict().values()
        for cur_data_info in cur_data_info_list:
            if cur_data_info["community"] not in community_dict:
                community_dict[cur_data_info["community"]] = [
                    (cur_date, cur_data_info["unit_price"], cur_data_info["hhid"], cur_data_info["hourseSize"], cur_data_info["total_price"]),
                    (cur_date, cur_data_info["unit_price"], cur_data_info["hhid"], cur_data_info["hourseSize"], cur_data_info["total_price"]),
                    cur_data_info["position"]
                ]
            else:
                begin_date = community_dict[cur_data_info["community"]][0][0]
                end_date = community_dict[cur_data_info["community"]][1][0]
                if cur_date < begin_date:
                    community_dict[cur_data_info["community"]][0] = (cur_date, cur_data_info["unit_price"], cur_data_info["hhid"], cur_data_info["hourseSize"], cur_data_info["total_price"])
                if cur_date > end_date:
                    community_dict[cur_data_info["community"]][1] = (cur_date, cur_data_info["unit_price"], cur_data_info["hhid"], cur_data_info["hourseSize"], cur_data_info["total_price"])
    total_df = pd.concat(df_list)
    total_df.to_csv("eroom_stats_size_%s.csv" % int(time.time()), encoding='utf-8-sig')

    print("calculate unit price")
    print(total_df)

    final_community_data_list = []
    for community, data_info in community_dict.items():
        begin_unit_price = data_info[0][1]
        end_unit_price = data_info[1][1]
        position = data_info[2]
        unit_price_rate = 100.0 * (end_unit_price - begin_unit_price) / begin_unit_price
        begin_date = data_info[0][0]
        end_date = data_info[1][0]
        begin_hhid = data_info[0][2]
        end_hhid = data_info[1][2]
        begin_house_size = data_info[0][3]
        end_house_size = data_info[1][3]
        begin_total_price = data_info[0][4]
        end_total_price = data_info[1][4]
        final_community_data = {"community": community, "unit_price_rate": unit_price_rate,
                                "position": position, "begin_date": begin_date, "end_date": end_date,
                                "begin_unit_price": begin_unit_price, "end_unit_price": end_unit_price,
                                "begin_hhid": begin_hhid, "end_hhid": end_hhid,
                                "begin_house_size": begin_house_size, "end_house_size": end_house_size,
                                "begin_total_price": begin_total_price, "end_total_price": end_total_price}
        final_community_data_list.append(final_community_data)
    final_community_df = pd.DataFrame(final_community_data_list)
    print(final_community_df)
    final_community_df.to_csv("final_community_eroom_stats_size_%s.csv" % int(time.time()), encoding='utf-8-sig')


if __name__ == '__main__':
    main()
