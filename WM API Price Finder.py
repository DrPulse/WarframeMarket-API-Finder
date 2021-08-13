import requests
import json
import string
import pprint
import datetime
import webbrowser

# URL and credentials storage
password = ""
mail = ""
Token_JWT = ""
main_URL = "https://api.warframe.market/v1/items"
login_URL = "https://api.warframe.market/v1/auth/signin"
profile_URL = "https://api.warframe.market/v1/profile"

Nbr_item_output = 5
Plateform_Selector = 1

#Function for printing the chosen plateform
def plateform_print(input_plat):
        Platform = {
            "1": 'pc',
            "2": 'ps4',
            "3": 'xbox',
            "4": 'switch',
        }
        return Platform.get(input_plat)


# Main function that will loop forever
def WarframeMain():
    
    # Searching for item in a loop if it fails
    while True:
        print("\nSearch for an item")
        WMsearch = input()
        print("\nSearching for " + WMsearch.upper().replace('_', ' ') + "...\n")

        head = {'content type': 'application/json', 'Platform': plateform_print(Plateform_Selector)}

        #WMsearch = "mesa_prime_set"
        WMitemR = requests.get('https://api.warframe.market/v1/items/' + WMsearch.replace(' ', '_') + '/orders', headers=head)
        #WMitemR = requests.get('https://api.warframe.market/v1/items/mesa_prime_set/statistics') # a retirer a terme
        #pprint.pprint(WMitemR.json()) #print de test pour les infos de l'item
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
    MinPrice = data['payload']['orders'][0]['platinum'] #Grab the first sell value of live statistics for the last 48 hours
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

    # Sorting by date first and then lowest price
    SortedWMList = sorted(WMList, key= lambda x: (x['platinum'], x['last_update']))
    print("\nThe", Nbr_item_output, "minimum prices found in the last ~24 hours for " + WMsearch.upper().replace('_', ' ') +" are\n")

    # Print of only the 5 first elements
    for element in range(Nbr_item_output):
        print(SortedWMList[element]['platinum'],"platinum as of :", SortedWMList[element]['last_update'][0:10])

    # Ask to open the web page of the requested item
    def browser_open():
        print("\nWould you like to buy/sell " + WMsearch.upper().replace('_', ' ') + " ? y/N")
        browser_answer = input()
        if browser_answer == "y":
            webbrowser.open_new('https://warframe.market/items/' + WMsearch.replace(' ', '_'))    
    browser_open()


    # Restart the script
    def restart_script():
        print('\nStart a new search? Y/n')
        restart_answer = input()
        if restart_answer == "y" or restart_answer == "":
            WarframeMain()
        elif restart_answer == "n":
            print('\nEnter any key to close the program')
            close_input = input() # to not instantly close the window program
    restart_script()  

    

###########################################################################################################################
# First code executed here

# Grabing the date of the day to extract only the data of the last 24 hours
Date_Today = datetime.date.today()
Date_Current = Date_Today.strftime("%Y-%m-%d")
Date_Yesterday = (Date_Today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

# Testing API responses according to URL in the program
print("\nTesting API responses\n")
WMresponseR = requests.get(main_URL)
print(WMresponseR)

#Program starting only if the API works, ask for the plateform to look for
if WMresponseR.status_code == 200:
    print("API OK\n")
    
    while True:
        print("\nFor which plateform do you want to use this program ? PC is by default\n 1 - PC \t2 - PS4 \t3 - XBOX \t4 - SWITCH\n")
        Plateform_Selector = input()
        if Plateform_Selector == "1" or Plateform_Selector == "2" or Plateform_Selector == "3" or Plateform_Selector == "4" or Plateform_Selector == "":
            if(Plateform_Selector == ""): Plateform_Selector = "1"
            break
        else:
            print("\nError while selecting the plateform")

    print("You have chosen the following plateform :",plateform_print(Plateform_Selector))
    WarframeMain()
elif WMresponseR.status_code == 404:
    print("API ERROR\n")
    print("Something is wrong about the status of the API, check the URL used, the status of warframe market, your internet connection, your firewall and launch again the program.")
    close_input = input() # to not instantly close the window program
    

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


