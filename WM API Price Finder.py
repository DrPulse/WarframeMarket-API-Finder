import requests
import json
import string
import pprint
import datetime
import webbrowser

#import for keyboard stop loop
from pynput import keyboard
from threading import Thread
from time import sleep

# URL and credentials storage
password = ""
mail = ""
Token_JWT = ""
main_URL = "https://api.warframe.market/v1/items"
login_URL = "https://api.warframe.market/v1/auth/signin"
profile_URL = "https://api.warframe.market/v1/profile"

# Grabing the date of the day to extract only the data of the last 24 hours
Date_Today = datetime.date.today()
Date_Current = Date_Today.strftime("%Y-%m-%d")
Date_Yesterday = (Date_Today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

# Function for the begining of the program for showing the first text and choose waht to do
def start_menu():
    Info_text = ("\nThis program has the following features : \n- A search function for a mod or item of the market,"
        "\n- A tracking feature for set items and price in a file that you can modify via this program or directly." 
        "\n\tYou will be alerted if one or more items are available on the website at the set price or lower")
    print(Info_text)

    while True:
        print("\nWhat do you want to do :\n1 : search (default) \t 2 : track item price")
        menu_input = input()
        if menu_input == "" or menu_input == "1":
            search_item()
            break
        elif menu_input == "2":
            #insert function for tracking
            tracking_prices()
            break
        else:
            print("\nerror while selecting the feature, try again")


#Function to select which platform you use
def platform_selector():
    while True:
            print("\nFor which platform do you want to use this program ? PC is by default\n 1 - PC \t2 - PS4 \t3 - XBOX \t4 - SWITCH\n")
            platform_selec = input()
            if platform_selec == "1" or platform_selec == "2" or platform_selec == "3" or platform_selec == "4" or platform_selec == "":
                if(platform_selec == ""): platform_selec = "1"
                break
            else:
                print("\nError while selecting the platform")
    platform = platform_print(platform_selec).upper()
    print("You have chosen the following platform :",platform)
    return platform


# Function for printing the chosen platform
def platform_print(input_plat):
        Platform = {
            "1": 'pc',
            "2": 'ps4',
            "3": 'xbox',
            "4": 'switch',
        }
        return Platform.get(input_plat)


# Ask to open the web page of the requested item
def browser_open(search_string):
    print("\nWould you like to buy/sell " + search_string.upper().replace('_', ' ') + " ? y/N")
    browser_answer = input()
    if browser_answer == "y":
        webbrowser.open_new('https://warframe.market/items/' + search_string.replace(' ', '_')) 


# Restart the script or transfer to main menu
def restart_script():
    print("\nDo you want to go to the main menu ? Y/n")
    restart_menu = input()
    if restart_menu == "y" or restart_menu == "":
        start_menu()
    else:
        print('\nPress Enter to close the program')
        

# Function that will search for a specific item or mod in the market
def search_item():
    
    Nbr_item_output = 10
    platform_search = platform_selector()

    # Searching for item in a loop if it fails
    while True:
        print("\nSearch for an item")
        WMsearch = input()
        print("\nSearching for " + WMsearch.upper().replace('_', ' ') + "...\n")

        # Request of the item on the appropriate platform
        head = {'content type': 'application/json', 'Platform': platform_print(platform_search)}
        WMitemR = requests.get('https://api.warframe.market/v1/items/' + WMsearch.replace(' ', '_') + '/orders', headers=head)
       
        print(WMitemR)
        if WMitemR.status_code == 200:
            print("Request OK\n")
            break
        elif WMitemR.status_code == 404:
            print("Request failed\n\nMake sure to use the proper name of items, ex : mesa prime set, mesa prime blueprint\n")

    # Output data in a json file
    data = WMitemR.json()
    with open ('data.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    # Looking for the lowest prices
    MinPrice = data['payload']['orders'][1]['platinum'] #Grab the first sell value of live statistics for the last 48 hours
    data_access = data['payload']['orders'] #Precising the data field

    # Loop for determining the lowest price available
    i=0; j=0
    WMList = []
    for item in data_access:
        i+=1  
        if item['order_type'] == "sell":        # Grabing only the sell orders
            data_date = item['last_update'][0:10]  # Extraction of only the date seperated with -
            if data_date == Date_Current or data_date == Date_Yesterday:    # Extracting date of today or
                WMList.insert(j,data_access[i-1])
                j+=1

    # Sorting by price first and then date
    SortedWMList = sorted(WMList, key= lambda x: (x['platinum'], x['last_update']))
    WMListLen = len(SortedWMList)
    
    # Print of only by default the 10 first elements or all elements if < 10
    if(WMListLen < Nbr_item_output):
        Nbr_item_output = WMListLen

    print("\nThe", Nbr_item_output, "minimum prices found in the last ~24 hours for " + WMsearch.upper().replace('_', ' ') +" are\n")
    for element in range(Nbr_item_output):
        print(SortedWMList[element]['platinum'],"platinum as of :", SortedWMList[element]['last_update'][0:10])

    browser_open(WMsearch)
    print("\nStart a new search? Y/n")
    restart_answer = input()
    if restart_answer == "y" or restart_answer == "":
        search_item()
    else:
        restart_script()  

def loop_price_check():
    while True:
        print('sleeping')
        sleep(10)

def on_press(key, abortKey='esc'):    
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys    

    print('pressed %s' % (k))
    if k == abortKey:
        print('end loop ...')
        return False  # stop listener

def tracking_prices():
       
    abortKey = 't'
    listener = keyboard.Listener(on_press=on_press, abortKey=abortKey)
    listener.start()  # start to listen on a separate thread

    # start thread with loop
    Thread(target=loop_price_check, args=(), name='loop_price_check', daemon=True).start()

    listener.join() # wait for abortKey
    print("oui c la fin")


###########################################################################################################################
#                                                            MAIN                                                         #
###########################################################################################################################

def main():
    
    # Testing API responses according to URL in the program
    print("Testing API responses\n")
    WMresponseR = requests.get(main_URL)
    print(WMresponseR)

    #Program starting only if the API works, ask for the platform to look for
    if WMresponseR.status_code == 200:
        print("API OK\n") 
        start_menu()

    elif WMresponseR.status_code == 404:
        print("API ERROR\n")
        print("Something is wrong about the status of the API, check the URL used, the status of warframe market, your internet connection, your firewall and launch again the program.")
    else:
        print(WMresponseR.status_code)
        print("Something is wrong about the status of the API, check the URL used, the status of warframe market, your internet connection, your firewall and launch again the program.")
        
    close_input = input() # to not instantly close the window program

if __name__ == "__main__":
    main()


"""
#login
WMloginR = requests.post(login_URL, headers = {'Authorization' : 'Token_JWT', 'language' : 'en', 'accept' : 'application/json', 'platform' : 'pc', 'auth_type' : 'header'}, json={'email' : mail, 'password' : password, 'auth_type' : 'header'})
print(WMloginR)
#pprint.pprint(WMlogin.json()) #Payload checking for credentials (debugging)
print("login OK\n")
"""
"""
WMprofileR = requests.get(profile_URL)
WMprofileR.json()
pprint.pprint(WMprofileR.json())
"""


