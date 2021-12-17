import requests
from bs4 import BeautifulSoup
from json import loads

from flask import Flask, request, jsonify


app = Flask(__name__)
list_of_words = []
url = 'http://www.yomaker.ru/yoslovar.htm'

page = requests.get(url).content.decode('cp1251')
soup = BeautifulSoup(page, "html.parser")
words = soup.findAll('p')

with open('text.txt', 'w', encoding='utf-8') as file:
    flag = False
    for word in words:
        word_edited = str(word).strip('<p>').strip('</p>').split()
        if word_edited:
            word_edited = word_edited[0]
            word_edited = word_edited.split('(')[0]
            word_edited = word_edited.strip('<p>').strip('</p>')
            word_edited = word_edited.strip(',')
        if word_edited == 'авиасъёмка':
            flag = True
        if len(word_edited) != 1 and word_edited and flag:
            list_of_words.append(word_edited)
            file.write(word_edited)
            file.write('\n')


@app.route('/is_valid_yo')
def index():
    if request.args:
        word = request.args.get('word')
        data = {}
        print(list_of_words, word)
        if word in list_of_words:
            data['is_word_in_dict'] = 'true'
        else:
            data['is_word_in_dict'] = 'false'
        return jsonify(data)
    else:
        return 'No args'


@app.route('/get_all')
def get_all_words():
    global list_of_words
    return jsonify(list_of_words)


@app.route('/transform', methods=['POST'])
def transform_word():
    global list_of_words
    if request.data:
        js = loads(request.data)
        if 'word' not in js:
            return jsonify(['Wrong parameter'])
        word = js['word']
        start = 0
        list_of_indexes = []
        s = word[::]
        s1 = s[::]
        if s1 in list_of_words:
            return jsonify({word: s1})
        s1 = s1.replace('е', 'ё')
        if s1 in list_of_words:
            print(s1)
            return jsonify({word: s1})
        while True:
            s = s[start + 1:]
            if 'е' in s:
                start = s.index('е')
                list_of_indexes.append(start)
            else:
                break
        for i in range(len(list_of_indexes)):
            s1 = s1.replace('е', 'ё')
            if s1 in list_of_words:
                return jsonify({word: s1})
        s1 = s[::-1]
        for i in range(len(list_of_indexes)):
            s1 = s1.replace('е', 'ё')
            if s1 in list_of_words:
                return jsonify({word: s1})
        return jsonify({'status': 'Wrong word'})
    else:
        return jsonify('Word needed')


def main():
    global list_of_words

    app.run(port=5000)
    print('----------------------------------------------------')
    print(list_of_words)
    print('----------------------------------------------------')


if __name__ == '__main__':
    main()