# Configurar Imgur para subir fotos

Esta configuracion se hace una sola vez y toma menos de 5 minutos. No requiere tarjeta de credito ni configuraciones complejas.

---

## Paso 1 — Crear cuenta en Imgur

1. Ir a [imgur.com](https://imgur.com) y crear una cuenta gratuita (o iniciar sesion si ya tenes)

---

## Paso 2 — Obtener el Client ID

1. Ir a [api.imgur.com/oauth2/addclient](https://api.imgur.com/oauth2/addclient)
2. Llenar el formulario:
   - **Application name:** `kobo-umap`
   - **Authorization type:** seleccionar **"Anonymous usage without user authorization"**
   - **Email:** tu correo
3. Click en **"Submit"**
4. En la pantalla siguiente aparece el **Client ID** — copiarlo

---

## Paso 3 — Agregar el Client ID al script

Abrir `kobo_a_umap.py` y pegar el Client ID en esta linea:

```python
IMGUR_CLIENT_ID = "aca_va_tu_client_id"
```

---

## Listo

A partir de ahi, cada vez que se corra el script con `--fotos`, las imagenes se suben automaticamente a Imgur con URLs publicas permanentes.

El script guarda un archivo `imgur_cache.json` en la carpeta para no volver a subir fotos que ya fueron subidas antes.

---

## Preguntas frecuentes

### Las imagenes son publicas?
Si. Cualquier persona con el link puede ver las fotos. No aparecen en busquedas publicas de Imgur a menos que se publiquen explicitamente.

### Hay limite de fotos?
La cuenta gratuita permite subir hasta 50 imagenes por hora. Para un proyecto de mapeo colectivo es mas que suficiente.

### Que pasa si borro `imgur_cache.json`?
El script volvera a subir todas las fotos y generara URLs nuevas. Las fotos anteriores en Imgur quedan huerfanas pero no se borran.
