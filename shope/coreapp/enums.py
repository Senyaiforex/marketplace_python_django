from django.utils.translation import gettext as _

# Статусы платежа
PENDING_STATUS = 'pending'
WAITING_FOR_CAPTURE_STATUS = 'waiting for capture'
CANCELED_STATUS = 'canceled'
SUCCEDED_STATUS = 'succeeded'

PAYMENT_STATUSES = (
    (PENDING_STATUS, _('Created by')),
    (WAITING_FOR_CAPTURE_STATUS, _('Pending write-off')),
    (CANCELED_STATUS, _('Cancelled')),
    (SUCCEDED_STATUS, _('Successfully completed')))

# Статусы заказа
PAID_STATUS = 'paid'
NOT_PAID_STATUS = 'not paid'

ORDER_STATUSES = (
    (PAID_STATUS, _('Paid')),
    (NOT_PAID_STATUS, _('Not paid for'))
)

# Способы сортировки
SORT_TYPES = ('new', '-new',
              'popular', '-popular',
              'price', '-price',
              'reviews', '-reviews')

# Типы доставки
DEFAULT = 'Default delivery'
EXPRESS = 'Express delivery'

DELIVERY_TYPE = (
    (DEFAULT, _('Default delivery')),
    (EXPRESS, _('Express delivery'))
)
