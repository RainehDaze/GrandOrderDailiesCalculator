"""Calculates expected # of dailies to run based on desired number of gems/pieces etc.
 with data taken from the overall dailies droprate sheets

 IF UNFAMILIAR WITH PROGRAMMING: only change the values before problem.
 e.g. change pieces = 12 to pieces = 30 if you want more pieces.
 Then press run."""

from pulp import *

pieces = 12
monuments = 12
blue = 32
red = 32
gold = 32  # Number of each desired material. Change here (default: SR values)

problem = LpProblem("Saber Dailies", LpMinimize)  # problem to solve

ap_ten = LpVariable("10AP", 0, None, LpInteger)
ap_twenty = LpVariable("20AP", 0, None, LpInteger)
ap_thirty = LpVariable("30AP", 0, None, LpInteger)
ap_forty = LpVariable("40AP", 0, None, LpInteger)

problem += 10*ap_ten + 20*ap_twenty + 30*ap_thirty + 40*ap_forty, "AP Used"  # the objective function
problem += 0.222*ap_ten + 0.694*ap_twenty + 0.998*ap_thirty + 0.742*ap_forty >= pieces, "Pieces Required"  # constraints
problem += 0.023*ap_ten + 0.086*ap_twenty + 0.346*ap_thirty + 0.521*ap_forty >= monuments, "Monuments Required"  # constraints
problem += 1.259*ap_ten + 1.067*ap_twenty >= blue, "Blue Gems Required"  # constraints
problem += 0.825*ap_twenty + 1.345*ap_thirty + 1.169*ap_forty >= red, "Red Gems Required"  # constraints
problem += 0.052*ap_thirty + 0.283*ap_forty >= gold, "Gold Gems Required"  # constraints

problem.writeLP("SaberDailies.lp")

problem.solve()

print("Status:", LpStatus[problem.status])

for v in problem.variables():
    print(v.name, "=", v.varValue)
print("Total AP Required: ", value(problem.objective))