from .verify import get_errors_fails, mark_incomplete, mark_complete
import os
task1_id = '032dcdb6-69e1-450c-96aa-819a45d6aed3' # Iteratively check if the input is a valid guess
task2_id = '93eb2ed4-e6e3-40e5-9a7d-a774d9e5f8e6' # Check whether the guess is in the word
task3_id = '5ea59e77-6f08-41e7-99e6-eb73a9709d22' # Create functions to run the checks
task4_id = 'a3bc621a-19e0-4bff-bc9e-1eba3ee09160' # Update your documentation

task_list = [
    task1_id,
    task2_id,
    task3_id,
    task4_id
]

if 'milestone_3_p1.txt' in os.listdir('.'):
    errors = get_errors_fails('milestone_3_p1.txt')
    if len(errors) != 0:
        mark_incomplete(task1_id, errors['test_presence_milestone_3'])
