# WarframeMarket-Price-Tracker

Python CLI script to find Warframe market infos about items price and setting price track for desired items

## Documentation

This script is using the currently only API available for Warframe Market : apiVersion : v1
documentation of the API : https://warframe.market/fr/api_docs

The script use the website https://warframe.market/ where the players post sell and buy offers and the API use the page https://api.warframe.market/v1/items/ + the name of the desired item to retrieve its data.

The item requested must be as the website wants it, the whitespaces, underscores or capitals letters doesn't matter, it's taken care of by the program

Exemple : mesa_prime_set or mesa prime set

It cannot be "mesa prime" if you want to check a set of mesa prime.

It also can track a set list of items in a json file and will perform a check of prices every set value in minutes

## Usage

You can watch for items from different plateform and regions, so it's not reserved for pc players in en region only.

As said you can perfrom a research on the website and it will return the 10 (or less if there isn't 10) lower prices
You can also track specific items under a specific price (data in the tracked.json file). 

You don't need to open the file and change data (but you can), it's implemented in the script

I tried to make this program as self explanatory as possible, so you'll be tell when something went good or wrong and what's the cause of it

## Pre requesites

You will need to install python (designed and tested in Python 3.8.1 I didn't test others versions yet, will be updated if so)
https://www.python.org/downloads/

Once python is installed you will need to install the required packages, by using the following command .

```
pip install -r requirements.txt
```
 
## How to use 

Once you have done the above steps all you should need to do is run the script with command prompt or by clicking the py file on windows.
```
python WM_API_Price_Finder.py
```
If you can't find the item you're looking for, check the website 

## Future plans

- Add the option to go back to the menu wheneven you want to not be forced to complete a search or anything before that.
- Add an auto buy order option tag on the items you want to track
- Add a rank mod/arcane tag on the items you want to track to check only the mods/arcanes at set rank
- Add a region tag in the items you wanna track to only track the items of the set region, or all regions if you don't put any

## Known issues

When you use the tracking feature once, escape it, you won't be able to use it again, it won't show anything but you still can escape it and use the other feature as usual. I attend to fix it asap

When you add an item to tracked.json the program doesn't check yet if the item exist by doing a request yet, but it will pass during the check loop if the request fail

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License

The source code for the script is licensed under the MIT license, which you can find in the LICENSE file.

  