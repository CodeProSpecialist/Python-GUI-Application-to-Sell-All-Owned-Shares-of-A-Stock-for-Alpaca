import tkinter as tk
from datetime import datetime, timedelta
import yfinance as yf
from prettytable import PrettyTable
import talib as ta
import alpaca_trade_api as tradeapi
import os
import pytz

# Initialize the Alpaca API
APIKEYID = os.getenv('APCA_API_KEY_ID')
APISECRETKEY = os.getenv('APCA_API_SECRET_KEY')
APIBASEURL = os.getenv('APCA_API_BASE_URL')
api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)

eastern_zone = 'America/New_York'
current_time_zone = datetime.now(pytz.timezone(eastern_zone))

global current_time_eastern

current_time_eastern = datetime.now(pytz.timezone(eastern_zone)).strftime("%A, %b-%d-%Y %H:%M:%S")

global account

global positions

global position

global symbol

positions = api.list_positions()

# Fetch account information from Alpaca
account = api.get_account()

for position in positions:
    symbol = position.symbol


# Function to get stock data using yfinance
def get_stock_data_yfinance(symbol, start_date, end_date):
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None


# Function to convert timestamp to Eastern time format
def convert_to_eastern_time(timestamp):
    if timestamp.tzinfo is None:
        # If the timestamp is naive, assume it's in UTC and convert to Eastern timezone
        eastern_zone = pytz.timezone('US/Eastern')
        timestamp_utc = pytz.utc.localize(timestamp)
        timestamp_eastern = timestamp_utc.astimezone(eastern_zone)
    else:
        # If the timestamp is already timezone-aware, convert it to Eastern timezone directly
        eastern_zone = pytz.timezone('US/Eastern')
        timestamp_eastern = timestamp.astimezone(eastern_zone)

    return timestamp_eastern.strftime("%A, %b-%d-%Y %H:%M:%S")


