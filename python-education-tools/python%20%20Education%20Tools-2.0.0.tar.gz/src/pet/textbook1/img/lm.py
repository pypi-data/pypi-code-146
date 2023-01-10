import matplotlib.pyplot as plt
import scipy as sp
import seaborn as sns
from pet.data.load_data import load_data

students = load_data('st.xlsx')
g = sns.lmplot(x="数学", y="总分", robust=True, data=students)


def annotate(data, **kws):
    r, p = sp.stats.pearsonr(students['数学'], students['总分'])
    ax = plt.gca()
    ax.text(.05, .8, 'r={:.2f}, p={:.2g}'.format(r, p),
            transform=ax.transAxes)


g.map_dataframe(annotate)
plt.show()
