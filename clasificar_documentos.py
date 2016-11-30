#!/usr/bin/env python
# -*- coding: utf-8 -*-
#encoding:utf-8

########################################################################################################################
### Aplicar el clasificador de noticias deportivas a un conjunto de noticias sin clasificar
########################################################################################################################
### Este script determina la categoría de un conjunto de noticias pendientes de clasificar
########################################################################################################################

import os
import re
import sys
import json
import random
import shutil
import string
import codecs
import unicodedata

import nltk
from nltk.corpus.reader import *
from nltk.corpus import stopwords
from nltk.probability import ConditionalProbDist, ELEProbDist
from nltk import FreqDist

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cross_validation import train_test_split as tts

import pylib as pl

########################################################################################################################
### Funciones de extracción de palabras, palabras características, entrenamiento...
########################################################################################################################

def get_words_in_documents(documents):
    all_words = []
    for (words, category) in documents:
        all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features        

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

########################################################################################################################
### Inicio de proceso
########################################################################################################################
if __name__ == '__main__':
    
    sys.stdout.write("\n==============================================================================================\n")
    sys.stdout.write("== Clasifica noticias deportivas.\n")
    sys.stdout.write("==============================================================================================\n\n")

    ### Carga el corpus, que contiene documentos de todas las categorías que se desea determinar
    ### Los documentos se encuentran en ficheos de texto en un directorio determinado.
    ### En el nombre de cada fichero se anota la categoriá a la que pertenece
    sys.stdout.write("\nINFO: Cargando corpus\n")
    path_corpus = './mycorpus/'
    sport_news = CategorizedPlaintextCorpusReader(path_corpus, r'.*\.txt', cat_pattern=r'(\w+)-*')
    documents = [(list(sport_news.words(fileid)), category)
                  for category in sport_news.categories()
                  for fileid in sport_news.fileids(category)]
    np.random.shuffle(documents)
    categories = sport_news.categories()

    sys.stdout.write('- Directorio del corpus..........: {}\n'.format(path_corpus))
    sys.stdout.write('- Número de documentos del corpus: {}\n'.format(len(os.listdir(path_corpus))))
    sys.stdout.write('- Número de palabras del corpus..: {}\n'.format(len(sport_news.words())))
    sys.stdout.write('\n %-15s%s\n' % (u'Categorías', u'nº docs.'))
    sys.stdout.write('------------------------\n')
    for category in categories:
        sys.stdout.write(' %-15s %6s\n' % (category, str(len(sport_news.fileids(category)))))
        
    ### Obtiene la lista de palabras características: lista de palabras distintas de todos los documentos ordenadas por frecuencia de aparición
    sys.stdout.write("\nINFO: Obteniendo la lista de palabras características\n")
    word_features = get_word_features(get_words_in_documents(documents))

    ### Carga el clasificador
    sys.stdout.write("\nINFO: Cargando el clasificador de documentos\n")
    import pickle
    f = open('my_classifier.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()    

    ### Aplica el clasificador a una colección de textos de noticias pendientes de clasificar
    sys.stdout.write("\nINFO: Clasificando noticias pendientes de clasificación\n")
    lista_ficheros_test = pl.getListaFicheros('./elmundo/deportes/sinclasificar/', ext = '.json')
    f = open('out_clasificados.txt', 'w')
    cont_futbol = 0
    for fichero in lista_ficheros_test:

        # Carga el JSON de un fichero
        obj = pl.getJsonFromFile(fichero)
        if obj == None:
            continue

        title = pl.getProperty(obj, 'title')
        summary = pl.getProperty(obj, 'summary')
        content = pl.getProperty(obj, 'content')
        keywords = pl.getProperty(obj, 'keywords')

        texto = pl.limpiarTexto(title + '\n\n' + summary + '\n\n' + content)

        # Obtiene la categoría de la noticia
        categoria = classifier.classify(extract_features(texto.split()))

        # Obtiene la distribución de probabilidades por categoría
        distribucion = classifier.prob_classify(extract_features(texto.split()))
        categorias = list(distribucion.samples())

        print '\n===', categoria, '============================'
        print '- keywords:', keywords.encode('utf-8')
        print '- fichero.:', fichero.encode('utf-8')
        print '- titulo..:', title.encode('utf-8')
        print '- summary.:', summary.encode('utf-8')
        for item in categorias:
            print '- Probabilidad de %-20s: %10s' % (item, distribucion.prob(item))
            
        f.write('\n=== %s ============================\n' % (categoria))
        f.write('- keywords: %s\n' % (keywords.encode('utf-8')))
        f.write('- fichero.: %s\n' % (fichero.encode('utf-8')))
        f.write('- titulo..: %s\n' % (title.encode('utf-8')))
        f.write('- summary.: %s\n' % (summary.encode('utf-8')))
        for item in categorias:
            f.write('- Probabilidad de %-20s: %10s\n' % (item, distribucion.prob(item)))
    
    f.close()    
    

    
    