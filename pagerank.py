import os
import re
from graph import dict_2_graph, display_dict
import time

DAMPING = 0.85
DIRECTORY = "./corpus"


def crawl(directory):
    """
    Corpus içerisinde yer alan tüm sayfalar için bir sözlük yapısı oluşturur.
    Key = Page
    Values = Outlinked Pages
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            # dosyayı aç.
            contents = f.read()
            # dosya içerisindeki linkleri regex ile bul.
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            # dosya isimlerinden .html kısmını kaldıralım.
            links = [link.split('.')[0] for link in links]
            filename = filename.split(".")[0]
            # aynı sayfaya birden fazla link gitmiş olabilir. kontrol edelim.
            pages[filename] = set(links) - {filename}

    return pages


def iterate_pagerank(corpus, damping_factor):
    # en başta tüm sayfaların PR değerlerini 1 / N olarak ata.
    pagerank = {item: 1 / len(list(corpus)) for item in list(corpus)}
    list_of_pages = list(pagerank)
    number_of_pages = len(list_of_pages)
    # veriler accuracy değeri kadar değişmeyene dek döngü devam edecek.
    accuracy = 0.001

    while True:
        # önceki ve sonraki PR değerleri arasındaki farkı tutalım.
        change_in_pageranks = []
        # her bir sayfanın PR değerini hesapla.
        for page in list_of_pages:
            # önceki değeri sakla.
            previous_pagerank = pagerank[page]

            # formüldeki ilk kısmı hesapla.
            random_probability = 1 / number_of_pages

            # formülün diğer kısmını hesapla. Bir sonraki for içerisinde güncellenecek.
            following_link_probability = 0

            # ilgili sayfa içerisindeki linklenen sayfaları gez.
            for incoming_page in list_of_pages:
                # linklenen sayfa
                links_of_incoming_page = corpus[incoming_page]
                # eğer bu sayfa şu andaki sayfa içerisinde linklenmişse olasılığı artır.
                if page in links_of_incoming_page:
                    following_link_probability += (pagerank[incoming_page] / len(links_of_incoming_page))

            # formülü tamamla.
            pagerank[page] = ((1 - damping_factor) * random_probability) + (damping_factor * following_link_probability)
            # değişimi kaydet.
            change_in_pageranks.append(abs(pagerank[page] - previous_pagerank))

        # eğer accuracy'den daha az değişim olduysa döngüyü bitir.
        if all([i < accuracy for i in change_in_pageranks]):
            return pagerank


def main():
    corpus = crawl(DIRECTORY)
    ranks = iterate_pagerank(corpus, DAMPING)

    display_dict(corpus)

    time.sleep(2)

    dict_2_graph(corpus, ranks)



if __name__ == "__main__":
    main()
