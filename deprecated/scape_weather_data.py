from datetime import datetime, timedelta
import json
import requests

import pandas as pd

def scrape_weather_data_with_selenium(year, month, day):
    r = requests.get(f'https://api.weather.com/v1/location/KBUR:9:US/observations/historical.json?apiKey=e1f10a1e78da46f5b10a1e78da96f525&units=e&startDate={year}{month:02}{day:02}')
    observations = json.loads(r.text)['observations']
    wind_speeds = []
    for observation in observations:
        t = datetime.fromtimestamp(observation['valid_time_gmt']) - timedelta(hours=3)
        t = t.strftime('%m/%d/%Y %I:%M:%S %p')
        wind_speed = observation['wspd']
        wind_speeds.append((t, wind_speed))

    return wind_speeds


def scraped_data_to_df(data, date):
    df = pd.DataFrame(data, columns=['Time', 'Wind Speed'])
    # Add the date to the DataFrame
    df['Date'] = pd.to_datetime(date)

    df = df[['Date', 'Time', 'Wind Speed']]
    return df


if __name__ == '__main__':
    # Usage example
    # Generate a list of dates for the year 2022
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2021, 12, 31)
    date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    weather_data_frames = []
    missing_dates = []
    for date in date_list:
        print("date is: ", date)
        try:
            weather_data_frames.append(scraped_data_to_df(scrape_weather_data_with_selenium(date.year, date.month, date.day), date))
        except:
            print("nothing for date: ", date)
            missing_dates.append(date)

    # Concatenate all the DataFrames into a single large DataFrame
    combined_weather_df = pd.concat(weather_data_frames, ignore_index=True)

    combined_weather_df.head()
    print(combined_weather_df)
    combined_weather_df.to_csv('historical_weather_data_LA_2021.csv')

        # Open a new text file in write mode
    with open('missing_dates.txt', 'w') as file:
        for date in missing_dates:
            file.write(date + '\n')  # write each date on a new line

    print("The file has been created with the missing dates.")

