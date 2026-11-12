import requests
import pandas as pd
import time

API_ENDPOINT = "https://pokeapi.co/api/v2/pokemon/"
POKETYPES = ["normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison", "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy", "stellar"]

# TODO reformat the API-data to a DataFrame
# TODO filter the data based on the inputted order and type
# TODO enrich data by calculating the BMI and adding that as another stat to the dataframe.
# TODO save the dataframe as JSON
# TODO save the dataframe as CSV


def get_pokerange():
    chosen_range = input("Which range of pokedex entries do you want to search for (1-1025)? Don't make the range too big, as it takes a while to fetch the data from the API.\nSeparate the start of the range and end of the range by a space, like '1 2'.\n")

    try:
        range_list = chosen_range.split(" ")
        end = range_list[1]
    except IndexError:
        print("The program could not handle your inputted format. Please stick to the format as described. Try again.")
        get_pokerange()
    else:
        pokerange = [int(num) for num in range_list]

    pokerange.sort()
    pokerange[1] += 1
    print(pokerange)

    if pokerange[0] < 1:
        print(f"{pokerange[0]} is below the legal threshold of 1. Please input a different starting value.")
        get_pokerange()
    if pokerange[1] > 1025:
        print(f"{pokerange[1]} is above the legal threshold of 1025. Please input a lower number.")
        get_pokerange()

    return pokerange


def get_poketype():
    chosen_type = input(f"Which type of pokemon do you want filtered? These are the legal types: {POKETYPES}\n").lower()
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
        response = requests.get(url=url)
        response.raise_for_status()
        raw_data.append(response.json())
        time.sleep(1)
    return raw_data


def main():
    chosen_range = get_pokerange()
    chosen_type = get_poketype()
    raw_data = get_api_data(chosen_range)
    print(raw_data)


main()
