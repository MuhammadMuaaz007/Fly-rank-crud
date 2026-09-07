import urllib.request
import urllib.error
import json

BASE = "http://127.0.0.1:8000"

def get(path):
    try:
        with urllib.request.urlopen(BASE + path) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

def post(path, data):
    body = json.dumps(data).encode()
    req = urllib.request.Request(BASE + path, data=body,
          headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

def put(path, data):
    body = json.dumps(data).encode()
    req = urllib.request.Request(BASE + path, data=body,
          headers={"Content-Type": "application/json"}, method="PUT")
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

def delete(path):
    req = urllib.request.Request(BASE + path, method="DELETE")
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, None
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

print("--- Stage 4 checks ---")

# Create a task to work with
s, b = post("/tasks", {"title": "Buy milk"})
print(f"POST /tasks          -> {s}  {b}")
new_id = b["id"]

# Update title
s, b = put(f"/tasks/{new_id}", {"title": "Buy oat milk"})
print(f"PUT  title           -> {s}  {b}")

# Mark done
s, b = put(f"/tasks/{new_id}", {"done": True})
print(f"PUT  done=true       -> {s}  {b}")

# PUT empty body -> 400
s, b = put(f"/tasks/{new_id}", {})
print(f"PUT  empty body      -> {s}  {b}")

# PUT unknown id -> 404
s, b = put("/tasks/99", {"done": True})
print(f"PUT  unknown id      -> {s}  {b}")

# DELETE
s, b = delete(f"/tasks/{new_id}")
print(f"DELETE task          -> {s}")

# DELETE unknown -> 404
s, b = delete("/tasks/99")
print(f"DELETE unknown id    -> {s}  {b}")

# Final list
s, b = get("/tasks")
print(f"GET /tasks (final)   -> {s}  count={len(b)}")
