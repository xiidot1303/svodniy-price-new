from bot.models import Settings

async def is_registration_active():
    if setting := await Settings.objects.filter().afirst():
        return setting.registration
    else:
        return False