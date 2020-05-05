import argparse
import json
import os

from jinja2 import Environment, FileSystemLoader, Template


def to_java_type(rep, is_obj_type=False):
    if isinstance(rep, dict):
        t = rep["type"]
        if t == "array":
            item_type = to_java_type(rep["items"], True)
            result = f"List<{item_type}>"
            return result
        elif t == "map":
            key_type = to_java_type(rep["keys"], True)
            value_type = to_java_type(rep["values"], True)
            return f"Map<{key_type}, {value_type}>"
        else:
            return to_java_type(t)
    elif isinstance(rep, list):
        ts = set(rep)
        if len(ts) == 2 and "null" in ts:
            ts.remove("null")
            return to_java_type(ts.pop(), True)
    elif rep == "int":
        return "int" if not is_obj_type else "Integer"
    elif rep == "string":
        return "String"
    elif rep == "float" or rep == "double":
        return "double" if not is_obj_type else "Double"
    elif rep == "boolean":
        return "boolean" if not is_obj_type else "Boolean"
    elif rep == "ResponseBody":
        return "Response"
    elif isinstance(rep, str):
        return rep + "DTO"
    else:
        raise Exception(str(rep))


def hyphen_to_camel(s):
    parts = s.split("-")
    return "".join([parts[0]] + [p.capitalize() for p in parts[1:]])


def cvt_int(name):
    return f'Integer.parseInt({name})'


def cvt_float(name):
    return f'Double.parseDouble({name})'


def cvt_str(name):
    return name


def cvt_bool(name):
    return f'Boolean.valueOf({name})'


def cvt_class(name):
    return f'_convertParam({name}, new TypeReference<>(){{}})'


param_converter_map = {
    "int": cvt_int,
    "Integer": cvt_int,
    "double": cvt_float,
    "float": cvt_float,
    "String": cvt_str,
    "boolean": cvt_bool
}


class Param:
    def __init__(self, spec: dict):
        self.hyphen_name = spec["name"]
        self.java_name = hyphen_to_camel(self.hyphen_name)
        self.java_type = to_java_type(spec)
        f_cvt = param_converter_map.get(self.java_type, cvt_class)
        self.conv = f_cvt(f'params.get("{self.hyphen_name}")')


def run_database(messages, jinja_env):
    tmpl = jinja_env.get_template("vertx-method.java.jinja2")
    for name in messages:
        service = messages[name]
        resp_type = to_java_type(service["response"])
        returns_void = service.get("backendMethodReturnsVoid", False)
        params = [Param(p) for p in service["request"]]
        data = {
            "name": name,
            "params": params,
            "arg_list": ", ".join(p.java_name for p in params),
            "resp_type": resp_type,
            "returns_void": returns_void,
        }
        print(tmpl.render(**data))


def run_no_database(messages, jinja_env):
    pass


def run(no_database=False):
    service_spec_file = os.getenv("SERVICE_SPEC_FILE")
    with open(service_spec_file, "r") as f:
        services = json.load(f)
    env = Environment(loader=FileSystemLoader("./templates", encoding="utf-8"))
    env.trim_blocks = True
    env.lstrip_blocks = True
    messages = services["messages"]
    if no_database:
        run_no_database({k: messages[k] for k in messages if messages[k].get("noDatabase", False)}, env)
    else:
        run_database({k: messages[k] for k in messages if not messages[k].get("noDatabase", False)}, env)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--no-database", action="store_true")
    cmd_args = argparser.parse_args()
    run(**vars(cmd_args))
