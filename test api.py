import requests
import json
import string
import pprint
import webbrowser

#URL and credentials storage
password = ""
mail = ""
Token_JWT = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWQiOiI1T0RhSFRVZUN4Zm9iVkUxcjlMVDk5Y1UwZmU3N09rdCIsImNzcmZfdG9rZW4iOiI5OTJmMzM3NWY0Yzk2ODY2N2Y2YWIwMjU4NTM5OGYxZjVjZmNmNTQ0IiwiZXhwIjoxNjMzMjAzODQzLCJpYXQiOjE2MjgwMTk4NDMsImlzcyI6Imp3dCIsImF1ZCI6Imp3dCIsImF1dGhfdHlwZSI6ImNvb2tpZSIsInNlY3VyZSI6ZmFsc2UsImp3dF9pZGVudGl0eSI6Ijk5RDNNNUZvTDFtUnJIck9iVkVYcnAxbTE3NHZlUDJDIiwibG9naW5fdWEiOiJiJ01vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjkwLjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvOTAuMCciLCJsb2dpbl9pcCI6ImInOTMuMjEuOTkuODgnIn0.mslfC-t2MlPi3gmJjgWUDHbAfBzV5u1i3WITLOP1x9U"
main_URL = "https://api.warframe.market/v1/items"
login_URL = "https://api.warframe.market/v1/auth/signin"
profile_URL = "https://api.warframe.market/v1/profile"

#Testing API responses
print("\nTesting API responses")
responseR = requests.get(main_URL)
print("")
print(responseR)
print("API OK\n\n")

"""
#login
loginR = requests.post(login_URL, headers = {'Authorization' : 'Token_JWT', 'language' : 'en', 'accept' : 'application/json', 'platform' : 'pc', 'auth_type' : 'header'}, json={'email' : mail, 'password' : password, 'auth_type' : 'header'})
print(loginR)
#pprint.pprint(l.json()) #Payload checking for credentials (debugging)
print("login OK\n")
"""
"""
p = requests.get(profile_URL)
p.json()
pprint.pprint(p.json())
"""


#Searching for item
print("Search for an item")
search = input()
print("\nSearching for " + search + "...\n")

#search = "mesa_prime_set"
itemR = requests.get('https://api.warframe.market/v1/items/' + search.replace(' ', '_') + '/statistics')
#itemR = requests.get('https://api.warframe.market/v1/items/mesa_prime_set/statistics') # a retirer a terme
#pprint.pprint(itemR.json())
print(itemR)
if(itemR.status_code == 200):
    print("Request OK\n")
elif(itemR.status_code == 404):
    print("Request denied\n")

#Output data in a json file
data = itemR.json()
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
            
print(data_access[3])
    
print("\nThe minimum price found in the last 48 hours for " + search +" is" , MinPrice , "platinum\n")


"""
print('Would you like to buy/sell ' + string.capwords(search) + "? y/n")
browser_answer = input()
if browser_answer == "y":
	webbrowser.open_new('https://warframe.market/items/' + search.replace(' ', '_'))
"""