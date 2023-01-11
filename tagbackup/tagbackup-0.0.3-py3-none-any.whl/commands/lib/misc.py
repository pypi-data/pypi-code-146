import csv
import io


def tags_to_csv(tags):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(tags)
    return output.getvalue()
