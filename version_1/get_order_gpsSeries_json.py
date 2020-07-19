import pandas as pd
import numpy as np
import os
import csv
from tqdm import tqdm
import csv
from Config import config
from Utils import SaveJson

"""
得到json格式运单数据
"""

complete_train_path = './data/complete_train.csv'
order_folder_path = './data/order_folder'
order_gps_folder_path = './data/test'
order_json_path = 'data/order_json'

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

with open(order_json_path, 'w', encoding='utf-8', newline='') as f:
    csv_writer = csv.writer(f)
    for i in unusual_order:
        csv_writer.writerow([i])
print('done')
print(unusual_order)



