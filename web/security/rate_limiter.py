"""
速率限制器 - 防止滥用和DoS攻击
"""

import time
from collections import defaultdict, deque
from threading import Lock
from typing import Dict, Deque, Tuple


class RateLimiter:
    """基于滑动窗口的速率限制器"""
    
    def __init__(self, max_per_minute: int = 30, max_per_hour: int = 500):
        """
        初始化速率限制器
        
        Args:
            max_per_minute: 每分钟最大请求数
            max_per_hour: 每小时最大请求数
        """
        self.max_per_minute = max_per_minute
        self.max_per_hour = max_per_hour
        
        # 存储每个IP的请求时间戳
        self.requests: Dict[str, Deque[float]] = defaultdict(deque)
        self.lock = Lock()
    
    def is_allowed(self, client_id: str) -> Tuple[bool, str]:
        """
        检查是否允许请求
        
        Args:
            client_id: 客户端标识（通常是IP地址）
        
        Returns:
            (是否允许, 拒绝原因)
        """
        with self.lock:
            now = time.time()
            
            # 清理过期的请求记录
            self._cleanup_old_requests(client_id, now)
            
            # 检查分钟级限制
            minute_ago = now - 60
            recent_requests = [t for t in self.requests[client_id] if t > minute_ago]
            if len(recent_requests) >= self.max_per_minute:
                return False, f"超过速率限制：每分钟最多{self.max_per_minute}次请求"
            
            # 检查小时级限制
            hour_ago = now - 3600
            hourly_requests = [t for t in self.requests[client_id] if t > hour_ago]
            if len(hourly_requests) >= self.max_per_hour:
                return False, f"超过速率限制：每小时最多{self.max_per_hour}次请求"
            
            # 记录本次请求
            self.requests[client_id].append(now)
            
            return True, ""
    
    def _cleanup_old_requests(self, client_id: str, now: float):
        """清理1小时前的请求记录"""
        hour_ago = now - 3600
        while self.requests[client_id] and self.requests[client_id][0] < hour_ago:
            self.requests[client_id].popleft()
    
    def get_stats(self, client_id: str) -> Dict[str, int]:
        """获取客户端的请求统计"""
        with self.lock:
            now = time.time()
            minute_ago = now - 60
            hour_ago = now - 3600
            
            requests = self.requests.get(client_id, deque())
            
            return {
                "last_minute": len([t for t in requests if t > minute_ago]),
                "last_hour": len([t for t in requests if t > hour_ago]),
                "remaining_minute": max(0, self.max_per_minute - len([t for t in requests if t > minute_ago])),
                "remaining_hour": max(0, self.max_per_hour - len([t for t in requests if t > hour_ago])),
            }
    
    def reset(self, client_id: str = None):
        """重置限制（用于测试或管理）"""
        with self.lock:
            if client_id:
                self.requests.pop(client_id, None)
            else:
                self.requests.clear()


# 全局速率限制器实例
rate_limiter = RateLimiter(max_per_minute=30, max_per_hour=500)

