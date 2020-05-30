from django.db import connection
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Case, When, Value, CharField
from django.db.models import Q
from collections import namedtuple

def qs_to_csv_response(qs, filename):
    sql, params = qs.query.sql_with_params()
    sql = f"COPY ({sql}) TO STDOUT WITH (FORMAT CSV, HEADER, DELIMITER ',')"
    filename = f'{filename}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    with connection.cursor() as cur:
        sql = cur.mogrify(sql, params)
        cur.copy_expert(sql, response)
    return response

def get_qs_for_vacation(date=timezone.now().date()):
    QS = namedtuple('QS', 'on_dismissal on_vacation on_review')
    on_dismissal = Q(dismissal_date__isnull=False) | Q(dismissal_date__lte=date)
    on_vacation = Q(vacation__isnull=False) | (Q(vacation__start_date__lte=date) & Q(vacation__end_date__gte=date))
    on_review = Q(vacationreview__isnull=False) & (Q(vacationreview__start_date__lte=date) & Q(vacationreview__end_date__gte=date))
    qs = QS(
        on_dismissal,
        on_vacation,
        on_review
    )
    return qs

# для полей из набора вида ((1,_('foo')),(2,_('bar')))
def map_choices(field_name, choices):
    return Case(
        *[When(**{field_name: value, 'then': Value(str(representation))})
            for value, representation in choices],
        output_field=CharField()
    )