"""Ejemplo de uso del sistema CS-GradeCalculator."""

from src.models.student import Student
from src.services.grade_calculator import GradeCalculator
from src.policies.attendance_policy import AttendancePolicy
from src.policies.extra_points_policy import ExtraPointsPolicy


def main():
    """Ejemplo principal del caso de uso CU001."""
    print("=" * 60)
    print("CS-GradeCalculator - Sistema de Cálculo de Notas")
    print("=" * 60)
    print()

    # Configurar políticas del sistema
    attendance_policy = AttendancePolicy()
    extra_points_policy = ExtraPointsPolicy(
        all_years_teachers=[True, True, True]  # RF03: Todos los docentes acuerdan
    )

    # Crear calculador
    calculator = GradeCalculator(attendance_policy, extra_points_policy)

    # Caso 1: Estudiante con asistencia suficiente y todos los criterios
    print("CASO 1: Estudiante con todas las condiciones favorables")
    print("-" * 60)

    student1 = Student(student_id="20210001")

    # RF01: Registrar evaluaciones
    print("\nRegistrando evaluaciones:")
    calculator.register_evaluation(student1, grade=16.0, weight=30.0)
    print("  - Evaluación 1: Nota 16.0, Peso 30%")
    calculator.register_evaluation(student1, grade=14.0, weight=30.0)
    print("  - Evaluación 2: Nota 14.0, Peso 30%")
    calculator.register_evaluation(student1, grade=18.0, weight=40.0)
    print("  - Evaluación 3: Nota 18.0, Peso 40%")

    # RF02: Registrar asistencia
    calculator.register_attendance(student1, has_reached_minimum=True)
    print("\nAsistencia mínima: Cumplida ✓")

    # RF04: Calcular nota final
    grade_detail1 = calculator.calculate_final_grade(student1)

    # RF05: Mostrar detalle
    print("\n" + str(grade_detail1))
    print("\n" + "=" * 60 + "\n")

    # Caso 2: Estudiante sin asistencia mínima
    print("CASO 2: Estudiante sin asistencia mínima")
    print("-" * 60)

    student2 = Student(student_id="20210002")

    print("\nRegistrando evaluaciones:")
    calculator.register_evaluation(student2, grade=18.0, weight=50.0)
    print("  - Evaluación 1: Nota 18.0, Peso 50%")
    calculator.register_evaluation(student2, grade=17.0, weight=50.0)
    print("  - Evaluación 2: Nota 17.0, Peso 50%")

    calculator.register_attendance(student2, has_reached_minimum=False)
    print("\nAsistencia mínima: NO cumplida ✗")

    grade_detail2 = calculator.calculate_final_grade(student2)

    print("\n" + str(grade_detail2))
    print("\n" + "=" * 60 + "\n")

    # Caso 3: Sin puntos extra (no todos los docentes acuerdan)
    print("CASO 3: Sin puntos extra")
    print("-" * 60)

    extra_points_policy_no = ExtraPointsPolicy(
        all_years_teachers=[True, False, True]  # No todos acuerdan
    )
    calculator_no_extra = GradeCalculator(attendance_policy, extra_points_policy_no)

    student3 = Student(student_id="20210003")

    print("\nRegistrando evaluaciones:")
    calculator_no_extra.register_evaluation(student3, grade=15.0, weight=100.0)
    print("  - Evaluación 1: Nota 15.0, Peso 100%")

    calculator_no_extra.register_attendance(student3, has_reached_minimum=True)
    print("\nAsistencia mínima: Cumplida ✓")
    print("Puntos extra: No disponibles (no todos los docentes acuerdan)")

    grade_detail3 = calculator_no_extra.calculate_final_grade(student3)

    print("\n" + str(grade_detail3))
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
