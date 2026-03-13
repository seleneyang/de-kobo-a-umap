#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║         KOBO → UMAP  |  Convertidor de datos                ║
║  Para colectivas que mapean con KoboToolbox + UMap           ║
╚══════════════════════════════════════════════════════════════╝

USO BÁSICO (sin fotos):
    python3 kobo_a_umap.py datos.csv

USO CON FOTOS (sube imágenes a Google Drive automáticamente):
    python3 kobo_a_umap.py datos.csv --fotos carpeta_con_fotos/

RESULTADO:
    Un archivo  datos_umap.geojson  listo para importar en UMap.

INSTRUCCIONES UMAP:
    1. En tu mapa de UMap, click en "Importar datos"
    2. Sube el archivo .geojson generado
    3. En "Plantilla de contenido emergente" escribe solo:  {popup}
    4. ¡Listo!

PRIMERA VEZ CON FOTOS:
    Necesitás el archivo credentials.json de Google.
    Seguí la guía en docs/guia-google-drive.md
"""

import csv
import json
import sys
import os
import argparse
import pickle

# ─────────────────────────────────────────────
#   ⚙️  CONFIGURACIÓN  — ajusta estos valores
# ─────────────────────────────────────────────

COLUMNA_NOMBRE    = "Nombre del lugar"
COLUMNA_FOTO      = "Foto del lugar"
COLUMNA_FOTO_URL  = "Foto del lugar_URL"   # URL directa que exporta Kobo automáticamente
ANCHO_IMAGEN      = 300
CARPETA_DRIVE     = "fotos_mapa"
COLUMNA_LAT       = "_Ubicación GPS_latitude"
COLUMNA_LON       = "_Ubicación GPS_longitude"
SEPARADOR_CSV     = ";"                    # Kobo exporta con ; en lugar de ,

COLUMNAS_EXCLUIR = {
    "_id", "_uuid", "_submission_time", "_validation_status",
    "_notes", "_status", "_submitted_by", "__version__", "_tags", "_index",
    # Metadatos de ubicación
    "_Ubicación del establecimiento_altitude",
    "_Ubicación del establecimiento_precision",
    "Ubicación del establecimiento",
    "_Ubicación GPS_altitude",
    "_Ubicación GPS_precision",
    "Ubicación GPS",
    # Metadatos de tiempo y sistema
    "start", "end", "meta/rootUuid",
    # Campos de formularios anteriores
    "Muchas gracias! Acá termina este registro.",
    "Muchas gracias!!",
}

SCOPES         = ["https://www.googleapis.com/auth/drive.file"]
TOKEN_FILE     = "token_google.pickle"
CREDENTIALS_FILE = "credentials.json"


# ─────────────────────────────────────────────
#   📸  GOOGLE DRIVE
# ─────────────────────────────────────────────

def autenticar_google():
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
    except ImportError:
        print("\n❌ Faltan las librerías de Google. Instalálas con:")
        print("   pip3 install google-auth google-auth-oauthlib google-api-python-client")
        sys.exit(1)

    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as t:
            creds = pickle.load(t)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"\n❌ No se encontró '{CREDENTIALS_FILE}'.")
                print("   Seguí la guía en docs/guia-google-drive.md")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as t:
            pickle.dump(creds, t)
        print("✅ Sesión de Google guardada.")

    return creds


def obtener_o_crear_carpeta(service, nombre):
    query = (f"name='{nombre}' and "
             "mimeType='application/vnd.google-apps.folder' and trashed=false")
    res = service.files().list(q=query, fields="files(id)").execute().get("files", [])

    if res:
        print(f"   📁 Carpeta '{nombre}' encontrada en Drive.")
        return res[0]["id"]

    carpeta = service.files().create(
        body={"name": nombre, "mimeType": "application/vnd.google-apps.folder"},
        fields="id"
    ).execute()
    fid = carpeta["id"]
    service.permissions().create(
        fileId=fid, body={"type": "anyone", "role": "reader"}
    ).execute()
    print(f"   📁 Carpeta '{nombre}' creada en Drive (pública).")
    return fid


def subir_foto(service, ruta_local, carpeta_id):
    from googleapiclient.http import MediaFileUpload

    nombre = os.path.basename(ruta_local)
    query  = f"name='{nombre}' and '{carpeta_id}' in parents and trashed=false"
    exist  = service.files().list(q=query, fields="files(id)").execute().get("files", [])

    if exist:
        fid = exist[0]["id"]
    else:
        ext   = os.path.splitext(nombre)[1].lower()
        mimes = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                 ".png": "image/png",  ".webp": "image/webp"}
        mime  = mimes.get(ext, "image/jpeg")
        arch  = service.files().create(
            body={"name": nombre, "parents": [carpeta_id]},
            media_body=MediaFileUpload(ruta_local, mimetype=mime),
            fields="id"
        ).execute()
        fid = arch["id"]
        service.permissions().create(
            fileId=fid, body={"type": "anyone", "role": "reader"}
        ).execute()

    return f"https://drive.google.com/uc?export=view&id={fid}"


def preparar_drive(carpeta_local):
    try:
        from googleapiclient.discovery import build
    except ImportError:
        print("\n❌ Faltan las librerías de Google.")
        sys.exit(1)

    print("\n🔐 Conectando con Google Drive...")
    service    = build("drive", "v3", credentials=autenticar_google())
    carpeta_id = obtener_o_crear_carpeta(service, CARPETA_DRIVE)

    exts  = {".jpg", ".jpeg", ".png", ".webp"}
    fotos = [f for f in os.listdir(carpeta_local)
             if os.path.splitext(f)[1].lower() in exts]

    if not fotos:
        print(f"   ⚠️  Sin imágenes en '{carpeta_local}'")
        return {}

    print(f"\n📸 Subiendo {len(fotos)} fotos...")
    urls = {}
    for i, nombre in enumerate(fotos, 1):
        url = subir_foto(service, os.path.join(carpeta_local, nombre), carpeta_id)
        urls[nombre] = url
        print(f"   [{i}/{len(fotos)}] {nombre} → ok")

    print("✅ Fotos listas.\n")
    return urls


# ─────────────────────────────────────────────
#   🗺️  CONVERSIÓN A GEOJSON
# ─────────────────────────────────────────────

def csv_a_geojson(ruta_csv, urls_fotos=None):
    if urls_fotos is None:
        urls_fotos = {}

    features = []

    with open(ruta_csv, newline="", encoding="utf-8-sig") as f:
        reader  = csv.DictReader(f, delimiter=SEPARADOR_CSV)
        columnas = reader.fieldnames or []

        cols_popup = [
            c for c in columnas
            if c not in COLUMNAS_EXCLUIR
            and c not in {COLUMNA_NOMBRE, COLUMNA_FOTO, COLUMNA_FOTO_URL, COLUMNA_LAT, COLUMNA_LON}
        ]

        for row in reader:
            try:
                lat = float(row.get(COLUMNA_LAT, "").strip())
                lon = float(row.get(COLUMNA_LON, "").strip())
            except (ValueError, TypeError):
                print(f"  ⚠️  Sin coordenadas: {row.get(COLUMNA_NOMBRE, '?').strip()}")
                continue

            nombre   = row.get(COLUMNA_NOMBRE, "Sin nombre").strip()
            # Primero URL directa de Kobo, luego fallback a Google Drive
            url_foto = row.get(COLUMNA_FOTO_URL, "").strip()
            if not url_foto:
                nom_foto = row.get(COLUMNA_FOTO, "").strip()
                url_foto = urls_fotos.get(nom_foto, "")

            # Popup en Markdown
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
#   🚀  MAIN
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Kobo → GeoJSON para UMap")
    parser.add_argument("csv", help="CSV exportado desde KoboToolbox")
    parser.add_argument("--fotos", "-f", metavar="CARPETA",
                        help="Carpeta con fotos exportadas de Kobo", default=None)
    args = parser.parse_args()

    if not os.path.exists(args.csv):
        print(f"❌ Archivo no encontrado: {args.csv}")
        sys.exit(1)

    urls = {}
    if args.fotos:
        if not os.path.isdir(args.fotos):
            print(f"❌ Carpeta no encontrada: {args.fotos}")
            sys.exit(1)
        urls = preparar_drive(args.fotos)

    print(f"\n📂 Procesando: {args.csv}")
    geojson = csv_a_geojson(args.csv, urls)

    salida = os.path.splitext(args.csv)[0] + "_umap.geojson"
    with open(salida, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    total     = len(geojson["features"])
    con_foto  = sum(1 for ft in geojson["features"] if ft["properties"].get("imagen"))

    print(f"✅ {total} puntos exportados → {salida}")
    if args.fotos:
        print(f"   📸 {con_foto} puntos con imagen")
    print()
    print("─" * 52)
    print("PRÓXIMOS PASOS EN UMAP:")
    print(f"  1. Importar datos → subir: {os.path.basename(salida)}")
    print("  2. Plantilla de contenido emergente:  {popup}")
    print("  3. Guardar — ¡listo!")
    print("─" * 52)


if __name__ == "__main__":
    main()
