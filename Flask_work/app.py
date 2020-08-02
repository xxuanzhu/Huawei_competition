#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
from flask import Flask, jsonify, render_template, request
import json

from flask_cors import CORS

# 实例化app对象
app = Flask(__name__)
CORS(app, resources=r'/*')

state_matrix = np.array(
    [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
        [17, 18, 19, 20],
        [21, 22, 23, 14],
        [25, 26, 27, 28],
        [29, 30, 31, 32],
        [33, 34, 35, 36],
        [37, 38, 39, 40]])


@app.route('/res_data/compare', methods=['POST', 'GET'])
def app_index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',  # 任何ip都可以访问
            port=5000,  # 端口
            debug=True)
