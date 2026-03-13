# Script para pasar los datos recopilados desde Kobo para cargar en UMAP


## KOBO → UMAP  |  Convertidor de datos
Para colectivas que mapean con KoboToolbox + UMap

USO:
    python kobo_a_umap.py mi_archivo.csv

RESULTADO:
    Un archivo  ```mi_archivo_umap.geojson``` listo para importar en UMap.

INSTRUCCIONES UMAP:
* En tu mapa de UMap, click en "_Importar datos_"
* Sube el archivo ```.geojson``` generado
* En "Plantilla de contenido emergente" escribe solo:  ```{popup}```

SOBRE LAS IMÁGENES:
El CSV de Kobo debe tener una columna llamada exactamente:
foto (o cualquier nombre que configures en ```COLUMNA_FOTO``` abajo) con la URL pública de la imagen o el nombre del archivo.

Si la URL base de tus fotos es siempre la misma, configura
```BASE_URL_FOTOS``` abajo para que se complete automáticamente.
"""

import csv
import json
import sys
import os

# CONFIGURACIÓN
## Ajusta estos valores

**Columna con el nombre del lugar (tal como aparece en el CSV de Kobo)**
COLUMNA_NOMBRE = ```"Nombre del establecimiento "```


**Columna con la foto  ← agrégala en tu formulario Kobo con tipo "image"**
Kobo exporta la columna con el nombre de la pregunta. Ajústalo aquí.
COLUMNA_FOTO = ```"foto_establecimiento"```


**Si las fotos están en un servidor propio, pon la URL base aquí.**
Ejemplo: ```"https://tusitio.org/fotos/"```
Si la columna ya trae la URL completa, déjalo vacío: ""
```BASE_URL_FOTOS = ""```


**Ancho de imagen en el popup de UMap (en píxeles). None = sin restricción.**
```pANCHO_IMAGEN = 300```


**Columnas de latitud y longitud en el CSV de Kobo**
```COLUMNA_LAT = "_Ubicación del establecimiento_latitude"```
```COLUMNA_LON = "_Ubicación del establecimiento_longitude"```


**Columnas que NO quieres que aparezcan en el popup (metadatos internos de Kobo)**
```COLUMNAS_EXCLUIR = 
    "_id", "_uuid", "_submission_time", "_validation_status",
    "_notes", "_status", "_submitted_by", "__version__", "_tags", "_index",
    "_Ubicación del establecimiento_altitude",
    "_Ubicación del establecimiento_precision",
    "Ubicación del establecimiento",
    "Muchas gracias! Acá termina este registro.",
    "Muchas gracias!!",```
