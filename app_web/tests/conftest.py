import os
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from usuarios.models import Usuario
from proyectos.models import Proyecto, Tarea
from analisis_mercado.models import Habilidad, OfertaEmpleo
from motor_ia.models import ModeloIA

@pytest.fixture(scope='session')
def django_db_setup():
    """Configurar la base de datos de prueba"""
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }

@pytest.fixture
def admin_user():
    """Crear usuario administrador"""
    return Usuario.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        rol='ADMIN'
    )

@pytest.fixture
def gestor_user():
    """Crear usuario gestor"""
    return Usuario.objects.create_user(
        username='gestor',
        email='gestor@example.com',
        password='gestor123',
        rol='GESTOR'
    )

@pytest.fixture
def colaborador_user():
    """Crear usuario colaborador"""
    return Usuario.objects.create_user(
        username='colaborador',
        email='colaborador@example.com',
        password='colaborador123',
        rol='COLAB'
    )

@pytest.fixture
def habilidades():
    """Crear habilidades de prueba"""
    habilidades = []
    for nombre in ['Python', 'Django', 'JavaScript']:
        habilidad = Habilidad.objects.create(nombre=nombre)
        habilidades.append(habilidad)
    return habilidades

@pytest.fixture
def proyecto(gestor_user, colaborador_user, habilidades):
    """Crear proyecto de prueba"""
    proyecto = Proyecto.objects.create(
        titulo='Proyecto de Prueba',
        descripcion='Descripción del proyecto de prueba',
        fecha_inicio='2024-01-01',
        fecha_fin_estimada='2024-12-31',
        estado='PEND',
        creador=gestor_user
    )
    proyecto.colaboradores.add(colaborador_user)
    proyecto.habilidades_requeridas.add(*habilidades)
    return proyecto

@pytest.fixture
def tarea(proyecto, colaborador_user, habilidades):
    """Crear tarea de prueba"""
    return Tarea.objects.create(
        titulo='Tarea de Prueba',
        descripcion='Descripción de la tarea de prueba',
        proyecto=proyecto,
        asignado_a=colaborador_user,
        estado='PEND',
        prioridad='ALTA',
        fecha_fin_estimada='2024-12-31'
    )

@pytest.fixture
def oferta_empleo(habilidades):
    """Crear oferta de empleo de prueba"""
    oferta = OfertaEmpleo.objects.create(
        titulo='Oferta de Prueba',
        empresa='Empresa de Prueba',
        ubicacion='Madrid',
        descripcion='Descripción de la oferta de prueba',
        requisitos='Requisitos de la oferta de prueba',
        salario_min=30000,
        salario_max=50000,
        fecha_publicacion='2024-01-01',
        url_original='https://example.com/oferta',
        fuente='TECNO'
    )
    oferta.habilidades.add(*habilidades)
    return oferta

@pytest.fixture
def modelo_ia():
    """Crear modelo de IA de prueba"""
    return ModeloIA.objects.create(
        nombre='Modelo de Prueba',
        descripcion='Descripción del modelo de prueba',
        tipo='REC',
        version='1.0.0',
        fecha_entrenamiento='2024-01-01',
        precision=0.85,
        parametros={
            'algorithm': 'random_forest',
            'n_estimators': 100
        },
        archivo_modelo='modelos/test_model.pkl',
        activo=True
    )

@pytest.fixture
def api_client():
    """Crear cliente de API de prueba"""
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, admin_user):
    """Crear cliente de API autenticado"""
    api_client.force_authenticate(user=admin_user)
    return api_client

@pytest.fixture
def mock_scraper(mocker):
    """Mock para el scraper"""
    mock = mocker.patch('datos_externos.scrapers.base_scraper.BaseScraper')
    mock.return_value.scrape.return_value = [
        {
            'titulo': 'Oferta Mock',
            'empresa': 'Empresa Mock',
            'ubicacion': 'Madrid',
            'descripcion': 'Descripción mock',
            'requisitos': 'Requisitos mock',
            'salario_min': 30000,
            'salario_max': 50000,
            'fecha_publicacion': '2024-01-01',
            'url_original': 'https://example.com/mock',
            'fuente': 'TECNO'
        }
    ]
    return mock

@pytest.fixture
def mock_ia_model(mocker):
    """Mock para el modelo de IA"""
    mock = mocker.patch('motor_ia.models.ModeloIA.predict')
    mock.return_value = {
        'prediccion': 'Recomendación mock',
        'confianza': 0.85
    }
    return mock 