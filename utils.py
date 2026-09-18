import pandas as pd
import random



def calculate_gpa(df, grading_scale):
    # df = dataframe of courses for one semester
    # grading_scale = dict mapping grade to points, e.g. {"A":5, "B":4,...}

    # Convert grades to points
    df["Points"] = df["Grade"].map(grading_scale)

    # Weighted points = Points * Units
    df["Weighted"] = df["Points"] * df["Units"]

    # Semester_GPA = sum(weighted points) / sum(units)
    semester_gpa = df["Weighted"].sum() / df["Units"].sum()

    return round(semester_gpa, 2)


def generate_course_plan(required_gpa, num_courses, units_per_course, grading_scale):
    """
    Generate a list of courses and grades that would achieve the required GPA.
    - required_gpa: GPA per unit needed
    - num_courses: number of courses to generate
    - units_per_course: list of units for each course
    - grading_scale: dict, e.g., {"A":5, "B":4, "C":3...}
    """
    points_values = sorted(grading_scale.values(), reverse=True)
    grades_keys = list(grading_scale.keys())

    course_plan = []

    total_units = sum(units_per_course)

    total_points_needed = required_gpa * total_units

    remaining_points = total_points_needed

    for i in range(num_courses):
        units = units_per_course[i]
        avg_points_course = remaining_points / sum(units_per_course[i:])

        closest_points = min(points_values, key=lambda x: abs(x - avg_points_course))
        grade = [k for k, v in grading_scale.items() if v == closest_points][0]

        course_plan.append({
            "Course": f"Course {i+1}",
            "Units": units,
            "Grade": grade,
            "Points": closest_points,
            "Weighted": closest_points * units
        })

        remaining_points -= closest_points * units

    return pd.DataFrame(course_plan)
