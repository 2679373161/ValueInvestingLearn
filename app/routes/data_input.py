#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据输入API路由

处理宏观数据、市场情绪数据的手动输入和查询
"""

import logging
from flask import Blueprint, request, jsonify

from ..services.data_service import DataService

# 创建蓝图
data_input_bp = Blueprint('data_input', __name__)
logger = logging.getLogger(__name__)


@data_input_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'service': 'data_input'
    })


@data_input_bp.route('/macro', methods=['POST'])
def add_macro_data():
    """
    添加宏观数据

    Request Body:
    {
        "date": "2024-01-15",
        "market": "a_share",
        "pmi": 50.5,
        "cpi": 2.1,
        "ppi": 1.8,
        "m2": 8.5,
        "interest_rate": 3.0,
        "other_macro": {}
    }
    """
    try:
        data = request.get_json()

        # 数据验证
        required_fields = ['date', 'market']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'缺少必需字段: {field}'
                }), 400

        # 保存数据
        data_service = DataService()
        result = data_service.save_macro_data(data)

        return jsonify({
            'message': '宏观数据保存成功',
            'data': result
        }), 201

    except Exception as e:
        logger.error(f"保存宏观数据失败: {e}")
        return jsonify({
            'error': '保存宏观数据失败',
            'message': str(e)
        }), 500


@data_input_bp.route('/macro', methods=['GET'])
def get_macro_data():
    """
    获取宏观数据

    Query Parameters:
    - market: 市场类型 (a_share, hong_kong, nasdaq)
    - start_date: 开始日期
    - end_date: 结束日期
    """
    try:
        market = request.args.get('market', 'a_share')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        data_service = DataService()
        data = data_service.get_macro_data(market, start_date, end_date)

        return jsonify({
            'data': data,
            'count': len(data)
        })

    except Exception as e:
        logger.error(f"获取宏观数据失败: {e}")
        return jsonify({
            'error': '获取宏观数据失败',
            'message': str(e)
        }), 500


@data_input_bp.route('/market-sentiment', methods=['POST'])
def add_market_sentiment():
    """
    添加市场情绪数据

    Request Body:
    {
        "date": "2024-01-15",
        "market": "a_share",
        "volatility": 15.5,
        "investor_sentiment": 65.0,
        "technical_indicators": {
            "rsi": 55.0,
            "macd": 2.5,
            "bollinger_bands": 1.2
        }
    }
    """
    try:
        data = request.get_json()

        # 数据验证
        required_fields = ['date', 'market']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'缺少必需字段: {field}'
                }), 400

        # 保存数据
        data_service = DataService()
        result = data_service.save_market_sentiment(data)

        return jsonify({
            'message': '市场情绪数据保存成功',
            'data': result
        }), 201

    except Exception as e:
        logger.error(f"保存市场情绪数据失败: {e}")
        return jsonify({
            'error': '保存市场情绪数据失败',
            'message': str(e)
        }), 500


@data_input_bp.route('/market-sentiment', methods=['GET'])
def get_market_sentiment():
    """
    获取市场情绪数据

    Query Parameters:
    - market: 市场类型
    - start_date: 开始日期
    - end_date: 结束日期
    """
    try:
        market = request.args.get('market', 'a_share')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        data_service = DataService()
        data = data_service.get_market_sentiment(market, start_date, end_date)

        return jsonify({
            'data': data,
            'count': len(data)
        })

    except Exception as e:
        logger.error(f"获取市场情绪数据失败: {e}")
        return jsonify({
            'error': '获取市场情绪数据失败',
            'message': str(e)
        }), 500


@data_input_bp.route('/industry', methods=['POST'])
def add_industry_data():
    """
    添加行业基本面数据

    Request Body:
    {
        "date": "2024-01-15",
        "market": "a_share",
        "industry": "technology",
        "free_cash_flow": 120.5,
        "industry_sentiment": 70.0
    }
    """
    try:
        data = request.get_json()

        # 数据验证
        required_fields = ['date', 'market', 'industry']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'缺少必需字段: {field}'
                }), 400

        # 保存数据
        data_service = DataService()
        result = data_service.save_industry_data(data)

        return jsonify({
            'message': '行业数据保存成功',
            'data': result
        }), 201

    except Exception as e:
        logger.error(f"保存行业数据失败: {e}")
        return jsonify({
            'error': '保存行业数据失败',
            'message': str(e)
        }), 500


@data_input_bp.route('/industry', methods=['GET'])
def get_industry_data():
    """
    获取行业基本面数据

    Query Parameters:
    - market: 市场类型
    - industry: 行业类型
    - start_date: 开始日期
    - end_date: 结束日期
    """
    try:
        market = request.args.get('market', 'a_share')
        industry = request.args.get('industry')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        data_service = DataService()
        data = data_service.get_industry_data(market, industry, start_date, end_date)

        return jsonify({
            'data': data,
            'count': len(data)
        })

    except Exception as e:
        logger.error(f"获取行业数据失败: {e}")
        return jsonify({
            'error': '获取行业数据失败',
            'message': str(e)
        }), 500