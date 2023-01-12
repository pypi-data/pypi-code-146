from tcsoa.gen.Internal_ProjectManagement._2014_10.services import ScheduleManagementService as imp0
from tcsoa.gen.Internal_ProjectManagement._2008_06.services import ScheduleManagementService as imp1
from tcsoa.gen.Internal_ProjectManagement._2007_06.services import ScheduleManagementService as imp2
from tcsoa.gen.Internal_ProjectManagement._2011_06.services import ScheduleManagementService as imp3
from tcsoa.gen.Internal_ProjectManagement._2007_01.services import ScheduleManagementService as imp4
from tcsoa.gen.Internal_ProjectManagement._2012_02.services import ScheduleManagementService as imp5
from tcsoa.gen.Internal_ProjectManagement._2010_04.services import ScheduleManagementService as imp6
from tcsoa.gen.Internal_ProjectManagement._2009_10.services import ScheduleManagementService as imp7
from tcsoa.base import TcService


class ScheduleManagementService(TcService):
    deferredSave = imp0.deferredSave
    getSchedulesToinsert = imp1.getSchedulesToinsert
    loadProgramView = imp2.loadProgramView
    loadProgramView2 = imp3.loadProgramView
    loadResourceAssignments = imp2.loadResourceAssignments
    loadSchedule = imp4.loadSchedule
    loadSchedules = imp1.loadSchedules
    modifySchedule = imp4.modifySchedule
    modifySchedule2 = imp2.modifySchedule
    modifySchedule3 = imp1.modifySchedule
    modifySchedules = imp3.modifySchedules
    pasteTasks = imp0.pasteTasks
    translateFive = imp5.translateFive
    translateFour = imp6.translateFour
    translateOne = imp7.translateOne
    translateThree = imp7.translateThree
    translateTwo = imp7.translateTwo
