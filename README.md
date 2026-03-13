# Kobo a UMap

**Herramienta para colectivas activistas que mapean con KoboToolbox y UMap.**

Convierte automáticamente las exportaciones CSV de KoboToolbox en archivos GeoJSON listos para importar en [UMap](https://umap.openstreetmap.fr), con popups que incluyen nombre, imagen y todos los campos del formulario.

---

## ¿Qué hace este script?

- Lee el CSV exportado desde KoboToolbox
- Genera un archivo `.geojson` compatible con UMap
- Crea un popup automático con:
  - Nombre del lugar
  - Imagen (formateada para UMap)
  - Todos los campos del formulario
- Solo necesitas poner `{popup}` en la plantilla de UMap y ¡listo!

---

## Requisitos

- Python 3.7 o superior
- Sin dependencias externas (solo usa librerías estándar de Python)

Verificá tu versión de Python con:
```bash
python3 --version
```

---

## Instalación

```bash
# 1. Clona el repositorio
git clone https://github.com/TU_USUARIO/kobo-a-umap.git
cd kobo-a-umap

# 2. ¡Listo! No hay dependencias que instalar.
```

---

## Uso

### Paso 1 — Exportar desde KoboToolbox

1. En KoboToolbox, ve a tu formulario → **Descargar datos**
2. Formato: **CSV**
3. Seleccioná **"Usar etiquetas en lugar de nombres XML"**
4. Descargá el archivo

### Paso 2 — Configurar el script

Abrí `kobo_a_umap.py` y ajustá la sección `⚙️ CONFIGURACIÓN`:

```python
COLUMNA_NOMBRE  = "Nombre del establecimiento"  # columna con el nombre del lugar
COLUMNA_FOTO    = "foto_establecimiento"         # columna con la foto (tipo image en Kobo)
BASE_URL_FOTOS  = ""                             # URL base si las fotos están en tu servidor
ANCHO_IMAGEN    = 300                            # ancho de imagen en el popup (px)
```

### Paso 3 — Correr el script

```bash
python3 kobo_a_umap.py mi_archivo.csv
```

Genera automáticamente `mi_archivo_umap.geojson`.

### Paso 4 — Importar en UMap

1. Abrí tu mapa en UMap
2. Click en **Importar datos** (ícono de flecha hacia arriba)
3. Subí el archivo `.geojson` generado
4. En **"Plantilla de contenido emergente"** escribí solo: `{popup}`
5. Guardá el mapa — ¡los popups ya funcionan!

---

## Sobre las imágenes

Para que aparezcan imágenes en el popup, tu formulario Kobo debe tener una pregunta de tipo **Photo**. El script las formatea automáticamente según el estándar de UMap:

```
https://url-de-la-imagen.com|300
```

Si las fotos están en un servidor propio (por ejemplo, tu sitio web), configurá `BASE_URL_FOTOS` con la URL base y el script completará las rutas automáticamente.

---

## Ejemplo de popup generado

```
# Botica Familiar

[imagen]

**Tipo de establecimiento:** Farmacia local
**¿Tiene AE a la venta?:** Sí
**¿Cómo fue el trato?:** Amable, profesional, sin juicios
**¿Qué calificación le darías?:** Muy bueno
**¿Recomendarías este lugar?:** Sí
```

---

## Contribuciones

Este proyecto es de código abierto y fue creado para apoyar el trabajo de colectivas feministas y activistas. Si tenés sugerencias o mejoras, abrí un issue o un pull request.

