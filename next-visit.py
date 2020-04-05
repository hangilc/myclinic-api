import datetime
import re
from typing import Optional

re_input = re.compile(r"\s*((\d{4}-)?(\d{2}-\d{2}))?\s*\+(\d+)(\w+)?")


def get_base_date(whole_part, year_part, month_day_part) -> datetime.date:
    if not whole_part:
        return datetime.date.today()
    else:
        if not year_part:
            today = datetime.date.today()
            year_part = str(today.year) + "-"
        s = f"{year_part}{month_day_part}"
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()


def get_date_diff(amount_part, unit_part) -> Optional[datetime.timedelta]:
    amount = int(amount_part)
    if not unit_part:
        unit_part = "d"
    if unit_part in ["d", "day", "days"]:
        return datetime.timedelta(days=amount)
    elif unit_part in ["w", "week", "weeks"]:
        return datetime.timedelta(weeks=amount)
    else:
        return None


if __name__ == "__main__":
    print("end with .")
    while True:
        line = input("> ")
        if line == ".":
            break
        m = re_input.match(line)
        if m:
            base_date = get_base_date(m.group(1), m.group(2), m.group(3))
            diff = get_date_diff(m.group(4), m.group(5))
            d = base_date + diff
            if d:
                print(d)
            else:
                print("Invalid input")
        else:
            print("Invalid input.", "(base-date) +[days][unit]")
