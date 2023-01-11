import jpype
import asposecells
jpype.startJVM()
from asposecells.api import Workbook, CellsHelper, FileFormatType, License

# lic = License()
# lic.setLicense("Aspose.Cells.lic")

print(CellsHelper.getVersion())

wb = Workbook(FileFormatType.XLSX)
wb.getWorksheets().get(0).getCells().get("A1").putValue("testing...")
wb.save("wb.xlsx")

jpype.shutdownJVM()