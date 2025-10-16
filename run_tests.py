#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试运行脚本

运行所有测试：python run_tests.py
运行单元测试：python run_tests.py unit
运行集成测试：python run_tests.py integration
运行性能测试：python run_tests.py performance
"""

import sys
import os
import unittest
import argparse


def run_unit_tests():
    """运行单元测试"""
    print("\n=== 运行单元测试 ===")
    loader = unittest.TestLoader()
    suite = loader.discover('tests/unit', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def run_integration_tests():
    """运行集成测试"""
    print("\n=== 运行集成测试 ===")
    loader = unittest.TestLoader()
    suite = loader.discover('tests/integration', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def run_performance_tests():
    """运行性能测试"""
    print("\n=== 运行性能测试 ===")
    loader = unittest.TestLoader()
    suite = loader.discover('tests/performance', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def run_all_tests():
    """运行所有测试"""
    print("=== 运行所有测试 ===")

    unit_success = run_unit_tests()
    integration_success = run_integration_tests()
    performance_success = run_performance_tests()

    all_success = unit_success and integration_success and performance_success

    print("\n=== 测试结果汇总 ===")
    print(f"单元测试: {'通过' if unit_success else '失败'}")
    print(f"集成测试: {'通过' if integration_success else '失败'}")
    print(f"性能测试: {'通过' if performance_success else '失败'}")
    print(f"总体结果: {'所有测试通过' if all_success else '有测试失败'}")

    return all_success


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='运行量化择时指标应用测试')
    parser.add_argument('test_type', nargs='?', default='all',
                       choices=['all', 'unit', 'integration', 'performance'],
                       help='测试类型: all, unit, integration, performance')

    args = parser.parse_args()

    # 添加项目根目录到Python路径
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    success = False

    if args.test_type == 'all':
        success = run_all_tests()
    elif args.test_type == 'unit':
        success = run_unit_tests()
    elif args.test_type == 'integration':
        success = run_integration_tests()
    elif args.test_type == 'performance':
        success = run_performance_tests()

    # 根据测试结果退出
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()