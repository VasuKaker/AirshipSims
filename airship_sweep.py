import numpy as np
param_range = np.linspace(1, 30, 59)

from solar import *
x_solar = []
y_solar = []
for param in param_range:
    opti.set_value(airspeed, param)
    try:
        sol = opti.solve()
        opti.set_initial(sol.value_variables())
        x_solar.append(param)
        y_solar.append(sol.value(length))
    except:
        pass

from solar_drifting.airship import *
x_solar_drifting = []
y_solar_drifting = []
for param in param_range:
    opti.set_value(airspeed, param * 24 / 8)
    try:
        sol = opti.solve()
        opti.set_initial(sol.value_variables())
        x_solar_drifting.append(param)
        y_solar_drifting.append(sol.value(length))
    except:
        pass

from hydrogen.airship import *
x_hydrogen = []
y_hydrogen = []
for param in param_range:
    opti.set_value(airspeed, param)
    try:
        sol = opti.solve()
        opti.set_initial(sol.value_variables())
        x_hydrogen.append(param)
        y_hydrogen.append(sol.value(length))
    except:
        pass


import matplotlib.pyplot as plt
plt.figure()
plt.plot(x_solar, y_solar, '.-', label="Battery Solar-Electric")
plt.plot(x_solar_drifting, y_solar_drifting, '.-', label = "Drifting Solar-Electric")
plt.plot(x_hydrogen, y_hydrogen, '.-', label = "Hydrogen")
comparison_color = (1, 0.5, 0.5)
# plt.axhline(245, color=comparison_color)
# plt.text(0.1, 246.5, "Hindenburg", color =comparison_color)
plt.axhline(58, color=comparison_color)
plt.text(0.1, 59.5, "Goodyear Blimp", color = comparison_color)
plt.axvline(17, color=comparison_color)
plt.text(17.2, 75, "95% Wind\n(summer, 30N, 60 kft)", rotation = 90, color=comparison_color)
plt.grid(True)
plt.ylim((0, 200))
plt.xlabel("Design Wind Speed [m/s]")
plt.ylabel("Length [m]")
plt.title("Airship Sizing")
plt.legend()
plt.savefig("length.png", dpi=600)
plt.show()



import numpy as np
param_range = np.linspace(1, 30, 59)

from solar import *
x_solar = []
y_solar = []
for param in param_range:
    opti.set_value(airspeed, param)
    try:
        sol = opti.solve()
        opti.set_initial(sol.value_variables())
        x_solar.append(param)
        y_solar.append(sol.value(diameter))
    except:
        pass

from solar_drifting.airship import *
x_solar_drifting = []
y_solar_drifting = []
for param in param_range:
    opti.set_value(airspeed, param * 24 / 8)
    try:
        sol = opti.solve()
        opti.set_initial(sol.value_variables())
        x_solar_drifting.append(param)
        y_solar_drifting.append(sol.value(diameter))
    except:
        pass

from hydrogen.airship import *
x_hydrogen = []
y_hydrogen = []
for param in param_range:
    opti.set_value(airspeed, param)
    try:
        sol = opti.solve()
        opti.set_initial(sol.value_variables())
        x_hydrogen.append(param)
        y_hydrogen.append(sol.value(diameter))
    except:
        pass


import matplotlib.pyplot as plt
plt.figure()
plt.plot(x_solar, y_solar, '.-', label="Battery Solar-Electric")
plt.plot(x_solar_drifting, y_solar_drifting, '.-', label = "Drifting Solar-Electric")
plt.plot(x_hydrogen, y_hydrogen, '.-', label = "Hydrogen")
comparison_color = (1, 0.5, 0.5)
# plt.axhline(245, color=comparison_color)
# plt.text(0.1, 246.5, "Hindenburg", color =comparison_color)
plt.axhline(16.5, color=comparison_color)
plt.text(0.1, 16.7, "Goodyear Blimp", color = comparison_color)
plt.axvline(17, color=comparison_color)
plt.text(17.2, 20, "95% Wind\n(summer, 30N, 60 kft)", rotation = 90, color=comparison_color)
plt.grid(True)
plt.ylim((10, 35))
plt.xlabel("Design Wind Speed [m/s]")
plt.ylabel("Diameter [m]")
plt.title("Airship Sizing")
plt.legend()
plt.savefig("diameter.png", dpi=600)
plt.show()

import numpy as np
param_range = np.linspace(1, 30, 59)

from solar import *
x_solar = []
y_solar = []
for param in param_range:
    opti.set_value(airspeed, param)
    try:
        sol = opti.solve()
        opti.set_initial(sol.value_variables())
        x_solar.append(param)
        y_solar.append(sol.value(mass_total))
    except:
        pass

from solar_drifting.airship import *
x_solar_drifting = []
y_solar_drifting = []
for param in param_range:
    opti.set_value(airspeed, param * 24 / 8)
    try:
        sol = opti.solve()
        opti.set_initial(sol.value_variables())
        x_solar_drifting.append(param)
        y_solar_drifting.append(sol.value(mass_total))
    except:
        pass

from hydrogen.airship import *
x_hydrogen = []
y_hydrogen = []
for param in param_range:
    opti.set_value(airspeed, param)
    try:
        sol = opti.solve()
        opti.set_initial(sol.value_variables())
        x_hydrogen.append(param)
        y_hydrogen.append(sol.value(mass_total))
    except:
        pass

import matplotlib.pyplot as plt
plt.figure()
plt.semilogy(x_solar, y_solar, '.-', label="Battery Solar-Electric")
plt.semilogy(x_solar_drifting, y_solar_drifting, '.-', label = "Drifting Solar-Electric")
plt.plot(x_hydrogen, y_hydrogen, '.-', label = "Hydrogen")
comparison_color = (1, 0.5, 0.5)
plt.axvline(17, color=comparison_color)
plt.text(17.2, 1000, "95% Wind\n(summer, 30N, 60 kft)", rotation = 90, color=comparison_color)
plt.grid(True, which="both", ls="-", color='0.65')
plt.ylim((1e2, 1e4))
plt.xlabel("Design Wind Speed [m/s]")
plt.ylabel("TOGW [kg]")
plt.title("Airship Sizing")
plt.legend()
plt.savefig("togw.png", dpi=600)
plt.show()
