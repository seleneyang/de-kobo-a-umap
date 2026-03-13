# Guia para el taller — Kobo a UMap

Esta guia esta pensada para usarse durante el taller con la colectiva. Seguirla paso a paso con las companeras.

---

## Antes del taller — checklist

- [ ] Todas tienen Python 3 instalado (`python3 --version` en la terminal)
- [ ] Todas tienen las librerias de Google instaladas (`pip3 install google-auth google-auth-oauthlib google-api-python-client`)
- [ ] Todas tienen acceso a su formulario de KoboToolbox
- [ ] El formulario tiene los campos obligatorios (ver seccion abajo)
- [ ] Se configuro Google Drive siguiendo `docs/guia-google-drive.md`
- [ ] Se creo un mapa en UMap para practicar
- [ ] Se descargo este repositorio en las computadoras

---

## Campos que debe tener el formulario de Kobo

### Obligatorios

| Que pregunta | Tipo en Kobo | Nombre interno sugerido |
|---|---|---|
| Nombre del lugar | Text | `nombre_lugar` |
| Ubicacion GPS | Geopoint | `ubicacion_gps` |

Kobo desglosa el GPS automaticamente en 4 columnas al exportar. El script usa solo `_latitude` y `_longitude`.

### Para mostrar fotos en el popup

| Que pregunta | Tipo en Kobo | Nombre interno sugerido |
|---|---|---|
| Foto del lugar | Photo | `foto_lugar` |

### El resto: libertad total

Cualquier otra pregunta agregada aparecera automaticamente en el popup. No hay que tocar el script.

---

## Etiqueta vs. nombre interno

Kobo maneja dos nombres por cada pregunta:

- **Etiqueta** — lo que ve la usuaria al llenar el formulario. Ejemplo: "Como se llama este lugar?"
- **Nombre interno** — lo que aparece como columna en el CSV exportado. Ejemplo: `nombre_lugar`

El script usa los **nombres internos**. En el editor del formulario, al hacer click en una pregunta, aparece el campo "Nombre de datos" — ese es el nombre interno.

---

## Parte 1 — Exportar datos desde KoboToolbox (10 min)

### Exportar el CSV

1. Entrar a [kobotoolbox.org](https://kobotoolbox.org)
2. Click en el formulario
3. Click en **"Descargar datos"**
4. Configurar:
   - Formato: **CSV**
   - Activar **"Usar etiquetas en lugar de nombres XML"**
5. Click en **"Exportar"** y luego **"Descargar"**

### Exportar las fotos

En la misma pantalla de descarga:

1. Buscar la opcion **"Archivos multimedia"** o **"Media attachments"**
2. Descargar el ZIP
3. Descomprimir en una carpeta, por ejemplo `fotos/`

El archivo CSV y la carpeta de fotos deben quedar juntos en la misma carpeta que el script.

---

## Parte 2 — Configurar el script (15 min)

Abrir `kobo_a_umap.py` con cualquier editor de texto y ajustar la seccion `CONFIGURACION`:

```python
COLUMNA_NOMBRE = "Nombre del lugar"   # nombre interno de la columna del lugar
COLUMNA_FOTO   = "Foto del lugar"     # nombre interno de la pregunta tipo Photo
ANCHO_IMAGEN   = 300                  # ancho de imagen en el popup (px)
SEPARADOR_CSV  = ";"                  # separador del CSV
COLUMNA_LAT    = "_Ubicacion GPS_latitude"
COLUMNA_LON    = "_Ubicacion GPS_longitude"
```

Como saber los nombres exactos:
- Opcion A: Abrir el CSV con Excel o Google Sheets y mirar la primera fila
- Opcion B: En Kobo, editor del formulario → click en la pregunta → campo "Nombre de datos"

Los nombres deben ser exactamente iguales a los del CSV, incluyendo mayusculas, minusculas y espacios.

---

## Parte 3 — Correr el script (5 min)

### En Windows

1. Abrir la carpeta donde esta el script
2. En la barra de direcciones escribir `cmd` y presionar Enter
3. Escribir:

```
python kobo_a_umap.py datos.csv --fotos fotos/
```

### En Mac / Linux

```bash
cd Descargas/kobo-a-umap
python3 kobo_a_umap.py datos.csv --fotos fotos/
```

### Que deberia ver

```
Conectando con Google Drive...
   Carpeta 'fotos_mapa' encontrada en Drive.

Subiendo 3 fotos...
   [1/3] foto_001.jpg → ok
   [2/3] foto_002.jpg → ok
   [3/3] foto_003.jpg → ok
Fotos listas.

Procesando: datos.csv
3 puntos exportados → datos_umap.geojson
   3 puntos con imagen

----------------------------------------------------
PROXIMOS PASOS EN UMAP:
  1. Importar datos → subir: datos_umap.geojson
  2. Plantilla de contenido emergente:  {popup}
  3. Guardar — listo!
----------------------------------------------------
```

La primera vez abre el navegador para autorizar Google Drive. Las veces siguientes es automatico.

---

## Parte 4 — Importar en UMap (10 min)

1. Abrir el mapa en [umap.openstreetmap.fr](https://umap.openstreetmap.fr)
2. Click en el icono de lapiz para editar
3. En el panel lateral, click en **"Importar datos"**
4. Subir el archivo `.geojson` generado
5. Formato: GeoJSON (se detecta automaticamente)
6. Click en **"Importar"**

### Activar el popup

1. Click en **"Propiedades del mapa"**
2. Buscar **"Plantilla de contenido emergente"**
3. Escribir exactamente: `{popup}`
4. Guardar

---

## Problemas frecuentes

### El script exporta 0 puntos / "Sin coordenadas"
Los nombres de `COLUMNA_LAT` y `COLUMNA_LON` no coinciden con el CSV. Abrir el CSV, buscar las columnas con numeros de coordenadas y copiar sus nombres exactos en el script.

### El popup aparece sin datos
El nombre interno en el script no coincide con el del CSV. Copiar el nombre exacto de la primera fila del CSV y pegarlo en `COLUMNA_NOMBRE`.

### "No se encontro el archivo"
Verificar que el nombre del CSV en el comando sea exactamente igual al nombre del archivo incluyendo la extension `.csv`.

### "Fila sin coordenadas validas, se omite"
Algun registro se guardo sin GPS. Es normal — el script lo avisa y continua con los demas.

### El popup aparece vacio en UMap
Verificar que se escribio exactamente `{popup}` (con llaves, en minusculas) en la plantilla.

### Las imagenes no aparecen en UMap
Verificar que el script se corrio con `--fotos` y que la carpeta contenia las imagenes correctas.

### Error de Google Drive la primera vez
Seguir la guia en `docs/guia-google-drive.md`.

---

## Recursos

- [KoboToolbox — Documentacion](https://support.kobotoolbox.org)
- [UMap — Ayuda](https://umap.openstreetmap.fr/es/help/)
- [Instalar Python](https://www.python.org/downloads/)

---

Guia creada para el taller de mapeo colectivo.
