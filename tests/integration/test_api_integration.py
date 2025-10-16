#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API集成测试
"""

import unittest
import tempfile
import os
import json
from datetime import datetime

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app import create_app


class TestAPIIntegration(unittest.TestCase):
    """API集成测试类"""

    def setUp(self):
        """测试前准备"""
        # 创建临时目录用于测试
        self.temp_dir = tempfile.mkdtemp()
        self.data_dir = os.path.join(self.temp_dir, 'data')
        os.makedirs(self.data_dir, exist_ok=True)

        # 设置环境变量
        os.environ['DATA_DIR'] = self.data_dir

        # 创建测试应用
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        # 创建测试数据文件
        self._create_test_data()

    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def _create_test_data(self):
        """创建测试数据"""
        # 宏观数据
        macro_data = [
            {
                "date": "2024-01-15",
                "market": "a_share",
                "pmi": 50.5,
                "cpi": 2.1,
                "ppi": 1.8,
                "m2": 8.5,
                "interest_rate": 3.0
            },
            {
                "date": "2024-01-16",
                "market": "a_share",
                "pmi": 51.2,
                "cpi": 2.3,
                "ppi": 1.9,
                "m2": 8.6,
                "interest_rate": 3.1
            }
        ]

        # 市场情绪数据
        sentiment_data = [
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
        ]

        # 行业数据
        industry_data = [
            {
                "date": "2024-01-15",
                "market": "a_share",
                "industry": "technology",
                "free_cash_flow": 120.5,
                "industry_sentiment": 70.0
            }
        ]

        # 写入测试数据文件
        with open(os.path.join(self.data_dir, 'macro_data.json'), 'w', encoding='utf-8') as f:
            json.dump(macro_data, f, ensure_ascii=False, indent=2)

        with open(os.path.join(self.data_dir, 'market_sentiment_data.json'), 'w', encoding='utf-8') as f:
            json.dump(sentiment_data, f, ensure_ascii=False, indent=2)

        with open(os.path.join(self.data_dir, 'industry_data.json'), 'w', encoding='utf-8') as f:
            json.dump(industry_data, f, ensure_ascii=False, indent=2)

    def test_health_endpoint(self):
        """测试健康检查端点"""
        response = self.client.get('/api/data/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')

    def test_api_docs_endpoint(self):
        """测试API文档端点"""
        response = self.client.get('/api/docs')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('title', data)
        self.assertIn('version', data)
        self.assertIn('endpoints', data)

    def test_add_macro_data(self):
        """测试添加宏观数据"""
        new_data = {
            "date": "2024-01-17",
            "market": "a_share",
            "pmi": 52.1,
            "cpi": 2.4,
            "ppi": 2.0,
            "m2": 8.7,
            "interest_rate": 3.2
        }

        response = self.client.post('/api/data/macro', json=new_data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['message'], '宏观数据添加成功')

    def test_get_macro_data(self):
        """测试获取宏观数据"""
        response = self.client.get('/api/data/macro?market=a_share&start_date=2024-01-01&end_date=2024-01-31')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_add_market_sentiment_data(self):
        """测试添加市场情绪数据"""
        new_data = {
            "date": "2024-01-16",
            "market": "a_share",
            "volatility": 16.2,
            "investor_sentiment": 68.0,
            "technical_indicators": {
                "rsi": 58.0,
                "macd": 2.8,
                "bollinger_bands": 1.3
            }
        }

        response = self.client.post('/api/data/market-sentiment', json=new_data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['message'], '市场情绪数据添加成功')

    def test_add_industry_data(self):
        """测试添加行业数据"""
        new_data = {
            "date": "2024-01-16",
            "market": "a_share",
            "industry": "finance",
            "free_cash_flow": 150.2,
            "industry_sentiment": 75.0
        }

        response = self.client.post('/api/data/industry', json=new_data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['message'], '行业数据添加成功')

    def test_calculate_timing_indicators(self):
        """测试计算择时指标"""
        request_data = {
            "market": "a_share",
            "date": "2024-01-15"
        }

        response = self.client.post('/api/analysis/timing-indicators', json=request_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertIn('timing_score', data)
        self.assertIn('indicators', data)

        indicators = data['indicators']
        self.assertIn('macro', indicators)
        self.assertIn('industry', indicators)
        self.assertIn('sentiment', indicators)

    def test_get_ai_analysis(self):
        """测试获取AI分析"""
        request_data = {
            "market": "a_share",
            "timing_indicators": {
                "macro_score": 85,
                "industry_score": 72,
                "sentiment_score": 77
            }
        }

        response = self.client.post('/api/analysis/ai-analysis', json=request_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertIn('summary', data)
        self.assertIn('recommendations', data)
        self.assertIn('risk_level', data)

    def test_calculate_position_sizing(self):
        """测试计算仓位配置"""
        request_data = {
            "market": "a_share",
            "timing_score": 78,
            "risk_tolerance": "中等"
        }

        response = self.client.post('/api/analysis/position-sizing', json=request_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertIn('suggested_position', data)
        self.assertIn('max_position', data)
        self.assertIn('min_position', data)
        self.assertIn('allocation', data)

    def test_get_market_comparison(self):
        """测试获取市场比较"""
        response = self.client.get('/api/analysis/market-comparison')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertIn('a_share', data)
        self.assertIn('hong_kong', data)
        self.assertIn('nasdaq', data)

    def test_get_analysis_summary(self):
        """测试获取分析摘要"""
        response = self.client.get('/api/analysis/summary?market=a_share&date=2024-01-15')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertIn('market', data)
        self.assertIn('date', data)
        self.assertIn('timing_score', data)

    def test_get_timing_score_trend(self):
        """测试获取择时评分趋势"""
        response = self.client.get('/api/visualization/timing-score-trend?market=a_share&start_date=2024-01-01&end_date=2024-01-31')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertIsInstance(data, list)

    def test_error_handling(self):
        """测试错误处理"""
        # 测试无效的请求数据
        invalid_data = {
            "date": "2024-01-15",
            "market": "a_share"
            # 缺少必需的字段
        }

        response = self.client.post('/api/data/macro', json=invalid_data)
        self.assertEqual(response.status_code, 400)

        # 测试不存在的端点
        response = self.client.get('/api/nonexistent')
        self.assertEqual(response.status_code, 404)

    def test_data_validation(self):
        """测试数据验证"""
        # 测试超出范围的数值
        invalid_data = {
            "date": "2024-01-15",
            "market": "a_share",
            "pmi": 200,  # 超出合理范围
            "cpi": 2.1,
            "ppi": 1.8,
            "m2": 8.5,
            "interest_rate": 3.0
        }

        response = self.client.post('/api/data/macro', json=invalid_data)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()