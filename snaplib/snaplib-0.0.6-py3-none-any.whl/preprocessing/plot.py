def plot(df):
    plt.figure(figsize=(int(len(df.columns)/4) if len(df.columns)>30 else 10, 10))
    plt.pcolor(df.isnull(), cmap='Blues_r')
    plt.yticks([int(el*(len(df)/10)) for el in range(0, 10)])
    plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns, rotation=80)
    plt.show()
    return plt