from app.services import *
from app.models import Drug, Provider
from django.db.models import Case, When, Value, IntegerField

def update_or_create_drug_by_data(values):
    # filter drugs already same with database and excel
    # Create a Q object for each dict in values
    # queries = [Q(**item) for item in values]
    
    # # Combine the Q objects using OR
    # q_object = queries.pop()
    # for query in queries:
    #     q_object |= query
    # existing_drugs = Drug.objects.filter(q_object).values_list(
    #                 'title', 'title_en', 'term', 'price', 
    #                 'provider_name', 'manufacturer', 'country'
    #             )
    # existing_drugs = Drug.objects.filter(
    #         title__in=[v['title'] for v in values], 
    #         title_en__in=[v['title_en'] for v in values], 
    #         term__in=[v['term'] for v in values], 
    #         price__in=[v['price'] for v in values],  
    #         provider_name__in=[v['provider_name'] for v in values],
    #         manufacturer__in=[v['manufacturer'] for v in values], 
    #         country__in=[v['country'] for v in values], 
    #     ).values_list(
    #                 'title', 'title_en', 'term', 'price', 
    #                 'provider_name', 'manufacturer', 'country'
    #             )

    # filter drugs which is not used in excel
    # deleting_drugs = Drug.objects.exclude(
    #         pk__in = existing_drugs.values_list('pk', flat=True)
    #     )

    # create models that are not available database
    # existing_drugs_set = set(existing_drugs)
    new_drugs = [
        Drug(
            title=value['title'], 
            title_en=value['title_en'], 
            term=value['term'], 
            price=value['price'], 
            provider_name=value['provider_name'], 
            manufacturer=value['manufacturer'], 
            country=value['country'], 
            atc=value['atc'],
            ) 
            for value in values 
            # if tuple(value.values()) not in existing_drugs_set
        ]
    
    # Delete unused drugs
    # deleting_drugs.delete()
    Drug.objects.all().delete()

    # Create drugs by data
    Drug.objects.bulk_create(new_drugs)


def get_drug_by_pk(pk):
    obj = get_object_or_404(Drug, pk=pk)
    return obj

def delete_drugs_which_is_not_in_list(l):
    drugs = Drug.objects.exclude(pk__in=l)
    drugs.delete()

def filter_drugs_by_title(title):
    query = Drug.objects.filter(title = title)
    return query

def filter_drugs_by_title_regex(words, text_en, text_ru, text):
    drugs = Drug.objects.filter(
        # Q(title__iregex=text_en) | Q(title__iregex=text_ru) | Q(title__icontains=text) |
        # Q(title_en__iregex=text_en) | Q(title_en__iregex=text_ru) | Q(title_en__icontains=text)
        )
    for word in words:
        drugs = drugs.filter(
            Q(title__iregex=word[0]) | Q(title__iregex=word[1]) |
            Q(title_en__iregex=word[0]) |
            Q(atc__iregex=word[0]) | Q(atc__iregex=word[1])
        )
    drugs = drugs.distinct('title').values_list('pk', flat=True)
    drugs = Drug.objects.filter(pk__in=drugs).annotate(
        order_index=Case(
            When(title=text, then=Value(1)),
            When(title__startswith=text_ru, then=Value(2)),
            When(title__startswith=text_ru[:3] if text_ru else '', then=Value(3)),
            When(title__startswith=text_ru[:2] if text_ru else '', then=Value(3.1)),
            When(title__startswith=text_ru[0] if text_ru else '', then=Value(3.2)),
            When(title__icontains=text_ru, then=Value(4)),
            When(title_en__startswith=text_en, then=Value(5)),
            When(title_en__icontains=text_en, then=Value(6)),
            When(atc__startswith=text_en, then=Value(7)),
            When(atc__icontains=text_ru, then=Value(8)),
            default=Value(100), output_field=IntegerField(),  
        )
    )
    drugs = drugs.order_by('order_index', 'title')
    return drugs

def delete_drugs_all():
    for drug in Drug.objects.all():
        drug.delete()

def get_max_and_min_price_of_drugs_query(query):
    import re
    prices = query.values_list('price', flat=True)
    pattern = r'\d+(\.\d+)?'
    new_prices = [float(element) for element in prices if re.match(pattern, element)]
    try:
        return max(new_prices), min(new_prices)
    except:
        return '', ''
### PROVER SERVICE
def update_or_create_provider_by_data(values):
    # filter providers already same with database and excel
    existing_providers = Provider.objects.filter(
            name__in=[v['name'] for v in values], 
            phone__in=[v['phone'] for v in values], 
            address__in=[v['address'] for v in values], 
        ).values_list(
                    'name', 'phone', 'address'
                )

    # filter providers which is not used in excel
    deleting_providers = Provider.objects.exclude(
            pk__in = existing_providers.values_list('pk', flat=True)
        )

    # create models that are not available database
    existing_providers_set = set(existing_providers)
    new_providers = [
        Provider(
            name=value['name'], 
            phone=value['phone'], 
            address=value['address'],
            ) 
            for value in values 
            if tuple(value.values()) not in existing_providers_set
        ]
    
    # Delete unused providers
    deleting_providers.delete()

    # Create providers by data
    Provider.objects.bulk_create(new_providers)



def get_provider_by_name_contains(name):
    name = name.replace(' - ', '-')
    filter = Provider.objects.filter(name__contains = name.lower())
    return filter[0] if filter else None

def delete_providers_all():
    for provider in Provider.objects.all():
        provider.delete()