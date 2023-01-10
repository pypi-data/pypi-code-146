from logilab.common.date import date_range, ONEDAY
from logilab.mtconverter import xml_escape

from cubicweb import _
from cubicweb.predicates import is_instance, rql_condition
from cubicweb_web.view import EntityView
from cubicweb_web.views import tabs


class TrackPrimaryView(tabs.TabbedPrimaryView):
    __select__ = is_instance("Track")
    tabs = [_("trackinfo"), _("tracktalkslist"), _("tracktalksschedule")]
    default_tab = "trackinfo"

    def render_entity_title(self, entity):
        self.w("<h1>%s</h1>" % xml_escape(entity.dc_long_title()))


class TrackInfoView(EntityView):
    __select__ = is_instance("Track")
    __regid__ = "trackinfo"

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        if entity.description:
            self.w("<div>%s</div>" % entity.dc_description("text/html"))


class TrackTalksList(EntityView):
    __select__ = is_instance("Track")
    __regid__ = "tracktalkslist"

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        _ = self._cw._
        rql = (
            "Any T, group_concat(U), ST, SP, L GROUPBY T, ST, SP, L "
            "ORDERBY ST WHERE T location L, T start_time ST, "
            "T end_time SP, U leads T, T in_track TR, T in_state S, "
            'S name "accepted", TR eid %(x)s'
        )
        rset = self._cw.execute(rql, {"x": entity.eid})
        if rset:
            headers = (
                _("Talk title"),
                _("Speaker"),
                _("Begin"),
                _("End"),
                _("Location"),
            )
            self.wview("table", rset, headers=headers, cellvids={1: "users_list"})
        else:
            self.w("<div>%s</div>" % _("No accepted talk yet in this track"))


class TrackTalksSchedule(EntityView):
    __select__ = is_instance("Track") & rql_condition("T in_track X")
    __regid__ = "tracktalksschedule"

    def cell_call(self, row, col):
        track = self.cw_rset.get_entity(row, col)
        talks = self._cw.execute(
            "Any T WHERE T in_track TR, TR eid %(e)s, "
            'T in_state S, S name "accepted"',
            {"e": track.eid},
        )
        if not talks:
            return
        track_cal = track.cw_adapt_to("ICalendarable")
        for day in date_range(track_cal.start, track_cal.stop + ONEDAY):
            self.w('<table style="width:100%">')
            self.w("<tr>")
            self.w("<td>")
            self.wview("onedaycal", talks, initargs={"day": day, "title": track.title})
            self.w("</td>")
            self.w("</tr></table>")
