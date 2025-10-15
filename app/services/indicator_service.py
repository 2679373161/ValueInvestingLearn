#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
指标计算服务

负责择时指标的计算和评分
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from ..utils.config import config_manager
from .data_service import DataService


class IndicatorService:
    """指标计算服务"""

    def __init__(self):
        self.data_service = DataService()
        self.logger = logging.getLogger(__name__)

    def calculate_timing_indicators(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算择时指标

        Args:
            data: 输入数据

        Returns:
            Dict[str, Any]: 择时指标结果
        """
        try:
            market = data['market']
            date = data['date']

            # 计算各维度评分
            macro_score = self._calculate_macro_score(data.get('macro_data', {}))
            industry_score = self._calculate_industry_score(data.get('industry_data', {}))
            sentiment_score = self._calculate_sentiment_score(data.get('market_sentiment', {}))

            # 获取权重配置
            weights = config_manager.get_timing_weights()

            # 计算综合评分
            overall_score = (
                macro_score * weights.get('macro_fundamental', 0.4) +
                industry_score * weights.get('industry_fundamental', 0.3) +
                sentiment_score * weights.get('market_sentiment', 0.3)
            )

            # 生成结果
            result = {
                'market': market,
                'date': date,
                'overall_score': round(overall_score, 2),
                'macro_score': round(macro_score, 2),
                'industry_score': round(industry_score, 2),
                'sentiment_score': round(sentiment_score, 2),
                'weights': weights,
                'calculated_at': datetime.now().isoformat(),
                'strength_level': self._get_strength_level(overall_score)
            }

            # 保存结果
            self.data_service.save_timing_indicators(result)

            self.logger.info(f"计算择时指标完成: {market} - {date} - 评分: {overall_score}")
            return result

        except Exception as e:
            self.logger.error(f"计算择时指标失败: {e}")
            raise

    def _calculate_macro_score(self, macro_data: Dict[str, Any]) -> float:
        """计算宏观基本面评分"""
        try:
            macro_config = config_manager.get('timing_indicators.macro_indicators', {})
            total_score = 0.0
            total_weight = 0.0

            # PMI评分
            pmi = macro_data.get('pmi')
            if pmi is not None:
                pmi_config = macro_config.get('pmi', {})
                pmi_score = self._calculate_pmi_score(pmi, pmi_config)
                pmi_weight = pmi_config.get('weight', 0.2)
                total_score += pmi_score * pmi_weight
                total_weight += pmi_weight

            # CPI评分
            cpi = macro_data.get('cpi')
            if cpi is not None:
                cpi_config = macro_config.get('cpi', {})
                cpi_score = self._calculate_cpi_score(cpi, cpi_config)
                cpi_weight = cpi_config.get('weight', 0.2)
                total_score += cpi_score * cpi_weight
                total_weight += cpi_weight

            # PPI评分
            ppi = macro_data.get('ppi')
            if ppi is not None:
                ppi_config = macro_config.get('ppi', {})
                ppi_score = self._calculate_ppi_score(ppi, ppi_config)
                ppi_weight = ppi_config.get('weight', 0.15)
                total_score += ppi_score * ppi_weight
                total_weight += ppi_weight

            # M2评分
            m2 = macro_data.get('m2')
            if m2 is not None:
                m2_config = macro_config.get('m2', {})
                m2_score = self._calculate_m2_score(m2, m2_config)
                m2_weight = m2_config.get('weight', 0.15)
                total_score += m2_score * m2_weight
                total_weight += m2_weight

            # 利率评分
            interest_rate = macro_data.get('interest_rate')
            if interest_rate is not None:
                rate_config = macro_config.get('interest_rate', {})
                rate_score = self._calculate_interest_rate_score(interest_rate, rate_config)
                rate_weight = rate_config.get('weight', 0.15)
                total_score += rate_score * rate_weight
                total_weight += rate_weight

            # 其他宏观指标
            other_macro = macro_data.get('other_macro', {})
            if other_macro:
                other_config = macro_config.get('other_macro', {})
                other_weight = other_config.get('weight', 0.15)
                total_weight += other_weight

            # 归一化评分
            if total_weight > 0:
                return (total_score / total_weight) * 100
            else:
                return 50.0  # 默认中性评分

        except Exception as e:
            self.logger.error(f"计算宏观评分失败: {e}")
            return 50.0

    def _calculate_pmi_score(self, pmi: float, config: Dict[str, Any]) -> float:
        """计算PMI评分"""
        threshold_good = config.get('threshold_good', 50)
        threshold_bad = config.get('threshold_bad', 45)

        if pmi >= threshold_good:
            return 100.0
        elif pmi <= threshold_bad:
            return 0.0
        else:
            # 线性插值
            return ((pmi - threshold_bad) / (threshold_good - threshold_bad)) * 100

    def _calculate_cpi_score(self, cpi: float, config: Dict[str, Any]) -> float:
        """计算CPI评分"""
        threshold_good = config.get('threshold_good', 2.0)
        threshold_bad = config.get('threshold_bad', 5.0)

        if cpi <= threshold_good:
            return 100.0
        elif cpi >= threshold_bad:
            return 0.0
        else:
            # 线性插值
            return 100 - ((cpi - threshold_good) / (threshold_bad - threshold_good)) * 100

    def _calculate_ppi_score(self, ppi: float, config: Dict[str, Any]) -> float:
        """计算PPI评分"""
        threshold_good = config.get('threshold_good', 1.5)
        threshold_bad = config.get('threshold_bad', 4.0)

        if ppi <= threshold_good:
            return 100.0
        elif ppi >= threshold_bad:
            return 0.0
        else:
            # 线性插值
            return 100 - ((ppi - threshold_good) / (threshold_bad - threshold_good)) * 100

    def _calculate_m2_score(self, m2: float, config: Dict[str, Any]) -> float:
        """计算M2评分"""
        threshold_good = config.get('threshold_good', 8.0)
        threshold_bad = config.get('threshold_bad', 15.0)

        if m2 <= threshold_good:
            return 100.0
        elif m2 >= threshold_bad:
            return 0.0
        else:
            # 线性插值
            return 100 - ((m2 - threshold_good) / (threshold_bad - threshold_good)) * 100

    def _calculate_interest_rate_score(self, rate: float, config: Dict[str, Any]) -> float:
        """计算利率评分"""
        threshold_good = config.get('threshold_good', 2.0)
        threshold_bad = config.get('threshold_bad', 5.0)

        if rate <= threshold_good:
            return 100.0
        elif rate >= threshold_bad:
            return 0.0
        else:
            # 线性插值
            return 100 - ((rate - threshold_good) / (threshold_bad - threshold_good)) * 100

    def _calculate_industry_score(self, industry_data: Dict[str, Any]) -> float:
        """计算行业基本面评分"""
        try:
            industry_config = config_manager.get('timing_indicators.industry_indicators', {})
            total_score = 0.0
            total_weight = 0.0

            # 自由现金流评分
            fcf = industry_data.get('free_cash_flow')
            if fcf is not None:
                fcf_config = industry_config.get('free_cash_flow', {})
                fcf_score = self._calculate_fcf_score(fcf)
                fcf_weight = fcf_config.get('weight', 0.6)
                total_score += fcf_score * fcf_weight
                total_weight += fcf_weight

            # 行业情绪评分
            industry_sentiment = industry_data.get('industry_sentiment')
            if industry_sentiment is not None:
                sentiment_config = industry_config.get('industry_sentiment', {})
                sentiment_score = industry_sentiment  # 假设已经是0-100的评分
                sentiment_weight = sentiment_config.get('weight', 0.4)
                total_score += sentiment_score * sentiment_weight
                total_weight += sentiment_weight

            # 归一化评分
            if total_weight > 0:
                return total_score / total_weight
            else:
                return 50.0

        except Exception as e:
            self.logger.error(f"计算行业评分失败: {e}")
            return 50.0

    def _calculate_fcf_score(self, fcf: float) -> float:
        """计算自由现金流评分"""
        # 简化的评分逻辑，实际应用中需要更复杂的计算
        if fcf > 0:
            return min(fcf / 10 * 100, 100)  # 假设10为优秀水平
        else:
            return 0.0

    def _calculate_sentiment_score(self, sentiment_data: Dict[str, Any]) -> float:
        """计算市场情绪评分"""
        try:
            sentiment_config = config_manager.get('timing_indicators.market_sentiment_indicators', {})
            total_score = 0.0
            total_weight = 0.0

            # 波动率评分
            volatility = sentiment_data.get('volatility')
            if volatility is not None:
                vol_config = sentiment_config.get('volatility', {})
                vol_score = self._calculate_volatility_score(volatility)
                vol_weight = vol_config.get('weight', 0.3)
                total_score += vol_score * vol_weight
                total_weight += vol_weight

            # 投资者情绪评分
            investor_sentiment = sentiment_data.get('investor_sentiment')
            if investor_sentiment is not None:
                investor_config = sentiment_config.get('investor_sentiment', {})
                investor_score = investor_sentiment  # 假设已经是0-100的评分
                investor_weight = investor_config.get('weight', 0.4)
                total_score += investor_score * investor_weight
                total_weight += investor_weight

            # 技术指标评分
            technical_indicators = sentiment_data.get('technical_indicators', {})
            if technical_indicators:
                tech_config = sentiment_config.get('technical_indicators', {})
                tech_score = self._calculate_technical_score(technical_indicators)
                tech_weight = tech_config.get('weight', 0.3)
                total_score += tech_score * tech_weight
                total_weight += tech_weight

            # 归一化评分
            if total_weight > 0:
                return total_score / total_weight
            else:
                return 50.0

        except Exception as e:
            self.logger.error(f"计算市场情绪评分失败: {e}")
            return 50.0

    def _calculate_volatility_score(self, volatility: float) -> float:
        """计算波动率评分"""
        # 简化的评分逻辑：波动率越低越好
        if volatility <= 10:
            return 100.0
        elif volatility >= 30:
            return 0.0
        else:
            return 100 - ((volatility - 10) / 20) * 100

    def _calculate_technical_score(self, technical_indicators: Dict[str, Any]) -> float:
        """计算技术指标评分"""
        # 简化的综合技术指标评分
        score = 50.0

        # RSI评分
        rsi = technical_indicators.get('rsi')
        if rsi is not None:
            if 30 <= rsi <= 70:
                score += 20
            elif rsi < 30 or rsi > 70:
                score -= 20

        # MACD评分
        macd = technical_indicators.get('macd')
        if macd is not None:
            if macd > 0:
                score += 15
            else:
                score -= 15

        # 布林带评分
        bollinger = technical_indicators.get('bollinger_bands')
        if bollinger is not None:
            if abs(bollinger) <= 1:
                score += 15
            else:
                score -= 15

        return max(0, min(100, score))

    def _get_strength_level(self, score: float) -> str:
        """获取择时强度等级"""
        thresholds = config_manager.get('position_sizing.scoring_thresholds', {})

        if score >= thresholds.get('very_strong', 80):
            return 'very_strong'
        elif score >= thresholds.get('strong', 60):
            return 'strong'
        elif score >= thresholds.get('neutral', 40):
            return 'neutral'
        elif score >= thresholds.get('weak', 20):
            return 'weak'
        else:
            return 'very_weak'

    def calculate_position_sizing(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算仓位建议

        Args:
            data: 输入数据

        Returns:
            Dict[str, Any]: 仓位建议
        """
        try:
            timing_score = data['timing_score']
            available_capital = data.get('available_capital', 100000)
            risk_per_trade = data.get('risk_per_trade_percentage', 2)

            # 获取仓位配置
            position_sizes = config_manager.get('position_sizing.position_sizes', {})
            strength_level = self._get_strength_level(timing_score)

            # 计算建议仓位比例
            position_percentage = position_sizes.get(strength_level, 0)

            # 计算建议仓位金额
            position_amount = (position_percentage / 100) * available_capital

            # 计算单笔风险金额
            risk_amount = (risk_per_trade / 100) * available_capital

            result = {
                'market': data['market'],
                'date': data['date'],
                'timing_score': timing_score,
                'strength_level': strength_level,
                'position_percentage': position_percentage,
                'position_amount': round(position_amount, 2),
                'available_capital': available_capital,
                'risk_per_trade_percentage': risk_per_trade,
                'risk_amount': round(risk_amount, 2),
                'calculated_at': datetime.now().isoformat()
            }

            return result

        except Exception as e:
            self.logger.error(f"计算仓位建议失败: {e}")
            raise

    def get_timing_indicators(self, market: str, start_date: Optional[str] = None,
                            end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取择时指标历史数据"""
        return self.data_service.get_timing_indicators(market, start_date, end_date)

    def compare_markets(self, markets: List[str], date: Optional[str] = None) -> Dict[str, Any]:
        """多市场比较分析"""
        try:
            comparison_data = {}

            for market in markets:
                # 获取该市场的最新择时指标
                timing_data = self.get_timing_indicators(market)
                if timing_data:
                    latest_data = timing_data[0]  # 最新的数据
                    comparison_data[market] = {
                        'overall_score': latest_data.get('overall_score', 0),
                        'macro_score': latest_data.get('macro_score', 0),
                        'industry_score': latest_data.get('industry_score', 0),
                        'sentiment_score': latest_data.get('sentiment_score', 0),
                        'strength_level': latest_data.get('strength_level', 'neutral'),
                        'date': latest_data.get('date')
                    }

            # 按综合评分排序
            sorted_markets = sorted(
                comparison_data.items(),
                key=lambda x: x[1]['overall_score'],
                reverse=True
            )

            return {
                'markets': dict(sorted_markets),
                'best_market': sorted_markets[0][0] if sorted_markets else None,
                'comparison_date': date or datetime.now().strftime('%Y-%m-%d')
            }

        except Exception as e:
            self.logger.error(f"市场比较分析失败: {e}")
            raise

    def get_analysis_summary(self, market: str, date: Optional[str] = None) -> Dict[str, Any]:
        """获取分析摘要"""
        try:
            # 获取最新择时指标
            timing_data = self.get_timing_indicators(market)
            if not timing_data:
                return {'error': '暂无分析数据'}

            latest_data = timing_data[0]

            # 获取宏观数据
            macro_data = self.data_service.get_macro_data(market)
            latest_macro = macro_data[0] if macro_data else {}

            # 获取市场情绪数据
            sentiment_data = self.data_service.get_market_sentiment(market)
            latest_sentiment = sentiment_data[0] if sentiment_data else {}

            summary = {
                'market': market,
                'analysis_date': latest_data.get('date'),
                'overall_score': latest_data.get('overall_score', 0),
                'strength_level': latest_data.get('strength_level', 'neutral'),
                'component_scores': {
                    'macro': latest_data.get('macro_score', 0),
                    'industry': latest_data.get('industry_score', 0),
                    'sentiment': latest_data.get('sentiment_score', 0)
                },
                'key_indicators': {
                    'pmi': latest_macro.get('pmi'),
                    'cpi': latest_macro.get('cpi'),
                    'volatility': latest_sentiment.get('volatility'),
                    'investor_sentiment': latest_sentiment.get('investor_sentiment')
                },
                'recommendation': self._generate_recommendation(latest_data)
            }

            return summary

        except Exception as e:
            self.logger.error(f"获取分析摘要失败: {e}")
            raise

    def _generate_recommendation(self, timing_data: Dict[str, Any]) -> str:
        """生成投资建议"""
        score = timing_data.get('overall_score', 0)
        strength_level = timing_data.get('strength_level', 'neutral')

        recommendations = {
            'very_strong': '强烈买入 - 择时信号非常强劲',
            'strong': '建议买入 - 择时信号强劲',
            'neutral': '观望 - 择时信号中性',
            'weak': '谨慎 - 择时信号偏弱',
            'very_weak': '回避 - 择时信号非常弱'
        }

        return recommendations.get(strength_level, '暂无建议')

    # 可视化相关方法
    def get_timing_score_trend(self, market: str, start_date: Optional[str] = None,
                              end_date: Optional[str] = None, indicator_type: str = 'overall') -> List[Dict[str, Any]]:
        """获取择时评分趋势数据"""
        timing_data = self.get_timing_indicators(market, start_date, end_date)

        trend_data = []
        for data in timing_data:
            if indicator_type == 'overall':
                score = data.get('overall_score', 0)
            elif indicator_type == 'macro':
                score = data.get('macro_score', 0)
            elif indicator_type == 'industry':
                score = data.get('industry_score', 0)
            elif indicator_type == 'sentiment':
                score = data.get('sentiment_score', 0)
            else:
                score = data.get('overall_score', 0)

            trend_data.append({
                'date': data.get('date'),
                'score': score,
                'strength_level': data.get('strength_level', 'neutral')
            })

        return trend_data

    def get_market_comparison_data(self, markets: List[str], date: Optional[str],
                                  indicators: List[str]) -> Dict[str, Any]:
        """获取市场比较图表数据"""
        comparison_result = self.compare_markets(markets, date)
        market_data = comparison_result.get('markets', {})

        chart_data = {}
        for indicator in indicators:
            chart_data[indicator] = {}
            for market, data in market_data.items():
                chart_data[indicator][market] = data.get(indicator, 0)

        return chart_data

    def get_indicator_breakdown(self, market: str, date: Optional[str]) -> Dict[str, Any]:
        """获取指标分解数据"""
        timing_data = self.get_timing_indicators(market)
        if not timing_data:
            return {}

        latest_data = timing_data[0]
        weights = latest_data.get('weights', {})

        return {
            'macro': {
                'score': latest_data.get('macro_score', 0),
                'weight': weights.get('macro_fundamental', 0.4)
            },
            'industry': {
                'score': latest_data.get('industry_score', 0),
                'weight': weights.get('industry_fundamental', 0.3)
            },
            'sentiment': {
                'score': latest_data.get('sentiment_score', 0),
                'weight': weights.get('market_sentiment', 0.3)
            }
        }

    def get_position_sizing_chart_data(self, market: str, date: Optional[str],
                                     available_capital: float) -> Dict[str, Any]:
        """获取仓位配置图表数据"""
        timing_data = self.get_timing_indicators(market)
        if not timing_data:
            return {}

        latest_data = timing_data[0]
        timing_score = latest_data.get('overall_score', 0)

        # 计算不同评分下的仓位建议
        position_data = {}
        for score in range(0, 101, 10):
            position_data[str(score)] = self.calculate_position_sizing({
                'market': market,
                'date': date,
                'timing_score': score,
                'available_capital': available_capital
            })

        return {
            'current_score': timing_score,
            'position_data': position_data
        }

    def get_sentiment_analysis_data(self, market: str, start_date: Optional[str],
                                  end_date: Optional[str]) -> Dict[str, Any]:
        """获取市场情绪分析数据"""
        sentiment_data = self.data_service.get_market_sentiment(market, start_date, end_date)

        analysis_data = []
        for data in sentiment_data:
            analysis_data.append({
                'date': data.get('date'),
                'volatility': data.get('volatility', 0),
                'investor_sentiment': data.get('investor_sentiment', 0),
                'technical_score': self._calculate_technical_score(data.get('technical_indicators', {}))
            })

        return {
            'sentiment_data': analysis_data,
            'average_volatility': sum(d['volatility'] for d in analysis_data) / len(analysis_data) if analysis_data else 0,
            'average_sentiment': sum(d['investor_sentiment'] for d in analysis_data) / len(analysis_data) if analysis_data else 0
        }

    def get_dashboard_summary(self, market: str, date: Optional[str]) -> Dict[str, Any]:
        """获取仪表盘摘要数据"""
        analysis_summary = self.get_analysis_summary(market, date)
        position_data = self.calculate_position_sizing({
            'market': market,
            'date': date,
            'timing_score': analysis_summary.get('overall_score', 0),
            'available_capital': 100000
        })

        return {
            'analysis': analysis_summary,
            'position': position_data,
            'market_config': config_manager.get_market_config(market)
        }