from os import path
import yaml
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("from collections import namedtuple\n\n")
spec_file = path.join(path.abspath(path.dirname(__file__)), "consts.yml")
with open(spec_file, "r", encoding="utf-8") as f:
    for k, v in yaml.safe_load(f).items():
        print(f"\n# {k}\n")
        if k == "meisai_sections":
            print("""
MeisaiSectionComponent = namedtuple("_MeisaiSectionComponent", "name ident label")

""")
            for m in v:
                print(f"{m['name']} = MeisaiSectionComponent('{m['name']}', '{m['ident']}', '{m['label']}')")
            names = ", ".join([m['name'] for m in v])
            print(f"MeisaiSections = [{names}]")
        else:
            for name, value in v.items():
                print(f"{name} = {repr(value)}")
