#!/usr/bin/env python3
"""
KOBO A UMAP — Convertidor de datos
Para colectivas que mapean con KoboToolbox y UMap

USO SIN FOTOS:
    python3 kobo_a_umap.py datos.csv

USO CON FOTOS (sube imagenes a Cloudinary automaticamente):
    python3 kobo_a_umap.py datos.csv --fotos carpeta_de_fotos/

RESULTADO:
    Un archivo datos_umap.geojson listo para importar en UMap.

INSTRUCCIONES UMAP:
    1. Importar datos -> subir el archivo .geojson generado
    2. En Plantilla de contenido emergente escribir solo: {popup}
    3. Listo
"""

import csv
import json
import sys
import os
import argparse

# ─────────────────────────────────────────────
#   CONFIGURACION — ajusta estos valores
# ─────────────────────────────────────────────

COLUMNA_NOMBRE   = "Nombre del lugar"
COLUMNA_FOTO     = "Foto del lugar"
COLUMNA_FOTO_URL = "Foto del lugar_URL"
ANCHO_IMAGEN     = 300
COLUMNA_LAT      = "_Ubicación GPS_latitude"
COLUMNA_LON      = "_Ubicación GPS_longitude"
SEPARADOR_CSV    = ";"

# Credenciales de Cloudinary
# Obtenerlas en cloudinary.com -> Settings -> API Keys
CLOUDINARY_CLOUD_NAME = "dpcw1ueng"
CLOUDINARY_API_KEY    = "766928646231284"
CLOUDINARY_API_SECRET = ""  # <- pegar aqui el API Secret (no subir al repo)

COLUMNAS_EXCLUIR = {
    "_id", "_uuid", "_submission_time", "_validation_status",
    "_notes", "_status", "_submitted_by", "__version__", "_tags", "_index",
    "_Ubicación del establecimiento_altitude",
    "_Ubicación del establecimiento_precision",
    "Ubicación del establecimiento",
    "_Ubicación GPS_altitude",
    "_Ubicación GPS_precision",
    "Ubicación GPS",
    "start", "end", "meta/rootUuid",
    "Muchas gracias! Acá termina este registro.",
    "Muchas gracias!!",
}

# ─────────────────────────────────────────────
#   CLOUDINARY
# ─────────────────────────────────────────────

CACHE_FILE = "cloudinary_cache.json"

def cargar_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def guardar_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def subir_foto_cloudinary(ruta_local, cache):
    nombre = os.path.basename(ruta_local)

    if nombre in cache:
        print(f"   (cache) {nombre}")
        return cache[nombre]

    try:
        import cloudinary
        import cloudinary.uploader
    except ImportError:
        print("\nFalta la libreria de Cloudinary. Instalarla con:")
        print("   pip3 install cloudinary")
        sys.exit(1)

    if not CLOUDINARY_API_SECRET:
        print("\nFalta CLOUDINARY_API_SECRET en la configuracion del script.")
        sys.exit(1)

    cloudinary.config(
        cloud_name = CLOUDINARY_CLOUD_NAME,
        api_key    = CLOUDINARY_API_KEY,
        api_secret = CLOUDINARY_API_SECRET
    )

    result = cloudinary.uploader.upload(
        ruta_local,
        folder = "fotos_mapa",
        use_filename = True,
        unique_filename = False,
        overwrite = True
    )

    url = result["secure_url"]
    cache[nombre] = url
    guardar_cache(cache)
    return url


def preparar_cloudinary(carpeta_local):
    exts  = {".jpg", ".jpeg", ".png", ".webp"}
    fotos = [f for f in os.listdir(carpeta_local)
             if os.path.splitext(f)[1].lower() in exts]

    if not fotos:
        print(f"   Sin imagenes en '{carpeta_local}'")
        return {}

    cache = cargar_cache()
    print(f"\nSubiendo {len(fotos)} fotos a Cloudinary...")
    urls = {}
    for i, nombre in enumerate(fotos, 1):
        ruta = os.path.join(carpeta_local, nombre)
        url  = subir_foto_cloudinary(ruta, cache)
        # Guardar con nombre original y también con espacios (como exporta Kobo)
        urls[nombre] = url
        urls[nombre.replace("_", " ")] = url
        print(f"   [{i}/{len(fotos)}] {nombre} -> ok")

    print("Fotos listas.\n")
    return urls


