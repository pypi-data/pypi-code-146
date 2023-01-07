# pylint: disable=line-too-long
translation = {
"LanguageSettingHint": "Language Setting will be taken into effect after restarting Visual Sponge",
"WelcomeHint": "Welcome to use Visual Sponge!",
"bgSelectHint": "Select the color and opacity at top and at bottom, or directly input the RGBA function for the background color.",
"addLabelAlert": 'Please create selections before adding label',
"formCompleteAlert": "Please complete the previous form",
"MovieHint": "Recording the canvas, please wait to finish...",
"MovieOrPrintScreenFinishedHint": "Completed！The file has been saved as:\n",
"PrintScreenHint": "Printing the screen, please wait to finish...",
"AtomSelectionHint": "Select the atoms by AtomSelectionSpec of <a target=_blank href=http://3dmol.csb.pitt.edu/doc/types.html#AtomSelectionSpec>3dmol.js</a></br>Keywords：residue name(resn) coordinate(x),(y),(z) element(elem) residue index(resi) atom name(atom) atom index(serial) number of bonds(bonds) model(model)</br>Example: {model: 0, atom: 'OW', byres: true}",
}
translation.update({
"HelpHelpHint":
"""Use HELP(command) to get the detailed help of the command.
    Example:
        HELP("HELP")
    All available commands are: """,
"CommandHelpHelp":
"""HELP(command=None)
    gives the help of the command.

    :param command: the string of the command
    :return: the help of the command""",
"CommandHelpConfigure":
"""CONFIGURE(section, option, value=None)
    gets or sets the value of the option in the configuration file.

    :param section: the section of the option
    :param option: the name of the option
    :param value: the value which will be set to if not None
    :return: the value of the option""",
"CommandHelpDefault":
"""DEFAULT(mid)
    sets the mid-th model as the default model

    :param mid: the id of the model
    :return: the default model""",
"CommandHelpDelete":
"""DELETE(obj, id_)
    deletes the mid-th instance of the object

    :param obj: the object to delete， now only Model supported
    :param id: the id of the instance to delete
    :return: the deleted instance""",
"CommandHelpHide":
"""HIDE(obj, id_)
    hides the mid-th instance of the object

    :param obj: the object to hide， now only Model supported
    :param id: the id of the instance to hide
    :return: the hidden instance""",
"CommandHelpModel":
"""MODEL(m, format_=None, **kwargs)
    loads the model

    :param m: the model to load
    :param format_: the format of the model
    :return: the loaded model""",
"CommandHelpMovie":
"""MOVIE(filename, fps=60, bitRate=8500000, start=0, stop=-1, stride=1, interval=100)
    makes a movie

    :param filename: the file name to save the movie. The format will be guessed based on the suffix
    :param fps: frame per second
    :param bitRate: bit per second
    :param start: the start frame of the trajectorry
    :param stop: the stop frame of the trajectorry. If negative, the last |stop| frame will be used
    :param stride: the strie frame of the trajectory
    :param interval: the trajectory frames move every interval miloseconds
    :return: the absolute file name""",
"CommandHelpPrintscreen":
"""PRINTSCREEN(filename)
    print screen

    :param filename: the file name to save the print screen. The format will be guessed based on the suffix
    :return: the absolute file name""",
"CommandHelpShow":
"""SHOW(obj, id_)
    shows the mid-th instance of the object

    :param obj: the object to show， now only Model supported
    :param id: the id of the instance to show
    :return: the shown instance""",
"CommandHelpTraj":
"""TRAJ(traj, format_=None, m=None, append=False, **kwargs):
    loads the trajectory

    :param traj: the trajectory
    :param format_: the format of the trajectory
    :param m: the model to load the trajectory。If None，the default model will be used (Model.WORKING_MODEL)
    :param append: whether to append or replace the original trajectory
    :return: the model loaded the trajectory""",
"CommandHelpVersion":
"""VERSION()
    gives the version information

    :return: version information""",
})
