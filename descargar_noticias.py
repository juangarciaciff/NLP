#!/usr/bin/env python
# -*- coding: utf-8 -*-
#encoding:utf-8

########################################################################################################################
### Obtener documentos de noticias deportivas
########################################################################################################################
### Este script descarga noticias de deportes del dirio El Mundo (http://www.elmundo.es/deportes.html).
### Cada noticia se descargará de una url y se extraerá su título, sumario, texto, keywords, fecha, etc.
### Para asignar la categoría a cada noticia se buscará una palabra identificativa entre sus keywords.
### Se identificarán noticias de categorías como FUTBOL, BALONCESTO, TENIS, GOLF, CICLISMO, ATLETISMO, etc
### La información obtenida de cada noticia se almacenará en un fichero JSON.
########################################################################################################################

import requests
import sys
import os
import re
import json
import time
from lxml import html, etree

########################################################################################################################
### Descarga una url
########################################################################################################################
def download(url):
    r = requests.get(url)
    if r.status_code != 200:
        sys.stderr.write("ERROR!!!: {} descargando url {}\n".format(r.status_code, url))
        return None

    return r

########################################################################################################################
### Obtiene la lista de url (no repetidas) de un árbol DOM
########################################################################################################################
def parseNewUrls(tree, done_urls, pattern=None):
    results = tree.xpath('//a/@href')
    if pattern:
        results = filter(lambda u: any([p.match(u) for p in pattern]), results)

    new_urls = set()
    for r in results:
        r = r.rsplit("#", 1)[0]
        r = r.rsplit("?", 1)[0]
        if r not in done_urls:
            new_urls.add(r)
    return new_urls

########################################################################################################################
### Parsea el contenido del árbol DOM en datos de una noticia y los almacena en un fichero con formato JSON
########################################################################################################################
def parseContent(tree, filename=None, meta=None):
    data = {}
    xpath_string = { 'title': "//article/h1[@itemprop='headline']/text()",
                     'summary': "//article/div[@itemprop='articleBody']/p[@class='summary-lead']//text()",
                     'author': "//footer/ul/li[@itemprop='name']//text()",
                     'jobTitle': "//footer/ul/li[@itemprop='jobTitle']//text()",
                     'location': "//footer/ul/li[@itemprop='address']//text()",
                     'datetime': "//article/div[@itemprop='articleBody']/time//text()",
                     'content': "//article/div[@itemprop='articleBody']/p[not(@class='summary-lead')]//text()",
                     'keywords': "//meta[@name='keywords']/@content",
                     'url': "//meta[@property='og:url']/@content"
                    }

    for key, value in xpath_string.iteritems():
        try:
            item = tree.xpath(value)
            if not isinstance(item, basestring):
                if key == 'summary':
                    item = '. '.join(item).strip()
                else:
                    item = ''.join(item).strip()
            data[key] = item.strip()
        except Exception:
            pass
 
    if data['content'] == None or data['content'].strip() == '' or data['keywords'] == None or data['keywords'] == '':        
        return None

    if filename and any(data.values()):
        data.update(meta)
        with open(filename, 'w') as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False).encode('utf8'))
            f.close()
        return data
    else:
        return None

########################################################################################################################
### Proceso recursivo de descarga de noticias
########################################################################################################################
def parseRecursive(init_url, content_pattern=None, visit_pattern=None, output_dir=None):
    urls = set([init_url])
    done = []
    i = 1
    while len(urls):
        url = urls.pop()
        sys.stdout.write("[{}/{}] - {}\n".format(i, len(urls)+len(done), url))
        try:
            page = download(url)
            
            tree = html.fromstring(page.content)
            new_urls = parseNewUrls(tree, done, visit_pattern)
            urls.update(new_urls)
            
            if not content_pattern or any([p.match(url) for p in content_pattern]):

                url_pattern = re.compile('https?:\/\/(www.)?elmundo.es\/deportes\/(?P<year>\d{4})\/(?P<month>\d{2})\/(?P<day>\d{2})\/(?P<uuid>[\d\w]+).html')
                meta = url_pattern.match(url).groupdict()

                filename = os.path.join(output_dir, meta['uuid'] + '.json')

                parseContent(tree, filename, meta)

        except KeyboardInterrupt:
            sys.stdout.write("INFO: Interrumpido por el usuario.\n")
            return
            
        except Exception as e:
            sys.stderr.write("ERROR!!!: {}\n".format(str(e)))
        
        time.sleep(0.100)
        i += 1
        done.append(url)

########################################################################################################################
### Inicio de proceso
########################################################################################################################
if __name__ == '__main__':

    sys.stdout.write("\n==============================================================================================\n")
    sys.stdout.write("== Descarga noticias deportivas de http://www.elmundo.es/deportes.html\n")
    sys.stdout.write("==============================================================================================\n\n")
    
    # Url y patrones de descarga
    url = "http://www.elmundo.es/deportes.html"
    content_pattern = [re.compile('https?:\/\/(www.)?elmundo.es\/deportes\/(?P<year>\d{4})\/(?P<month>\d{2})\/(?P<day>\d{2})\/(?P<uuid>[\d\w]+).html'),]
    visit_pattern = [re.compile('https?:\/\/(www.)?elmundo.es\/deportes.*'),]

    # Fichero de salida
    output_dir = os.path.join(os.path.dirname(__file__), './elmundo/deportes/')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Ejecuta el proceso de descarga
    parseRecursive(url, content_pattern, visit_pattern, output_dir)


