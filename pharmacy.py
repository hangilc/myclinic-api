import os
from typing import List
import re


class Pharmacy:
    def __init__(self, name, fax, addr):
        self.name = name
        self.fax = fax
        self.addr = addr

    def __repr__(self):
        return f"<Pharmacy name={self.name}, fax={self.fax}, addr={self.addr}>"

    def to_dict(self):
        return {
            "name": self.name,
            "fax": self.fax,
            "addr": self.addr
        }


def pharmacy_list_file():
    return os.getenv("MYCLINIC_PHARMACY_LIST")


re_title = re.compile(r'【(.+)】')
re_fax = re.compile(r'fax:\s*(\+\d+)')
re_addr = re.compile(r'〒(\d{3}-\d{4})\s+(.+)')


def read_pharmacy_list(path: str) -> List[Pharmacy]:
    result = []
    name = None
    fax = None
    addr = None

    def flush():
        nonlocal name, fax, addr
        if name and fax and addr:
            result.append(Pharmacy(name, fax, addr))
        name = None
        fax = None
        addr = None

    with open(path, "r", encoding="UTF-8") as fp:
        for line in fp:
            line = line.strip()
            if not line:
                continue
            m = re_title.match(line)
            if m:
                flush()
                name = m.group(1)
                continue
            m = re_fax.match(line)
            if m:
                fax = m.group(1)
                continue
            m = re_addr.match(line)
            if m:
                addr = (m.group(1), m.group(2))
                continue
    flush()
    return result


def get_pharmacy_list():
    return read_pharmacy_list(pharmacy_list_file())


if __name__ == "__main__":
    for pharmacy_entry in get_pharmacy_list():
        print(pharmacy_entry)
