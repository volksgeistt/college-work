"""
for the given dataset, 'Data.csv', calc the mean, median and standard deviation
for the specified numerical column. (don't use df.describe)
"""
import pandas as pd

df = pd.read_csv("data.csv")

mean = df["Pulse"].mean()
median = df["Pulse"].median()
std_dev = df["Pulse"].std()

print(f"Mean: {mean}")
print(f"Median: {median}")
print(f"Standard Deviation: {std_dev}")



