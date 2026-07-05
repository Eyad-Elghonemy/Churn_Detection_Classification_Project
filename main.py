from fastapi import FastAPI


app = FastAPI()

@app.get('/')  
def home():
    return {
            "Message": f"Welcome To My App API v1.0"
    }
    
    