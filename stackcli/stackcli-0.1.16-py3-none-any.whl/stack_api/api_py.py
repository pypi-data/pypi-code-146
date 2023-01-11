import sys
sys.path.append( '..' )

from fastapi import FastAPI

# API Definition
app = FastAPI()

# End-points
@app.put("/log")
def log(loss: float):
    return {"loss": loss}