# ─────────────────────────────────────────────
#   CONVERSION A GEOJSON
# ─────────────────────────────────────────────

def csv_a_geojson(ruta_csv, urls_fotos=None):
    if urls_fotos is None:
        urls_fotos = {}

    features = []

    with open(ruta_csv, newline="", encoding="utf-8-sig") as f:
        reader   = csv.DictReader(f, delimiter=SEPARADOR_CSV)
        columnas = reader.fieldnames or []

        cols_popup = [
            c for c in columnas
            if c not in COLUMNAS_EXCLUIR
            and c not in {COLUMNA_NOMBRE, COLUMNA_FOTO, COLUMNA_FOTO_URL,
                          COLUMNA_LAT, COLUMNA_LON}
        ]

        for row in reader:
            try:
                lat = float(row.get(COLUMNA_LAT, "").strip())
                lon = float(row.get(COLUMNA_LON, "").strip())
            except (ValueError, TypeError):
                print(f"  Sin coordenadas: {row.get(COLUMNA_NOMBRE, '?').strip()}")
                continue

            nombre   = row.get(COLUMNA_NOMBRE, "Sin nombre").strip()
            # Si se subieron fotos a Cloudinary, usarlas siempre
            # Si no, intentar la URL directa del CSV
            nom_foto = row.get(COLUMNA_FOTO, "").strip()
            if urls_fotos:
                url_foto = urls_fotos.get(nom_foto, "")
            else:
                url_foto = row.get(COLUMNA_FOTO_URL, "").strip()

            lineas = [f"# {nombre}", ""]
            if url_foto:
                lineas += ["{{" + url_foto + "|" + str(ANCHO_IMAGEN) + "}}", ""]
            for col in cols_popup:
                v = row.get(col, "").strip()
                if v:
                    lineas.append(f"**{col}:** {v}")

            props = {"name": nombre, "popup": "\n".join(lineas)}
            if url_foto:
                props["imagen"] = f"{url_foto}|{ANCHO_IMAGEN}"
            for col in cols_popup:
                v = row.get(col, "").strip()
                if v:
                    props[col] = v

            features.append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": props,
            })

    return {"type": "FeatureCollection", "features": features}


# ─────────────────────────────────────────────
#   MAIN
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Kobo a GeoJSON para UMap")
    parser.add_argument("csv", help="CSV exportado desde KoboToolbox")
    parser.add_argument("--fotos", "-f", metavar="CARPETA",
                        help="Carpeta con fotos exportadas de Kobo", default=None)
    args = parser.parse_args()

    if not os.path.exists(args.csv):
        print(f"Archivo no encontrado: {args.csv}")
        sys.exit(1)

    urls = {}
    if args.fotos:
        if not os.path.isdir(args.fotos):
            print(f"Carpeta no encontrada: {args.fotos}")
            sys.exit(1)
        urls = preparar_cloudinary(args.fotos)

    print(f"\nProcesando: {args.csv}")
    geojson = csv_a_geojson(args.csv, urls)

    salida = os.path.splitext(args.csv)[0] + "_umap.geojson"
    with open(salida, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    total    = len(geojson["features"])
    con_foto = sum(1 for ft in geojson["features"] if ft["properties"].get("imagen"))

    print(f"Listo. {total} puntos exportados -> {salida}")
    if args.fotos:
        print(f"   {con_foto} puntos con imagen")
    print()
    print("-" * 52)
    print("PROXIMOS PASOS EN UMAP:")
    print(f"  1. Importar datos -> subir: {os.path.basename(salida)}")
    print("  2. Plantilla de contenido emergente:  {popup}")
    print("  3. Guardar")
    print("-" * 52)


if __name__ == "__main__":
    main()
