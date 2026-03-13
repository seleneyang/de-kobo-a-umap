# Guia para el taller — Kobo a UMap

Esta guia esta pensada para usarse durante el taller con la colectiva. Podes seguirla paso a paso con las companeras.

---

## Antes del taller — checklist

- [ ] Todas tienen Python 3 instalado (`python3 --version` en la terminal)
- [ ] Todas tienen acceso a su formulario de KoboToolbox
- [ ] El formulario de Kobo tiene los campos obligatorios (ver seccion abajo)
- [ ] Se creo un mapa en UMap para practicar
- [ ] Se descargo este repositorio en las computadoras

---

## Campos que debe tener el formulario de Kobo

Antes de recopilar datos, asegurate de que el formulario tenga estos campos:

### Obligatorios (el script no funciona sin estos)

| Que pregunta | Tipo en Kobo | Nombre interno sugerido |
|---|---|---|
| Nombre del lugar | Text | `nombre_lugar` |
| Ubicacion GPS | Geopoint | `ubicacion_gps` |

Kobo desglosa el GPS automaticamente en 4 columnas al exportar: `_latitude`, `_longitude`, `_altitude` y `_precision`. El script usa solo las dos primeras — no tenes que hacer nada extra.

### Opcional (para mostrar fotos en el popup)

| Que pregunta | Tipo en Kobo | Nombre interno sugerido |
|---|---|---|
| Foto del lugar | Photo | `foto_lugar` |

Cuando el formulario tiene una pregunta de tipo **Photo**, Kobo genera automaticamente una columna extra llamada `foto_lugar_URL` con la URL directa de cada imagen. El script la usa sin necesidad de ningun servidor externo.

### El resto: libertad total

Cualquier otra pregunta que agreguen (texto, seleccion unica, seleccion multiple, numeros) aparecera automaticamente en el popup de UMap. No hay que tocar el script.

---

## Etiqueta vs. nombre interno — diferencia importante

Kobo maneja dos nombres por cada pregunta:

- **Etiqueta** — lo que ve la usuaria al llenar el formulario. Ejemplo: "Como se llama este lugar?"
- **Nombre interno** — lo que aparece como columna en el CSV exportado. Ejemplo: `nombre_lugar`

El script usa los **nombres internos**. Por eso en la seccion `CONFIGURACION` del script hay que poner exactamente el nombre interno que eligieron en Kobo.

**Donde veo el nombre interno en Kobo?**
En el editor del formulario, al hacer click en una pregunta, aparece el campo **"Nombre de datos"** — ese es el nombre interno.

---

## Parte 1 — Exportar datos desde KoboToolbox (10 min)

