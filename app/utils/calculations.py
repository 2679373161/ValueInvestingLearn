#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
计算工具模块

包含各种数学计算和数据处理工具
"""

import math
from typing import List, Dict, Any, Optional


def normalize_score(value: float, min_val: float, max_val: float, reverse: bool = False) -> float:
    """
    归一化评分

    Args:
        value: 原始值
        min_val: 最小值
        max_val: 最大值
        reverse: 是否反向（值越小越好）

    Returns:
        float: 归一化后的评分（0-100）
    """
    if min_val == max_val:
        return 50.0  # 默认中性评分

    if reverse:
        # 值越小越好
        normalized = (max_val - value) / (max_val - min_val)
    else:
        # 值越大越好
        normalized = (value - min_val) / (max_val - min_val)

    # 限制在0-1范围内
    normalized = max(0.0, min(1.0, normalized))

    # 转换为0-100评分
    return normalized * 100


def calculate_weighted_average(scores: List[float], weights: List[float]) -> float:
    """
    计算加权平均值

    Args:
        scores: 评分列表
        weights: 权重列表

    Returns:
        float: 加权平均分
    """
    if len(scores) != len(weights):
        raise ValueError("评分和权重列表长度必须相同")

    if not scores:
        return 0.0

    total_weight = sum(weights)
    if total_weight == 0:
        return sum(scores) / len(scores) if scores else 0.0

    weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
    return weighted_sum / total_weight


def linear_interpolation(value: float, x1: float, y1: float, x2: float, y2: float) -> float:
    """
    线性插值

    Args:
        value: 输入值
        x1, y1: 第一个点的坐标
        x2, y2: 第二个点的坐标

    Returns:
        float: 插值结果
    """
    if x1 == x2:
        return (y1 + y2) / 2

    return y1 + (value - x1) * (y2 - y1) / (x2 - x1)


def calculate_volatility_score(volatility: float) -> float:
    """
    计算波动率评分

    Args:
        volatility: 波动率值

    Returns:
        float: 波动率评分（0-100）
    """
    # 波动率越低越好
    if volatility <= 10:
        return 100.0
    elif volatility >= 30:
        return 0.0
    else:
        return linear_interpolation(volatility, 10, 100, 30, 0)


def calculate_technical_score(indicators: Dict[str, Any]) -> float:
    """
    计算技术指标综合评分

    Args:
        indicators: 技术指标字典

    Returns:
        float: 技术指标评分（0-100）
    """
    score = 50.0  # 基础评分

    # RSI评分
    rsi = indicators.get('rsi')
    if rsi is not None:
        if 30 <= rsi <= 70:
            score += 20  # RSI在合理区间
        elif rsi < 30 or rsi > 70:
            score -= 20  # RSI超买或超卖

    # MACD评分
    macd = indicators.get('macd')
    if macd is not None:
        if macd > 0:
            score += 15  # MACD为正，看涨信号
        else:
            score -= 15  # MACD为负，看跌信号

    # 布林带评分
    bollinger = indicators.get('bollinger_bands')
    if bollinger is not None:
        if abs(bollinger) <= 1:
            score += 15  # 价格在布林带内
        else:
            score -= 15  # 价格触及布林带边界

    # 确保评分在0-100范围内
    return max(0, min(100, score))


def calculate_position_size(timing_score: float, available_capital: float,
                          position_sizes: Dict[str, float]) -> Dict[str, float]:
    """
    计算仓位大小

    Args:
        timing_score: 择时评分
        available_capital: 可用资金
        position_sizes: 仓位配置字典

    Returns:
        Dict[str, float]: 仓位计算结果
    """
    # 确定强度等级
    strength_level = _get_strength_level(timing_score)

    # 获取仓位比例
    position_percentage = position_sizes.get(strength_level, 0)

    # 计算仓位金额
    position_amount = (position_percentage / 100) * available_capital

    return {
        'strength_level': strength_level,
        'position_percentage': position_percentage,
        'position_amount': position_amount
    }


def _get_strength_level(score: float) -> str:
    """
    获取择时强度等级

    Args:
        score: 择时评分

    Returns:
        str: 强度等级
    """
    if score >= 80:
        return 'very_strong'
    elif score >= 60:
        return 'strong'
    elif score >= 40:
        return 'neutral'
    elif score >= 20:
        return 'weak'
    else:
        return 'very_weak'


def calculate_risk_amount(available_capital: float, risk_percentage: float) -> float:
    """
    计算单笔风险金额

    Args:
        available_capital: 可用资金
        risk_percentage: 风险百分比

    Returns:
        float: 风险金额
    """
    return (risk_percentage / 100) * available_capital


def smooth_data(data: List[float], window_size: int = 3) -> List[float]:
    """
    数据平滑处理（移动平均）

    Args:
        data: 原始数据列表
        window_size: 窗口大小

    Returns:
        List[float]: 平滑后的数据
    """
    if len(data) < window_size:
        return data

    smoothed = []
    for i in range(len(data)):
        start = max(0, i - window_size + 1)
        end = i + 1
        window_data = data[start:end]
        smoothed.append(sum(window_data) / len(window_data))

    return smoothed


def calculate_correlation(x: List[float], y: List[float]) -> float:
    """
    计算两个序列的相关系数

    Args:
        x: 第一个序列
        y: 第二个序列

    Returns:
        float: 相关系数（-1到1）
    """
    if len(x) != len(y):
        raise ValueError("两个序列长度必须相同")

    n = len(x)
    if n < 2:
        return 0.0

    # 计算均值
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    # 计算协方差和标准差
    covariance = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x))
    std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y))

    if std_x == 0 or std_y == 0:
        return 0.0

    return covariance / (std_x * std_y)


def normalize_weights(weights: Dict[str, float]) -> Dict[str, float]:
    """
    归一化权重

    Args:
        weights: 原始权重字典

    Returns:
        Dict[str, float]: 归一化后的权重
    """
    total = sum(weights.values())
    if total == 0:
        return weights

    return {key: value / total for key, value in weights.items()}


def calculate_composite_score(scores: Dict[str, float], weights: Dict[str, float]) -> float:
    """
    计算综合评分

    Args:
        scores: 各维度评分
        weights: 各维度权重

    Returns:
        float: 综合评分
    """
    # 归一化权重
    normalized_weights = normalize_weights(weights)

    # 计算加权平均
    total_score = 0.0
    total_weight = 0.0

    for dimension, score in scores.items():
        weight = normalized_weights.get(dimension, 0.0)
        total_score += score * weight
        total_weight += weight

    if total_weight == 0:
        return 0.0

    return total_score / total_weight