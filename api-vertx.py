import argparse
import json
import os

from jinja2 import Environment, FileSystemLoader, Template


def to_java_type(rep, is_obj_type=False, type_hints=None):
    if isinstance(rep, dict):
        t = rep["type"]
        hints = rep.get("typeHints", None)
        if t == "array":
            item_type = to_java_type(rep["items"], True, hints)
            result = f"List<{item_type}>"
            return result
        elif t == "map":
            key_type = to_java_type(rep["keys"], True)
            value_type = to_java_type(rep["values"], True, hints)
            return f"Map<{key_type}, {value_type}>"
        else:
            return to_java_type(t, is_obj_type, hints)
    elif isinstance(rep, list):
        ts = set(rep)
        if len(ts) == 2 and "null" in ts:
            ts.remove("null")
            return to_java_type(ts.pop(), True, type_hints)
    elif rep == "int":
        return "int" if not is_obj_type else "Integer"
    elif rep == "string":
        if type_hints and  "date" in type_hints:
            return "LocalDate"
        else:
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


def cvt_date(name):
    return f'LocalDate.parse({name})'


def cvt_list_int(name):
    return f'{ name }.stream().map(Integer::valueOf).collect(toList())'


def cvt_list_double(name):
    return f'{ name }.stream().map(Double::valueOf).collect(toList())'


def cvt_list_str(name):
    return f'{ name }'


def cvt_class(name):
    return f'_convertParam({name}, new TypeReference<>(){{}})'


param_converter_map = {
    "int": cvt_int,
    "Integer": cvt_int,
    "double": cvt_float,
    "float": cvt_float,
    "String": cvt_str,
    "boolean": cvt_bool,
    "LocalDate": cvt_date,
}

param_list_converter_map = {
    "List<Integer>": cvt_list_int,
    "List<Double>": cvt_list_double,
    "List<String>": cvt_list_str,
}


class Param:
    def __init__(self, spec: dict):
        self.is_nullable = isinstance(spec["type"], list) and "null" in spec["type"]
        self.default_value = spec.get("defaultValue", None)
        self.hyphen_name = spec["name"]
        self.java_name = hyphen_to_camel(self.hyphen_name)
        self.java_type = to_java_type(spec, is_obj_type=self.is_nullable)
        self.conv = self.make_cvt()

    def make_cvt(self):
        if self.is_nullable:
            conv = self.make_regular_converter()
            check = f'params.contains("{self.hyphen_name}")'
            default_value = self.default_value
            if self.java_type == "String" and default_value is not None:
                default_value = f'"{default_value}"'
            elif default_value is None:
                default_value = "null"
            return f'{check} ? {conv} : {default_value}'
        else:
            return self.make_regular_converter()

    def make_regular_converter(self):
        single_cvt = param_converter_map.get(self.java_type)
        if single_cvt:
            return single_cvt(f'params.get("{self.hyphen_name}")')
        else:
            list_cvt = param_list_converter_map.get(self.java_type)
            if list_cvt:
                return list_cvt(f'params.getAll("{self.hyphen_name}")')
            else:
                return cvt_class(f'params.get("{self.hyphen_name}")')


class Body:
    def __init__(self, spec: dict):
        self.hyphen_name = spec["name"]
        self.java_name = hyphen_to_camel(self.hyphen_name)
        self.java_type = to_java_type(spec, True)
        self.conv = f'_convertParam(ctx.getBodyAsString(), new TypeReference<>(){{}})'


def is_body(spec) -> bool:
    return "isBody" in spec and spec["isBody"]


def run_database(messages, jinja_env):
    tmpl = jinja_env.get_template("vertx-method.java.jinja2")
    names = []
    for name in messages:
        service = messages[name]
        names.append((service["url"], name))
        resp_type = to_java_type(service["response"])
        returns_void = service.get("backendMethodReturnsVoid", False)
        params = [Param(p) for p in service["request"] if not is_body(p)]
        bodies = [Body(p) for p in service["request"] if is_body(p)]
        data = {
            "name": name,
            "backend_method_name": service.get("backendMethodName", name),
            "params": params,
            "body": bodies[0] if bodies else None,
            "arg_list": ", ".join(hyphen_to_camel(p["name"]) for p in service["request"]),
            "resp_type": resp_type,
            "returns_void": returns_void,
        }
        print(tmpl.render(**data))
    list_tmpl_str = """
    {
        {% for n in names -%}
        funcMap.put("{{ n[0] }}", this::{{ n[1] }});
        {% endfor -%}
    }
        """
    list_tmpl = Template(list_tmpl_str)
    print(list_tmpl.render(names=names))


def run_no_database(messages, jinja_env):
    tmpl = jinja_env.get_template("vertx-no-database.java.jinja2")
    names = []
    for name in messages:
        service = messages[name]
        names.append((service["url"], name))
        resp_type = to_java_type(service["response"])
        returns_void = service.get("backendMethodReturnsVoid", False)
        params = [Param(p) for p in service["request"] if not is_body(p)]
        bodies = [Body(p) for p in service["request"] if is_body(p)]
        data = {
            "name": name,
            "backend_method_name": service.get("backendMethodName", name),
            "params": params,
            "body": bodies[0] if bodies else None,
            "arg_list": ", ".join(hyphen_to_camel(p["name"]) for p in service["request"]),
            "resp_type": resp_type,
            "returns_void": returns_void,
        }
        print(tmpl.render(**data))
    list_tmpl_str = """
    {
        {% for n in names -%}
        noDatabaseFuncMap.put("{{ n[0] }}", this::{{ n[1] }});
        {% endfor -%}
    }
        """
    list_tmpl = Template(list_tmpl_str)
    print(list_tmpl.render(names=names))


def run(no_database=False, only=None):
    service_spec_file = os.getenv("SERVICE_SPEC_FILE")
    with open(service_spec_file, "r") as f:
        services = json.load(f)
    env = Environment(loader=FileSystemLoader("./templates", encoding="utf-8"))
    env.trim_blocks = True
    env.lstrip_blocks = True
    messages = services["messages"]
    if only:
        if no_database:
            run_no_database({k: messages[k] for k in messages
                             if messages[k].get("noDatabase", False) and (k == only or messages[k].get("url") == only)},
                            env)
        else:
            run_database({k: messages[k] for k in messages
                          if not messages[k].get("noDatabase", False) and (k == only or messages[k].get("url") == only)},
                         env)
    else:
        if no_database:
            run_no_database({k: messages[k] for k in messages if messages[k].get("noDatabase", False)}, env)
        else:
            run_database({k: messages[k] for k in messages if not messages[k].get("noDatabase", False)}, env)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--no-database", action="store_true")
    argparser.add_argument("--only", help="handle single function")
    cmd_args = argparser.parse_args()
    run(**vars(cmd_args))
