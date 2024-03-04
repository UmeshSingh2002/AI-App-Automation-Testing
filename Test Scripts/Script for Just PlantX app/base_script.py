# Python/Pytest
import pytest
import os
import csv
import base64
import time
import importlib

# ------- UTILITIES -------

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
        base64_data = base64.b64encode(binary_data).decode('utf-8')

    return base64_data


# ------- TESTING INFRASTRUCTURE -------

# Load AppTester implementations from app_scripts directory and instantiate.
def loadAppTesters():
    implementation_dir = f'./app_scripts'

    # Load all Python files in the directory
    implementation_files = [f[:-3] for f in os.listdir(implementation_dir) if f.endswith('.py') and f != '__init__.py']

    app_tester_instances = []

    # Import each implementation dynamically and run functions
    for implementation_file in implementation_files:
        module_name = f"{implementation_dir}.{implementation_file}"
        module = importlib.import_module(f'.{implementation_file}', '.app_scripts')

        # Assuming each implementation class has the same name as the file
        app_tester_class = getattr(module, implementation_file)

        # Create an instance of the implementation class
        app_tester = app_tester_class()
        app_tester_instances.append(app_tester)
        print(f'\n######### Testing App: {implementation_file} #########')

    return app_tester_instances

# Load Image paths and ground truth values from pic-data.csv
def loadConfig(driver, csv_file_path, upload_images=True):
    path_base = os.getcwd()
    index = 0
    img_gt_pairs = []

    with open(csv_file_path, 'r') as csv_file:
        if upload_images:
            print(f'\nUploading test images...')

        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if upload_images:
                input_image = row['input_image']
                img_path = os.path.join(path_base, 'pic', input_image)
                destination_path = f"/storage/emulated/0/Pictures/{'0'*(3 - len(str(index)))}{index}.png"

                img_base64 = image_to_base64(img_path)

                print(f'\t- {destination_path}')
                driver.push_file(destination_path, img_base64)

            img_gt_pairs.append(row)
            index += 1

    print(f'\nLoaded config from {csv_file_path}\n')
    return img_gt_pairs

# Both expected_result and actual_result are in the format:
#   - [PLANT_NAME, DISEASE_NAME]
def validate_test_case(expected_result, actual_result):
    # Check if both lists have size 2
    if len(expected_result) != 2 or len(actual_result) != 2:
        raise ValueError("Both results must have size 2.")

    # Convert values and strings to lowercase for case-insensitive comparison
    expected_plant = expected_result[0].lower()
    expected_disease = expected_result[1].lower()
    predicted_plant = actual_result[0].lower()
    predicted_disease = actual_result[1].lower()

    # Check if the corresponding strings contain the corresponding values
    correct_plant = expected_plant in predicted_plant
    correct_disease = expected_disease in predicted_disease

    return correct_plant, correct_disease

# Run test cases on a given AppTester instance
def runTests(driver, tester, test_cases):
    results = []
    init_index = 1 # lexically sorted image list index
    
    passed_tests = 0
    passed_plant = 0
    passed_disease = 0

    for test_index in range(init_index, len(test_cases)):
        row = test_cases[test_index-1]
        input_image = row['input_image']
        ground_truth = [row['expected_plant'], row['expected_disease']]

        print(f'\nAnalyzing {input_image}')
        print(f'\tExpected Result: {ground_truth}')

        extracted_result = tester.analyzeImage(driver, test_index)
        results.append(extracted_result)
        print(f'\tActual Result: {extracted_result}')

        if None not in extracted_result:
            plant_correct, disease_correct = validate_test_case(ground_truth, extracted_result)
        else:
            plant_correct = False
            disease_correct = False

        if plant_correct and disease_correct:
            print('\t----------PASS-----------')
            passed_tests += 1
        else:
            print('\t----------FAIL-----------')
            if plant_correct:
                passed_plant += 1
            if disease_correct:
                passed_disease += 1

    return (passed_tests, passed_plant, passed_disease, test_index)

def main():
    csv_file_path = './pic-data.csv'
    app_tester_instances = loadAppTesters()

    for tester in app_tester_instances:
        driver = tester.initializeDriver()

        test_cases = loadConfig(driver, csv_file_path, upload_images=True)
        time.sleep(5)

        passed_tests, passed_plant, passed_disease, total_tests = runTests(driver, tester, test_cases)

        print('------- Tests Complete -------')
        print(f'\n\tTotal Test Count: {total_tests}')
        print(f'\tTotal Passed Tests: {passed_tests}')

        accuracy = passed_tests/total_tests * 100
        plant_accuracy = passed_plant / total_tests * 100
        disease_accuracy = passed_disease / total_tests * 100
        print(f'\n\tTotal Accuracy: {accuracy}%')
        print(f'\t\t- Plant Identification Accuracy: {passed_plant}/{total_tests} {plant_accuracy}%')
        print(f'\t\t- Disease Identification Accuracy: {passed_disease}/{total_tests} {disease_accuracy}%')

        driver.quit()

if __name__ == '__main__':
    main()