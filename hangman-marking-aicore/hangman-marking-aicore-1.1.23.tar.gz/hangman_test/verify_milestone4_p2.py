from .verify import get_errors_fails, mark_incomplete, mark_complete
import os
task1_id = 'c82f56aa-237b-49c6-ba48-67c67e80f569' # Create the class
task2_id = 'f64ba6c9-f685-4c47-88a5-7503ada30b8d' # Create methods for running the checks
task3_id = '2f2ccea4-f88e-4bbe-8063-1a3cf77c6d6d' # Define what happens if the letter is in the word
task4_id = '04dc4041-10bf-4c02-84cd-892b1913adf4' # Define what happens if the letter is NOT in the word
task5_id = '56c6b4ba-e027-46e2-98e0-bed884e02336' # Update your documentation

task_name_list = [
    ('test_attributes', task1_id),
    ('test_methods', task2_id),
    ('test_correct_guess', task3_id),
    ('test_incorrect_guess', task4_id),
    ('test_presence_readme', task5_id),
]

if 'milestone_4_p2.txt' in os.listdir('.'):
    errors = get_errors_fails('milestone_4_p2.txt')
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
