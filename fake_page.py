import os.path

from html2vec import *
import argparse


if __name__ == "__main__":
    good_pages = ['alpha.html', 'mts.html', 'raif.html', 'sber.html', 'vk.html']

    parser = argparse.ArgumentParser(description='fake site', add_help=False)
    parser.add_argument('-f', "--file", type=str,
                        help='One path to get vec, two to get similarity')
    path = parser.parse_args().file
    model1: Html2Vec = Html2Vec()
    model1.relatives = 5
    with open(path, encoding="utf8") as f:
        html = f.read()

    for page in good_pages:
        full_path = os.path.join('websites', page)
        with open(full_path, encoding="utf8") as f:
            original_page_html = f.read()
        similar = []
        dict_diff = compare_html(html, original_page_html)
        num_diff = np.array(list(dict_diff.values())).mean()
        if num_diff <= 50_000:
            similar.append(page)
        print(f'Difference with {page} is {num_diff}')
    print()
    print('This page in similar with ', *similar)






