import casadi as cas

try:
    from atmosphere import *
    from aerodynamics import *
except ModuleNotFoundError:
    from .atmosphere import *
    from .aerodynamics import *

def main(airspeed_val, battery_hours_val):
    opti = cas.Opti()
    BATTERY_HOURS_VAL = battery_hours_val
    BATTERY_SPECIFIC_ENERGY = 225
    # Constants
    g = 9.81  # m/s^2

    # Conditions
    altitude = opti.parameter()  # m, 65 kft = 19812 m
    opti.set_value(altitude, 30)

    airspeed = opti.parameter()  # m/s, wind speed at altitude
    opti.set_value(airspeed, airspeed_val)

    P = get_pressure_at_altitude(altitude)
    T = get_temperature_at_altitude(altitude)
    mu = get_viscosity_from_temperature(T)
    rho = get_density_at_altitude(altitude)

    # Design
    length = 50 * opti.variable()
    opti.set_initial(length, 50)
    opti.subject_to([
        length / 5 > 1,
    ])

    opti.subject_to([
        length / 100 < 1,
    ])

    diameter = 10 * opti.variable()
    opti.set_initial(diameter, 10)
    opti.subject_to([
        diameter / 1 > 1,
    ])

    fineness_ratio = length / diameter

    ### Geometry


    # Wetted area
    a = length / 2
    b = diameter / 2
    c = diameter / 2
    p = 1.6
    S_wetted = 4 * cas.pi * (
            (
                    (a * b) ** p + (a * c) ** p + (b * c) ** p
            ) / 3
    ) ** (1 / p) # Approximate, but very close (<2%)

    # Volume
    volume = 4 / 3 * cas.pi * a * b * c

    ### Aerodynamics
    # Tail sizing
    C_ht = 0.065  # tail volume coefficient
    L_ht = 0.35  # tail lever arm
    S_tail = C_ht * length * volume ** (2 / 3) / L_ht
    AR_ht = 0.5  # tail aspect ratio
    b_tail = 2 * diameter / length * cas.sqrt(
        (length / 2) ** 2 - length ** 2
    ) + 2 * cas.sqrt(
        S_tail / 2 * AR_ht
    )

    # Drag buildup

    q = 0.5 * rho * airspeed ** 2

    Re_fuse = rho * airspeed * length / mu
    form_factor = form_factor_ellipsoid(fineness_ratio)
    Cf_fuse = Cf_flat_plate(Re_fuse) * form_factor

    drag_fuse = q * Cf_fuse * S_wetted

    drag_total = drag_fuse / 0.51  # taken from typical blimp ratios given in link at top

    ### Buoyancy
    # Inner mass
    overpressure = 240  # Pa, citing Raymer
    fill_pressure = P + overpressure  # ambient pressure
    # fill_molar_mass = 0.00100784  # kg / mol, Hydrogen
    fill_molar_mass = 0.00400260 # kg / mol, Helium
    mass_fill = fill_pressure * volume * fill_molar_mass / R_universal / T

    # Displaced mass
    mass_displaced = rho * volume

    # Force calculation
    force_buoyant = (mass_displaced - mass_fill) * g

    ### Propulsion

    ## Motor and prop
    thrust = drag_total

    propeller_diameter = opti.variable()  # diameter per propeller
    opti.set_initial(propeller_diameter, 5)
    opti.subject_to([
        propeller_diameter / 0.1 > 1
    ])

    n_propellers = 1
    area_propulsive = cas.pi / 4 * propeller_diameter ** 2 * n_propellers
    coefficient_of_performance = 0.7  # a total WAG

    power = 0.5 * thrust * airspeed * (
            (
                    thrust / (area_propulsive * airspeed ** 2 * rho / 2) + 1
            ) ** 0.5 + 1
    ) / coefficient_of_performance

    mass_motor_raw = power / 4140.8  # 4140.8 W/kg
    mass_motor_mounted = 2 * mass_motor_raw  # similar to a quote from Raymer, modified to make sensible units, prop weight roughly subtracted

    propeller_n_blades = 2
    mass_propellers = n_propellers * 0.495 * (propeller_diameter / 1.25) ** 2 * cas.fmax(1,
                                                                            power / 14914) ** 2  # Baselining to a 125cm E-Props Top 80 Propeller for paramotor, with scaling assumptions

    mass_propulsion = mass_motor_mounted + mass_propellers

    # Account for payload power
    power_payload = 250
    power += power_payload

    ## Solar
    eta_charging = 0.98
    eta_motor = 0.85
    eta_solar = 0.22
    rho_solar = 0.3  # kg/m^2, solar cell area density, from Burton's model
    insolation_solar = 400 * eta_solar # W/m^2, mean daily solar insolation (roughly at 40 deg N @ summer solstice)

    S_solar = power / insolation_solar / eta_charging / eta_motor / eta_solar

    solar_area_fraction = S_solar / (cas.pi * (length / 2) * (diameter/2))
    opti.subject_to([
        solar_area_fraction < 1
    ])

    mass_solar = rho_solar * S_solar

     # Wh/kg, seems high but this is what is used in Burton's solar model, and specs from Amprius seem to indicate it's possible
    mass_battery = 1 * (power * BATTERY_HOURS_VAL) / BATTERY_SPECIFIC_ENERGY
    mass_wires = 0.015 * (length / 3) * (power / 3000)  # a guess from 10 AWG aluminum wire
    mass_propulsion += mass_solar + mass_battery + mass_wires

    ## Gas Engine

    ## Hydrogen Fuel Cell


    ### Structural
    # envelope_area_density = 0.062  # kg/m^2, from https://www.techbriefs.com/component/content/article/tb/techbriefs/materials/1197
    envelope_area_density = 1390 * 0.000051 # kg/m^2, a guess from mylar @ typical weather balloon thicknesses; from https://www.weather.gov/bmx/kidscorner_weatherballoons
    mass_envelope = envelope_area_density * S_wetted
    mass_structural = mass_envelope * (28.5 + 12.5 + 4 + 15) / (28.5) # from (relevant) mass fractions given in Fig. 1. of https://www.dglr.de/publikationen/2018/480209.pdf


    mass_payload = 30

    mass_total = mass_structural + mass_payload + mass_propulsion

    force_weight = mass_total * g

    ### Dynamics
    opti.subject_to([
        force_buoyant / force_weight >= 1
        # force_buoyant >= force_weight
    ])
    LD_effective = force_buoyant / drag_total

    ### Finalize Optimization and Solve
    # opti.subject_to([
    #     length < 50
    # ])
    opti.minimize(mass_total / 5e2)

    p_opts = {}
    s_opts = {}
    s_opts["max_iter"] = 1e2
    s_opts["mu_strategy"] = "adaptive"
    # s_opts["start_with_resto"] = "yes"
    s_opts["required_infeasibility_reduction"] = 0.1
    s_opts["expect_infeasible_problem"] = "yes"
    opti.solver('ipopt', p_opts, s_opts)

    try:
        sol = opti.solve()
    except:
        sol = opti.debug

    ##### Text output
    # out = lambda x, val: print("%s: %f" % (x, val))  # input a variable name as a string
    # print("xs is: ", xs)
    print_title = lambda s: print("\n********** %s **********" % s.upper())

    vars_of_interest = ["length", "diameter", "propeller_diameter", "LD_effective", "S_wetted", "volume", "mass_total", "mass_payload", "mass_structural", "mass_propulsion", "power", "solar_area_fraction", "mass_battery", "BATTERY_SPECIFIC_ENERGY", "S_solar"]
    print_title("Results")

    # for var_name in vars_of_interest:
    #     print(f"{var_name}: {sol.value(eval(var_name, locals()))}")
    results_dict = {}

    for var_name in vars_of_interest:
        results_dict[var_name] = sol.value(eval(var_name, locals()))

    return results_dict

"""
Takeaways:
* For most of the design space, you want a blimp, not a rigid airship. (Rigid gets better for heavier payloads, but is still not great due to altitude.)
* Square-cube law works backwards, you actually can't operate very well in the 30 kg payload design space... f_payload == 0.15 or so.
    Payload mass fractions get better as you get bigger.
* Even the most conservative designs (low wind, allow downrange drift, etc.) are massive - roughly 30 meters long. 
* The need to carry batteries makes a HUGE difference, as this can easily be 1/3 of the TOGW in high winds.
"""

if __name__ == "__main__":
    airspeed_val = 5
    battery_hours_val = 24
    print(main(airspeed_val, battery_hours_val))