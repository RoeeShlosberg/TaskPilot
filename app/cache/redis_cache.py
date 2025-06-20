import redis
import json
import hashlib
from typing import Optional, Any
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class RedisCache:
    """Redis cache implementation for AI responses"""
    
    def __init__(self):
        self.redis_client = None
        self._connect()
    
    def _connect(self):
        """Connect to Redis with error handling"""
        try:
            self.redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                password=settings.redis_password if settings.redis_password else None,
                db=settings.redis_db,
                decode_responses=True,
                socket_connect_timeout=5,  # Set a timeout for connection attempts
                socket_timeout=5  # Set a timeout for operations
            )
            # Test connection
            self.redis_client.ping()
            logger.info("Redis connection established successfully")
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {e}")
            self.redis_client = None
    
    def _generate_cache_key(self, endpoint: str, task_data: dict) -> str:
        """Generate a unique cache key based on endpoint and task data"""
        # Create a hash of the task data for consistent keys
        task_str = json.dumps(task_data, sort_keys=True)
        task_hash = hashlib.md5(task_str.encode()).hexdigest()
        return f"ai_cache:{endpoint}:{task_hash}"
    
    def get(self, endpoint: str, task_data: dict) -> Optional[Any]:
        """Get cached AI response"""
        if not self.redis_client:
            return None
        
        try:
            cache_key = self._generate_cache_key(endpoint, task_data)
            cached_data = self.redis_client.get(cache_key)
            
            if cached_data:
                logger.info(f"Cache hit for {endpoint}")
                return json.loads(cached_data)
            
            logger.info(f"Cache miss for {endpoint}")
            return None
            
        except Exception as e:
            logger.error(f"Error getting from cache: {e}")
            return None
    
    def set(self, endpoint: str, task_data: dict, response: Any) -> bool:
        """Set AI response in cache"""
        if not self.redis_client:
            return False
        
        try:
            cache_key = self._generate_cache_key(endpoint, task_data)
            cached_data = json.dumps(response)
            
            self.redis_client.setex(
                cache_key,
                settings.redis_ttl,
                cached_data
            )
            
            logger.info(f"Cached response for {endpoint}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return False
    
    def delete(self, endpoint: str, task_data: dict) -> bool:
        """Delete specific cached response"""
        if not self.redis_client:
            return False
        
        try:
            cache_key = self._generate_cache_key(endpoint, task_data)
            result = self.redis_client.delete(cache_key)
            return bool(result)
            
        except Exception as e:
            logger.error(f"Error deleting from cache: {e}")
            return False
    
    def clear_all(self) -> bool:
        """Clear all AI cache entries"""
        if not self.redis_client:
            return False
        
        try:
            keys = self.redis_client.keys("ai_cache:*")
            if keys:
                self.redis_client.delete(*keys)
                logger.info(f"Cleared {len(keys)} cache entries")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False
    
    def get_cache_stats(self) -> dict:
        """Get cache statistics"""
        if not self.redis_client:
            return {"connected": False, "total_keys": 0}
        
        try:
            keys = self.redis_client.keys("ai_cache:*")
            return {
                "connected": True,
                "total_keys": len(keys),
                "memory_usage": self.redis_client.info("memory")["used_memory_human"],
                "redis_version": self.redis_client.info("server")["redis_version"]
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"connected": False, "error": str(e)}


# Global cache instance
cache = RedisCache()
