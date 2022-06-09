import hashlib
from datetime import datetime


def print_horizontal_line(length=60):
    print('-'*length)


def print_text_in_horizontal_line(text, length=60):
    line_len = (length - len(text))//2
    print()
    print('-'*line_len, text, '-'*line_len)
    print()


def print_forecast_data(forecast):
    for key, value in forecast.items():
        print(f'{key.title():<20}', value)


def get_str_formatted_for_table(s: str, length=22):
    if isinstance(s, str):
        len_ellipsis = 2
        s = (s[:length - len_ellipsis*2] + '.'*len_ellipsis) if len(s) > length else s
    return f'{s:<{length}}'


def print_cities(cities):
    columns = ['idx', 'name', 'country', 'state', 'latitude', 'longitude']

    print_horizontal_line(length=120)
    for column in columns:
        print(get_str_formatted_for_table(column.upper()), end='')
    print('\n')

    for i, city in enumerate(cities):
        print(get_str_formatted_for_table(i), city, sep='')

    print_horizontal_line(length=120)


def get_date_input():
    month = int(input('Enter month: '))
    day = int(input('Enter day: '))
    curr_year = datetime.now().year

    try:
        return datetime(year=curr_year, month=month, day=day).date()
    except ValueError as e:
        print('Error:', e)
        return get_date_input()


def get_formatted_date(date, format='%d %b, %Y'):
    return date.strftime(format)


def get_hash(value):
    return hashlib.sha224(value.encode('utf-8')).hexdigest()
