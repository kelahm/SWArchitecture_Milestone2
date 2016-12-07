#This is a repo for the Trade Net assignment in Software Arch

###Check the [wiki](https://github.com/kelahm/SWArchitecture_Milestone2/wiki) to find out how to run the website on your local machine.

##Notes:
1. On the search page search for company names not the ticker.

2. In the step, "Sell 100 shares of Twitter (TWTR) - Rejected because Customer #1 doesn't own shares in TWTR".
in order to get to the sell stock page you have to know the link if you do not own the stock. if you own the stock the sell link should be in your portfolio.

3. In the step, "Buy 1000 shares of Google (GOOG) - Rejected because of insufficient cash - can only use cash available to purchase shares".
The Tradier API for some reason will not return Google stock when the search function is used. You can view the Google stock page at [this link](http://localhost:8000/TradeNet/details/GOOG) if needed.
