#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具模块

包含配置管理、计算工具等辅助功能
"""

from .config import config_manager, init_config
from .calculations import (
    normalize_score,
    calculate_weighted_average,
    linear_interpolation
)

__all__ = [
    'config_manager',
    'init_config',
    'normalize_score',
    'calculate_weighted_average',
    'linear_interpolation'
]