#!/usr/bin/env python
# -*- coding: utf-8 -*-
#encoding:utf-8

import re
import os
import sys
import json
import string
import codecs
import nltk
from nltk.corpus import stopwords


########################################################################################################################
### Librería de utilidades
########################################################################################################################


########################################################################################################################
### Ejecuta una lista de expresiones regulares sobre un texto
########################################################################################################################
def exereg(rules, texto):
    resultado = texto
    for rule in rules:
        resultado = rule[0].sub(rule[1], resultado)
    resultado = resultado.strip()
    return resultado

########################################################################################################################
### Elimina los acentos de un texto
########################################################################################################################
re_rules_acentos = [
    [ re.compile(u'[ÁÀÄÂ]', re.I), u'A' ],
    [ re.compile(u'[ÉÈËÊ]', re.I), u'E' ],
    [ re.compile(u'[ÍÌÏÎ]', re.I), u'I' ],
    [ re.compile(u'[ÓÒÖÔ]', re.I), u'O' ],
    [ re.compile(u'[ÚÙÜÛ]', re.I), u'U' ],
    [ re.compile(u'[áàäâ]', re.I), u'a' ],
    [ re.compile(u'[éèëê]', re.I), u'e' ],
    [ re.compile(u'[íìïî]', re.I), u'i' ],
    [ re.compile(u'[óòöô]', re.I), u'o' ],
    [ re.compile(u'[úùüû]', re.I), u'u' ],
]
def quitarAcentos(texto):
    return exereg(re_rules_acentos, texto)

########################################################################################################################
### Obtiene la lista de ficheros de un directorio con una determinada extensión
########################################################################################################################
def getListaFicheros(path, ext = None):
    lista_ficheros = []
    try:
        if path != None:
            if ext == None:
                extlower = None
            else:
                extlower = ext.lower()
            for file in os.listdir(path):
                (nombre, extension) = os.path.splitext(file)
                if extlower == None or extension.lower() == extlower:
                    fichero = os.path.join(path, file)
                    lista_ficheros.append(fichero)
    except Exception as e:
        sys.stderr.write("ERROR!!!: {}\n".format(str(e)))
        lista_ficheros = []
    return lista_ficheros

########################################################################################################################
### Carga una lista de stop-words en español y la normalizamos (mayúsculas y sin acentos)
########################################################################################################################
stop_words = stopwords.words('spanish')
stop_words = [quitarAcentos(word.upper()) for word in stopwords.words('spanish')]

########################################################################################################################
### Crea un stemmer utilizando el algoritmo Snowball
########################################################################################################################
stemmer = nltk.stem.SnowballStemmer("spanish")

########################################################################################################################
### Normaliza, limpia, tokeniza y extrae las raíces de los tokens de un texto
########################################################################################################################    
def limpiarTexto(texto):
    # Reemplaza los acentos
    texto = quitarAcentos(texto)
    # Elimina los signos de puntuación
    texto = re.sub('[%s]' % re.escape(string.punctuation), ' ', texto)
    texto = re.sub('[<>«»¡!¿\?\(\)\[\]\{\}]', ' ', texto)
    # Elimina los tokens numéricos
    texto = re.sub(' [\d]*(,|\.)?[\d]+ ', ' ', texto)
    # Elimina los espacios repetidos
    texto = re.sub('[\s\t\n\r]+', ' ', texto)
    # Obtiene las palabras del texto
    words = nltk.tokenize.word_tokenize(texto, language='spanish')
    # Elimina las stop words
    words = [word for word in words if word not in stop_words]
    # Elimina todo aquel token que no contenga al menos una letra
    words = [word for word in words if re.match('[A-Z]', word)]
    # Reduce los tokens a su raíz utilizando el algoritmo Snowball
    stems = map(lambda word: stemmer.stem(word), words)
    # Regenera el texto concatenado las palabras resultantes
    texto_limpio = ' '.join(stems)
    # Pasa el texto a mayúsculas
    texto_limpio = texto_limpio.upper()
    # Retona el texto resultante tras el proceso de limpieza
    return texto_limpio

########################################################################################################################
### Carga en un objeto JSON una noticia desde su fichero
########################################################################################################################
def getJsonFromFile(fichero):
    try:
        with codecs.open(fichero, encoding='utf-8') as f:
            obj = json.loads(f.read())
            f.close()
        return obj
    except:
        sys.stderr.write("ERROR!!!: no se pudo leer el JSON del fichero {}.\n".format(fichero))
        return None
    
########################################################################################################################
### Obtiene una propiedad de un diccionario
########################################################################################################################
def getProperty(obj, name):
    try:
        return obj[name]
    except:
        sys.stdout.write("WARNING!!!: propiedad {} no encontrada en el objeto.\n".format(name))
        return ''
