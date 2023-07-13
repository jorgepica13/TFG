# Clasificacion de galaxias mediante Deep Learning

Este proyecto aborda el desafio de la clasificacion de galaxias utilizando tecnicas de Deep Learning, desarrollando un modelo de clasificacion preciso y eficiente que pueda analizar grandes conjuntos de datos astronomicos y asignar de manera automatica las galaxias en 3 categorias diferentes: elipticas, espirales o indeterminadas.

El objetivo principal de este trabajo se centra en aliviar la carga de trabajo que supone etiquetar numerosos tipos de galaxias de la gran cantidad de imagenes que se obtienen regularmente de los radiotelescopios. Actualmente, la participacion humana es necesaria para realizar estas tareas, lo que ralentiza la utilizacion de las imagenes etiquetadas en procesos posteriores.

## Directorios

- **AuxiliaryCodes:** Este directorio contiene los distintos codigos que se han usado para tratar o modificar las imagenes, como crear las mascaras, realizar recortes y eliminar ciertas imagenes. Todo el contenido se puede visualizar en [Auxiliary Codes](./Auxiliary%20Codes/).

- **Classification:** Este directorio contiene los codigos necesarios para llevar a cabo el entrenamiento del modelo de clasificacion, asi como el codigo necesario para evaluar la precision del modelo en test. Todo el contenido se puede visualizar en [Classification](./Classification/).

- **Datasets:** Este directorio contiene los distintos conjuntos de imagenes (imagenes originales, imagenes recortadas e imagenes restauradas) con los que se han realizado tanto los entrenamientos como la validacion y el test, ademas de los archivos CSV y JSON con informacion de las galaxias. Todo el contenido se puede visualizar en [Datasets](./Datasets/).
  - **Masks:** Este directorio contiene los distintos conjuntos de imagenes con sus respectivas mascaras (binarias y multiclase) con los que se han realizado tanto los entrenamientos como la validacion y el test. Todo el contenido se puede visualizar en [Masks](./Datasets/Masks/).

- **DesktopApp:** Este directorio contiene el codigo principal [Main File](./Desktop%20App/mainFile.py) que se encarga de la correcta ejecucion de la aplicacion y todos aquellos codigos que necesita el archivo principal para realizar el proceso completo de clasificacion. Todo el contenido se puede visualizar en [Desktop App](./Desktop%20App/).

- **GAN:** Este directorio contiene el codigo de [Real-ESRGAN](./GAN/Real_ESRGAN.ipynb) para la generacion de imagenes.

- **LIME:** Este directorio contiene el codigo de [LIME](./LIME/LIME_explainer.ipynb) para la explicabilidad de los modelos creados.

- **Segmentation:** Este directorio contiene los codigos necesarios para llevar a cabo el entrenamiento del modelo de segmentacion, asi como el codigo necesario para evaluar la precision del modelo en test. Todo el contenido se puede visualizar en [Segmentation](./Segmentation/).

## Archivos

- **Memoria:** Este archivo contiene la memoria del proyecto. La memoria es un documento detallado en el que se recoge todo el desarrollo y resultados del proyecto. Todo el contenido se puede visualizar en [Memoria](./Memoria.pdf).