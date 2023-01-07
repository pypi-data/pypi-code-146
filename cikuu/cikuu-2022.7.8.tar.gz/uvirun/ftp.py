# 2022.12.31  uvicorn ftp:app --host 0.0.0.0 --port 80 --reload
import fastapi,uvicorn,re,os
from collections import Counter

app		= fastapi.FastAPI()
from fastapi.middleware.cors import CORSMiddleware  #https://fastapi.tiangolo.com/zh/tutorial/cors/
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

from fastapi.staticfiles import StaticFiles #http://localhost/static/index.html | https://9to5answer.com/how-to-serve-static-files-in-fastapi
app.mount("/static", StaticFiles(directory="static", html = True), name="static")  # index.html 

@app.get('/')
def home():  return fastapi.responses.HTMLResponse(content=f"<h2> ftp filelist </h2><a href='/docs'> docs </a> | <a href='/redoc'> redoc </a><br>last update: 2022.12.31")

if __name__ == "__main__":   #uvicorn.run(app, host='0.0.0.0', port=80)
	uvicorn.run(app, host='0.0.0.0', port=80)

# http://files.jukuu.com:8001/static/dic-VERB-dobj-NOUN/ban.json
#ubuntu@essaydm:/data/files$ nohup uvicorn ftp:app --host 0.0.0.0 --port 8001 --reload & 