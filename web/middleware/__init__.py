"""
中间件：错误处理、日志、CORS等
"""

from .error_handler import add_error_handlers

__all__ = ["add_error_handlers"]
