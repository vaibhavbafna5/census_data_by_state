## Demographic Census Data by State

Spec can be found [here](https://docs.google.com/document/d/16SBPGHY_kbDQLDR4tlT1_5sBnIhIpfFftw5X8WJhvEE/edit)

### Setup Instructions
* initialize virtual environment
* install dependencies specified in `requirements3.txt` (note: requirements are excessive, but necessary if using Jupyter)

### Running Instructions
`python generate_census_data_by_state.py` - generates CSVs for 50 states based on 2021 data

`python generate_census_data_by_state.py [year]` - generates CSVs for 50 states based on data for the specified year, otherwise fails gracefully if year desired isn't available 
