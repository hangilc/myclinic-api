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


def cvt_param(request_param):
    hyphen_name = request_param["name"]
    name = hyphen_to_camel(hyphen_name)
    typ = to_java_type(request_param)
    if "typeHints" in request_param:
        hint = request_param["typeHints"]
        if hint == ["date"]:
            typ = "LocalDate"
        else:
            raise Exception(f"Cannot handle type: {request_param}")
    is_body = "isBody" in request_param and request_param["isBody"]
    annot = f'@QueryParam("{hyphen_name}") ' if not is_body else ""
    return f'{annot}{typ} {name}'


def run_no_database(messages, jinja_env):
    tmpl = jinja_env.get_template("resteasy-no-database-method.java.jinja2")
    for name in messages:
        service = messages[name]
        resp_type = to_java_type(service["response"])
        defaults = [{"name": hyphen_to_camel(p["name"]), "defaultValue": p["defaultValue"]}
                    for p in service["request"] if "defaultValue" in p]
        args = ", ".join([hyphen_to_camel(a["name"]) for a in service["request"]])
        returns_void = service.get("backendMethodReturnsVoid", False)
        backend_method_name = service["backendMethodName"] if service.get("backendMethodName", False) else name
        binding = {
            "name": name,
            "url": service["url"],
            "method": service["httpMethod"].upper(),
            "response_type": resp_type,
            "param_list": ", ".join(cvt_param(p) for p in service["request"]),
        }
        print(tmpl.render(**binding))


default_stmt_template = """if( {{ name }} == null ){
            {{ name }} = {{ defaultValue }};
        }
"""


def run_database(messages, jinja_env):
    tmpl = jinja_env.get_template("resteasy-method.java.jinja2")
    default_tmpl = Template(default_stmt_template)
    for name in messages:
        service = messages[name]
        resp_type = to_java_type(service["response"])
        defaults = [{"name": hyphen_to_camel(p["name"]), "defaultValue": p["defaultValue"]}
                    for p in service["request"] if "defaultValue" in p]
        args = ", ".join([hyphen_to_camel(a["name"]) for a in service["request"]])
        returns_void = service.get("backendMethodReturnsVoid", False)
        backend_method_name = service["backendMethodName"] if service.get("backendMethodName", False) else name
        binding = {
            "name": name,
            "url": service["url"],
            "method": service["httpMethod"].upper(),
            "response_type": resp_type,
            "param_list": ", ".join(cvt_param(p) for p in service["request"]),
            "default_stmts": [default_tmpl.render(p) for p in defaults],
            "args": args,
            "backend_method_name": backend_method_name,
            "returns_void": returns_void
        }
        print(tmpl.render(**binding))


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
