# Scripts de Ejemplo para Windows

Este directorio contiene scripts de ejemplo para ejecutar el proyecto en Windows.
Estos scripts son específicos del entorno de desarrollo y deben adaptarse a tu configuración local.

## Scripts Disponibles

### activate_env.bat.example

Activa el entorno virtual de Python

### run_development.bat.example  

Ejecuta Odoo en modo desarrollo con el módulo CRM Social Extension

### setup_database.bat.example

Crea y configura la base de datos inicial

## Configuración

1. Copia los archivos `.example` y renómbralos sin la extensión `.example`
2. Edita las rutas para que coincidan con tu instalación de Odoo
3. Configura las variables de base de datos según tu entorno

## Ejemplo de Uso

```bash
# Activar entorno virtual
activate_env.bat

# Ejecutar en desarrollo
run_development.bat

# O crear nueva base de datos
setup_database.bat
```

## Nota

Estos scripts son específicos para Windows. Para Linux/Mac, crear scripts equivalentes en bash.
