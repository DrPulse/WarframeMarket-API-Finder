import requests
import json
import datetime
import webbrowser
import os.path
from time import sleep

#import for keyboard stop loop
from pynput import keyboard
from threading import Thread


# URL storage 
main_URL = "https://api.warframe.market/v1/items"
login_URL = "https://api.warframe.market/v1/auth/signin"
profile_URL = "https://api.warframe.market/v1/profile"

# Global variables
Date_Today = datetime.date.today()
Date_Current = Date_Today.strftime("%Y-%m-%d")
Date_Yesterday = (Date_Today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
Keep_going = True
Track_file = "tracked.json"

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
            tracking_prices_management()
            break
        else:
            print("\nError while selecting the feature, try again")


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
def platform_print(input_plat:str):
        platform = {
            "1": 'pc',
            "2": 'ps4',
            "3": 'xbox',
            "4": 'switch',
        }
        return platform.get(input_plat)


# Ask to open the web page of the requested item
def browser_open(search_string:str):
    print("\nWould you like to buy/sell " + search_string.upper().replace('_', ' ') + " ? y/N")
    browser_answer = input()
    if browser_answer == "y":
        webbrowser.open_new('https://warframe.market/items/' + search_string.replace(' ', '_')) 


# Restart the script by going to main menu
def restart_script():
    print("\nDo you want to go to the main menu ? Y/n")
    restart_menu = input()
    if restart_menu == "y" or restart_menu == "":
        start_menu()
    else:
        print('\nPress Enter to close the program')
        

# Function that will search for a specific item or mod in the market2
def search_item():
    
    nbr_item_output = 10
    platform_search = platform_selector()

    # Searching for item in a loop if it fails
    while True:
        print("\nSearch for an item")
        wm_search = input()
        print("\nSearching for " + wm_search.upper().replace('_', ' ') + "...\n")

        # Request of the item on the appropriate platform
        head = {'content type': 'application/json', 'Platform': platform_print(platform_search)}
        wm_item_request = requests.get('https://api.warframe.market/v1/items/' + wm_search.replace(' ', '_') + '/orders', headers=head)
       
        print(wm_item_request)
        if wm_item_request.status_code == 200:
            print("Request OK\n")
            break
        elif wm_item_request.status_code == 404:
            print("Request failed\n\nMake sure to use the proper name of items, ex : mesa prime set, mesa prime blueprint\n")

    # Output data in a json file
    print(type(wm_item_request))
    data = wm_item_request.json()
    

    # Looking for the lowest prices
    MinPrice = data['payload']['orders'][1]['platinum'] #Grab the first sell value of live statistics for the last 48 hours
    data_access = data['payload']['orders'] #Precising the data field

    # Loop for determining the lowest price available
    i=0; j=0
    wm_list = []
    for item in data_access:
        i+=1  
        if item['order_type'] == "sell":        # Grabing only the sell orders
            #print(item['user']['status'])
            data_date = item['last_update'][0:10]  # Extraction of only the date seperated with -
            if data_date == Date_Current or data_date == Date_Yesterday:    # Extracting date of today or
                wm_list.insert(j,data_access[i-1])
                j+=1

    # Sorting by price first and then date
    sorted_wm_list = sorted(wm_list, key= lambda x: (x['platinum'], x['last_update']))
    wm_list_len = len(sorted_wm_list)
    
    # Print of only by default the 10 first elements or all elements if < 10
    if(wm_list_len < nbr_item_output):
        nbr_item_output = wm_list_len

    print("\nThe", nbr_item_output, "minimum prices found in the last ~24 hours all status combined for " + wm_search.upper().replace('_', ' ') +" are\n")
    for element in range(nbr_item_output):
        print(sorted_wm_list[element]['platinum'],"platinum as of :", sorted_wm_list[element]['last_update'][0:10])

    browser_open(wm_search)
    print("\nStart a new search? Y/n")
    restart_answer = input()
    if restart_answer == "y" or restart_answer == "":
        search_item()
    else:
        restart_script()  


# Function that split the tracking features into others function for more clarity in the code
def tracking_prices_management():
    while True:    
        print("\nEntered tracking prices menu, what do you want to do :\n1 : Launch track mode \t2 : Add/Remove an item/mod/arcane \t3 : See the list of track items \t4 : Returning to the main menu\n")
        track_input = input()
        
        if track_input == "" or track_input == "1":
            tracking_prices()
            break

        elif track_input == "2":
            trackfile_management()

        elif track_input == "3":
            print("\nHere is what is the items tracked insid tracked.json")
            tracked_print()
            break

        elif track_input == "4":
            restart_script()

        else:
            print("Error while choosing what to do, try again")

    restart_script()


# Loop for tracking the prices of set items in json file
def loop_price_check(loop_frequency:int, data_loop:dict, plateform:str):
    while Keep_going:
        head = {'content type': 'application/json', 'Platform': platform_print(plateform)}
       
        # double loop that request all the items in tracked.json        
        for categories in data_loop:
            print("\n\nFor the", categories, "category :")
            for element in data_loop[categories]:
                list_items = []
                
                # try the request first in case there is a type and request fail so we can still do the other items
                try:
                    wf_track_item = requests.get('https://api.warframe.market/v1/items/' + element['name'].lower().replace(' ', '_') + '/orders', headers=head)
                    
                    # Extracting the data ine of every item from tracked.json
                    data_track_item = wf_track_item.json()
                    dt = data_track_item['payload']['orders']                 
                    output_structure={}
                    
                    # loop that checks for online and ingame offers under the set price
                    for wf_item in dt:
                        if wf_item['order_type'] == "sell" and (wf_item['user']['status'] == "online" or wf_item['user']['status'] == "ingame"):
                            if  wf_item['platinum'] <= element['price']:                             
                                list_items.append({'name': wf_item['user']['ingame_name'], 'price' : wf_item['platinum'], 'reg': wf_item['user']['region']})
                    
                    # list that collect every order under the set price
                    output_structure[str(element['name'])] = list_items
                    print("\n-",element['name'].upper().replace('_', ' '), ":", str(element['price']), "platinum")
                    
                    # print based on incrasing price of items
                    output_sorted = sorted(output_structure[element['name']], key=lambda x: x['price'])
                    for k in output_sorted:
                        print("\tPrice :", k['price'], "\tRegion :", k['reg'],"\t","Player name :", k['name'], )    
                
                except Exception:
                    print("\nError with", element['name'],"check that it's using the correct format")
                    continue
                
            if data_loop[categories] == []:
                print("\nNo items to track in the", categories, "category")
        #pprint.pprint(output_structure)

        print("\nAuto search done, doing it again in", loop_frequency,"minutes")
        sleep(loop_frequency*60)


# Detection of pressed key
def on_press(key, abortKey='esc'):    
    global Keep_going
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys    

    if k == abortKey:
        Keep_going = False
        print('\nEnd of checking prices')
        sleep(1)
        return False  # stop listener


# Function that launch the tracking loop, ask how often the loop is refreshed and create tracked.json if not created
def tracking_prices():
    check_price_time = 5
    platform_track = platform_selector()
    
    while True:
        print("\nTracking prices mode, how frequently do you want to check prices in minutes ? Press Enter for default 5 min")
        check_price_time = input()
        if check_price_time.isnumeric() and int(check_price_time) > 0:
            break
        elif check_price_time == "":
            check_price_time = 5
            break
        else:
            print("Error while setting loop time check, enter an integer value")
    print("\nPress escape to end the tracking loop")
   # initialize tracked.json field if not already created
    file_structure = {"items": [],"mods": [], "arcanes":[]}

    if os.path.isfile(Track_file): 
        print("Tracked file present in directory")
    else:
        print("File not present, creating it")
        write_json(file_structure, Track_file)
        

    data_tracked = load_json(Track_file)
    
    abortKey = 'esc'
    listener = keyboard.Listener(on_press=on_press, abortKey=abortKey)
    listener.start()  # start to listen on a separate thread
    
    # start thread with loop
    Thread(target=loop_price_check, args=(int(check_price_time), data_tracked, platform_track), name='loop_price_check', daemon=True).start()
    listener.join() # wait for abortKey
      

#Function where you can add or delete items in tracked.json
def trackfile_management():
    print("\nHere is the current track items :")
    tracked_print()

    # while used to get a correct command to prevent errors and typo in tracked.json
    while True:
        print("\n\nTo add a new item use the key word add , then the category (items, mods, arcanes) and the name, with or without '_' symbol and the limit price"
        "\nTo remove an item use the key word remove or rm, then the category (items, mods, arcanes) and the line number of the item"
        "\nExample : add flow mods 15 /// remove items 1\n")
        input_management = input()
        words = input_management.split(' ')
        command_type = words[0]
        
        if command_type == "add":
            if len(words) < 4:
                print("error typing")
            else:                   
                category = words[-2]
                price = words[-1]
                name = words[1:-2]
                        
                if category != "items" and category != "mods" and category != "arcanes":
                    print("\nError while choosing the category, use items, mods or arcanes")

                elif isinstance(price, float) or not (price.isdigit()) or (int(price) <= 0) :
                    print("\nError while choosing the price, use positive non null integer numbers")

                else: 
                    adding = {'name': ' '.join(name), 'price': int(price)}
                    break
                
        elif command_type == "remove" or command_type == "rm":
            if len(words) < 3 or len(words) > 3:
                print("error typing")
            else:
                category = words[1]
                row = words[-1]

                if category != "items" and category != "mods" and category != "arcanes":
                    print("\nError while choosing the category, use items, mods or arcanes")  

                elif isinstance(row, float) or not (row.isdigit()) or (int(row) <= 0) :
                    print("\nError while choosing the line to delete, use positive non null integer numbers")      

                else: 
                    row = int(row)-1    # Convert into an integer and reduce the value by one cause start index is 0 not 1
                    break
        else:
            print("\nError while typing command")
   
    data = load_json(Track_file)

    if command_type == "add":
        add_json(data, Track_file, category,adding)
        print("Data added")
    elif command_type == "remove" or command_type == "rm":
        del_json(data, Track_file, category, row)
        print("Data removed")

    
# Print tracked.json data
def tracked_print():
    data = load_json(Track_file)
    for category in data:
        print("\n-",category)
        for item in data[category]:
            print("\t{:<25s} at {} platinum".format(item['name'].upper(), item['price']))   # better print that reserve 25 characters before the next print object

# Load all the data of the passed file        
def load_json(filename:str):
    with open(filename) as f:
        data = json.load(f)
    return data


# Function that write given data in a given file
def write_json(data:dict, filename:str):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


# Function that add a given item in tracked.json
def add_json(data:dict, filename:str, selector:str, text:dict):
    with open(filename) as file:
        data = json.load(file)
        tmp = data[selector]
        tmp.append(text)
        write_json(data, filename)


# Function that delete a given dict in the list of tracked.json
def del_json(data:dict, filename:str, selector:str, row:int):
    with open(filename) as file:    
        data = json.load(file)
        tmp = data[selector]
        tmp.pop(row)
        write_json(data, filename)

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
