#!/usr/bin/env python3

import os
import sys
import codecs
import cgi
import cgitb
import json
import html
from search_aux import filter_books_json
cgitb.enable()

encoding = 'windows-1251' if os.name == 'nt' else 'utf-8'
if os.name == 'nt' and sys.stdout.encoding != 'windows-1251':
    sys.stdout = codecs.getwriter('windows-1251')(sys.stdout.buffer, 'strict')

HTML_PAGE = """Content-Type: text/html; charset={}\n\n
<html>
<title>Пошук Книжок</title>
<form method=POST action="search.py">
<body>
<h3>Параметри пошуку:</h3>
    <p>
        Назва книжки: <input type=text name=title value=""><br>
        Прізвище автора: <input type=text name=author value=""><br>
        Рік видавництва: від <input type=text name=year_from value=""> до <input type=text name=year_to value=""><br>
        <input type=submit value="Знайти"><br>
        <input type=hidden name=file_name value="{}">
    </p>
<br>
<pre>
{}
</pre>
</body>
</form>
</html>
"""
form = cgi.FieldStorage(encoding=encoding)

file_name = form["file_name"].value
# book_title = form["book_title"].value
# author_name = form["author_name"].value
# year_from, year_to = form["year_from"].value, form["year_to"].value

kw = dict()
for var in ["title", "author", "year_from", "year_to"]:
    if var not in form:
        continue
    var_value = form[var].value
    if "year" in var:
        kw[var] = int(var_value)
    else:
        kw[var] = var_value


response = filter_books_json(file_name, **kw)
print(HTML_PAGE.format(encoding, file_name, html.escape(json.dumps(response, indent=4))))
