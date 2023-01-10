from .verify import get_errors_fails, mark_incomplete, mark_complete
import os
task1_id = '6abbafb7-59a3-481a-9b1f-837e37b5826c' # Code the logic of the game
task2_id = 'f9464de6-74a0-43f7-aa62-91f2677b267f' # Document your experience

task_name_list = [
    ('test_play_hangman', task1_id),
    ('test_presence_readme', task2_id),
]

if 'milestone_5_p2.txt' in os.listdir('.'):
    errors = get_errors_fails('milestone_5_p2.txt')
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
