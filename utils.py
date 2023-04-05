import datetime

def get_current_date():
  now = datetime.datetime.now()
  return f'{now.year}-{now.month}-{now.day}'

def get_merge_value(MoneyValue):
  units = MoneyValue.units
  nano = f'0.{MoneyValue.nano}' if MoneyValue.nano > 1e8 else f'0.0{MoneyValue.nano}'
  return units+float(nano)