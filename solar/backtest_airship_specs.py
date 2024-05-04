import pandas as pd
import subprocess
import re
from airship_lowaltitude import get_pressure_at_altitude, get_temperature_at_altitude, get_viscosity_from_temperature, get_density_at_altitude, form_factor_ellipsoid, Cf_flat_plate
import math
import matplotlib.pyplot as plt
import numpy as np
import argparse
import airship_lowaltitude as airship_lowaltitude

POWER_PAYLOAD = 250

def compute_solar_input(airship_results, solar_intensity):
    # Access the 'S_solar' attribute from airship_results
    S_solar = airship_results['S_solar']
    
    # Multiply 'S_solar' by the solar_intensity
    solar_input = S_solar * solar_intensity

    eta_charging = 0.98
    eta_motor = 0.85
    eta_solar = 0.22
    electrical_power = solar_input * eta_charging * eta_motor * eta_solar
    
    return electrical_power


def compute_energy_consumption(airship_results, airspeed):
    # Constants
    g = 9.81  # m/s^2

    # Conditions
    altitude = 30  # m, 65 kft = 19812 m
    airspeed = airspeed  # m/s, wind speed at altitude

    P = get_pressure_at_altitude(altitude)
    T = get_temperature_at_altitude(altitude)
    mu = get_viscosity_from_temperature(T)
    rho = get_density_at_altitude(altitude)

    # Design
    length = airship_results["length"]
    diameter = airship_results["diameter"]

    fineness_ratio = length / diameter

    # Wetted area
    a = length / 2
    b = diameter / 2
    c = diameter / 2
    p = 1.6
    
    S_wetted = 4 * math.pi * (
            (
                    (a * b) ** p + (a * c) ** p + (b * c) ** p
            ) / 3
    ) ** (1 / p)  # Approximate, but very close (<2%)

    # Drag buildup

    q = 0.5 * rho * airspeed ** 2

    Re_fuse = rho * airspeed * length / mu
    
    form_factor = form_factor_ellipsoid(fineness_ratio)
    Cf_fuse = Cf_flat_plate(Re_fuse) * form_factor

    drag_fuse = q * Cf_fuse * S_wetted

    drag_total = drag_fuse / 0.51  # taken from typical blimp ratios given in link at top

    # Propulsion
    thrust = drag_total

    propeller_diameter = airship_results["propeller_diameter"]  # diameter per propeller

    n_propellers = 1
    area_propulsive = math.pi / 4 * propeller_diameter ** 2 * n_propellers
    coefficient_of_performance = 0.7  # a total WAG

    power = 0.5 * thrust * airspeed * (
            (
                    thrust / (area_propulsive * airspeed ** 2 * rho / 2) + 1
            ) ** 0.5 + 1
    ) / coefficient_of_performance

    return power + POWER_PAYLOAD



def backtest_airship(airship_results, solar_windspeed_data):
    print("airship_results is: ", airship_results)
    initial_battery_energy = airship_results["mass_battery"] * airship_results["BATTERY_SPECIFIC_ENERGY"]
    solar_area = airship_results["S_solar"]

    # Make a copy of solar_windspeed_data
    solar_windspeed_data_copy = solar_windspeed_data[:]

    # Apply compute_energy_consumption function on the dataframe, looking at the 'Wind Speed' column
    solar_windspeed_data_copy['Energy Consumption'] = solar_windspeed_data_copy['Wind Speed'].apply(lambda x: compute_energy_consumption(airship_results, x))

    # Apply compute_solar_input on the dataframe, looking at the 'GHI' column
    solar_windspeed_data_copy['Solar Input'] = solar_windspeed_data_copy['GHI'].apply(lambda x: compute_solar_input(airship_results, x))


    # # Take the initial battery energy (variable defined), and subtract the output of compute_energy_consumption and add the output of compute_solar_input
    # solar_windspeed_data_copy['Battery Energy'] = initial_battery_energy - solar_windspeed_data_copy['Energy Consumption'] + solar_windspeed_data_copy['Solar Input']
    
    battery_energy_list = [initial_battery_energy]
    # print("len(solar_windspeed_data_copy) is: ", len(solar_windspeed_data_copy))
    for i in range(1, len(solar_windspeed_data_copy)):
        energy_consumed = solar_windspeed_data_copy['Energy Consumption'].iloc[i]
        solar_energy_output = solar_windspeed_data_copy['Solar Input'].iloc[i]

        if not (np.isnan(energy_consumed) or np.isnan(solar_energy_output)):
            energy = battery_energy_list[-1] - energy_consumed + solar_energy_output
        else:
            energy = battery_energy_list[-1]
        
        energy = min(energy, initial_battery_energy)
        
        battery_energy_list.append(energy)
        # print("energy is: ", energy)

    assert len(battery_energy_list) == len(solar_windspeed_data_copy)

    solar_windspeed_data_copy['Battery Energy'] = battery_energy_list
        
    return solar_windspeed_data_copy

def visualize_battery_SOC(findings, results, name):
    plt.figure(figsize=(10,6))
    plt.plot(findings.index/24, findings['Battery Energy']/1000)
    plt.xlabel('Time (Days)')
    plt.ylabel('Battery Energy (kWh)')
    plt.title('Battery Energy over Time')
    plt.grid(True)
    params = ['length', 'diameter', 'mass_total', 'mass_battery', 'S_solar']
    param_values = [results[param] for param in params]
    legend_text = "\n".join([f"{param}: {value:.2f}" for param, value in zip(params, param_values)])
    y_pos = min(findings['Battery Energy']) if  min(findings['Battery Energy']) < 0 else  min(findings['Battery Energy'])
    plt.text(0, y_pos / 1000, legend_text, horizontalalignment='left', 
         verticalalignment='bottom', fontsize=12, bbox=dict(facecolor='none', edgecolor='black'))

    plt.savefig(f'backtest_results/{name}.png')
    # plt.show()

    # plt.show()

def main(airspeed, battery_hours, filename):
    results = airship_lowaltitude.main(airspeed, battery_hours)
    solar_windspeed_data = pd.read_csv('processed_solar_wind_data_LA_2021.csv')
    findings = backtest_airship(results, solar_windspeed_data)
    visualize_battery_SOC(findings, results, filename)
    return findings, results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', '--filename', type=str, help='Filename to save the backtesting results to')
    parser.add_argument('-a', '--airspeed', type=float, help='Airspeed for the airship')
    parser.add_argument('-b', '--battery_hours', type=float, help='Battery hours for the airship')
    
    args = parser.parse_args()
    filename = args.filename
    airspeed = args.airspeed
    battery_hours = args.battery_hours
    main(airspeed, battery_hours, filename)