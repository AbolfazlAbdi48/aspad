from . import jalali


def jalali_converter_dict(time) -> dict:
    jmonths = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد',
               'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']

    time_to_str = f'{time.year},{time.month},{time.day}'
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    for index, month in enumerate(jmonths):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    # output = f'{time_to_list[2]} {time_to_list[1]} {time_to_list[0]} '

    return {'day': time_to_list[2], 'month': time_to_list[1], 'year': time_to_list[0]}


def jalali_converter_str(time) -> str:
    str_time = jalali_converter_dict(time)
    return f"{str_time['day']} {str_time['month']} {str_time['year']}"


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
