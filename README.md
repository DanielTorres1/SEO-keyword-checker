# Analizador SEO con PageSpeed Insights

Script de Python que analiza elementos SEO de páginas web y genera reportes en Excel con formato condicional.

## 📋 Características

- ✅ Análisis de Keywords en:
  - Título de la página
  - Meta descripción
  - Encabezados H1
  - Texto alternativo de imágenes
- ✅ Validación de URLs amigables
- ✅ Métricas de PageSpeed Insights (opcional):
  - Accesibilidad (Mobile/Desktop)
  - Rendimiento (Mobile/Desktop)
- ✅ Reporte Excel con colores (verde = cumple, rojo = no cumple)

## 🚀 Instalación

### 1. Instalar dependencias

```bash
git cloe https://github.com/DanielTorres1/SEO-keyword-checker
cd SEO-keyword-checker
python3 -m venv venv
source venv/bin/activate
pip install requests beautifulsoup4 openpyxl selenium webdriver-manager python-dotenv
```

### 2. Configurar API Key (Opcional pero Recomendado)

Crea un archivo `.env` en la raíz del proyecto:

```bash
API_KEY=tu_api_key_aqui
```

**Ventajas de usar .env:**
- No necesitas pasar `--api-key` cada vez que ejecutas el script
- La API key no aparece en el historial de comandos
- El archivo `.env` está en `.gitignore` para evitar subirlo a GitHub

## 💡 Uso

### Análisis completo (con PageSpeed)
```bash
python seo_analyzer.py
```
> Si configuraste `.env` con tu API key, se usará automáticamente.

### Solo análisis SEO (sin PageSpeed, más rápido)
```bash
python seo_analyzer.py --no-pagespeed
```

### Con API key en línea de comandos (sobrescribe .env)
```bash
python seo_analyzer.py --api-key TU_API_KEY
```

### Archivo de configuración personalizado
```bash
python seo_analyzer.py --config-file mi_config.json
```

### Combinando opciones
```bash
python seo_analyzer.py --config-file sites.json --api-key TU_API_KEY
```

## 🔑 Obtener API Key de Google (Gratis)

La API de PageSpeed Insights tiene límites de tasa sin API key (muy pocas consultas por minuto). Para analizar múltiples URLs:

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un proyecto nuevo (o usa uno existente)
3. Habilita "PageSpeed Insights API"
4. Ve a "Credenciales" → "Crear credenciales" → "Clave de API"
5. Copia la API key generada
6. Úsala con: `--api-key TU_API_KEY`

**Nota:** La API es gratuita con límites generosos (25,000 consultas/día).

## 📁 Formato del archivo site.json

**Formato con múltiples keywords:**
```json
[
  {
    "URL": "https://ejemplo.com/",
    "keywords": ["palabra clave 1", "palabra clave 2", "palabra clave 3"]
  },
  {
    "URL": "https://ejemplo.com/pagina2",
    "keywords": ["otra keyword"]
  }
]
```

**Formato con una sola keyword:**
```json
[
  {
    "URL": "https://ejemplo.com/",
    "Keyword": "palabra clave principal"
  }
]
```

## 📊 Resultado

El script genera `seo_report_YYYY-MM-DD.xlsx` con:

| Elemento | Color | Significado |
|----------|-------|-------------|
| 🟢 SÍ | Verde | Keyword encontrada / Criterio cumplido |
| 🔴 NO | Rojo | Keyword NO encontrada / Criterio NO cumplido |
| 🟢 3 de 5 | Verde | Más del 50% de imágenes con keyword en alt text |
| 🔴 1 de 5 | Rojo | 50% o menos de imágenes con keyword en alt text |
| 🟢 90-100 | Verde | PageSpeed: Excelente |
| 🟡 50-89 | Amarillo | PageSpeed: Necesita mejora |
| 🔴 0-49 | Rojo | PageSpeed: Malo |
| N/A | - | PageSpeed no disponible (desactivado o error) |

### Columnas del reporte:
- URL
- Keyword
- Título + ✓ Keyword en Título
- Meta Descripción + ✓ Keyword en Meta
- H1 + ✓ Keyword en H1
- Alt Text Imágenes + Keyword en Alt Text (formato: "X de Y")
- ✓ URL Amigable
- Accesibilidad(Mobile)
- PageSpeed(Mobile)
- Accesibilidad(Web)
- PageSpeed(Web)

## ⚠️ Limitaciones

**Sin API Key:**
- La API de PageSpeed tiene límites muy estrictos (~1-2 consultas por minuto)
- El script añade pausas de 3 segundos entre requests
- Para más de 2-3 URLs, se recomienda usar una API key

**Con API Key:**
- Límite de 25,000 consultas/día (gratis)
- Pausas de 1 segundo entre requests
- Mucho más rápido y confiable

## 🛠️ Opciones de línea de comandos

```
usage: seo_analyzer.py [-h] [--config-file CONFIG_FILE] [--no-pagespeed] [--api-key API_KEY]

optional arguments:
  -h, --help            Muestra este mensaje de ayuda
  --config-file CONFIG_FILE
                        Archivo de configuración JSON (default: site.config)
  --no-pagespeed        Desactivar análisis de PageSpeed Insights (más rápido)
  --api-key API_KEY     API key de Google para PageSpeed Insights
```

## 📝 Ejemplos

```bash
# Análisis rápido sin PageSpeed
./venv/bin/python seo_analyzer.py --no-pagespeed

# Con API key para análisis completo
./venv/bin/python seo_analyzer.py --api-key AIzaSy...

# Archivo personalizado
./venv/bin/python seo_analyzer.py --config-file sitios_produccion.json

# Archivo personalizado con API key
./venv/bin/python seo_analyzer.py --config-file sitios_produccion.json --api-key AIzaSy...
```
