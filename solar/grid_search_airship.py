from backtest_airship_specs import main
import pandas as pd
import json
from tqdm import tqdm
import argparse
# main(5, 24, 'test.png')

def eval_battery_soc(findings):
    battery_soc = findings['Battery Energy']
    total_battery_capacity = max(battery_soc)
    print("total_battery_capacity is: ", total_battery_capacity)
    percentage_time_20_40 = len([i for i in battery_soc if 0.2*total_battery_capacity <= i <= 0.4*total_battery_capacity])/len(battery_soc)
    percentage_time_below_20 = len([i for i in battery_soc if i < 0.2*total_battery_capacity])/len(battery_soc)

    score = -1*percentage_time_20_40 - 5*percentage_time_below_20

    return score


if __name__ == '__main__':
    vars_of_interest = ["length", "diameter", "propeller_diameter", "LD_effective", "S_wetted", "volume", "mass_total", "mass_payload", "mass_structural", "mass_propulsion", "power", "solar_area_fraction", "mass_battery", "BATTERY_SPECIFIC_ENERGY", "S_solar"]
    df = pd.DataFrame(columns=vars_of_interest)
    findings_dict = {}

    parser = argparse.ArgumentParser(description="Script with blimp_speed argument.")
    
    # Add the -a_s / --additional_speed argument
    parser.add_argument(
        '-b_s', '--blimp_speed',
        type=float,  # Use float or int as appropriate
        default=0.0,  # Set a default value, if needed
        help="Specify an additional speed value"
    )
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Access the additional speed argument
    blimp_speed = float(args.blimp_speed)


    for airspeed in tqdm(range(1, 16)):
        for battery_hours_val in range(5, 155, 5):
            findings, airship_dim = main(airspeed, battery_hours_val, f'test_{airspeed}_{battery_hours_val}', blimp_speed)
            findings_dict[f'{airspeed}_{battery_hours_val}'] = findings['Battery Energy'].tolist()
            
            score = eval_battery_soc(findings)
            new_row = {var: airship_dim[var] for var in vars_of_interest}
            new_row['score'] = score
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    # df = pd.DataFrame(columns=['airspeed', 'battery_hours_val', 'length', 'diameter', 'S_solar', 'mass_battery', 'battery_energy', 'score'])

    with open('findings.json', 'w') as f:
        json.dump(findings_dict, f, indent=4)
    
    df = df.reset_index(drop=True)
    df = df.sort_values(by=['score', 'length'], ascending=[False, True])
    df.to_csv('airship_scores.csv')