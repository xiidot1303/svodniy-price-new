import xlrd
from app.services.drug_service import (
    update_or_create_drug_by_data, 
    update_or_create_provider_by_data, 
)
from app.utils import fix_format_date_in_excel
from app.models import Excel
from datetime import datetime
import traceback

def get_last_excel():
    obj = Excel.objects.all().last()
    return obj

def read_excel_and_update_providers(file_url = 'files/prices.xls'):
    try:
        # open workbook
        book = xlrd.open_workbook(file_url)
        # set sheet2 that providers list
        sheet2 = book.sheet_by_index(0)

        ## READ PROVIDERS PAGE
        # get values of providers
        provider_values = [
            {
                'name': str(sheet2.cell_value(i, 1)).lower(),
                'phone': sheet2.cell_value(i, 2),
                'address': sheet2.cell_value(i, 3),
                'tg_id': str(sheet2.cell_value(i, 5)),
                'operators': sheet2.cell_value(i, 6)
            }
            for i in range(3, sheet2.nrows)
        ]
        # update or create objects
        update_or_create_provider_by_data(provider_values)

        return 1, ""
    except Exception as ex:
        full_tb = traceback.format_exc()
        return -1, full_tb


def read_excel_and_update_drugs(file_url = 'files/prices.xls'):
    try:
        # open workbook
        book = xlrd.open_workbook(file_url)
        # set sheet1 that drugs list
        sheet1 = book.sheet_by_index(0)

        ## READ DRUGS PAGE
        # get values of drugs
        drug_values = [
            {
                'title': sheet1.cell_value(i, 0), 'title_en': sheet1.cell_value(i, 1), 
                'term': fix_format_date_in_excel(sheet1.cell_value(i, 5)), 'price': str(sheet1.cell_value(i, 4)), 
                'provider_name': sheet1.cell_value(i, 6), 'manufacturer': sheet1.cell_value(i, 7), 
                'country': sheet1.cell_value(i, 8), 'atc': sheet1.cell_value(i, 9)
            }
            for i in range(2, sheet1.nrows)
            ]
        # update or create objects
        update_or_create_drug_by_data(drug_values)
        return 1, ""
    except Exception as ex:
        return -1, ex
