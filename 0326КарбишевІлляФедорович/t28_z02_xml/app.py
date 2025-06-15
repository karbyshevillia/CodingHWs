"""
T28.2 Скласти програму, яка працює в оточенні веб-сервера, для розв’язання задачі.
Знайти у даному рядку символ та довжину найдовшої послідовності однакових символів,
що йдуть підряд. Ввести рядок у браузері. Повернути символ та довжину найдовшої
послідовності символів у форматі:
a) JSON
b) XML (дана робота)
Структуру даних JSON та XML визначити самостійно.
"""

from flask import Flask, request, Response

import xml.etree.ElementTree as ET

app = Flask(__name__)

def find_longest_sequence(s):
    if not s:
        return '', 0

    max_char = s[0]
    max_len = 1
    current_char = s[0]
    current_len = 1

    for i in range(1, len(s)):
        if s[i] == current_char:
            current_len += 1
        else:
            if current_len > max_len:
                max_len = current_len
                max_char = current_char
            current_char = s[i]
            current_len = 1

    if current_len > max_len:
        max_len = current_len
        max_char = current_char

    return max_char, max_len

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text', '')
        char, length = find_longest_sequence(text)

        root = ET.Element("result")
        ET.SubElement(root, "symbol").text = char
        ET.SubElement(root, "length").text = str(length)
        xml_str = ET.tostring(root, encoding='utf-8', method='xml')

        return Response(xml_str, mimetype='application/xml')

    # HTML-форма як текст
    return '''
        <!doctype html>
        <html lang="uk">
        <head>
            <meta charset="utf-8">
            <title>Аналіз рядка</title>
        </head>
        <body>
            <h1>Найдовша послідовність однакових символів</h1>
            <form method="POST">
                <label>Введіть рядок:</label><br>
                <input type="text" name="text" required>
                <button type="submit">Надіслати</button>
            </form>
        </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
