# Python-Application-to-Sell-All-Owned-Shares-of-A-Stock-for-Alpaca
This is a helpful Python window application to quickly sell all owned shares of a stock when you are waiting for a better selling price. 
This Python application is so new that it is in the beta testing phase for right now. 

Here is a better introduction to this Python Program:

Introducing the "Stock Market Insights with Alpaca" application!

Are you an investor who wants to stay up-to-date with the latest stock market data and make informed decisions? Look no further! With our powerful and user-friendly Python application, you can effortlessly fetch, analyze, and even sell stocks using Alpaca API. Let's take a closer look at what this amazing tool can do for you:

1. Real-Time Stock Data: Our application fetches real-time stock data using the Yahoo Finance API. Enter any stock symbol, and within seconds, you'll have access to essential information, including the current price, open, close, low, high, and percentage changes for the last 7 days.

2. Bollinger Bands Analysis: We've integrated the incredible Talib library to calculate and display Bollinger Bands for your chosen stock. This tool will help you identify potential price trends and make informed investment decisions.

3. Alpaca Account Information: Stay on top of your investment game with the ability to view your Alpaca account information directly within the application. See your current cash balance and number of day trades left, keeping you well-informed about your trading status.

4. Sell Stocks with Ease: Selling all owned shares of a stock is just a click away! Our application seamlessly interacts with Alpaca, allowing you to sell your stocks quickly and effortlessly.

5. Stay Updated: With a single click, you can start updating stock market prices, so you never miss a beat. Our real-time updates will keep you informed about the latest stock prices at all times.

6. User-Friendly Interface: We've designed our application to be intuitive and easy to navigate. Enter your stock symbol, specify the number of days for data query (default: 7), and let the information unfold!

Are you excited to dive into the world of data-driven investments? The "Stock Market Insights with Alpaca" application is your key to unlocking the full potential of your investments. Stay ahead of the market, make smart decisions, and maximize your returns.

Download the application now and elevate your investment journey like never before! Remember, the future of finance is at your fingertips with "Stock Market Insights with Alpaca."


[Disclaimer: This application does not provide financial advice. Always do your own research before making investment decisions. Past performance is not indicative of future results.]

After placing your alpaca keys at the bottom of /home/nameofyourhomefolderhere/.bashrc you simply run the command in a command terminal like:

python3 Sell-all-of-my-owned-shares-right-now-for-Alpaca.py

Disclaimer: Remember that all trading involves risks. The ability to successfully implement these strategies depends on both market conditions and individual skills and knowledge. As such, trading should only be done with funds that you can afford to lose. Always do thorough research before making investment decisions, and consider consulting with a financial advisor. This is use at your own risk software. This software does not include any warranty or guarantees other than the useful tasks that may or may not work as intended for the software application end user. The software developer shall not be held liable for any financial losses or damages that occur as a result of using this software for any reason to the fullest extent of the law. Using this software is your agreement to these terms. This software is designed to be helpful and useful to the end user.

Place your alpaca code keys in the location: /home/name-of-your-home-folder/.bashrc Be careful to not delete the entire .bashrc file. Just add the 4 lines to the bottom of the .bashrc text file in your home folder, then save the file. .bashrc is a hidden folder because it has the dot ( . ) in front of the name. Remember that the " # " pound character will make that line unavailable. To be helpful, I will comment out the real money account for someone to begin with an account that does not risk using real money. The URL with the word "paper" does not use real money. The other URL uses real money. Making changes here requires you to reboot your computer or logout and login to apply the changes.

The 4 lines to add to the bottom of .bashrc are:

export APCA_API_KEY_ID='zxzxzxzxzxzxzxzxzxzxz'

export APCA_API_SECRET_KEY='zxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzx'

#export APCA_API_BASE_URL='https://api.alpaca.markets'

export APCA_API_BASE_URL='https://paper-api.alpaca.markets'