# Function to fetch stock data and update the text widget
def fetch_stock_data():
    symbol = symbol_entry.get().upper()
    if not symbol:
        show_error("Please enter a stock symbol.")
        return

    # Get the number of days from the input box (default to 120 if not specified or invalid)
    try:
        num_days = int(days_entry.get())
    except ValueError:
        num_days = 120

    # Calculate the start and end dates based on today's date and the number of days
    today = datetime.today()
    end_date = today  # Today's date
    start_date = end_date - timedelta(days=num_days)  # Number of days ago from today

    data = get_stock_data_yfinance(symbol, start_date, end_date)
    if data is not None:
        # Extracting columns for open, close, low, high, and current price
        price_data = data[['Open', 'Close', 'Low', 'High']].copy()

        # Calculate percentage changes using .loc to avoid SettingWithCopyWarning
        price_data.loc[:, '1D % Change'] = price_data['Close'].pct_change(periods=1)
        price_data.loc[:, '3D % Change'] = price_data['Close'].pct_change(periods=3)
        price_data.loc[:, '1W % Change'] = price_data['Close'].pct_change(periods=5)
        price_data.loc[:, '1M % Change'] = price_data['Close'].pct_change(periods=20)
        price_data.loc[:, '6M % Change'] = price_data['Close'].pct_change(periods=120)
        price_data.loc[:, '1Y % Change'] = price_data['Close'].pct_change(periods=252)

        # Get the current time in Eastern timezone
        eastern_zone = pytz.timezone('US/Eastern')
        current_time_eastern = datetime.now(eastern_zone).strftime("%A, %b-%d-%Y %H:%M:%S")

        # Calculate the current price from the fetched data
        current_data = data.iloc[-1]
        current_price = current_data['Close']

        # Display the stock data in the text widget
        text_widget.delete('1.0', 'end')
        text_widget.insert('end', "Stock Symbol: " + symbol + "\n")
        text_widget.insert('end', "Current Price: " + f"{current_price:.2f}" + "\n")
        text_widget.insert('end', "Current Time (Eastern): " + current_time_eastern + "\n\n")

        # Print account information
        account = api.get_account()
        account_time = convert_to_eastern_time(datetime.now(pytz.utc))  # Corrected the datetime.datetime.now() typo
        text_widget.insert('end', "Account Information:\n")
        text_widget.insert('end', f"{account_time}\n")
        text_widget.insert('end',
                           f"Day Trade Count: {account.daytrade_count} out of 3 total Day Trades in 5 business days.\n")
        text_widget.insert('end', f"Current Account Cash: ${float(account.cash):.2f}\n")
        text_widget.insert('end', "--------------------\n")

        # Print current positions
        text_widget.insert('end', "\nCurrent Positions:\n")
        positions = api.list_positions()
        for position in positions:
            symbol = position.symbol
            current_price = float(position.current_price)
            text_widget.insert('end', f"Symbol: {symbol}, Current Price: ${current_price:.2f}\n")
            text_widget.insert('end', "--------------------\n")

        text_widget.insert('end', "Price Data for the Last 7 Days:\n")

        # Printing the data for the last 7 days using PrettyTable
        table = PrettyTable(
            ["Date", "Open", "Close", "Low", "High", "1D % Change", "3D % Change", "1W % Change", "1M % Change",
             "6M % Change", "1Y % Change"])
        table.align = "r"

        for date, row in price_data.iterrows():
            table.add_row([date.strftime('%Y-%m-%d'),
                           f"{row['Open']:.2f}", f"{row['Close']:.2f}", f"{row['Low']:.2f}",
                           f"{row['High']:.2f}", f"{row['1D % Change']:.2%}", f"{row['3D % Change']:.2%}",
                           f"{row['1W % Change']:.2%}", f"{row['1M % Change']:.2%}", f"{row['6M % Change']:.2%}",
                           f"{row['1Y % Change']:.2%}"])

        text_widget.insert('end', table)

        # Calculate Bollinger Bands using talib
        upper_band, middle_band, lower_band = ta.BBANDS(price_data['Close'], timeperiod=20, nbdevup=2, nbdevdn=2)

        # Creating a PrettyTable for Bollinger Bands
        bb_table = PrettyTable(["Date", "Upper Band", "Middle Band", "Lower Band"])
        bb_table.align = "r"

        for date, upper, middle, lower in zip(price_data.index, upper_band, middle_band, lower_band):
            bb_table.add_row([date.strftime('%Y-%m-%d'), f"{upper:.2f}", f"{middle:.2f}", f"{lower:.2f}"])

        text_widget.insert('end', "\nBollinger Bands:\n")
        text_widget.insert('end', bb_table)

    else:
        show_error(f"Failed to fetch stock data for symbol: {symbol}")


# Function to display an error message in a separate window
def show_error(message):
    error_window = tk.Toplevel(main_window)
    error_window.title("Error")
    error_window.geometry("400x250")

    error_label = tk.Label(error_window, text=message)
    error_label.pack()

    ok_button = tk.Button(error_window, text="OK", command=error_window.destroy)
    ok_button.pack()


# Function to get current positions using Alpaca API
def get_positions(api):
    positions = api.list_positions()
    return positions


# Function to sell all stocks for the given symbol
def sell_all_stocks():
    symbol = symbol_entry.get().upper()
    if not symbol:
        show_error("Please enter a stock symbol.")
        return

    try:

        get_positions(api)

        for position in positions:
            symbol = position.symbol

            stock_exists = any(position.symbol == symbol for position in positions)

            if not stock_exists:
                show_error(f"No positions found for symbol: {symbol}")
                return

        api.submit_order(
            symbol=position.symbol,
            qty=position.qty,
            side='sell',
            type='market',
            time_in_force='day'
        )
        print(f"Submitted order to sell all shares of {position.symbol}")

        show_result(f"Successfully sold all shares for symbol: {symbol}")

    except Exception as e:
        show_error(f"Error selling stocks: {e}")


