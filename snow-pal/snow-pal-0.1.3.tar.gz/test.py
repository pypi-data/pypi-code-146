import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import snowpal

#pal = snowpal.palettes('poo')

#print(pal)




pal = ['#beb94d','#828155','#4f581d','#30401c','#272b1c']
sns.palplot(pal)
plt.show()


data = np.array([1,2,3,4,4,4,5,5,5,5,5,5,5,5,6,6,6,6,7,7,7,8,9,10])
sns.boxplot(
    data=[data, data*1.2, data*1.7, data*2.1, data*2.6],
    palette=pal,
)
plt.show()