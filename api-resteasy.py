import json
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
    elif rep == "float":
        return "double" if not is_obj_type else "Double"
    elif rep == "boolean":
        return "boolean" if not is_obj_type else "Boolean"
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


default_stmt_template = """if( {{ name }} == null ){
            {{ name }} = {{ defaultValue }};
        }
"""


def run():
    with open("java/service.json", "r") as f:
        services = json.load(f)
    env = Environment(loader=FileSystemLoader("./templates", encoding="utf-8"))
    tmpl = env.get_template("resteasy-method.java.jinja2")
    default_tmpl = Template(default_stmt_template)
    for name in services["messages"]:
        service = services["messages"][name]
        resp_type = to_java_type(service["response"])
        defaults = [{"name": hyphen_to_camel(p["name"]), "defaultValue": p["defaultValue"]} for p in service["request"] if "defaultValue" in p]
        args = ", ".join([hyphen_to_camel(a["name"]) for a in service["request"]])
        binding = {
            "name": name,
            "url": service["url"],
            "method": service["httpMethod"].upper(),
            "response_type": resp_type,
            "param_list": ", ".join(cvt_param(p) for p in service["request"]),
            "default_stmts": [default_tmpl.render(p) for p in defaults],
            "args": args
        }
        print(tmpl.render(**binding))


if __name__ == "__main__":
    run()