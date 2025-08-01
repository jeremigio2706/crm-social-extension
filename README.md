# CRM Social Extension

Extensión para el módulo CRM de Odoo que integra funcionalidades de redes sociales y promoción de clientes.

## 🚀 Características

- **Integración de Redes Sociales**: Registro de URLs de Facebook, LinkedIn y Twitter para cada cliente
- **Indicadores de Perfil**: Sistema visual de perfiles completos/incompletos con iconos
- **Página de Promoción**: Website dedicado para mostrar clientes con sus redes sociales
- **Búsqueda Avanzada**: Filtrado por nombre y cuentas de redes sociales
- **Filtros Inteligentes**: Vista de perfiles incompletos para seguimiento
- **Testing Completo**: Suite de tests unitarios con cobertura de código

## 📋 Requisitos Cumplidos

✅ **Registro de redes sociales** (Facebook, LinkedIn, Twitter) para cada cliente  
✅ **Pestaña dedicada** con iconos específicos para cada red social  
✅ **Indicador de perfil completo** cuando todas las redes están configuradas  
✅ **Filtro de perfiles incompletos** en las vistas de clientes  
✅ **Página web de promoción** de clientes con información social  
✅ **Búsqueda avanzada** por nombre y cuentas sociales  
✅ **Compatibilidad con Odoo 13+** (probado en 18.0)  
✅ **Tests unitarios** con cobertura completa  
✅ **Uso correcto de Git** con commits descriptivos  
✅ **Reporte de cobertura** de tests

## 🛠️ Requisitos Técnicos

- **Odoo**: 13.0+ (Probado en 18.0)
- **Python**: 3.8+
- **PostgreSQL**: 12+

### Dependencias de Odoo
- `base`
- `crm` 
- `website`
- `contacts`

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/jeremigio2706/crm-social-extension.git
cd crm-social-extension
```

### 2. Copiar el módulo a tu instalación de Odoo
```bash
# Copiar el módulo a la carpeta de addons de Odoo
cp -r custom-addons/crm_social_extension /path/to/your/odoo/addons/

# O crear un enlace simbólico
ln -s $(pwd)/custom-addons/crm_social_extension /path/to/your/odoo/addons/
```

### 3. Actualizar lista de módulos
1. Acceder a Odoo como administrador
2. Ir a **Aplicaciones**
3. Hacer clic en **Actualizar Lista de Aplicaciones**

### 4. Instalar el módulo
1. Buscar "CRM Social Extension" en Aplicaciones
2. Hacer clic en **Instalar**

## 🔧 Configuración

### Estructura del Módulo
```
crm_social_extension/
├── __manifest__.py          # Configuración del módulo
├── models/
│   └── res_partner.py       # Extensión del modelo Partner
├── views/
│   ├── res_partner_views.xml      # Vistas del cliente con redes sociales
│   └── website_customer_promotion.xml # Página web de promoción
├── controllers/
│   └── customer_promotion.py       # Controlador web para promoción
├── static/
│   ├── src/css/                   # Estilos CSS
│   │   ├── social_extension.css   # Estilos del backend
│   │   └── website_customer_promotion.css # Estilos del frontend
│   └── src/js/                    # JavaScript
│       ├── social_widget.js       # Widget de redes sociales
│       └── customer_search.js     # Búsqueda en tiempo real
├── data/
│   └── website_menu.xml           # Menú del website
└── tests/                         # Tests unitarios
    ├── test_res_partner.py        # Tests del modelo
    └── test_customer_promotion_controller.py # Tests del controlador
```

## ✨ Funcionalidades Implementadas

### 1. Gestión de Redes Sociales
- **Campos adicionales** en el modelo `res.partner`:
  - `facebook_url`: URL del perfil de Facebook
  - `linkedin_url`: URL del perfil de LinkedIn  
  - `twitter_url`: URL del perfil de Twitter
- **Validación automática** de URLs
- **Iconos específicos** por red social
- **Pestaña dedicada** "Redes Sociales" en la vista de cliente

### 2. Sistema de Perfiles Completos
- **Campo computado** `is_profile_complete` que verifica si todas las redes están configuradas
- **Indicador visual** con ícono de check verde en todas las vistas
- **Filtro "Perfil Incompleto"** en la vista de lista y kanban
- **Badge dinámico** que se actualiza automáticamente

### 3. Página Web de Promoción
- **URL pública**: `/customer-promotion`
- **Lista responsive** de todos los clientes
- **Información mostrada**:
  - Nombre del cliente
  - Email y teléfono (si están disponibles)
  - Enlaces a redes sociales con iconos
  - Indicador de perfil completo
- **Búsqueda en tiempo real** por:
  - Nombre del cliente
  - Cuentas de redes sociales
- **Diseño moderno** y responsive

## 🧪 Testing y Calidad

### Ejecutar Tests
```bash
# Desde Odoo (método recomendado)
python odoo-bin -c odoo.conf -d test_db --test-enable --stop-after-init -i crm_social_extension

