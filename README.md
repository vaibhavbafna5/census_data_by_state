## Demographic Census Data by State

### General
Spec can be found [here](https://docs.google.com/document/d/16SBPGHY_kbDQLDR4tlT1_5sBnIhIpfFftw5X8WJhvEE/edit).

CSV files are saved in the current directory as `[STATE_NAME]_[YEAR].csv`

### Setup
* initialize virtual environment for python > 3.7
* install dependencies specified in `requirements3.txt`

### Running
`python generate_census_data_per_state_by_year.py` - generates CSVs for 50 states based on 2020 data

`python generate_census_data_per_state_by_year.py [year]` - generates CSVs for 50 states based on data for the specified year
