# Kobo a UMap

**Herramienta para colectivas activistas que mapean con KoboToolbox y UMap.**

Convierte automáticamente las exportaciones CSV de KoboToolbox en archivos GeoJSON listos para importar en [UMap](https://umap.openstreetmap.fr), con popups que incluyen nombre, imagen y todos los campos del formulario.

**[Ver ejemplo de resultado en el mapa](https://geojson.io/#data=data:text/x-url,https://raw.githubusercontent.com/seleneyang/de-kobo-a-umap/main/datos/ejemplo/ejemplo_resultado_umap.geojson)**

---

## Que hace este script

- Lee el CSV exportado desde KoboToolbox
- Genera un archivo `.geojson` compatible con UMap
- Crea un popup automatico con nombre, imagen y todos los campos del formulario
- Las fotos se toman de la URL que Kobo exporta directamente — no se necesita ningun servidor externo
- Solo necesitas poner `{popup}` en la plantilla de UMap y listo

---

## Requisitos

- Python 3.7 o superior
- Sin dependencias externas (solo usa librerias estandar de Python)

Verifica tu version de Python con:
```bash
python3 --version
```

---

## Instalacion

```bash
# 1. Clona el repositorio
git clone https://github.com/TU_USUARIO/kobo-a-umap.git
cd kobo-a-umap

# 2. Listo. No hay dependencias que instalar.
```

---

## Uso

### Paso 1 — Exportar desde KoboToolbox

1. En KoboToolbox, ve a tu formulario → **Descargar datos**
2. Formato: **CSV**
3. Selecciona **"Usar etiquetas en lugar de nombres XML"**
4. Descarga el archivo

### Paso 2 — Configurar el script

Abre `kobo_a_umap.py` y ajusta la seccion `CONFIGURACION`:

```python
COLUMNA_NOMBRE   = "Nombre del lugar"    # nombre interno de la columna del lugar
COLUMNA_FOTO     = "Foto del lugar"      # nombre interno de la pregunta tipo Photo
COLUMNA_FOTO_URL = "Foto del lugar_URL"  # Kobo genera esta columna automaticamente
ANCHO_IMAGEN     = 300                   # ancho de imagen en el popup (px)
SEPARADOR_CSV    = ";"                   # separador del CSV exportado por Kobo
COLUMNA_LAT      = "_Ubicacion GPS_latitude"
COLUMNA_LON      = "_Ubicacion GPS_longitude"
```

> Los nombres de columna deben coincidir exactamente con los de la primera fila del CSV.

### Paso 3 — Correr el script

```bash
python3 kobo_a_umap.py mi_archivo.csv
```

Genera automaticamente `mi_archivo_umap.geojson`.

### Paso 4 — Importar en UMap

1. Abre tu mapa en UMap
2. Click en **Importar datos**
3. Sube el archivo `.geojson` generado
4. En **"Plantilla de contenido emergente"** escribe solo: `{popup}`
5. Guarda el mapa

---

## Sobre las imagenes

El script usa la columna `_URL` que Kobo genera automaticamente al exportar formularios con preguntas de tipo **Photo**. No se necesita ningun servidor externo ni configuracion adicional.

---

## Estructura del repositorio

```
kobo-a-umap/
├── kobo_a_umap.py              <- Script principal
├── README.md                   <- Esta guia
├── .gitignore                  <- Archivos excluidos de Git
├── datos/
│   └── ejemplo/
│       └── ejemplo_resultado_umap.geojson   <- Ejemplo de salida
└── docs/
    └── guia-taller.md          <- Guia paso a paso para el taller
```

---

## Ejemplo de popup generado

```
# Nombre del lugar

[imagen]

**Tipo de establecimiento:** Farmacia local
**Tiene AE a la venta:** Si
**Como fue el trato:** Amable, profesional, sin juicios
**Calificacion del servicio:** Muy bueno
```

---

## Contribuciones

Este proyecto es de codigo abierto y fue creado para apoyar el trabajo de colectivas feministas y activistas. Si tienes sugerencias o mejoras, abre un issue o un pull request.

---

## Licencia

MIT — libre para usar, modificar y compartir.
