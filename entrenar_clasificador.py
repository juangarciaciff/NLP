#!/usr/bin/env python
# -*- coding: utf-8 -*-
#encoding:utf-8

### http://python-apuntes.blogspot.com.es/2016/10/sentiment-analysis.html
### http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/

########################################################################################################################
### Generar y entrenar un clasificador de noticias deportivas
########################################################################################################################
### Este script genera y entrena un clasificador de noticias deportivas.
### El clasificador utilizado es: NaiveBayesClassifier.
### Para entrenar el clasificador se utiliza un corpus de noticias clasificadas descargadas previamente de Internet. 
### Una vez entrenado, el clasificador es guardado en un fichero en disco.
########################################################################################################################

import os
import re
import sys
import json
import random
import codecs
import nltk
from nltk.corpus.reader import *
from nltk.probability import ConditionalProbDist, ELEProbDist
from nltk import FreqDist
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import pylib as pl

########################################################################################################################
### Funciones de extracción de palabras, características, entrenamiento...
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

def train(labeled_featuresets, estimator=ELEProbDist):
    # Crea una distribución P(label)
    label_probdist = estimator(label_freqdist)
    # Crea una distribución P(fval|label, fname)
    feature_probdist = {}
    return NaiveBayesClassifier(label_probdist, feature_probdist)

########################################################################################################################
### Inicio de proceso
########################################################################################################################
if __name__ == '__main__':

    sys.stdout.write("\n==============================================================================================\n")
    sys.stdout.write("== Crea y entrena un clasificador de noticias deportivas.\n")
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

    ### Obtiene el juego de datos de entrenamiento para poder entrenar el clasificador
    sys.stdout.write("\nINFO: Obteniendo el juego de datos de entrenamiento\n")
    training_set = nltk.classify.apply_features(extract_features, documents)

    ### Entrena el clasificador con el juego de datos de entrenamiento obtenido
    sys.stdout.write("\nINFO: Entrenando el clasificador\n")
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    
    ### Guarda el clasificador en un fichero
    sys.stdout.write("\nINFO: Guardando clasificador en un fichero\n")
    import pickle
    f = open('my_classifier.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()

