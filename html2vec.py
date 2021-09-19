import argparse
import sys
import typing

import spacy
import numpy as np
import lxml.etree
import requests
import re
from collections import defaultdict

# python -m spacy download en_core_web_md

english: spacy.lang.en.English = spacy.load("en_core_web_md")
russian: spacy.lang.ru.Russian = spacy.load("ru_core_news_lg")

good_tags = ['textarea', 'input', 'button', 'a', 'div']
good_attrs = ['aria-label', 'placeholder', 'type', 'href']


class Node:
    def __init__(self) -> None:
        self.xpath: str = '/'
        self.element: lxml.etree._Element = lxml.etree._Element()
        self.vector: typing.Optional[np.array] = None
        self.position: int = 0

    def __repr__(self) -> str:
        return "<Node: {}>".format(self.element)

    def get_parent(self) -> typing.Optional[lxml.etree._Element]:
        parent = self.element.getparent()
        if parent.tag in good_tags:
            return parent
        return None

    def get_children(self) -> typing.Generator[lxml.etree._Element, None, None]:
        yield from self.element

    def get_tag(self) -> str:
        return self.element.tag

    def __get_text(self) -> str:
        return ' '.join([
            self.element.text or '',
            self.element.tag or '',
        ]).strip()

    def get_attributes(self) -> dict:
        return self.element.attrib

    def get_shape(self) -> tuple:
        return (5, 300)

    def get_vector(self) -> np.array:
        if self.vector is None:
            tag: str = self.get_tag()
            text: str = self.__get_text()
            x1: np.array = english(tag).vector
            if re.findall(r"[а-яА-Я]", text):
                x2: np.array = russian(text).vector
            else:
                x2: np.array = english(text).vector

            x3: np.array = np.zeros(x1.shape)
            x4: np.array = np.array([self.position, ] * self.get_shape()[1])
            x5: np.array = english(' '.join([
                name.split('[')[0]
                for name in self.xpath.split('/')
            ])).vector
            for key, value in self.get_attributes().items():
                if key not in good_attrs:
                    continue
                if re.findall(r"[а-яА-Я]", value):
                    second = russian(value).vector
                else:
                    second = english(value).vector
                x3 += english(tag).vector * second
            self.vector: np.array = np.array([
                x1,  # Tag type.
                x2,  # Text vector.
                x3,  # Numeric representation of attributes.
                x4,  # Indicator of vertical position.
                x5,  # Numeric representation of xpath.
            ])
            assert self.vector.shape == self.get_shape()
        return self.vector

    def __add__(self, node: 'Node') -> 'Node':
        assert isinstance(node, self.__class__)
        self.vector = self.get_vector() + node.get_vector()
        return self


class Html2Vec:
    def __init__(self) -> None:
        self.relatives: int = 5

    def __repr__(self) -> str:
        return "<Model: {}>".format(self.__class__.__name__)

    def fit(self, text: str) -> dict:
        assert isinstance(text, str)
        assert text
        html: lxml.etree.HTML = lxml.etree.HTML(text)
        root: lxml.etree._ElementTree = html.getroottree()
        total_nodes: int = len(root.xpath(".//*"))
        index: dict = {}
        tags_dict: defaultdict = defaultdict(lambda: [])
        for i, element in enumerate(html.iter()):
            if element.tag not in good_tags:
                continue
            xpath: str = root.getpath(element)
            node: Node = Node()
            node.position = i / total_nodes
            node.element = element
            node.xpath = xpath
            index[xpath] = node
        for level in range(self.relatives):
            for node in index.values():
                if node.get_parent() is not None:
                    xpath: str = root.getpath(node.get_parent())
                    parent: Node = index[xpath]
                    node += parent
                for element in node.get_children():
                    try:
                        xpath: str = root.getpath(element)
                        child: Node = index[xpath]
                        node += child
                    except Exception:
                        pass
        for node in index.values():
            tags_dict[node.get_tag()].append(node.get_vector())
        for key in tags_dict.keys():
            tags_dict[key] = np.array(tags_dict[key]).mean(axis=0)
        return dict(tags_dict)


def get_dist(vec1, vec2):
    assert vec1.shape == vec2.shape
    diff = vec1 - vec2
    return np.sqrt((diff * diff).sum())


def compare_html(html1: str, html2: str):
    model1: Html2Vec = Html2Vec()
    model1.relatives = 5
    data1 = model1.fit(html1)

    model2: Html2Vec = Html2Vec()
    model2.relatives = 5
    data2 = model2.fit(html2)

    diff_dict = {}
    # diff_vector = []
    for tag in set(data1.keys()) & set(data2.keys()):
        lst = []
        for ind in range(5):
            lst.append(get_dist(data1[tag][ind], data2[tag][ind]))
        diff_dict[tag] = np.array(lst).mean()
    # diff_vector = np.array(diff_vector).mean(axis=1)
    return diff_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='html2vec', add_help=False)
    parser.add_argument('paths', metavar='N', type=str, nargs='+',
                        help='One path to get vec, two to get similarity')
    args = parser.parse_args().paths
    if len(args) == 1:
        model1: Html2Vec = Html2Vec()
        model1.relatives = 5
        with open(args[0], encoding="utf8") as f:
            html1 = f.read()
        vec = model1.fit(html1)
        print(vec)

    elif len(args) == 2:
        with open(args[0], encoding="utf8") as f:
            html1 = f.read()

        with open(args[1], encoding="utf8") as f:
            html2 = f.read()
        com = compare_html(html1, html2)
        # print(com)
        print('Similarity: ', np.array(list(com.values())).mean())
        print('If similarity lower than 50_000 then websites are alike')
