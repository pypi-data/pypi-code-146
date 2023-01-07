import argparse
import requests

url = "https://dbc-b6c4ca60-2788.cloud.databricks.com/api/2.0/clusters/spark-versions?token=dapi75bb6f2e6e903bf9d18872fcc84f3ba1"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)


def main():

	parser = argparse.ArgumentParser(prog ='gfg',
									description ='GfG article demo package.')

	parser.add_argument('integers', metavar ='N', type = int, nargs ='+',
						help ='an integer for the accumulator')
	parser.add_argument('-greet', action ='store_const', const = True,
						default = False, dest ='greet',
						help ="Greet Message from Geeks For Geeks.")
	parser.add_argument('--sum', dest ='accumulate', action ='store_const',
						const = sum, default = max,
						help ='sum the integers (default: find the max)')

	args = parser.parse_args()
 
 

	if args.greet:
		print("Welcome to GeeksforGeeks !")
		if args.accumulate == max:
			print("The Computation Done is Maximum")
		else:
			print("The Computation Done is Summation")
		print("And Here's your result:", end =" ")

	print(args.accumulate(args.integers))
