from app.services import *
from app.models import Usage
from django.db.models import Count

def create_usage(drug_title, bot_user):
    Usage.objects.create(
        drug_title=drug_title,
        bot_user=bot_user, 
        lang=bot_user.lang
    )
    return True

def count_usage_by_lang(from_, to):
    query = Usage.objects.filter(datetime__range=(from_, to)).values('lang').annotate(count=Count('lang'))
    result = {
        query_dict['lang']: query_dict['count'] for query_dict in query
    }
    result['uz'] = 0 if not 'uz' in result else result['uz']
    result['ru'] = 0 if not 'ru' in result else result['ru']
    return result

def count_usage_of_users_by_lang(from_, to):
    ru_users_count = Usage.objects.filter(bot_user__lang='ru', datetime__range=(from_, to)).values('bot_user').distinct().count()
    uz_users_count = Usage.objects.filter(bot_user__lang='uz', datetime__range=(from_, to)).values('bot_user').distinct().count()
    return {'ru': ru_users_count, 'uz': uz_users_count}

def filter_usage_drug_titles_count(from_, to):
    drug_title_counts = Usage.objects.filter(datetime__range=(from_, to)).values('drug_title').annotate(count=Count('drug_title')).order_by('-count')
    return drug_title_counts

def filter_usage_bot_users_count(from_, to):
    bot_users_counts = Usage.objects.filter(datetime__range=(from_, to)).values('bot_user').annotate(count=Count('bot_user')).values(
        'bot_user__name', 'bot_user__username', 'count'
        ).order_by('-count')
    return bot_users_counts