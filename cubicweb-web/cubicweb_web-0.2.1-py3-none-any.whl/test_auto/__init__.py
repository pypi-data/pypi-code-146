# auto-populating test classes and utilities ###################################

# XXX cleanup unprotected_entities & all mess
from cubicweb.devtools import SYSTEM_RELATIONS
from cubicweb.devtools.fill import insert_entity_queries, make_relations_queries
from cubicweb.devtools.testlib import unprotected_entities, CubicWebTC, CubicWebDebugger
from logilab.common.testlib import Tags, nocoverage
from yams import ValidationError


def how_many_dict(schema, cnx, how_many, skip):
    """given a schema, compute how many entities by type we need to be able to
    satisfy relations cardinality.

    The `how_many` argument tells how many entities of which type we want at
    least.

    Return a dictionary with entity types as key, and the number of entities for
    this type as value.
    """
    relmap = {}
    for rschema in schema.relations():
        if rschema.final:
            continue
        for subj, obj in rschema.relation_definitions:
            card = rschema.relation_definition(subj, obj).cardinality
            # if the relation is mandatory, we'll need at least as many subj and
            # obj to satisfy it
            if card[0] in "1+" and card[1] in "1?":
                # subj has to be linked to at least one obj,
                # but obj can be linked to only one subj
                # -> we need at least as many subj as obj to satisfy
                #    cardinalities for this relation
                relmap.setdefault((rschema, subj), []).append(str(obj))
            if card[1] in "1+" and card[0] in "1?":
                # reverse subj and obj in the above explanation
                relmap.setdefault((rschema, obj), []).append(str(subj))
    unprotected = unprotected_entities(schema)
    for etype in skip:  # XXX (syt) duh? explain or kill
        unprotected.add(etype)
    howmanydict = {}
    # step 1, compute a base number of each entity types: number of already
    # existing entities of this type + `how_many`
    for etype in unprotected_entities(schema, strict=True):
        howmanydict[str(etype)] = cnx.execute("Any COUNT(X) WHERE X is %s" % etype)[0][
            0
        ]
        if etype in unprotected:
            howmanydict[str(etype)] += how_many
    # step 2, augment nb entity per types to satisfy cardinality constraints,
    # by recomputing for each relation that constrained an entity type:
    #
    # new num for etype = max(current num, sum(num for possible target etypes))
    #
    # XXX we should first check there is no cycle then propagate changes
    for (rschema, etype), targets in relmap.items():
        relfactor = sum(howmanydict[e] for e in targets)
        howmanydict[str(etype)] = max(relfactor, howmanydict[etype])
    return howmanydict