# Function to display the result of selling stocks in a separate window
def show_result(message):
    result_window = tk.Toplevel(main_window)
    result_window.title("Sell Result")
    result_window.geometry("400x250")

    result_label = tk.Label(result_window, text=message)
    result_label.pack()

    ok_button = tk.Button(result_window, text="OK", command=result_window.destroy)
    ok_button.pack()


# Function to start updating stock market prices loop
def start_price_update():
    global update_running

    if update_running:
        return  # The update loop is already running

    # Set the update_running flag to 1 to indicate that the loop is running
    update_running = 1

    # Start the update loop
    update_stock_prices()


def stop_price_update():
    global update_running

    # Set the update_running flag to 0 to stop the loop
    update_running = 0


# Function to update stock prices
def update_stock_prices():
    global update_running
    symbol = symbol_entry.get().upper()
    if not symbol:
        return

    # Fetch the most recent data for the given stock symbol to get the current price and time
    stock = yf.Ticker(symbol)
    current_data = stock.history(period="1d")
    current_price = current_data["Close"].iloc[-1]

    # Get the current time in Eastern timezone
    eastern_zone = pytz.timezone('US/Eastern')
    current_time_eastern = datetime.now(eastern_zone).strftime("%A, %b-%d-%Y %H:%M:%S")

    # Display the current price without the time
    text_widget.insert('end', f"\nCurrent Price: {current_price:.2f}\n")
    text_widget.insert('end', f"Current Time (Eastern): {current_time_eastern}\n")

    # Schedule the next update after just less than 1 second
    main_window.after(650, update_stock_prices)


# Function to clear the text widget
def clear_text():
    text_widget.delete('1.0', 'end')


# Create the main window
main_window = tk.Tk()
main_window.title("Sell All Owned Shares of a Stock for Alpaca Program")
main_window.geometry("1300x950")

# Label for the stock symbol entry
label = tk.Label(
    main_window,
    text="Enter the Stock Symbol:",
    anchor='e',  # Align the text to the right side of the label
)
label.pack(side='top', padx=5)

# Stock symbol entry
symbol_entry = tk.Entry(main_window)
symbol_entry.pack(side='top')
symbol_entry.focus()

# Label for the number of days entry
days_label = tk.Label(
    main_window,
    text="Number of Days for Data Query (Default: 120):",
    anchor='e',
)
days_label.pack(side='top', padx=5)

# Entry box for number of days
days_entry = tk.Entry(main_window)
days_entry.pack(side='top', padx=5)

# Set the default value for number of days to 120
days_entry.insert(0, '120')

# Button to fetch stock data
fetch_button = tk.Button(
    main_window,
    text="Fetch Stock Data",
    command=fetch_stock_data,
)
fetch_button.pack(side='top', padx=5)

# Text widget to display the stock data
text_widget = tk.Text(main_window)
text_widget.pack(side='top', fill='both', expand=True)

# Button to sell all stocks
sell_button = tk.Button(
    main_window,
    text="Sell All Stocks for Current Symbol",
    command=sell_all_stocks,
)
sell_button.pack(side='top', padx=5)

# Button to start updating stock market prices loop
update_button = tk.Button(
    main_window,
    text="Start updating stock market prices",
    command=start_price_update,
)
update_button.pack(side='top', padx=5)

# Add the "Stop updating stock market prices" button
stop_update_button = tk.Button(
    main_window,
    text="Stop updating stock market prices",
    command=stop_price_update
)
stop_update_button.pack(side="top", padx=5)

# Add the "Clear Text" button
clear_button = tk.Button(
    main_window,
    text="Clear Text",
    command=clear_text
)
clear_button.pack(side="top", padx=5)

# Add an empty label for additional vertical space at the bottom
empty_label = tk.Label(main_window, text="")
empty_label.pack(side="bottom", pady=2)

# Global variable to indicate if the stock market update loop is running
update_running = 0

# Start the Tkinter event loop
main_window.mainloop()
