
import .jsontool  as jt
import .heron	as he
import .rabbit	as bit

if __name__ == "__main__":
	""" 
	    to run in command line
		hebit json_file [json_files ...] [-other parameters]

	    to run in ipython
		cfg=jt.load_cli('command line input')
		out=he.go(*cfg)
	"""
	he.go()
	""" """
