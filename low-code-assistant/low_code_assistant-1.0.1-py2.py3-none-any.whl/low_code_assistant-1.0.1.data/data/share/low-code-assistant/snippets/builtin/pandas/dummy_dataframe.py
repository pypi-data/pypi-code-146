# author: Maarten Breddels
# date: Wed 8 Sep 2022
# requires pandas:
#  pip install pandas
import numpy as np
import pandas as pd

N = 100
x = np.arange(N)
y = x**2
z = np.random.random(N)
animal = np.random.choice(["cat", "dog", "cat", "dog"], size=N)

df = pd.DataFrame(
    {
        "x": x,
        "y": y,
        "z": z,
        "animal": animal,
    }
)
df
