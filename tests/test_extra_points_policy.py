"""Tests unitarios para ExtraPointsPolicy."""

import pytest
from src.policies.extra_points_policy import ExtraPointsPolicy


class TestExtraPointsPolicy:
    """Tests para la clase ExtraPointsPolicy."""

    def test_shouldApplyExtraPointsWhenAllTeachersAgree(self):
        """Debería aplicar puntos extra cuando todos los docentes acuerdan."""
        policy = ExtraPointsPolicy(all_years_teachers=[True, True, True])

        extra_points = policy.calculate_extra_points(student_meets_criteria=True)

        assert extra_points == 1.0
        assert policy.should_apply_extra_points() is True

    def test_shouldNotApplyExtraPointsWhenNotAllTeachersAgree(self):
        """No debería aplicar puntos extra si no todos los docentes acuerdan."""
        policy = ExtraPointsPolicy(all_years_teachers=[True, False, True])

        extra_points = policy.calculate_extra_points(student_meets_criteria=True)

        assert extra_points == 0.0
        assert policy.should_apply_extra_points() is False

    def test_shouldNotApplyExtraPointsWhenStudentDoesNotMeetCriteria(self):
        """No debería aplicar puntos extra si el estudiante no cumple criterios."""
        policy = ExtraPointsPolicy(all_years_teachers=[True, True, True])

        extra_points = policy.calculate_extra_points(student_meets_criteria=False)

        assert extra_points == 0.0
        assert policy.should_apply_extra_points(student_meets_criteria=False) is False

    def test_shouldAllowCustomExtraPointsAmount(self):
        """Debería permitir configurar una cantidad personalizada de puntos extra."""
        custom_points = 2.5
        policy = ExtraPointsPolicy(
            all_years_teachers=[True, True],
            extra_points_amount=custom_points
        )

        extra_points = policy.calculate_extra_points(student_meets_criteria=True)

        assert extra_points == custom_points
        assert policy.extra_points_amount == custom_points

    def test_shouldRaiseErrorWhenTeachersListIsEmpty(self):
        """Debería lanzar error cuando la lista de docentes está vacía."""
        with pytest.raises(ValueError, match="no puede estar vacía"):
            ExtraPointsPolicy(all_years_teachers=[])

    def test_shouldRaiseErrorWhenTeachersListIsNotList(self):
        """Debería lanzar error cuando no es una lista."""
        with pytest.raises(ValueError, match="debe ser una lista"):
            ExtraPointsPolicy(all_years_teachers="invalid")

    def test_shouldRaiseErrorWhenTeachersListContainsNonBooleans(self):
        """Debería lanzar error cuando la lista contiene no booleanos."""
        with pytest.raises(ValueError, match="deben ser booleanos"):
            ExtraPointsPolicy(all_years_teachers=[True, "False", True])

    def test_shouldReturnCopyOfTeachersList(self):
        """Debería retornar una copia de la lista de docentes (inmutabilidad)."""
        original_list = [True, True, False]
        policy = ExtraPointsPolicy(all_years_teachers=original_list)

        teachers_copy = policy.all_years_teachers
        teachers_copy[0] = False

        assert policy.all_years_teachers == original_list
