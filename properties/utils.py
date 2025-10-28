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
    redis_conn = get_redis_connection("default")
    stats = redis_conn.info("stats")
    hits = stats.get("keyspace_hits", 0)
    misses = stats.get("keyspace_misses", 0)

    hit_ratio = hits / (hits + misses)  # no conditional

    metrics = {
        "keyspace_hits": hits,
        "keyspace_misses": misses,
        "hit_ratio": hit_ratio
    }

    logger.info(f"Redis cache metrics: {metrics}")
    return metrics

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
