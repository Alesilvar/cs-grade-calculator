"""Política de puntos extra - RF03."""

from typing import List


class ExtraPointsPolicy:
    """Gestiona la política de puntos extra según criterios definidos.

    Implementa RF03: Consulta de política de puntos extra definida
    colectivamente por los docentes del año académico (allYearsTeachers).
    """

    DEFAULT_EXTRA_POINTS = 0.0
    EXTRA_POINTS_WHEN_AGREED = 1.0

    def __init__(
        self,
        all_years_teachers: List[bool],
        extra_points_amount: float = EXTRA_POINTS_WHEN_AGREED
    ):
        """Inicializa la política de puntos extra.

        Args:
            all_years_teachers: Lista de booleanos indicando si cada docente
                               está de acuerdo en otorgar puntos extra
            extra_points_amount: Cantidad de puntos extra a otorgar si aplica

        Raises:
            ValueError: Si la lista de docentes está vacía
        """
        self._validate_teachers_list(all_years_teachers)
        self._all_years_teachers = all_years_teachers
        self._extra_points_amount = extra_points_amount

    def should_apply_extra_points(self, student_meets_criteria: bool = True) -> bool:
        """Determina si se deben aplicar puntos extra.

        Se aplican puntos extra solo si:
        1. TODOS los docentes están de acuerdo (allYearsTeachers = all True)
        2. El estudiante cumple los criterios definidos

        Args:
            student_meets_criteria: Si el estudiante cumple los criterios

        Returns:
            True si se deben aplicar puntos extra, False en caso contrario
        """
        all_teachers_agree = all(self._all_years_teachers)
        return all_teachers_agree and student_meets_criteria

    def calculate_extra_points(self, student_meets_criteria: bool = True) -> float:
        """Calcula los puntos extra a aplicar.

        Args:
            student_meets_criteria: Si el estudiante cumple los criterios

        Returns:
            Cantidad de puntos extra (0.0 si no aplica)
        """
        if self.should_apply_extra_points(student_meets_criteria):
            return self._extra_points_amount
        return self.DEFAULT_EXTRA_POINTS

    def _validate_teachers_list(self, teachers: List[bool]) -> None:
        """Valida la lista de docentes.

        Args:
            teachers: Lista de acuerdos de docentes

        Raises:
            ValueError: Si la lista es inválida
        """
        if not isinstance(teachers, list):
            raise ValueError("all_years_teachers debe ser una lista")
        if len(teachers) == 0:
            raise ValueError("La lista de docentes no puede estar vacía")
        if not all(isinstance(t, bool) for t in teachers):
            raise ValueError("Todos los elementos deben ser booleanos")

    @property
    def all_years_teachers(self) -> List[bool]:
        """Obtiene la lista de acuerdos de docentes."""
        return self._all_years_teachers.copy()

    @property
    def extra_points_amount(self) -> float:
        """Obtiene la cantidad de puntos extra."""
        return self._extra_points_amount

    def __repr__(self) -> str:
        """Representación string de la política."""
        agreement_status = "all agree" if all(self._all_years_teachers) else "not all agree"
        return (
            f"ExtraPointsPolicy(teachers={len(self._all_years_teachers)}, "
            f"{agreement_status}, points={self._extra_points_amount})"
        )
