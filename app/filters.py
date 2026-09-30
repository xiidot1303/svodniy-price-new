from datetime import datetime, time, timedelta

from django.contrib.admin import ListFilter


class OrderDateRangeFilter(ListFilter):
    """From/to date range over the parent Order's datetime.

    OrderItem has no date of its own, so the range is applied to
    ``order__datetime`` (indexed). Datetimes are naive local time
    (USE_TZ = False), so the bounds are built as plain datetimes.

    Subclasses ListFilter rather than SimpleListFilter because this filter
    owns two query params instead of one: SimpleListFilter.__init__ only
    pops `parameter_name`, leaving date_from/date_to unclaimed, which makes
    the changelist raise IncorrectLookupParameters and redirect to ?e=1.
    """

    title = 'Дата заказа'
    template = 'admin/date_range_filter.html'

    date_from_param = 'date_from'
    date_to_param = 'date_to'

    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)
        # claim our params so the changelist does not treat them as
        # unrecognised lookups
        for param in self.expected_parameters():
            if param in params:
                self.used_parameters[param] = params.pop(param)

    def expected_parameters(self):
        return [self.date_from_param, self.date_to_param]

    def has_output(self):
        return True

    def value(self, param):
        value = self.used_parameters.get(param)
        # Django >= 5 hands filters a list of values per param
        if isinstance(value, (list, tuple)):
            value = value[-1] if value else None
        return value or ''

    def choices(self, changelist):
        # jazzmin renders every filter inside one shared form, so the two
        # inputs just need their names and current values - the surrounding
        # form carries the other filters and submits them together
        yield {
            'date_from_param': self.date_from_param,
            'date_to_param': self.date_to_param,
            'date_from': self.value(self.date_from_param),
            'date_to': self.value(self.date_to_param),
            'label_from': 'С',
            'label_to': 'По',
        }

    @staticmethod
    def _parse(value):
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except (TypeError, ValueError):
            return None

    def queryset(self, request, queryset):
        date_from = self._parse(self.value(self.date_from_param))
        date_to = self._parse(self.value(self.date_to_param))

        if date_from:
            queryset = queryset.filter(
                order__datetime__gte=datetime.combine(date_from, time.min))
        if date_to:
            # inclusive of the whole "to" day
            queryset = queryset.filter(
                order__datetime__lt=datetime.combine(
                    date_to + timedelta(days=1), time.min))
        return queryset
