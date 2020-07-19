from math import radians, cos, sin, asin, sqrt
import pandas as pd
from Config import config
import json
import os

def Harversine(lon1, lat1, lon2, lat2):
    """计算两个经纬度坐标之间的距离

    Args:
        lon1 (float):
        lat1 (float):
        lon2 (float):
        lat2 (float):

    Returns:
        distance: 距离
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # Haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    d = c * r
    return d

def get_port_info(test_path):
    """ 得到港口数据
                Args:

                Returns：
                    port_data (dict):  得到港口数据{'TRANS_NODE_NAME': {'longitude':xx, 'latitude':xx}}

        """

    data = pd.read_csv(test_path)
    test_route_set = data['TRANSPORT_TRACE'].unique()
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


class SaveJson(object):

    def save_file(self, path, item):

        # 先将字典对象转化为可写入文本的字符串
        item = json.dumps(item)

        try:
            if not os.path.exists(path):
                with open(path, "w", encoding='utf-8') as f:
                    f.write(item + ",\n")
                    print("^_^ write success")
            else:
                with open(path, "a", encoding='utf-8') as f:
                    f.write(item + ",\n")
                    print("^_^ write success")
        except Exception as e:
            print("write error==>", e)


