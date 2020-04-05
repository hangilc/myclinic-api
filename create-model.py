from jinja2 import Environment, FileSystemLoader
import json
import re
import tmpl_helper


class ValueCompiler(tmpl_helper.Compiler):
    def __init__(self, models):
        super().__init__(models)

    def compile_primitive(self, prim_name, src, attr=None):
        if prim_name == "int":
            return f"confirm_int({src})"
        elif prim_name == "float" or prim_name == "double":
            return f"confirm_float({src})"
        elif prim_name == "string":
            return f"confirm_str({src})"

    def compile_model(self, model, src_expr, attr=None):
        return f"{model['name']}.from_dict({src_expr})"


class JsonSourceCompiler(tmpl_helper.Compiler):
    def __init__(self, models):
        super().__init__(models)

    def compile_primitive(self, prim_name, src, attr=None):
        if prim_name == "string":
            if attr is not None and "typeHints" in attr:
                type_hints = attr["typeHints"]
                if "date" in type_hints:
                    return f"cvt_to_date_string({src})"
                if "datetime" in type_hints:
                    return f"cvt_to_datetime_string({src})"
        if prim_name == "int":
            return f"cvt_to_int({src})"
        return src

    def compile_model(self, model, src_expr, attr=None):
        return f"{src_expr}.to_dict()"


def jinja_filter_append(values, arg):
    return [value + arg for value in values]


def jinja_filter_prepend(values, arg):
    return [arg + value for value in values]


env = Environment(loader=FileSystemLoader("./templates", encoding="utf-8"))
env.filters["append"] = jinja_filter_append
env.filters["prepend"] = jinja_filter_prepend


def print_head():
    tmpl = env.get_template("model-header.py.jinja2")
    print(tmpl.render())


def camel_to_snake(name):
    return re.sub(r'(?<!^)(?=[A-Z0-9])', '_', name).lower()


def model_type(field):
    type_hints = field.get("typeHints", [])
    if "date" in type_hints:
        return "Date"
    if "datetime" in type_hints:
        return "DateTime"
    typespec = field["type"]
    if typespec == "int":
        return "Integer"
    elif typespec == "string":
        return "String"
    elif typespec == "double" or typespec == "float":
        return "Float"
    else:
        raise Exception("unknown type: " + typespec)


def model_field(field):
    name = camel_to_snake(field["name"])
    col_name = field["mysqlColName"] if "mysqlColName" in field else name
    mtype = model_type(field)
    extra = ""
    if "isPrimaryKey" in field and field["isPrimaryKey"]:
        extra += ", primary_key=True"
    return f'{name} = Column("{col_name}", {mtype}{extra})'


def model_name(field):
    return camel_to_snake(field["name"])


def field_expr(field, compiler):
    fname = field["name"]
    return compiler.compile(field, f"d['{fname}']")


def json_expr(field, compiler):
    mname = model_name(field)
    return compiler.compile(field, f"self.{mname}")


def print_body():
    with open("./java/dto.json", "r") as f:
        spec = json.load(f)
    compiler = ValueCompiler(spec)
    json_src_compiler = JsonSourceCompiler(spec)
    tmpl_model = env.get_template("model-model.py.jinja2")
    tmpl_class = env.get_template("model-class.py.jinja2")
    tmpl_conv = env.get_template("model-conv.py.jinja2")
    for model in spec:
        binding = {
            "class_name": model["name"],
            "names": [model_name(f) for f in model["fields"]],
            "params": [model_name(f)+"=None" for f in model["fields"]]
        }
        if "mysqlTable" in model:
            tmpl = tmpl_model
            binding["tablename"] = model["mysqlTable"]
            binding["fields"] = [model_field(f) for f in model["fields"]]
        else:
            tmpl = tmpl_class
        print(tmpl.render(**binding))
        cbinding = {
            "class_name": model["name"],
            "fields": [{
                "model_name": model_name(f),
                "json_expr": json_expr(f, json_src_compiler),
                "expr": field_expr(f, compiler),
                "json_name": f.get("jsonName", f["name"])
            } for f in model["fields"]]
        }
        print(tmpl_conv.render(**cbinding))


if __name__ == "__main__":
    print_head()
    print_body()
