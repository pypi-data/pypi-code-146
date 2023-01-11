## $Id: tests.py 17176 2022-11-25 11:54:59Z henrik $
##
## Copyright (C) 2011 Uli Fouquet & Henrik Bettermann
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""
Tests for hostels and their UI components.
"""
import os
import shutil
import tempfile
import grok
import pytz
from datetime import datetime, timedelta
from zope.event import notify
from zope.interface.verify import verifyClass, verifyObject
from zope.component.hooks import setSite, clearSite
from zope.testbrowser.testing import Browser
from zope.security.interfaces import Unauthorized
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility, getUtility
from waeup.kofa.app import University
from waeup.kofa.hostels.interfaces import (
    IHostelsContainer, IHostel, IBed, IHostelsUtils)
from waeup.kofa.hostels.vocabularies import NOT_OCCUPIED
from waeup.kofa.hostels.container import HostelsContainer
from waeup.kofa.hostels.hostel import Hostel, Bed
from waeup.kofa.hostels.batching import HostelProcessor, BedProcessor
from waeup.kofa.hostels.export import BedExporter, HostelExporter
from waeup.kofa.testing import (FunctionalLayer, FunctionalTestCase)
from waeup.kofa.students.student import Student
from waeup.kofa.students.accommodation import BedTicket
from waeup.kofa.university.department import Department

HOSTEL_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_hostel_data.csv'),
    'rb').read()

HOSTEL_HEADER_FIELDS = HOSTEL_SAMPLE_DATA.split(
    '\n')[0].split(',')

BED_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_bed_data.csv'),
    'rb').read()

BED_HEADER_FIELDS = BED_SAMPLE_DATA.split(
    '\n')[0].split(',')

class HostelsContainerTestCase(FunctionalTestCase):

    layer = FunctionalLayer

    def test_interfaces(self):
        # Make sure the correct interfaces are implemented.
        self.assertTrue(
            verifyClass(
                IHostelsContainer, HostelsContainer)
            )
        self.assertTrue(
            verifyObject(
                IHostelsContainer, HostelsContainer())
            )
        self.assertTrue(
            verifyClass(
                IHostel, Hostel)
            )
        self.assertTrue(
            verifyObject(
                IHostel, Hostel())
            )
        self.assertTrue(
            verifyClass(
                IBed, Bed)
            )
        bed = Bed()
        bed.bed_id = u'a_b_c_d'
        bed.bed_type = u'a_b_c'
        self.assertTrue(
            verifyObject(
                IBed, bed)
            )
        return

    def test_base(self):
        # We cannot call the fundamental methods of a base in that case
        container = HostelsContainer()
        hostel = Hostel()
        # We cannot add arbitrary objects
        department = Department()
        self.assertRaises(
            TypeError, container.addHostel, department)
        self.assertRaises(
            TypeError, hostel.addBed, department)
        # Application is expired if startdate or enddate are not set
        # or current datetime is outside application period.
        self.assertTrue(container.expired)
        delta = timedelta(days=10)
        container.startdate = datetime.now(pytz.utc) - delta
        self.assertTrue(container.expired)
        container.enddate = datetime.now(pytz.utc) + delta
        self.assertFalse(container.expired)

class HostelsFullSetup(FunctionalTestCase):

    def setUp(self):
        super(HostelsFullSetup, self).setUp()

        # Setup a sample site for each test
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        # we add the site immediately after creation to the
        # ZODB. Catalogs and other local utilities are not setup
        # before that step.
        self.app = self.getRootFolder()['app']
        # Set site here. Some of the following setup code might need
        # to access grok.getSite() and should get our new app then
        setSite(app)

        # Add student with subobjects
        student = Student()
        student.firstname = u'Anna'
        student.lastname = u'Tester'
        student.reg_number = u'123'
        student.matric_number = u'234'
        student.sex = u'f'
        self.app['students'].addStudent(student)
        self.student_id = student.student_id
        self.student = self.app['students'][self.student_id]
        self.student['studycourse'].current_session = 2004
        self.student['studycourse'].entry_session = 2004

        # The students_catalog must be informed that the
        # session attribute has changed
        notify(grok.ObjectModifiedEvent(self.student))

        # Set accommodation_session
        self.app['hostels'].accommodation_session = 2004

        # Create a hostel
        hostel = Hostel()
        hostel.hostel_id = u'hall-x'
        self.app['hostels'][hostel.hostel_id] = hostel

        # Create a bed
        bed = Bed()
        bed.bed_id = u'hall_block_room_bed'
        bed.bed_number = 1
        bed.bed_type = u'regular_male_fr'
        self.app['hostels'][hostel.hostel_id][bed.bed_id] = bed

        self.container_path = 'http://localhost/app/hostels'
        self.student_path = 'http://localhost/app/students/%s' % self.student_id
        self.manage_container_path = self.container_path + '/@@manage'
        self.add_hostel_path = self.container_path + '/addhostel'

        # Put the prepopulated site into test ZODB and prepare test
        # browser
        self.browser = Browser()
        self.browser.handleErrors = False

        self.logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'hostels.log')

    def tearDown(self):
        super(HostelsFullSetup, self).tearDown()
        clearSite()
        shutil.rmtree(self.dc_root)

class HostelsContainerTests(HostelsFullSetup):

    layer = FunctionalLayer

    def test_release_expired_allocations(self):
        self.app['hostels'].allocation_expiration = 7
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        cat = queryUtility(ICatalog, name='beds_catalog')
        bedticket = BedTicket()
        bedticket.booking_session = 2004
        bedticket.bed_coordinates = u'anything'
        self.student['accommodation'].addBedTicket(bedticket)
        self.app[
            'hostels']['hall-x']['hall_block_room_bed'].owner = self.student_id
        notify(grok.ObjectModifiedEvent(
            self.app['hostels']['hall-x']['hall_block_room_bed']))
        self.assertEqual(
            self.app['hostels']['hall-x']['hall_block_room_bed'].bed_type,
            'regular_male_fr')
        results = cat.searchResults(owner=(self.student_id, self.student_id))
        self.assertEqual(len(results), 1)
        self.browser.open(self.container_path + '/releaseexpired')
        self.assertTrue('Portal must be in maintenance mode for releasing expired bed allocations'
            in self.browser.contents)
        grok.getSite()['configuration'].maintmode_enabled_by = u'any_id'
        self.browser.open(self.container_path + '/releaseexpired')
        self.assertTrue('No bed released' in self.browser.contents)
        delta = timedelta(days=10)
        bedticket.booking_date = datetime.utcnow() - delta
        self.browser.open(self.container_path + '/releaseexpired')
        self.assertTrue(
            'Successfully released beds: hall_block_room_bed (K1000000)'
            in self.browser.contents)
        results = cat.searchResults(owner=(self.student_id, self.student_id))
        self.assertEqual(len(results), 0)
        self.assertMatches(bedticket.display_coordinates,
            '-- booking expired (2015-10-14 08:35:38 UTC) --')
        # The owner has been removed and the bed reserved.
        self.assertEqual(
            self.app['hostels']['hall-x']['hall_block_room_bed'].owner,
            NOT_OCCUPIED)
        self.assertEqual(
            self.app['hostels']['hall-x']['hall_block_room_bed'].bed_type,
            'regular_male_reserved')
        # Accommodation session can't be changed if hostels are not empty.
        self.browser.open(self.manage_container_path)
        self.browser.getControl(name="form.accommodation_session").value = ['2005']
        self.browser.getControl("Save").click()
        self.assertTrue(
            'You can\'t change the booking session before clearing all hostels'
            in self.browser.contents)
        # Releasing is logged.
        logcontent = open(self.logfile).read()
        self.assertTrue(
            'hostels.browser.ReleaseExpiredAllocationsPage - hostels - '
            'released: hall_block_room_bed (K1000000)'
            in logcontent)
        return

    def test_bed_statistics(self):
        utils = getUtility(IHostelsUtils)
        self.app['hostels']['hall-x'][
            'hall_block_room_bed'].owner = NOT_OCCUPIED
        notify(grok.ObjectModifiedEvent(
            self.app['hostels']['hall-x']['hall_block_room_bed']))
        stats = utils.getBedStatistics()
        self.assertEqual(stats,
            {'regular_male_fr': (0, 1, 1),
             'regular_female_fi': (0, 0, 0),
             'regular_male_re': (0, 0, 0),
             'regular_female_fr': (0, 0, 0),
             'regular_female_all': (0, 0, 0),
             'regular_female_re': (0, 0, 0),
             'regular_female_reserved': (0, 0, 0),
             'regular_male_reserved': (0, 0, 0),
             'regular_male_fi': (0, 0, 0),
             'regular_male_all': (0, 0, 0)}
             )
        self.app[
            'hostels']['hall-x']['hall_block_room_bed'].owner = self.student_id
        notify(grok.ObjectModifiedEvent(
            self.app['hostels']['hall-x']['hall_block_room_bed']))
        stats = utils.getBedStatistics()
        self.assertEqual(stats,
            {'regular_male_fr': (1, 0, 1),
             'regular_female_fi': (0, 0, 0),
             'regular_male_re': (0, 0, 0),
             'regular_female_fr': (0, 0, 0),
             'regular_female_all': (0, 0, 0),
             'regular_female_re': (0, 0, 0),
             'regular_female_reserved': (0, 0, 0),
             'regular_male_reserved': (0, 0, 0),
             'regular_male_fi': (0, 0, 0),
             'regular_male_all': (0, 0, 0)}
             )

class BedCatalogTests(HostelsFullSetup):

    layer = FunctionalLayer

    def test_get_catalog(self):
        # We can get a beds catalog if we wish
        cat = queryUtility(ICatalog, name='beds_catalog')
        assert cat is not None

    def test_search_by_type(self):
        # We can find a certain bed
        cat = queryUtility(ICatalog, name='beds_catalog')
        results = cat.searchResults(
            bed_type=(u'regular_male_fr', u'regular_male_fr'))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['hostels']['hall-x']['hall_block_room_bed']

    def test_search_by_owner(self):
        # We can find a certain bed
        myobj = self.app['hostels']['hall-x']['hall_block_room_bed']
        myobj.owner = u'abc'
        notify(grok.ObjectModifiedEvent(myobj))
        cat = queryUtility(ICatalog, name='beds_catalog')
        results = cat.searchResults(owner=(u'abc', u'abc'))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['hostels']['hall-x']['hall_block_room_bed']

class HostelsUITests(HostelsFullSetup):

    layer = FunctionalLayer

    def test_anonymous_access(self):
        # Anonymous users can't access hostels containers
        self.assertRaises(
            Unauthorized, self.browser.open, self.manage_container_path)
        return

    def test_add_search_edit_delete_manage_hostels(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.container_path)
        self.browser.getLink("Manage accommodation").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.manage_container_path)
        self.browser.getControl("Add hostel").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.add_hostel_path)
        self.browser.getControl("Create hostel").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertTrue('Hostel created' in self.browser.contents)
        self.browser.open(self.container_path + '/addhostel')
        self.browser.getControl("Create hostel").click()
        self.assertTrue('The hostel already exists' in self.browser.contents)
        hall = self.app['hostels']['hall-1']
        hall.blocks_for_female = ['A','B']
        self.browser.open(self.container_path + '/hall-1')
        expected = '...<ul id="form.blocks_for_female" ><li>Block A</li>...'
        self.assertMatches(expected,self.browser.contents)
        self.browser.open(self.container_path + '/hall-1/manage')
        self.browser.getControl(name="form.rooms_per_floor").value = '1'
        self.browser.getControl("Save").click()
        self.assertTrue('Form has been saved' in self.browser.contents)
        # Since the testbrowser does not support Javascrip the
        # save action cleared the settings above and we have to set them
        # again.
        self.assertTrue(len(hall.blocks_for_female) == 0)
        hall.blocks_for_female = ['A','B']
        hall.beds_for_fresh = ['A']
        hall.beds_for_returning = ['B']
        hall.beds_for_final = ['C']
        hall.beds_for_all = ['D','E']
        self.browser.getControl("Update all beds").click()
        self.assertTrue('Portal must be in maintenance mode for bed updates'
            in self.browser.contents)
        grok.getSite()['configuration'].maintmode_enabled_by = u'any_id'
        self.browser.getControl("Update all beds").click()
        expected = '...0 empty beds removed, 10 beds added, 0 occupied beds modified ()...'
        self.assertMatches(expected,self.browser.contents)
        cat = queryUtility(ICatalog, name='beds_catalog')
        results = cat.searchResults(
            bed_type=('regular_female_all', 'regular_female_all'))
        results = [(x.bed_id, x.bed_type) for x in results]
        self.assertEqual(results,
            [(u'hall-1_A_101_D', u'regular_female_all'),
             (u'hall-1_A_101_E', u'regular_female_all'),
             (u'hall-1_B_101_D', u'regular_female_all'),
             (u'hall-1_B_101_E', u'regular_female_all')])
        # Reserve beds.
        self.browser.getControl("Switch reservation", index=0).click()
        self.assertTrue('No item selected' in self.browser.contents)
        ctrl = self.browser.getControl(name='val_id')
        ctrl.getControl(value='hall-1_A_101_A').selected = True
        ctrl.getControl(value='hall-1_A_101_B').selected = True
        ctrl.getControl(value='hall-1_A_101_C').selected = True
        ctrl.getControl(value='hall-1_A_101_D').selected = True
        self.browser.getControl("Switch reservation", index=0).click()
        self.assertTrue('Successfully switched beds: hall-1_A_101_A (reserved)'
            in self.browser.contents)
        self.assertEqual(self.app['hostels']['hall-1'][
            'hall-1_A_101_D'].bed_type, 'regular_female_reserved')
        # The catalog has been updated.
        results = cat.searchResults(
            bed_type=('regular_female_all', 'regular_female_all'))
        results = [(x.bed_id, x.bed_type) for x in results]
        self.assertEqual(results,
            [(u'hall-1_A_101_E', u'regular_female_all'),
             (u'hall-1_B_101_D', u'regular_female_all'),
             (u'hall-1_B_101_E', u'regular_female_all')])
        results = cat.searchResults(
            bed_type=('regular_female_reserved', 'regular_female_reserved'))
        results = [(x.bed_id, x.bed_type) for x in results]
        self.assertEqual(results,
            [(u'hall-1_A_101_A', u'regular_female_reserved'),
             (u'hall-1_A_101_B', u'regular_female_reserved'),
             (u'hall-1_A_101_C', u'regular_female_reserved'),
             (u'hall-1_A_101_D', u'regular_female_reserved')])
        # Change hostel configuration with one bed booked.
        hall['hall-1_A_101_E'].owner = u'anyid'
        notify(grok.ObjectModifiedEvent(hall['hall-1_A_101_E']))
        hall.beds_for_fresh = ['A', 'E']
        hall.beds_for_all = ['D']
        self.browser.getControl("Update all beds").click()
        expected = '...9 empty beds removed, 9 beds added, 1 occupied beds modified...'
        self.assertMatches(expected,self.browser.contents)
        # Updating beds (including booked beds!) does update catalog.
        results = cat.searchResults(
            bed_type=('regular_female_all', 'regular_female_all'))
        results = [(x.bed_id, x.bed_type) for x in results]
        # The reservation of hall-1_A_101_D has been cancelled.
        self.assertEqual(results,
            [(u'hall-1_A_101_D', u'regular_female_all'),
             (u'hall-1_B_101_D', u'regular_female_all')])
        # Release bed which has previously been booked.
        bedticket = BedTicket()
        bedticket.booking_session = 2004
        bedticket.bed_coordinates = u'anything'
        self.student['accommodation'].addBedTicket(bedticket)
        self.app['hostels']['hall-1']['hall-1_A_101_D'].owner = self.student_id
        notify(grok.ObjectModifiedEvent(self.app['hostels']['hall-1']['hall-1_A_101_D']))
        self.browser.open(self.container_path + '/hall-1/manage')
        ctrl = self.browser.getControl(name='val_id')
        self.browser.getControl("Release selected beds", index=0).click()
        self.assertMatches("...No item selected...", self.browser.contents)
        ctrl = self.browser.getControl(name='val_id')
        ctrl.getControl(value='hall-1_A_101_D').selected = True
        self.browser.getControl("Release selected beds", index=0).click()
        self.assertMatches(
          '...Successfully released beds: hall-1_A_101_D (%s)...' % self.student_id,
          self.browser.contents)
        self.assertMatches(bedticket.bed_coordinates,
          u' -- booking cancelled on <YYYY-MM-DD hh:mm:ss> UTC --')
        # The catalog has been updated.
        results = cat.searchResults(owner=(self.student_id, self.student_id))
        assert len(results) == 0
        # If we release a free bed, nothing will happen.
        ctrl = self.browser.getControl(name='val_id')
        ctrl.getControl(value='hall-1_A_101_D').selected = True
        self.browser.getControl("Release selected beds", index=0).click()
        self.assertMatches(
          '...No allocated bed selected...', self.browser.contents)
        # Managers can manually allocate eligible students after cancellation.
        self.browser.open(self.container_path + '/hall-1/hall-1_A_101_A')
        # 'not occupied' is not accepted.
        self.browser.getControl("Save").click()
        self.assertMatches(
            "...No valid student id...",
            self.browser.contents)
        # Invalid student ids are not accepted.
        self.browser.getControl(name="form.owner").value = 'nonsense'
        self.browser.getControl("Save").click()
        self.assertMatches(
            "...Either student does not exist or student "
            "is not eligible to book accommodation...",
            self.browser.contents)
        self.browser.getControl(name="form.owner").value = self.student_id
        self.browser.getControl("Save").click()
        self.assertMatches("...Form has been saved...", self.browser.contents)
        # Students can only be allocated once.
        self.browser.open(self.container_path + '/hall-1/hall-1_A_101_B')
        self.browser.getControl(name="form.owner").value = self.student_id
        self.browser.getControl("Save").click()
        self.assertMatches(
            "...This student resides in bed hall-1_A_101_A...",
            self.browser.contents)
        # If we open the same form again, we will be redirected to hostel
        # manage page. Beds must be released first before they can be
        # allocated to other students.
        self.browser.open(self.container_path + '/hall-1/hall-1_A_101_A')
        self.assertEqual(self.browser.url,
            self.container_path + '/hall-1/@@manage#tab2')
        # Updating the beds again will not affect the allocation and also
        # the bed numbering remains the same.
        old_number = self.app['hostels']['hall-1']['hall-1_A_101_A'].bed_number
        old_owner = self.app['hostels']['hall-1']['hall-1_A_101_A'].owner
        self.browser.getControl("Update all beds").click()
        # 8 beds have been removed and re-added, 2 beds remains untouched
        # because they are occupied.
        expected = '...8 empty beds removed, 8 beds added, 0 occupied beds modified...'
        self.assertMatches(expected,self.browser.contents)
        new_number = self.app['hostels']['hall-1']['hall-1_A_101_A'].bed_number
        new_owner = self.app['hostels']['hall-1']['hall-1_A_101_A'].owner
        self.assertEqual(new_number, old_number)
        self.assertEqual(new_owner, old_owner)
        # If we change the bed type of an allocated bed, the modification will
        # be indicated.
        hall.blocks_for_female = ['B']
        hall.blocks_for_male = ['A']
        self.browser.getControl("Update all beds").click()
        expected = '...8 empty beds removed, 8 beds added, ' + \
            '2 occupied beds modified (hall-1_A_101_A, hall-1_A_101_E, )...'
        self.assertMatches(expected,self.browser.contents)
        new_number = self.app['hostels']['hall-1']['hall-1_A_101_A'].bed_number
        # Also the number of the bed has changed.
        self.assertFalse(new_number == old_number)
        # The number of occupied beds are displayed on container page.
        self.browser.open(self.container_path)
        self.assertTrue('2 of 10' in self.browser.contents)
        bedticket.bed = self.app['hostels']['hall-1']['hall-1_A_101_A']
        # Managers can open the bed statistics page
        self.browser.getLink("Bed statistics").click()
        self.assertTrue('Bed Statistics</h1>' in self.browser.contents)
        # Remove entire hostel.
        self.browser.open(self.manage_container_path)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        ctrl.getControl(value=value).selected = True
        self.browser.getControl("Remove selected", index=0).click()
        self.assertTrue('Successfully removed' in self.browser.contents)
        # Catalog is empty.
        results = cat.searchResults(
            bed_type=('regular_female_all', 'regular_female_all'))
        results = [x for x in results]
        assert len(results) == 0
        # Bed has been removed from bedticket
        self.assertEqual(bedticket.bed, None)
        # Actions are logged.
        logcontent = open(self.logfile).read()
        self.assertTrue(
            'hall-1 - 9 empty beds removed, 9 beds added, 1 occupied '
            'beds modified (hall-1_A_101_E, )'
            in logcontent)

    def test_clear_hostels(self):
        grok.getSite()['configuration'].maintmode_enabled_by = u'any_id'
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.container_path)
        self.browser.getLink("Manage accommodation").click()
        self.browser.getControl("Add hostel").click()
        self.browser.getControl("Create hostel").click()
        hall = self.app['hostels']['hall-1']
        hall.blocks_for_female = ['A','B']
        hall.rooms_per_floor = 1
        hall.beds_for_fresh = ['A']
        hall.beds_for_returning = ['B']
        hall.beds_for_final = ['C']
        hall.beds_for_all = ['D','E']
        self.browser.open(self.container_path + '/hall-1/manage')
        self.browser.getControl("Update all beds").click()
        cat = queryUtility(ICatalog, name='beds_catalog')
        results = cat.searchResults(bed_type=(None, None))
        self.assertEqual(len(results), 11)
        self.browser.getControl("Clear hostel").click()
        self.assertEqual(len(self.app['hostels']['hall-1']), 0)
        # Only the bed in hall-x remains in the catalog.
        results = cat.searchResults(bed_type=(None, None))
        self.assertEqual(len(results), 1)
        # We can clear all hostels at the same time.
        self.browser.open(self.manage_container_path)
        self.browser.getControl("Clear all hostels").click()
        results = cat.searchResults(bed_type=(None, None))
        self.assertEqual(len(results), 0)
        # Both actions have been logged.
        logcontent = open(self.logfile).read()
        self.assertTrue('INFO - zope.mgr - hostels.browser.HostelManageFormPage'
                        ' - hall-1 - cleared' in logcontent)
        self.assertTrue('zope.mgr - hostels.browser.HostelsContainerManagePage'
                        ' - hostels - all hostels cleared' in logcontent)

class ExportTests(HostelsFullSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(ExportTests, self).setUp()
        self.workdir = tempfile.mkdtemp()
        self.outfile = os.path.join(self.workdir, 'myoutput.csv')
        return

    def test_export_hostels(self):
        exporter = HostelExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'beds_for_all,beds_for_final,beds_for_fresh,beds_for_pre,'
            'beds_for_returning,blocks_for_female,'
            'blocks_for_male,floors_per_block,hostel_id,hostel_name,maint_fee,'
            'rooms_per_floor,sort_id,special_handling\r\n[],[],[],[],[],[],[],'
            '1,hall-x,Hall 1,0.0,2,10,regular\r\n'
            )
        return

    def test_export_beds(self):
        exporter = BedExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'bed_id,bed_number,bed_type,owner,hall,block,room,bed,'
            'special_handling,sex,bt\r\nhall_block_room_bed,1,regular_male_fr,,'
            'hall,block,room,bed,regular,male,fr\r\n'
            )
        return

    def tearDown(self):
        super(ExportTests, self).tearDown()
        clearSite()
        shutil.rmtree(os.path.dirname(self.outfile))

class HostelBedProcessorTest(HostelsFullSetup):

    layer = FunctionalLayer

    def test_import(self):
        self.processor = HostelProcessor()
        self.workdir = tempfile.mkdtemp()
        self.csv_file = os.path.join(self.workdir, 'sample_hostel_data.csv')
        open(self.csv_file, 'wb').write(HOSTEL_SAMPLE_DATA)
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, HOSTEL_HEADER_FIELDS)
        self.assertEqual(num_warns,0)
        self.assertEqual(len(self.app['hostels'].keys()), 11) # including hall-x
        self.assertEqual(self.app['hostels'][
            'block-a-upper-hostel'].hostel_id,'block-a-upper-hostel')
        self.assertEqual(self.app['hostels'][
            'block-a-upper-hostel'].beds_for_final, ['A', 'B'])
        logcontent = open(self.logfile).read()
        self.assertTrue(
            "Hostel Processor - sample_hostel_data - block-a-upper-hostel - "
            "updated: "
            "beds_for_pre=['G'], floors_per_block=1, "
            "special_handling=regular, "
            "beds_for_final=['A', 'B'], rooms_per_floor=32, "
            "hostel_id=block-a-upper-hostel, "
            "sort_id=20, beds_for_returning=['C', 'D'], "
            "hostel_name=Block A Upper Hostel, beds_for_fresh=['E', 'F'], "
            "blocks_for_female=['A']"
            in logcontent)
        shutil.rmtree(os.path.dirname(fin_file))
        shutil.rmtree(self.workdir)
        # The manage page can be opened.
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.container_path + '/block-a-upper-hostel')
        self.browser.getLink("Manage").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        return

    def test_import_update_hostel_and_beds(self):
        self.processor = HostelProcessor()
        self.workdir = tempfile.mkdtemp()
        self.csv_file = os.path.join(self.workdir, 'sample_hostel_data.csv')
        open(self.csv_file, 'wb').write(HOSTEL_SAMPLE_DATA)
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, HOSTEL_HEADER_FIELDS)
        # We import the same file in update mode
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, HOSTEL_HEADER_FIELDS, 'update')
        self.assertEqual(num_warns,0)
        logcontent = open(self.logfile).read()
        self.assertTrue(
            "Hostel Processor - sample_hostel_data - block-a-upper-hostel - "
            "updated: "
            "beds_for_pre=['G'], floors_per_block=1, "
            "special_handling=regular, "
            "beds_for_final=['A', 'B'], rooms_per_floor=32, "
            "hostel_id=block-a-upper-hostel, "
            "sort_id=20, beds_for_returning=['C', 'D'], "
            "hostel_name=Block A Upper Hostel, beds_for_fresh=['E', 'F'], "
            "blocks_for_female=['A']"
            in logcontent)
        # Update the beds of first hostel
        self.app['hostels']['block-a-upper-hostel'].updateBeds()
        # Import beds
        self.processor = BedProcessor()
        self.csv_file = os.path.join(self.workdir, 'sample_bed_data.csv')
        open(self.csv_file, 'wb').write(BED_SAMPLE_DATA)
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, BED_HEADER_FIELDS, 'update')
        self.assertEqual(num_warns,2)
        fail_file_content = open(fail_file).read()
        logcontent = open(self.logfile).read()
        self.assertEqual(
            'owner,bed_id,hostel_id,reserved,--ERRORS--\r\n'
            '<IGNORE>,block-a-upper-hostel_A_101_C,block-a-upper-hostel,2,'
            'reserved: invalid value\r\n'
            'K999,block-a-upper-hostel_A_101_E,block-a-upper-hostel,0,'
            'owner: student does not exist\r\n',
            fail_file_content)
        self.assertTrue(
            'system - Bed Processor (update only) - sample_bed_data - '
            'block-a-upper-hostel_A_101_A - updated: nothing'
            in logcontent)
        self.assertTrue(
            'system - Bed Processor (update only) - sample_bed_data - '
            'block-a-upper-hostel_A_101_B - updated: reserved'
            in logcontent)
        self.assertTrue(
            'system - Bed Processor (update only) - sample_bed_data - '
            'block-a-upper-hostel_A_101_D - updated: owner=K1000000'
            in logcontent)
        self.assertEqual(
            self.app['hostels']['block-a-upper-hostel']
                    ['block-a-upper-hostel_A_101_D'].owner, 'K1000000')
        self.assertEqual(
            self.app['hostels']['block-a-upper-hostel']
                    ['block-a-upper-hostel_A_101_B'].bed_type,
                    'regular_female_reserved')
        shutil.rmtree(os.path.dirname(fin_file))
        shutil.rmtree(self.workdir)
        return
