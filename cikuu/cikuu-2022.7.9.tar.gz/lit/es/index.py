# 2022.8.7
from lit import *

app_state = st.experimental_get_query_params()
if not isinstance(app_state, str): app_state = {k: v[0] if isinstance(v, list) else v for k, v in app_state.items()} 
if 'f' in app_state: 
	x = __import__(f"func.{app_state['f']}", fromlist=['run'])
	x.run(app_state)
else: 
	st.title("Func list [ run() ]")
	for root, dirs, files in os.walk("func",topdown=False):
		for file in files: 
			if file.endswith(".py") and not file.startswith("_") : 
				file = file.split(".")[0]
				st.write(f"[{file}](?f={file})")

if __name__ == '__main__': 
	pass 