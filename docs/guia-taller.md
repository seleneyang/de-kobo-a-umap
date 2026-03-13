# Guia para el taller — Kobo a UMap

Esta guia esta pensada para usarse durante el taller con la colectiva. Seguirla paso a paso con las companeras.

---

## Antes del taller — checklist

- [ ] Todas tienen Python 3 instalado (`python3 --version` en la terminal)
- [ ] Todas tienen la libreria de Cloudinary instalada (`pip3 install cloudinary`)
- [ ] Todas tienen cuenta en Cloudinary y sus tres credenciales configuradas en el script (Cloud name, API Key y API Secret) — ver "Paso 0" abajo
- [ ] Todas tienen acceso a su formulario de KoboToolbox
- [ ] El formulario tiene los campos obligatorios (ver seccion abajo)
- [ ] Se creo un mapa en UMap para practicar
- [ ] Se descargo este repositorio en las computadoras

---

## Paso 0 — Configurar Cloudinary (obligatorio, solo la primera vez)

Este paso debe completarse ANTES de correr el script. Sin las credenciales de Cloudinary el script no puede subir las fotos y fallara.

### Crear cuenta

1. Ir a [cloudinary.com](https://cloudinary.com)
2. Click en **"Sign up for free"**
3. Llenar el formulario y confirmar el correo

### Obtener las credenciales

1. Iniciar sesion en Cloudinary
2. Ir a **Settings** → **API Keys**
3. Anotar estos tres datos:
   - **Cloud name** — aparece en la parte superior de la pagina (ejemplo: `dpcw1ueng`)
   - **API Key** — numero en la columna "API Key" de la fila **Root**
   - **API Secret** — click en los asteriscos de la fila **Root** para revelarlo

### Agregar las credenciales al script

Abrir `kobo_a_umap.py` con cualquier editor de texto y completar estas tres lineas en la seccion `CONFIGURACION`:

```python
CLOUDINARY_CLOUD_NAME = "tu_cloud_name"
CLOUDINARY_API_KEY    = "tu_api_key"
CLOUDINARY_API_SECRET = "tu_api_secret"
```

> El API Secret es una clave privada. No compartirlo ni subirlo a GitHub.

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
2. Click en el formulario → click en **"Descargar datos"**
3. Configurar:
   - Formato: **CSV**
   - Activar **"Usar etiquetas en lugar de nombres XML"**
4. Click en **"Exportar"** y luego **"Descargar"**

### Exportar las fotos

En la misma pantalla de descarga:

1. Buscar la opcion **"Archivos multimedia"** o **"Media attachments"**
2. Descargar el ZIP
3. Descomprimir en una carpeta, por ejemplo `fotos/`

El CSV y la carpeta de fotos deben quedar en la misma carpeta que el script.

---

## Parte 2 — Configurar el script (10 min)

Ademas de las credenciales de Cloudinary del Paso 0, ajustar el resto de la seccion `CONFIGURACION` en `kobo_a_umap.py`:

```python
COLUMNA_NOMBRE        = "Nombre del lugar"   # nombre interno de la columna del lugar
COLUMNA_FOTO          = "Foto del lugar"     # nombre interno de la pregunta tipo Photo
ANCHO_IMAGEN          = 300                  # ancho de imagen en el popup (px)
SEPARADOR_CSV         = ";"                  # separador del CSV
COLUMNA_LAT           = "_Ubicacion GPS_latitude"
COLUMNA_LON           = "_Ubicacion GPS_longitude"
CLOUDINARY_CLOUD_NAME = "tu_cloud_name"      # del Paso 0
CLOUDINARY_API_KEY    = "tu_api_key"         # del Paso 0
CLOUDINARY_API_SECRET = "tu_api_secret"      # del Paso 0
```

Como saber los nombres exactos de las columnas:
- Abrir el CSV con Excel o Google Sheets y mirar la primera fila
- O en Kobo: editor del formulario → click en la pregunta → campo "Nombre de datos"

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
Subiendo 3 fotos a Cloudinary...
   [1/3] foto_001.jpg -> ok
   [2/3] foto_002.jpg -> ok
   [3/3] foto_003.jpg -> ok
Fotos listas.

Procesando: datos.csv
Listo. 3 puntos exportados -> datos_umap.geojson
   3 puntos con imagen

----------------------------------------------------
PROXIMOS PASOS EN UMAP:
  1. Importar datos -> subir: datos_umap.geojson
  2. Plantilla de contenido emergente:  {popup}
  3. Guardar
----------------------------------------------------
```

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

### El script falla con error de Cloudinary
Verificar que las tres credenciales (Cloud name, API Key y API Secret) estan correctamente pegadas en el script. Ver Paso 0.

### El script exporta 0 puntos / "Sin coordenadas"
Los nombres de `COLUMNA_LAT` y `COLUMNA_LON` no coinciden con el CSV. Abrir el CSV, buscar las columnas con coordenadas y copiar sus nombres exactos en el script.

### El popup aparece sin datos
El nombre en `COLUMNA_NOMBRE` no coincide con el CSV. Copiar el nombre exacto de la primera fila.

### "No se encontro el archivo"
Verificar que el nombre del CSV en el comando sea exactamente igual al nombre del archivo incluyendo `.csv`.

### "Fila sin coordenadas validas, se omite"
Algun registro se guardo sin GPS. Es normal — el script continua con los demas.

### El popup aparece vacio en UMap
Verificar que se escribio exactamente `{popup}` (con llaves, en minusculas) en la plantilla.

### Las imagenes no aparecen en UMap
Verificar que las credenciales de Cloudinary estan configuradas y que el script se corrio con `--fotos`.

---

## Recursos

- [KoboToolbox — Documentacion](https://support.kobotoolbox.org)
- [UMap — Ayuda](https://umap.openstreetmap.fr/es/help/)
- [Instalar Python](https://www.python.org/downloads/)
- [Cloudinary — Registro](https://cloudinary.com)

---

Guia creada para el taller de mapeo colectivo.
