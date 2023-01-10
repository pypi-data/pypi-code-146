from tcsoa.gen.AuthorizedDataAccess._2007_06.services import LicenseManagementService as imp0
from tcsoa.gen.AuthorizedDataAccess._2009_10.services import LicenseManagementService as imp1
from tcsoa.gen.AuthorizedDataAccess._2017_05.services import LicenseManagementService as imp2
from tcsoa.gen.AuthorizedDataAccess._2013_05.services import LicenseManagementService as imp3
from tcsoa.gen.AuthorizedDataAccess._2018_06.services import LicenseManagementService as imp4
from tcsoa.gen.AuthorizedDataAccess._2012_09.services import LicenseManagementService as imp5
from tcsoa.base import TcService


class LicenseManagementService(TcService):
    attachLicenses = imp0.attachLicenses
    attachLicenses2 = imp1.attachLicenses
    attachOrDetachLicensesFromObjects = imp2.attachOrDetachLicensesFromObjects
    createOrUpdateLicense = imp3.createOrUpdateLicense
    createOrUpdateLicense2 = imp4.createOrUpdateLicense
    deleteLicense = imp0.deleteLicense
    getLicenseDetails = imp0.getLicenseDetails
    getLicenseDetails2 = imp1.getLicenseDetails2
    getLicenseDetails3 = imp5.getLicenseDetails3
    getLicenseDetails4 = imp3.getLicenseDetails4
    getLicenseIdsAndTypes = imp0.getLicenseIdsAndTypes
    removeLicenses = imp0.removeLicenses
    setLicenseDetails = imp0.setLicenseDetails
    setLicenseDetails2 = imp1.setLicenseDetails
    setLicenseDetails3 = imp5.setLicenseDetails
