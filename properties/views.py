from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_page
from .models import Property  # Make sure you have a Property model
from django.http import JsonResponse
from .utils import get_all_properties

def property_list(request):
    properties = get_all_properties()
    return JsonResponse({"data": properties})

# Cache the view for 15 minutes (60 sec * 15)
@cache_page(60 * 15)
def property_list(request):
    properties = Property.objects.all().values(
        'id', 'title', 'description', 'price', 'address'
    )
    
    return JsonResponse({"data": properties})
