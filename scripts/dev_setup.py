#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开发环境设置脚本

用于快速设置开发环境和验证配置
"""

import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")

    if version.major == 3 and version.minor >= 9:
        print("[OK] Python版本符合要求")
        return True
    else:
        print("[ERROR] Python版本过低，需要3.9或更高版本")
        return False


def check_dependencies():
    """检查关键依赖"""
    dependencies = [
        ("Flask", "flask"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("requests", "requests"),
    ]

    all_installed = True
    for name, package in dependencies:
        try:
            __import__(package)
            print(f"[OK] {name} 已安装")
        except ImportError:
            print(f"[ERROR] {name} 未安装")
            all_installed = False

    return all_installed


def check_project_structure():
    """检查项目结构"""
    required_dirs = [
        "app",
        "app/routes",
        "app/services",
        "app/models",
        "app/utils",
        "frontend/src",
        "frontend/src/components",
        "frontend/src/services",
        "tests",
        "config",
        "data",
        "docs",
    ]

    all_exists = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"[OK] 目录存在: {dir_path}")
        else:
            print(f"[ERROR] 目录缺失: {dir_path}")
            all_exists = False

    return all_exists


def main():
    """主函数"""
    print("量化择时指标应用 - 开发环境检查")
    print("=" * 50)

    # 检查Python版本
    print("\n1. 检查Python环境:")
    python_ok = check_python_version()

    # 检查依赖
    print("\n2. 检查Python依赖:")
    deps_ok = check_dependencies()

    # 检查项目结构
    print("\n3. 检查项目结构:")
    structure_ok = check_project_structure()

    print("\n" + "=" * 50)
    if python_ok and deps_ok and structure_ok:
        print("开发环境检查通过！可以开始开发。")
        return 0
    else:
        print("开发环境存在问题，请检查上述错误。")
        return 1


if __name__ == "__main__":
    sys.exit(main())