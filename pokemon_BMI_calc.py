import requests
import pandas as pd
import time

API_ENDPOINT = "https://pokeapi.co/api/v2/pokemon/"
POKETYPES = ["normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison", "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy", "stellar"]

# TODO make an API-endpoint creator, so you can input which pokémon you want and you get the stats back.
# TODO get data from poke API; make a selection of what you want. I want to compare different pokémon together.
# TODO reformat the API-data to a DataFrame
# TODO filter the data based on the inputted order and type
# TODO enrich data by calculating the BMI and adding that as another stat to the dataframe.
# TODO save the dataframe as JSON
# TODO save the dataframe as CSV


def get_pokerange():
    chosen_range = input("Which range of pokedex entries do you want to search for? Separate the start of the range and end of the range by a space, like '1 2'.\n")

    try:
        range_list = chosen_range.split(" ")
        end = range_list[1]
    except IndexError:
        print("The program could not handle your inputted format. Please stick to the format as described. Try again.")
        get_pokerange()
    else:
        pokerange = [int(num) for num in range_list]

        return pokerange


def get_poketype():
    chosen_type = input(f"Which type of pokemon do you want filtered? These are the legal types: {POKETYPES}\n").lower()
    if chosen_type not in POKETYPES:
        get_poketype()
    else:
        return chosen_type


def main():
    chosen_range = get_pokerange()
    chosen_type = get_poketype()


main()
