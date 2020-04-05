import json
from jinja2 import Environment, FileSystemLoader
import re
import tmpl_helper
import sys
import io


class ParamCompiler(tmpl_helper.Compiler):
    def __init__(self, models):
        super().__init__(models)

    def compile_primitive(self, prim_name, src, attr=None):
        if prim_name == "int":
            return f"int({src})"
        elif prim_name == "float" or prim_name == "double":
            return f"float({src})"
        elif prim_name == "string":
            return src
        else:
            raise Exception("Cannot handle type ({prim_name})")

    def compile_model(self, model, src_expr, attr=None):
        raise Exception(f"Cannot handle parameter ({model['name']})")


class BodyCompiler(tmpl_helper.Compiler):
    def __init__(self, models):
        super().__init__(models)

    def compile_primitive(self, prim_name, src, attr=None):
        if prim_name == "int":
            return f"confirm_int({src})"
        elif prim_name == "float" or prim_name == "double":
            return f"confirm_float({src})"
        elif prim_name == "string":
            return f"confirm_str({src})"
        else:
            raise Exception("Cannot handle type ({prim_name})")

    def compile_model(self, model, src_expr, attr=None):
        return f"model.{model['name']}.from_dict({src_expr})"


def camel_to_snake(name):
    return re.sub(r'(?<!^)(?=[A-Z0-9])', '_', name).lower()


def camel_to_hyphen(name):
    return re.sub(r'(?<!^)(?=[A-Z0-9])', '-', name).lower()


def to_param_name(para):
    return camel_to_snake(para).replace("-", "_")


def para_to_arg(para, param_compiler, body_compiler):
    par_name = para["name"]
    var_name = camel_to_snake(para["name"]).replace("-", "_")
    if "isBody" in para:
        expr = body_compiler.compile(para, "request.get_json(force=True)")
    else:
        if para["type"] == "array":
            src = f"request.args.getlist('{par_name}')"
        else:
            src = f"request.args.get('{par_name}')"
        expr = param_compiler.compile(para, src)
    return f"{var_name} = {expr}"


def get_args(message, param_compiler, body_compiler):
    return [para_to_arg(p, param_compiler, body_compiler) for p in message["request"]]


prolog = """
from server_app import (
    app, request, Session, jsonify, impl, ImplementationError, model,
    confirm_str, send_file, MyclinicContext, 
    enter_myclinic_logs, emit_myclinic_logs
)


"""

epilog = """
def init_routes():
    pass
"""


def run():
    with open("./java/service.json", "r") as f:
        spec = json.load(f)
    with open("./java/dto.json", "r") as f:
        models = json.load(f)
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    param_compiler = ParamCompiler(models)
    body_compiler = BodyCompiler(models)
    env = Environment(loader=FileSystemLoader("./templates", encoding="utf-8"))
    # tmpl_head = env.get_template("server-header.py.jinja2")
    # print(tmpl_head.render())
    print(prolog)
    tmpl = env.get_template("server-route.py.jinja2")
    for name in spec["messages"]:
        message = spec["messages"][name]
        no_database = message.get("noDatabase", False)
        binding = {
            "url": message["url"],
            "name": camel_to_hyphen(name),
            "method": message["httpMethod"].upper(),
            "fun_name": camel_to_snake(name),
            "args": get_args(message, param_compiler, body_compiler),
            "no_database": no_database,
            "is_streaming": message.get("isStreaming", False),
            "param_names": ([] if no_database else ["session"]) +
                           [camel_to_snake(p["name"]).replace("-", "_") for p in message["request"]]
        }
        print(tmpl.render(**binding))
    print(epilog)
    # tmpl_foot = env.get_template("server-footer.py.jinja2")
    # print(tmpl_foot.render())


if __name__ == "__main__":
    run()
