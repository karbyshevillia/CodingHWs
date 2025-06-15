#!/usr/bin/env python3

import cgi
import json
from classes import *
import os
import sys
import codecs

encoding = 'windows-1251' if os.name == 'nt' else 'utf-8'
if os.name == 'nt' and sys.stdout.encoding != 'windows-1251':
    sys.stdout = codecs.getwriter('windows-1251')(sys.stdout.buffer, 'strict')

HTML_PAGE = """
<!DOCTYPE html>
<html>
<html style="background-color:silver">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset={}\n\n">
</head>
<title>Обробка повторюваних символів</title>
<body>
  <p align="center"><h1>Обробка повторюваних символів (JSON)</h1>
  <hr>
  <form method=POST action="http://localhost:8000/cgi-bin/script.py">
     <h4>Введіть рядок для обробки:</h4>
     <hr>
     <p><label for="string"><strong>Поле вводу:</strong></label>
        <input type="text" name="string_val" id="string" 
              required="required" placeholder="Введіть рядок" size='100'>
     </p>
     <hr>
     <p><input type='submit' value="Проаналізувати повторювані символи"></p>
     <hr>
     <p><strong>JSON: </strong>{}</p>
  </form>
</body>

</html>
"""

form = cgi.FieldStorage()
string = form['string_val'].value
D = JSONConsecutiveSymbols(string)
print(HTML_PAGE.format(encoding,
                       json.dumps(D.dict,
                                  ensure_ascii = True,
                                  indent = None)))