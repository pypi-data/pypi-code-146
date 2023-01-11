#!/usr/bin/env python
from seams import Seams
from abc import ABC, abstractmethod
import os
import tempfile
import json
import calendar
import datetime
import sys
import argparse
from seams.severity import Severity
from traceback import format_tb
class Pipeline(ABC):
    

    def __init__(self, SECRET, APP_ID, TENANT_ID, URL=None):
        '''
        Create an instance of the Pipeline interface
        '''
        self.result_files = []
        self.logs = []
        self.user_logs = []
        self.secret = SECRET
        if URL:
            self.seams = Seams(URL)
        else:
            self.seams = Seams()
        self.seams.connect(SECRET, APP_ID, TENANT_ID)

    
    @abstractmethod
    def run(self, data):
        '''
        Abstract class that will be overwritten by the user
        '''
        print("ERROR: this method should be overridden")


    def start(self):
        '''
        starts a pipeline and does all the buildup and tear down for every pipeline

        :returns:
            JSON object representing the status of the completed pipeline
        '''
        try:
            #getting parameters and setting them to appropriate class variables
            parameters = self.__get_parameters()
            self.vertex_id = parameters["vertex_id"]
            self.tenant_id = parameters["tenant_id"]
            #setting pipeline status to IN PROGRESS
            self.update_pipeline_status_in_progress() 
            #getting the run parameters of pipeline
            data = json.loads(self.seams.get_vertex_by_id(self.tenant_id, self.vertex_id)["runParameters"])

            if "Files" in data:
                #downloading files
                self.log(Severity.INFO, "downloading files...")
                data["files"] = self.download_input_files()
            #running abstract run method
            self.run(data)
            #setting pipeline to DONE when finished
            return self.update_pipeline_status_done()
        except Exception as e:
            print("exception: ", e)
            #if pipeline fails setting pipeline to ERROR and printing out the stack trace
            etype, value, tb = sys.exc_info()
            #formats the exception type into a string and grabs only the class type of the error
            exception_type = str(type(value)).replace("'", "").split(" ")[1][:-1]
            if exception_type == "KeyError":
                self.log(Severity.ERROR, exception_type, ": Input parameter ", str(value).replace("'", ""), " does not match any of the expected arguments for this pipeline", for_user=True)
            self.log(Severity.ERROR, format_tb(tb))
            self.log(Severity.ERROR, exception_type, ": ", str(value).replace("'", ""), for_user=True)
            self.update_pipeline_status_error()


    def update_pipeline_status_in_progress(self):
        '''
        sets the pipeline status to IN PROGRESS

        :returns:
            JSON object representing the status of the completed pipeline
        '''
        attributes = {
            "status": "IN PROGRESS"
        }
        return self.seams.update_vertex(self.tenant_id, self.vertex_id, "PipelineRun", attributes)
    

    def update_pipeline_status_done(self):
        '''
        sets the pipeline status to DONE

        :returns:
            JSON object representing the status of the completed pipeline
        '''
        upload_log_files = self.__build_log_upload_files()
        attributes = {
            "status": "DONE",
            "runResults": self.result_files,
            "logs": upload_log_files[0],
            "userLogs": upload_log_files[1]
        }
        # Iterates over all the result files and adds them as an edge to the pipelineRun
        for item in self.result_files:
            self.seams.attach_edges(self.tenant_id, self.vertex_id, "Has Result File", [item["id"]])
        return self.seams.update_vertex(self.tenant_id, self.vertex_id, "PipelineRun", attributes)
        

    def update_pipeline_status_error(self):
        '''
        sets the pipeline status to ERROR

        :returns:
            JSON object representing the status of the completed pipeline
        '''
        upload_log_files = self.__build_log_upload_files()
        attributes = {
            "status": "ERROR",
            "runResults": self.result_files,
            "logs": upload_log_files[0],
            "userLogs": upload_log_files[1]
        }
        # Iterates over all the result files and adds them as an edge to the pipelineRun
        for item in self.result_files:
            self.seams.attach_edges(self.tenant_id, self.vertex_id, "Has Result File", [item["id"]])
        return self.seams.update_vertex(self.tenant_id, self.vertex_id, "PipelineRun", attributes)


    def download_input_files(self):
        '''
        downloads any files needed by the pipeline

        :returns:
            list of file paths for files downloaded for the pipeline
        '''
        #gets the run parameters of the pipeline
        data = json.loads(self.seams.get_vertex_by_id(self.tenant_id, self.vertex_id)["runParameters"])
        files = []
        #downloads files in pipeline, adds them to a temp file, adds file path to a list, attaches file vertices to pipelineRun
        for item in data["Files"]:
            self.seams.attach_edges(self.tenant_id, self.vertex_id, "Has Input File", [item['vertexId']])
            download = self.seams.download_files(self.tenant_id, item["vertexId"])
            for item in download:
                temp_file_full_path = os.path.join(tempfile.gettempdir(), item)
                files.append(temp_file_full_path)
                f = open(temp_file_full_path, "w", encoding="utf-8")
                f.write(download[item])
                f.close()
        return files


    def create_chart_from_file(self, parent_vertex_id, file_vertex_id, chart_name, x_label_column, y_label_column, chart_type):
        '''
        Creates a chart vertex type and attaches an edge to connect it to the parent

        :param parent_vertex_id:
            Vertex id of the vertex the edge is coming from
        :param file_vertex_id:
            Vertex id of the file you want to create the chart from
        :param chart_name"
            Name of the chart, this will also be the name of the Chart vertex (something like "Pressure vs Time")
        :param x_label_column:
            X data column name
        :param  y_label_column:
            Y data column name
        :param chart_type:
            Type of chart to display "line", "pie", "doughnut", "scatter", "vertical", "horizontal" (last two are different types of bar charts)

        :returns (edge_result, chart_vertex_id): 
            Tuple of edge connection result and new chart vertex id
        '''
        attributes = {
            "datasource_file_id": file_vertex_id,
            "title": chart_name,
            "dataset_1_labels_column": x_label_column,
            "dataset_1_values_column": y_label_column,
            "type": chart_type
        }
        chart_vertex = self.seams.create_vertex(self.tenant_id, "Chart", chart_name, attributes)
        edge_result = self.seams.attach_edges(self.tenant_id, parent_vertex_id, "Charts", [chart_vertex["id"]])
        return (edge_result, chart_vertex["id"])
    

    def upload_files(self, caption, files, file_type):
        '''
        uploads any files 

        :returns:
            JSON object representing the status of the upload
        '''
        return self.seams.upload_files(self.tenant_id, caption, files, file_type=file_type)


    def get_result_files(self):
        '''
        returns a list of all files created by the pipeline

        :returns:
            list of all files created by the pipelie
        '''
        return self.result_files


    def add_result_file(self, file_vertex_id, label, name):
        '''
        adds a new result file to the result files list

        '''
        new_file = {
            "id": file_vertex_id,
            "label": label, 
            "name": name
        }
        self.result_files.append(new_file)
    

    def get_tenant_id(self):
        '''
        Returns tenant id
        '''
        return self.tenant_id


    def log(self, log_severity, *args, for_user=False, print_out=True):
        '''
        logs any stdout or stderr and saves it to the pipeline run vertex

        :param log_severity:
            The severity of the log, severity will be verified by the Severity class  **REQUIRED**
        :param *args:
            Comma delimited list of anything the user wishes to print out  **REQUIRED**
        :param for_user:
            False by default, if set to True will send the log to userLogs  **REQUIRED**
        '''
        #gets UTC time
        date = datetime.datetime.now(datetime.timezone.utc)
        result = ""
        #check if severity exists
        temp_args = args
        if isinstance(log_severity, Severity):
            for arg in temp_args:
                if isinstance(arg, list):
                    #checks if each item is a dict
                    temp = ""
                    if isinstance(arg[0], dict):
                        for item in arg:
                            temp = temp + json.dumps(item) + ", "
                        temp = temp.rstrip(temp[-2:])
                        result = result + "[" + "".join(temp) + "]"
                    else:
                        result = result + " ".join(arg)
                elif isinstance(arg, dict):
                    result = result + json.dumps(arg)
                else:
                    result = result + str(arg)
            #creating log object
            log = {
                "severity": log_severity.name,
                "date": str(date),
                "message": result
            }
            #builds readable string and prints it out
            str_log = "{}   {}   {}".format(log["severity"], date, log["message"])
            if print_out:
                print(str_log)
            #appends to logs and user_logs if requested
            self.logs.append(log)
            if for_user:
                self.user_logs.append(log)


    def create_new_file(self, filename):
        """Creates a new tempfile and returns the filepath

        Returns tuple with filepath and filename of new file

        """
        i = 0
        split_name = filename.split(".")
        new_filename = ""
        for item in split_name:
            if i == len(split_name)-1:
                new_filename = new_filename + "_" + str(datetime.datetime.now()) + "." + item
            else:
                new_filename = new_filename + "." + item
            i+=1
        new_filename = new_filename.replace(" ", "_").replace(":", ".").lstrip(".")
        upload_file_path = os.path.join(tempfile.gettempdir(), new_filename)
        return upload_file_path, new_filename


    def __build_log_upload_files(self):
        '''
        private method to build and upload log files

        :returns:
            (vertex_id of log file, vertex_id of user_log file)
        '''
        #creates new tempfile for logs
        logs_name = self.create_new_file("pipeline_logs.json")
        log_temp_file_full_path = os.path.join(tempfile.gettempdir(), logs_name[1])
        #opens/writes/closes new temp log file
        log_file = open(log_temp_file_full_path, "w", encoding="utf-8")
        log_file.write(str(self.logs))
        log_file.close()
        #uploads log file and attaches it as an edge to the pipeline run
        log_file_upload = self.upload_files("logs for {}".format(self.vertex_id), log_temp_file_full_path, file_type="File")
        self.seams.attach_edges(self.tenant_id, self.vertex_id, "Logs", [log_file_upload[0]["id"]])
        #creates new tempfile for user_logs
        user_logs_name = self.create_new_file("pipeline_user_logs.json")
        user_log_temp_file_full_path = os.path.join(tempfile.gettempdir(), user_logs_name[1])
        #opens/writes/closes new temp user_log file
        user_log_file = open(user_log_temp_file_full_path, "w", encoding="utf-8")
        user_log_file.write(str(self.user_logs))
        user_log_file.close()
        #uploads user_log file and attaches it as an edge to the pipeline run
        user_log_file_upload = self.upload_files("user logs for {}".format(self.vertex_id), user_log_temp_file_full_path, file_type="File")
        self.seams.attach_edges(self.tenant_id, self.vertex_id, "UserLogs", [user_log_file_upload[0]["id"]])

        return (log_file_upload[0]["id"], user_log_file_upload[0]["id"])


    def __get_parameters(self):
        '''
        private method to get the parameters in a pipeline

        :returns:
            dict of all the command line arguments sent to the pipeline
        '''
        parser = argparse.ArgumentParser()
        parser.add_argument("tenant_id",
                            help="Vertex ID of the pipeline job")
        parser.add_argument("vertex_id",
                            help="Vertex ID of the pipeline job")

        args = parser.parse_args()
        if not (args.tenant_id and args.vertex_id):
            parser.error(
                "Tenant Id and Vertex Id required - do -h for help")

        parameters = {"tenant_id": args.tenant_id, "vertex_id": args.vertex_id}
        return parameters
