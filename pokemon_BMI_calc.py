import requests
import pandas as pd
import time

API_ENDPOINT = "https://pokeapi.co/api/v2/pokemon/"
POKETYPES = ["normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison", "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy", "stellar"]

# TODO reformat the API-data to a DataFrame
# TODO filter the API data for height, weight, id, name, types
# TODO enrich data by calculating the BMI and adding that as another stat to the dataframe.
# TODO save the dataframe as JSON
# TODO save the dataframe as CSV


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


def get_poketype():
    chosen_type = input(f"Which type of pokemon do you want filtered? These are the legal types: {POKETYPES}\n").lower()
    # Check whether the user has inputted a legal poketype.
    if chosen_type not in POKETYPES:
        get_poketype()
    else:
        return chosen_type


def create_api_endpoint(poke_id):
    url = API_ENDPOINT + f"{poke_id}/"
    return url


def get_api_data(pokerange):
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
    filtered_data = []
    for raw_pokemon_data in raw_data:
        pokemon = {}
        pokemon["id"] = raw_pokemon_data["id"]
        pokemon["name"] = raw_pokemon_data["name"]
        pokemon["height"] = raw_pokemon_data["height"]
        pokemon["weight"] = raw_pokemon_data["weight"]
        pokemon["order"] = raw_pokemon_data["order"]
        pokemon["types"] = [type["type"]["name"] for type in raw_pokemon_data["types"]]
        filtered_data.append(pokemon)
    return filtered_data


def main():
    chosen_range = get_pokerange()
    chosen_type = get_poketype()
    raw_data = get_api_data(chosen_range)
    filtered_data = filter_data(raw_data)
    print(filtered_data)


main()
