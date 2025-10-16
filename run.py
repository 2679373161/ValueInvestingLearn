#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化择时指标应用 - 启动脚本

基于多维度择时框架的量化分析工具
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import main

if __name__ == '__main__':
    main()