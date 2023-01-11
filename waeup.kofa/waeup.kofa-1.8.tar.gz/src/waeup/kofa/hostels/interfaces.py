## $Id: interfaces.py 17176 2022-11-25 11:54:59Z henrik $
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
from  grok import getSite
from datetime import datetime
from zope.component import getUtility
from zope.catalog.interfaces import ICatalog
from zope.interface import invariant, Invalid, Attribute, Interface
from zope import schema
from waeup.kofa.interfaces import (
    IKofaObject, academic_sessions_vocab, registration_states_vocab)
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.hostels.vocabularies import (
    bed_letters, blocks, SpecialHandlingSource,
    NOT_OCCUPIED)
from waeup.kofa.students.interfaces import (IStudentsUtils)

# Define a validation method for sort ids
class NotASortId(schema.ValidationError):
    __doc__ = u"Invalid sort_id"

def validate_sort_id(value):
    if not value < 1000:
        raise NotASortId(value)
    return True

class IHostelsContainer(IKofaObject):
    """A container for hostel objects.
    """

    expired = Attribute('True if current datetime is in application period.')
    statistics = Attribute('Bed category statistics')

    startdate = schema.Datetime(
        title = _(u'Hostel Allocation Start Date'),
        required = False,
        description = _('Example: ') + u'2011-12-01 18:30:00+01:00',
        )

    enddate = schema.Datetime(
        title = _(u'Hostel Allocation Closing Date'),
        required = False,
        description = _('Example: ') + u'2011-12-31 23:59:59+01:00',
        )

    accommodation_session = schema.Choice(
        title = _(u'Booking Session'),
        source = academic_sessions_vocab,
        #default = datetime.now().year,
        required = False,
        readonly = False,
        )

    accommodation_states = schema.List(
        title = _(u'Allowed States'),
        value_type = schema.Choice(
            vocabulary = registration_states_vocab,
            ),
        defaultFactory=list,
        )

    allocation_expiration = schema.Int(
        title = _(u'Allocation Expiration Time (days)'),
        description = _(
            'Number of days after which allocation is being annulled'),
        required = False,
        )

    def clearAllHostels():
        """Clear all hostels.
        """

    def addHostel(hostel):
        """Add a hostel.
        """

    def releaseExpiredAllocations(n):
        """Release bed if bed allocation has expired. Allocation expires
        after `n` days if maintenance fee has not been paid.
        """

    def writeLogMessage(view, message):
        """Add an INFO message to hostels.log.
        """

class IHostel(IKofaObject):
    """Representation of a hostel.
    """

    bed_statistics = Attribute('Number of booked and total beds')

    def clearHostel():
        """Remove all beds.
        """

    def updateBeds():
        """Fill hostel with beds or update beds.
        """

    hostel_id = schema.TextLine(
        title = _(u'Hostel Id'),
        )

    sort_id = schema.Int(
        title = _(u'Sort Id'),
        required = True,
        default = 10,
        constraint=validate_sort_id,
        )

    hostel_name = schema.TextLine(
        title = _(u'Hostel Name'),
        required = True,
        default = u'Hall 1',
        )

    floors_per_block = schema.Int(
        title = _(u'Floors per Block'),
        required = True,
        default = 1,
        )

    rooms_per_floor = schema.Int(
        title = _(u'Rooms per Floor'),
        required = True,
        default = 2,
        )

    blocks_for_female = schema.List(
        title = _(u'Blocks for Female Students'),
        value_type = schema.Choice(
            vocabulary = blocks
            ),
        defaultFactory=list,
        )

    blocks_for_male = schema.List(
        title = _(u'Blocks for Male Students'),
        value_type = schema.Choice(
            vocabulary = blocks
            ),
        defaultFactory=list,
        )

    beds_for_pre= schema.List(
        title = _(u'Beds for Pre-Study Students'),
        value_type = schema.Choice(
            vocabulary = bed_letters
            ),
        defaultFactory=list,
        )

    beds_for_fresh = schema.List(
        title = _(u'Beds for Fresh Students'),
        value_type = schema.Choice(
            vocabulary = bed_letters
            ),
        defaultFactory=list,
        )

    beds_for_returning = schema.List(
        title = _(u'Beds for Returning Students'),
        value_type = schema.Choice(
            vocabulary = bed_letters
            ),
        defaultFactory=list,
        )

    beds_for_final = schema.List(
        title = _(u'Beds for Final Year Students'),
        value_type = schema.Choice(
            vocabulary = bed_letters
            ),
        defaultFactory=list,
        )

    beds_for_all = schema.List(
        title = _(u'Beds without category'),
        value_type = schema.Choice(
            vocabulary = bed_letters
            ),
        defaultFactory=list,
        )

    special_handling = schema.Choice(
        title = _(u'Special Handling'),
        source = SpecialHandlingSource(),
        required = True,
        default = u'regular',
        )

    maint_fee = schema.Float(
        title = _(u'Rent'),
        default = 0.0,
        required = False,
        )

    @invariant
    def blocksOverlap(hostel):
        bfe = hostel.blocks_for_female
        bma = hostel.blocks_for_male
        if set(bfe).intersection(set(bma)):
            raise Invalid(_('Female and male blocks overlap.'))

    @invariant
    def bedsOverlap(hostel):
        beds = (hostel.beds_for_fresh +
                hostel.beds_for_returning +
                hostel.beds_for_final +
                hostel.beds_for_pre +
                hostel.beds_for_all)
        if len(beds) != len(set(beds)):
            raise Invalid(_('Bed categories overlap.'))

    def writeLogMessage(view, message):
        """Add an INFO message to hostels.log.
        """

