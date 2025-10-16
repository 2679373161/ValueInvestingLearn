#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据服务单元测试
"""

import unittest
import tempfile
import os
import json
from datetime import datetime
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.services.data_service import DataService


class TestDataService(unittest.TestCase):
    """数据服务单元测试类"""

    def setUp(self):
        """测试前准备"""
        # 创建临时目录用于测试
        self.temp_dir = tempfile.mkdtemp()
        self.data_dir = os.path.join(self.temp_dir, 'data')
        os.makedirs(self.data_dir, exist_ok=True)

        # 创建测试数据文件
        self.test_macro_data = [
            {
                "date": "2024-01-15",
                "market": "a_share",
                "pmi": 50.5,
                "cpi": 2.1,
                "ppi": 1.8,
                "m2": 8.5,
                "interest_rate": 3.0
            }
        ]

        self.test_sentiment_data = [
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

        # 写入测试数据文件
        with open(os.path.join(self.data_dir, 'macro_data.json'), 'w', encoding='utf-8') as f:
            json.dump(self.test_macro_data, f, ensure_ascii=False, indent=2)

        with open(os.path.join(self.data_dir, 'market_sentiment_data.json'), 'w', encoding='utf-8') as f:
            json.dump(self.test_sentiment_data, f, ensure_ascii=False, indent=2)

        # 创建数据服务实例
        self.data_service = DataService()
        self.data_service.data_dir = self.data_dir

    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_save_macro_data_success(self):
        """测试成功保存宏观数据"""
        new_data = {
            "date": "2024-01-16",
            "market": "a_share",
            "pmi": 51.2,
            "cpi": 2.3,
            "ppi": 1.9,
            "m2": 8.6,
            "interest_rate": 3.1
        }

        result = self.data_service.save_macro_data(new_data)
        self.assertIsInstance(result, dict)
        self.assertIn("id", result)
        self.assertIn("created_at", result)

    def test_get_macro_data(self):
        """测试获取宏观数据"""
        data = self.data_service.get_macro_data("a_share", "2024-01-01", "2024-01-31")
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_save_market_sentiment(self):
        """测试保存市场情绪数据"""
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

        result = self.data_service.save_market_sentiment(new_data)
        self.assertIsInstance(result, dict)
        self.assertIn("id", result)
        self.assertIn("created_at", result)

    def test_get_market_sentiment(self):
        """测试获取市场情绪数据"""
        data = self.data_service.get_market_sentiment("a_share", "2024-01-01", "2024-01-31")
        self.assertIsInstance(data, list)

    def test_save_industry_data(self):
        """测试保存行业数据"""
        new_data = {
            "date": "2024-01-16",
            "market": "a_share",
            "industry": "technology",
            "free_cash_flow": 130.5,
            "industry_sentiment": 75.0
        }

        result = self.data_service.save_industry_data(new_data)
        self.assertIsInstance(result, dict)
        self.assertIn("id", result)
        self.assertIn("created_at", result)

    def test_get_industry_data(self):
        """测试获取行业数据"""
        data = self.data_service.get_industry_data("a_share", "technology", "2024-01-01", "2024-01-31")
        self.assertIsInstance(data, list)

    def test_data_validation(self):
        """测试数据验证"""
        # 测试缺少必需字段的数据
        invalid_data = {
            "date": "2024-01-16",
            # 缺少market字段
            "pmi": 51.2,
            "cpi": 2.3
        }

        with self.assertRaises(ValueError):
            self.data_service.save_macro_data(invalid_data)

    def test_backup_data(self):
        """测试数据备份"""
        result = self.data_service.backup_data()
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()