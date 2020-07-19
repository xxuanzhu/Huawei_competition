import pandas as pd
import numpy as np
from tqdm import tqdm
import csv
from Config import config
import os
from Utils import get_port_info
import json
import os


complete_train_path = './data/complete_train.csv'
order_folder_path = './data/order_folder'
route_path_folder = './data/gps'

data = pd.read_csv('./data/unusual_order_folder/unusual-order2carrier_10-15.csv', header=None, names=['loadingOrder', 'carrierName'])
data.sort_values('carrierName', inplace=True)
data.to_csv('./data/unusual_order_folder/unusual-order2carrier_10-15.csv')

# port = get_port_info(config.test_data_path)
# port = json.dumps(port)
#
# with open('./data/port.json', "w", encoding='utf-8') as f:
#     f.write(port + ",\n")
#     print("^_^ write success")
#
# print(port)