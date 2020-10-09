import time
import sympy as sp
import numpy as np
import marshal as ms
import dill

dill.settings['recurse'] = True

from numpy import *
d2r = np.deg2rad
r2d = np.degrees

from sympy.physics.vector import init_vprinting
from sympy.physics.mechanics import dynamicsymbols

theta, alpha, a, d = dynamicsymbols('theta alpha a d')

rot = sp.Matrix([[sp.cos(theta), -sp.sin(theta)*sp.cos(alpha), sp.sin(theta)*sp.sin(alpha)],
                 [sp.sin(theta), sp.cos(theta)*sp.cos(alpha), -sp.cos(theta)*sp.sin(alpha)],
                 [0, sp.sin(alpha), sp.cos(alpha)]])

trans = sp.Matrix([a*sp.cos(theta),a*sp.sin(theta),d])

last_row = sp.Matrix([[0, 0, 0, 1]])

# DH-matrix
m = sp.Matrix.vstack(sp.Matrix.hstack(rot, trans), last_row)

theta1, theta2, theta3 = dynamicsymbols('theta1 theta2 theta3')

# Link lenghts [m]
d1 = 0.034
a2 = 0.08
a3 = 0.14

# Compute DH-matrix
m01 = m.subs({theta:theta1, d:d1, a:0, alpha:pi/2})
m12 = m.subs({theta:pi/2+theta2, d:0, a:a2, alpha:0})
m23 = m.subs({theta:-pi/2+theta3, d:0, a:a3, alpha:0})
m34 = m.subs({theta:pi/2, d:0, a:0, alpha:pi/2})
m04 = (m01*m12*m23*m34)

mtcp = sp.simplify(m04)

# Create function
px = mtcp[0,3]
py = mtcp[1,3]
pz = mtcp[2,3]
fx = sp.lambdify((theta1, theta2, theta3), px, 'numpy')
fy = sp.lambdify((theta1, theta2, theta3), py, 'numpy')
fz = sp.lambdify((theta1, theta2, theta3), pz, 'numpy')

dill.dump(fx, open("fx", "wb"))
dill.dump(fy, open("fy", "wb"))
dill.dump(fz, open("fz", "wb"))

print(time.clock())