1. Entra a [kobotoolbox.org](https://kobotoolbox.org) con tu cuenta
2. Haz click en tu formulario
3. En la barra superior, click en **"Descargar datos"**
4. Configura la exportacion:
   - **Formato:** CSV
   - **Exportar:** Todos los datos
   - Activa **"Usar etiquetas en lugar de nombres XML"**
5. Click en **"Exportar"** y luego **"Descargar"**

El archivo descargado tendra un nombre largo con la fecha. Podes renombrarlo a algo mas corto como `datos.csv`.

---

## Parte 2 — Configurar el script (15 min)

Abre el archivo `kobo_a_umap.py` con cualquier editor de texto (Bloc de notas, TextEdit, VSCode, etc.).

Busca la seccion que dice `CONFIGURACION` y ajusta estas lineas:

```python
COLUMNA_NOMBRE   = "Nombre del lugar"    # nombre interno de tu columna de nombre
COLUMNA_FOTO     = "Foto del lugar"      # nombre interno de tu pregunta tipo Photo
COLUMNA_FOTO_URL = "Foto del lugar_URL"  # Kobo genera esta columna automaticamente
ANCHO_IMAGEN     = 300                   # ancho de imagen en el popup (px)
SEPARADOR_CSV    = ";"                   # separador del CSV — casi siempre es ;
COLUMNA_LAT      = "_Ubicacion GPS_latitude"   # ajusta segun tu formulario
COLUMNA_LON      = "_Ubicacion GPS_longitude"  # ajusta segun tu formulario
```

**Como saber los nombres exactos de mis columnas:**
- Opcion A: Abre el CSV con Excel o Google Sheets y mira la primera fila
- Opcion B: En Kobo, entra al editor del formulario → click en la pregunta → mira el campo "Nombre de datos"

Los nombres deben ser exactamente iguales a los del CSV, incluyendo mayusculas, minusculas y espacios.

---

## Parte 3 — Correr el script (5 min)

### En Windows

1. Abre la carpeta donde esta el script
2. En la barra de direcciones del explorador, escribe `cmd` y presiona Enter
3. En la ventana negra que aparece, escribe:

```
python kobo_a_umap.py nombre_de_tu_archivo.csv
```

### En Mac / Linux

1. Abre la Terminal
2. Navega hasta la carpeta con `cd`:

```bash
cd Descargas/kobo-a-umap
```

3. Corre el script:

```bash
python3 kobo_a_umap.py nombre_de_tu_archivo.csv
```

### Que deberia ver

```
Procesando: datos.csv
3 puntos exportados → datos_umap.geojson

----------------------------------------------------
PROXIMOS PASOS EN UMAP:
  1. Importar datos → subir: datos_umap.geojson
  2. Plantilla de contenido emergente:  {popup}
  3. Guardar — listo!
----------------------------------------------------
```

---

## Parte 4 — Importar en UMap (10 min)

1. Abre tu mapa en [umap.openstreetmap.fr](https://umap.openstreetmap.fr)
2. Haz click en el icono de lapiz para editar
3. En el panel lateral, click en **"Importar datos"**
4. Arrastra o selecciona el archivo `.geojson` generado
5. Formato: **GeoJSON** (se detecta automaticamente)
6. Click en **"Importar"**

### Activar el popup automatico

1. En el panel lateral, click en **"Propiedades del mapa"**
2. Busca **"Plantilla de contenido emergente"**
3. Escribe exactamente: `{popup}`
4. Guarda

Los marcadores ya deberian mostrar el popup con toda la informacion.

---

## Problemas frecuentes

### El script exporta 0 puntos / "Sin coordenadas"
El nombre de las columnas de latitud y longitud no coincide. Abre el CSV, busca las columnas que contienen numeros de coordenadas y copia sus nombres exactos en `COLUMNA_LAT` y `COLUMNA_LON` en el script.

### El script no encuentra mis columnas / el popup aparece sin datos
El nombre interno en el script no coincide con el del CSV. Abre el CSV, copia el nombre exacto de la columna (primera fila) y pegalo en la seccion `CONFIGURACION` del script.

### "No se encontro el archivo"
Verifica que el nombre del CSV que escribiste en el comando sea exactamente igual al nombre del archivo, incluyendo la extension `.csv`.

### "Fila sin coordenadas validas, se omite"
Algun registro en Kobo se guardo sin ubicacion GPS. Esto es normal — el script lo avisa y continua con los demas.

### El popup aparece vacio
Verifica que en UMap escribiste exactamente `{popup}` (con llaves, en minusculas) en la plantilla de contenido emergente.

### Las imagenes no aparecen
Verifica que `COLUMNA_FOTO_URL` tiene el nombre exacto de la columna `_URL` en tu CSV. Kobo la genera automaticamente cuando el formulario tiene una pregunta tipo Photo.

---

## Como agregar una pregunta de foto en Kobo

1. En KoboToolbox, abre el editor de tu formulario
2. Haz click en **"+ Agregar pregunta"**
3. Selecciona el tipo **"Photo"**
4. Dale un nombre simple, como `foto_lugar`
5. Guarda el formulario

Al exportar el CSV, Kobo incluira automaticamente una columna `foto_lugar_URL` con la URL de cada foto. Actualiza `COLUMNA_FOTO_URL` en el script con ese nombre.

---

## Recursos utiles

- [KoboToolbox — Documentacion](https://support.kobotoolbox.org)
- [UMap — Ayuda](https://umap.openstreetmap.fr/es/help/)
- [Instalar Python](https://www.python.org/downloads/)

---

Guia creada para el taller de mapeo colectivo.
