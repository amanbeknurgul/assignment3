import csv


class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            self.students = list(reader)

        print(f"Loaded {len(self.students)} students.")

    def preview(self):
        print("\nPreview:")

        for student in self.students[:3]:
            print(
                student["student_id"],
                "| Country:",
                student["country"],
                "| GPA:",
                student["GPA"],
                "| Final score:",
                student["final_exam_score"]
            )