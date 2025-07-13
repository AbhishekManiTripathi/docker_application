# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class TableRequest(BaseModel):
    number: int

@app.post("/generate_table/")
def generate_table(request: TableRequest):
    """
    Generates a multiplication table for the given number.
    """
    if request.number <= 0:
        raise HTTPException(status_code=400, detail="Number must be a positive integer.")

    table_data = []
    for i in range(1, 11):  # Table up to 10
        table_data.append({"multiplier": i, "result": request.number * i})
    return {"number": request.number, "table": table_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)