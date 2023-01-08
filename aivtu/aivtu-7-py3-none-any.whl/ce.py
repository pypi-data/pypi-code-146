import csv
with open("3.csv") as f:
    csv_file = csv.reader(f)
    pdata = []
    ndata = []
    for i in list(csv_file):
        if i[-1] == 'Y':
            pdata.append(i)
        elif i[-1] == 'N':
            ndata.append(i)

specific = pdata[1][:-1]
general = ['?' for i in range(len(specific))]
final = []

for i in pdata:
    for j in range(len(specific)):
        if i[j] != specific[j]:
            specific[j] = "?"
for i in ndata:
    for j in range(len(specific)):
        if i[j] != specific[j]:
            general[j] = specific[j]
            if len(set(general)) != 1:
                final.append(general[:])            
            general[j] = "?"

print("\nFinal Specific hypothesis:\n", specific)
print("\nFinal General hypothesis:\n", final)
