import requests
import json
import string
import pprint
import webbrowser

# URL and credentials storage
password = ""
mail = ""
Token_JWT = ""
main_URL = "https://api.warframe.market/v1/items"
login_URL = "https://api.warframe.market/v1/auth/signin"
profile_URL = "https://api.warframe.market/v1/profile"


# Main function that will loop forever
def WarframeMain():
    
    # Searching for item in a loop if it fails
    while True:
        print("Search for an item")
        search = input()
        print("\nSearching for " + search.upper().replace('_', ' ') + "...\n")

        #search = "mesa_prime_set"
        WMitemR = requests.get('https://api.warframe.market/v1/items/' + search.replace(' ', '_') + '/statistics')
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

    # ooking for the lowest prices
    MinPrice = data['payload']['statistics_live']['48hours'][1]['min_price'] #Grab the first sell value of live statistics for the last 48 hours
    data_access = data['payload']['statistics_live']['48hours'] #Precising the data field

    # Loop for determining the lowest price available
    i=0; j=0
    WMList = []
    for item in data_access:
        i+=1
        if item['order_type'] == "sell":
            WMList.insert(j,data_access[i-1])
            j+=1

    # Sorting by date first and then lowest price
    SortedWMList = sorted(WMList, key= lambda x: (x['min_price'], x['datetime']))
    print("\nThe 5 minimum prices found in the last ~48 hours for " + search.upper().replace('_', ' ') +" are\n")

    # Print of only the 5 first elements
    for element in range(5):
        print(SortedWMList[element]['min_price'],"platinum as of :", SortedWMList[element]['datetime'])


    # Ask to open the web page of the requested item
    def browser_open():
        print("\nWould you like to buy/sell " + search.upper().replace('_', ' ') + " ? y/n")
        browser_answer = input()
        if browser_answer == "y":
            webbrowser.open_new('https://warframe.market/items/' + search.replace(' ', '_'))    
    browser_open()


    # Restart the script
    def restart_script():
        print('\nStart a new search? Y/n')
        restart_answer = input()
        if restart_answer == "y" or restart_answer == "":
            WarframeMain()
        if restart_answer == "n":
            print('Goodbye')
    restart_script()  

###########################################################################################################################
# First code executed here
# Testing API responses according to URL in the program
print("\nTesting API responses\n")
WMresponseR = requests.get(main_URL)
print(WMresponseR)

if WMresponseR.status_code == 200:
    print("API OK\n")
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


