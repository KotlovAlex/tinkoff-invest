import os

from dotenv import load_dotenv
load_dotenv()

from tinkoff.invest import Client

token = os.environ["TOKEN"]

from utils import get_current_date, get_merge_value

def get_portfolio():
   with Client(token) as client:
      accounts = client.users.get_accounts()
      account_id = accounts.accounts[0].id

      portfolio_amount = 0
      virtual_portfolio_amount = 0

      portfolio = client.operations.get_portfolio(account_id=account_id)
      positions = portfolio.positions

      with open(f'log-{get_current_date()}.txt', 'w', encoding='utf-8') as log:
         print('Купленные инструменты', file=log)
         print('_____________________', file=log)

      for position in positions:
        price = get_merge_value(position.current_price)
        quantity = get_merge_value(position.quantity)
        instrument_id = position.instrument_uid
        instrument_info = client.instruments.get_instrument_by(id_type=3, id=instrument_id).instrument
        name = instrument_info.name
        portfolio_amount += price * quantity
        with open(f'log-{get_current_date()}.txt', 'a', encoding='utf-8') as log:
          print({
            "price": price,
            "quantity": quantity,
            "amount": price * quantity,
            "name": name
          }, file=log)
      with open(f'log-{get_current_date()}.txt', 'a', encoding='utf-8') as log:
        print("Подарочные инструменты", file=log)
        print("______________________", file=log)
      virtual_positions = portfolio.virtual_positions
      for position in virtual_positions:
        price = get_merge_value(position.current_price)
        quantity = get_merge_value(position.quantity)
        instrument_id = position.instrument_uid
        instrument_info = client.instruments.get_instrument_by(id_type=3, id=instrument_id).instrument
        name = instrument_info.name
        virtual_portfolio_amount += price * quantity
        with open(f'log-{get_current_date()}.txt', 'a', encoding='utf-8') as log:
          print({
            "price": price,
            "quantity": quantity,
            "amount": price * quantity,
            "name": name
            }, file=log)
      with open(f'log-{get_current_date()}.txt', 'a', encoding='utf-8') as log: 
        print("_________________________", file=log)
        print(f'Стоимость реального портфеля: {round(portfolio_amount, 2)}', file=log)
        print(f'Стоимость виртуального портфеля: {round(virtual_portfolio_amount, 2)}', file=log)
        print(f'Стоимость полного портфеля: {round(portfolio_amount + virtual_portfolio_amount, 2)}', file=log)

if __name__ == "__main__":
  get_portfolio()