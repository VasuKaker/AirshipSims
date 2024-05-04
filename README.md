The code here does the design, optimization, simulation, and backtesting of solar powered airships on low altitudes.

1. We first extract relevant weather data from the NREL NSRDB database. We choose Los Angeles for our case study, extracting all relevant datapoints at hourly intervals over 2021 (historical_solar_data_complete_LA_2021.csv). We then process this, extracting Time, Wind Speed, and GHI (global horizontal irradiation) as our three key variables
2. 
