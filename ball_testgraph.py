import numpy as np
import matplotlib.pyplot as plt
import get_rms as gm

filename = gm.get_file_name()

xy = np.loadtxt(filename)
x = [el[0] for el in xy]
y = [el[1] for el in xy]


plt.plot(x,y)
plt.show()
