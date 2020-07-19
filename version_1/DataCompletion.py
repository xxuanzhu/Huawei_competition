import pandas as pd
import numpy as np
from tqdm import tqdm
import csv
from Config import config

order_route_path = './data/order_route_train.csv'
complete_train_path = './data/complete_train.csv'


def get_test_route_set(path):
    """得到测试集的路径数据
            Args:
                path: 测试集路径

            Returns：
                test_route_set (dict): 非重复的船的路由

        """
    data = pd.read_csv(path)
    test_route_set = data['TRANSPORT_TRACE'].unique()
    return test_route_set


test_route_set = get_test_route_set(config.test_data_path)  # 读取测试数据路由


def get_port_info():
    """ 得到港口数据
                Args:

                Returns：
                    port_data (dict):  得到港口数据{'TRANS_NODE_NAME': {'longitude':xx, 'latitude':xx}}

        """
    port_data = {}
    test_port_set = set()  # set()创建一个无序不重复元素集
    for route in test_route_set:
        ports = route.split('-')
        test_port_set = set.union(test_port_set, set(ports))
    port_data_origin = pd.read_csv(config.train_port_data_path)
    for item in port_data_origin.itertuples():
        # 如果这个港口名在测试数据里，则加入port_data（name，longitude，latitude）
        if getattr(item, 'TRANS_NODE_NAME') in test_port_set:  # getattr() 函数用于返回一个对象属性值。
            port_data[getattr(item, 'TRANS_NODE_NAME')] = {'LONGITUDE': getattr(item, 'LONGITUDE'),
                                                           'LATITUDE': getattr(item, 'LATITUDE')}
    return port_data


# 存着在测试数据中出现的港口数据({name:longitude,latitude)
port_data = get_port_info()

order_route = {}
train_data_origin_chunk = pd.read_csv(config.train_gps_data_path, chunksize=2000000,
                                      usecols=[0, 1, 2, 3, 4, 5, 6, 7, 12], header=None,
                                      names=['loadingOrder', 'carrierName', 'timestamp', 'longitude', 'latitude',
                                             'vesselMMSI', 'speed', 'direction', 'TRANSPORT_TRACE'])

# 生成训练数据中的运单港口路由
for chunk in tqdm(train_data_origin_chunk):
    for row in chunk.itertuples(index=False):  # 对每个gps数据
        for (port, port_info) in port_data.items():  # 对测试集中的每个港口数据
            if abs(row[3] - port_info['LONGITUDE']) < 0.3 and abs(
                    row[4] - port_info['LATITUDE']) < 0.3:  # 如果此条gps数据的经纬度经纬度漂移相差小于0.3，说明到港
                if (not row[0] in order_route):  # 这条gps数据所属的运单号还没有出现在列表内，添加此运单
                    order_route[row[0]] = []
                if (not port in order_route[row[0]]):  # 这个港口不在此运单中，添加此港口
                    order_route[row[0]].append(port)

with open(order_route_path, 'w', encoding='utf-8', newline='') as f:
    csv_writer = csv.writer(f)
    for (order, order_info) in order_route.items():
        if (len(order_info) == 1):
            continue
        csv_writer.writerow([order, '-'.join(order_info)])

print('- write csv done -')

train_data_origin_chunk = pd.read_csv(config.train_gps_data_path, chunksize=2000000, usecols=[0, 1, 2, 3, 4, 6, 7, 12],
                                      header=None,
                                      names=['loadingOrder', 'carrierName', 'timestamp', 'longitude', 'latitude',
                                             'speed', 'direction',
                                             'TRANSPORT_TRACE'])

# 生成完整的训练集的运单路径
with open(complete_train_path, 'w', encoding='utf-8', newline='') as f:
    csv_writer = csv.writer(f)
    for chunk in tqdm(train_data_origin_chunk):  # 对每条gps数据
        for row in chunk.itertuples(index=False):
            if (row[0] in order_route):  # 如果此运单号在运单路由里
                if row[6] == -1:
                    continue
                if (len(order_route[row[0]]) < 0):
                    continue
                edit_line = row._asdict()  # 将一个namedtuple对象转换为一个orderdict字典
                edit_line.pop('direction')
                edit_line['TRANSPORT_TRACE'] = '-'.join(order_route[row[0]])  # 接上对应运单号的路由
                list_values = [i for i in edit_line.values()]
                csv_writer.writerow(list_values)
