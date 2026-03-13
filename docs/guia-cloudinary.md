# Configurar Cloudinary para subir fotos

Esta configuracion se hace una sola vez y toma menos de 5 minutos.

---

## Paso 1 — Crear cuenta en Cloudinary

1. Ir a [cloudinary.com](https://cloudinary.com)
2. Click en **"Sign up for free"**
3. Llenar el formulario y confirmar el correo

---

## Paso 2 — Obtener las credenciales

1. Iniciar sesion en Cloudinary
2. Ir a **Settings** → **API Keys**
3. Anotar estos tres datos:
   - **Cloud name** (aparece arriba, ejemplo: `dpcw1ueng`)
   - **API Key** (columna API Key de la fila "Root")
   - **API Secret** (click en los asteriscos de la fila "Root" para revelarlo)

---

## Paso 3 — Agregar las credenciales al script

Abrir `kobo_a_umap.py` y completar estas lineas:

```python
CLOUDINARY_CLOUD_NAME = "tu_cloud_name"
CLOUDINARY_API_KEY    = "tu_api_key"
CLOUDINARY_API_SECRET = "tu_api_secret"
```

---

## Importante — no subir el API Secret al repo

El archivo `kobo_a_umap.py` con el API Secret NO debe subirse a GitHub. El `.gitignore` ya esta configurado para recordarlo, pero la responsabilidad es de cada usuaria.

Una opcion segura es mantener dos versiones del script:
- Una sin el secret para el repo
- Una con el secret solo en la computadora local

---

## Como funciona el cache

El script guarda un archivo `cloudinary_cache.json` con las URLs de las fotos ya subidas. La proxima vez que se corra, reutiliza esas URLs sin volver a subir las fotos. Solo sube las nuevas.

---

## Preguntas frecuentes

### Las imagenes son publicas?
Si. Cloudinary sirve las imagenes con URLs publicas permanentes.

### Hay limite de fotos?
El plan gratuito incluye 25 GB de almacenamiento y 25 GB de transferencia mensual. Para un proyecto de mapeo colectivo es mas que suficiente.

### Que pasa si borro `cloudinary_cache.json`?
El script volvera a subir todas las fotos. Las anteriores en Cloudinary quedan pero sin referencia local.
