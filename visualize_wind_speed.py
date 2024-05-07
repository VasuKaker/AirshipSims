import pandas as pd
import matplotlib.pyplot as plt

def process_and_plot():
    # Read the data
    data = pd.read_csv('processed_solar_wind_data_LA_2021.csv')
    
    # Convert the indices to days
    data.index = data.index / 24
    
    # Create a subplot for wind speed and GHI
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)

    # Plot wind speed
    color = 'tab:blue'
    ax1.set_xlabel('Day')
    ax1.set_ylabel('Wind Speed (m/s)', color=color)
    ax1.plot(data.index, data['Wind Speed'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Plot GHI
    color = 'tab:red'
    ax2.set_xlabel('Day')
    ax2.set_ylabel('GHI (W/m^2)', color=color)
    ax2.plot(data.index, data['GHI'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # Show the plots
    plt.show()

if __name__ == '__main__':
    process_and_plot()