#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化择时指标应用

主应用模块初始化
"""

import logging
from typing import List
from flask import Flask
from flask_cors import CORS

from .utils.config import init_config, config_manager


def create_app():
    """
    创建Flask应用实例

    Returns:
        Flask: Flask应用实例
    """
    app = Flask(__name__)

    # 初始化配置
    if not init_config():
        raise RuntimeError("配置初始化失败")

    # 应用配置
    app.config['SECRET_KEY'] = config_manager.get('app.secret_key')
    app.config['DEBUG'] = config_manager.get('app.debug', False)

    # 启用CORS
    cors_origins = config_manager.get('server.cors_origins', [])
    CORS(app, origins=cors_origins)

    # 配置日志
    _setup_logging()

    # 注册蓝图
    _register_blueprints(app)

    # 注册错误处理器
    _register_error_handlers(app)

    # 添加API文档端点
    _add_api_docs(app)

    return app


def _setup_logging():
    """配置日志系统"""
    log_config = config_manager.get('logging', {})
    log_level = getattr(logging, log_config.get('level', 'INFO'))

    # 只使用控制台日志，避免文件权限问题
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )


def _register_blueprints(app):
    """注册蓝图"""
    from .routes.data_input import data_input_bp
    from .routes.analysis import analysis_bp
    from .routes.visualization import visualization_bp

    app.register_blueprint(data_input_bp, url_prefix='/api/data')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(visualization_bp, url_prefix='/api/visualization')


def _register_error_handlers(app):
    """注册错误处理器"""

    @app.errorhandler(404)
    def not_found(error):
        return {
            'error': '资源未找到',
            'message': str(error)
        }, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {
            'error': '服务器内部错误',
            'message': '请稍后重试'
        }, 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f"未处理的异常: {error}")
        return {
            'error': '服务器错误',
            'message': '发生未知错误'
        }, 500


def _add_api_docs(app):
    """添加API文档端点"""

    @app.route('/api/docs')
    def api_docs():
        """API文档页面"""
        return {
            'title': '量化择时指标应用 API',
            'version': '1.0.0',
            'description': '基于多维度择时框架的量化分析工具API',
            'endpoints': {
                'data': {
                    'macro': '/api/data/macro',
                    'market_sentiment': '/api/data/market-sentiment',
                    'industry': '/api/data/industry',
                    'health': '/api/data/health'
                },
                'analysis': {
                    'timing_indicators': '/api/analysis/timing-indicators',
                    'ai_analysis': '/api/analysis/ai-analysis',
                    'position_sizing': '/api/analysis/position-sizing',
                    'market_comparison': '/api/analysis/market-comparison',
                    'summary': '/api/analysis/summary',
                    'health': '/api/analysis/health'
                },
                'visualization': {
                    'timing_score_trend': '/api/visualization/timing-score-trend',
                    'market_comparison_chart': '/api/visualization/market-comparison-chart',
                    'indicator_breakdown': '/api/visualization/indicator-breakdown',
                    'position_sizing_chart': '/api/visualization/position-sizing-chart',
                    'sentiment_analysis': '/api/visualization/sentiment-analysis',
                    'macro_indicators': '/api/visualization/macro-indicators',
                    'dashboard_summary': '/api/visualization/dashboard-summary',
                    'health': '/api/visualization/health'
                }
            }
        }