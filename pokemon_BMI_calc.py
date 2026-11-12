import requests
import pandas as pd
import time

API_ENDPOINT = "https://pokeapi.co/api/v2/pokemon/"


def get_pokerange():
    chosen_range = input("Which range of pokedex entries do you want to search for (1-1025)? A maximum range of 100 has been set, as it would otherwise take too long to fetch the data from the API.\nSeparate the start of the range and end of the range by a space, like '1 2'.\n")

    # Check whether the user input format is correct.
    try:
        range_list = chosen_range.split(" ")
        end = range_list[1]
    except IndexError:
        print("The program could not handle your inputted format. Please stick to the format as described. Try again.")
        get_pokerange()
    else:
        pokerange = [int(num) for num in range_list]

    # sort the numbers in ascending order.
    pokerange.sort()
    pokerange[1] += 1

    # check whether the user's inputs are within legal range.
    if pokerange[0] < 1:
        print(f"{pokerange[0]} is below the legal threshold of 1. Please input a different starting value.")
        get_pokerange()
    if pokerange[1] > 1025:
        print(f"{pokerange[1]} is above the legal threshold of 1025. Please input a lower number.")
        get_pokerange()

    # check whether the user's input range is a maximum of 100
    if pokerange[1] - pokerange[0] > 100:
        print(f"Your given range ({pokerange[1] - pokerange[0]}) is longer than 100. Please make your range smaller.")
        get_pokerange()

    return pokerange


def create_api_endpoint(poke_id):
    url = API_ENDPOINT + f"{poke_id}/"
    return url


def get_api_data(pokerange):
    print("\n -------------- Fetching data from the API. -------------- \n")
    raw_data = []
    for id in range(pokerange[0],pokerange[1]):
        url = create_api_endpoint(id)
        # get the data from the api, raise for HTTP errors and timeout errors. Built-in delay of 1 second as I don't want to flood the API with requests.
        try:
            response = requests.get(url=url,timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}.")
        except requests.exceptions.Timeout:
            print("A timeout occurred when trying to reach the API.")
        else:
            raw_data.append(response.json())
        finally:
            time.sleep(1)

    return raw_data


def filter_data(raw_data):
    print("\n -------------- Filtering data. -------------- \n")
    # Filter the raw API-data with the presepecified filtercriteria.
    filtered_data = []
    for raw_datum in raw_data:
        filtered_datum = {}
        filtered_datum["id"] = raw_datum["id"]
        filtered_datum["name"] = raw_datum["name"]
        filtered_datum["order"] = raw_datum["order"]
        filtered_datum["types"] = [type["type"]["name"] for type in raw_datum["types"]]
        filtered_datum["height"] = raw_datum["height"]
        filtered_datum["weight"] = raw_datum["weight"]
        filtered_data.append(filtered_datum)
    data_df = pd.DataFrame(filtered_data)
    return data_df


def calculate_bmi(height, weight):
    # pokemon weight is in kg, height in dm, so we divide by 10 to get the unit in m
    try:
        bmi = round(weight/(height/10)**2, 2)
    except ZeroDivisionError:
        print(f"Could not calculate the bmi of {height} and {weight}. Dividing by 0 is not allowed.")
        return None
    else:
        return bmi


def enrich_data(data):
    # Adds a column named "bmi" to the dataframe
    data["bmi"] = calculate_bmi(data.height,data.weight)
    return data


def create_savefilename(pokerange):
    # creates a savefilename based on the range of pokemon the user specified. Format: "pokeID_start-range_to_end-range_bmi"
    return f"pokeID_{pokerange[0]}_to_{pokerange[1] - 1}_bmi"


def save_to_csv(dataframe, savefilename):
    dataframe.to_csv(savefilename + ".csv", index=0)
    return


def save_to_json(dataframe, savefilename):
    dataframe.to_json(savefilename + ".json")
    return


def main():
    chosen_range = get_pokerange()
    raw_pokemon = get_api_data(chosen_range)
    filtered_pokemon = filter_data(raw_pokemon)
    enriched_pokemon = enrich_data(filtered_pokemon)
    savefilename = create_savefilename(chosen_range)
    save_to_csv(enriched_pokemon,savefilename)
    save_to_json(enriched_pokemon,savefilename)
    return


main()
