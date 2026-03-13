# Kobo a UMap

Herramienta para colectivas activistas que mapean con KoboToolbox y UMap.

Convierte exportaciones CSV de KoboToolbox en archivos GeoJSON listos para importar en [UMap](https://umap.openstreetmap.fr), con popups que incluyen nombre, imagen y todos los campos del formulario.

**[Ver ejemplo en el mapa](https://geojson.io/#data=data:text/x-url,https://raw.githubusercontent.com/seleneyang/de-kobo-a-umap/main/datos/ejemplo/ejemplo_resultado_umap.geojson)**

---

## Que hace este script

- Lee el CSV exportado desde KoboToolbox
- Sube las fotos a Google Drive y genera URLs publicas automaticamente
- Genera un archivo `.geojson` listo para UMap con un popup por punto que incluye nombre, foto y todos los campos del formulario
- En UMap solo hay que poner `{popup}` en la plantilla de contenido emergente

---

## Requisitos

- Python 3.7 o superior

Para verificar:
```bash
python3 --version
```

Para usar con fotos, instalar las librerias de Google una sola vez:
```bash
pip3 install google-auth google-auth-oauthlib google-api-python-client
```

---

## Instalacion

```bash
git clone https://github.com/TU_USUARIO/kobo-a-umap.git
cd kobo-a-umap
```

---

## Configuracion del script

Abrir `kobo_a_umap.py` con cualquier editor de texto y ajustar la seccion `CONFIGURACION`:

```python
COLUMNA_NOMBRE = "Nombre del lugar"   # nombre interno de la columna del lugar
COLUMNA_FOTO   = "Foto del lugar"     # nombre interno de la pregunta tipo Photo
ANCHO_IMAGEN   = 300                  # ancho de imagen en el popup (px)
SEPARADOR_CSV  = ";"                  # separador del CSV exportado por Kobo
COLUMNA_LAT    = "_Ubicacion GPS_latitude"
COLUMNA_LON    = "_Ubicacion GPS_longitude"
```

Los nombres deben coincidir exactamente con los de la primera fila del CSV. Para verlos, abrir el CSV con Excel o Google Sheets y mirar la primera fila.

---

## Uso

### Paso 0 — Configurar Google Drive (solo la primera vez)

Para que las fotos sean visibles en UMap necesitan estar en una URL publica. El script las sube automaticamente a Google Drive, pero primero hay que darle acceso.

1. Ir a [console.cloud.google.com](https://console.cloud.google.com) e iniciar sesion con la cuenta de Google donde se guardaran las fotos
2. Crear un proyecto nuevo llamado `kobo-umap`
3. Ir a **APIs y servicios** → **Biblioteca** → buscar **Google Drive API** → **Habilitar**
4. Ir a **APIs y servicios** → **Credenciales** → **Crear credenciales** → **ID de cliente de OAuth**
5. Si pide configurar la pantalla de consentimiento: elegir **Externo**, poner un nombre cualquiera y guardar
6. Tipo de aplicacion: **Aplicacion de escritorio** → nombre `kobo-umap-script` → **Crear**
7. Descargar el JSON generado y renombrarlo a exactamente `credentials.json`
8. Copiar `credentials.json` a la misma carpeta donde esta `kobo_a_umap.py`

La proxima vez que se corra el script con `--fotos`, abrira el navegador para autorizar el acceso. Despues de aceptar, queda guardado y no vuelve a pedirlo.

Ver instrucciones detalladas en `docs/guia-google-drive.md`.

---

### Paso 1 — Exportar desde KoboToolbox

1. Entrar a [kobotoolbox.org](https://kobotoolbox.org) con la cuenta
2. Click en el formulario
3. Click en **"Descargar datos"**
4. Configurar:
   - Formato: **CSV**
   - Activar **"Usar etiquetas en lugar de nombres XML"**
5. Click en **"Exportar"** y luego **"Descargar"**

Si el formulario tiene fotos, exportarlas tambien desde la misma pantalla:

6. Buscar la opcion **"Archivos multimedia"** o **"Media attachments"**
7. Descargar el ZIP y descomprimirlo en una carpeta, por ejemplo `fotos/`

### Paso 2 — Correr el script

Sin fotos:
```bash
python3 kobo_a_umap.py datos.csv
```

Con fotos:
```bash
python3 kobo_a_umap.py datos.csv --fotos fotos/
```

La primera vez que se corre con `--fotos`, el script abre el navegador para autorizar el acceso a Google Drive. Las veces siguientes es automatico. Ver `docs/guia-google-drive.md` para configurar esto.

### Paso 3 — Importar en UMap

1. Abrir el mapa en [umap.openstreetmap.fr](https://umap.openstreetmap.fr)
2. Click en el icono de lapiz para editar
3. En el panel lateral, click en **"Importar datos"**
4. Subir el archivo `.geojson` generado por el script
5. Formato: GeoJSON (se detecta automaticamente)
6. Click en **"Importar"**

### Paso 4 — Activar el popup

1. En el panel lateral, click en **"Propiedades del mapa"**
2. Buscar **"Plantilla de contenido emergente"**
3. Escribir exactamente: `{popup}`
4. Guardar

Los marcadores ya muestran el popup con nombre, foto y todos los campos.

---

## Campos que debe tener el formulario de Kobo

### Obligatorios

| Que pregunta | Tipo en Kobo | Nombre interno sugerido |
|---|---|---|
| Nombre del lugar | Text | `nombre_lugar` |
| Ubicacion GPS | Geopoint | `ubicacion_gps` |

Kobo desglosa el GPS automaticamente en 4 columnas al exportar. El script usa solo `_latitude` y `_longitude`.

### Para mostrar fotos

| Que pregunta | Tipo en Kobo | Nombre interno sugerido |
|---|---|---|
| Foto del lugar | Photo | `foto_lugar` |

### El resto

Cualquier otra pregunta del formulario aparece automaticamente en el popup. No hay que modificar el script.

---

## Problemas frecuentes

**El script exporta 0 puntos**
Los nombres de `COLUMNA_LAT` y `COLUMNA_LON` no coinciden con el CSV. Abrir el CSV, buscar las columnas con coordenadas y copiar sus nombres exactos en el script.

**El popup aparece sin datos**
El valor de `COLUMNA_NOMBRE` no coincide con el CSV. Copiar el nombre exacto de la primera fila del CSV.

**Las imagenes no aparecen en UMap**
Verificar que el script se corrio con `--fotos` y que la carpeta contenia las imagenes. Ver `docs/guia-google-drive.md` si hay errores de autenticacion.

**El popup aparece vacio en UMap**
Verificar que se escribio exactamente `{popup}` (con llaves, en minusculas) en la plantilla de contenido emergente.

---

## Estructura del repositorio

```
kobo-a-umap/
├── kobo_a_umap.py              <- Script principal
├── README.md                   <- Esta guia
├── requirements.txt            <- Librerias necesarias para fotos
├── .gitignore
├── datos/
│   └── ejemplo/
│       └── ejemplo_resultado_umap.geojson
└── docs/
    ├── guia-taller.md          <- Guia paso a paso para el taller
    └── guia-google-drive.md    <- Configuracion de Google Drive (una sola vez)
```

---

## Contribuciones

Proyecto de codigo abierto creado para apoyar el trabajo de colectivas feministas y activistas. Sugerencias y mejoras bienvenidas via issues o pull requests.
