import numpy as np
import matplotlib.pyplot as plt
from solution import fr2_mcol

def kernel(x, t):
    return 1 / (1 - x * t)

def rhs(x):
    return 1 + x ** 2

a = -0.5
b = 0.5
n = 101
X = np.linspace(a, b, n)
lamb = -1

x, y = fr2_mcol(lamb, X, kernel, rhs)

plt.plot(x, y, label="Наближений розв'язок")
plt.title("Наближений розв’язок методом колокації")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid()
plt.show()
