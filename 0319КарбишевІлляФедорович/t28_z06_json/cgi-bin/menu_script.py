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

def establish_file(file_name):
    HTML_PAGE = """Content-Type: text/html; charset={}\n\n
    <html>
    <title>Книжки</title>
    <body>
    <h3>Книжки</h3>
    <pre>
    {}
    </pre>
    </body>
    </html>
    """

    if not file_name:
        response = "Не визначено ім'я файлу"
    else:
        with open(file_name, encoding=encoding) as f:
            response = json.dumps(json.load(f), indent=2)
    print(HTML_PAGE.format(encoding, html.escape(response)))

def search_books(file_name: str):
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
    # response = ""
    # form = cgi.FieldStorage(encoding=encoding)
    # book_title = form["book_title"].value
    # author_name = form["author_name"].value
    # year_from, year_to = form["year_from"].value, form["year_to"].value
    # response = filter_books_json(file_name,
    #                              author = author_name,
    #                              title = book_title,
    #                              year_from = int(year_from),
    #                              year_to = int(year_to))
    response = filter_books_json(file_name)
    print(HTML_PAGE.format(encoding, file_name, html.escape(json.dumps(response, indent=4))))


result = "Нічого не вибрано"
form = cgi.FieldStorage()
if 'menu' in form:
    flag = int(form['menu'].value)
    file_name = form['file_name'].value
    file_name = file_name.strip()
    if flag == 1:
        establish_file(file_name)
    elif flag == 2:
        search_books(file_name)
