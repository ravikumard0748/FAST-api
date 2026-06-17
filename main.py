from fastapi import FastAPI

app = FastAPI()

def greet():
    print("My first fast api code")
greet()