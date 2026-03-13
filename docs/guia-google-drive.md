# Configurar Google Drive para subir fotos

Esta configuracion se hace una sola vez. Despues el script sube las fotos automaticamente.

---

## Por que se necesita esto

Las fotos recopiladas con Kobo se guardan en los servidores de Kobo con acceso privado. Para que aparezcan en UMap necesitan estar en una URL publica. El script las sube automaticamente a Google Drive.

---

## Paso 1 — Crear el proyecto en Google Cloud (10 min)

1. Entrar a [console.cloud.google.com](https://console.cloud.google.com) con la cuenta de Google donde se guardaran las fotos

2. Click en el selector de proyectos (arriba a la izquierda) → **"Nuevo proyecto"**
   - Nombre: `kobo-umap`
   - Click en **"Crear"**

3. Menu izquierdo → **"APIs y servicios"** → **"Biblioteca"**

4. Buscar **"Google Drive API"** → click → **"Habilitar"**

---

## Paso 2 — Crear las credenciales

1. Menu izquierdo → **"APIs y servicios"** → **"Credenciales"**

2. Click en **"+ Crear credenciales"** → **"ID de cliente de OAuth"**

3. Si pide configurar la pantalla de consentimiento:
   - Click en **"Configurar pantalla de consentimiento"**
   - Elegir **"Externo"** → **"Crear"**
   - Nombre de la app: `kobo-umap`
   - Correo de soporte: el email propio
   - Guardar y continuar en todos los pasos siguientes
   - Al final click en **"Volver al panel"**

4. Ir al menu izquierdo → click en **"Publico"**

5. Bajar hasta la seccion **"Usuarios de prueba"** → click en **"+ Agregar usuarios"**
   - Escribir el correo de Google con el que se autorizara el script (el mismo con el que se inicio sesion en Google Cloud)
   - Click en **"Guardar"**

6. Volver a **"Credenciales"** → **"+ Crear credenciales"** → **"ID de cliente de OAuth"**

7. Tipo de aplicacion: **"Aplicacion de escritorio"**
   - Nombre: `kobo-umap-script`
   - Click en **"Crear"**

8. Click en **"Descargar JSON"**

9. Renombrar el archivo descargado a exactamente: `credentials.json`

10. Copiar ese archivo a la misma carpeta donde esta `kobo_a_umap.py`

---

## Paso 3 — Instalar las librerias

```bash
pip3 install google-auth google-auth-oauthlib google-api-python-client
```

En Windows:
```
pip install google-auth google-auth-oauthlib google-api-python-client
```

---

## Paso 4 — Primera ejecucion

La primera vez que se corre el script con `--fotos`:

1. Se abre el navegador automaticamente
2. Pide iniciar sesion con Google
3. Muestra: "kobo-umap-script quiere acceder a tu Google Drive"
4. Click en **"Continuar"**

Si Google muestra el error **"Acceso bloqueado: la app no completo el proceso de verificacion"**: significa que el correo no fue agregado como usuario de prueba en el Paso 2. Volver a Google Cloud → **Google Auth Platform** → **Publico** → **Usuarios de prueba** → agregar el correo y volver a intentar.

Si Google muestra advertencia de "app no verificada": click en **"Avanzado"** → **"Ir a kobo-umap-script"** → **"Permitir"**. Es normal para apps personales.

Despues de esto se guarda un archivo `token_google.pickle`. Las veces siguientes el script no vuelve a pedir autorizacion.

---

## Estructura de archivos necesaria

```
mi-proyecto/
├── kobo_a_umap.py       <- el script
├── credentials.json     <- descargado de Google Cloud
├── datos.csv            <- exportacion de Kobo
└── fotos/               <- fotos exportadas de Kobo (descomprimidas)
    ├── foto_001.jpg
    ├── foto_002.jpg
    └── ...
```

---

## Preguntas frecuentes

### Los datos estan seguros?
El script solo tiene permiso para subir archivos a Drive (`drive.file`). No puede leer ni modificar archivos que no haya creado el mismo.

### Que pasa si borro `token_google.pickle`?
El script pedira autorizacion de nuevo en el navegador.

### Puedo usar otra cuenta de Google?
Si. Borrar `token_google.pickle` y la proxima vez iniciar sesion con otra cuenta.
