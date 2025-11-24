#!/bin/bash

# Script para ejecutar análisis de SonarQube con credenciales configuradas
# Backend - Student 48

echo "🔍 Ejecutando análisis de SonarQube para Backend-Student-48..."
echo ""

# Paso 1: Ejecutar tests con cobertura
echo "📊 Paso 1: Ejecutando tests con cobertura..."
pytest
if [ $? -ne 0 ]; then
    echo "❌ Error: Los tests fallaron. Revisa los errores antes de continuar."
    exit 1
fi
echo "✅ Tests ejecutados correctamente"
echo ""

# Verificar que el archivo de cobertura XML se generó
if [ ! -f "coverage.xml" ]; then
    echo "❌ Error: No se generó el archivo coverage.xml"
    exit 1
fi
echo "✅ Archivo de cobertura generado: coverage.xml"
echo ""

# Paso 2: Ejecutar SonarQube Scanner
echo "🔍 Paso 2: Ejecutando SonarQube Scanner..."
echo ""

# IMPORTANTE: Necesitas proporcionar la URL del servidor SonarQube
# Opciones comunes:
# - SonarCloud: https://sonarcloud.io
# - SonarQube local: http://localhost:9000
# - Servidor UTEC: [preguntar al profesor]

SONAR_HOST_URL="${SONAR_HOST_URL:-http://localhost:9000}"
SONAR_TOKEN="sqp_4b753953739d931735419dfa62fd300c74b2475d"

echo "📡 Servidor SonarQube: $SONAR_HOST_URL"
echo "🔑 Project Key: Backend-Student-48"
echo ""

if command -v sonar-scanner &> /dev/null; then
    sonar-scanner \
        -Dsonar.host.url="$SONAR_HOST_URL" \
        -Dsonar.login="$SONAR_TOKEN"

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Análisis completado exitosamente!"
        echo "📊 Revisa los resultados en: $SONAR_HOST_URL/dashboard?id=Backend-Student-48"
    else
        echo ""
        echo "❌ Error en el análisis. Verifica la conexión al servidor SonarQube."
    fi
else
    echo "⚠️  sonar-scanner no está instalado."
    echo ""
    echo "Ejecuta manualmente con:"
    echo ""
    echo "sonar-scanner \\"
    echo "  -Dsonar.host.url=$SONAR_HOST_URL \\"
    echo "  -Dsonar.login=$SONAR_TOKEN"
    echo ""
    echo "O usa Docker:"
    echo ""
    echo "docker run --rm -e SONAR_HOST_URL=\"$SONAR_HOST_URL\" -e SONAR_TOKEN=\"$SONAR_TOKEN\" -v \"\$(pwd):/usr/src\" sonarsource/sonar-scanner-cli"
fi
