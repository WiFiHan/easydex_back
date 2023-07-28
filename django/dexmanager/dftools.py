from datetime import datetime, timedelta
import pandas as pd
from pandas import DataFrame
import random
from .models import SrcDex

def get_date_information(today, isInvest, period):
  if isInvest:
    date_range = [today.date() - timedelta(days=i) for i in range(31)]
    formatted_indices = [datetime.strptime(date.strftime("%Y-%m-%d"), "%Y-%m-%d") for date in date_range]
    df = pd.DataFrame(index=formatted_indices)
  else:
    if period == 'D':
        start_date = '2023-07-19'
        end_date = '2023-07-28'
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        formatted_indices = [date.strftime('%Y%m%d') for date in date_range]
        df = pd.DataFrame(index=formatted_indices)
    elif period == 'M':
        start_date = '2022-09-01'
        end_date = '2023-06-30'
        date_range = pd.date_range(start=start_date, end=end_date, freq='M')
        formatted_indices = [date.strftime('%Y%m') for date in date_range]
        df = pd.DataFrame(index=formatted_indices)
    elif period == 'Q':
        start_year = 2021
        end_year = 2023
        quarters_per_year = 4
        last_quarter = (end_year - start_year) * quarters_per_year + 2
        quarters = [f"{year}Q{quarter}" for year in range(start_year, end_year + 1) for quarter in range(1, quarters_per_year + 1)]
        quarters = quarters[:last_quarter]
        df = pd.DataFrame(index=quarters)
    elif period == 'A':
        start_year = 2014
        end_year = 2023
        date_range = [f"{year}" for year in range(start_year, end_year + 1)]
        df = pd.DataFrame(index=date_range)
    else:
        raise ValueError("Invalid period argument. Use 'D', 'M', 'Q', or 'A'.")

  return df

def merge_src_df(src_dict : dict , df : DataFrame, isInvest : bool):
  src_df = pd.DataFrame.from_dict(src_dict, orient='index', columns=['src'])
  if isInvest:
    src_df.index = pd.to_datetime(src_df.index, format='%m/%d/%Y')
    
  df = df.merge(src_df, left_index=True, right_index=True, how='left')

  return df

def merge_compare_df(index : int, compare_dict : dict, df : DataFrame, isInvest: bool):
  compare_df = pd.DataFrame.from_dict(compare_dict, orient='index', columns=[f'{index}'])
  if isInvest:
    compare_df.index = pd.to_datetime(compare_df.index, format='%m/%d/%Y')
  df = df.merge(compare_df, left_index=True, right_index=True, how='left')

  return df

def get_tags_from_corr(df : DataFrame):
  df = df.apply(lambda x: pd.to_numeric(x.astype(str).str.replace(',',''), errors='coerce'))
  coefs = df.corrwith(df['src'], numeric_only=True)
  filtered_coefs = coefs[abs(coefs) > 0.5]
  sorted_coefs = filtered_coefs.abs().sort_values(ascending=False)
  ordered_indices = sorted_coefs.index.tolist()
  if 'src' in ordered_indices:
    ordered_indices.remove('src')
  if len(ordered_indices) > 5:
    ordered_indices = ordered_indices[:5]

  json_tags = {}
  for idx in ordered_indices:
    json_tags[idx] = round(coefs[idx], 3)

  random_indicies = get_random_tags(ordered_indices)
  for idx in random_indicies:
    json_tags[str(idx)] = "random"
    
  return json_tags

def get_random_tags(exclude_list):
  start_idx = SrcDex.objects.first().id
  end_idx = SrcDex.objects.last().id
  random_indicies = []
  while (len(random_indicies) < 8 - len(exclude_list)):
    random_number = random.randint(start_idx, end_idx)
    if random_number not in exclude_list:
      random_indicies.append(random_number)
  return random_indicies