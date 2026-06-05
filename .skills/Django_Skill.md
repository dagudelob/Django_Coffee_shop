---
name: django-best-practices
description: Core guidelines and best practices for developing Django applications. Covers architecture, models, ORM optimization, security, and project structure.
license: MIT
---

# Django Best Practices Skill

Este documento sirve como guía y "skill" para seguir las mejores prácticas de desarrollo en proyectos con Django.

## 1. Estructura del Proyecto
- **Apps pequeñas y enfocadas:** Divide tu proyecto en aplicaciones (`apps`) con una responsabilidad única. Si una app hace muchas cosas, divídela.
- **Configuración (Settings):** Usa variables de entorno (por ejemplo, con `django-environ` o `python-dotenv`) para manejar credenciales, claves secretas (`SECRET_KEY`), y configuraciones de base de datos.
- **Evita hardcodear rutas:** Usa `pathlib.Path` o `os.path` en conjunto con `BASE_DIR`.

## 2. Modelos (Models)
- **Fat Models, Skinny Views:** La lógica de negocio y validaciones de datos deben vivir en los modelos (o en servicios separados), no en las vistas.
- **Usa Choices:** Si un campo tiene opciones limitadas, usa `choices` (o `models.TextChoices` / `models.IntegerChoices` en versiones recientes de Django).
- **Método `__str__`:** Siempre define el método `__str__` en tus modelos para que sean fáciles de identificar en el panel de administración de Django y en la consola.
- **Índices y Constraints:** Usa `db_index=True` en campos por los que buscas frecuentemente, y usa `UniqueConstraint` para evitar datos duplicados a nivel de base de datos.

## 3. Consultas a la Base de Datos (ORM)
- **Evita el problema N+1:** Usa `select_related()` (para relaciones Foreign Key) y `prefetch_related()` (para relaciones Many-to-Many o Inversas) cuando vayas a iterar sobre objetos relacionados.
- **Solo trae lo que necesitas:** Usa `.values()`, `.values_list()`, o `.only()` / `.defer()` si solo necesitas un par de campos y quieres optimizar la consulta.

## 4. Vistas (Views)
- **Class-Based Views (CBVs) vs Function-Based Views (FBVs):** 
  - Usa **CBVs** (como `ListView`, `DetailView`, `CreateView`) para operaciones estándar (CRUD) porque ahorran mucho código y son reutilizables.
  - Usa **FBVs** cuando la vista tenga una lógica de flujo muy compleja o personalizada que no se ajuste a las vistas genéricas.
- **Mantén las vistas limpias:** La vista solo debería recibir la request, llamar a la lógica de negocio (modelo/servicio), y devolver la response.

## 5. URLs y Enrutamiento
- **Nombres de URLs:** Siempre asigna un `name='mi_vista'` a tus paths.
- **Namespaces:** Usa el atributo `app_name` dentro de `urls.py` de cada app para crear un namespace (ej. `firstapp:car_list`).
- **No uses rutas hardcodeadas en HTML:** Usa siempre la etiqueta `{% url 'nombre_vista' %}` en tus templates en lugar de escribir la ruta manual `/ruta/`.

## 6. Templates
- **Herencia de Templates:** Crea un `base.html` que contenga la estructura principal (navbar, footer, imports de CSS/JS) y usa `{% extends 'base.html' %}` y bloques `{% block content %}` en las plantillas hijas.
- **Incluir componentes:** Usa `{% include 'partials/_component.html' %}` para código HTML repetitivo (como tarjetas o botones).

## 7. Seguridad
- **DEBUG = False en producción:** Nunca despliegues con DEBUG=True.
- **Protección CSRF:** Asegúrate de incluir `{% csrf_token %}` en todos los formularios de métodos POST.
- **Nunca confíes en el input del usuario:** Valida siempre los datos recibidos (con ModelForms, Forms o serializers). Django ya protege contra inyecciones SQL si usas su ORM.

## 8. Entorno Virtual y Dependencias
- Mantén siempre un archivo `requirements.txt` o usa `pyproject.toml` (como con `uv`, `poetry`, o `pip-tools`) para rastrear las dependencias.
- El directorio del entorno virtual (`.venv`) siempre debe estar en tu `.gitignore`.
