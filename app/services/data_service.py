#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据管理服务

负责数据的存储、查询、验证和备份
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from ..utils.config import config_manager


class DataService:
    """数据管理服务"""

    def __init__(self):
        self.data_file = Path(config_manager.get('database.file_path', 'data/application_data.json'))
        self.logger = logging.getLogger(__name__)
        self._ensure_data_file()

    def _ensure_data_file(self):
        """确保数据文件存在"""
        try:
            if not self.data_file.exists():
                self.data_file.parent.mkdir(parents=True, exist_ok=True)
                initial_data = {
                    'macro_data': [],
                    'market_sentiment': [],
                    'industry_data': [],
                    'timing_indicators': [],
                    'ai_analysis': [],
                    'metadata': {
                        'created_at': datetime.now().isoformat(),
                        'last_updated': datetime.now().isoformat()
                    }
                }
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump(initial_data, f, indent=2, ensure_ascii=False)
                self.logger.info(f"创建数据文件: {self.data_file}")
        except Exception as e:
            self.logger.error(f"创建数据文件失败: {e}")
            raise

    def _load_data(self) -> Dict[str, Any]:
        """加载数据文件"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"加载数据文件失败: {e}")
            raise

    def _save_data(self, data: Dict[str, Any]):
        """保存数据文件"""
        try:
            data['metadata']['last_updated'] = datetime.now().isoformat()
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"保存数据文件失败: {e}")
            raise

    def save_macro_data(self, macro_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        保存宏观数据

        Args:
            macro_data: 宏观数据

        Returns:
            Dict[str, Any]: 保存后的数据
        """
        try:
            # 数据验证
            self._validate_macro_data(macro_data)

            # 添加时间戳
            macro_data['created_at'] = datetime.now().isoformat()
            macro_data['id'] = f"macro_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # 保存数据
            data = self._load_data()
            data['macro_data'].append(macro_data)
            self._save_data(data)

            self.logger.info(f"保存宏观数据: {macro_data['id']}")
            return macro_data

        except Exception as e:
            self.logger.error(f"保存宏观数据失败: {e}")
            raise

    def get_macro_data(self, market: str, start_date: Optional[str] = None,
                      end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取宏观数据

        Args:
            market: 市场类型
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            List[Dict[str, Any]]: 宏观数据列表
        """
        try:
            data = self._load_data()
            macro_data = data.get('macro_data', [])

            # 过滤数据
            filtered_data = [
                item for item in macro_data
                if item.get('market') == market
            ]

            # 日期过滤
            if start_date:
                filtered_data = [
                    item for item in filtered_data
                    if item.get('date', '') >= start_date
                ]

            if end_date:
                filtered_data = [
                    item for item in filtered_data
                    if item.get('date', '') <= end_date
                ]

            # 按日期排序
            filtered_data.sort(key=lambda x: x.get('date', ''), reverse=True)

            return filtered_data

        except Exception as e:
            self.logger.error(f"获取宏观数据失败: {e}")
            raise

    def save_market_sentiment(self, sentiment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        保存市场情绪数据

        Args:
            sentiment_data: 市场情绪数据

        Returns:
            Dict[str, Any]: 保存后的数据
        """
        try:
            # 数据验证
            self._validate_market_sentiment_data(sentiment_data)

            # 添加时间戳
            sentiment_data['created_at'] = datetime.now().isoformat()
            sentiment_data['id'] = f"sentiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # 保存数据
            data = self._load_data()
            data['market_sentiment'].append(sentiment_data)
            self._save_data(data)

            self.logger.info(f"保存市场情绪数据: {sentiment_data['id']}")
            return sentiment_data

        except Exception as e:
            self.logger.error(f"保存市场情绪数据失败: {e}")
            raise

    def get_market_sentiment(self, market: str, start_date: Optional[str] = None,
                           end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取市场情绪数据

        Args:
            market: 市场类型
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            List[Dict[str, Any]]: 市场情绪数据列表
        """
        try:
            data = self._load_data()
            sentiment_data = data.get('market_sentiment', [])

            # 过滤数据
            filtered_data = [
                item for item in sentiment_data
                if item.get('market') == market
            ]

            # 日期过滤
            if start_date:
                filtered_data = [
                    item for item in filtered_data
                    if item.get('date', '') >= start_date
                ]

            if end_date:
                filtered_data = [
                    item for item in filtered_data
                    if item.get('date', '') <= end_date
                ]

            # 按日期排序
            filtered_data.sort(key=lambda x: x.get('date', ''), reverse=True)

            return filtered_data

        except Exception as e:
            self.logger.error(f"获取市场情绪数据失败: {e}")
            raise

    def save_industry_data(self, industry_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        保存行业基本面数据

        Args:
            industry_data: 行业数据

        Returns:
            Dict[str, Any]: 保存后的数据
        """
        try:
            # 数据验证
            self._validate_industry_data(industry_data)

            # 添加时间戳
            industry_data['created_at'] = datetime.now().isoformat()
            industry_data['id'] = f"industry_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # 保存数据
            data = self._load_data()
            data['industry_data'].append(industry_data)
            self._save_data(data)

            self.logger.info(f"保存行业数据: {industry_data['id']}")
            return industry_data

        except Exception as e:
            self.logger.error(f"保存行业数据失败: {e}")
            raise

    def get_industry_data(self, market: str, industry: Optional[str] = None,
                         start_date: Optional[str] = None,
                         end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取行业基本面数据

        Args:
            market: 市场类型
            industry: 行业类型
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            List[Dict[str, Any]]: 行业数据列表
        """
        try:
            data = self._load_data()
            industry_data = data.get('industry_data', [])

            # 过滤数据
            filtered_data = [
                item for item in industry_data
                if item.get('market') == market
            ]

            if industry:
                filtered_data = [
                    item for item in filtered_data
                    if item.get('industry') == industry
                ]

            # 日期过滤
            if start_date:
                filtered_data = [
                    item for item in filtered_data
                    if item.get('date', '') >= start_date
                ]

            if end_date:
                filtered_data = [
                    item for item in filtered_data
                    if item.get('date', '') <= end_date
                ]

            # 按日期排序
            filtered_data.sort(key=lambda x: x.get('date', ''), reverse=True)

            return filtered_data

        except Exception as e:
            self.logger.error(f"获取行业数据失败: {e}")
            raise

    def save_timing_indicators(self, indicators: Dict[str, Any]) -> Dict[str, Any]:
        """
        保存择时指标数据

        Args:
            indicators: 择时指标数据

        Returns:
            Dict[str, Any]: 保存后的数据
        """
        try:
            # 添加时间戳
            indicators['created_at'] = datetime.now().isoformat()
            indicators['id'] = f"timing_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # 保存数据
            data = self._load_data()
            data['timing_indicators'].append(indicators)
            self._save_data(data)

            self.logger.info(f"保存择时指标: {indicators['id']}")
            return indicators

        except Exception as e:
            self.logger.error(f"保存择时指标失败: {e}")
            raise

    def get_timing_indicators(self, market: str, start_date: Optional[str] = None,
                            end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取择时指标数据

        Args:
            market: 市场类型
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            List[Dict[str, Any]]: 择时指标列表
        """
        try:
            data = self._load_data()
            timing_data = data.get('timing_indicators', [])

            # 过滤数据
            filtered_data = [
                item for item in timing_data
                if item.get('market') == market
            ]

            # 日期过滤
            if start_date:
                filtered_data = [
                    item for item in filtered_data
                    if item.get('date', '') >= start_date
                ]

            if end_date:
                filtered_data = [
                    item for item in filtered_data
                    if item.get('date', '') <= end_date
                ]

            # 按日期排序
            filtered_data.sort(key=lambda x: x.get('date', ''), reverse=True)

            return filtered_data

        except Exception as e:
            self.logger.error(f"获取择时指标失败: {e}")
            raise

    def _validate_macro_data(self, data: Dict[str, Any]):
        """验证宏观数据"""
        required_fields = ['date', 'market']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"宏观数据缺少必需字段: {field}")

    def _validate_market_sentiment_data(self, data: Dict[str, Any]):
        """验证市场情绪数据"""
        required_fields = ['date', 'market']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"市场情绪数据缺少必需字段: {field}")

    def _validate_industry_data(self, data: Dict[str, Any]):
        """验证行业数据"""
        required_fields = ['date', 'market', 'industry']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"行业数据缺少必需字段: {field}")

    def backup_data(self) -> bool:
        """备份数据"""
        try:
            if not config_manager.get('database.backup_enabled', True):
                return True

            backup_dir = Path('data/backups')
            backup_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = backup_dir / f"backup_{timestamp}.json"

            data = self._load_data()
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self.logger.info(f"数据备份成功: {backup_file}")
            return True

        except Exception as e:
            self.logger.error(f"数据备份失败: {e}")
            return False

    def save_ai_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        保存AI分析结果

        Args:
            analysis_data: AI分析数据

        Returns:
            Dict[str, Any]: 保存后的数据
        """
        try:
            # 添加时间戳
            analysis_data['created_at'] = datetime.now().isoformat()
            analysis_data['id'] = f"ai_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # 保存数据
            data = self._load_data()
            data['ai_analysis'].append(analysis_data)
            self._save_data(data)

            self.logger.info(f"保存AI分析结果: {analysis_data['id']}")
            return analysis_data

        except Exception as e:
            self.logger.error(f"保存AI分析结果失败: {e}")
            raise

    def get_ai_analysis(self, market: str, start_date: Optional[str] = None,
                       end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取AI分析数据

        Args:
            market: 市场类型
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            List[Dict[str, Any]]: AI分析数据列表
        """
        try:
            data = self._load_data()
            ai_data = data.get('ai_analysis', [])

            # 过滤数据
            filtered_data = [
                item for item in ai_data
                if item.get('market') == market
            ]

            # 日期过滤
            if start_date:
                filtered_data = [
                    item for item in filtered_data
                    if item.get('date', '') >= start_date
                ]

            if end_date:
                filtered_data = [
                    item for item in filtered_data
                    if item.get('date', '') <= end_date
                ]

            # 按日期排序
            filtered_data.sort(key=lambda x: x.get('date', ''), reverse=True)

            return filtered_data

        except Exception as e:
            self.logger.error(f"获取AI分析数据失败: {e}")
            raise