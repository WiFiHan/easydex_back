from datetime import datetime, timedelta
import pandas as pd
from pandas import DataFrame

def get_date_information(today):
  date_range = [today.date() - timedelta(days=i) for i in range(31)]
  formatted_indices = [datetime.strptime(date.strftime("%Y-%m-%d"), "%Y-%m-%d") for date in date_range]
  df = pd.DataFrame(index=formatted_indices)

  return df


def merge_src_df(src_dict : dict , df : DataFrame):
  src_df = pd.DataFrame.from_dict(src_dict, orient='index', columns=['src'])
  src_df.index = pd.to_datetime(src_df.index, format='%m/%d/%Y')
  df = df.merge(src_df, left_index=True, right_index=True, how='left')

  return df

def merge_compare_df(index : int, compare_dict : dict, df : DataFrame):
  compare_df = pd.DataFrame.from_dict(compare_dict, orient='index', columns=[f'{index}'])
  compare_df.index = pd.to_datetime(compare_df.index, format='%m/%d/%Y')
  df = df.merge(compare_df, left_index=True, right_index=True, how='left')

  return df

def get_tags_from_corr(df : DataFrame):
  df = df.apply(lambda x: pd.to_numeric(x.astype(str).str.replace(',',''), errors='coerce'))
  coefs = df.corrwith(df['src'], numeric_only=True)
  filtered_coefs = coefs[abs(coefs) > 0.7]
  if filtered_coefs.empty:
      filtered_coefs = coefs[abs(coefs) > 0.5]
  sorted_coefs = filtered_coefs.abs().sort_values(ascending=False)
  ordered_indices = sorted_coefs.index.tolist()
  ordered_indices.pop(0)
  if len(ordered_indices) > 5:
      ordered_indices = ordered_indices[:5]

  json_tags = {}
  for idx in ordered_indices:
      json_tags[idx] = round(coefs[idx], 3)
    
  return json_tags
