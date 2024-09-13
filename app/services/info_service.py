from app.models import Info

def get_info():
    if info_query := Info.objects.all():
        info = info_query.first()
    else:
        info = None
    return info