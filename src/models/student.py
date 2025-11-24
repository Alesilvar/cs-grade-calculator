"""Modelo de Estudiante."""

from typing import List, Optional
from .evaluation import Evaluation


class Student:
    """Representa un estudiante con sus evaluaciones y datos.

    Agrupa la información del estudiante necesaria para el cálculo de notas.
    """

    MAX_EVALUATIONS = 10  # RNF01: Máximo 10 evaluaciones por estudiante

    def __init__(
        self,
        student_id: str,
        evaluations: Optional[List[Evaluation]] = None,
        has_reached_minimum_classes: bool = False
    ):
        """Inicializa un estudiante.

        Args:
            student_id: Código o identificador del estudiante
            evaluations: Lista de evaluaciones del estudiante
            has_reached_minimum_classes: Si cumplió asistencia mínima (RF02)

        Raises:
            ValueError: Si el ID es inválido o excede el límite de evaluaciones
        """
        self._validate_student_id(student_id)

        self._student_id = student_id
        self._evaluations = evaluations or []
        self._has_reached_minimum_classes = has_reached_minimum_classes

        self._validate_evaluations_limit()

    @property
    def student_id(self) -> str:
        """Obtiene el ID del estudiante."""
        return self._student_id

    @property
    def evaluations(self) -> List[Evaluation]:
        """Obtiene la lista de evaluaciones."""
        return self._evaluations.copy()

    @property
    def has_reached_minimum_classes(self) -> bool:
        """Obtiene si el estudiante cumplió la asistencia mínima (RF02)."""
        return self._has_reached_minimum_classes

    def add_evaluation(self, evaluation: Evaluation) -> None:
        """Agrega una evaluación al estudiante.

        Args:
            evaluation: Evaluación a agregar

        Raises:
            ValueError: Si se excede el límite de evaluaciones (RNF01)
        """
        if len(self._evaluations) >= self.MAX_EVALUATIONS:
            raise ValueError(
                f"No se pueden agregar más de {self.MAX_EVALUATIONS} evaluaciones"
            )
        self._evaluations.append(evaluation)

    def set_attendance_status(self, has_reached_minimum: bool) -> None:
        """Establece el estado de asistencia del estudiante (RF02).

        Args:
            has_reached_minimum: Si cumplió la asistencia mínima
        """
        self._has_reached_minimum_classes = has_reached_minimum

    def _validate_student_id(self, student_id: str) -> None:
        """Valida el ID del estudiante."""
        if not isinstance(student_id, str):
            raise ValueError("El ID del estudiante debe ser un string")
        if not student_id or student_id.strip() == "":
            raise ValueError("El ID del estudiante no puede estar vacío")

    def _validate_evaluations_limit(self) -> None:
        """Valida que no se exceda el límite de evaluaciones (RNF01)."""
        if len(self._evaluations) > self.MAX_EVALUATIONS:
            raise ValueError(
                f"No se pueden tener más de {self.MAX_EVALUATIONS} evaluaciones"
            )

    def __repr__(self) -> str:
        """Representación string del estudiante."""
        return (
            f"Student(id={self._student_id}, "
            f"evaluations={len(self._evaluations)}, "
            f"attendance={self._has_reached_minimum_classes})"
        )
