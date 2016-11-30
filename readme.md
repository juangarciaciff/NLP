# CLASIFICADOR DE DOCUMENTOS
- Autor: Juan Antonio García Cuevas
- Fecha: noviembre 2016
***

## Descripción:
**Conjunto de scripts que permiten descargar un conjunto de documentos de internet, generar un corpus y crear y entrenar un clasificador de noticas**:

- descargar_noticias.py
- generar_corpus.py
- entrenar_clasificador.py
- clasificar_documentos.py
- pylib.py

## Ejecución:
**Ejecutar los 4 primeros scripts anteriores en orden de aparición**:

1. descargar_noticias.py
2. generar_corpus.py
3. entrenar_clasificador.py
4. clasificar_documentos.py

> NOTA: No se ha subido ningún fichero de datos al repositorio, porque pueden obtenerse ejecutando los propios scripts.

> NOTA: La clasificación incorrecta de algunos documentos puede deberse a que no pertenezca a ninguna de las categorías catalogadas (ajedrez, béisbol...).

Las pruebas se han realizado con un conjunto de documentos de unas 10.000 noticias.

***
# Script: descargar_noticias.py

- Este script descarga noticias deportivas de Internet, extrae su información y la almacena en disco.
    - Url de descargas: _http://www.elmundo.es/deportes.html_
    - Directorio de grabación: _./elmundo/deportes/_
    - Formato de ficheros grabados en disco: _JSON_

- Del docuemnto HTML de cada noticia descargada se extrae, entre otra, la siguiente información:
    - título
    - sumario
    - texto de la noticia
    - keywords
    - ...

- A cada noticia descargada se asigna un categoría, extraída de de las keywords del documento HTML original. Las categorías tratadas son las siguientes:
    - FUTBOL
    - TENIS
    - GOLF
    - CICLISMO
    - ATLETISMO
    - BOXEO
    - MOTOCICLISMO
    - BALONCESTO
    - BALONMANO
    - NATACION
    - FORMULA1
    - OLIMPIADAS

    ![Descarga](images/descarga.png)

***
# Script: generar_corpus.py

- Este script genera un corpus de noticas deportivas a partir de las noticias descargadas y guardadas en disco con el script anterior (_descargar_noticias.py_).

- El texto de cada noticia es tratado de la siguiente forma:
    - Se pasa el texto a mayúsculas
    - Se reemplazan las letras acentuadas
    - Se eliminan los signos de puntuación
    - Se eliminan los tokens numéricos
    - Se eliminan las stop words
    - Se eliminan los tokens que no contengan al menos una letra
    - Se reducen los tokens a su raíz mediante el algoritmo Snowball

- Por cada noticia se genera un fichero TXT en el directorio _./mycorpus_, con la lista de tokens resultantes y la categoría a la que pertenece. El nombre del fichero contiene al inicio el identificador de la categoría a la que pertenece.

- Durante este proceso, las noticias a las que no se ha podido asignar una categoría a través de los keywords, se mueven al directorio _./elmundo/deportes/sinclasificar/_, para poder ser clasificadas posteriormente una vez obtenido el clasificador.

    ![Corpus inicio](images/corpus1.png)
    ![Corpus fin](images/corpus2.png)

***
# Script: entrenar_clasificador.py

- Este script crea y entrena un clasificador de documentos a partir del corpus previamente generado y guardado en disco por el script anterior (_generar_corpus.py_).

- Se ha utilizado un clasificador bayesiano ingenuo (NaiveBayesClassifier), un clasificador de aprendizaje supervisado (deduce una función a partir de datos de entrenamiento, como ejemplos ya clasificados) que, dado un nuevo ejemplo, nos permite cuantificar la probabilidad de ocurrencia de una hipótesis.

- El clasificador entrenado es almacenado en disco en el fichero _my_classifier.pickle_.

    ![Clasificador](images/clasificador.png)

***
# Script: clasificar_documentos.py

- Este script lee documentos de noticias sin clasificar y aplica el clasificador para intentar determinar a qué categoría pertenece.

    ![EjemploClasificacion](images/ejemplo_clasificacion.png)

- Se adjunta el fichero _out_clasificados.txt_ con el resultado de la clasificación de 300 noticias que no han formado parte del entrenamiento del clasificador.


- Algunos ejemplos de clasificación:

