import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
def S(x, p=0, c=1): #defino la función sigmoidea
    return 1/(1+np.exp(-(p+c*x)))
c = np.linspace(0,20,20)
rhos = np.linspace(-10,10,20)
x = np.linspace(-20,20,100)
for i in range(20):
  plt.plot(x,S(x,p=0,c=c[i]),alpha = ( 1/(i+1)))
plt.savefig()
plt.show()
