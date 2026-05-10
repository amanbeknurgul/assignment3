class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        print("Not implemented — use a child class")

    def print_results(self):
        for key, value in self.result.items():
            print(f"{key}: {value}")

    def __str__(self):
        return f"DataAnalyser: base class, {len(self.students)} students"


class TopStudentsAnalyser(DataAnalyser):
    def __init__(self, students):
        super().__init__(students)

    def analyse(self):
        sorted_students = sorted(
            self.students,
            key=lambda student: float(student["final_exam_score"]),
            reverse=True
        )

        self.result = {
            "total_students": len(self.students),
            "top_10": sorted_students[:10]
        }

    def print_results(self):
        print("\n==============================")
        print("TOP STUDENTS ANALYSIS REPORT")
        print("==============================")
        print(f"total_students: {self.result['total_students']}")
        print("top_10:")

        for student in self.result["top_10"]:
            print(
                student["student_id"],
                "| score:",
                student["final_exam_score"],
                "| GPA:",
                student["GPA"],
                "| country:",
                student["country"]
            )

        print("==============================")

    def __str__(self):
        return f"TopStudentsAnalyser: Top Students Analysis, {len(self.students)} students"


class CountryAnalyser(DataAnalyser):
    def __init__(self, students):
        super().__init__(students)

    def analyse(self):
        countries = {}

        for student in self.students:
            country = student["country"]
            countries[country] = countries.get(country, 0) + 1

        top_3 = sorted(
            countries.items(),
            key=lambda item: item[1],
            reverse=True
        )[:3]

        self.result = {
            "total_students": len(self.students),
            "total_countries": len(countries),
            "top_3": top_3
        }

    def print_results(self):
        print("\n==============================")
        print("COUNTRY ANALYSIS REPORT")
        print("==============================")
        super().print_results()
        print("==============================")

    def __str__(self):
        return f"CountryAnalyser: Country Analysis, {len(self.students)} students"