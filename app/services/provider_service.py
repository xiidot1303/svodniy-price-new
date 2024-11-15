from app.services import *
from app.models import Provider


async def get_provider_by_name_contains(name):
    name = name.replace(' - ', '-')
    obj = await Provider.objects.filter(name__contains=name.lower()).afirst()
    return obj


async def filter_provider_by_name(name: str) -> dict:
    filter_dict = {
        "name__icontains": name
    }
    return filter_dict
