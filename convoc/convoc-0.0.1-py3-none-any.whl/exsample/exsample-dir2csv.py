from convoc import dir2csv

# Convert directory structure to csv
result = dir2csv(root_dir='target', output='csv/recover.csv', level=2)

# Output list of converted directories
# At the same time, csv/recover.csv is generated.
print(result)