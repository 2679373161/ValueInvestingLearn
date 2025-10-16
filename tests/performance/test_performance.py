#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能测试
"""

import unittest
import time
import tempfile
import os
import json
from datetime import datetime, timedelta

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app import create_app


class TestPerformance(unittest.TestCase):
    """性能测试类"""

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

        # 创建大量测试数据
        self._create_large_test_data()

    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def _create_large_test_data(self):
        """创建大量测试数据用于性能测试"""
        # 创建365天的数据（一年）
        macro_data = []
        sentiment_data = []
        industry_data = []

        start_date = datetime(2023, 1, 1)
        for i in range(365):
            current_date = start_date + timedelta(days=i)
            date_str = current_date.strftime('%Y-%m-%d')

            # 宏观数据
            macro_data.append({
                "date": date_str,
                "market": "a_share",
                "pmi": 50.0 + (i % 10) - 5,  # 在45-55之间波动
                "cpi": 2.0 + (i % 20) * 0.1,  # 在2.0-3.9之间波动
                "ppi": 1.5 + (i % 15) * 0.1,  # 在1.5-2.9之间波动
                "m2": 8.0 + (i % 10) * 0.1,   # 在8.0-8.9之间波动
                "interest_rate": 3.0 + (i % 5) * 0.1  # 在3.0-3.4之间波动
            })

            # 市场情绪数据
            sentiment_data.append({
                "date": date_str,
                "market": "a_share",
                "volatility": 10.0 + (i % 20),  # 在10-29之间波动
                "investor_sentiment": 50.0 + (i % 40),  # 在50-89之间波动
                "technical_indicators": {
                    "rsi": 30.0 + (i % 50),  # 在30-79之间波动
                    "macd": -2.0 + (i % 8) * 0.5,  # 在-2.0到1.5之间波动
                    "bollinger_bands": 0.5 + (i % 15) * 0.1  # 在0.5-1.9之间波动
                }
            })

            # 行业数据（每5天一个数据点）
            if i % 5 == 0:
                industry_data.append({
                    "date": date_str,
                    "market": "a_share",
                    "industry": "technology",
                    "free_cash_flow": 100.0 + (i % 50),  # 在100-149之间波动
                    "industry_sentiment": 50.0 + (i % 40)  # 在50-89之间波动
                })

        # 写入测试数据文件
        with open(os.path.join(self.data_dir, 'macro_data.json'), 'w', encoding='utf-8') as f:
            json.dump(macro_data, f, ensure_ascii=False, indent=2)

        with open(os.path.join(self.data_dir, 'market_sentiment_data.json'), 'w', encoding='utf-8') as f:
            json.dump(sentiment_data, f, ensure_ascii=False, indent=2)

        with open(os.path.join(self.data_dir, 'industry_data.json'), 'w', encoding='utf-8') as f:
            json.dump(industry_data, f, ensure_ascii=False, indent=2)

    def test_api_response_time(self):
        """测试API响应时间"""
        endpoints_to_test = [
            ('/api/data/health', 'GET', None),
            ('/api/docs', 'GET', None),
            ('/api/data/macro?market=a_share&start_date=2023-01-01&end_date=2023-12-31', 'GET', None),
            ('/api/analysis/market-comparison', 'GET', None),
        ]

        max_response_time = 2.0  # 最大允许响应时间（秒）

        for endpoint, method, data in endpoints_to_test:
            start_time = time.time()

            if method == 'GET':
                response = self.client.get(endpoint)
            elif method == 'POST':
                response = self.client.post(endpoint, json=data)

            end_time = time.time()
            response_time = end_time - start_time

            self.assertEqual(response.status_code, 200, f"{endpoint} 返回状态码 {response.status_code}")
            self.assertLessEqual(response_time, max_response_time,
                               f"{endpoint} 响应时间 {response_time:.3f}s 超过限制 {max_response_time}s")

            print(f"{endpoint}: {response_time:.3f}s")

    def test_concurrent_requests(self):
        """测试并发请求性能"""
        import threading

        results = []
        errors = []

        def make_request(endpoint, method, data):
            try:
                start_time = time.time()

                if method == 'GET':
                    response = self.client.get(endpoint)
                elif method == 'POST':
                    response = self.client.post(endpoint, json=data)

                end_time = time.time()
                response_time = end_time - start_time

                results.append({
                    'endpoint': endpoint,
                    'response_time': response_time,
                    'status_code': response.status_code
                })
            except Exception as e:
                errors.append(f"{endpoint}: {str(e)}")

        # 创建并发请求
        threads = []
        endpoints = [
            ('/api/data/health', 'GET', None),
            ('/api/docs', 'GET', None),
            ('/api/data/macro?market=a_share&start_date=2023-01-01&end_date=2023-01-31', 'GET', None),
            ('/api/analysis/market-comparison', 'GET', None),
        ]

        # 每个端点创建3个并发请求
        for endpoint, method, data in endpoints:
            for _ in range(3):
                thread = threading.Thread(target=make_request, args=(endpoint, method, data))
                threads.append(thread)

        # 启动所有线程
        for thread in threads:
            thread.start()

        # 等待所有线程完成
        for thread in threads:
            thread.join()

        # 检查结果
        self.assertEqual(len(errors), 0, f"并发请求中出现错误: {errors}")

        # 计算平均响应时间
        avg_response_time = sum(r['response_time'] for r in results) / len(results)
        max_response_time = max(r['response_time'] for r in results)

        print(f"并发测试结果:")
        print(f"  总请求数: {len(results)}")
        print(f"  平均响应时间: {avg_response_time:.3f}s")
        print(f"  最大响应时间: {max_response_time:.3f}s")

        # 验证所有请求都成功
        for result in results:
            self.assertEqual(result['status_code'], 200,
                           f"{result['endpoint']} 返回状态码 {result['status_code']}")

    def test_large_data_processing(self):
        """测试大数据量处理性能"""
        # 测试获取一年数据
        start_time = time.time()

        response = self.client.get('/api/data/macro?market=a_share&start_date=2023-01-01&end_date=2023-12-31')

        end_time = time.time()
        response_time = end_time - start_time

        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        # 验证返回了正确的数据量
        self.assertEqual(len(data), 365)

        # 响应时间应该在合理范围内
        max_response_time = 3.0  # 3秒内处理365条数据
        self.assertLessEqual(response_time, max_response_time,
                           f"大数据量处理时间 {response_time:.3f}s 超过限制 {max_response_time}s")

        print(f"大数据量处理测试:")
        print(f"  数据量: {len(data)} 条")
        print(f"  处理时间: {response_time:.3f}s")

    def test_timing_indicators_calculation_performance(self):
        """测试择时指标计算性能"""
        # 测试多个日期的择时指标计算
        dates_to_test = [
            "2023-01-15",
            "2023-03-15",
            "2023-06-15",
            "2023-09-15",
            "2023-12-15"
        ]

        total_time = 0
        successful_calculations = 0

        for date in dates_to_test:
            request_data = {
                "market": "a_share",
                "date": date
            }

            start_time = time.time()
            response = self.client.post('/api/analysis/timing-indicators', json=request_data)
            end_time = time.time()

            if response.status_code == 200:
                total_time += (end_time - start_time)
                successful_calculations += 1

            self.assertEqual(response.status_code, 200, f"日期 {date} 计算失败")

        avg_calculation_time = total_time / successful_calculations
        max_calculation_time = 1.0  # 单次计算最大允许时间

        self.assertLessEqual(avg_calculation_time, max_calculation_time,
                           f"平均择时指标计算时间 {avg_calculation_time:.3f}s 超过限制 {max_calculation_time}s")

        print(f"择时指标计算性能测试:")
        print(f"  成功计算次数: {successful_calculations}")
        print(f"  平均计算时间: {avg_calculation_time:.3f}s")

    def test_memory_usage(self):
        """测试内存使用情况"""
        import psutil
        import os

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # 执行一些操作
        for i in range(100):
            response = self.client.get('/api/data/macro?market=a_share&start_date=2023-01-01&end_date=2023-01-31')
            self.assertEqual(response.status_code, 200)

        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        # 内存增长应该在合理范围内
        max_memory_increase = 50  # MB
        self.assertLessEqual(memory_increase, max_memory_increase,
                           f"内存增长 {memory_increase:.2f}MB 超过限制 {max_memory_increase}MB")

        print(f"内存使用测试:")
        print(f"  初始内存: {initial_memory:.2f}MB")
        print(f"  最终内存: {final_memory:.2f}MB")
        print(f"  内存增长: {memory_increase:.2f}MB")


if __name__ == '__main__':
    unittest.main()