class AutoPopulateTest(CubicWebTC):
    """base class for test with auto-populating of the database"""

    __abstract__ = True

    test_db_id = "autopopulate"

    tags = CubicWebTC.tags | Tags("autopopulated")

    pdbclass = CubicWebDebugger
    # this is a hook to be able to define a list of rql queries
    # that are application dependent and cannot be guessed automatically
    application_rql = []

    no_auto_populate = ()
    ignored_relations = set()

    def to_test_etypes(self):
        return unprotected_entities(self.schema, strict=True)

    def custom_populate(self, how_many, cnx):
        pass

    def post_populate(self, cnx):
        pass

    @nocoverage
    def auto_populate(self, how_many):
        """this method populates the database with `how_many` entities
        of each possible type. It also inserts random relations between them
        """
        with self.admin_access.cnx() as cnx:
            with cnx.security_enabled(read=False, write=False):
                self._auto_populate(cnx, how_many)
                cnx.commit()

    def _auto_populate(self, cnx, how_many):
        self.custom_populate(how_many, cnx)
        vreg = self.vreg
        howmanydict = how_many_dict(self.schema, cnx, how_many, self.no_auto_populate)
        for etype in unprotected_entities(self.schema):
            if etype in self.no_auto_populate:
                continue
            nb = howmanydict.get(etype, how_many)
            for rql, args in insert_entity_queries(etype, self.schema, vreg, nb):
                cnx.execute(rql, args)
        edict = {}
        for etype in unprotected_entities(self.schema, strict=True):
            rset = cnx.execute("%s X" % etype)
            edict[str(etype)] = set(row[0] for row in rset.rows)
        existingrels = {}
        ignored_relations = SYSTEM_RELATIONS | self.ignored_relations
        for rschema in self.schema.relations():
            if rschema.final or rschema in ignored_relations or rschema.rule:
                continue
            rset = cnx.execute("DISTINCT Any X,Y WHERE X %s Y" % rschema)
            existingrels.setdefault(rschema.type, set()).update((x, y) for x, y in rset)
        q = make_relations_queries(
            self.schema, edict, cnx, ignored_relations, existingrels=existingrels
        )
        for rql, args in q:
            try:
                cnx.execute(rql, args)
            except ValidationError as ex:
                # failed to satisfy some constraint
                print("error in automatic db population", ex)
                cnx.commit_state = None  # reset uncommitable flag
        self.post_populate(cnx)

    def iter_individual_rsets(self, etypes=None, limit=None):
        etypes = etypes or self.to_test_etypes()
        with self.admin_access.web_request() as req:
            for etype in etypes:
                if limit:
                    rql = "Any X LIMIT %s WHERE X is %s" % (limit, etype)
                else:
                    rql = "Any X WHERE X is %s" % etype
                rset = req.execute(rql)
                for row in range(len(rset)):
                    if limit and row > limit:
                        break
                    # XXX iirk
                    rset2 = rset.limit(limit=1, offset=row)
                    yield rset2

    def iter_automatic_rsets(self, limit=10):
        """generates basic resultsets for each entity type"""
        etypes = self.to_test_etypes()
        if not etypes:
            return
        with self.admin_access.web_request() as req:
            for etype in etypes:
                yield req.execute("Any X LIMIT %s WHERE X is %s" % (limit, etype))
            etype1 = etypes.pop()
            try:
                etype2 = etypes.pop()
            except KeyError:
                etype2 = etype1
            # test a mixed query (DISTINCT/GROUP to avoid getting duplicate
            # X which make muledit view failing for instance (html validation fails
            # because of some duplicate "id" attributes)
            yield req.execute(
                "DISTINCT Any X, MAX(Y) GROUPBY X WHERE X is %s, Y is %s"
                % (etype1, etype2)
            )
            # test some application-specific queries if defined
            for rql in self.application_rql:
                yield req.execute(rql)

    def _test_everything_for(self, rset):
        """this method tries to find everything that can be tested
        for `rset` and yields a callable test (as needed in generative tests)
        """
        propdefs = self.vreg["propertydefs"]
        # make all components visible
        for k, v in propdefs.items():
            if k.endswith("visible") and not v["default"]:
                propdefs[k]["default"] = True
        for view in self.list_views_for(rset):
            backup_rset = rset.copy(rset.rows, rset.description)
            with self.subTest(name=self._testname(rset, view.__regid__, "view")):
                self.view(
                    view.__regid__, rset, rset.req.reset_headers(), "main-template"
                )
            # We have to do this because some views modify the
            # resultset's syntax tree
            rset = backup_rset
        for action in self.list_actions_for(rset):
            with self.subTest(name=self._testname(rset, action.__regid__, "action")):
                self._test_action(action)
        for box in self.list_boxes_for(rset):
            self.w_list = []
            w = self.mocked_up_w
            with self.subTest(name=self._testname(rset, box.__regid__, "box")):
                box.render(w)

    def mocked_up_w(self, text, *args, escape=True):
        # we don't care about escape here since we are in a test context
        if not args:
            self.w_list.append(text)
        elif isinstance(args[0], dict):
            self.w_list.append(text % args[0])
        else:
            self.w_list.append(text % args)

    @staticmethod
    def _testname(rset, objid, objtype):
        return "%s_%s_%s" % ("_".join(rset.column_types(0)), objid, objtype)


# concrete class for automated application testing  ############################


class AutomaticWebTest(AutoPopulateTest):
    """import this if you wan automatic tests to be ran"""

    tags = AutoPopulateTest.tags | Tags("web", "generated")

    def setUp(self):
        if self.__class__ is AutomaticWebTest:
            # Prevent direct use of AutomaticWebTest to avoid database caching
            # issues.
            return
        super().setUp()

        # access to self.app for proper initialization of the authentication
        # machinery (else some views may fail)
        self.app

    def test_one_each_config(self):
        self.auto_populate(1)
        for rset in self.iter_automatic_rsets(limit=1):
            self._test_everything_for(rset)

    def test_ten_each_config(self):
        self.auto_populate(10)
        for rset in self.iter_automatic_rsets(limit=10):
            self._test_everything_for(rset)

    def test_startup_views(self):
        for vid in self.list_startup_views():
            with self.admin_access.web_request() as req:
                with self.subTest(vid=vid):
                    self.view(vid, None, req)
