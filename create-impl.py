import json
from jinja2 import Environment, FileSystemLoader
import re


def camel_to_snake(name):
    return re.sub(r'(?<!^)(?=[A-Z0-9])', '_', name).lower()


def to_param_name(para):
    return camel_to_snake(para).replace("-", "_")


def run():
    with open("./java/service.json", "r") as f:
        spec = json.load(f)
    env = Environment(loader=FileSystemLoader("./templates", encoding="utf-8"))
    tmpl = env.get_template("impl-fun.py.jinja2")
    for name in spec["messages"]:
        message = spec["messages"][name]
        params = ["session"] + [to_param_name(p["name"]) for p in message["request"]]
        binding = {
            "name": camel_to_snake(name),
            "params": params
        }
        print(tmpl.render(**binding))


if __name__ == "__main__":
    run()
