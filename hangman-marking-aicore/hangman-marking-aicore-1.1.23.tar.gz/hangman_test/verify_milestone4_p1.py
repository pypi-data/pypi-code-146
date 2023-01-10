from .verify import get_errors_fails, mark_incomplete, mark_complete
import os
task1_id = 'c82f56aa-237b-49c6-ba48-67c67e80f569' # Create the class
task2_id = 'f64ba6c9-f685-4c47-88a5-7503ada30b8d' # Create methods for running the checks
task3_id = '2f2ccea4-f88e-4bbe-8063-1a3cf77c6d6d' # Define what happens if the letter is in the word
task4_id = '04dc4041-10bf-4c02-84cd-892b1913adf4' # Define what happens if the letter is NOT in the word
task5_id = '56c6b4ba-e027-46e2-98e0-bed884e02336' # Update your documentation

task_list = [
    task1_id,
    task2_id,
    task3_id,
    task4_id,
    task5_id
]

if 'milestone_4_p1.txt' in os.listdir('.'):
    errors = get_errors_fails('milestone_4_p1.txt')
    if len(errors) != 0:
        if 'test_presence_milestone_4' in errors:
            mark_incomplete(task1_id, errors['test_presence_milestone_4'])
        elif 'test_presence_class' in errors:
            mark_incomplete(task1_id, errors['test_presence_class'])
