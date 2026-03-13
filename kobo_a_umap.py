#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║         KOBO → UMAP  |  Convertidor de datos                ║
║  Para colectivas que mapean con KoboToolbox + UMap           ║
╚══════════════════════════════════════════════════════════════╝

USO:
    python kobo_a_umap.py mi_archivo.csv

RESULTADO:
    Un archivo  mi_archivo_umap.geojson  listo para importar en UMap.

INSTRUCCIONES UMAP:
    1. En tu mapa de UMap, click en "Importar datos"
    2. Sube el archivo .geojson generado
    3. En "Plantilla de contenido emergente" escribe solo:  {popup}
    4. ¡Listo! El popup ya incluye nombre e imagen formateada.

SOBRE LAS IMÁGENES:
    El CSV de Kobo debe tener una columna llamada exactamente:
        foto   (o cualquier nombre que configures en COLUMNA_FOTO abajo)
    con la URL pública de la imagen o el nombre del archivo.

    Si la URL base de tus fotos es siempre la misma, configura
    BASE_URL_FOTOS abajo para que se complete automáticamente.
"""

import csv
import json
import sys
import os

# ─────────────────────────────────────────────
#   ⚙️  CONFIGURACIÓN  — ajusta estos valores
# ─────────────────────────────────────────────

# Columna con el nombre del lugar (tal como aparece en el CSV de Kobo)
COLUMNA_NOMBRE = "Nombre del establecimiento "

# Columna con la foto  ← agrégala en tu formulario Kobo con tipo "image"
# Kobo exporta la columna con el nombre de la pregunta. Ajústalo aquí.
COLUMNA_FOTO = "foto_establecimiento"

# Si las fotos están en un servidor propio, pon la URL base aquí.
# Ejemplo: "https://tusitio.org/fotos/"
# Si la columna ya trae la URL completa, déjalo vacío: ""
BASE_URL_FOTOS = ""

# Ancho de imagen en el popup de UMap (en píxeles). None = sin restricción.
ANCHO_IMAGEN = 300

# Columnas de latitud y longitud en el CSV de Kobo
COLUMNA_LAT = "_Ubicación del establecimiento_latitude"
COLUMNA_LON = "_Ubicación del establecimiento_longitude"

# Columnas que NO quieres que aparezcan en el popup (metadatos internos de Kobo)
COLUMNAS_EXCLUIR = {
    "_id", "_uuid", "_submission_time", "_validation_status",
    "_notes", "_status", "_submitted_by", "__version__", "_tags", "_index",
    "_Ubicación del establecimiento_altitude",
    "_Ubicación del establecimiento_precision",
    "Ubicación del establecimiento",
    "Muchas gracias! Acá termina este registro.",
    "Muchas gracias!!",
}

# ─────────────────────────────────────────────
#   🔧  LÓGICA DEL SCRIPT  (no necesitas editar)
# ─────────────────────────────────────────────

def formatear_url_imagen(valor):
    """Devuelve la URL completa de la imagen."""
    if not valor or not valor.strip():
        return None
    url = valor.strip()
    if not url.startswith("http") and BASE_URL_FOTOS:
        url = BASE_URL_FOTOS.rstrip("/") + "/" + url
    return url


def construir_popup(row, columnas_extras):
    """
    Construye el HTML del popup de UMap.
    Formato UMap para imágenes: https://url.com|ancho
    """
    nombre = row.get(COLUMNA_NOMBRE, "Sin nombre").strip()
    url_foto = formatear_url_imagen(row.get(COLUMNA_FOTO, ""))

    lineas = []

    # Nombre como título
    lineas.append(f"# {nombre}")
    lineas.append("")

    # Imagen (si existe)
    if url_foto:
        if ANCHO_IMAGEN:
            lineas.append(f"{{{{foto_establecimiento.jpg}}}}")
            # Nota: UMap usa la sintaxis  https://url|ancho  en el campo de imagen
            # Se incluye en la propiedad especial de abajo
        else:
            lineas.append(f"{{{{foto_establecimiento.jpg}}}}")
        lineas.append("")

    # Resto de campos
    for col in columnas_extras:
        valor = row.get(col, "").strip()
        if valor:
            lineas.append(f"**{col}:** {valor}")

    return "\n".join(lineas)


def csv_a_geojson(ruta_csv):
    features = []

    with open(ruta_csv, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        columnas = reader.fieldnames or []

        # Columnas que van al popup (excluye coordenadas, foto y las excluidas)
        columnas_popup = [
            c for c in columnas
            if c not in COLUMNAS_EXCLUIR
            and c != COLUMNA_NOMBRE
            and c != COLUMNA_FOTO
            and c != COLUMNA_LAT
            and c != COLUMNA_LON
        ]

        for row in reader:
            lat_str = row.get(COLUMNA_LAT, "").strip()
            lon_str = row.get(COLUMNA_LON, "").strip()

            # Omitir filas sin coordenadas válidas
            try:
                lat = float(lat_str)
                lon = float(lon_str)
            except (ValueError, TypeError):
                print(f"  ⚠️  Fila sin coordenadas válidas, se omite: {row.get(COLUMNA_NOMBRE, '?')}")
                continue

            nombre = row.get(COLUMNA_NOMBRE, "Sin nombre").strip()
            url_foto = formatear_url_imagen(row.get(COLUMNA_FOTO, ""))

            # ── Propiedades para UMap ──────────────────────────────
            props = {}
            props["name"] = nombre  # UMap usa "name" para el título del marcador

            # Imagen formateada para UMap
            if url_foto:
                if ANCHO_IMAGEN:
                    props["_umap_options"] = {}  # placeholder
                    # La URL con ancho se pone directamente en el popup
                    imagen_umap = f"{url_foto}|{ANCHO_IMAGEN}"
                else:
                    imagen_umap = url_foto
                props["imagen"] = imagen_umap
            else:
                imagen_umap = None

            # Construir popup en formato Markdown que entiende UMap
            lineas_popup = [f"# {nombre}", ""]

            if imagen_umap:
                lineas_popup.append(f"{{imagen}}")   # UMap reemplaza esto con la imagen
                lineas_popup.append("")

            for col in columnas_popup:
                valor = row.get(col, "").strip()
                if valor:
                    lineas_popup.append(f"**{col}:** {valor}")

            props["popup"] = "\n".join(lineas_popup)

            # Resto de columnas como propiedades individuales (útil para filtros en UMap)
            for col in columnas_popup:
                valor = row.get(col, "").strip()
                if valor:
                    props[col] = valor

            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]   # GeoJSON: [longitud, latitud]
                },
                "properties": props
            }
            features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    return geojson


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nEjemplo de uso:")
        print("  python kobo_a_umap.py mis_datos.csv\n")
        sys.exit(1)

    ruta_csv = sys.argv[1]

    if not os.path.exists(ruta_csv):
        print(f"❌ No se encontró el archivo: {ruta_csv}")
        sys.exit(1)

    print(f"\n📂 Procesando: {ruta_csv}")
    geojson = csv_a_geojson(ruta_csv)

    # Nombre del archivo de salida
    base = os.path.splitext(ruta_csv)[0]
    ruta_salida = base + "_umap.geojson"

    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    total = len(geojson["features"])
    print(f"✅ ¡Listo! {total} puntos exportados a: {ruta_salida}")
    print()
    print("─" * 50)
    print("PRÓXIMOS PASOS EN UMAP:")
    print("  1. Abre tu mapa → click en 'Importar datos'")
    print(f"  2. Sube el archivo: {os.path.basename(ruta_salida)}")
    print("  3. En 'Plantilla de contenido emergente' escribe:  {popup}")
    print("  4. Guarda y ¡ya aparece el popup con nombre e imagen!")
    print("─" * 50)
    print()


if __name__ == "__main__":
    main()
