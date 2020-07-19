import numpy as np
import pandas as pd

class Config:
    def __init__(self):
        super().__init__()
        self.data_dir_path = './data/'

        self.test_data_path = self.data_dir_path + 'R2 ATest 0711.csv'  # 测试数据集
        self.train_gps_data_path = self.data_dir_path + 'train0711.csv' # 历史运单GPS
        self.train_port_data_path = self.data_dir_path + 'port.csv'  # 港口坐标数据
        self.train_loadingOrderEvent_data_path = self.data_dir_path + 'loadingOrderEvent.csv'  # 历史运单事件数据
        self.nb_workers = 1
        self.train_data_columns = ['loadingOrder', 'carrierName', 'timestamp', 'longitude',
                      'latitude', 'vesselMMSI', 'speed', 'direction',
                      'vesselNextport', 'vesselNextportETA', 'vesselStatus', 'vesselDataSource', 'TRANSPORT_TRACE']



config = Config()


