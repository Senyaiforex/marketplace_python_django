from io import BytesIO
from django.http import HttpRequest, HttpResponse
import pandas as pd
from repositories import ProductSelectRepository

_product_repository = ProductSelectRepository()


def export_product_to_xls(request: HttpRequest) \
        -> HttpResponse:
    products = _product_repository.get_all_products()
    excel_file = BytesIO()
    excel_writer = pd.ExcelWriter(excel_file)
    result = dict()
    for product in products:
        for name_field in product._meta.fields:
            if name_field.name not in result.keys():
                result[name_field.name] = list()
            if name_field.name not in (
                    "created_at",
                    "updated_at",
            ):
                result[name_field.name].append(
                    product.__getattribute__(str(name_field.name))
                )
            else:
                result[name_field.name].append(
                    product.__getattribute__(
                        str(name_field.name)
                    ).isoformat(sep=" ")
                )
    df = pd.DataFrame(
        result
    )
    df.to_excel(excel_writer, sheet_name='products')
    excel_writer.close()
    excel_file.seek(0)

    response = HttpResponse(
        excel_file.read(),
        content_type='application/vnd.openxmlformats-'
                     'officedocument.spreadsheetml.sheet',
    )
    response[
        'Content-Disposition'
    ] = 'attachment; filename=products.xlsx'
    response['Set-Cookie'] = 'fileDownload=true; path=/'
    return response
