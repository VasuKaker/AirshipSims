from solar.airship import *
import casadi.tools as tools

# dg = tools.dotgraph(mass_total, direction="LR").write_pdf("model.pdf")
dg = tools.dotgraph(mass_total, direction="LR").write_svg("model.svg")

# import casadi as cas
# import casadi.tools as tools
#
# a = cas.SX(2)
# b = cas.SX(3)
# c = (a + b) * a
#
# tools.dotdraw(c)