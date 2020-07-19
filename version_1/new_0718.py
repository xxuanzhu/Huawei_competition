import pandas as pd
import numpy as np
import os
import csv
from tqdm import tqdm
import csv
from Config import config

complete_train_path = './data/complete_train.csv'
order_folder_path = './data/order_folder'
route_path_folder = './data/test'
test_data_path = './data/test/BRSSZ-HKHKG.csv'

carrier = pd.read_csv('./data/carrier_info.csv', header=None, names=['loadingOrder', 'carrierName'])
unusual_order = pd.read_csv('./data/unusual_order_folder/unusual_order_10-15ays.csv', header=None,
                            names=['loadingOrder'])

with open('data/unusual_order_folder/unusual-order2carrier_10-15.csv', 'w', encoding='utf-8', newline='') as f:
    csv_writer = csv.writer(f)
    for index1, row1 in tqdm(unusual_order.iterrows()):
        for index2, row2 in carrier.iterrows():
            if (row1['loadingOrder'] == row2['loadingOrder']):
                order = {}
                order['loadingOrder'] = row1['loadingOrder']
                order['carrierName'] = row2['carrierName']
                list_values = [i for i in order.values()]
                csv_writer.writerow(list_values)
            else:
                continue
