#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI分析服务

集成DeepSeek API进行择时分析和建议生成
"""

import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

from openai import OpenAI

from ..utils.config import config_manager
from .data_service import DataService


class AIService:
    """AI分析服务"""

    def __init__(self):
        self.data_service = DataService()
        self.logger = logging.getLogger(__name__)
        self.client = self._init_openai_client()
        self.cache = {}

    def _init_openai_client(self) -> Optional[OpenAI]:
        """初始化OpenAI客户端"""
        try:
            ai_config = config_manager.get_ai_config()
            api_key = ai_config.get('api_key')
            base_url = ai_config.get('base_url')

            if not api_key or api_key == "your-deepseek-api-key-here":
                self.logger.warning("AI API密钥未配置，AI功能将无法使用")
                return None

            return OpenAI(
                api_key=api_key,
                base_url=base_url
            )

        except Exception as e:
            self.logger.error(f"初始化OpenAI客户端失败: {e}")
            return None

    def analyze_timing_indicators(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI分析择时指标

        Args:
            data: 择时指标数据

        Returns:
            Dict[str, Any]: AI分析结果
        """
        try:
            # 检查缓存
            cache_key = self._generate_cache_key(data)
            if self._check_cache(cache_key):
                self.logger.info("使用缓存的AI分析结果")
                return self.cache[cache_key]

            # 检查客户端是否可用
            if not self.client:
                return self._generate_fallback_analysis(data)

            # 准备分析数据
            analysis_data = self._prepare_analysis_data(data)

            # 调用AI分析
            analysis_result = self._call_ai_analysis(analysis_data)

            # 保存分析结果
            analysis_result['calculated_at'] = datetime.now().isoformat()
            analysis_result['market'] = data['market']
            analysis_result['date'] = data['date']

            self.data_service.save_ai_analysis(analysis_result)

            # 缓存结果
            self._cache_result(cache_key, analysis_result)

            self.logger.info(f"AI分析完成: {data['market']} - {data['date']}")
            return analysis_result

        except Exception as e:
            self.logger.error(f"AI分析失败: {e}")
            return self._generate_fallback_analysis(data)

    def _prepare_analysis_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """准备分析数据"""
        market = data['market']
        date = data['date']

        # 获取择时指标
        timing_data = data.get('timing_indicators')
        if not timing_data:
            timing_data = self.data_service.get_timing_indicators(market)
            if timing_data:
                timing_data = timing_data[0]  # 使用最新的数据

        # 获取宏观数据
        macro_data = self.data_service.get_macro_data(market)
        latest_macro = macro_data[0] if macro_data else {}

        # 获取市场情绪数据
        sentiment_data = self.data_service.get_market_sentiment(market)
        latest_sentiment = sentiment_data[0] if sentiment_data else {}

        # 获取行业数据
        industry_data = self.data_service.get_industry_data(market)
        latest_industry = industry_data[0] if industry_data else {}

        analysis_data = {
            'market': market,
            'date': date,
            'timing_indicators': timing_data,
            'macro_data': latest_macro,
            'market_sentiment': latest_sentiment,
            'industry_data': latest_industry,
            'market_config': config_manager.get_market_config(market),
            'weights': config_manager.get_timing_weights()
        }

        return analysis_data

    def _call_ai_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """调用AI分析"""
        try:
            # 构建提示词
            prompt = self._build_analysis_prompt(analysis_data)

            # AI配置
            ai_config = config_manager.get_ai_config()
            model = ai_config.get('model', 'deepseek-chat')
            max_tokens = ai_config.get('max_tokens', 2000)
            temperature = ai_config.get('temperature', 0.7)

            # 调用API
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的量化投资分析师，专门从事择时分析。请基于提供的择时指标数据，给出专业的投资分析和建议。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )

            # 解析响应
            ai_response = response.choices[0].message.content
            analysis_result = self._parse_ai_response(ai_response, analysis_data)

            return analysis_result

        except Exception as e:
            self.logger.error(f"调用AI分析API失败: {e}")
            raise

    def _build_analysis_prompt(self, analysis_data: Dict[str, Any]) -> str:
        """构建分析提示词"""
        market = analysis_data['market']
        date = analysis_data['date']
        timing_data = analysis_data['timing_indicators']
        macro_data = analysis_data['macro_data']
        sentiment_data = analysis_data['market_sentiment']
        industry_data = analysis_data['industry_data']
        weights = analysis_data['weights']

        prompt = f"""
请基于以下择时指标数据，对{market}市场在{date}的投资时机进行分析：

## 择时指标概览
- 综合评分: {timing_data.get('overall_score', 0)}/100
- 宏观基本面评分: {timing_data.get('macro_score', 0)}/100 (权重: {weights.get('macro_fundamental', 0.4)})
- 行业基本面评分: {timing_data.get('industry_score', 0)}/100 (权重: {weights.get('industry_fundamental', 0.3)})
- 市场情绪评分: {timing_data.get('sentiment_score', 0)}/100 (权重: {weights.get('market_sentiment', 0.3)})
- 择时强度: {timing_data.get('strength_level', 'neutral')}

## 宏观基本面数据
- PMI: {macro_data.get('pmi', 'N/A')}
- CPI: {macro_data.get('cpi', 'N/A')}%
- PPI: {macro_data.get('ppi', 'N/A')}%
- M2增速: {macro_data.get('m2', 'N/A')}%
- 利率: {macro_data.get('interest_rate', 'N/A')}%

## 市场情绪数据
- 波动率: {sentiment_data.get('volatility', 'N/A')}%
- 投资者情绪: {sentiment_data.get('investor_sentiment', 'N/A')}/100
- 技术指标: {json.dumps(sentiment_data.get('technical_indicators', {}), ensure_ascii=False)}

## 行业基本面数据
- 自由现金流: {industry_data.get('free_cash_flow', 'N/A')}
- 行业情绪: {industry_data.get('industry_sentiment', 'N/A')}/100

请提供以下分析内容：

1. **综合评估**：对当前择时信号的整体评价
2. **优势分析**：当前市场的积极因素和优势
3. **风险提示**：需要注意的风险和不利因素
4. **投资建议**：具体的买入/卖出/观望建议
5. **仓位建议**：基于择时强度的仓位配置建议
6. **时间展望**：短期和中期的市场展望

请用专业、客观的语言进行分析，避免使用过于情绪化的表述。
"""

        return prompt

    def _parse_ai_response(self, ai_response: str, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """解析AI响应"""
        try:
            # 尝试解析JSON格式的响应
            if ai_response.strip().startswith('{') and ai_response.strip().endswith('}'):
                return json.loads(ai_response)

            # 如果是文本格式，进行结构化处理
            analysis_result = {
                'market': analysis_data['market'],
                'date': analysis_data['date'],
                'ai_analysis': ai_response,
                'summary': self._extract_summary(ai_response),
                'recommendation': self._extract_recommendation(ai_response),
                'risk_level': self._extract_risk_level(ai_response),
                'time_horizon': self._extract_time_horizon(ai_response)
            }

            return analysis_result

        except Exception as e:
            self.logger.warning(f"解析AI响应失败，使用原始响应: {e}")
            return {
                'market': analysis_data['market'],
                'date': analysis_data['date'],
                'ai_analysis': ai_response,
                'summary': 'AI分析结果',
                'recommendation': '请参考详细分析',
                'risk_level': 'medium',
                'time_horizon': 'short_term'
            }

    def _extract_summary(self, response: str) -> str:
        """提取分析摘要"""
        # 简化的摘要提取逻辑
        lines = response.split('\n')
        for line in lines:
            if '综合评估' in line or '整体评价' in line:
                return line.strip()
        return response[:100] + '...' if len(response) > 100 else response

    def _extract_recommendation(self, response: str) -> str:
        """提取投资建议"""
        lines = response.split('\n')
        for line in lines:
            if '建议' in line and ('买入' in line or '卖出' in line or '观望' in line):
                return line.strip()
        return '请参考详细分析'

    def _extract_risk_level(self, response: str) -> str:
        """提取风险等级"""
        response_lower = response.lower()
        if '高风险' in response_lower or '极高风险' in response_lower:
            return 'high'
        elif '低风险' in response_lower or '风险较低' in response_lower:
            return 'low'
        else:
            return 'medium'

    def _extract_time_horizon(self, response: str) -> str:
        """提取时间展望"""
        response_lower = response.lower()
        if '长期' in response_lower or '中长期' in response_lower:
            return 'long_term'
        elif '中期' in response_lower:
            return 'medium_term'
        else:
            return 'short_term'

    def _generate_cache_key(self, data: Dict[str, Any]) -> str:
        """生成缓存键"""
        market = data['market']
        date = data['date']
        return f"{market}_{date}"

    def _check_cache(self, cache_key: str) -> bool:
        """检查缓存"""
        ai_config = config_manager.get_ai_config()
        if not ai_config.get('cache_enabled', True):
            return False

        if cache_key in self.cache:
            cache_ttl = ai_config.get('cache_ttl_minutes', 60) * 60  # 转换为秒
            cached_time = self.cache[cache_key].get('cached_at', 0)
            if time.time() - cached_time < cache_ttl:
                return True
            else:
                # 缓存过期，删除
                del self.cache[cache_key]

        return False

    def _cache_result(self, cache_key: str, result: Dict[str, Any]):
        """缓存结果"""
        ai_config = config_manager.get_ai_config()
        if ai_config.get('cache_enabled', True):
            result['cached_at'] = time.time()
            self.cache[cache_key] = result

    def _generate_fallback_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """生成备用分析结果"""
        timing_data = data.get('timing_indicators', {})
        overall_score = timing_data.get('overall_score', 0)
        strength_level = timing_data.get('strength_level', 'neutral')

        # 基于评分生成简单的分析
        if overall_score >= 80:
            analysis = "择时信号非常强劲，建议积极配置仓位。宏观基本面、行业基本面和市场情绪均表现良好。"
            recommendation = "强烈买入"
            risk_level = "low"
        elif overall_score >= 60:
            analysis = "择时信号强劲，建议适度配置仓位。市场整体表现积极，但需关注潜在风险。"
            recommendation = "建议买入"
            risk_level = "medium"
        elif overall_score >= 40:
            analysis = "择时信号中性，建议观望或轻仓操作。市场存在不确定性，需要更多数据支持。"
            recommendation = "观望"
            risk_level = "medium"
        elif overall_score >= 20:
            analysis = "择时信号偏弱，建议谨慎操作或减仓。市场面临较多不利因素。"
            recommendation = "谨慎"
            risk_level = "high"
        else:
            analysis = "择时信号非常弱，建议回避或空仓。市场环境恶劣，风险较高。"
            recommendation = "回避"
            risk_level = "high"

        return {
            'market': data['market'],
            'date': data['date'],
            'ai_analysis': analysis,
            'summary': f"择时评分{overall_score}，强度{strength_level}",
            'recommendation': recommendation,
            'risk_level': risk_level,
            'time_horizon': 'short_term',
            'is_fallback': True,
            'calculated_at': datetime.now().isoformat()
        }

    def save_ai_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        保存AI分析结果

        Args:
            analysis_data: AI分析数据

        Returns:
            Dict[str, Any]: 保存后的数据
        """
        try:
            # 保存到数据服务
            result = self.data_service.save_ai_analysis(analysis_data)
            return result

        except Exception as e:
            self.logger.error(f"保存AI分析结果失败: {e}")
            raise

    def get_ai_analysis_history(self, market: str, start_date: Optional[str] = None,
                               end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取AI分析历史

        Args:
            market: 市场类型
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            List[Dict[str, Any]]: AI分析历史列表
        """
        try:
            return self.data_service.get_ai_analysis(market, start_date, end_date)

        except Exception as e:
            self.logger.error(f"获取AI分析历史失败: {e}")
            return []