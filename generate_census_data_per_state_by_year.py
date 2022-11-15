import sys
import censusdata
from us import states
import pandas as pd
import requests
import sys

# TODO: remove hardcoded global
YEAR = 2020

def generate_survey_codes_for_each_state():
    """
    Takes more LOC than hardcoding the survey codes. 
    """
    codes = []
    for i in range(ord('A'), ord('I') + 1):
        letter = str.upper(chr(i))
        full_code = f'B01001{letter}'
        codes.append(full_code)
    
    codes
    return codes

def get_variables_to_concepts_and_labels_mapping(survey_code):
    """
    Params:
    - survey_code: str - 
    """
    variables = censusdata.censustable('acs5', 2019, survey_code)
    variables_to_concepts_and_labels = {}

    for v in variables:
        variables_to_concepts_and_labels[v] = variables[v]['concept'] + " " + variables[v]['label']

    return variables_to_concepts_and_labels

def get_data_by_group_and_state(survey_code, state_fips):
    """
    Params:
    - group : str - group level tag (e.g. B01001A)
    - state : str - number representation of a state (e.g. 01 --> Alabama)
    
    Returns:
    - dataframe of mapped survey codes to concepts & labels to values  (e.g. B01001A_001E --> SEX BY AGE HISPANIC OR LATINO ALONE UNDER 5 --> 864,675)
    """

    url = f'https://api.census.gov/data/{YEAR}/acs/acs5?get=group({survey_code})&for=state:{state_fips}'
    print(f"url: {url}")
    r = requests.get(url)
    r_json = r.json()

    variables_to_values = dict(zip(r_json[0][:-3], r_json[1][:-3]))
    variables_to_concepts_and_labels_mapping = get_variables_to_concepts_and_labels_mapping(survey_code)
    variables_to_values = {variables_to_concepts_and_labels_mapping[k]:v for k,v in variables_to_values.items() if v != None and k in variables_to_concepts_and_labels_mapping}
            
    return variables_to_values

### ----- MAIN -----

# attempt to read year, not a great check - should improve this
if len(sys.argv) > 1:
    try:
        YEAR = str(sys.argv[1])
        data = get_data_by_group_and_state('B01001A', '01')
    except:
        print("invalid year entered for ACS, please try again")
        exit()

# get survey codes per state
survey_codes = generate_survey_codes_for_each_state()

# generate CSVs
# format: CONCEPT + LABEL --> VALUE
for state in states.STATES:
    print(f"working on state {state.name}")
    state_df = pd.DataFrame()
    for survey_code in survey_codes:
        survey_data = get_data_by_group_and_state(survey_code, str(state.fips))
        survey_df = pd.DataFrame.from_dict(survey_data, orient='index', columns=['Values'])
        state_df = pd.concat([state_df, survey_df])

    print(state_df)
    state_df.to_csv(f'{state.name}_{YEAR}.csv')
    print(f"finished {state.name}")
