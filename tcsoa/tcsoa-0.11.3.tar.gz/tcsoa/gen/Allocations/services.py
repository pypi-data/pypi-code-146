from tcsoa.gen.Allocations._2007_01.services import AllocationService as imp0
from tcsoa.gen.Allocations._2011_06.services import AllocationService as imp1
from tcsoa.base import TcService


class AllocationService(TcService):
    addAllocationLines = imp0.addAllocationLines
    changeAllocatedBOMWindows = imp0.changeAllocatedBOMWindows
    changeAllocationContext = imp0.changeAllocationContext
    changeICContext = imp0.changeICContext
    closeAllocationWindow = imp0.closeAllocationWindow
    createAllocationContext = imp0.createAllocationContext
    createAllocationContext2 = imp1.createAllocationContext2
    deleteAllocationLines = imp0.deleteAllocationLines
    findAllocatedBOMViews = imp0.findAllocatedBOMViews
    findAllocationContexts = imp0.findAllocationContexts
    getBOMViews = imp0.getBOMViews
    modifyAllocationLines = imp0.modifyAllocationLines
    openAllocationWindow = imp0.openAllocationWindow
    saveAllocationWindow = imp0.saveAllocationWindow
