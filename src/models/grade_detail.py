"""Modelo de detalle de cálculo de nota - RF05."""


class GradeDetail:
    """Representa el detalle del cálculo de la nota final.

    Implementa RF05: Visualización del detalle del cálculo.
    """

    def __init__(
        self,
        weighted_average: float,
        attendance_penalty: float,
        extra_points: float,
        final_grade: float
    ):
        """Inicializa el detalle de cálculo.

        Args:
            weighted_average: Promedio ponderado de evaluaciones
            attendance_penalty: Penalización por inasistencia
            extra_points: Puntos extra aplicados
            final_grade: Nota final calculada
        """
        self._weighted_average = weighted_average
        self._attendance_penalty = attendance_penalty
        self._extra_points = extra_points
        self._final_grade = final_grade

    @property
    def weighted_average(self) -> float:
        """Obtiene el promedio ponderado."""
        return self._weighted_average

    @property
    def attendance_penalty(self) -> float:
        """Obtiene la penalización por asistencia."""
        return self._attendance_penalty

    @property
    def extra_points(self) -> float:
        """Obtiene los puntos extra aplicados."""
        return self._extra_points

    @property
    def final_grade(self) -> float:
        """Obtiene la nota final."""
        return self._final_grade

    def to_dict(self) -> dict:
        """Convierte el detalle a diccionario para facilitar visualización.

        Returns:
            Diccionario con todos los componentes del cálculo
        """
        return {
            "weighted_average": round(self._weighted_average, 2),
            "attendance_penalty": round(self._attendance_penalty, 2),
            "extra_points": round(self._extra_points, 2),
            "final_grade": round(self._final_grade, 2)
        }

    def __repr__(self) -> str:
        """Representación string del detalle."""
        return (
            f"GradeDetail(weighted_avg={self._weighted_average:.2f}, "
            f"penalty={self._attendance_penalty:.2f}, "
            f"extra={self._extra_points:.2f}, "
            f"final={self._final_grade:.2f})"
        )

    def __str__(self) -> str:
        """Representación legible del detalle para el usuario."""
        return (
            f"Detalle del Cálculo:\n"
            f"  - Promedio Ponderado: {self._weighted_average:.2f}\n"
            f"  - Penalización por Asistencia: {self._attendance_penalty:.2f}\n"
            f"  - Puntos Extra: {self._extra_points:.2f}\n"
            f"  - Nota Final: {self._final_grade:.2f}"
        )
