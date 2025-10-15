#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化择时指标应用 - 主应用文件

基于多维度择时框架的量化分析工具
"""

import os
import sys
from . import create_app


def main():
    """主应用入口"""
    try:
        app = create_app()

        # 获取配置
        from .utils.config import config_manager
        host = config_manager.get('server.host', '0.0.0.0')
        port = config_manager.get('server.port', 5000)
        debug = config_manager.get('app.debug', False)

        print(f"启动量化择时指标应用...")
        print(f"服务地址: http://{host}:{port}")
        print(f"调试模式: {debug}")

        app.run(host=host, port=port, debug=debug)

    except Exception as e:
        print(f"应用启动失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()