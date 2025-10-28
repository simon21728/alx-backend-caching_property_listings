from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

# Existing low-level caching function
def get_all_properties():
    queryset = cache.get('all_properties')
    if not queryset:
        queryset = Property.objects.all()
        cache.set('all_properties', queryset, 3600)  # cache for 1 hour
    return queryset

# New function: get Redis cache metrics
def get_redis_cache_metrics():
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info("stats")
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        hit_ratio = hits / (hits + misses)  

        metrics = {
            "keyspace_hits": hits,
            "keyspace_misses": misses,
            "hit_ratio": hit_ratio
        }

        logger.info(f"Redis cache metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error fetching Redis metrics: {e}")
        return {"keyspace_hits": 0, "keyspace_misses": 0, "hit_ratio": 0.0}

def get_all_properties():
    # Try fetching from Redis
    properties = cache.get('all_properties')
    
    if properties is None:
        # Not in cache, fetch from DB
        properties = list(Property.objects.all().values(
            'id', 'title', 'description', 'price', 'address'
        ))
        # Store in Redis for 1 hour
        cache.set('all_properties', properties, 3600)
    
    return properties
