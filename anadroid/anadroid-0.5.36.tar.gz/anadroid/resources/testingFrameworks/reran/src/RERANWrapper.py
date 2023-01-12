import os
import sys
import argparse
from subprocess import call, check_output, Popen, PIPE
from multiprocessing import Process
import os.path as path

default_tests_path="tests"
translate_jar_path= os.path.join("build", "RERANTranslate.jar")
replay_bin_path= os.path.join("build", "replay")

def record_events(filename):
	cmd = "adb shell getevent -t > " + filename
	pipes = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
	std_out, std_err = pipes.communicate()
	pipes.wait()

class RERANWrapper(object):
	"""docstring for RERANWrapper"""
	def __init__(self, tests_folder, translator_jar_path, replay_bin_path):
		self.translator_jar_path = translator_jar_path
		self.replay_bin_path = replay_bin_path
		self.tests_folder = tests_folder


	def pushToDevice(self, in_name):
		filename=path.basename(in_name)
		os.system("adb push " + in_name + " /sdcard/" + filename)
		os.system("adb push " + self.replay_bin_path + " /sdcard/")
		os.system("adb shell su -c \" cp /sdcard/" +filename+ " /data/local/ \"" )
		os.system("adb shell su -c \" cp /sdcard/replay" + " /data/local/ \"" )
		os.system("adb shell su -c \" chmod 777  /data/local/replay\"")

	def replay(self, app_id, in_name):
		filename=path.basename(in_name)
		# run replay program with 0 delay time
		os.system("adb shell su -c \" /data/local/./replay /data/local/" + filename+ " 0\"" )


	def translate_events(self, fileDir, filename):
		new_file="translated_" + filename
		os.system(f"java -jar {self.translator_jar_path} {os.path.join(fileDir, filename)} {os.path.join(fileDir, new_file)}")
		return os.path.join(fileDir, new_file)


	def record(self, app_id, out_name):
		#check if exists directory for this app
		dirname = os.path.join(self.tests_folder, app_id)
		if not os.path.exists(dirname) or not os.path.isdir(dirname):
			os.mkdir(dirname)
		# creates killable process that runs record_events function, since there isn't an easy way to kill threads in python
		p = Process(target=record_events, args=(str(os.path.join(dirname, out_name)),))
		p.start()
		input("press any key to stop recording")
		p.terminate()
		the_new_file = self.translate_events(str(dirname), out_name)
		print(f"translated events to  {the_new_file}")
		return the_new_file


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-r", "--replaypath", default=replay_bin_path, type=str)
	parser.add_argument("-tf", "--testfolder", default=default_tests_path, type=str)
	parser.add_argument("-jar", "--jarpath", default=translate_jar_path, type=str)
	parser.add_argument("-t", "--task", default="all", type=str)
	parser.add_argument("-o", "--outputfile", default="reran.out", type=str)
	parser.add_argument("-a", "--appid", default="unknown_app", type=str)
	args = parser.parse_args()
	task_name = args.task
	reran = RERANWrapper(args.testfolder, args.jarpath, args.replaypath)
	if task_name == "record":
		reran.record(args.appid, args.outputfile)
	elif task_name == "replay":
		reran.replay(args.appid, args.outputfile)
	elif task_name == "push":
		reran.pushToDevice(args.outputfile)
	elif task_name == "all":
		new_file = reran.record(args.appid, args.outputfile)
		reran.pushToDevice(new_file)
		reran.replay(args.appid, new_file)
