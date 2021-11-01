# ML-30

## Install
```
git clone https://github.com/WoodieDudy/html2vec.git
cd ml-30
```
Create and activate venv in any convenient way
```
python3 -m pip install -r requirements.txt
```

## Run
```
python3 .\html2vec.py D:\vk.html D:\alpha.html
```

If you specify one path, then it will return a dictionary, where the keys are tags, and the values are vectors.
If you pass two paths, then their similarity will return to you.
If similarity lower than 80_000 then websites are alike



# ML-40
## Run
```
python3 .\fake_page.py -f "path to html"
```

The algorithm divides each html page into tags (nodes).
For each node, it is distinguished by five properties: the name of the tag,
text inside it, tag attributes, numeric position in the code,
full path to the tag. Further, each text value in the parameters
turns into a vector (for Russian text it uses the Russian model, and for English it uses the code oriented model).
Further, for each tag, its average vector is calculated. This can be thought of as a page vector (a dictionary of vectors). Then calculates the distance between the same tags
in data on html pages. This can already be considered a ready-made metric, but for clarity it turns into one number.
Pages can be considered similar if their difference is less than 80_000
