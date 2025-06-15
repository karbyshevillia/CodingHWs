"""
T28.6 Скласти програму, яка працює в оточенні веб-сервера, для розв’язання задачі. Дано
файл у форматі
a) JSON,
b) XML, (дана робота)
який містить відомості про книги. Відомості про кожну книгу - це прізвище автора, назва
та рік видання. Підібрати усі книги за заданою назвою та/або автором та/або періодом
видання. Вводити відомості про книги треба на окремій сторінці. На іншій сторінці
вводити обмеження та показувати відібрані книги.
"""


from flask import Flask, request, Response

import xml.etree.ElementTree as ET
import os

app = Flask(__name__)
BOOKS_FILE = 'book.xml'


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename.endswith('.xml'):
            uploaded_file.save(BOOKS_FILE)
            return '<p>Файл успішно завантажено.</p><a href="/search">Перейти до пошуку</a>'
        else:
            return 'Будь ласка, завантажте XML-файл.'

    return '''
        <!doctype html>
        <html lang="uk">
        <head><meta charset="utf-8"><title>Завантаження XML</title></head>
        <body>
            <h1>Завантажити XML з книгами</h1>
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="file" accept=".xml" required>
                <button type="submit">Завантажити</button>
            </form>
        </body>
        </html>
    '''


@app.route('/search', methods=['GET', 'POST'])
def search():
    if not os.path.exists(BOOKS_FILE):
        return '<p>Файл книг не знайдено. <a href="/upload">Завантажити</a></p>'

    if request.method == 'POST':
        author = request.form.get('author', '').lower()
        title = request.form.get('title', '').lower()
        year_from = request.form.get('year_from')
        year_to = request.form.get('year_to')

        tree = ET.parse(BOOKS_FILE)
        root = tree.getroot()

        result_root = ET.Element('books')

        for book in root.findall('book'):
            b_author = book.find('author').text.lower()
            b_title = book.find('title').text.lower()
            b_year = int(book.find('year').text)

            match = True
            if author and author not in b_author:
                match = False
            if title and title not in b_title:
                match = False
            if year_from and b_year < int(year_from):
                match = False
            if year_to and b_year > int(year_to):
                match = False

            if match:
                result_root.append(book)

        xml_str = ET.tostring(result_root, encoding='utf-8', method='xml')
        return Response(xml_str, mimetype='application/xml')

    return '''
        <!doctype html>
        <html lang="uk">
        <head><meta charset="utf-8"><title>Пошук книг</title></head>
        <body>
            <h1>Пошук книг</h1>
            <form method="POST">
                <label>Автор:</label><br>
                <input type="text" name="author"><br><br>

                <label>Назва:</label><br>
                <input type="text" name="title"><br><br>

                <label>Рік з:</label><br>
                <input type="number" name="year_from"><br><br>

                <label>Рік до:</label><br>
                <input type="number" name="year_to"><br><br>

                <button type="submit">Пошук</button>
            </form>
        </body>
        </html>
    '''


if __name__ == '__main__':
    app.run(debug=True)
