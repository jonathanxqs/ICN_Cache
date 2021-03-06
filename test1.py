from scipy.optimize import curve_fit
from scipy.special import zetac
import numpy
import matplotlib.pyplot as plt
import scipy.special as sps



def f(x, a):
    return (x**-a)/zetac(a)


result = curve_fit(f, x, y, p0=[0.56])
p = result[0]

print(p)