import time
from binance.client import Client

# Set up your binance API credentials
api_key = 'In3ZMfHGcgaa2nmFxDvNboeZZ3AvP37lAaZzqoiMQXwmPLe0JsHx9qoyaOtwcuYt'
api_secret = 'jyTQI65PWyOGZgMsLd8LBgXWgpz0IsscqjVGMEdMWI9CiZILDC5b8JqmdcMs2sOk'
client = Client(api_key, api_secret)

# Define your trading parameters
symbol = 'BTCUSDT'          # The trading pair to trade
buy_threshold = 0.02        # The percentage threshold for buying (e.g. 2% belowing the lowest price)
sell_threshold = 0.01       # The percentage threshold for selling (e.g. 1% above the highest price)

# Track the lowest and highest prices
lowest_price = None
highest_price = None

def check_price():
    global lowest_price, highest_price

    # Get the latest ticker price
    ticker = client.get_ticker(symbol=symbol)
    current_price = float(ticker['lastPrice'])

    # Update the lowest and highest prices
    if lowest_price is None or current_price < lowest_price:
        lowest_price = current_price
    if highest_price is None or current_price > highest_price:
        highest_price = current_price
    
    if current_price <= (lowest_price * (1 - buy_threshold)):
        # Calculate the maximum quantity that can be bought
        base_asset = symbol[3:]     # Extract the base symbol (e.g. USDT from BTCUSDT)
        balance = client.get_asset_balance(asset=base_asset)
        available_balance = float(balance['free'])
        quantity = available_balance / current_price        # Buy as much as possible with the available balance

        # Place a buy order with the maximum quantity
        order = client.create_order(
            symbol=symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print(f"\033[1;32mBuy Order Placed At {current_price} || Quantity: {quantity:.8f} {symbol}\033[0m")
        print("\033[1;32mOrder Details:\033[0m")
        print("\033[1;32mOrder ID: ", order['orderId'], "\033[0m")
        print("\033[1;32mOrder Status: ", order['status'], "\033[0m")
    elif current_price >= (highest_price * (1 + sell_threshold)):
        # Place a sell order with the previously bought quantity
        # First, get the account balance for the trading pair
        balance = client.get_asset_balance(asset=symbol[:3])        # Get the balance for the base asset (e.g. BTC)
        quantity = float(balance['free'])       # Use the available balance to sell
        order = client.create_order(
            symbol=symbol,
            side=Client.SIDE_SELL,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print(f"\033[1;34mSell Order Placed At {current_price} || Quantity: {quantity:.8f} {symbol}\033[0m")
        print("\033[1;34mOrder Details:\033[0m")
        print("\033[1;34mOrder ID: ", order['orderId'], "\033[0m")
        print("\033[1;34mOrder Status: ", order['status'], "\033[0m")

# Run the price checking loop
while True:
    check_price
    # Adjust the time interval (in seconds) based on your requirements
    time.sleep(10)