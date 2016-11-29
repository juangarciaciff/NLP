#!/usr/bin/env python
# -*- coding: utf-8 -*-
#encoding:utf-8

########################################################################################################################
### Generar un corpus de noticias deportivas
########################################################################################################################
### Este script genera un corpus de noticas de deportes a partir de las descargas del diario El Mundo.
### El texto de cada noticia es previamente tratado de la siguiente forma:
### - Se pasa el texto a mayúsculas
### - Reemplaza los acentos
### - Elimina los signos de puntuación
### - Elimina los tokens numéricos
### - Elimina los espacios repetidos
### - Elimina las stop words
### - Elimina todo token que no contenga al menos una letra
### - Reduce los tokens a su raíz utilizando el algoritmo Snowball
### La información de cada noticia se almacenará en un fichero TXT.
########################################################################################################################

import sys
import os
import re
import json
import codecs
import shutil
import string
import unicodedata
import nltk
from nltk.corpus.reader import *
from nltk.corpus import stopwords
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pylib as pl


# Lista de categorías de documentos que queremos tratar
lista_categorias = [ ['FUTBOL', 'FUTBOL'],
                     ['LIGA DE CAMPEONES', 'FUTBOL'],
                     ['PRIMERA DIVISION', 'FUTBOL'],
                     ['PREMIER LEAGUE', 'FUTBOL'],
                     ['FIFA', 'FUTBOL'],
                     ['UEFA', 'FUTBOL'],
                     ['BUNDESLIGA', 'FUTBOL'],
                     ['TENIS', 'TENIS'],
                     ['GOLF', 'GOLF'],
                     ['CICLISMO', 'CICLISMO'],
                     ['ATLETISMO', 'ATLETISMO'],
                     ['BOXEO', 'BOXEO'],
                     ['MOTOCICLISMO', 'MOTOCICLISMO'],
                     ['MOTOGP', 'MOTOCICLISMO'],
                     ['BALONCESTO', 'BALONCESTO'],
                     ['NBA', 'BALONCESTO'],
                     ['BEISBOL', 'BEISBOL'],
                     ['BALONMANO', 'BALONMANO'],
                     ['NATACION', 'NATACION'],
                     ['FORMULA 1', 'FORMULA1'],
                     ['FORMULA UNO', 'FORMULA1'],
                     ['AJEDREZ', 'AJEDREZ'],
                     ['OLIMPIADA', 'OLIMPIADAS'],
                     ['OLIMPICO', 'OLIMPIADAS'],
                     ['PARALIMPICO', 'OLIMPIADAS'],
                     ['RALLY DAKAR', 'AUTOMOVILISMO']
                   ]


########################################################################################################################
### Carga en un objeto JSON una noticia desde su fichero
########################################################################################################################
def leerFicheroNoticiaJSON(fichero):
    try:
        with codecs.open(fichero, encoding='utf-8') as f:
            obj = json.loads(f.read())
            f.close()
        if obj == None or obj['content'] == None or obj['content'].strip() == '':
            return None
        return obj
    except:
        sys.stderr.write("ERROR!!!: no se pudo leer el JSON del fichero {}.\n".format(fichero))
        return None

########################################################################################################################
### Graba un documento del corpus
########################################################################################################################
def grabarFicheroCorpusTXT(fichero, texto):
    with open(fichero, 'w') as f:
        f.write(texto.encode('utf-8'))
        f.close()

########################################################################################################################
### Carga una lista de ficheros JSON de noticias
########################################################################################################################    
def cargarDocumentos(lista_ficheros, path_pendientes, path_erroneos):
    resultado = []

    # Recore la lista de ficheros
    for fichero in lista_ficheros:

        # Carga el JSON de un fichero
        # Si se produce un error o no tiene la información esperada, se mueve el fichero a la carpeta de errores
        obj = leerFicheroNoticiaJSON(fichero)
        if obj == None:
            shutil.move(fichero, path_erroneos + os.path.basename(fichero))
            continue

        # Obtiene el texto completo de la noticia, lo toqueniza y lo añade a la lista de documentos
        texto = obj['title'] + '\n\n' + obj['summary'] + '\n\n' + obj['content']

        # Determina la categoría o categorías del documento. 
        # Si no se encuentra ninguna de las categorías esperadas en las keywords, mueve el fichero a la carpeta de pendientes de clasificación
        # Si se produce un error, mueve el fichero a la carpeta de errores
        flag = False
        try:

            keywords = pl.quitarAcentos(obj['keywords'])
            for item in lista_categorias:
                if re.search('.*' + item[0] + '.*', keywords, re.I):
                    flag = True
                    categoria = item[1]
                    resultado.append((texto, categoria))
                    print '- Leyendo: %4s %-15s %s' % (str(len(resultado)), categoria, fichero)

            if not flag:
                shutil.move(fichero, path_pendientes + os.path.basename(fichero))

        except:
            shutil.move(fichero, path_erroneos + os.path.basename(fichero))

    return resultado

