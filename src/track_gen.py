import csv
import numpy as np
from scipy.interpolate import splprep, splev
import matplotlib.pyplot as plt

data = list(csv.reader(open("./lap.csv"), quoting=csv.QUOTE_NONNUMERIC))

pts = np.asarray(data)

#B-spline representation of N dimentional curve
tck, u = splprep(pts.T, u=None, s=0.0, per=1) 
u_new = np.linspace(u.min(), u.max(), 500)
x_new, y_new = splev(u, tck, der=0)

plt.plot(pts[:,0], pts[:,1], 'ro')
plt.plot(x_new, y_new, 'b--')
plt.show()
