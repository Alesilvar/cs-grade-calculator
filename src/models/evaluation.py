"""Modelo de Evaluación - RF01."""


class Evaluation:
    """Representa una evaluación con su nota y peso porcentual.

    Implementa RF01: Registro de evaluaciones con nota y porcentaje de peso.
    """

    MIN_GRADE = 0.0
    MAX_GRADE = 20.0
    MIN_WEIGHT = 0.0
    MAX_WEIGHT = 100.0

    def __init__(self, grade: float, weight: float):
        """Inicializa una evaluación.

        Args:
            grade: Nota obtenida (0-20)
            weight: Peso porcentual sobre la nota final (0-100)

        Raises:
            ValueError: Si los valores están fuera del rango permitido
        """
        self._validate_grade(grade)
        self._validate_weight(weight)

        self._grade = float(grade)
        self._weight = float(weight)

    @property
    def grade(self) -> float:
        """Obtiene la nota de la evaluación."""
        return self._grade

    @property
    def weight(self) -> float:
        """Obtiene el peso porcentual de la evaluación."""
        return self._weight

    def _validate_grade(self, grade: float) -> None:
        """Valida que la nota esté en el rango permitido."""
        if not isinstance(grade, (int, float)):
            raise ValueError("La nota debe ser un número")
        if grade < self.MIN_GRADE or grade > self.MAX_GRADE:
            raise ValueError(
                f"La nota debe estar entre {self.MIN_GRADE} y {self.MAX_GRADE}"
            )

    def _validate_weight(self, weight: float) -> None:
        """Valida que el peso esté en el rango permitido."""
        if not isinstance(weight, (int, float)):
            raise ValueError("El peso debe ser un número")
        if weight < self.MIN_WEIGHT or weight > self.MAX_WEIGHT:
            raise ValueError(
                f"El peso debe estar entre {self.MIN_WEIGHT} y {self.MAX_WEIGHT}"
            )

    def __repr__(self) -> str:
        """Representación string de la evaluación."""
        return f"Evaluation(grade={self._grade}, weight={self._weight})"

    def __eq__(self, other) -> bool:
        """Compara dos evaluaciones."""
        if not isinstance(other, Evaluation):
            return False
        return self._grade == other._grade and self._weight == other._weight
