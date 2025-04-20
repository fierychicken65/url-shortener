from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
import string, random
import redis
import os
import socket

app = FastAPI()

# Connect to Redis container
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, db=0, decode_responses=True)

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.post("/shorten")
async def shorten_url(request: Request):
    body = await request.json()
    long_url = body.get("url")
    if not long_url:
        raise HTTPException(status_code=400, detail="URL is required")

    short_code = generate_short_code()
    r.set(short_code, long_url)

    pod_name = socket.gethostname()
    print(f"[{pod_name}] Shortened {long_url} -> {short_code}")

    return {"short_url": f"http://localhost:8000/{short_code}"}

@app.get("/{short_code}")
async def redirect_to_long_url(short_code: str):
    long_url = r.get(short_code)
    if not long_url:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=long_url)
