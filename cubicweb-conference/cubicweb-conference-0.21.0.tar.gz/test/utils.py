from cubicweb.devtools.testlib import CubicWebTC


class ConferenceTC(CubicWebTC):
    def setup_database(self):
        with self.admin_access.repo_cnx() as cnx:
            self.location = cnx.create_entity(
                "PostalAddress",
                street="1, rue du chat qui pêche",
                postalcode="75005",
                city="Paris",
            ).eid
            cnx.commit()
