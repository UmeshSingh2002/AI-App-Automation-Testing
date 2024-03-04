import time

from src.app_tester_core import loadAppTesters, loadConfig, runTests
from src.report_generator import generateReport

# ------- Main Entrypoint -------
def main():
    upload_images = True

    csv_file_path = './pic-data.csv'
    app_tester_instances = loadAppTesters()

    for tester in app_tester_instances:
        tester_name = f"{type(tester).__name__}"
        print(f'\n######### Testing App: {tester_name} #########')

        driver = tester.initializeDriver()
        if driver is None:
            continue

        test_cases = loadConfig(driver, csv_file_path, upload_images=upload_images)
        upload_images = False # Only need to transfer on first run
        time.sleep(5)

        passed_tests, passed_plant, passed_disease, total_tests, test_errors = runTests(driver, tester, test_cases)

        print('------- Tests Complete -------')
        print(f'\n\tTotal Test Count: {total_tests}')
        print(f'\tTotal Passed Tests: {passed_tests}')
        print(f'\tTotal Test Errors: {test_errors}')

        metric = {
            'tester_name': tester_name,
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'plant_only_pass': passed_plant,
            'disease_only_pass': passed_disease,
            'test_errors': test_errors
        }

        accuracy = passed_tests/total_tests * 100
        plant_accuracy = passed_plant / total_tests * 100
        disease_accuracy = passed_disease / total_tests * 100

        print(f'\tTotal Accuracy: {accuracy}%')
        print(f'\t\t- Plant Identification Only Accuracy: {passed_plant}/{total_tests} {plant_accuracy}%')
        print(f'\t\t- Disease Identification Only Accuracy: {passed_disease}/{total_tests} {disease_accuracy}%')

        driver.quit()

        time.sleep(5)
    
        generateReport([metric])

if __name__ == '__main__':
    main()