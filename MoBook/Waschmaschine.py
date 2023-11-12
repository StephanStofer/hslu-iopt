import numpy as np
import pyomo.environ as pyo

model = pyo.ConcreteModel("Waschmaschine in matrix form")

# Define the number of variables and constraints
n_vars = 3
n_constraints = 3
model.I = pyo.Set(initialize=range(n_vars), doc="Set of variables")
model.J = pyo.Set(initialize=range(n_constraints), doc="Set of constraints")

# Decision variables and their domain
model.x = pyo.Var(model.I, domain=pyo.NonNegativeReals)

# Define the vectors and matrices
c = np.array([-3000, -3400, -2200])
A = np.array([[-6, -8, 0], [0, 0, -1], [-8, -9, -4]])
b = np.array([-400, -120, -1000])


# Objective function
@model.Objective(sense=pyo.minimize)
def profit(m):
    return sum(c[i] * m.x[i] for i in model.I)


# Constraints
@model.Constraint(model.J)
def contraints(m, j):
    return sum(A[j, i] * m.x[i] for i in model.I) >= b[j]


# Solve and print solution
solver = pyo.SolverFactory('cbc')
solver.solve(model)
optimal_x = [pyo.value(model.x[i]) for i in model.I]
print(f"x = {tuple(np.round(optimal_x, 1))}")
print(f"optimal value = {-pyo.value(model.profit):.1f}")
