# Guía de SonarQube - Backend Student 48

## Tus Credenciales

- **Project Key**: `Backend-Student-48`
- **Token**: `sqp_4b753953739d931735419dfa62fd300c74b2475d`

## Métodos de Análisis

### Método 1: Script Automatizado (Recomendado)

```bash
# Si el servidor es local (localhost:9000)
./run_sonar.sh

# Si el servidor es diferente, especifica la URL:
SONAR_HOST_URL="https://sonarcloud.io" ./run_sonar.sh
```

### Método 2: Comandos Manuales

#### Opción A: Servidor Local

```bash
# 1. Generar cobertura
pytest

# 2. Ejecutar análisis
sonar-scanner \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=sqp_4b753953739d931735419dfa62fd300c74b2475d

# 3. Ver resultados en:
# http://localhost:9000/dashboard?id=Backend-Student-48
```

#### Opción B: SonarCloud

```bash
# 1. Generar cobertura
pytest

# 2. Ejecutar análisis
sonar-scanner \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.organization=tu-organizacion \
  -Dsonar.login=sqp_4b753953739d931735419dfa62fd300c74b2475d

# 3. Ver resultados en:
# https://sonarcloud.io/dashboard?id=Backend-Student-48
```

#### Opción C: Servidor UTEC (si aplica)

```bash
# 1. Generar cobertura
pytest

# 2. Ejecutar análisis (reemplaza <servidor-utec> con la URL correcta)
sonar-scanner \
  -Dsonar.host.url=<servidor-utec> \
  -Dsonar.login=sqp_4b753953739d931735419dfa62fd300c74b2475d
```

### Método 3: Docker (Sin instalar SonarScanner)

```bash
# 1. Generar cobertura
pytest

# 2. Ejecutar con Docker (servidor local)
docker run --rm \
  --network=host \
  -v "$(pwd):/usr/src" \
  -e SONAR_HOST_URL="http://localhost:9000" \
  -e SONAR_LOGIN="sqp_4b753953739d931735419dfa62fd300c74b2475d" \
  sonarsource/sonar-scanner-cli

# Para otro servidor:
docker run --rm \
  -v "$(pwd):/usr/src" \
  -e SONAR_HOST_URL="https://tu-servidor.com" \
  -e SONAR_LOGIN="sqp_4b753953739d931735419dfa62fd300c74b2475d" \
  sonarsource/sonar-scanner-cli
```

## Iniciar Servidor SonarQube Local (si no tienes uno)

```bash
# Opción 1: Docker (más fácil)
docker run -d --name sonarqube -p 9000:9000 sonarqube:latest

# Esperar 2-3 minutos para que inicie
# Acceder a: http://localhost:9000
# Usuario por defecto: admin / admin

# Opción 2: Descarga manual
# https://www.sonarqube.org/downloads/
```

## Verificar que Todo Funciona

```bash
# 1. Ejecutar tests
pytest

# 2. Verificar que coverage.xml existe
ls -la coverage.xml

# 3. Verificar configuración
cat sonar-project.properties

# 4. Ejecutar análisis
./run_sonar.sh
```

## Archivos Importantes

- `sonar-project.properties` - Configuración con tu Project Key
- `pytest.ini` - Genera coverage.xml automáticamente
- `run_sonar.sh` - Script con tu token configurado
- `coverage.xml` - Reporte de cobertura (se genera con pytest)

## Métricas que Verás en SonarQube

- 🐛 **Bugs**: 0 (esperado)
- 🔐 **Vulnerabilidades**: 0 (esperado)
- 💨 **Code Smells**: < 5 (esperado)
- 📊 **Cobertura**: > 50% (actual: ~80%)
- 🔄 **Duplicación**: < 3%
- 📏 **Complejidad**: Baja

## Troubleshooting

### Error: "Could not find coverage.xml"
```bash
# Solución: Asegúrate de ejecutar pytest primero
pytest
```

### Error: "Connection refused"
```bash
# Solución: Verifica que el servidor SonarQube esté corriendo
# Para servidor local:
docker ps | grep sonarqube
```

### Error: "Project not found"
```bash
# Solución: Verifica que el Project Key sea correcto
grep projectKey sonar-project.properties
# Debe mostrar: sonar.projectKey=Backend-Student-48
```

## Notas Importantes

- El token ya está configurado en `run_sonar.sh`
- No compartas tu token públicamente
- Si regeneras el token en SonarQube, actualiza `run_sonar.sh`
- La cobertura se calcula automáticamente al ejecutar pytest
