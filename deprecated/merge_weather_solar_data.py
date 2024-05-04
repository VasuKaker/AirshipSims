# import pandas as pd

# def merge_solar_windspeed_data(solar_data, wind_speed_data):
#     # Filter for 2021 data
#     solar_data = solar_data[solar_data['Year'] == 2021]

#     # Load the weather data
#     weather_data = pd.read_csv('historical_weather_data_LA_2021.csv')
#     print(weather_data)
#     # Convert the Time column to datetime
#     weather_data['Time'] = pd.to_datetime(weather_data['Time'])
#     # Round the time to the nearest half hour
#     weather_data['Time'] = weather_data['Time'].dt.round('30min')
#     weather_data = weather_data.drop_duplicates(subset='Time', keep='first').reset_index()
#     weather_data['Time'] = weather_data['Time'] - pd.Timedelta(minutes=30)
#     print(weather_data)

#     # Convert the Year, Month, Day, Hour, Minute columns to a datetime object
#     solar_data['Time'] = pd.to_datetime(solar_data[['Year', 'Month', 'Day', 'Hour', 'Minute']])
#     # Round the time to the nearest half hour
#     solar_data['Time'] = solar_data['Time'].dt.round('30min')
#     print("solar data is: ")
#     print(solar_data)
#     # Merge the solar and weather data on the Time column
#     merged_data = pd.merge(solar_data, weather_data, on='Time', how='left')
#     merged_data = merged_data.drop(columns=["index", "Unnamed: 0", "Year", "Month", "Day", "Hour", "Minute", "Date"])
#     print(merged_data.columns)
#     merged_data = merged_data[["Time", "Wind Speed", "GHI"]]
#     return merged_data


# if __name__ == '__main__':
#     # Load the solar data
#     solar_data = pd.read_csv('historical_solar_data_complete_LA_2021.csv')
#     weather_data = pd.read_csv('historical_weather_data_LA_2021.csv')
#     merged_data = merge_solar_windspeed_data(solar_data, weather_data)
#     merged_data.to_csv('merged_solar_windspeed_data_LA.csv')
#     merged_data.to_csv('AirshipSims_PeterSharpe/solar/merged_solar_windspeed_data_LA.csv')
#     print(merged_data.head(n=100))

