from .verify import get_errors_fails, mark_incomplete, mark_complete
import os
task1_id = '032dcdb6-69e1-450c-96aa-819a45d6aed3' # Iteratively check if the input is a valid guess
task2_id = '93eb2ed4-e6e3-40e5-9a7d-a774d9e5f8e6' # Check whether the guess is in the word
task3_id = '5ea59e77-6f08-41e7-99e6-eb73a9709d22' # Create functions to run the checks
task4_id = 'a3bc621a-19e0-4bff-bc9e-1eba3ee09160' # Update your documentation

task_name_list = [
    ('test_iterative_ask_letter', task1_id),
    ('test_check_letter', task2_id),
    ('test_function_definition', task3_id),
    ('test_presence_readme', task4_id),
]

if 'milestone_3_p2.txt' in os.listdir('.'):
    errors = get_errors_fails('milestone_3_p2.txt')
    print(errors)
    if len(errors) == 0:
        for task in task_name_list:
            mark_complete(task[1])
    else:
        for task_name, task_id in task_name_list:
            if task_name not in errors:
                mark_complete(task_id)
            else:
                mark_incomplete(task_id, errors[task_name])
                break
