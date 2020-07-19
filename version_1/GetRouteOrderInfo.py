import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import csv
from Config import config

route_order_folder_path = './data/route_order_data'
complete_train_path = './data/complete_train.csv'


def get_test_route_set(path):
    """得到测试集的路径数据
        Args:
            path: 测试集路径

        Returns：
            test_route_set (dict): 非重复的船的路由
            test_route_info (dict): 船的起始和终止港

    """
    test_route_info = {}
    data = pd.read_csv(path)
    test_route_set = data['TRANSPORT_TRACE'].unique()
    for route in test_route_set:
        ports = route.split("-")
        start_port = ports[0]
        dest_port = ports[-1]
        test_route_info[route] = {}
        test_route_info[route]['start_port'] = start_port
        test_route_info[route]['dest_port'] = dest_port
    return test_route_set, test_route_info

test_route_set, test_route_info = get_test_route_set(config.test_data_path)


def get_port_info():
    """ 得到港口数据
            Args:

            Returns：
                port_data (dict):  得到港口数据{'TRANS_NODE_NAME': {'longitude':xx, 'latitude':xx}}

    """
    port_data = {}
    test_port_set = set()
    for route in test_route_set:
        ports = route.split('-')
        test_port_set = set.union(test_port_set, set(ports))
    port_data_origin = pd.read_csv(config.train_port_data_path)
    for item in port_data_origin.itertuples():
        if getattr(item, 'TRANS_NODE_NAME') in test_port_set:
            port_data[getattr(item, 'TRANS_NODE_NAME')] = {'LONGITUDE': getattr(item, 'LONGITUDE'),
                                                           'LATITUDE': getattr(item, 'LATITUDE')}
    return port_data


port_data = get_port_info()


# 给测试集里每个路由创建csv文件,按照路由创建文件名
csv_file = {}
csv_writer = {}
for route in test_route_set:
    route_writer_path = os.path.join(route_order_folder_path, "{}.csv".format(route))
    csv_file[route] = open(route_writer_path, 'w', encoding='utf-8', newline='')
    csv_writer[route] = csv.writer(csv_file[route])

complete_train_chunk = pd.read_csv(complete_train_path, chunksize=2000000, header=None
                                   , names=['loadingOrder', 'timestamp', 'longitude', 'latitude', 'speed',
                                            'TRANSPORT_TRACE'])


# 如果测试集中的路由起止点与训练集的起止点相同，写入完整gps数据
for chunk in tqdm(complete_train_chunk):
    for row in chunk.itertuples(index=False):  # 对到港路由中每条运单的gps数据
        order_route = getattr(row, 'TRANSPORT_TRACE')  # 得到路由
        for test_route, route_info in test_route_info.items():
            if ((route_info['start_port'] in order_route) and (route_info['dest_port'] in order_route)):
                row_info = row._asdict()
                row_info.pop('TRANSPORT_TRACE')
                csv_writer[test_route].writerow(row_info.values())

for k, v in csv_file.items():
    v.close()
