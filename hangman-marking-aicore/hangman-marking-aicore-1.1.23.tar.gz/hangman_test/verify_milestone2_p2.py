from .verify import get_errors_fails, mark_incomplete, mark_complete
import os
task1_id = '3f496682-807d-4ba4-aa64-c09ebba9b83a' # Define the list of possible words
task2_id = '62158fc2-ba1d-49f4-aee0-66ec01f63baa' # Choose a random word from the list
task3_id = 'd592e5f4-6606-4a12-bbf2-7c160a09fd66' # Ask the user for an input
task4_id = '3de4ce88-cd39-4f85-a775-529a41c2fa17' # Check that the input is a single character
task5_id = '75e80e7f-ec62-459a-8858-9d2eb9d4beb6' # Start documenting your experience
task_name_list = [
                    ('test_length', task1_id),
                    ('test_random', task2_id),
                    ('test_ask_input', task3_id),
                    ('test_check_input', task4_id),
                    ('test_presence_readme', task5_id),
]

if 'milestone_2_p2.txt' in os.listdir('.'):
    errors = get_errors_fails('milestone_2_p2.txt')
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
