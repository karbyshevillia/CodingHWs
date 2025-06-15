#!/usr/bin/env python3

import json

def filter_json(file_name, **kwargs) -> dict:
    try:
        with open(file_name, "r") as j:
            entries = json.load(j)
        for key in kwargs:
            entries = [entry for entry in entries if entry[key] == kwargs[key]]
        return entries
    except Exception as e:
        print(f"Exception: {e}")


def filter_books_json(file_name, author=None, title=None, year_from=-10000, year_to=10000):
    kw = {"author": author, "title": title}
    kw = {k: v for k, v in kw.items() if v != None}
    try:
        if year_from > year_to:
            raise Exception("Рік ВІД перевищує за числовим значенням рік ДО")
        elif year_from == year_to:
            kw["year"] = year_from
            return filter_json(file_name, **kw)
        part_filtered = filter_json(file_name, **kw)
        filtered_year = [entry for entry in part_filtered if year_from <= entry["year"] <= year_to]
        return filtered_year
    except Exception as e:
        print(f"Exception: {e}")



# if __name__ == '__main__':
#     d = filter_books_json("../book.json", author="Tiutiunnyk", year_from=1976, year_to=1978)
#     print(json.dumps(d, indent=4))