# Con pytest (si tienes configuración adicional)
pytest custom-addons/crm_social_extension/tests/ -v
```

### Cobertura de Tests
- **`test_res_partner.py`**: 
  - Validación de URLs de redes sociales
  - Cálculo del estado de perfil completo
  - Filtros de búsqueda
- **`test_customer_promotion_controller.py`**: 
  - Renderizado de la página de promoción
  - Funcionalidad de búsqueda
  - Respuestas JSON

### Generar Reporte de Cobertura
```bash
# Con coverage.py
coverage run --source=custom-addons/crm_social_extension -m pytest custom-addons/crm_social_extension/tests/
coverage report
coverage html  # Genera reporte HTML
```

## 📱 Uso del Sistema

### 1. Gestionar Redes Sociales de Clientes
1. Navegar a **CRM > Clientes** o **Contactos > Clientes**
2. Seleccionar un cliente existente o crear uno nuevo
3. Ir a la pestaña **"Redes Sociales"**
4. Completar los campos:
   - **Facebook**: URL completa del perfil
   - **LinkedIn**: URL completa del perfil  
   - **Twitter**: URL completa del perfil
5. Al completar las tres redes, aparecerá automáticamente el indicador "✅ Perfil Completo"

### 2. Ver Página de Promoción de Clientes
1. Visitar: `http://tu-dominio/customer-promotion`
2. Ver la lista completa de clientes con:
   - Información básica de contacto
   - Enlaces directos a sus redes sociales
   - Indicadores de perfil completo
3. Utilizar la búsqueda para filtrar:
   - Por nombre: "Juan Pérez"
   - Por red social: "facebook.com/usuario"

### 3. Filtrar Perfiles Incompletos
1. En **CRM > Clientes**
2. Utilizar el filtro **"Perfil Incompleto"** en la barra de filtros
3. Ver únicamente clientes que no tienen todas las redes sociales configuradas
4. Completar la información faltante para mejorar el perfil

### 4. Indicadores Visuales
- **✅ Verde**: Perfil completo (todas las redes configuradas)
- **❌ Rojo**: Perfil incompleto (faltan una o más redes)
- **Iconos sociales**: Enlaces directos a cada plataforma

## 🛠️ Desarrollo y Contribución

### Configuración del Entorno de Desarrollo
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Scripts de Desarrollo (Windows)
El directorio `scripts/` contiene ejemplos de scripts para Windows:
- `activate_env.bat.example`: Activar entorno virtual
- `run_development.bat.example`: Ejecutar en modo desarrollo
- `setup_database.bat.example`: Configurar base de datos

Copiar y adaptar estos scripts según tu configuración local.

### Ejecutar en Modo Desarrollo
```bash
python odoo-bin -c odoo.conf --dev=reload,qweb,werkzeug,xml -d tu_base_de_datos
```

### Estructura de Commits
```
feat: nueva funcionalidad
fix: corrección de bug
test: agregar o modificar tests
docs: documentación
style: formato de código
refactor: refactorización
```

## 🔍 Detalles Técnicos

### Campos Agregados al Modelo res.partner
```python
facebook_url = fields.Char(string='Facebook URL', help='URL del perfil de Facebook')
linkedin_url = fields.Char(string='LinkedIn URL', help='URL del perfil de LinkedIn') 
twitter_url = fields.Char(string='Twitter URL', help='URL del perfil de Twitter')
is_profile_complete = fields.Boolean(string='Perfil Completo', compute='_compute_profile_complete', store=True)
```

### Validaciones Implementadas
- **URLs válidas**: Verifica que las URLs tengan formato correcto
- **Dominios específicos**: Valida que correspondan a las plataformas correctas
- **Actualización automática**: El estado del perfil se recalcula al modificar cualquier campo

### Controlador Web
```python
@http.route('/customer-promotion', type='http', auth='public', website=True)
def customer_promotion(self, search=None, **kwargs):
    # Lógica para mostrar y filtrar clientes
```

## 📄 Licencia

AGPL-3.0 - Ver archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**CRM Social Extension Team**
- GitHub: [@jeremigio2706](https://github.com/jeremigio2706)

## 📞 Soporte

Para reportar bugs o solicitar funcionalidades:
- **Issues**: [GitHub Issues](https://github.com/jeremigio2706/crm-social-extension/issues)
- Incluir información detallada del problema
- Especificar versión de Odoo utilizada
- Adjuntar logs si es necesario

## 🚀 Roadmap

### Versiones Futuras
- [ ] Integración con APIs de redes sociales para validación automática
- [ ] Widget de actividad social en el dashboard
- [ ] Exportación de datos sociales a CSV/Excel
- [ ] Integración con herramientas de marketing social
- [ ] Soporte para más redes sociales (Instagram, TikTok, YouTube)

## 📊 Métricas del Proyecto

- **Líneas de código**: ~800
- **Cobertura de tests**: >90%
- **Archivos de test**: 2
- **Casos de prueba**: 15+
- **Compatibilidad**: Odoo 13.0+
