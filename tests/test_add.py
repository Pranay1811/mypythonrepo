from app.add import app
import json

def test_add_get():
    client = app.test_client()
    res = client.get("/add?a=2&b=3")
    assert res.status_code == 200
    assert res.is_json
    assert res.get_json()["result"] == 5.0

def test_add_json():
    client = app.test_client()
    res = client.post("/add", json={"a": 1.5, "b": 2.25})
    assert res.status_code == 200
    assert res.get_json()["result"] == 3.75

def test_add_bad_input():
    client = app.test_client()
    res = client.get("/add")
    assert res.status_code == 400
