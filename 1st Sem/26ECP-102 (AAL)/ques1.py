"""
    Calculate the co-realtion coefficient for the following data.
    x = [10,12,15,18,20,25]
    y = [20,24,30,35,40,48]
    plot the graph with the title, x,y axis label

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

x = np.array([10, 12, 15, 18, 20, 25])
y =  np.array([20, 24, 30, 35, 40, 48])

df = pd.DataFrame(x,y)

print("Correlation-Coefficient:")
print(df.corr())

plt.scatter(x, y)
plt.title("Correlation X and Y")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()
