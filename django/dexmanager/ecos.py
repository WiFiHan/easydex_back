import requests
from .models import SrcDex
from .utils import reduce_title

def get_url_period(index_period):
    period_dict = {"D": "/D/20230719/20230728/", "M": "/M/202209/202306/", "Q": "/Q/2021Q1/2023Q2/", "A": "/A/2014/2023/"}
    return period_dict[index_period]

def truncate_string(original_string):
    last_dot_index = original_string.rfind(".")
    if "2008.9" in original_string: last_dot_index = 5
    if last_dot_index != -1:
        truncated_string = original_string[last_dot_index + 1 :]
        return truncated_string.strip()
    return original_string

def validate_title(title):
    if title[-2:] in ["1)", "2)", "4)"]: title = title[:-3]
    elif title == "C 제조업": title = "제조업"
    elif title == "C-1.2.대출금": title = "대출금"
    return title.strip()

def get_statistic(index_period, table_code, index_code):
    url_prefix = "http://ecos.bok.or.kr/api/StatisticSearch/1AJBYOG5GZJC0OMYBOSO/json/kr/1/10/"
    url_period = get_url_period(index_period)
    url = url_prefix + table_code + url_period + index_code

    response = requests.get(url)

    if response.status_code == 200:
        try:
            row_list = response.json().get('StatisticSearch').get('row')
            category = truncate_string(row_list[0].get('STAT_NAME'))
            title = validate_title(row_list[0].get('ITEM_NAME1'))
            subtitle = row_list[0].get('ITEM_NAME2')
            if not subtitle: 
                saved_title = category + '/' + title
            else:
                saved_title = category + '/' + title + '/' + subtitle
            unit = row_list[0].get('UNIT_NAME')
            if not unit: unit = "unitless"

            values = dict()
            for row in row_list:
                values[row.get('TIME')] = row.get('DATA_VALUE')
        except Exception as e:
            print(f"Error parsing data: {e}", table_code, index_code)
            return "Failed to parse data"
        try:
            Dex, created = SrcDex.objects.get_or_create(title=saved_title)
            if created:
                Dex.category = category
                Dex.unit = unit
                Dex.isInvest = False
                Dex.search_keyword = [title]
                Dex.reduced_title = reduce_title(saved_title)
                Dex.period = index_period
            Dex.values = values
            Dex.save()

            return f"{title} created" if created else f"{title} updated"
        except Exception as e:
            print(f"Error saving data: {e}")
            return "Failed to save data"
    else:
        print(f"Request failed with status code {response.status_code} while processing code {index_code}")
        return "Request failed"