class IBed(IKofaObject):
    """Representation of a bed.
    """

    coordinates = Attribute('Coordinates tuple derived from bed_id')
    hall = Attribute('Hall id, for exporter only')
    block = Attribute('Block letter, for exporter only')
    room = Attribute('Room number, for exporter only')
    bed = Attribute('Bed letter, for exporter only')
    special_handling = Attribute('Special handling code, for exporter only')
    sex = Attribute('Sex, for exporter only')
    bt = Attribute('Last part of bed type, for exporter only')

    def bookBed(student_id):
        """Book a bed for a student.
        """

    def switchReservation():
        """Reserves bed or relases reserved bed respectively.
        """

    def releaseBedIfMaintenanceNotPaid():
        """Release bed if maintenance fee has not been paid on time.
        Reserve bed so that it cannot be automatically booked by someone else.
        """

    bed_id = schema.TextLine(
        title = _(u'Bed Id'),
        required = True,
        default = u'',
        )

    bed_type = schema.TextLine(
        title = _(u'Bed Type'),
        required = True,
        default = u'',
        )

    bed_number = schema.Int(
        title = _(u'Bed Number'),
        required = True,
        )

    owner = schema.TextLine(
        title = _(u'Owner (Student)'),
        description = _('Enter valid student id.'),
        required = True,
        default = u'',
        )

    @invariant
    def allowed_owners(bed):
        if bed.owner == NOT_OCCUPIED:
            return
        catalog = getUtility(ICatalog, name='students_catalog')
        accommodation_span = getUtility(IStudentsUtils).ACCOMMODATION_SPAN
        accommodation_session = getSite()['hostels'].accommodation_session
        students = catalog.searchResults(current_session=(
            accommodation_session-accommodation_span,accommodation_session))
        student_ids = [student.student_id for student in students]
        if not bed.owner in student_ids:
            raise Invalid(_(
                "Either student does not exist or student "
                "is not eligible to book accommodation."))
        catalog = getUtility(ICatalog, name='beds_catalog')
        beds = catalog.searchResults(owner=(bed.owner,bed.owner))
        if len(beds):
            allocated_bed = [bed.bed_id for bed in beds][0]
            raise Invalid(_(
                "This student resides in bed ${a}.",
                mapping = {'a':allocated_bed}))

    def writeLogMessage(view, message):
        """Add an INFO message to hostels.log.
        """

class IHostelsUtils(Interface):
    """A collection of methods which are subject to customization.
    """

    def getBedStatistics():
        """Return bed statistics.
        """
