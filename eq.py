import re

import numpy as np

eq_string = """\
offset = 4 + random + 1
location = 1 + origin + offset
origin = 3 + 5
random = 2


"""


class Equation:
  def __init__(self, eq_str):
    # self.vars = set()
    self.sub_eqs = []
    # { var: {subequation_index: coefficient}}
    self.coefficients = {}
    self.values = []
    self.scan_for_variable(eq_str)

  def add_variable_coefficient(self, var, co, subeq_idx):

    if var in self.coefficients:
      curr_co = self.coefficients[var].get(subeq_idx, 0)
      curr_co += co
      self.coefficients[var][subeq_idx] = curr_co
    else:
      self.coefficients[var] = {subeq_idx: co}

  def scan_for_variable(self, eq_str):

    subeq_idx = 0
    for l in eq_str.splitlines():
      if len(l.strip()) == 0:
        continue

      self.sub_eqs.append(l)
      lhs_var, rhs = (x.strip() for x in l.split('='))

      # LHS
      self.add_variable_coefficient(lhs_var, 1, subeq_idx)

      # RHS

      elements = list(x for x in re.split(r'[ =\+]', rhs) if len(x) > 0)
      for elem in elements:
        # check for empty string
        try:
          if len(self.values) == subeq_idx:
            self.values.append(0)
          v = int(elem)
        except ValueError:
          self.add_variable_coefficient(elem, -1, subeq_idx)
          # self.vars.add(elem)
        else:
          self.values[subeq_idx] += v

      subeq_idx += 1

  def construct_coefficient_matrix(self):
    total_vars = len(self.coefficients)
    co_matrix = np.zeros((total_vars, total_vars))
    var_count = 0
    for var, subeq_co in self.coefficients.items():
      for subeq_idx, co in subeq_co.items():
        co_matrix[subeq_idx, var_count] = co

      var_count += 1

    return co_matrix

  def solve(self):
    co = self.construct_coefficient_matrix()
    solution = np.linalg.solve(co, self.values)
    for i, var in enumerate(self.coefficients):
      print var, solution[i]
    return solution


equation = Equation(eq_string)
equation.solve()
