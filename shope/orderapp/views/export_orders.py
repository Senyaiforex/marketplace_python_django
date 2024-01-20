from io import BytesIO

from django.http import HttpRequest, HttpResponse
import pandas as pd

from repositories import OrderRepository

_order_repository = OrderRepository()


def export_orders_to_xls(request: HttpRequest)\
        -> HttpResponse:
    orders = _order_repository.get_orders_by_user_id(
        user_id=request.user.id
    )
    excel_file = BytesIO()
    excel_writer = pd.ExcelWriter(excel_file)
    result = dict()
    for order in orders:
        for name_field in order._meta.fields:
            if name_field.name not in result.keys():
                result[name_field.name] = list()
            if name_field.name not in (
                    "created_at",
                    "updated_at",
            ):
                result[name_field.name].append(
                    order.__getattribute__(str(name_field.name))
                )
            else:
                result[name_field.name].append(order.__getattribute__(
                    str(name_field.name)).isoformat(sep=" ")
                                               )

    df = pd.DataFrame(
        result
    )
    df.to_excel(excel_writer, sheet_name='orders')

    excel_writer.close()
    excel_file.seek(0)

    response = HttpResponse(
        excel_file.read(),
        content_type='application/vnd.openxmlformats-'
                     'officedocument.spreadsheetml.sheet',
    )
    response[
        'Content-Disposition'
    ] = 'attachment; filename=orders.xlsx'
    response['Set-Cookie'] = 'fileDownload=true; path=/'
    return response
