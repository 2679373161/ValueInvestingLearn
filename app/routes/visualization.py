#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可视化API路由

处理图表数据和可视化配置
"""

import logging
from flask import Blueprint, request, jsonify

from ..services.indicator_service import IndicatorService

# 创建蓝图
visualization_bp = Blueprint('visualization', __name__)
logger = logging.getLogger(__name__)


@visualization_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'service': 'visualization'
    })


@visualization_bp.route('/timing-score-trend', methods=['GET'])
def get_timing_score_trend():
    """
    获取择时评分趋势数据

    Query Parameters:
    - market: 市场类型
    - start_date: 开始日期
    - end_date: 结束日期
    - indicator_type: 指标类型 (overall, macro, industry, sentiment)
    """
    try:
        market = request.args.get('market', 'a_share')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        indicator_type = request.args.get('indicator_type', 'overall')

        indicator_service = IndicatorService()
        data = indicator_service.get_timing_score_trend(
            market, start_date, end_date, indicator_type
        )

        return jsonify({
            'data': data,
            'count': len(data)
        })

    except Exception as e:
        logger.error(f"获取择时评分趋势失败: {e}")
        return jsonify({
            'error': '获取择时评分趋势失败',
            'message': str(e)
        }), 500


@visualization_bp.route('/market-comparison-chart', methods=['GET'])
def get_market_comparison_chart():
    """
    获取市场比较图表数据

    Query Parameters:
    - date: 分析日期
    - markets: 市场列表，逗号分隔
    - indicators: 指标列表，逗号分隔
    """
    try:
        date = request.args.get('date')
        markets = request.args.get('markets', 'a_share,hong_kong,nasdaq').split(',')
        indicators = request.args.get('indicators', 'overall_score,macro_score,industry_score,sentiment_score').split(',')

        indicator_service = IndicatorService()
        data = indicator_service.get_market_comparison_data(
            markets, date, indicators
        )

        return jsonify({
            'data': data,
            'markets': markets,
            'indicators': indicators
        })

    except Exception as e:
        logger.error(f"获取市场比较图表数据失败: {e}")
        return jsonify({
            'error': '获取市场比较图表数据失败',
            'message': str(e)
        }), 500


@visualization_bp.route('/indicator-breakdown', methods=['GET'])
def get_indicator_breakdown():
    """
    获取指标分解数据

    Query Parameters:
    - market: 市场类型
    - date: 分析日期
    """
    try:
        market = request.args.get('market', 'a_share')
        date = request.args.get('date')

        indicator_service = IndicatorService()
        data = indicator_service.get_indicator_breakdown(market, date)

        return jsonify({
            'data': data
        })

    except Exception as e:
        logger.error(f"获取指标分解数据失败: {e}")
        return jsonify({
            'error': '获取指标分解数据失败',
            'message': str(e)
        }), 500


@visualization_bp.route('/position-sizing-chart', methods=['GET'])
def get_position_sizing_chart():
    """
    获取仓位配置图表数据

    Query Parameters:
    - market: 市场类型
    - date: 分析日期
    - available_capital: 可用资金
    """
    try:
        market = request.args.get('market', 'a_share')
        date = request.args.get('date')
        available_capital = request.args.get('available_capital', 100000)

        indicator_service = IndicatorService()
        data = indicator_service.get_position_sizing_chart_data(
            market, date, float(available_capital)
        )

        return jsonify({
            'data': data
        })

    except Exception as e:
        logger.error(f"获取仓位配置图表数据失败: {e}")
        return jsonify({
            'error': '获取仓位配置图表数据失败',
            'message': str(e)
        }), 500


@visualization_bp.route('/sentiment-analysis', methods=['GET'])
def get_sentiment_analysis():
    """
    获取市场情绪分析数据

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
        data = indicator_service.get_sentiment_analysis_data(
            market, start_date, end_date
        )

        return jsonify({
            'data': data
        })

    except Exception as e:
        logger.error(f"获取市场情绪分析数据失败: {e}")
        return jsonify({
            'error': '获取市场情绪分析数据失败',
            'message': str(e)
        }), 500


@visualization_bp.route('/macro-indicators', methods=['GET'])
def get_macro_indicators():
    """
    获取宏观指标数据

    Query Parameters:
    - market: 市场类型
    - start_date: 开始日期
    - end_date: 结束日期
    """
    try:
        market = request.args.get('market', 'a_share')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        from ..services.data_service import DataService
        data_service = DataService()
        data = data_service.get_macro_data(market, start_date, end_date)

        return jsonify({
            'data': data,
            'count': len(data)
        })

    except Exception as e:
        logger.error(f"获取宏观指标数据失败: {e}")
        return jsonify({
            'error': '获取宏观指标数据失败',
            'message': str(e)
        }), 500


@visualization_bp.route('/dashboard-summary', methods=['GET'])
def get_dashboard_summary():
    """
    获取仪表盘摘要数据

    Query Parameters:
    - market: 市场类型
    - date: 分析日期
    """
    try:
        market = request.args.get('market', 'a_share')
        date = request.args.get('date')

        indicator_service = IndicatorService()
        summary = indicator_service.get_dashboard_summary(market, date)

        return jsonify({
            'data': summary
        })

    except Exception as e:
        logger.error(f"获取仪表盘摘要数据失败: {e}")
        return jsonify({
            'error': '获取仪表盘摘要数据失败',
            'message': str(e)
        }), 500