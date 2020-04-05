avro_primitive_types = ["null", "boolean", "int", "long", "float", "double", "bytes", "string"]


class Compiler:
    def __init__(self, models):
        self.models = models

    def compile(self, avro_schema, src_expr):
        if isinstance(avro_schema, str) or isinstance(avro_schema, list):
            avro_schema = {"type": avro_schema}
        is_nullable = avro_schema.get("nullable", False)
        if avro_schema.get("isAutoInc", False):
            is_nullable = True
        t = avro_schema["type"]
        if t == "array":
            c = self.compile(avro_schema["items"], "x")
            return f"[{c} for x in {src_expr}]"
        if isinstance(t, list):
            if len(t) == 1:
                t = t[0]
            if len(t) == 2 and "null" in t:
                i = t.index("null")
                t = t[1 - i]
                is_nullable = True
            else:
                raise Exception("Cannot handle type: " + repr(t))
        if isinstance(t, str):
            if t in avro_primitive_types:
                expr = self.compile_primitive(t, src_expr, attr=avro_schema)
            else:
                m = self.find_model(t)
                if m is None:
                    raise Exception("cannot find model: " + t)
                expr = self.compile_model(m, src_expr, attr=avro_schema)
            if is_nullable:
                return f"None if {src_expr} is None else {expr}"
            else:
                return expr
        raise Exception("Cannot compile: " + repr(avro_schema))

    def find_model(self, name):
        for m in self.models:
            if m["name"] == name:
                return m
        return None

    # noinspection PyMethodMayBeStatic
    def compile_primitive(self, prim_name, src_expr, attr=None):
        pass

    # noinspection PyMethodMayBeStatic
    def compile_model(self, model, src_expr, attr=None):
        pass

# class CompilerOrig:
#     def compile(self, avro_type, src):
#         avro_type = self.normalize_avro_type(avro_type)
#         atype = avro_type["type"]
#         hints = avro_type.get("typeHints", [])
#         if atype == "int":
#             return self.compile_int(src, hints)
#         if atype == "string":
#             return self.compile_str(src, hints)
#         if atype == "float" or atype == "double":
#             return self.compile_float(src, hints)
#         if atype == "array":
#             item_type = self.normalize_avro_type(avro_type["items"])
#             f = self.compile(avro_type["items"], "x")
#             return f"[{f} for x in {src}]"
#         return self.compile_obj(atype, src, hints)
#
#     # noinspection PyMethodMayBeStatic
#     def compile_int(self, src, hints):
#         return f"int({src})"
#
#     # noinspection PyMethodMayBeStatic
#     def compile_str(self, src, hints):
#         return f"str({src})"
#
#     # noinspection PyMethodMayBeStatic
#     def compile_float(self, src, hints):
#         return f"float({src})"
#
#     # noinspection PyMethodMayBeStatic
#     def compile_obj(self, cls, src, hints):
#         return f"{cls}({src})"
#
#     @staticmethod
#     def normalize_avro_type(avro_type):
#         if isinstance(avro_type, str):
#             avro_type = {"type": avro_type}
#         while isinstance(avro_type["type"], dict):
#             avro_type = avro_type["type"]
#         if isinstance(avro_type["type"], str):
#             avro_type["type"] = [avro_type["type"]]
#
#         return avro_type
