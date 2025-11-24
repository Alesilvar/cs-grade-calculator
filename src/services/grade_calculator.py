"""Calculador de notas finales - RF04 y RF05."""

from typing import List
from ..models.evaluation import Evaluation
from ..models.student import Student
from ..models.grade_detail import GradeDetail
from ..policies.attendance_policy import AttendancePolicy
from ..policies.extra_points_policy import ExtraPointsPolicy


class GradeCalculator:
    """Calcula la nota final de estudiantes considerando evaluaciones, asistencia y puntos extra.

    Implementa:
    - RF01: Registro de evaluaciones
    - RF04: Cálculo de nota final
    - RF05: Detalle del cálculo
    - RNF03: Cálculo determinista
    """

    MIN_FINAL_GRADE = 0.0
    MAX_FINAL_GRADE = 20.0
    MINIMUM_WEIGHT_SUM = 100.0

    def __init__(
        self,
        attendance_policy: AttendancePolicy,
        extra_points_policy: ExtraPointsPolicy
    ):
        """Inicializa el calculador de notas.

        Args:
            attendance_policy: Política de asistencia a aplicar
            extra_points_policy: Política de puntos extra a aplicar
        """
        self._attendance_policy = attendance_policy
        self._extra_points_policy = extra_points_policy

    def calculate_final_grade(self, student: Student) -> GradeDetail:
        """Calcula la nota final de un estudiante (RF04 y RF05).

        El cálculo es determinista (RNF03) y sigue estos pasos:
        1. Calcula el promedio ponderado de las evaluaciones
        2. Aplica política de asistencia (penalización si corresponde)
        3. Aplica política de puntos extra (si corresponde)
        4. Asegura que el resultado esté en el rango [0, 20]

        Args:
            student: Estudiante con sus evaluaciones y datos

        Returns:
            GradeDetail con el detalle completo del cálculo

        Raises:
            ValueError: Si no hay evaluaciones o los pesos no suman 100%
        """
        self._validate_student_data(student)

        # Paso 1: Promedio ponderado
        weighted_average = self._calculate_weighted_average(student.evaluations)

        # Paso 2: Aplicar política de asistencia
        grade_after_attendance = self._attendance_policy.apply_penalty(
            student.has_reached_minimum_classes,
            weighted_average
        )
        attendance_penalty = self._attendance_policy.calculate_penalty_amount(
            student.has_reached_minimum_classes,
            weighted_average
        )

        # Paso 3: Aplicar puntos extra
        extra_points = self._extra_points_policy.calculate_extra_points(
            student_meets_criteria=True
        )
        grade_with_extra = grade_after_attendance + extra_points

        # Paso 4: Asegurar rango válido [0, 20]
        final_grade = self._clamp_grade(grade_with_extra)

        return GradeDetail(
            weighted_average=weighted_average,
            attendance_penalty=attendance_penalty,
            extra_points=extra_points,
            final_grade=final_grade
        )

    def _calculate_weighted_average(self, evaluations: List[Evaluation]) -> float:
        """Calcula el promedio ponderado de las evaluaciones.

        Args:
            evaluations: Lista de evaluaciones del estudiante

        Returns:
            Promedio ponderado
        """
        if not evaluations:
            return 0.0

        total_weighted_sum = sum(
            evaluation.grade * (evaluation.weight / 100.0)
            for evaluation in evaluations
        )

        return total_weighted_sum

    def _validate_student_data(self, student: Student) -> None:
        """Valida los datos del estudiante antes del cálculo.

        Args:
            student: Estudiante a validar

        Raises:
            ValueError: Si los datos son inválidos
        """
        if not student.evaluations:
            raise ValueError("El estudiante debe tener al menos una evaluación")

        total_weight = sum(evaluation.weight for evaluation in student.evaluations)

        if abs(total_weight - self.MINIMUM_WEIGHT_SUM) > 0.01:
            raise ValueError(
                f"Los pesos de las evaluaciones deben sumar {self.MINIMUM_WEIGHT_SUM}%, "
                f"pero suman {total_weight}%"
            )

    def _clamp_grade(self, grade: float) -> float:
        """Asegura que la nota esté en el rango válido [0, 20].

        Args:
            grade: Nota a validar

        Returns:
            Nota dentro del rango permitido
        """
        return max(self.MIN_FINAL_GRADE, min(grade, self.MAX_FINAL_GRADE))

    def register_evaluation(
        self,
        student: Student,
        grade: float,
        weight: float
    ) -> None:
        """Registra una nueva evaluación para el estudiante (RF01).

        Args:
            student: Estudiante al que se agrega la evaluación
            grade: Nota obtenida
            weight: Peso porcentual

        Raises:
            ValueError: Si se excede el límite de evaluaciones
        """
        evaluation = Evaluation(grade, weight)
        student.add_evaluation(evaluation)

    def register_attendance(
        self,
        student: Student,
        has_reached_minimum: bool
    ) -> None:
        """Registra el estado de asistencia del estudiante (RF02).

        Args:
            student: Estudiante a actualizar
            has_reached_minimum: Si cumplió la asistencia mínima
        """
        student.set_attendance_status(has_reached_minimum)

    def __repr__(self) -> str:
        """Representación string del calculador."""
        return (
            f"GradeCalculator(attendance={self._attendance_policy}, "
            f"extra_points={self._extra_points_policy})"
        )
