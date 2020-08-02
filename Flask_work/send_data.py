#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import os
from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
from flask_cors import CORS
from threading import Timer
import time
import numpy as np
import pandas as pd

# 50, 55, 55, 59, 56, 44, 66, 54, 52, 53
# 实例化app对象
app = Flask(__name__)
CORS(app, resources=r'/*')

# 处理gps数据
gps_folder_path = 'gps/'
fileList = os.listdir(gps_folder_path)
all_gps_data = []
for file in fileList:
    path = os.path.join(gps_folder_path, file)
    file_base = os.path.basename(path).split('.')[0]
    arr = file_base.split('_')
    order = arr[0]
    data = pd.read_csv(path, usecols=[1, 2])
    value = data.values
    row = data.shape[0]
    col = data.shape[1]
    trajectory = []
    for i in range(row):
        if col == 1:
            continue
        if i == 0:
            trajectory.append(value[0][0])
            trajectory.append(value[0][1])
        elif value[i][0]-value[i-1][0] != 0 and value[i][1]-value[i-1][1] != 0:
            trajectory.append(value[i][0]-value[i-1][0])
            trajectory.append(value[i][1]-value[i-1][1])
    if trajectory:
        all_gps_data.append(trajectory)


@app.route('/res_data/gps', methods=['GET', 'POST'])
def send_car():
    return json.dumps(all_gps_data)




if __name__ == '__main__':
    # main()
    app.run(host='0.0.0.0',  # 任何ip都可以访问
            port=5000,  # 端口
            debug=True
            )
