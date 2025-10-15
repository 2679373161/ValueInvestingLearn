import pytest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import create_app


@pytest.fixture
def app():
    """创建测试应用实例"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()