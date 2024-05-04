import pandas as pd

def process_weather_data(file_name):
    # Read the csv file
    df = pd.read_csv(file_name)

    # Convert the Year, Month, Day, Hour, Minute columns to a single datetime column
    df['Datetime'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour', 'Minute']])

    # Select only the required columns
    df = df[['Datetime', 'GHI', 'Wind Speed']]

    return df

if __name__ == "__main__":
    processed_data = process_weather_data('historical_solar_data_complete_LA_2021.csv')
    processed_data.to_csv('AirshipSims_PeterSharpe/solar/processed_solar_wind_data_LA_2021.csv')
    processed_data.to_csv('processed_solar_wind_data_LA_2021.csv')
    
    