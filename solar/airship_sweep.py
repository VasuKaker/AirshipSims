from airship import *

param_range = np.linspace(1, 30, 60)
x = []
y = []

for param in param_range:
    opti.set_value(airspeed, param)
    try:
        sol = opti.solve()
        opti.set_initial(sol.value_variables())
        x.append(param)
        y.append(sol.value(length))
    except:
        pass

import matplotlib.pyplot as plt
plt.figure()
plt.plot(x, y, '.-')
plt.grid(True)
plt.xlabel("Design Wind Speed [m/s]")
plt.ylabel("Length [m]")
plt.title("Solar Airship Sizing")
plt.show()

from airship import *

param_range = np.linspace(1, 30, 60)
x = []
y = []

for param in param_range:
    opti.set_value(airspeed, param)
    try:
        sol = opti.solve()
        opti.set_initial(sol.value_variables())
        x.append(param)
        y.append(sol.value(mass_total))
    except:
        pass

import matplotlib.pyplot as plt
plt.figure()
plt.plot(x, y, '.-')
plt.grid(True)
plt.xlabel("Design Wind Speed [m/s]")
plt.ylabel("TOGW [kg]")
plt.title("Solar Airship Sizing")
plt.show()

# import plotly.express as px
# px.line(
#     x=x,
#     y=y,
# ).show()
