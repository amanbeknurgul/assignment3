import os
import csv
import json


class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")
        if os.path.exists(self.filename):
            print(f"File found: {self.filename}")
            return True
        else:
            print(f"Error: {self.filename} not found. Please download the file from LMS.")
            return False

    def create_output_folder(self, folder='output'):
        print("Checking output folder...")
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Output folder created: {folder}/")
        else:
            print(f"Output folder already exists: {folder}/")


class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("Loading data...")
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.students = list(reader)
            print(f"Data loaded successfully: {len(self.students)} students")
            return self.students
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found. Please check the filename.")
            return []
        except Exception as e:
            print(f"Error while reading file: {e}")
            return []

    def preview(self, n=5):
        print(f"First {n} rows:")
        print("------------------------------")
        for student in self.students[:n]:
            print(
                f"{student['student_id']} | {student['age']} | "
                f"{student['gender']} | {student['country']} | GPA: {student['GPA']}"
            )
        print("------------------------------")


class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        valid_students = []

        for student in self.students:
            try:
                score = float(student['final_exam_score'])
                gpa = float(student['GPA'])

                valid_students.append({
                    "student_id": student['student_id'],
                    "country": student['country'],
                    "major": student['major'],
                    "final_exam_score": score,
                    "GPA": gpa
                })
            except ValueError:
                print(f"Warning: could not convert value for student {student.get('student_id', 'Unknown')} — skipping row.")
                continue
            except KeyError:
                print("Warning: Required column not found.")
                continue

        top_10 = sorted(
            valid_students,
            key=lambda x: x['final_exam_score'],
            reverse=True
        )[:10]

        top_scorers = list(filter(lambda s: self.safe_float(s.get('final_exam_score')) > 95, self.students))
        gpa_values = list(map(lambda s: self.safe_float(s.get('GPA')), self.students))
        good_assignments = list(filter(lambda s: self.safe_float(s.get('assignment_score')) > 90, self.students))

        print("------------------------------")
        print("Lambda / Map / Filter")
        print("------------------------------")
        print(f"Students with score > 95 : {len(top_scorers)}")
        print(f"GPA values (first 5) : {gpa_values[:5]}")
        print(f"Students assignment > 90 : {len(good_assignments)}")
        print("------------------------------")

        ranked_top_10 = []
        for i, student in enumerate(top_10, start=1):
            ranked_top_10.append({
                "rank": i,
                "student_id": student["student_id"],
                "country": student["country"],
                "major": student["major"],
                "final_exam_score": student["final_exam_score"],
                "GPA": student["GPA"]
            })

        self.result = {
            "analysis": "Top 10 Students by Exam Score",
            "total_students": len(self.students),
            "top_10": ranked_top_10
        }

        return self.result

    def print_results(self):
        print("------------------------------")
        print("Top 10 Students by Exam Score")
        print("------------------------------")
        for student in self.result.get("top_10", []):
            print(
                f"{student['rank']}. {student['student_id']} | "
                f"{student['country']} | {student['major']} | "
                f"Score: {student['final_exam_score']} | GPA: {student['GPA']}"
            )
        print("------------------------------")

    @staticmethod
    def safe_float(value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0


class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(self.result, f, indent=4)
            print(f"Result saved to {self.output_path}")
        except Exception as e:
            print(f"Error while saving JSON: {e}")


def main():
    fm = FileManager('students.csv')
    if not fm.check_file():
        print("Stopping program.")
        return

    fm.create_output_folder()

    dl = DataLoader('students.csv')
    dl.load()

    if not dl.students:
        print("No data loaded. Program stopped.")
        return

    dl.preview()

    analyser = DataAnalyser(dl.students)
    analyser.analyse()
    analyser.print_results()

    saver = ResultSaver(analyser.result, 'output/result.json')
    saver.save_json()

    print("\nTesting exception handling:")
    wrong_loader = DataLoader("wrong_file.csv")
    wrong_loader.load()


if __name__ == "__main__":
    main()