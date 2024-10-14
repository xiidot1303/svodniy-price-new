from app.models import Info

async def get_info():
    info  = await Info.objects.filter().afirst()
    return info