#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
择时数据模型

定义择时分析相关的数据模型
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class MacroData(BaseModel):
    """宏观数据模型"""
    id: Optional[str] = None
    date: str
    market: str
    pmi: Optional[float] = None
    cpi: Optional[float] = None
    ppi: Optional[float] = None
    m2: Optional[float] = None
    interest_rate: Optional[float] = None
    other_macro: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "date": "2024-01-15",
                "market": "a_share",
                "pmi": 50.5,
                "cpi": 2.1,
                "ppi": 1.8,
                "m2": 8.5,
                "interest_rate": 3.0,
                "other_macro": {}
            }
        }


class MarketSentiment(BaseModel):
    """市场情绪数据模型"""
    id: Optional[str] = None
    date: str
    market: str
    volatility: Optional[float] = None
    investor_sentiment: Optional[float] = None
    technical_indicators: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
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
        }


class IndustryData(BaseModel):
    """行业基本面数据模型"""
    id: Optional[str] = None
    date: str
    market: str
    industry: str
    free_cash_flow: Optional[float] = None
    industry_sentiment: Optional[float] = None
    created_at: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "date": "2024-01-15",
                "market": "a_share",
                "industry": "technology",
                "free_cash_flow": 120.5,
                "industry_sentiment": 70.0
            }
        }


class TimingIndicators(BaseModel):
    """择时指标模型"""
    id: Optional[str] = None
    market: str
    date: str
    overall_score: float = Field(..., ge=0, le=100)
    macro_score: float = Field(..., ge=0, le=100)
    industry_score: float = Field(..., ge=0, le=100)
    sentiment_score: float = Field(..., ge=0, le=100)
    weights: Dict[str, float]
    strength_level: str
    calculated_at: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "market": "a_share",
                "date": "2024-01-15",
                "overall_score": 75.5,
                "macro_score": 80.0,
                "industry_score": 70.0,
                "sentiment_score": 65.0,
                "weights": {
                    "macro_fundamental": 0.4,
                    "industry_fundamental": 0.3,
                    "market_sentiment": 0.3
                },
                "strength_level": "strong"
            }
        }


class AIAnalysis(BaseModel):
    """AI分析结果模型"""
    id: Optional[str] = None
    market: str
    date: str
    ai_analysis: str
    summary: str
    recommendation: str
    risk_level: str
    time_horizon: str
    is_fallback: bool = False
    calculated_at: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "market": "a_share",
                "date": "2024-01-15",
                "ai_analysis": "基于当前择时指标分析，市场整体表现积极...",
                "summary": "择时评分75.5，强度strong",
                "recommendation": "建议买入",
                "risk_level": "medium",
                "time_horizon": "short_term"
            }
        }


class PositionSizing(BaseModel):
    """仓位建议模型"""
    market: str
    date: str
    timing_score: float = Field(..., ge=0, le=100)
    strength_level: str
    position_percentage: float
    position_amount: float
    available_capital: float
    risk_per_trade_percentage: float
    risk_amount: float
    calculated_at: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "market": "a_share",
                "date": "2024-01-15",
                "timing_score": 75.5,
                "strength_level": "strong",
                "position_percentage": 60.0,
                "position_amount": 60000.0,
                "available_capital": 100000.0,
                "risk_per_trade_percentage": 2.0,
                "risk_amount": 2000.0
            }
        }


class MarketComparison(BaseModel):
    """市场比较模型"""
    markets: Dict[str, Dict[str, Any]]
    best_market: Optional[str] = None
    comparison_date: str

    class Config:
        schema_extra = {
            "example": {
                "markets": {
                    "a_share": {
                        "overall_score": 75.5,
                        "macro_score": 80.0,
                        "industry_score": 70.0,
                        "sentiment_score": 65.0,
                        "strength_level": "strong"
                    },
                    "hong_kong": {
                        "overall_score": 65.0,
                        "macro_score": 70.0,
                        "industry_score": 60.0,
                        "sentiment_score": 65.0,
                        "strength_level": "neutral"
                    }
                },
                "best_market": "a_share",
                "comparison_date": "2024-01-15"
            }
        }


class AnalysisSummary(BaseModel):
    """分析摘要模型"""
    market: str
    analysis_date: str
    overall_score: float
    strength_level: str
    component_scores: Dict[str, float]
    key_indicators: Dict[str, Optional[float]]
    recommendation: str

    class Config:
        schema_extra = {
            "example": {
                "market": "a_share",
                "analysis_date": "2024-01-15",
                "overall_score": 75.5,
                "strength_level": "strong",
                "component_scores": {
                    "macro": 80.0,
                    "industry": 70.0,
                    "sentiment": 65.0
                },
                "key_indicators": {
                    "pmi": 50.5,
                    "cpi": 2.1,
                    "volatility": 15.5,
                    "investor_sentiment": 65.0
                },
                "recommendation": "建议买入 - 择时信号强劲"
            }
        }