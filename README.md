# Kobo a UMap

Herramienta para colectivas activistas que mapean con KoboToolbox y UMap.

Convierte exportaciones CSV de KoboToolbox en archivos GeoJSON listos para importar en [UMap](https://umap.openstreetmap.fr), con popups que incluyen nombre, imagen y todos los campos del formulario.

**[Ver ejemplo en el mapa](https://geojson.io/#data=data:text/x-url,https://raw.githubusercontent.com/seleneyang/de-kobo-a-umap/main/datos/ejemplo/ejemplo_resultado_umap.geojson)**

---

## Que hace este script

- Lee el CSV exportado desde KoboToolbox
- Sube las fotos a Google Drive y genera URLs publicas automaticamente
- Genera un archivo `.geojson` listo para UMap con popups de nombre e imagen
- Solo hay que poner `{popup}` en la plantilla de UMap

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

## Flujo de trabajo

Cada vez que quieran actualizar el mapa:

```
1. Exportar CSV desde Kobo
2. Exportar ZIP de fotos desde Kobo
3. Descomprimir el ZIP
4. Correr el script
5. Importar el GeoJSON en UMap
```

Los pasos 1 y 2 se hacen en la misma pantalla de Kobo. El paso 4 sube las fotos a Drive y genera el GeoJSON en un solo comando.

---

## Instalacion

```bash
git clone https://github.com/TU_USUARIO/kobo-a-umap.git
cd kobo-a-umap
```

---

## Uso

### Sin fotos

```bash
python3 kobo_a_umap.py datos.csv
```

### Con fotos (recomendado)

```bash
python3 kobo_a_umap.py datos.csv --fotos carpeta_de_fotos/
```

El script sube las fotos a Google Drive automaticamente y genera el GeoJSON con las URLs publicas. La primera vez abre el navegador para autorizar el acceso a Drive — ver `docs/guia-google-drive.md`.

### Resultado

Genera `datos_umap.geojson`. Importarlo en UMap y poner `{popup}` en la plantilla de contenido emergente.

---

## Configuracion

Abrir `kobo_a_umap.py` y ajustar la seccion `CONFIGURACION`:

```python
COLUMNA_NOMBRE = "Nombre del lugar"   # nombre interno de la columna del lugar
COLUMNA_FOTO   = "Foto del lugar"     # nombre interno de la pregunta tipo Photo
ANCHO_IMAGEN   = 300                  # ancho de imagen en el popup (px)
SEPARADOR_CSV  = ";"                  # separador del CSV exportado por Kobo
COLUMNA_LAT    = "_Ubicacion GPS_latitude"
COLUMNA_LON    = "_Ubicacion GPS_longitude"
```

Los nombres deben coincidir exactamente con los de la primera fila del CSV.

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
    └── guia-google-drive.md
```

---

## Contribuciones

Proyecto de codigo abierto creado para apoyar el trabajo de colectivas feministas y activistas. Sugerencias y mejoras bienvenidas via issues o pull requests.

