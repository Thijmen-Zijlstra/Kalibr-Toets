import pytest
import pandas as pd
from pokemon_BMI_calc import calculate_bmi, create_api_endpoint, enrich_data

# TODO creëer test voor de BMI caluclator
# TODO creëer test voor enrich_data
# TODO creëer test voor create_api_endpoint

def test_calculate_bmi():
    assert calculate_bmi(20,2) == "5"
    assert calculate_bmi(10,0) == "None"
    assert calculate_bmi(20,-2) == "5"
    assert calculate_bmi(-20,2) == "-5"


def test_create_api_endpoint():
    assert create_api_endpoint(16) == "https://pokeapi.co/api/v2/pokemon/16/"
    assert create_api_endpoint("Ditto") == "https://pokeapi.co/api/v2/pokemon/Ditto/"
    assert create_api_endpoint(17.01992) == "https://pokeapi.co/api/v2/pokemon/17.01992/"


@pytest.fixture
def create_mock_dataframe(heights, weights):
    mock_dataframe = pd.DataFrame([{'weight': weights[0], 'height': heights[0]}, {'weight': weights[1], 'height':heights[1]}])
    return mock_dataframe


def test_enrich_data():
    assert enrich_data(create_mock_dataframe([20,10],[5,6]))["bmi"] != None
