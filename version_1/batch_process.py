import pandas as pd
import numpy as np
import os
import csv
from tqdm import tqdm
import csv
from Config import config

"""
生成时间异常的订单数据
"""

complete_train_path = './data/complete_train.csv'
order_folder_path = './data/order_folder'
order_gps_folder_path = './data/gps'
unusual_order_path = 'data/unusual_order_folder/unusual_order_30+days.csv'

unusual_order = set()
fileList = os.listdir(order_gps_folder_path)
for file in fileList:
    path = os.path.join(order_gps_folder_path, file)
    file_base = os.path.basename(path).split('.')[0]
    arr = file_base.split('_')
    order = arr[0]
    test_chunk = pd.read_csv(path, header=None,
                             names=['timestamp', 'longitude', 'latitude', 'speed', 'direction'])
    row_index = test_chunk.shape[0]-1
    time_last = pd.to_datetime(test_chunk.loc[row_index, 'timestamp'], infer_datetime_format=True)
    time_first = pd.to_datetime(test_chunk.loc[1, 'timestamp'], infer_datetime_format=True)
    time_diff = (time_last - time_first).total_seconds()
    if time_diff > 2592000:
        unusual_order.add(order)

with open(unusual_order_path, 'w', encoding='utf-8', newline='') as f:
    csv_writer = csv.writer(f)
    for i in unusual_order:
        csv_writer.writerow([i])
print('done')
print(unusual_order)
# print(unusual_order)

    # file_base = os.path.basename(path).split('.')[0]
    # new_path = os.path.join(route_path_folder, file_base)
    # os.mkdir(new_path)
    # csv_file = {}
    # csv_writer = {}
    # order= []
    # for chunk in tqdm(test_chunk):
    #     order.append(chunk['loadingOrder'].unique())
    # order_unique = []
    # for i in order:
    #     for j in i:
    #         order_unique.append(j)
    #
    #
    # for order in order_unique:
    #     order_writer_path = os.path.join(new_path, "{}.csv".format(order))
    #     csv_file[order] = open(order_writer_path, 'w', encoding='utf-8', newline='')
    #     csv_writer[order] = csv.writer(csv_file[order])
    #
    # test_chunk = pd.read_csv(path, chunksize=200000, header=None,
    #                          names=['loadingOrder', 'timestamp', 'longitude', 'latitude', 'speed'])
    #
    # for chunk in tqdm(test_chunk):
    #     for row in chunk.itertuples(index=False):
    #         if row[0] in order_unique:
    #             row_info = row._asdict()
    #             csv_writer[row[0]].writerow(row_info.values())
    #
    # for k, v in csv_file.items():
    #     v.close()


