from .verify import get_errors_fails, mark_incomplete, mark_complete
import os
task1_id = '3f496682-807d-4ba4-aa64-c09ebba9b83a' # Define the list of possible words
task2_id = '62158fc2-ba1d-49f4-aee0-66ec01f63baa' # Choose a random word from the list
task3_id = 'd592e5f4-6606-4a12-bbf2-7c160a09fd66' # Ask the user for an input
task4_id = '3de4ce88-cd39-4f85-a775-529a41c2fa17' # Check that the input is a single character
task5_id = '75e80e7f-ec62-459a-8858-9d2eb9d4beb6' # Start documenting your experience

if 'milestone_2_p1.txt' in os.listdir('.'):
    errors = get_errors_fails('milestone_2_p1.txt')
    if len(errors) != 0:
        mark_incomplete(task1_id, errors['test_presence_milestone_2'])
