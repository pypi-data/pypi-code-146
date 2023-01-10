from datetime import date
from logilab.common.testlib import unittest_main

from cubicweb.devtools import BASE_URL
from cubicweb_web.views import actions, workflow

from cubicweb_conference.views import actions as confactions

from utils import ConferenceTC


class ConferenceActionsTC(ConferenceTC):
    def setup_database(self):
        super().setup_database()
        with self.admin_access.repo_cnx() as cnx:
            self.create_user(cnx, "guest", groups=("guests",))
            self.create_user(cnx, "user")
            chair = self.create_user(cnx, "chair")
            reviewer = self.create_user(cnx, "reviewer")
            self.conf = cnx.create_entity(
                "Conference",
                title="my conf",
                url_id="url_conf",
                start_on=date(2010, 1, 27),
                end_on=date(2010, 1, 29),
                call_open=True,
                take_place_at=self.location,
                reverse_is_chair_at=chair,
                reverse_is_reviewer_at=reviewer,
            ).eid
            cnx.commit()

    def test_admin(self):
        with self.admin_access.web_request() as req:
            rset = req.execute("Any C WHERE C is Conference")
            conf = req.entity_from_eid(self.conf)
            self.assertListEqual(
                sorted(self.pactions(req, rset), key=lambda x: x[0]),
                sorted(
                    [
                        ("workflow", workflow.WorkflowActions),
                        ("edit", confactions.ModifyAction),
                        ("managepermission", actions.ManagePermissionsAction),
                        ("addrelated", actions.AddRelatedActions),
                        ("delete", actions.DeleteAction),
                        ("addtalkinconf", confactions.AddTalkInConferenceAction),
                    ],
                    key=lambda x: x[0],
                ),
            )
            self.assertListEqual(
                self.action_submenu(req, rset, "addrelated"),
                [
                    (
                        "add Track in_conf Conference object",
                        f"{BASE_URL}add/Track"
                        f"?__linkto=in_conf%%3A%(eid)s%%3Asubject&"
                        f"__redirectpath=conference%%2F%(url)s&"
                        f"__redirectvid=" % {"eid": conf.eid, "url": conf.url_id},
                    ),
                ],
            )

    def test_chair(self):
        with self.new_access("chair").web_request() as req:
            rset = req.execute("Any C WHERE C is Conference")
            conf = req.entity_from_eid(self.conf)
            self.assertListEqual(
                sorted(self.pactions(req, rset), key=lambda x: x[0]),
                sorted(
                    [
                        ("workflow", workflow.WorkflowActions),
                        ("edit", confactions.ModifyAction),
                        ("addrelated", actions.AddRelatedActions),
                        ("addtalkinconf", confactions.AddTalkInConferenceAction),
                    ],
                    key=lambda x: x[0],
                ),
            )
            self.assertListEqual(
                self.action_submenu(req, rset, "addrelated"),
                [
                    (
                        "add Track in_conf Conference object",
                        f"{BASE_URL}add/Track"
                        f"?__linkto=in_conf%%3A%(eid)s%%3Asubject&"
                        f"__redirectpath=conference%%2F%(url)s&"
                        f"__redirectvid=" % {"eid": conf.eid, "url": conf.url_id},
                    ),
                ],
            )

    def test_other(self):
        for login in ("reviewer", "user", "guest"):
            with self.new_access(login).web_request() as req:
                rset = req.execute("Any C WHERE C is Conference")
                self.assertListEqual(
                    sorted(self.pactions(req, rset), key=lambda x: x[0]),
                    sorted(
                        [
                            ("workflow", workflow.WorkflowActions),
                            ("addrelated", actions.AddRelatedActions),
                        ],
                        key=lambda x: x[0],
                    ),
                    "failed for %s" % login,
                )
                self.assertListEqual(self.action_submenu(req, rset, "addrelated"), [])


class TrackActionsTC(ConferenceActionsTC):
    def setup_database(self):
        super().setup_database()
        with self.admin_access.repo_cnx() as cnx:
            self.track = cnx.create_entity(
                "Track", title="a track", in_conf=self.conf
            ).eid
            cnx.commit()

    def test_admin(self):
        with self.admin_access.web_request() as req:
            rset = req.execute("Any T WHERE T is Track")
            self.assertListEqual(
                sorted(self.pactions(req, rset), key=lambda x: x[0]),
                sorted(
                    [
                        ("edit", confactions.ModifyAction),
                        ("managepermission", actions.ManagePermissionsAction),
                        ("addrelated", actions.AddRelatedActions),
                        ("delete", actions.DeleteAction),
                        ("addtalkintrack", confactions.AddTalkInTrackAction),
                    ],
                    key=lambda x: x[0],
                ),
            )
            self.assertListEqual(self.action_submenu(req, rset, "addrelated"), [])

    def test_chair(self):
        with self.new_access("chair").web_request() as req:
            rset = req.execute("Any T WHERE T is Track")
            self.assertListEqual(
                sorted(self.pactions(req, rset), key=lambda x: x[0]),
                sorted(
                    [
                        ("edit", confactions.ModifyAction),
                        ("addrelated", actions.AddRelatedActions),
                        ("delete", actions.DeleteAction),
                        ("addtalkintrack", confactions.AddTalkInTrackAction),
                    ],
                    key=lambda x: x[0],
                ),
            )
            self.assertListEqual(self.action_submenu(req, rset, "addrelated"), [])

    def test_other(self):
        for login in ("reviewer", "user", "guest"):
            with self.new_access(login).web_request() as req:
                rset = req.execute("Any T WHERE T is Track")
                self.assertListEqual(
                    sorted(self.pactions(req, rset), key=lambda x: x[0]),
                    sorted(
                        [
                            ("addrelated", actions.AddRelatedActions),
                        ],
                        key=lambda x: x[0],
                    ),
                    "failed for %s" % login,
                )
                self.assertListEqual(self.action_submenu(req, rset, "addrelated"), [])


if __name__ == "__main__":
    unittest_main()
