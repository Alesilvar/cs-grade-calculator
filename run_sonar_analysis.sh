#!/bin/bash

# Script para ejecutar análisis de SonarQube en CS-GradeCalculator

echo "🔍 Iniciando análisis de SonarQube..."
echo ""

# Paso 1: Ejecutar tests con cobertura
echo "📊 Paso 1: Ejecutando tests con cobertura..."
pytest
if [ $? -ne 0 ]; then
    echo "❌ Error: Los tests fallaron. Por favor, corrija los errores antes de continuar."
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
echo "IMPORTANTE: Asegúrate de tener configurado uno de los siguientes:"
echo "  - SonarQube Cloud con token de autenticación"
echo "  - SonarQube Server local ejecutándose"
echo ""

# Verificar si existe el scanner de SonarQube
if command -v sonar-scanner &> /dev/null; then
    echo "📡 Ejecutando sonar-scanner..."
    sonar-scanner
    echo ""
    echo "✅ Análisis completado. Revisa los resultados en tu instancia de SonarQube."
else
    echo "⚠️  sonar-scanner no está instalado."
    echo ""
    echo "Para continuar, tienes dos opciones:"
    echo ""
    echo "OPCIÓN 1: Instalar SonarQube Scanner localmente"
    echo "  - Descarga: https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/"
    echo "  - Luego ejecuta: sonar-scanner"
    echo ""
    echo "OPCIÓN 2: Usar Docker"
    echo "  docker run --rm -v \"\$(pwd):/usr/src\" sonarsource/sonar-scanner-cli"
    echo ""
    echo "OPCIÓN 3: SonarQube Cloud (recomendado para proyectos pequeños)"
    echo "  1. Crea una cuenta en: https://sonarcloud.io"
    echo "  2. Crea un nuevo proyecto y obtén tu token"
    echo "  3. Ejecuta:"
    echo "     sonar-scanner \\"
    echo "       -Dsonar.organization=<tu-org> \\"
    echo "       -Dsonar.host.url=https://sonarcloud.io \\"
    echo "       -Dsonar.login=<tu-token>"
fi
