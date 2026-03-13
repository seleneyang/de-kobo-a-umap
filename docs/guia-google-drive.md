# 🔑 Guía para conectar el script con Google Drive

Esta configuración se hace **una sola vez**. Después, el script sube las fotos automáticamente sin volver a pedirte nada.

---

## ¿Por qué necesito esto?

Cuando Kobo recopila fotos, las guarda como archivos locales en tu computadora. Para que aparezcan en UMap, deben estar en internet con una URL pública. Este script las sube automáticamente a tu Google Drive.

---

## Paso 1 — Crear el proyecto en Google Cloud (10 min)

> No te asustés con el nombre — es solo el panel donde Google te da permiso para usar tu propio Drive desde un script.

1. Entrá a [console.cloud.google.com](https://console.cloud.google.com)
   - Iniciá sesión con la cuenta de Google que usarás para guardar las fotos

2. Arriba a la izquierda, click en el selector de proyectos → **"Nuevo proyecto"**
   - Nombre: `kobo-umap` (o el que quieras)
   - Click en **"Crear"**

3. En el menú de la izquierda: **"APIs y servicios"** → **"Biblioteca"**

4. Buscá **"Google Drive API"** → click → **"Habilitar"**

---

## Paso 2 — Crear las credenciales

1. En el menú izquierdo: **"APIs y servicios"** → **"Credenciales"**

2. Click en **"+ Crear credenciales"** → **"ID de cliente de OAuth"**

3. Si te pide configurar la "Pantalla de consentimiento":
   - Click en **"Configurar pantalla de consentimiento"**
   - Elegí **"Externo"** → **"Crear"**
   - Nombre de la app: `Kobo UMap`
   - Correo de soporte: tu email
   - Scrolleá hasta abajo → **"Guardar y continuar"**
   - En los siguientes pasos ("Permisos" y "Usuarios de prueba") podés dejar todo como está y continuar
   - Al final click en **"Volver al panel"**

4. Volvé a **"Credenciales"** → **"+ Crear credenciales"** → **"ID de cliente de OAuth"**

5. Tipo de aplicación: **"Aplicación de escritorio"**
   - Nombre: `kobo-umap-script`
   - Click en **"Crear"**

6. Se abre una ventana con tus credenciales. Click en **"Descargar JSON"**

7. Renombrá el archivo descargado a exactamente: **`credentials.json`**

8. Copiá ese archivo a la misma carpeta donde está el script `kobo_a_umap.py`

---

## Paso 3 — Instalar las librerías necesarias

Abrí la terminal y corré:

```bash
pip3 install google-auth google-auth-oauthlib google-api-python-client
```

En Windows:
```
pip install google-auth google-auth-oauthlib google-api-python-client
```

---

## Paso 4 — Primera ejecución (autorización)

La primera vez que uses el script con `--fotos`, va a:

1. Abrir tu navegador automáticamente
2. Pedirte que inicies sesión con tu cuenta de Google
3. Mostrar una pantalla que dice **"kobo-umap-script quiere acceder a tu Google Drive"**
4. Click en **"Continuar"** (o **"Allow"**)

> ⚠️ Si Google muestra una advertencia de "app no verificada", click en **"Avanzado"** → **"Ir a kobo-umap-script"**. Esto es normal para apps personales.

Después de esto, se guarda un archivo `token_google.pickle` en la carpeta. Las próximas veces el script no volverá a pedir autorización.

---

## Paso 5 — Usar el script con fotos

```bash
python3 kobo_a_umap.py datos.csv --fotos carpeta_con_fotos/
```

### ¿Cómo exportar las fotos desde Kobo?

1. En KoboToolbox → tu formulario → **"Descargar datos"**
2. Exportá también los **"Archivos multimedia"** (hay una opción separada)
3. Las fotos se descargan en un ZIP — descomprimílas en una carpeta
4. Pasale esa carpeta al script con `--fotos`

---

## Resultado en Google Drive

El script crea automáticamente una carpeta llamada `fotos_mapa` en tu Drive con todas las imágenes. Esta carpeta es **pública para lectura** (cualquiera con el link puede ver las fotos, pero no puede modificarlas ni ver el resto de tu Drive).

---

## Estructura de archivos necesaria

```
mi-proyecto/
├── kobo_a_umap.py       ← el script
├── credentials.json     ← el archivo que descargaste de Google
├── datos.csv            ← tu exportación de Kobo
└── fotos/               ← carpeta con las fotos exportadas de Kobo
    ├── foto_001.jpg
    ├── foto_002.jpg
    └── ...
```

---

## Preguntas frecuentes

### ¿Mis datos están seguros?
El script solo tiene permiso para **subir archivos** a tu Drive (`drive.file`). No puede leer ni modificar archivos que no haya creado él mismo.

### ¿Qué pasa si borro el archivo `token_google.pickle`?
El script te pedirá autorizarte de nuevo en el navegador.

### ¿Puedo usar otra cuenta de Google?
Sí. Borrá el archivo `token_google.pickle` y la próxima vez podés iniciar sesión con otra cuenta.

### El script dice "app no verificada" en Google
Es normal para proyectos personales. Click en **"Avanzado"** → **"Ir a kobo-umap-script (no seguro)"** → **"Permitir"**.

---

*Si tenés problemas, revisá que `credentials.json` esté en la misma carpeta que el script.*
