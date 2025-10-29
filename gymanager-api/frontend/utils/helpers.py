from datetime import datetime


MONTH_NAMES_MAPPING = {
    1: "janeiro",
    2: "fevereiro",
    3: "março",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro"
}


def format_api_date(original_date_str, original_format, desired_format):
    date_obj = datetime.strptime(original_date_str, original_format)
    return date_obj.strftime(desired_format)
