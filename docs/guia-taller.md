# Guía para el taller — Kobo → UMap

Esta guía está pensada para usarse durante el taller con la colectiva. Podés seguirla paso a paso con las compañeras.

---

## Antes del taller — checklist

- [ ] Todas tienen Python 3 instalado (`python3 --version` en la terminal)
- [ ] Todas tienen acceso a su formulario de KoboToolbox
- [ ] Se creó un mapa en UMap para practicar
- [ ] Se descargó este repositorio en las computadoras

---

## Parte 1 — Exportar datos desde KoboToolbox (10 min)

1. Entrá a [kobotoolbox.org](https://kobotoolbox.org) con tu cuenta
2. Hacé click en tu formulario
3. En la barra superior, click en **"Descargar datos"** (ícono de nube)
4. Configurá la exportación:
   - **Formato:** CSV
   - **Exportar:** Todos los datos
   - Activá **"Usar etiquetas en lugar de nombres XML"**
5. Click en **"Exportar"** y luego **"Descargar"**

> 💡 **Tip:** El archivo descargado va a tener un nombre largo con la fecha. Podés renombrarlo a algo más corto como `datos.csv`.

---

## Parte 2 — Configurar el script (15 min)

Abrí el archivo `kobo_a_umap.py` con cualquier editor de texto (Bloc de notas, TextEdit, VSCode, etc.).

Buscá la sección que dice `CONFIGURACIÓN` y ajustá estas líneas:

### ¿Cómo sé el nombre exacto de mis columnas?

Abrí el CSV con Excel o Google Sheets y mirá la primera fila — esos son los nombres de columnas.

```python
# Cambiá esto por el nombre exacto de tu columna de nombre
COLUMNA_NOMBRE = "Nombre del establecimiento"

# Cambiá esto por el nombre de tu pregunta tipo "foto" en Kobo
COLUMNA_FOTO = "foto_establecimiento"

# Si tus fotos están en un servidor propio, poné la URL base aquí
# Si no tenés fotos todavía, dejalo vacío: ""
BASE_URL_FOTOS = ""

# Ancho de la imagen en el popup (en píxeles)
ANCHO_IMAGEN = 300
```

> **Importante:** Los nombres de columnas deben ser **exactamente** iguales, incluyendo mayúsculas, minúsculas y espacios.

---

## Parte 3 — Correr el script (5 min)

### En Windows

1. Abrí la carpeta donde está el script
2. En la barra de direcciones del explorador, escribí `cmd` y presioná Enter
3. En la ventana negra que aparece, escribí:

```
python kobo_a_umap.py nombre_de_tu_archivo.csv
```

### En Mac / Linux

1. Abrí la Terminal
2. Navegá hasta la carpeta con `cd`:

```bash
cd Descargas/kobo-a-umap
```

3. Corré el script:

```bash
python3 kobo_a_umap.py nombre_de_tu_archivo.csv
```

### ¿Qué debería ver?

```
Procesando: datos.csv
¡Listo! 71 puntos exportados a: datos_umap.geojson

──────────────────────────────────────────────────
PRÓXIMOS PASOS EN UMAP:
  1. Abre tu mapa → click en 'Importar datos'
  2. Sube el archivo: datos_umap.geojson
  3. En 'Plantilla de contenido emergente' escribe:  {popup}
  4. Guarda y ¡ya aparece el popup con nombre e imagen!
──────────────────────────────────────────────────
```

---

## Parte 4 — Importar en UMap (10 min)

1. Abrí tu mapa en [umap.openstreetmap.fr](https://umap.openstreetmap.fr)
2. Hacé click en el ícono de **lápiz** para editar
3. En el panel lateral, click en **"Importar datos"** (flecha hacia arriba ↑)
4. Arrastrá o seleccioná el archivo `.geojson` generado
5. Formato: **GeoJSON** (se detecta automáticamente)
6. Click en **"Importar"**

### Activar el popup automático

1. En el panel lateral, click en **"Propiedades del mapa"** (ícono de engranaje)
2. Buscá **"Plantilla de contenido emergente"**
3. Escribí exactamente: `{popup}`
4. Guardá

¡Los marcadores ya deberían mostrar el popup con toda la información!

---

## Problemas frecuentes

### "No se encontró el archivo"
Verificá que el nombre del CSV que escribiste en el comando sea exactamente igual al nombre del archivo, incluyendo la extensión `.csv`.

### "Fila sin coordenadas válidas, se omite"
Algún registro en Kobo se guardó sin ubicación GPS. Esto es normal — el script lo avisa y continúa con los demás.

### El popup aparece vacío
Verificá que en UMap escribiste exactamente `{popup}` (con llaves, en minúsculas) en la plantilla de contenido emergente.

### Las imágenes no aparecen
- Verificá que `COLUMNA_FOTO` tiene el nombre exacto de tu columna en el CSV
- Las imágenes deben ser URLs públicas accesibles desde internet
- Verificá que `BASE_URL_FOTOS` está configurada correctamente si usás rutas relativas

---

## Cómo agregar una pregunta de foto en Kobo

Para que el script pueda mostrar imágenes:

1. En KoboToolbox, abrí el editor de tu formulario
2. Hacé click en **"+ Agregar pregunta"**
3. Seleccioná el tipo **"Photo"** (Foto)
4. Dale un nombre simple, como `foto_establecimiento`
5. Guardá el formulario

Cuando las activistas recopilen datos, podrán tomar una foto del lugar directamente desde la app de Kobo.

---

## Recursos útiles

- [KoboToolbox — Documentación](https://support.kobotoolbox.org)
- [UMap — Ayuda](https://umap.openstreetmap.fr/es/help/)
- [Instalar Python](https://www.python.org/downloads/)

---

*Guía creada para el taller de mapeo colectivo.*
