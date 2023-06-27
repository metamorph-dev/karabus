from fastapi import FastAPI


app = FastAPI(docs_url="/")


@app.get("/hello-world/")
async def say_hello():
    return {"message": "Hello, world!"}
