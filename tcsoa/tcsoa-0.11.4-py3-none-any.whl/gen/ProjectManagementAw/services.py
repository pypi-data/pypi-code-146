from tcsoa.gen.ProjectManagementAw._2019_06.services import ScheduleManagementAwService as imp0
from tcsoa.gen.ProjectManagementAw._2017_06.services import ScheduleManagementAwService as imp1
from tcsoa.gen.ProjectManagementAw._2018_12.services import ScheduleManagementAwService as imp2
from tcsoa.gen.ProjectManagementAw._2015_07.services import ScheduleManagementAwService as imp3
from tcsoa.gen.ProjectManagementAw._2020_05.services import ScheduleManagementAwService as imp4
from tcsoa.gen.ProjectManagementAw._2016_12.services import ScheduleManagementAwService as imp5
from tcsoa.base import TcService


class ScheduleManagementAwService(TcService):
    claimAssignments = imp0.claimAssignments
    createMasterSchedule = imp1.createMasterSchedule
    createMasterScheduleAsync = imp1.createMasterScheduleAsync
    createMultipleTaskDeliverables = imp2.createMultipleTaskDeliverables
    createTaskDeliverables = imp3.createTaskDeliverables
    designateDiscipline = imp2.designateDiscipline
    designateDisciplineAsync = imp2.designateDisciplineAsync
    getResourceChartInfo = imp4.getResourceChartInfo
    loadAssignedTasks = imp0.loadAssignedTasks
    loadBaseline = imp2.loadBaseline
    loadSchedule = imp5.loadSchedule
    loadSchedule2 = imp2.loadSchedule2
    recalculateSchedules = imp2.recalculateSchedules
    recalculateSchedulesAsync = imp2.recalculateSchedulesAsync
    removeAssignments = imp5.removeAssignments
    removeAssignmentsAsync = imp5.removeAssignmentsAsync
    replaceMemberAssignments = imp5.replaceMemberAssignments
    replaceMemberAssignmentsAsync = imp5.replaceMemberAssignmentsAsync
    shiftSchedules = imp4.shiftSchedules
    shiftSchedulesAsync = imp4.shiftSchedulesAsync
