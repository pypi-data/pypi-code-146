from logilab.mtconverter import xml_escape

from cubicweb import _
from cubicweb.predicates import is_instance, has_related_entities
from cubicweb.predicates import authenticated_user
from cubicweb_web.views.idownloadable import DownloadBox
from cubicweb_web.component import EntityCtxComponent
from cubicweb_web.views import primary, calendar
from cubicweb_web.views.ajaxcontroller import ajaxfunc


class TalkPrimaryView(primary.PrimaryView):
    __select__ = is_instance(
        "Talk",
    )

    def render_entity_title(self, entity):
        self.w(
            '<h1><span class="etype">%s</span> %s</h1>'
            % (entity.dc_type().capitalize(), xml_escape(entity.dc_title()))
        )
        self.w('<table class="talk"><tr><td>')
        self.render_talk_info(entity)
        self.w("</td><td>")
        self.w("</td></tr></table>")

    def render_talk_info(self, entity):
        self.w("<div>")
        self.w(
            '<span class="speaker">%s %s</span>'
            % (
                self._cw._("Presented by"),
                self._cw.view(
                    "csv", entity.related("leads", "object"), subvid="outofcontext"
                ),
            )
        )
        if entity.track:
            self.w(" %s <span>" % self._cw._("in"))
            self.w("%s </span> " % entity.track.view("incontext"))
        self.render_talk_time_place(entity)
        self.w("</div>")

    def render_talk_time_place(self, entity):
        _ = self._cw._
        if entity.start_time or entity.end_time:
            self.w('<span class="talktime">')
            if entity.start_time and entity.end_time:
                self.w(
                    _("on %(sdate)s from %(stime)s to %(etime)s")
                    % (
                        {
                            "sdate": self._cw.format_date(entity.start_time),
                            "stime": self._cw.format_time(entity.start_time),
                            "etime": self._cw.format_time(entity.end_time),
                        }
                    )
                )
            self.w("</span>")
        if entity.location:
            self.w(
                "<span> {} {}</span>".format(_("in room"), xml_escape(entity.location))
            )

    def render_entity_attributes(self, entity):
        if entity.description:
            self.w("<h5>%s</h5>" % self._cw._("Abstract"))
            self.w("<div>%s</div>" % entity.dc_description("text/html"))


class AttendanceComponent(EntityCtxComponent):
    __regid__ = "attendance"
    __select__ = (
        EntityCtxComponent.__select__ & is_instance("Talk") & authenticated_user()
    )
    context = "ctxtoolbar"

    def init_rendering(self):
        self._cw.add_js("cubes.conference.js")
        user = self._cw.user
        eid = self.entity.eid
        rset = self._cw.execute(
            "Any X WHERE U attend X, U eid %(u)s, X eid %(x)s",
            {"u": user.eid, "x": eid},
        )
        if rset.rowcount:
            # user is already attending this talk
            self.klass = "delete_attend"
            self.title = _("click here if you do not plan to attend this talk")
            self.label, self.label_id = _("You plan to attend"), "attend"
        else:
            # user is not attending the talk
            self.klass = "set_attend"
            self.title = _("click here if you plan to attend this talk")
            self.label, self.label_id = _("You do not plan to attend"), "unattend"
        # count attendees
        rql = "Any COUNT(U) WHERE U attend X, X eid %s" % eid
        self.nb_person = self._cw.execute(rql)[0][0]

    def render_body(self, w):
        w(
            '<div class="%s" id="%s" data-eid="%s">'
            % (self.__regid__, self.domid, self.entity.eid)
        )
        w(
            '<div class="attendbutton %s" title="%s" id="%s">'
            '<div id="attendinfo">%s</div><div>(%s %s)</div></div>'
            % (
                self.klass,
                self._cw._(self.title),
                self.label_id,
                self._cw._(self.label),
                self.nb_person,
                self._cw._("people plan to attend"),
            )
        )
        w("</div>")


@ajaxfunc
def conference_delete_attend(self, talkeid):
    usereid = self._cw.user.eid
    self._cw.execute(
        "DELETE U attend X WHERE U eid %(u)s, X eid %(x)s", {"u": usereid, "x": talkeid}
    )


@ajaxfunc
def conference_set_attend(self, talkeid):
    usereid = self._cw.user.eid
    self._cw.execute(
        "SET U attend X WHERE U eid %(u)s, X eid %(x)s", {"u": usereid, "x": talkeid}
    )


class TalkCalendarItem(calendar.CalendarItemView):
    __select__ = is_instance("Talk")

    def cell_call(self, row, col, dates=False):
        talk = self.cw_rset.complete_entity(row)
        persons = self._cw.execute(
            "Any P WHERE P leads X, X eid %(x)s", {"x": talk.eid}
        ).entities()
        self.w(
            '<a href="%s">%s - %s</a>'
            % (
                talk.absolute_url(),
                xml_escape(talk.dc_title()),
                xml_escape(", ".join(p.dc_long_title() for p in persons)),
            )
        )
        if talk.location:
            self.w("<div>[{} {}]</div>".format(self._cw._("room"), talk.location))


class AttachmentsDownloadBox(DownloadBox):
    """A box containing all downloadable attachments of a Talk"""

    __regid__ = "attachments_downloads_box"
    __select__ = is_instance("Talk") & has_related_entities(
        "has_attachments", "subject"
    )
    title = _("Attachments")

    def init_rendering(self):
        self.items = self.entity.has_attachments
