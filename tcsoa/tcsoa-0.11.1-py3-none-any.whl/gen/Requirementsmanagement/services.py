from tcsoa.gen.Requirementsmanagement._2007_01.services import RequirementsManagementService as imp0
from tcsoa.gen.Requirementsmanagement._2012_09.services import RequirementsManagementService as imp1
from tcsoa.gen.Requirementsmanagement._2008_06.services import RequirementsManagementService as imp2
from tcsoa.gen.Requirementsmanagement._2010_09.services import RequirementsManagementService as imp3
from tcsoa.gen.Requirementsmanagement._2009_10.services import RequirementsManagementService as imp4
from tcsoa.gen.Requirementsmanagement._2011_06.services import RequirementsManagementService as imp5
from tcsoa.base import TcService


class RequirementsManagementService(TcService):
    createOrUpdate = imp0.createOrUpdate
    exportToApplication = imp0.exportToApplication
    getBomlineAfterCreate = imp1.getBomlineAfterCreate
    getRichContent = imp0.getRichContent
    getRichContent2 = imp2.getRichContent
    importFromApplication = imp0.importFromApplication
    moveLine = imp3.moveLine
    openStdNote = imp4.openStdNote
    publishColumnConfiguration = imp5.publishColumnConfiguration
    setRichContent = imp0.setRichContent
    setStdNote = imp4.setStdNote
