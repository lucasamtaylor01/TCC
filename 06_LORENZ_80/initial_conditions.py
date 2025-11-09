from parameters import a, f, nu_0, g_0

# HARDLEY
y1 = f[0]/(a[0]*nu_0*(1+a[0]*g_0))
x1 = -nu_0*a[0]*y1
z1 = y1


x0 = [x1, 0, 0]
y0 = [y1, -(10 ** (-5)), 0]
z0 = [z1, 10 ** (-5), 0]

"""
# DEFAULT

x0 = [0.1,0.1,0.1]
y0 = [0.1,0.1,0.1]
z0 = [0.1,0.1,0.1]
"""

days = 290