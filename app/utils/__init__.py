from datetime import datetime, date, timedelta
import requests
import json
from transliterate import translit
from asgiref.sync import async_to_sync, sync_to_async

def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

async def datetime_now():
    now = datetime.now()
    return now

async def time_now():
    now = datetime.now()
    return now.time()

async def today():
    today = date.today()
    return today

def fix_format_date_in_excel(value):
    try:
        n = int(value)
        result = (date(1899, 12, 30) + timedelta(days=n)).strftime("%d.%m.%Y")
    except:
        result = value
    return result

async def send_request(url, data=None, headers=None, type='get'):
    if type == 'get':
        response = requests.get(url, params=data, headers=headers)
        content = json.loads(response.content)
        headers = response.headers
    else:
        response = requests.post(url, json=data, headers=headers)
        content = json.loads(response.content)
        headers = response.headers

    return content, headers

async def prepare_drug_words(text):
    async def regexing_en(text):
        list_couples = [
            'ao', 'xh', 'ie', 'qk', 'cs', 'jy', 'kc'
        ]

        for i in list_couples:
            text = text.replace(i[0], f'({i[0]}|{i[1]})')
            text = text.replace(i[1], f'({i[0]}|{i[1]})')
            text = text.replace(f'{i[0]}|({i[0]}|{i[1]})', f'{i[0]}|{i[1]}')

        return text

    async def regexing_ru(text):
        list_couples = [
            'ао', 'её', 'ыи', 'юу', 'щш', 'сц', ['л', 'ль'], ['н', 'нь'], 
            ['ш', 'шь'], ['д', 'дь'], ['м', 'мь'], ['т', 'ть'], ['б', 'бь'],
        ]

        for i in list_couples:
            text = text.replace(i[0], f'({i[0]}|{i[1]})')
            text = text.replace(i[1], f'({i[0]}|{i[1]})')
            text = text.replace(f'{i[0]}|({i[0]}|{i[1]})', f'{i[0]}|{i[1]}')

        return text
    text = text.capitalize()
    text_ru = await sync_to_async(translit)(text, 'ru')
    text_en = await sync_to_async(translit)(text, 'ru', reversed=True)
    new_text = text.replace('-', ' ')
    # split words and add regexing in 2 lang
    words = []
    for word in new_text.split():
        words.append(
            [
                await regexing_en(await sync_to_async(translit)(word, 'ru', reversed=True)),
                await regexing_ru(await sync_to_async(translit)(word, 'ru')),
            ]
        )
    
    return words, text_en, text_ru, text