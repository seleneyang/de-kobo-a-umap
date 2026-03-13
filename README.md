# Kobo a UMap

Herramienta para colectivas activistas que mapean con KoboToolbox y UMap.

Convierte exportaciones CSV de KoboToolbox en archivos GeoJSON listos para importar en [UMap](https://umap.openstreetmap.fr), con popups que incluyen nombre, imagen y todos los campos del formulario.

**[Ver ejemplo en el mapa](https://geojson.io/#data=data:text/x-url,https://raw.githubusercontent.com/seleneyang/de-kobo-a-umap/main/datos/ejemplo/ejemplo_resultado_umap.geojson)**

---

## Que hace este script

- Lee el CSV exportado desde KoboToolbox
- Sube las fotos a Cloudinary y genera URLs publicas automaticamente
- Genera un archivo `.geojson` listo para UMap con un popup por punto que incluye nombre, foto y todos los campos del formulario
- En UMap solo hay que poner `{popup}` en la plantilla de contenido emergente

---

## Requisitos

- Python 3.7 o superior (sin dependencias externas)

Para verificar:
```bash
python3 --version
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
COLUMNA_NOMBRE  = "Nombre del lugar"   # nombre interno de la columna del lugar
COLUMNA_FOTO    = "Foto del lugar"     # nombre interno de la pregunta tipo Photo
ANCHO_IMAGEN    = 300                  # ancho de imagen en el popup (px)
SEPARADOR_CSV   = ";"                  # separador del CSV exportado por Kobo
COLUMNA_LAT     = "_Ubicacion GPS_latitude"
COLUMNA_LON     = "_Ubicacion GPS_longitude"
IMGUR_CLIENT_ID = "aca_va_tu_client_id"  # ver docs/guia-cloudinary.md
```

Los nombres de columna deben coincidir exactamente con los de la primera fila del CSV.

---

## Uso

### Paso 0 — Obtener el Client ID de Cloudinary (solo la primera vez)

1. Crear cuenta gratuita en [cloudinary.com](https://cloudinary.com)
2. Ir a [api.cloudinary.com/oauth2/addclient](https://api.cloudinary.com/oauth2/addclient)
3. Llenar el formulario:
   - Application name: `kobo-umap`
   - Authorization type: **"Anonymous usage without user authorization"**
4. Click en Submit — aparece el **Client ID**
5. Pegarlo en el script: `IMGUR_CLIENT_ID = "tu_client_id"`

Ver instrucciones detalladas en `docs/guia-cloudinary.md`.

### Paso 1 — Exportar desde KoboToolbox

1. Entrar a [kobotoolbox.org](https://kobotoolbox.org)
2. Click en el formulario → **"Descargar datos"**
3. Formato: **CSV** — activar **"Usar etiquetas en lugar de nombres XML"**
4. Exportar y descargar

Si el formulario tiene fotos:

5. En la misma pantalla buscar **"Archivos multimedia"** o **"Media attachments"**
6. Descargar el ZIP y descomprimirlo en una carpeta, por ejemplo `fotos/`

### Paso 2 — Correr el script

Sin fotos:
```bash
python3 kobo_a_umap.py datos.csv
```

Con fotos:
```bash
python3 kobo_a_umap.py datos.csv --fotos fotos/
```

Genera automaticamente `datos_umap.geojson`. Las fotos ya subidas se reutilizan desde el cache local.

### Paso 3 — Importar en UMap

1. Abrir el mapa en [umap.openstreetmap.fr](https://umap.openstreetmap.fr)
2. Click en el icono de lapiz para editar
3. En el panel lateral, click en **"Importar datos"**
4. Subir el archivo `.geojson` generado
5. Click en **"Importar"**

### Paso 4 — Activar el popup

1. Click en **"Propiedades del mapa"**
2. Buscar **"Plantilla de contenido emergente"**
3. Escribir exactamente: `{popup}`
4. Guardar

---

## Campos que debe tener el formulario de Kobo

### Obligatorios

| Que pregunta | Tipo en Kobo | Nombre interno sugerido |
|---|---|---|
| Nombre del lugar | Text | `nombre_lugar` |
| Ubicacion GPS | Geopoint | `ubicacion_gps` |

### Para mostrar fotos

| Que pregunta | Tipo en Kobo | Nombre interno sugerido |
|---|---|---|
| Foto del lugar | Photo | `foto_lugar` |

### El resto

Cualquier otra pregunta del formulario aparece automaticamente en el popup.

---

## Problemas frecuentes

**El script exporta 0 puntos**
Los nombres de `COLUMNA_LAT` y `COLUMNA_LON` no coinciden con el CSV. Abrir el CSV y copiar los nombres exactos de las columnas de coordenadas.

**El popup aparece sin datos**
El valor de `COLUMNA_NOMBRE` no coincide con el CSV.

**Las imagenes no aparecen en UMap**
Verificar que `IMGUR_CLIENT_ID` esta configurado y que el script se corrio con `--fotos`.

**El popup aparece vacio en UMap**
Verificar que se escribio exactamente `{popup}` en la plantilla de contenido emergente.

---

## Estructura del repositorio

```
kobo-a-umap/
├── kobo_a_umap.py
├── README.md
├── requirements.txt
├── .gitignore
├── datos/
│   └── ejemplo/
│       └── ejemplo_resultado_umap.geojson
└── docs/
    ├── guia-taller.md
    └── guia-cloudinary.md
```

---

## Contribuciones

Proyecto de codigo abierto creado para apoyar el trabajo de colectivas feministas y activistas. Sugerencias y mejoras bienvenidas via issues o pull requests.

---

## Licencia

MIT — libre para usar, modificar y compartir.
