import json
import os
import requests
from termcolor import colored

def clear():
    """ Clear the console """
    os.system(clear_command)


def colored_print(content, color):
    """ 'bold' termcolor.colored """
    return colored(content, color, attrs=["bold"])


def get_int_input(text):
    """ Retrieve an integer """
    valid = False
    while not valid:
        _input = input(text)
        try:
            _input = int(_input)
            valid = True
        except:
            print(colored_print("Invalid choice, try again.", 'red'))
    return _input


def get_option_input(options, text):
    """ Retrieve an option from a list of options """
    valid = False
    while not valid:
        _input = input(colored_print(text, "yellow"))
        for option in options:
            if _input.lower() == option[1].lower():
                return option[1].lower()
            elif _input.lower() == "help":
                help(options)
                break


def handle_option(data, entries, option):
    """ Run appropriate function for option retrieved """
    if option == "a":
        add_entry(data)
    elif option == "u":
        update_entry(data, entries)
    elif option == "r":
        remove_entry(data, entries)


def help(options):
    """ Print the list of options """
    print(colored_print("-"*47 + "\n" + " H E L P\n" + "-"*47, "yellow"))
    for option in options:
        print(colored_print(f"[{option[1]}] {option[0]}", "white"))
    print(colored_print("-"*47, "yellow"))


def validate_bundle_id(info):
    """ If bunlde ID lookup had results """
    if info['resultCount'] == 1:
        return True
    else:
        return False


def validate_file(data_path):
    """ If file exist and is not empty """
    if os.path.isfile(data_path) and os.path.getsize(data_path) > 0:
        return True
    return False


def load_entries(data_path):
    """ Load data from json file """
    if validate_file(data_path):
        with open(data_path, 'r') as data_file:
            data = json.load(data_file)
    else:
        with open('data.json', 'w') as data_file:
            data = {}
            json.dump(data, data_file, indent = 4, sort_keys = True)
    return data


def add_entry(data):
    """ Add an entry """
    bundle_id = input(colored_print("Bundle ID: ", "white"))
    store = get_option_input(countries, "Country (help: 'help'): ")
    info_url = "http://itunes.apple.com/" + store + "/lookup?bundleId=" + bundle_id
    info = requests.get(info_url).json()
    if validate_bundle_id(info):
        data[bundle_id] = {
                            "name": info['results'][0]['trackName'],
                            "version": info['results'][0]['version'],
                            "store": store,
                            "latest_version": True,
                            }


def update_entry(data, entries):
    """ Update the local version of an entry """
    valid = False
    while not valid:
        entry = get_int_input(colored_print("Entry to update (number next to app): ", "white"))
        for _entry in entries:
            if entry == _entry[0]:
                data[_entry[1]]['version'] = fetch_version(_entry[1], data[_entry[1]]['store'])
                valid = True
                break


def remove_entry(data, entries):
    """ Remove an entry """
    valid = False
    while not valid:
        entry = get_int_input(colored_print("Entry to remove (number next to app): ", "white"))
        for _entry in entries:
            if entry == _entry[0]:
                del data[_entry[1]]
                valid = True
                break


def fetch_version(bundle_id, store):
    """ Fetch the latest version of bundle ID from appropriate store """
    info_url = "http://itunes.apple.com/" + store + "/lookup?bundleId=" + bundle_id
    info = requests.get(info_url).json()
    return info['results'][0]['version']


def dump_data(data, data_path):
    """ Write the data to json file  """
    with open(data_path, 'w') as data_file:
        json.dump(data, data_file, indent = 4, sort_keys = True)


def start(data_path):
    """ Main """
    options = [["Add", "A"], ["Update", "U"], ["Remove", "R"]]
    entries = []
    data = load_entries(data_path)
    while True:
        clear()
        print(colored_print(r""" _   _           _ _  ___  ___
| | | |         | | | |  \/  |
| | | |_ __   __| | |_| .  . |_ __   __ _ _ __
| | | | '_ \ / _` | __| |\/| | '_ \ / _` | '__|
| |_| | |_) | (_| | |_| |  | | | | | (_| | |
 \___/| .__/ \__,_|\__\_|  |_/_| |_|\__, |_|
      | |                            __/ |
      |_| by @KevinIssaDev          |___/      """, "white") + "\n")
        print(colored_print("-"*47 + "\n" + " W A T C H   L I S T\n" + "-"*47, "yellow"))
        if data:
            for index, app in enumerate(data):
                entries.append([index, app])
                latest_version = fetch_version(app, data[app]["store"])
                if data[app]["version"] == latest_version:
                    data[app]["latest_version"] = False
                    print(colored_print(f"[{index}] ", "white") + colored_print(data[app]['name'], "green") + " | " + colored_print(data[app]['version'], "white"))
                else:
                    data[app]["latest_version"] = True
                    print(colored_print(f"[{index}] ", "white") + colored_print(data[app]['name'], "red") + " | " + colored_print(data[app]['version'], "white"))
        else:
            print(colored_print("No entries", "red"))
        print(colored_print("-"*47 + "\n" + " O P T I O N S\n" + "-"*47, "yellow"))
        for option in options:
            print(colored_print(f"[{option[1]}] {option[0]}", "white"))
        print(colored_print("-"*47, "yellow"))
        option = get_option_input(options, "Option: ")
        handle_option(data, entries, option)
        dump_data(data, data_path)

countries = [['Albania', 'AL'], ['Australia', 'AU'], ['Austria', 'AT'], ['Belgium', 'BE'], ['Brazil', 'BR'], ['Canada', 'CA'],
            ['China', 'CN'], ['Denmark', 'DK'], ['Dominican Republic', 'DO'], ['Egypt', 'EG'], ['Finland', 'FI'], ['France', 'FR'],
            ['Germany', 'DE'], ['Greece', 'GR'], ['Hong Kong', 'HK'], ['India', 'IN'], ['Indonesia', 'ID'], ['Ireland', 'IE'], ['Italy', 'IT'],
            ['Japan', 'JP'], ['South Korea', 'KR'], ['Luxembourg', 'LU'], ['Macedonia', 'MK'], ['Malaysia', 'MY'], ['Mexico', 'MX'],
            ['Netherlands', 'NL'], ['New Zealand', 'NZ'], ['North Korea', 'KP'], ['Norway', 'NO'], ['Pakistan', 'PK'], ['Philippines', 'PH'],
            ['Romania', 'RO'], ['Russian', 'RU'], ['Saudi Arabia', 'SA'], ['Serbia', 'RS'], ['Singapore', 'SG'], ['South Africa', 'ZA'],
            ['Sweden', 'SE'], ['Switzerland', 'CH'], ['Taiwan', 'TW'], ['Turkey', 'TR'], ['United Kingdom', 'GB'], ['United States', 'US'], ['Vietnam', 'VN']]

if __name__ == '__main__':
    clear_command = "cls" if os.name == "nt" else "clear"
    data_path = 'data.json'
    try:
        start(data_path)
    except KeyboardInterrupt:
        print(colored_print("\nExiting...", "red"))
    except EOFError:
        print(colored_print("\nExiting...", "red"))