########################################################################################################################
### Crea un corpus a partir de un conjunto de ficheros JSON con textos y categorizaciones
########################################################################################################################
def generarFicherosCorpus(path_corpus, path_noticias, path_pendientes, path_erroneos):

    # Crea el directorio donde mover las noticias que no contengan etiquetas que las identifiquen con nuestras categorías
    if not os.path.exists(path_pendientes):
        sys.stdout.write("\nINFO: Creando directorio de noticias pendientes de clasificación: {}\n".format(path_pendientes))
        os.makedirs(path_pendientes)

    # Crea el directorio donde mover las noticias que contengan errores
    if not os.path.exists(path_erroneos):
        sys.stdout.write("\nINFO: Creando directorio de documentos de noticias con errores: {}\n".format(path_erroneos))
        os.makedirs(path_erroneos)

    # Crea el drea el directorio donde copiar los ficheros del corpus
    if not os.path.exists(path_corpus):
        sys.stdout.write("\nINFO: Creando directorio de documentos del corpus: {}\n".format(path_corpus))
        os.makedirs(path_corpus)

    # Obtiene la lista de nombres de ficheros JSON que contienen las noticias
    sys.stdout.write("\nINFO: Obteniendo la lista de ficheros de noticias\n")
    lista_ficheros = pl.getListaFicheros(path_noticias, ext = '.json')
    if lista_ficheros == None or len(lista_ficheros) < 1:
        sys.stdout.write("WARNING!!! la lista de ficheros está vacía\n")
        return None

    # Carga los documentos
    sys.stdout.write("\nINFO: Cargando documentos de la lista de ficheros de noticias\n")
    documentos = cargarDocumentos(lista_ficheros, path_pendientes, path_erroneos)
    sys.stdout.write('- Número de documentos pendientes de clasificación: {}\n'.format(len(os.listdir(path_pendientes))))
    sys.stdout.write('- Número de documentos erróneos...................: {}\n'.format(len(os.listdir(path_erroneos))))
    
    # Transforma los documentos y los guarda en el corpus
    sys.stdout.write("\nINFO: Transformando los documentos y guardándolos en el corpus\n")
    cont = 0
    for documento in documentos:
        cont = cont + 1
        texto = pl.limpiarTexto(documento[0])
        categoria = documento[1]
        fichero = categoria + '-' + str(hash(documento))[1:] +'.txt'
        print '- Grabando: %4s\t%s' % (str(cont), fichero)
        grabarFicheroCorpusTXT(path_corpus + fichero, texto)

    # Carga el corpus y muestra un resumen
    sys.stdout.write("\nINFO: Cargando el corpus\n")
    sport_news = CategorizedPlaintextCorpusReader(path_corpus, r'.*\.txt', cat_pattern=r'(\w+)-*')
    categories = sport_news.categories()
    sys.stdout.write('- Directorio del corpus..........: {}\n'.format(path_corpus))
    sys.stdout.write('- Número de documentos del corpus: {}\n'.format(len(os.listdir(path_corpus))))
    sys.stdout.write('- Número de palabras del corpus..: {}\n'.format(len(sport_news.words())))
    sys.stdout.write('\n %-15s%s\n' % (u'Categorías', u'nº docs.'))
    sys.stdout.write('------------------------\n')
    for category in categories:
        sys.stdout.write(' %-15s %6s\n' % (category, str(len(sport_news.fileids(category)))))

########################################################################################################################
### Inicio de proceso
########################################################################################################################
if __name__ == '__main__':

    sys.stdout.write("\n==============================================================================================\n")
    sys.stdout.write("== Genera corpus de noticias deportivas.\n")
    sys.stdout.write("==============================================================================================\n\n")

    # Parámetros de configuración
    path_corpus = './mycorpus/'
    path_noticias = './elmundo/deportes/'
    path_pendientes = './elmundo/deportes/sinclasificar/'
    path_erroneos = './elmundo/deportes/erroneos/'

    # Ejecuta el proceso de generación del corpus
    generarFicherosCorpus(path_corpus, path_noticias, path_pendientes, path_erroneos)


