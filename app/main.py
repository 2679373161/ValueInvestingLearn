#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化择时指标应用 - 主应用文件

基于多维度择时框架的量化分析工具
"""

import os
from flask import Flask


def create_app():
    """创建Flask应用实例"""
    app = Flask(__name__)

    # 基础配置
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['DEBUG'] = os.environ.get('DEBUG', True)

    # 注册蓝图和路由
    from .routes import data_input, analysis, visualization
    app.register_blueprint(data_input.bp)
    app.register_blueprint(analysis.bp)
    app.register_blueprint(visualization.bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)