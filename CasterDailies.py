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

problem = LpProblem("Caster Dailies", LpMinimize)  # problem to solve

ap_ten = LpVariable("10AP", 0, None, LpInteger)
ap_twenty = LpVariable("20AP", 0, None, LpInteger)
ap_thirty = LpVariable("30AP", 0, None, LpInteger)
ap_forty = LpVariable("40AP", 0, None, LpInteger)

problem += 10*ap_ten + 20*ap_twenty + 30*ap_thirty + 40*ap_forty, "AP Used"  # the objective function
problem += 0.332*ap_ten + 0.830*ap_twenty + 0.964*ap_thirty + 0.804*ap_forty >= pieces, "Pieces Required"  # constraints
problem += 0.019*ap_ten + 0.071*ap_twenty + 0.323*ap_thirty + 0.567*ap_forty >= monuments, "Monuments Required"  # constraints
problem += 1.247*ap_ten + 0.966*ap_twenty >= blue, "Blue Gems Required"  # constraints
problem += 0.790*ap_twenty + 1.727*ap_thirty + 0.903*ap_forty >= red, "Red Gems Required"  # constraints
problem += 0.224*ap_thirty + 0.768*ap_forty >= gold, "Gold Gems Required"  # constraints

problem.writeLP("CasterDailies.lp")

problem.solve()

print("Status:", LpStatus[problem.status])

for v in problem.variables():
    print(v.name, "=", v.varValue)
print("Total AP Required: ", value(problem.objective))