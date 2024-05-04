The code here does the design, optimization, simulation, and backtesting of solar powered airships on low altitudes. Builds upon Peter Sharpe's past work on airship design for high altitudes.

1. We first extract relevant weather data from the NREL NSRDB database. We choose Los Angeles for our case study, extracting all relevant datapoints at hourly intervals over 2021 (historical_solar_data_complete_LA_2021.csv). We then process this, extracting Time, Wind Speed, and GHI (global horizontal irradiation) as our three key variables (processed_solar_wind_data_LA_2021.csv)

2. In the solar/ directory, we modify Peter Sharpe's airship.py file to airship_lowaltitude.py. We define main() which takes in airspeed and battery_hours_val (defined as 8 in peter sharpe's code, made into a parameter here, creates a battery such that it would take "battery_hours_val" hours of solar energy input @ 400 W m^-2 given the solar coverage to completely charge the battery), and returns an optimized airship design given those constraints.
3. In our backtest_airship_specs.py, we take our airship design and simulate the airship with its battery state of charge over the course of a year.
4. In our grid_search_airship.py file, we then iterate across the search space of design airspeeds (1 - 15) and battery_hours_val (5 - 150), and backtest every single one with our code from backtest_airship_specs.py
5. Our backtests output the battery state of charge (named as "test_{airspeed}_{battery_hours_val}.png" in results/ directory) with details on design construction.
