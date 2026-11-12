Pokémon BMI calculator

The goal of this Python program is the following:
1. Asks the user for a given ID-range and a poketype.
2. From an API (pokeapi.co), pokédata is fetched based on the given ID-range.
3. This data is then filtered based on ID, name, height, weight, type and order.
4. The data is then enriched by calculating the BMI of the filtered pokémon (based on their height (dm) and weight (kg) stats)
5. The data is then saved as both a .JSON file and a .CSV file in the same directory, named "pokeID_start-range_to_end-range_bmi"

For the program to work, you need Python v. 3.15.2
Necessery packages: requests, pandas, time,

Run the program by typing "$ python pokemon_BMI_calc.py" in the command line. Make sure your working directory is in the same directory as the pokemon_BMI_calc.py file.
The program automatically asks for user input if needed, like the pokedex range and pokemon type.

Run the tests in test_main.py by typing "$ python test_pokemon_BMI_calc.py" in the command line. This should automatically test the main caluclator functions.