```
=== FUTBOL ============================
- keywords: deportes,Champions League,Arsenal
- fichero.: ./elmundo/deportes/sinclasificar/5819ae56268e3ebb2d8b4581.json
- titulo..: Özil detuvo el tiempo en Sofía: una maravilla en seis segundos
- summary.: Puso la rúbrica a la remontada y pase a octavos del Arsenal con un excelso tanto en el minuto 88, dejando por el camino al portero y dos defensas. Álbum: Así fueron las geniales maniobras de Özil
- Probabilidad de MOTOCICLISMO        : 1.512934301e-33
- Probabilidad de FORMULA1            : 3.30635873213e-23
- Probabilidad de TENIS               : 3.44612352438e-20
- Probabilidad de BALONMANO           : 1.33597211062e-72
- Probabilidad de CICLISMO            : 1.33888540947e-23
- Probabilidad de FUTBOL              :        1.0
- Probabilidad de ATLETISMO           : 2.83536746812e-30
- Probabilidad de BOXEO               : 5.10780429096e-90
- Probabilidad de GOLF                : 6.5144863553e-79
- Probabilidad de BALONCESTO          : 2.6229008205e-14
- Probabilidad de NATACION            : 1.24676724121e-47
- Probabilidad de OLIMPIADAS          : 4.51686311052e-17

=== TENIS ============================
- keywords: deportes,US Open
- fichero.: ./elmundo/deportes/sinclasificar/57c075a8e2704e6f228b45ba.json
- titulo..: Nadal debuta ante Istomin en NY y comparte cuadro con Djokovic
- summary.: El español se mediría al número uno en un hipotético duelo de semifinales
- Probabilidad de MOTOCICLISMO        : 6.460904655e-71
- Probabilidad de FORMULA1            : 1.62666582767e-62
- Probabilidad de TENIS               :        1.0
- Probabilidad de BALONMANO           : 1.13552031176e-99
- Probabilidad de CICLISMO            : 2.38338395776e-62
- Probabilidad de FUTBOL              : 4.8948683941e-73
- Probabilidad de ATLETISMO           : 1.84187296052e-66
- Probabilidad de BOXEO               : 1.0334112834e-112
- Probabilidad de GOLF                : 3.27610900651e-96
- Probabilidad de BALONCESTO          : 3.33617264021e-58
- Probabilidad de NATACION            : 3.90977920493e-74
- Probabilidad de OLIMPIADAS          : 2.56011964209e-38

=== BALONCESTO ============================
- keywords: deportes,NBA,Golden State Warriors,Pau Gasol
- fichero.: ./elmundo/deportes/sinclasificar/56922376268e3e491d8b45ff.json
- titulo..: Stephen Curry vuelve a exhibirse
- summary.: El base de los Warriors dejó 38 puntos, 11 asistencias y 8 triples. Los Hawks vencieron a los Bulls de Pau y Mirotic, que hizo un partidazo
- Probabilidad de MOTOCICLISMO        : 2.48285422331e-64
- Probabilidad de FORMULA1            : 8.96545326118e-59
- Probabilidad de TENIS               : 1.53556316143e-54
- Probabilidad de BALONMANO           : 4.54443192644e-88
- Probabilidad de CICLISMO            : 1.85613688373e-56
- Probabilidad de FUTBOL              : 1.13571733815e-47
- Probabilidad de ATLETISMO           : 4.82077040431e-55
- Probabilidad de BOXEO               : 1.96739065204e-103
- Probabilidad de GOLF                : 3.68912097081e-90
- Probabilidad de BALONCESTO          :        1.0
- Probabilidad de NATACION            : 3.44812303234e-66
- Probabilidad de OLIMPIADAS          : 5.84190948559e-27

=== CICLISMO ============================
- keywords: deportes,Rally Dakar
- fichero.: ./elmundo/deportes/sinclasificar/56981417268e3e86078b46d3.json
- titulo..: Peterhansel y Price, cerca de la gloria
- summary.: 'Monsieur Dakar' domina con 51:55 de margen sobre Al Attiyah, mientras el australiano de KTM aventaja en 35:23 a Svitko
- Probabilidad de MOTOCICLISMO        : 4.65690706134e-09
- Probabilidad de FORMULA1            : 0.000128083938338
- Probabilidad de TENIS               : 1.83650709322e-09
- Probabilidad de BALONMANO           : 1.25851122025e-55
- Probabilidad de CICLISMO            : 0.999811772565
- Probabilidad de FUTBOL              : 2.41555631264e-06
- Probabilidad de ATLETISMO           : 1.32611750264e-18
- Probabilidad de BOXEO               : 3.36473490087e-73
- Probabilidad de GOLF                : 4.29356911477e-62
- Probabilidad de BALONCESTO          : 5.77020904643e-05
- Probabilidad de NATACION            : 2.21218232289e-31
- Probabilidad de OLIMPIADAS          : 1.93568892644e-08

=== OLIMPIADAS ============================
- keywords: deportes
- fichero.: ./elmundo/deportes/sinclasificar/577bf19cca4741605e8b45f3.json
- titulo..: El rey Lewis
- summary.: 
- Probabilidad de MOTOCICLISMO        : 6.61321957336e-23
- Probabilidad de FORMULA1            : 3.66746402102e-10
- Probabilidad de TENIS               : 1.03694703201e-08
- Probabilidad de BALONMANO           : 2.37256870593e-66
- Probabilidad de CICLISMO            : 4.25770060176e-14
- Probabilidad de FUTBOL              : 7.67865478931e-07
- Probabilidad de ATLETISMO           : 1.10840737742e-15
- Probabilidad de BOXEO               : 6.09297482425e-81
- Probabilidad de GOLF                : 1.42129617281e-73
- Probabilidad de BALONCESTO          : 6.31779647928e-05
- Probabilidad de NATACION            : 9.24189220746e-36
- Probabilidad de OLIMPIADAS          : 0.999936043433

=== TENIS ============================
- keywords: deportes,política - partidos,Roger Federer,Roma,objetivo,Masters 1000
- fichero.: ./elmundo/deportes/sinclasificar/57334e4322601d5e278b4686.json
- titulo..: Federer, peligro en Roma
- summary.: "No sé si jugaré mañana, depende de cómo esté y lo decidiré paso a paso. Espero que sí", dijo el suizo tras ganar en su debut. Novak Djokovic y Andy Murray pasaron a la segunda ronda tras vencer a Stephane Robert y Mikhail Kukushkin
- Probabilidad de MOTOCICLISMO        : 3.9175736045e-46
- Probabilidad de FORMULA1            : 1.87810800394e-34
- Probabilidad de TENIS               :        1.0
- Probabilidad de BALONMANO           : 6.34617588091e-82
- Probabilidad de CICLISMO            : 6.74023894519e-36
- Probabilidad de FUTBOL              : 1.24717043442e-29
- Probabilidad de ATLETISMO           : 2.47972607161e-40
- Probabilidad de BOXEO               : 3.51467432326e-97
- Probabilidad de GOLF                : 1.01522532317e-85
- Probabilidad de BALONCESTO          : 1.59395932551e-30
- Probabilidad de NATACION            : 2.51863790122e-52
- Probabilidad de OLIMPIADAS          : 2.22525016634e-20

=== FORMULA1 ============================
- keywords: deportes
- fichero.: ./elmundo/deportes/sinclasificar/5794c623ca4741635a8b45c1.json
- titulo..: Hamilton, cuando quiere: vence en Hungría y ya es líder del Mundial
- summary.: Logra su quinta victoria de la temporada tras jugar con Nico Rosberg. Fernando Alonso y Carlos Sainz intercambian sus posiciones en la salida y acaban séptimo y octavo respectivamente.. Alonso: "Estoy contento de ser el primero del resto"
- Probabilidad de MOTOCICLISMO        : 2.7478764779e-39
- Probabilidad de FORMULA1            :        1.0
- Probabilidad de TENIS               : 7.73089928904e-36
- Probabilidad de BALONMANO           : 1.76945322958e-86
- Probabilidad de CICLISMO            : 1.26965602115e-33
- Probabilidad de FUTBOL              : 1.18540835261e-35
- Probabilidad de ATLETISMO           : 5.02138993499e-45
- Probabilidad de BOXEO               : 3.63907934651e-104
- Probabilidad de GOLF                : 9.59591890492e-95
- Probabilidad de BALONCESTO          : 1.61927894634e-34
- Probabilidad de NATACION            : 4.99832262387e-57
- Probabilidad de OLIMPIADAS          : 2.58613252185e-31

=== BALONCESTO ============================
- keywords: deportes,NBA,Pau Gasol,Chicago Bulls,Brooklyn Nets
- fichero.: ./elmundo/deportes/sinclasificar/56ebc766ca4741755a8b467c.json
- titulo..: Los Bulls resisten sin Pau Gasol
- summary.: "Gasol se siente mucho mejor de las molestias que le afectan la rodilla y la inflamación también es menor", afirmó Fred Hoiberg
- Probabilidad de MOTOCICLISMO        : 4.06376377928e-36
- Probabilidad de FORMULA1            : 4.16983376804e-27
- Probabilidad de TENIS               : 4.25366657162e-22
- Probabilidad de BALONMANO           : 2.18464565618e-75
- Probabilidad de CICLISMO            : 3.83294595963e-26
- Probabilidad de FUTBOL              : 1.00080347317e-19
- Probabilidad de ATLETISMO           : 2.05809497506e-33
- Probabilidad de BOXEO               : 2.01176484561e-92
- Probabilidad de GOLF                : 2.08590491876e-80
- Probabilidad de BALONCESTO          :        1.0
- Probabilidad de NATACION            : 2.17228683494e-47
- Probabilidad de OLIMPIADAS          : 9.0931127281e-15

=== OLIMPIADAS ============================
- keywords: deportes,Rusia,Vladimir Putin,Estados Unidos,Alemania,Canadá
- fichero.: ./elmundo/deportes/sinclasificar/578d4c46268e3e1f0d8b4581.json
- titulo..: Así hizo Rusia 'desaparecer' los positivos para dominar los Juegos
- summary.: Putin amenaza con un posible boicot a los Juegos tras sugerir la AMA que Rusia sea vetada por hacer desaparecer 643 positivos por dopaje
- Probabilidad de MOTOCICLISMO        : 5.40188276958e-35
- Probabilidad de FORMULA1            : 7.54679467838e-30
- Probabilidad de TENIS               : 1.58357995576e-21
- Probabilidad de BALONMANO           : 9.08960634401e-74
- Probabilidad de CICLISMO            : 3.51731909467e-21
- Probabilidad de FUTBOL              : 3.8549382197e-24
- Probabilidad de ATLETISMO           : 6.15513309628e-15
- Probabilidad de BOXEO               : 7.13398770869e-83
- Probabilidad de GOLF                : 9.00430501146e-82
- Probabilidad de BALONCESTO          : 4.24611231127e-24
- Probabilidad de NATACION            : 2.71373479581e-34
- Probabilidad de OLIMPIADAS          :        1.0

=== FUTBOL ============================
- keywords: deportes,Gareth Bale,Álvaro Morata,Champions League,Opinión,política - partidos,Karim Benzema,delantero
- fichero.: ./elmundo/deportes/sinclasificar/581b28c522601dff6a8b4599.json
- titulo..: Quilombo táctico en Varsovia
- summary.: 
- Probabilidad de MOTOCICLISMO        : 3.8110507478e-29
- Probabilidad de FORMULA1            : 1.87867436173e-22
- Probabilidad de TENIS               : 1.49873924443e-20
- Probabilidad de BALONMANO           : 2.1115657426e-74
- Probabilidad de CICLISMO            : 3.72426215331e-21
- Probabilidad de FUTBOL              :        1.0
- Probabilidad de ATLETISMO           : 7.88085237735e-32
- Probabilidad de BOXEO               : 4.49945426585e-91
- Probabilidad de GOLF                : 1.38294925748e-79
- Probabilidad de BALONCESTO          : 4.14918915343e-15
- Probabilidad de NATACION            : 6.21823875736e-47
- Probabilidad de OLIMPIADAS          : 2.4263397762e-20

=== BALONCESTO ============================
- keywords: deportes,NBA
- fichero.: ./elmundo/deportes/sinclasificar/561f463c268e3e99508b45b4.json
- titulo..: Anna Cruz, campeona de la NBA femenina
- summary.: La base de los Minnesota Lynx es la segunda española en jugar unas Finales de la WNBA. Logra el cuarto anillo para el baloncesto nacional, tras los tres de Amaya Valdemoro
- Probabilidad de MOTOCICLISMO        : 4.59826742406e-38
- Probabilidad de FORMULA1            : 1.73463574119e-33
- Probabilidad de TENIS               : 2.27628168045e-25
- Probabilidad de BALONMANO           : 3.32220106341e-63
- Probabilidad de CICLISMO            : 9.40797388996e-31
- Probabilidad de FUTBOL              : 1.24571786568e-34
- Probabilidad de ATLETISMO           : 1.18506443163e-28
- Probabilidad de BOXEO               : 1.66709991315e-69
- Probabilidad de GOLF                : 8.14492707729e-60
- Probabilidad de BALONCESTO          :        1.0
- Probabilidad de NATACION            : 5.86415442926e-37
- Probabilidad de OLIMPIADAS          : 4.96303732371e-14

=== CICLISMO ============================
- keywords: deportes,Tour de Francia,Alejandro Valverde,Movistar
- fichero.: ./elmundo/deportes/sinclasificar/5786681e468aeb8c4b8b459f.json
- titulo..: Vendaval de Sagan y nuevo despiste de Nairo Quintana
- summary.: El eslovaco vence en Montpellier y sólo Froome le siguió el ritmo hasta el final.. Clasificación Etapa 11 - Tour de Francia 2016
- Probabilidad de MOTOCICLISMO        : 3.59090321314e-31
- Probabilidad de FORMULA1            : 1.31545282169e-30
- Probabilidad de TENIS               : 5.781208564e-30
- Probabilidad de BALONMANO           : 1.36366932773e-72
- Probabilidad de CICLISMO            :        1.0
- Probabilidad de FUTBOL              : 1.23353459364e-26
- Probabilidad de ATLETISMO           : 1.10362816766e-35
- Probabilidad de BOXEO               : 6.7012074793e-89
- Probabilidad de GOLF                : 9.25879496126e-79
- Probabilidad de BALONCESTO          : 6.56489239473e-28
- Probabilidad de NATACION            : 1.17816925016e-47
- Probabilidad de OLIMPIADAS          : 3.08992995472e-21

=== FORMULA1 ============================
- keywords: deportes,Rally Dakar,Stéphane Peterhansel,Carlos Sainz
- fichero.: ./elmundo/deportes/sinclasificar/569a4316268e3e1c5d8b4577.json
- titulo..: Peterhansel sigue siendo 'Monsieur Dakar'
- summary.: El piloto francés completó la última etapa en un tiempo de 1h 54m 28s. Con éste, el especialista de Peugeot, suma seis títulos en motos y seis en autos
- Probabilidad de MOTOCICLISMO        : 1.98650173325e-12
- Probabilidad de FORMULA1            : 0.994539630657
- Probabilidad de TENIS               : 4.42197166393e-09
- Probabilidad de BALONMANO           : 5.67927322405e-56
- Probabilidad de CICLISMO            : 9.59905201462e-06
- Probabilidad de FUTBOL              : 3.83930729498e-09
- Probabilidad de ATLETISMO           : 6.09009470319e-16
- Probabilidad de BOXEO               : 1.62707772948e-72
- Probabilidad de GOLF                : 1.48172307047e-60
- Probabilidad de BALONCESTO          : 0.00545043334022
- Probabilidad de NATACION            : 9.72407275468e-33
- Probabilidad de OLIMPIADAS          : 3.28687825814e-07

=== FUTBOL ============================
- keywords: deportes,economía, negocios y finanzas - computación e informática - redes,Iker Casillas,Real Madrid,once ideal,portería,FC Oporto
- fichero.: ./elmundo/deportes/sinclasificar/571f18fa22601dfd468b4608.json
- titulo..: Iker Casillas elige su once ideal para el Real Madrid... y no se incluye
- summary.: El portero da la alineación de su equipo de lujo entre los jugadores con los que convivió durante sus años en el club blanco
- Probabilidad de MOTOCICLISMO        : 1.45422283804e-23
- Probabilidad de FORMULA1            : 7.61311099976e-16
- Probabilidad de TENIS               : 2.55210220886e-11
- Probabilidad de BALONMANO           : 5.62801572143e-71
- Probabilidad de CICLISMO            : 1.57955079413e-12
- Probabilidad de FUTBOL              : 0.999999991985
- Probabilidad de ATLETISMO           : 8.62462440972e-27
- Probabilidad de BOXEO               : 3.526475887e-90
- Probabilidad de GOLF                : 1.15192987884e-76
- Probabilidad de BALONCESTO          : 7.94574760363e-09
- Probabilidad de NATACION            : 2.7271132135e-44
- Probabilidad de OLIMPIADAS          : 4.19088737258e-11

=== FUTBOL ============================
- keywords: deportes,Josep Guardiola,Pep Guardiola,Neymar,Ter Stegen,Manchester City,Luis Enrique,entrenador,Champions League
- fichero.: ./elmundo/deportes/sinclasificar/58066ebc46163f087c8b4676.json
- titulo..: La idea de Guardiola contra Messi
- summary.: El técnico, al frente de un City en construcción pero que ha ganado la posesión en todos sus partidos, reta al imprevisible Barça del argentino
- Probabilidad de MOTOCICLISMO        : 7.58842047508e-57
- Probabilidad de FORMULA1            : 1.17405577435e-50
- Probabilidad de TENIS               : 1.48257857421e-53
- Probabilidad de BALONMANO           : 4.06958627424e-86
- Probabilidad de CICLISMO            : 2.59938701473e-46
- Probabilidad de FUTBOL              :        1.0
- Probabilidad de ATLETISMO           : 3.10682828308e-56
- Probabilidad de BOXEO               : 8.48563876692e-101
- Probabilidad de GOLF                : 1.90348122644e-96
- Probabilidad de BALONCESTO          : 1.16598505941e-30
- Probabilidad de NATACION            : 1.14083960552e-62
- Probabilidad de OLIMPIADAS          : 3.90711745291e-43

=== OLIMPIADAS ============================
- keywords: deportes,estilo de vida y tiempo libre - juegos - ajedrez,Magnus Carlsen,campeón
- fichero.: ./elmundo/deportes/sinclasificar/581f8a8822601d3f488b4577.json
- titulo..: "La atención de Mr. Putin tiene un valor incalculable"
- summary.: "A los seis años le dije a mi abuela que algún día sería campeón del mundo". "Carlsen es una máquina de matar. Intenta ganar por todos los medios"
- Probabilidad de MOTOCICLISMO        : 5.79715791516e-15
- Probabilidad de FORMULA1            : 3.52137943004e-10
- Probabilidad de TENIS               : 1.04759626623e-06
- Probabilidad de BALONMANO           : 4.62855658601e-53
- Probabilidad de CICLISMO            : 2.17649258749e-08
- Probabilidad de FUTBOL              : 2.9453098935e-06
- Probabilidad de ATLETISMO           : 1.56763200382e-07
- Probabilidad de BOXEO               : 1.3161377906e-59
- Probabilidad de GOLF                : 2.22880313806e-60
- Probabilidad de BALONCESTO          : 0.000285561403377
- Probabilidad de NATACION            : 7.34414674801e-20
- Probabilidad de OLIMPIADAS          : 0.99971026681

=== FUTBOL ============================
- keywords: deportes,Leo Messi,FC Barcelona,RC Celta de Vigo,Luis Suárez,Neymar
- fichero.: ./elmundo/deportes/sinclasificar/56c0f322e2704e310a8b4590.json
- titulo..: Messi, tan genial como Cruyff
- summary.: El argentino emula el mítico penalti indirecto con el Ajax en 1982. El Barcelona pasa por encima de un valiente Celta en una segunda parte en la que acumuló hasta cinco goles. 'Hat trick' de Suárez en un 6-1 completado por Neymar y Rakitic. VOTE: ¿Cree que el penalti indirecto de Messi es ofensivo para el Celta?
- Probabilidad de MOTOCICLISMO        : 8.57435224031e-46
- Probabilidad de FORMULA1            : 2.37818423407e-37
- Probabilidad de TENIS               : 4.42944828743e-40
- Probabilidad de BALONMANO           : 3.47859243792e-77
- Probabilidad de CICLISMO            : 1.54114688388e-35
- Probabilidad de FUTBOL              :        1.0
- Probabilidad de ATLETISMO           : 2.09214979239e-45
- Probabilidad de BOXEO               : 4.44367559144e-91
- Probabilidad de GOLF                : 3.91490639133e-84
- Probabilidad de BALONCESTO          : 7.98223605496e-29
- Probabilidad de NATACION            : 8.16773618167e-57
- Probabilidad de OLIMPIADAS          : 5.11133474897e-31

=== OLIMPIADAS ============================
- keywords: deportes,Juegos Paralímpicos
- fichero.: ./elmundo/deportes/sinclasificar/57d0c1a5268e3e356d8b45f3.json
- titulo..: El "empoderamiento" paralímpico enciende la llama en Maracaná
- summary.: Récord de atletas... y recortes en los Paralímpicos. Un 'doodle' para dar comienzo a los XV Juegos Paralímpicos. Imágenes: Se inauguran los Juegos Paralímpicos
- Probabilidad de MOTOCICLISMO        : 4.79995194942e-31
- Probabilidad de FORMULA1            : 4.28148624499e-25
- Probabilidad de TENIS               : 1.33622197992e-18
- Probabilidad de BALONMANO           : 1.21065564339e-55
- Probabilidad de CICLISMO            : 2.33385519944e-19
- Probabilidad de FUTBOL              : 9.65299862642e-23
- Probabilidad de ATLETISMO           : 5.08313523536e-16
- Probabilidad de BOXEO               : 7.60796714098e-69
- Probabilidad de GOLF                : 3.59591298336e-67
- Probabilidad de BALONCESTO          : 3.46305492868e-23
- Probabilidad de NATACION            : 7.26565471465e-26
- Probabilidad de OLIMPIADAS          :        1.0

=== FUTBOL ============================
- keywords: deportes
- fichero.: ./elmundo/deportes/sinclasificar/56689c1422601d78068b45cf.json
- titulo..: Once federaciones exigen la dimisión de José Luis Sáez
- summary.: 
- Probabilidad de MOTOCICLISMO        : 4.26749846956e-18
- Probabilidad de FORMULA1            : 1.23141729379e-15
- Probabilidad de TENIS               : 3.02183440169e-10
- Probabilidad de BALONMANO           : 3.60238981107e-63
- Probabilidad de CICLISMO            : 4.25622143758e-05
- Probabilidad de FUTBOL              : 0.789862176492
- Probabilidad de ATLETISMO           : 3.48435501654e-19
- Probabilidad de BOXEO               : 8.8632937324e-78
- Probabilidad de GOLF                : 1.44411327603e-68
- Probabilidad de BALONCESTO          : 0.210090309098
- Probabilidad de NATACION            : 2.31190945592e-36
- Probabilidad de OLIMPIADAS          : 4.95189380914e-06

=== BALONCESTO ============================
- keywords: deportes
- fichero.: ./elmundo/deportes/sinclasificar/55f87f1446163fc1598b45ac.json
- titulo..: El grito de Pau Gasol: 'Venimos a Francia a ganarles aquí'
- summary.: 
- Probabilidad de MOTOCICLISMO        : 5.80545283444e-31
- Probabilidad de FORMULA1            : 1.35145241003e-21
- Probabilidad de TENIS               : 9.70254170042e-18
- Probabilidad de BALONMANO           : 1.91409492749e-70
- Probabilidad de CICLISMO            : 1.80377005794e-20
- Probabilidad de FUTBOL              : 1.10685322471e-07
- Probabilidad de ATLETISMO           : 5.53621583284e-31
- Probabilidad de BOXEO               : 3.25021602271e-92
- Probabilidad de GOLF                : 3.31181499513e-79
- Probabilidad de BALONCESTO          : 0.999996319295
- Probabilidad de NATACION            : 1.29311435837e-44
- Probabilidad de OLIMPIADAS          : 3.57002011976e-06

=== TENIS ============================
- keywords: deportes,Open de Australia
- fichero.: ./elmundo/deportes/sinclasificar/56ab6133268e3e59548b461d.json
- titulo..: Murray sobrevive a Raonic y repite final con Djokovic
- summary.: El escocés se impuso por 4-6, 7-5, 6-7(4), 6-4 y 6-2 en algo más de cuatro horas y tendrá opción de revancha con el número uno. Con la victoria de su hermano Jamie en dobles, es la primera vez en la Era Open que dos hermanos están en dos finales distintas de un grande
- Probabilidad de MOTOCICLISMO        : 8.59582379587e-59
- Probabilidad de FORMULA1            : 3.78165136768e-45
- Probabilidad de TENIS               :        1.0
- Probabilidad de BALONMANO           : 5.75057534374e-90
- Probabilidad de CICLISMO            : 1.54391352302e-52
- Probabilidad de FUTBOL              : 2.42543547755e-51
- Probabilidad de ATLETISMO           : 5.76156667501e-57
- Probabilidad de BOXEO               : 8.43564409291e-101
- Probabilidad de GOLF                : 1.30699130531e-91
- Probabilidad de BALONCESTO          : 1.50341185775e-45
- Probabilidad de NATACION            : 1.01731458598e-66
- Probabilidad de OLIMPIADAS          : 2.67627339922e-31

=== BALONCESTO ============================
- keywords: deportes,interés humano - premios,Blazers,Golden State Warriors,Most Valuable Player,Stephen Curry,final,NBA
- fichero.: ./elmundo/deportes/sinclasificar/573430be468aebec678b4573.json
- titulo..: Curry remata a los Blazers y lleva a los Warriors a la final del Oeste
- summary.: Los Golden State se enfrentarán al ganador del duelo entre los Spurs y Oklahoma City, que tienen ventaja de 3-2. Stephen Curry, un MVP como ninguno
- Probabilidad de MOTOCICLISMO        : 1.51912390275e-51
- Probabilidad de FORMULA1            : 1.07943759904e-49
- Probabilidad de TENIS               : 1.6609111192e-46
- Probabilidad de BALONMANO           : 4.92859893433e-83
- Probabilidad de CICLISMO            : 1.91090248982e-45
- Probabilidad de FUTBOL              : 3.72484118488e-40
- Probabilidad de ATLETISMO           : 9.59207882525e-46
- Probabilidad de BOXEO               : 3.54396987017e-100
- Probabilidad de GOLF                : 1.11023012376e-87
- Probabilidad de BALONCESTO          :        1.0
- Probabilidad de NATACION            : 1.26695114458e-59
- Probabilidad de OLIMPIADAS          : 4.90406388011e-28

=== FUTBOL ============================
- keywords: deportes,política - partidos,Kun Agüero,Crystal Palace,Manchester City,Aston Villa,Arsenal
- fichero.: ./elmundo/deportes/sinclasificar/569a85be46163f9b148b4622.json
- titulo..: La cacería del Kun Agüero
- summary.: Un doblete del delantero argentino al Crystal Palace lideró la goleada que mantiene en la pelea por el título al City (4-0). Recorta al Leicester, líder pese a tropezar con el colista (1-1). John Terry empata en el minuto 97 tras un polémico final
- Probabilidad de MOTOCICLISMO        : 2.33982931011e-42
- Probabilidad de FORMULA1            : 2.64197201649e-34
- Probabilidad de TENIS               : 1.83390892794e-31
- Probabilidad de BALONMANO           : 2.26006327823e-72
- Probabilidad de CICLISMO            : 4.63027700588e-30
- Probabilidad de FUTBOL              :        1.0
- Probabilidad de ATLETISMO           : 1.21238956046e-34
- Probabilidad de BOXEO               : 1.89705535884e-78
- Probabilidad de GOLF                : 6.06679489339e-74
- Probabilidad de BALONCESTO          : 1.31406992202e-27
- Probabilidad de NATACION            : 1.72005661826e-46
- Probabilidad de OLIMPIADAS          : 1.86159360407e-30

=== TENIS ============================
- keywords: deportes,Wimbledon,Serena Williams
- fichero.: ./elmundo/deportes/sinclasificar/577e7d2446163f19548b458b.json
- titulo..: Kerber impide la final entre las Williams
- summary.: La tenista germana vence a Venus y evita que las hermanas Williams se enfrenten en la final.. Serena esperaba rival tras deshacerse, en menos de una hora, de la rusa Elena Vesnina.
- Probabilidad de MOTOCICLISMO        : 5.71778724062e-37
- Probabilidad de FORMULA1            : 2.65631883287e-22
- Probabilidad de TENIS               :        1.0
- Probabilidad de BALONMANO           : 1.60323968397e-80
- Probabilidad de CICLISMO            : 9.97470626009e-31
- Probabilidad de FUTBOL              : 2.08631101439e-30
- Probabilidad de ATLETISMO           : 1.31292391832e-37
- Probabilidad de BOXEO               : 2.51386584978e-96
- Probabilidad de GOLF                : 2.60722987582e-80
- Probabilidad de BALONCESTO          : 1.86193726108e-26
- Probabilidad de NATACION            : 5.5991851102e-52
- Probabilidad de OLIMPIADAS          : 1.97456728051e-17

=== OLIMPIADAS ============================
- keywords: deportes,deporte - eventos deportivos - campeonato mundial,España,Mundial de Barcelona,Juegos de Londres,Juegos de Río,Grecia,Estados Unidos,jugador,Waterpolo
- fichero.: ./elmundo/deportes/sinclasificar/56f6b5ed268e3ecb168b464d.json
- titulo..: España recupera su carácter y se clasifica para los Juegos de Río
- summary.: Vence a Holanda por 10-7 en cuartos de final del Preolímpico ante una afición local que desbordó hasta los topes la piscina
- Probabilidad de MOTOCICLISMO        : 4.45692298612e-29
- Probabilidad de FORMULA1            : 5.77760525229e-20
- Probabilidad de TENIS               : 1.36335455767e-16
- Probabilidad de BALONMANO           : 2.68676398821e-61
- Probabilidad de CICLISMO            : 1.38909556966e-18
- Probabilidad de FUTBOL              : 4.84507861195e-18
- Probabilidad de ATLETISMO           : 2.956059953e-19
- Probabilidad de BOXEO               : 9.36276317273e-84
- Probabilidad de GOLF                : 1.54258214893e-70
- Probabilidad de BALONCESTO          : 9.43100648329e-13
- Probabilidad de NATACION            : 2.47519689646e-33
- Probabilidad de OLIMPIADAS          : 0.999999999999

=== CICLISMO ============================
- keywords: deportes,Vuelta a España
- fichero.: ./elmundo/deportes/sinclasificar/57b764cde2704e997a8b4601.json
- titulo..: Tiempo de revancha en la Vuelta a España
- summary.: Contador, recuperado; Froome, busca un título que se le resiste, y Nairo, que necesita alimentar su autoestima, se retan en una Vuelta montañosa. Froome: "Tengo asuntos pendientes con la Vuelta, fui dos veces segundo"
- Probabilidad de MOTOCICLISMO        : 2.19539989797e-34
- Probabilidad de FORMULA1            : 4.00719043312e-32
- Probabilidad de TENIS               : 1.09403741094e-25
- Probabilidad de BALONMANO           : 6.93622961387e-76
- Probabilidad de CICLISMO            :        1.0
- Probabilidad de FUTBOL              : 3.71632376791e-30
- Probabilidad de ATLETISMO           : 3.57286650101e-33
- Probabilidad de BOXEO               : 7.45244732599e-90
- Probabilidad de GOLF                : 4.93004603123e-78
- Probabilidad de BALONCESTO          : 1.15205514726e-27
- Probabilidad de NATACION            : 2.02038038249e-47
- Probabilidad de OLIMPIADAS          : 1.39680918734e-18

=== FUTBOL ============================
- keywords: deportes,FC Barcelona,Andrés Iniesta
- fichero.: ./elmundo/deportes/sinclasificar/57b1ad31ca4741554c8b45e7.json
- titulo..: Iniesta se pierde el inicio de la temporada por lesión
- summary.: El centrocampista sufre una distensión en la rodilla y será baja dos semanas. Mathieu, tres semanas de baja por una rotura fibrilar. Crónica: Un Barça superior decanta la Supercopa
- Probabilidad de MOTOCICLISMO        : 5.1242728637e-49
- Probabilidad de FORMULA1            : 8.26023467397e-45
- Probabilidad de TENIS               : 4.92810064527e-40
- Probabilidad de BALONMANO           : 9.00432586331e-80
- Probabilidad de CICLISMO            : 8.52268721713e-40
- Probabilidad de FUTBOL              :        1.0
- Probabilidad de ATLETISMO           : 1.59367000503e-47
- Probabilidad de BOXEO               : 3.52277891566e-106
- Probabilidad de GOLF                : 7.79965920575e-97
- Probabilidad de BALONCESTO          : 1.21712329094e-25
- Probabilidad de NATACION            : 2.36002600299e-61
- Probabilidad de OLIMPIADAS          : 1.34978526158e-35

=== CICLISMO ============================
- keywords: deportes,Vuelta a España
- fichero.: ./elmundo/deportes/sinclasificar/57d18cba22601d3e318b4628.json
- titulo..: Nielsen gana antes de la gran batalla
- summary.: El ciclista danés del Orica se impone en un desordenado 'sprint' en la víspera de la contrarreloj de 37 kilómetros con final en Calpe. Narración y clasificaciones de la 18ª etapa de la Vuelta
- Probabilidad de MOTOCICLISMO        : 1.00946179829e-37
- Probabilidad de FORMULA1            : 1.81463087263e-34
- Probabilidad de TENIS               : 1.12776206588e-32
- Probabilidad de BALONMANO           : 1.65355879414e-71
- Probabilidad de CICLISMO            :        1.0
- Probabilidad de FUTBOL              : 3.2934379329e-40
- Probabilidad de ATLETISMO           : 2.4111919149e-38
- Probabilidad de BOXEO               : 2.99252040344e-91
- Probabilidad de GOLF                : 2.660661757e-75
- Probabilidad de BALONCESTO          : 7.62637726538e-36
- Probabilidad de NATACION            : 5.23139447857e-51
- Probabilidad de OLIMPIADAS          : 3.17683590236e-27

=== BALONCESTO ============================
- keywords: deportes,política - partidos,Saski Baskonia,final,Euroliga
- fichero.: ./elmundo/deportes/sinclasificar/57338dca22601d0e5e8b45a8.json
- titulo..: La reconstrucción del Baskonia
- summary.: El Baskonia viaja a Berlín para disputar su primera Final Four en ocho años. Tras perder a cinco partidos contra la Kinder Bolonia en 2001, llegaron cuatro finales a cuatro consecutivas, entre 2005 y 2008
- Probabilidad de MOTOCICLISMO        : 1.60444147424e-52
- Probabilidad de FORMULA1            : 6.99633523418e-48
- Probabilidad de TENIS               : 3.97300321626e-44
- Probabilidad de BALONMANO           : 2.7406049241e-81
- Probabilidad de CICLISMO            : 2.39102303866e-45
- Probabilidad de FUTBOL              : 1.34758605106e-29
- Probabilidad de ATLETISMO           : 2.67825733132e-47
- Probabilidad de BOXEO               : 8.70665796906e-98
- Probabilidad de GOLF                : 2.28572429233e-89
- Probabilidad de BALONCESTO          :        1.0
- Probabilidad de NATACION            : 1.95995517278e-56
- Probabilidad de OLIMPIADAS          : 9.36092100128e-36

```

***
# Script: pylib.py

- Este script contiene algunas funciones de utilidades enpleadas en los scripts anteriores.

***
