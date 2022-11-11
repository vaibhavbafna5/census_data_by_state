import sys
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from census import Census
from us.states import STATES
import us
import requests
import pandas as pd

# uncomment below to visualize dataframes
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

# TODO: should put this as an env variable 
API_KEY = 'b3429317418aab0b6f375290db2a3420535d135c'

# TODO: not good to hardcode globals, make it more elegant
YEAR = '2021'

def generate_survey_codes_for_each_state():
    """
    A true beast of a function. 
    Takes more LOC than hardcoding the survey codes. 
    """
    codes = []
    for i in range(ord('A'), ord('I') + 1):
        letter = str.upper(chr(i))
        full_code = f'B01001{letter}'
        codes.append(full_code)
    
    codes
    return codes

def get_variable_names_to_labels_mapping(full_variables):
    """    
    Params:
    - full_variables : List[str] - list of full variables (e.g. ['B01001A_001E', 'B01001A_002E'])
    
    Returns:
    - mapping of inscrutable Census code --> CONCEPT + LABEL (e.g. 
    
    Approach partly ripped from here --> shorturl.at/bkLOP.
    """

    variables_to_labels = {}
    
    for full_variable in full_variables:
        variable_table_url = f'https://api.census.gov/data/{YEAR}/acs/acs5/variables/{full_variable}.html'
        v_table = pd.read_html(variable_table_url)
        variable_df = pd.DataFrame(v_table[0])
        variable_df['Label'].replace({"!!": " ", ":": ""}, regex=True, inplace=True)
        
        variables_to_labels[full_variable] = variable_df.iloc[0]['Concept'] + " " + variable_df.iloc[0]['Label']
        
    return variables_to_labels

def get_data_by_group_and_state(group, state):
    """
    Params:
    - group : str - group level tag (e.g. B01001A)
    - state : str - number representation of a state (e.g. 01 --> Alabama)
    
    Returns:
    - dict (e.g. B01001A_001E --> 864,675)
    """

    url = f'https://api.census.gov/data/{YEAR}/acs/acs1?get=group({group})&for=state:{state}'
    r = requests.get(url)
    r_json = r.json()

    variables_to_values = dict(zip(r_json[0][:-3], r_json[1][:-3]))
    variables_to_values = {k:v for k,v in variables_to_values.items() if v != None} 
            
    return variables_to_values

def main():
    survey_codes = generate_survey_codes_for_each_state()

    for state in STATES:
        print(f"generating csv for {state.name}")
        # intiialize empty dataframe
        state_df = pd.DataFrame(columns=['FULL_VARIABLE', 'CONCEPT', 'VALUE'])

        # get data for each type of survey
        for group_survey_code in survey_codes:
            survey_df = pd.DataFrame(columns=['FULL_VARIABLE', 'CONCEPT', 'VALUE'])

            survey_data = get_data_by_group_and_state(group_survey_code, str(state.fips))
            survey_variables = list(survey_data.keys())

            survey_variable_names_to_labels = get_variable_names_to_labels_mapping(survey_variables)

            # unite full variables, concepts, & numbers into 
            for variable, value in survey_data.items():
                concept = survey_variable_names_to_labels[variable]
                row = {
                    'FULL_VARIABLE' : variable, 
                    'CONCEPT' : concept,
                    'VALUE' : value
                }
                survey_df = survey_df.append(row, ignore_index=True)

            # append each survey df to the overall state df
            state_df = pd.concat([state_df, survey_df])

        state_df = state_df.reset_index(drop=True)
        state_df.to_csv(f'{state.name}.csv')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        YEAR = YEAR
        
    main()