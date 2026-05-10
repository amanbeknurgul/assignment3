from analytics import FileManager, DataLoader, ResultSaver, Report
from analytics.analyser import TopStudentsAnalyser, CountryAnalyser


def main():
    filename = "students.csv"

    file_manager = FileManager(filename)

    if not file_manager.check_file():
        return

    file_manager.create_output_folder()

    data_loader = DataLoader(filename)
    data_loader.load()
    data_loader.preview()

    print("\n------------------------------")
    print("Running all analysers:")
    print("------------------------------")

    analysers = [
        TopStudentsAnalyser(data_loader.students),
        CountryAnalyser(data_loader.students)
    ]

    for analyser in analysers:
        print(analyser)
        analyser.analyse()
        analyser.print_results()

    saver = ResultSaver({}, "output/result.json")
    report = Report(analysers[0], saver)
    report.generate()


if __name__ == "__main__":
    main()