import requests
import json
import string
import pprint
import webbrowser

#URL and credentials storage
password = ""
mail = ""
Token_JWT = ""
main_URL = "https://api.warframe.market/v1/items"
login_URL = "https://api.warframe.market/v1/auth/signin"
profile_URL = "https://api.warframe.market/v1/profile"

#Testing API responses
print("\nTesting API responses")
WMresponseR = requests.get(main_URL)
print("")
print(WMresponseR)
print("API OK\n")

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


#Searching for item
print("Search for an item")
search = input()
print("\nSearching for " + search + "...\n")

#search = "mesa_prime_set"
WMitemR = requests.get('https://api.warframe.market/v1/items/' + search.replace(' ', '_') + '/statistics')
#WMitemR = requests.get('https://api.warframe.market/v1/items/mesa_prime_set/statistics') # a retirer a terme
#pprint.pprint(WMitemR.json())
print(WMitemR)
if(WMitemR.status_code == 200):
    print("Request OK\n")
elif(WMitemR.status_code == 404):
    print("Request denied\n")

#Output data in a json file
data = WMitemR.json()
with open ('data.json', 'w') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

#Looking for the lowest prices
MinPrice = data['payload']['statistics_live']['48hours'][1]['min_price'] #Grab the first sell value of live statistics for the last 48 hours
data_access = data['payload']['statistics_live']['48hours'] #Precising the data field

#Loop for determining the lowest price available
for item in data_access:
    if item['order_type'] == "sell":
        if item['min_price'] < MinPrice: 
            MinPrice = item['min_price']
            test = data_access[3]
            
print(test)
    
print("\nThe minimum price found in the last 48 hours for " + search +" is" , MinPrice , "platinum\n")


"""
print('Would you like to buy/sell ' + string.capwords(search) + "? y/n")
browser_answer = input()
if browser_answer == "y":
	webbrowser.open_new('https://warframe.market/items/' + search.replace(' ', '_'))
"""