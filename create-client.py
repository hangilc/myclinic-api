import json
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader
import re


def camel_to_snake(name):
    return re.sub(r'(?<!^)(?=[A-Z0-9])', '_', name).lower()


def hyphen_to_snake(name):
    return name.replace("-", "_")


def req_to_param(req: Dict) -> str:
    name = camel_to_snake(req["name"])
    return hyphen_to_snake(name)


def compose_req_params(reqs: List[Dict]) -> str:
    parts = [
        f"'{req['name']}': {req_to_param(req)}"
        for req in reqs if not req.get("isBody", False)]
    return ", ".join(parts)


def compose_req_body(reqs: List[Dict]) -> str:
    body = [req for req in reqs if req.get("isBody", False)]
    if body:
        return f"data = {req_to_param(body[0])}"
    else:
        return ""


prolog = """
import requests
url = "http://127.0.0.1:28080/json"
"""


def run():
    with open("./java/service.json", "r") as f:
        spec = json.load(f)
    print(prolog)
    env = Environment(loader=FileSystemLoader("./templates", encoding="utf-8"))
    tmpl = env.get_template("client-function.py.jinja2")
    for name, info in spec["messages"].items():
        reqs = info["request"]
        req_params = compose_req_params(reqs)
        req_body = compose_req_body(reqs)
        kwargs = ""
        if req_params:
            kwargs += ", params=params"
        if req_body:
            kwargs += ", data=data"
        binding = {
            "name": camel_to_snake(name),
            "params": [req_to_param(req) for req in reqs],
            "req_params": req_params,
            "req_body": req_body,
            "method": info["httpMethod"],
            "url": "/" + info["url"],
            "kwargs": kwargs
        }
        print(tmpl.render(**binding))


if __name__ == "__main__":
    run()
