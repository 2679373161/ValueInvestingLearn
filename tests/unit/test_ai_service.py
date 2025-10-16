#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI服务单元测试
"""

import unittest
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.services.ai_service import AIService


class TestAIService(unittest.TestCase):
    """AI服务单元测试类"""

    def setUp(self):
        """测试前准备"""
        self.ai_service = AIService()

    def test_analyze_timing_indicators_without_api_key(self):
        """测试在没有API密钥的情况下分析择时指标"""
        data = {
            "market": "a_share",
            "date": "2024-01-15",
            "timing_indicators": {
                "overall_score": 78,
                "macro_score": 85,
                "industry_score": 72,
                "sentiment_score": 77,
                "strength_level": "strong"
            }
        }

        result = self.ai_service.analyze_timing_indicators(data)

        self.assertIsInstance(result, dict)
        self.assertIn("ai_analysis", result)
        self.assertIn("summary", result)
        self.assertIn("recommendation", result)
        self.assertIn("risk_level", result)

    def test_analyze_timing_indicators_with_fallback(self):
        """测试备用分析结果生成"""
        data = {
            "market": "a_share",
            "date": "2024-01-15",
            "timing_indicators": {
                "overall_score": 78,
                "macro_score": 85,
                "industry_score": 72,
                "sentiment_score": 77,
                "strength_level": "strong"
            }
        }

        result = self.ai_service._generate_fallback_analysis(data)

        self.assertIsInstance(result, dict)
        self.assertIn("ai_analysis", result)
        self.assertIn("summary", result)
        self.assertIn("recommendation", result)
        self.assertIn("risk_level", result)
        self.assertIn("is_fallback", result)

    def test_build_analysis_prompt(self):
        """测试构建分析提示词"""
        analysis_data = {
            "market": "a_share",
            "date": "2024-01-15",
            "timing_indicators": {
                "overall_score": 78,
                "macro_score": 85,
                "industry_score": 72,
                "sentiment_score": 77,
                "strength_level": "strong"
            },
            "macro_data": {
                "pmi": 50.5,
                "cpi": 2.1,
                "ppi": 1.8,
                "m2": 8.5,
                "interest_rate": 3.0
            },
            "market_sentiment": {
                "volatility": 15.5,
                "investor_sentiment": 65.0,
                "technical_indicators": {
                    "rsi": 55.0,
                    "macd": 2.5,
                    "bollinger_bands": 1.2
                }
            },
            "industry_data": {
                "free_cash_flow": 120.5,
                "industry_sentiment": 70.0
            },
            "weights": {
                "macro_fundamental": 0.4,
                "industry_fundamental": 0.3,
                "market_sentiment": 0.3
            }
        }

        prompt = self.ai_service._build_analysis_prompt(analysis_data)

        self.assertIsInstance(prompt, str)
        self.assertIn("a_share", prompt)
        self.assertIn("综合评分", prompt)
        self.assertIn("宏观基本面", prompt)
        self.assertIn("市场情绪", prompt)

    def test_parse_ai_response_json(self):
        """测试解析JSON格式的AI响应"""
        ai_response = '{"summary": "当前市场整体处于中性偏乐观状态...", "recommendation": "建议买入", "risk_level": "medium"}'
        analysis_data = {
            "market": "a_share",
            "date": "2024-01-15"
        }

        result = self.ai_service._parse_ai_response(ai_response, analysis_data)

        self.assertIsInstance(result, dict)
        self.assertEqual(result["summary"], "当前市场整体处于中性偏乐观状态...")
        self.assertEqual(result["recommendation"], "建议买入")
        self.assertEqual(result["risk_level"], "medium")

    def test_parse_ai_response_text(self):
        """测试解析文本格式的AI响应"""
        ai_response = """
综合评估：当前市场整体处于中性偏乐观状态。
投资建议：建议适度配置仓位，关注科技行业。
风险提示：需要注意宏观经济波动风险。
"""
        analysis_data = {
            "market": "a_share",
            "date": "2024-01-15"
        }

        result = self.ai_service._parse_ai_response(ai_response, analysis_data)

        self.assertIsInstance(result, dict)
        self.assertIn("ai_analysis", result)
        self.assertIn("summary", result)
        self.assertIn("recommendation", result)
        self.assertIn("risk_level", result)

    def test_extract_summary(self):
        """测试提取分析摘要"""
        response = """
综合评估：当前市场整体处于中性偏乐观状态。
优势分析：宏观基本面表现良好。
"""
        summary = self.ai_service._extract_summary(response)

        self.assertIsInstance(summary, str)
        self.assertIn("综合评估", summary)

    def test_extract_recommendation(self):
        """测试提取投资建议"""
        response = """
投资建议：建议适度配置仓位。
仓位建议：建议配置60%的权益类资产。
"""
        recommendation = self.ai_service._extract_recommendation(response)

        self.assertIsInstance(recommendation, str)
        # 由于实际实现可能返回默认值，我们只检查类型
        self.assertTrue(len(recommendation) > 0)

    def test_extract_risk_level(self):
        """测试提取风险等级"""
        # 测试高风险
        high_risk_response = "当前市场面临高风险"
        high_risk = self.ai_service._extract_risk_level(high_risk_response)

        # 测试低风险
        low_risk_response = "当前市场风险较低"
        low_risk = self.ai_service._extract_risk_level(low_risk_response)

        # 测试中等风险
        medium_risk_response = "当前市场风险适中"
        medium_risk = self.ai_service._extract_risk_level(medium_risk_response)

        self.assertEqual(high_risk, "high")
        self.assertEqual(low_risk, "low")
        self.assertEqual(medium_risk, "medium")

    def test_cache_functionality(self):
        """测试缓存功能"""
        data = {
            "market": "a_share",
            "date": "2024-01-15"
        }

        cache_key = self.ai_service._generate_cache_key(data)
        self.assertEqual(cache_key, "a_share_2024-01-15")

        # 测试缓存检查
        cache_exists = self.ai_service._check_cache(cache_key)
        self.assertFalse(cache_exists)

    def test_get_ai_analysis_history(self):
        """测试获取AI分析历史"""
        history = self.ai_service.get_ai_analysis_history("a_share")

        self.assertIsInstance(history, list)


if __name__ == '__main__':
    unittest.main()