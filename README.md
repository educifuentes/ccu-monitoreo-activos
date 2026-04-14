# Dashboard Monitoreo de Activos CCU

**Cliente:** Go to Market

Aplicación de monitoreo y validación de activos para CCU. Permite cruzar la información de censos, validar las bases de datos y realizar el seguimiento de los diferentes activos y métricas clave.

## Features

- **Reportes:** Dashboard general, vistas detalladas por clientes y reportes analíticos.
- **Herramientas:**
  - Explorador interactivo de tablas
  - Módulo de validación de datos
  - Documentación

## Deploy

Para publicar nuevos cambios ejecutar:

```bash
./scripts/release.sh
```

## Scripts

- **Generar tablas para Google Sheets:** `python scripts/_export_marts_to_csv.py`
- **Actualizar variables de entorno:** `./scripts/update_cloud_run_secrets.sh`

## Links

- [Ver Proyecto en Google Cloud Console (Cloud Run)](https://console.cloud.google.com/run?project=consulting-data-studio)
- [Fuente de Datos en Google Sheet compartido](https://docs.google.com/spreadsheets/d/11JgW2Z9cFrHvNFw21-zlvylTHHo5tvizJeA9oxHcDHU/edit?gid=0#gid=0)
