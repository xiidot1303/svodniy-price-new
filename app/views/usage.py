from app.views import *
from app.services.usage_service import *

@login_required
def usage_rate(request):
    # get params from request
    params = request.GET
    # get from_date from params 
    from_date = str(request.GET['from']) if 'from' in params else ''
    # change format of from_date
    m, d, y = from_date.split('/') if from_date else (1, 1, 1000)
    print(m)
    from_ = f"{y}-{m}-{d}"
    print(from_)

    # get to_date from params
    to_date = str(request.GET['to']) if 'to' in params else ''
    # change format of to_date
    m, d, y = to_date.split('/') if to_date else (1, 1, 3000)
    to = f"{y}-{m}-{d}"
    # filter usages
    searches_count = count_usage_by_lang(from_, to)
    searched_users_count = count_usage_of_users_by_lang(from_, to)
    drugs_count_list = filter_usage_drug_titles_count(from_, to)
    bot_users_count_list = filter_usage_bot_users_count(from_, to)
    context = {
        'searches_count': searches_count, 'searched_users_count': searched_users_count,
        'drugs_count_list': drugs_count_list, 'bot_users_count_list': bot_users_count_list,
        'from_date': from_date, 'to_date': to_date
        }
    return render(request, 'usage/usage_rate.html', context)