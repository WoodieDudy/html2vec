# ML-30
1) git clone https://github.com/WoodieDudy/html2vec.git
2) cd ml-30
3) create and activate venv in any convenient way
4) python3 -m pip install -r requirements.txt
5) python -m spacy download ru_core_news_lg
6) run command:

*python .\html2vec.py D:\vk.html D:\alpha.html*

If you specify one path, then it will return a dictionary, where the keys are tags, and the values are vectors.
If you pass two paths, then their similarity will return to you.
If similarity lower than 50_000 then websites are alike

or look on demo30.mkv




# ML-40
1) run command:
*python .\fake_page.py -f "path to html"*

Or look on demo40.mkv


Дальше по английски не могу)

Каждую html страничку алгоритм разбивает на тэги (ноды).
Для каждого нода он выделяет пять свойств: название тэга,
текст внутри него, атрибуры тэга, цифровая позиция в коде,
полный путь до тэга. Дальше каждое текстовое значение в параментрах
превращает в вектор (для русского текста использует русскую модель, а для английского модель ориентированную на код).
Дальше для каждого тега вычесляется его средний вектор. Это можно считать вектором страницы (словарем векторов). Потом вычисляет расстояние между одинаковыми тегами
в данных на врод html страницах. Это уже можно считать готовой метрикой, но для наглядности превращается в одно число.
Страницы можно считать похожими, если их difference меньше 80_000