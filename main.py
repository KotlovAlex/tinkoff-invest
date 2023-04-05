import os

from dotenv import load_dotenv
load_dotenv()

from tinkoff.invest import Client, GetOperationsByCursorRequest

token = os.environ["TOKEN"]


def get_operations():
  with Client(token) as client:
      accounts = client.users.get_accounts()
      account_id = accounts.accounts[0].id

      def get_request(cursor=""):
          return GetOperationsByCursorRequest(
              account_id=account_id,
              instrument_id="BBG004730N88",
              cursor=cursor,
              limit=1,
          )
      
      def get_info(operations):
        description = operations.items[0].description
        price_units = operations.items[0].price.units
        price_nano = operations.items[0].price.nano
        price = f'{price_units}.{price_nano if price_nano >= 1e8 else f"0{price_nano}"}'
        quantity = operations.items[0].quantity
        commission = f'{operations.items[0].commission.units}.{abs(operations.items[0].commission.nano)}'
        return description, price, quantity, commission

      def show_info(description, price, quantity, commission):
        print(description)
        print(f'Цена за одну: {price}')
        print(f'Количество: {quantity}')
        print(f'Коммисия: {commission}')
        print(f'Итого: {float(price)*quantity+float(commission)}')
        print('--------------------------------')

      def get_and_show_info(operations):
        description, price, quantity, commission = get_info(operations)
        show_info(description, price, quantity, commission)

      operations = client.operations.get_operations_by_cursor(get_request())
      get_and_show_info(operations)
      
      while operations.has_next:
          request = get_request(cursor=operations.next_cursor)
          operations = client.operations.get_operations_by_cursor(request)
          get_and_show_info(operations)

if __name__ == '__main__':
   pass