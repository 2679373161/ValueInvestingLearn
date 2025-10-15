#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析API路由

处理择时指标计算和AI分析
"""

import logging
from flask import Blueprint, request, jsonify

from ..services.indicator_service import IndicatorService
from ..services.ai_service import AIService

# 创建蓝图
analysis_bp = Blueprint('analysis', __name__)
logger = logging.getLogger(__name__)


@analysis_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'service': 'analysis'
    })


@analysis_bp.route('/timing-indicators', methods=['POST'])
def calculate_timing_indicators():
    """
    计算择时指标

    Request Body:
    {
        "market": "a_share",
        "date": "2024-01-15",
        "macro_data": {...},
        "industry_data": {...},
        "market_sentiment": {...}
    }
    """
    try:
        data = request.get_json()

        # 数据验证
        required_fields = ['market', 'date']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'缺少必需字段: {field}'
                }), 400

        # 计算指标
        indicator_service = IndicatorService()
        result = indicator_service.calculate_timing_indicators(data)

        return jsonify({
            'message': '择时指标计算成功',
            'data': result
        })

    except Exception as e:
        logger.error(f"计算择时指标失败: {e}")
        return jsonify({
            'error': '计算择时指标失败',
            'message': str(e)
        }), 500


@analysis_bp.route('/timing-indicators', methods=['GET'])
def get_timing_indicators():
    """
    获取择时指标历史数据

    Query Parameters:
    - market: 市场类型
    - start_date: 开始日期
    - end_date: 结束日期
    """
    try:
        market = request.args.get('market', 'a_share')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        indicator_service = IndicatorService()
        data = indicator_service.get_timing_indicators(market, start_date, end_date)

        return jsonify({
            'data': data,
            'count': len(data)
        })

    except Exception as e:
        logger.error(f"获取择时指标失败: {e}")
        return jsonify({
            'error': '获取择时指标失败',
            'message': str(e)
        }), 500


@analysis_bp.route('/ai-analysis', methods=['POST'])
def get_ai_analysis():
    """
    获取AI分析结果

    Request Body:
    {
        "market": "a_share",
        "date": "2024-01-15",
        "timing_indicators": {...},
        "include_position_sizing": true
    }
    """
    try:
        data = request.get_json()

        # 数据验证
        required_fields = ['market', 'date']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'缺少必需字段: {field}'
                }), 400

        # 获取AI分析
        ai_service = AIService()
        result = ai_service.analyze_timing_indicators(data)

        return jsonify({
            'message': 'AI分析成功',
            'data': result
        })

    except Exception as e:
        logger.error(f"获取AI分析失败: {e}")
        return jsonify({
            'error': '获取AI分析失败',
            'message': str(e)
        }), 500


@analysis_bp.route('/position-sizing', methods=['POST'])
def calculate_position_sizing():
    """
    计算仓位建议

    Request Body:
    {
        "market": "a_share",
        "date": "2024-01-15",
        "timing_score": 75.5,
        "available_capital": 100000,
        "risk_per_trade_percentage": 2
    }
    """
    try:
        data = request.get_json()

        # 数据验证
        required_fields = ['market', 'date', 'timing_score']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'缺少必需字段: {field}'
                }), 400

        # 计算仓位
        indicator_service = IndicatorService()
        result = indicator_service.calculate_position_sizing(data)

        return jsonify({
            'message': '仓位计算成功',
            'data': result
        })

    except Exception as e:
        logger.error(f"计算仓位失败: {e}")
        return jsonify({
            'error': '计算仓位失败',
            'message': str(e)
        }), 500


@analysis_bp.route('/market-comparison', methods=['GET'])
def compare_markets():
    """
    多市场比较分析

    Query Parameters:
    - date: 分析日期
    - markets: 市场列表，逗号分隔 (a_share,hong_kong,nasdaq)
    """
    try:
        date = request.args.get('date')
        markets = request.args.get('markets', 'a_share,hong_kong,nasdaq').split(',')

        indicator_service = IndicatorService()
        result = indicator_service.compare_markets(markets, date)

        return jsonify({
            'message': '市场比较分析成功',
            'data': result
        })

    except Exception as e:
        logger.error(f"市场比较分析失败: {e}")
        return jsonify({
            'error': '市场比较分析失败',
            'message': str(e)
        }), 500


@analysis_bp.route('/summary', methods=['GET'])
def get_analysis_summary():
    """
    获取分析摘要

    Query Parameters:
    - market: 市场类型
    - date: 分析日期
    """
    try:
        market = request.args.get('market', 'a_share')
        date = request.args.get('date')

        indicator_service = IndicatorService()
        summary = indicator_service.get_analysis_summary(market, date)

        return jsonify({
            'message': '分析摘要获取成功',
            'data': summary
        })

    except Exception as e:
        logger.error(f"获取分析摘要失败: {e}")
        return jsonify({
            'error': '获取分析摘要失败',
            'message': str(e)
        }), 500