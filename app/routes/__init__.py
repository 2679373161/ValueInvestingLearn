#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API路由模块

包含数据输入、分析和可视化相关的API端点
"""

from .data_input import data_input_bp
from .analysis import analysis_bp
from .visualization import visualization_bp

__all__ = ['data_input_bp', 'analysis_bp', 'visualization_bp']