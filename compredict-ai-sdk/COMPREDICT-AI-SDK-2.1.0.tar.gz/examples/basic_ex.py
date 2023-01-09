from compredict.client import api
from compredict.resources import resources
from time import sleep
from environ import Env
from sys import exit

env = Env()
env.read_env()

token = env("COMPREDICT_AI_CORE_KEY")
callback_url = env("COMPREDICT_AI_CORE_CALLBACK", None)
fail_on_error = env("COMPREDICT_AI_CORE_FAIL_ON_ERROR", False)

client = api.get_instance(token=token, callback_url=callback_url)
client.fail_on_error(option=fail_on_error)

# get a graph
# algorithm = client.get_algorithm("an-algorithm-id")
# graph = algorithm.get_detailed_graph()
# new_file = open('algorithm-input-graph.png', 'wb')
# shutil.copyfileobj(graph, new_file)
# graph.close()


algorithms = client.get_algorithms()

# Check if the user has algorithms to predict
if len(algorithms) == 0:
    print("No algorithms to proceed!")
    exit()

algorithm = algorithms[0]

tmp = algorithm.get_detailed_template()
tmp.close()  # It is tmp file. close the file to remove it.

data = dict()  # data for predictions

results = algorithm.run(data, evaluate=False)

if isinstance(results, resources.Task):
    print(results.job_id)

    while results.status != results.STATUS_FINISHED:
        print("task is not done yet.. waiting...")
        sleep(15)
        results.update()

    if results.success is True:
        print(results.predictions)
    else:
        print(results.error)

else:
    print(results.predictions)
