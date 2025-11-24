"""Política de asistencia - RF02."""


class AttendancePolicy:
    """Gestiona la política de asistencia y penalizaciones.

    Implementa RF02: Verificación de asistencia mínima y aplicación de
    penalizaciones según el reglamento de UTEC.
    """

    PENALTY_FOR_INSUFFICIENT_ATTENDANCE = 0.0

    def __init__(self, penalty_grade: float = PENALTY_FOR_INSUFFICIENT_ATTENDANCE):
        """Inicializa la política de asistencia.

        Args:
            penalty_grade: Nota aplicada si no se cumple asistencia mínima
        """
        self._penalty_grade = penalty_grade

    def apply_penalty(self, has_reached_minimum: bool, calculated_grade: float) -> float:
        """Aplica penalización si no se cumple la asistencia mínima.

        Args:
            has_reached_minimum: Si el estudiante cumplió asistencia mínima
            calculated_grade: Nota calculada antes de aplicar penalización

        Returns:
            Nota después de aplicar la penalización si corresponde
        """
        if not has_reached_minimum:
            return self._penalty_grade
        return calculated_grade

    def calculate_penalty_amount(
        self,
        has_reached_minimum: bool,
        calculated_grade: float
    ) -> float:
        """Calcula el monto de la penalización.

        Args:
            has_reached_minimum: Si el estudiante cumplió asistencia mínima
            calculated_grade: Nota calculada antes de penalización

        Returns:
            Monto de la penalización (negativo si hay penalización)
        """
        if not has_reached_minimum:
            return self._penalty_grade - calculated_grade
        return 0.0

    @property
    def penalty_grade(self) -> float:
        """Obtiene la nota de penalización."""
        return self._penalty_grade

    def __repr__(self) -> str:
        """Representación string de la política."""
        return f"AttendancePolicy(penalty_grade={self._penalty_grade})"
