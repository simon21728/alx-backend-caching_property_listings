from django.core.cache import cache
from .models import Property

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
