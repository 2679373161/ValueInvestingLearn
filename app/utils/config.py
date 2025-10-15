#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块

负责加载、验证和管理应用配置
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.logger = logging.getLogger(__name__)

    def load_config(self) -> bool:
        """
        加载配置文件

        Returns:
            bool: 是否成功加载配置
        """
        try:
            if not self.config_path.exists():
                self.logger.warning(f"配置文件不存在: {self.config_path}")
                self._create_default_config()
                return False

            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)

            self.logger.info(f"成功加载配置文件: {self.config_path}")
            return True

        except json.JSONDecodeError as e:
            self.logger.error(f"配置文件格式错误: {e}")
            return False
        except Exception as e:
            self.logger.error(f"加载配置文件失败: {e}")
            return False

    def _create_default_config(self):
        """创建默认配置文件"""
        try:
            # 确保配置目录存在
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            # 读取模板文件
            template_path = Path("config/config.template.json")
            if template_path.exists():
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_config = json.load(f)

                # 写入默认配置
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(template_config, f, indent=2, ensure_ascii=False)

                self.logger.info(f"已创建默认配置文件: {self.config_path}")
                self.logger.warning("请修改配置文件中的敏感信息（如API密钥）")
            else:
                self.logger.error("配置模板文件不存在")

        except Exception as e:
            self.logger.error(f"创建默认配置文件失败: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键，支持点分隔符（如 "app.name"）
            default: 默认值

        Returns:
            Any: 配置值
        """
        keys = key.split('.')
        value = self.config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any) -> bool:
        """
        设置配置值

        Args:
            key: 配置键
            value: 配置值

        Returns:
            bool: 是否成功设置
        """
        try:
            keys = key.split('.')
            config = self.config

            # 遍历到最后一个键的父级
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]

            # 设置值
            config[keys[-1]] = value
            return True

        except Exception as e:
            self.logger.error(f"设置配置失败: {e}")
            return False

    def save_config(self) -> bool:
        """
        保存配置到文件

        Returns:
            bool: 是否成功保存
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)

            self.logger.info(f"配置已保存到: {self.config_path}")
            return True

        except Exception as e:
            self.logger.error(f"保存配置失败: {e}")
            return False

    def validate_config(self) -> Dict[str, list]:
        """
        验证配置完整性

        Returns:
            Dict[str, list]: 验证结果，包含错误和警告
        """
        errors = []
        warnings = []

        # 检查必需配置
        required_keys = [
            "app.name",
            "app.secret_key",
            "server.port",
            "timing_indicators.weights.macro_fundamental",
            "timing_indicators.weights.industry_fundamental",
            "timing_indicators.weights.market_sentiment"
        ]

        for key in required_keys:
            if self.get(key) is None:
                errors.append(f"缺少必需配置: {key}")

        # 检查权重总和
        weights = self.get("timing_indicators.weights")
        if weights:
            total_weight = sum(weights.values())
            if abs(total_weight - 1.0) > 0.01:
                warnings.append(f"择时指标权重总和应为1.0，当前为: {total_weight}")

        # 检查API密钥
        ai_api_key = self.get("ai.api_key")
        if not ai_api_key or ai_api_key == "your-deepseek-api-key-here":
            warnings.append("AI API密钥未配置，AI功能将无法使用")

        # 检查数据目录
        data_path = self.get("database.file_path")
        if data_path:
            data_dir = Path(data_path).parent
            if not data_dir.exists():
                warnings.append(f"数据目录不存在: {data_dir}")

        return {
            "errors": errors,
            "warnings": warnings
        }

    def get_timing_weights(self) -> Dict[str, float]:
        """获取择时指标权重"""
        return self.get("timing_indicators.weights", {})

    def get_market_config(self, market: str) -> Dict[str, Any]:
        """获取特定市场配置"""
        return self.get(f"markets.{market}", {})

    def get_ai_config(self) -> Dict[str, Any]:
        """获取AI配置"""
        return self.get("ai", {})


# 全局配置实例
config_manager = ConfigManager()


def init_config() -> bool:
    """
    初始化配置

    Returns:
        bool: 是否成功初始化
    """
    if not config_manager.load_config():
        return False

    # 验证配置
    validation = config_manager.validate_config()

    if validation["errors"]:
        logger = logging.getLogger(__name__)
        for error in validation["errors"]:
            logger.error(error)
        return False

    if validation["warnings"]:
        logger = logging.getLogger(__name__)
        for warning in validation["warnings"]:
            logger.warning(warning)

    return True