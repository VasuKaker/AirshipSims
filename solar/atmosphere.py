import casadi as cas
import numpy as np

R_universal = 8.31432  # J/(mol*K); universal gas constant
M_air = 28.9644e-3  # kg/mol; molecular mass_total of air
R_air = R_universal / M_air  #


def get_pressure_at_altitude(altitude):
    """
    Fit to the 1976 COESA model; see "Gists and Ideas/Atmosphere Fitting" for details.
    Valid from 0 to 40 km.
    :param altitude:
    :return:
    """
    altitude_scaled = altitude / 40000

    p1 = -1.822942e+00
    p2 = 5.366751e+00
    p3 = -5.021452e+00
    p4 = -4.424532e+00
    p5 = 1.151986e+01

    x = altitude_scaled
    logP = p5 + x * (p4 + x * (p3 + x * (p2 + x * (p1))))

    pressure = cas.exp(logP)

    return pressure


def get_temperature_at_altitude(altitude):
    """
    Fit to the 1976 COESA model; see "Gists and Ideas/Atmosphere Fitting" for details.
    Valid from 0 to 40 km.
    :param altitude:
    :return:
    """

    altitude_scaled = altitude / 40000

    p1 = -2.122102e+01
    p2 = 7.000812e+01
    p3 = -8.759170e+01
    p4 = 5.047893e+01
    p5 = -1.176537e+01
    p6 = -3.566535e-02
    p7 = 5.649588e+00

    x = altitude_scaled
    logT = p7 + x * (p6 + x * (p5 + x * (p4 + x * (p3 + x * (p2 + x * (p1))))))

    temperature = cas.exp(logT)

    return temperature


def get_density_at_altitude(altitude):
    # More efficient to do this using equation of state, but you can use this if you really want.

    P = get_pressure_at_altitude(altitude)
    T = get_temperature_at_altitude(altitude)

    rho = P / (T * R_air)

    return rho


def get_speed_of_sound_from_temperature(temperature):
    """
    Finds the speed of sound from a_cruise specified temperature. Assumes ideal gas properties.
    :param temperature: Temperature, in Kelvin
    :return: Speed of sound, in matrix/s
    """
    return cas.sqrt(1.4 * R_air * temperature)


def get_viscosity_from_temperature(temperature):
    """
    Finds the dynamics viscosity of air from a_cruise specified temperature. Uses Sutherland's Law
    :param temperature: Temperature, in Kelvin
    :return: Dynamic viscosity, in kg/(matrix*s)
    """
    # Uses Sutherland's law from the temperature
    # From CFDWiki

    # Sutherland constant
    C1 = 1.458e-6  # kg/(matrix*s*sqrt(K))
    S = 110.4  # K

    mu = C1 * temperature ** (3 / 2) / (temperature + S)
    return mu


if __name__ == "__main__":
    test_altitudes = cas.linspace(0, 40000, 201)
    test_pressures = get_pressure_at_altitude(test_altitudes)
    test_temps = get_temperature_at_altitude(test_altitudes)
    print(test_pressures)
    print(test_pressures.shape)
    print("test_pressure at 15000 is: ", test_pressures[int(15000/40000*201)])
    print(test_altitudes)
    print(test_altitudes.shape)
