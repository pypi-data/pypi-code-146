#!/usr/bin/env python
""" PIPE STEP MYSTEP - Version 1.0.0

    REPLACE THIS TEXT WITH INFORMATION ON YOUR STEP

    Information from StepParent:
    This module defines the pipeline step parent object. Pipe steps are
    the modules responsible for all data reduction. They are called by
    the pipeline and work with pipedata objects. All pipe step objects are
    descendants from stepparent. Pipe steps are callable objects that return
    the reduced data product (as pipedata object).
    
    @author: YOUR NAME HERE
"""

import logging # logging object library
from darepype.drp.stepparent import StepParent

class StepMyStep(StepParent):
    """ DarePype Step MyStep Object
        The object is callable. It requires a valid configuration input
        (file or object) when it runs.
    """
    stepver = '0.1' # pipe step version
    
    def setup(self):
        """ ### Names and Parameters need to be Set Here ###

            Sets the internal names for the function and for saved files.

            Defines the input parameters for the current pipe step.
            Setup() is called at the end of __init__
            The parameters are stored in a list containing the following
            information:
            - name: The name for the parameter. This name is used when
                    calling the pipe step from command line or python shell.
                    It is also used to identify the parameter in the pipeline
                    configuration file.
            - default: A default value for the parameter. If nothing, set
                       '' for strings, 0 for integers and 0.0 for floats
            - help: A short description of the parameter.
        """
        ### Set Names
        # Name of the pipeline reduction step (same case as config file)
        self.name='mystep'
        # Identifier for saved file names.
        self.procname = 'MYS'
        # Set Logger for this pipe step
        self.log = logging.getLogger('pipe.step.%s' % self.name)
        ### Set Parameter list
        # Clear Parameter list
        self.paramlist = []
        # Append parameters
        self.paramlist.append(['sampar', 1.0,
            'Sample Parameter - parent only - no practical use'])

    def run(self):
        """ Runs the data reduction algorithm. The self.datain is run
            through the code, the result is in self.dataout.
        """
        self.log.debug('Running step %s' % self.name)
        # Minimal code set dataout to datain
        self.dataout = self.datain
    
    def reset(self):
        """ Resets the step to the same condition as it was when it was
            created. Internal variables are reset, any stored data is
            erased.
        """
        self.log.debug('Reset: done')
            
if __name__ == '__main__':
    """ Main function to run the pipe step from command line on a file.
        Command:
          python stepparent.py input.fits -arg1 -arg2 . . .
        Standard arguments:
          --config=ConfigFilePathName.txt : name of the configuration file
          -t, --test : runs the functionality test i.e. pipestep.test()
          --loglevel=LEVEL : configures the logging output for a particular level
          -h, --help : Returns a list of parameters
    """
    StepMyStep().execute()

""" === History ===
"""
