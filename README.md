# CS-GradeCalculator

Sistema de cálculo de notas finales para UTEC (Universidad de Ingeniería y Tecnología).

## Descripción

Backend en Python que implementa el módulo de cálculo de nota final, alineado con los Requerimientos Funcionales (RF) y Requerimientos No Funcionales (RNF) del sistema CS-GradeCalculator.

## Requerimientos Funcionales Implementados

- **RF01**: Registro de evaluaciones con nota obtenida y porcentaje de peso sobre la nota final
- **RF02**: Registro de asistencia mínima requerida por el reglamento académico
- **RF03**: Consulta de política de puntos extra definida colectivamente por docentes
- **RF04**: Cálculo de nota final considerando evaluaciones, asistencia y políticas de puntos extra
- **RF05**: Visualización del detalle del cálculo (promedio ponderado, penalizaciones, puntos extra)

## Requerimientos No Funcionales Cumplidos

- **RNF01**: Máximo 10 evaluaciones por estudiante
- **RNF02**: Soporte para hasta 50 usuarios concurrentes (diseño stateless)
- **RNF03**: Cálculo determinista (mismos datos = mismo resultado)
- **RNF04**: Tiempo de cálculo < 300ms por solicitud

## Estructura del Proyecto

```
aleu/
├── src/
│   ├── models/           # Modelos de dominio
│   │   ├── evaluation.py       # RF01: Evaluación con nota y peso
│   │   ├── student.py          # Estudiante con evaluaciones
│   │   └── grade_detail.py     # RF05: Detalle del cálculo
│   ├── services/         # Servicios principales
│   │   └── grade_calculator.py # RF04: Calculador de notas
│   └── policies/         # Políticas del sistema
│       ├── attendance_policy.py    # RF02: Política de asistencia
│       └── extra_points_policy.py  # RF03: Política de puntos extra
├── tests/                # Tests unitarios (>50% cobertura)
│   ├── test_evaluation.py
│   ├── test_student.py
│   ├── test_attendance_policy.py
│   ├── test_extra_points_policy.py
│   └── test_grade_calculator.py
├── requirements.txt      # Dependencias
├── pytest.ini           # Configuración de pytest
└── README.md
```

## Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd aleu

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar el paquete en modo desarrollo
pip install -e .
```

## Uso

### Ejemplo básico

```python
from src.models.student import Student
from src.services.grade_calculator import GradeCalculator
from src.policies.attendance_policy import AttendancePolicy
from src.policies.extra_points_policy import ExtraPointsPolicy

# Configurar políticas
attendance_policy = AttendancePolicy()
extra_points_policy = ExtraPointsPolicy(all_years_teachers=[True, True, True])

# Crear calculador
calculator = GradeCalculator(attendance_policy, extra_points_policy)

# Crear estudiante
student = Student(student_id="20210001")

# Registrar evaluaciones (RF01)
calculator.register_evaluation(student, grade=16.0, weight=30.0)
calculator.register_evaluation(student, grade=14.0, weight=30.0)
calculator.register_evaluation(student, grade=18.0, weight=40.0)

# Registrar asistencia (RF02)
calculator.register_attendance(student, has_reached_minimum=True)

# Calcular nota final (RF04)
grade_detail = calculator.calculate_final_grade(student)

# Visualizar detalle (RF05)
print(grade_detail)
print(f"Nota Final: {grade_detail.final_grade}")
```

## Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con cobertura
pytest --cov=src --cov-report=html

# Ejecutar tests específicos
pytest tests/test_grade_calculator.py
```

### Casos de Test Cubiertos

- ✅ Cálculo normal
- ✅ Caso sin asistencia mínima
- ✅ Caso con y sin puntos extra
- ✅ Casos borde (0 evaluaciones, pesos inválidos, notas límite)
- ✅ Verificación de determinismo (RNF03)
- ✅ Validación de límite de evaluaciones (RNF01)

## Arquitectura

### Diseño Orientado a Objetos

- **Separación de responsabilidades**: Cada clase tiene una responsabilidad única y bien definida
- **Bajo acoplamiento**: Las clases interactúan a través de interfaces claras
- **Alta cohesión**: Funcionalidades relacionadas están agrupadas
- **Principios SOLID**: Código mantenible y extensible

### Clases Principales

1. **Evaluation**: Representa una evaluación con nota y peso
2. **Student**: Agrupa evaluaciones y datos del estudiante
3. **GradeDetail**: Detalla los componentes del cálculo de nota
4. **AttendancePolicy**: Gestiona penalizaciones por asistencia
5. **ExtraPointsPolicy**: Gestiona puntos extra según acuerdos docentes
6. **GradeCalculator**: Orquesta el cálculo de nota final

## Calidad del Código

- ✅ Nombres significativos (sin x1, dato, aux)
- ✅ Sin valores mágicos (uso de constantes)
- ✅ Manejo correcto de errores y validaciones
- ✅ Comentarios relevantes y no redundantes
- ✅ Formato consistente (PEP 8)
- ✅ Tests unitarios con nomenclatura clara (shouldReturnXWhenY)

## Análisis con SonarQube

### Configuración Rápida

El proyecto incluye configuración lista para SonarQube:

```bash
# Opción 1: Usar script automatizado (recomendado)
./run_sonar_analysis.sh

# Opción 2: Ejecutar manualmente
pytest                    # Genera coverage.xml
sonar-scanner            # Ejecuta el análisis
```

### Métodos de Análisis

#### 1. SonarQube Cloud (Recomendado para comenzar)

```bash
# 1. Crear cuenta en https://sonarcloud.io
# 2. Crear nuevo proyecto y obtener token
# 3. Ejecutar análisis

pytest  # Generar cobertura

sonar-scanner \
  -Dsonar.organization=tu-organizacion \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.login=tu-token-aqui
```

#### 2. SonarQube con Docker (Servidor local)

```bash
# Iniciar servidor SonarQube
docker run -d --name sonarqube -p 9000:9000 sonarqube:latest

# Esperar a que inicie (visitar http://localhost:9000)
# Usuario por defecto: admin / admin

# Generar cobertura
pytest

# Ejecutar análisis
sonar-scanner \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=tu-token-generado
```

#### 3. Instalación local de SonarQube Scanner

```bash
# Descargar desde:
# https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/

# Después de instalar:
pytest
sonar-scanner
```

### Archivos de Configuración

- **sonar-project.properties**: Configuración del proyecto
- **pytest.ini**: Genera coverage.xml automáticamente
- **run_sonar_analysis.sh**: Script para análisis completo

### Métricas Analizadas

SonarQube evaluará:

- 🐛 **Bugs**: Errores potenciales en el código
- 🔐 **Vulnerabilidades**: Problemas de seguridad
- 💨 **Code Smells**: Problemas de mantenibilidad
- 📊 **Cobertura**: Porcentaje de código cubierto por tests
- 🔄 **Duplicación**: Código duplicado
- 📏 **Complejidad**: Complejidad ciclomática

## Licencia

Este proyecto es parte del curso CS3081 de UTEC.