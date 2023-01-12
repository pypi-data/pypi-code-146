# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Reporting views
"""

from __future__ import unicode_literals, absolute_import

import calendar
import json
import re
import datetime
import logging

import six

import rattail
from rattail.db import model, Session as RattailSession
from rattail.files import resource_path
from rattail.time import localtime
from rattail.threads import Thread
from rattail.util import simple_error, OrderedDict

import colander
from deform import widget as dfwidget
from mako.template import Template
from pyramid.response import Response
from webhelpers2.html import HTML, tags

from tailbone import forms
from tailbone.db import Session
from tailbone.views import View
from tailbone.views.exports import ExportMasterView, MasterView


plu_upc_pattern = re.compile(r'^000000000(\d{5})$')
weighted_upc_pattern = re.compile(r'^002(\d{5})00000\d$')

log = logging.getLogger(__name__)


def get_upc(product):
    """
    UPC formatter.  Strips PLUs to bare number, and adds "minus check digit"
    for non-PLU UPCs.
    """
    upc = six.text_type(product.upc)
    m = plu_upc_pattern.match(upc)
    if m:
        return six.text_type(int(m.group(1)))
    m = weighted_upc_pattern.match(upc)
    if m:
        return six.text_type(int(m.group(1)))
    return '{0}-{1}'.format(upc[:-1], upc[-1])


class OrderingWorksheet(View):
    """
    This is the "Ordering Worksheet" report.
    """

    report_template_path = 'tailbone:reports/ordering_worksheet.mako'

    upc_getter = staticmethod(get_upc)

    def __call__(self):
        if self.request.params.get('vendor'):
            vendor = Session.query(model.Vendor).get(self.request.params['vendor'])
            if vendor:
                departments = []
                uuids = self.request.params.get('departments')
                if uuids:
                    for uuid in uuids.split(','):
                        dept = Session.query(model.Department).get(uuid)
                        if dept:
                            departments.append(dept)
                preferred_only = self.request.params.get('preferred_only') == '1'
                body = self.write_report(vendor, departments, preferred_only)
                response = Response(content_type='text/html')
                response.headers['Content-Length'] = len(body)
                response.headers['Content-Disposition'] = 'attachment; filename=ordering.html'
                response.text = body
                return response
        return {}

    def write_report(self, vendor, departments, preferred_only):
        """
        Rendering engine for the ordering worksheet report.
        """

        q = Session.query(model.ProductCost)
        q = q.join(model.Product)
        q = q.filter(model.Product.deleted == False)
        q = q.filter(model.ProductCost.vendor == vendor)
        q = q.filter(model.Product.department_uuid.in_([x.uuid for x in departments]))
        if preferred_only:
            q = q.filter(model.ProductCost.preference == 1)

        costs = {}
        for cost in q:
            dept = cost.product.department
            subdept = cost.product.subdepartment
            costs.setdefault(dept, {})
            costs[dept].setdefault(subdept, [])
            costs[dept][subdept].append(cost)

        def cost_sort_key(cost):
            product = cost.product
            brand = product.brand.name if product.brand else ''
            key = '{0} {1}'.format(brand, product.description)
            return key

        now = localtime(self.request.rattail_config)
        data = dict(
            vendor=vendor,
            costs=costs,
            cost_sort_key=cost_sort_key,
            date=now.strftime('%a %d %b %Y'),
            time=now.strftime('%I:%M %p'),
            get_upc=self.upc_getter,
            rattail=rattail,
            )

        template_path = resource_path(self.report_template_path)
        template = Template(filename=template_path)
        return template.render(**data)


class InventoryWorksheet(View):
    """
    This is the "Inventory Worksheet" report.
    """

    report_template_path = 'tailbone:reports/inventory_worksheet.mako'

    upc_getter = staticmethod(get_upc)

    def __call__(self):
        """
        This is the "Inventory Worksheet" report.
        """

        departments = Session.query(model.Department)

        if self.request.params.get('department'):
            department = departments.get(self.request.params['department'])
            if department:
                body = self.write_report(department)
                response = Response(content_type=str('text/html'))
                response.headers[str('Content-Length')] = len(body)
                response.headers[str('Content-Disposition')] = str('attachment; filename=inventory.html')
                response.text = body
                return response

        departments = departments.order_by(model.Department.name)
        departments = departments.all()
        return{'departments': departments}

    def write_report(self, department):
        """
        Generates the Inventory Worksheet report.
        """

        def get_products(subdepartment):
            q = Session.query(model.Product)
            q = q.outerjoin(model.Brand)
            q = q.filter(model.Product.deleted == False)
            q = q.filter(model.Product.subdepartment == subdepartment)
            if self.request.params.get('weighted-only'):
                q = q.filter(model.Product.weighed == True)
            if self.request.params.get('exclude-not-for-sale'):
                q = q.filter(model.Product.not_for_sale == False)
            q = q.order_by(model.Brand.name, model.Product.description)
            return q.all()

        now = localtime(self.request.rattail_config)
        data = dict(
            date=now.strftime('%a %d %b %Y'),
            time=now.strftime('%I:%M %p'),
            department=department,
            get_products=get_products,
            get_upc=self.upc_getter,
            )

        template_path = resource_path(self.report_template_path)
        template = Template(filename=template_path)
        return template.render(**data)


class ReportOutputView(ExportMasterView):
    """
    Master view for report output
    """
    model_class = model.ReportOutput
    route_prefix = 'report_output'
    url_prefix = '/reports/generated'
    creatable = True
    downloadable = True
    bulk_deletable = True
    configurable = True
    config_title = "Reporting"
    config_url = '/reports/configure'

    grid_columns = [
        'id',
        'report_name',
        'filename',
        'created',
        'created_by',
    ]

    form_fields = [
        'id',
        'report_name',
        'report_type',
        'params',
        'filename',
        'created',
        'created_by',
    ]

    def __init__(self, request):
        super(ReportOutputView, self).__init__(request)
        self.report_handler = self.get_report_handler()

    def get_report_handler(self):
        app = self.get_rattail_app()
        return app.get_report_handler()

    def configure_grid(self, g):
        super(ReportOutputView, self).configure_grid(g)

        g.filters['report_name'].default_active = True
        g.filters['report_name'].default_verb = 'contains'

        g.set_link('filename')

    def configure_form(self, f):
        super(ReportOutputView, self).configure_form(f)

        # report_type
        f.set_renderer('report_type', self.render_report_type)

        # params
        f.set_renderer('params', self.render_params)

    def render_report_type(self, output, field):
        type_key = getattr(output, field)

        # just show type key by default
        rendered = type_key

        # (try to) show link to poser report if applicable
        if type_key and type_key.startswith('poser_'):
            app = self.get_rattail_app()
            poser_handler = app.get_poser_handler()
            poser_key = type_key[6:]
            report = poser_handler.normalize_report(poser_key)
            if not report.get('error'):
                url = self.request.route_url('poser_reports.view',
                                             report_key=poser_key)
                rendered = tags.link_to(type_key, url)

        # add help button if report has a link
        report = self.report_handler.get_report(type_key)
        if report and report.help_url:
            button = self.make_buefy_button("Help for this report",
                                            url=report.help_url,
                                            is_external=True,
                                            icon_left='question-circle')
            button = HTML.tag('div', class_='level-item', c=[button])
            rendered = HTML.tag('div', class_='level-item', c=[rendered])
            rendered = HTML.tag('div', class_='level-left', c=[rendered, button])

        return rendered

    def render_params(self, report, field):
        params = report.params
        if not params:
            return ""

        params = [{'key': key, 'value': value}
                  for key, value in params.items()]
        # TODO: should sort these according to true Report definition instead?
        params.sort(key=lambda param: param['key'])

        route_prefix = self.get_route_prefix()
        factory = self.get_grid_factory()
        g = factory(
            key='{}.params'.format(route_prefix),
            data=params,
            columns=['key', 'value'],
            labels={'key': "Name"},
        )
        if self.get_use_buefy():
            return HTML.literal(
                g.render_buefy_table_element(data_prop='paramsData'))
        else:
            return HTML.literal(g.render_grid())

    def get_params_context(self, report):
        params_data = []
        for name, value in (report.params or {}).items():
            params_data.append({
                'key': name,
                'value': value,
            })
        return params_data

    def template_kwargs_view(self, **kwargs):
        kwargs = super(ReportOutputView, self).template_kwargs_view(**kwargs)
        output = kwargs['instance']

        if self.get_use_buefy():
            kwargs['params_data'] = self.get_params_context(output)

        # build custom URL to re-build this report
        url = None
        if output.report_type:
            url = self.request.route_url('generate_specific_report',
                                         type_key=output.report_type,
                                         _query=output.params)
        kwargs['rerun_report_url'] = url

        return kwargs

    def template_kwargs_delete(self, **kwargs):
        kwargs = super(ReportOutputView, self).template_kwargs_delete(**kwargs)

        if self.get_use_buefy():
            report = kwargs['instance']
            kwargs['params_data'] = self.get_params_context(report)

        return kwargs

    def create(self):
        """
        View which allows user to choose which type of report they wish to
        generate.
        """
        use_buefy = self.get_use_buefy()

        # handler is responsible for determining which report types are valid
        reports = self.report_handler.get_reports()
        if isinstance(reports, OrderedDict):
            sorted_reports = list(reports)
        else:
            sorted_reports = sorted(reports, key=lambda k: reports[k].name)

        # make form to accept user choice of report type
        schema = NewReport().bind(valid_report_types=sorted_reports)
        form = forms.Form(schema=schema, request=self.request, use_buefy=use_buefy)
        form.submit_label = "Continue"
        form.cancel_url = self.request.route_url('report_output')

        # TODO: should probably "group" certain reports together somehow?
        # e.g. some for customers/membership, others for product movement etc.
        values = [(r.type_key, r.name) for r in reports.values()]
        values.sort(key=lambda r: r[1])
        if use_buefy:
            form.set_widget('report_type', forms.widgets.CustomSelectWidget(values=values))
            form.widgets['report_type'].set_template_values(input_handler='reportTypeChanged')
        else:
            form.set_widget('report_type', forms.widgets.PlainSelectWidget(values=values, size=10))

        # if form validates, that means user has chosen a report type, so we
        # just redirect to the appropriate "new report" page
        if form.validate(newstyle=True):
            raise self.redirect(self.request.route_url('generate_specific_report',
                                                       type_key=form.validated['report_type']))

        return self.render_to_response('choose', {
            'form': form,
            'dform': form.make_deform_form(),
            'reports': reports,
            'sorted_reports': sorted_reports,
            'report_descriptions': dict([(r.type_key, r.__doc__)
                                         for r in reports.values()]),
            'use_form': self.rattail_config.getbool(
                'tailbone', 'reporting.choosing_uses_form',
                default=False),
        })

    def generate(self):
        """
        View for actually generating a new report.  Allows user to provide
        input parameters specific to the report type, then creates a new report
        and redirects user to view the output.
        """
        app = self.get_rattail_app()
        use_buefy = self.get_use_buefy()
        type_key = self.request.matchdict['type_key']
        report = self.report_handler.get_report(type_key)
        if not report:
            return self.notfound()
        report_params = report.make_params(Session())
        route_prefix = self.get_route_prefix()

        NODE_TYPES = {
            bool: colander.Boolean,
            datetime.date: colander.Date,
            'decimal': colander.Decimal,
        }

        schema = colander.Schema()
        helptext = {}
        for param in report_params:

            # make a new node of appropriate schema type
            node_type = NODE_TYPES.get(param.type, colander.String)
            node = colander.SchemaNode(typ=node_type(), name=param.name)

            # maybe setup choices, if appropriate
            if param.type == 'choice':
                node.widget = dfwidget.SelectWidget(
                    values=report.get_choices(param.name, Session()))

            # allow empty value if param is optional
            if not param.required:
                node.missing = None

            # maybe set default value
            if hasattr(param, 'default'):
                node.default = param.default

            # set docstring
            helptext[param.name] = param.helptext

            schema.add(node)

        form = forms.Form(schema=schema, request=self.request,
                          use_buefy=use_buefy, helptext=helptext)
        form.submit_label = "Generate this Report"
        form.cancel_url = self.request.get_referrer(
            default=self.request.route_url('{}.create'.format(route_prefix)))

        # must declare jquery support for date fields, ugh
        # TODO: obviously would be nice for this to be automatic?
        for param in report_params:
            if param.type is datetime.date:
                form.set_type(param.name, 'date_jquery')

        # auto-select default choice for fields which have only one
        for param in report_params:
            if param.type == 'choice' and param.required:
                values = form.schema[param.name].widget.values
                if len(values) == 1:
                    form.set_default(param.name, values[0][0])

        # set default field values according to query string, if applicable
        if self.request.GET:
            for param in report_params:
                if param.name in self.request.GET:
                    value = self.request.GET[param.name]
                    if param.type is datetime.date:
                        value = app.parse_date(value)
                    elif param.type is bool:
                        value = self.rattail_config.parse_bool(value)
                    form.set_default(param.name, value)

        # if form validates, start generating new report output; show progress page
        if form.validate(newstyle=True):
            key = 'report_output.generate'
            progress = self.make_progress(key)
            kwargs = {'progress': progress}
            thread = Thread(target=self.generate_thread,
                            args=(report, form.validated, self.request.user.uuid),
                            kwargs=kwargs)
            thread.start()
            return self.render_progress(progress, {
                'cancel_url': self.request.route_url('report_output'),
                'cancel_msg': "Report generation was canceled",
            })

        # hide the "Create New" button for this page, b/c user is
        # already in the process of creating new..
        # TODO: this seems hacky, but works
        self.show_create_link = False

        return self.render_to_response('generate', {
            'report': report,
            'form': form,
            'dform': form.make_deform_form(),
        })

    def generate_thread(self, report, params, user_uuid, progress=None):
        """
        Generate output for the given report and params, and return the
        resulting :class:`rattail:~rattail.db.model.reports.ReportOutput`
        object.
        """
        session = RattailSession()
        user = session.query(model.User).get(user_uuid)
        try:
            output = self.report_handler.generate_output(session, report, params, user, progress=progress)

        # if anything goes wrong, rollback and log the error etc.
        except Exception as error:
            session.rollback()
            log.exception("Failed to generate '%s' report: %s", report.type_key, report)
            session.close()
            if progress:
                progress.session.load()
                progress.session['error'] = True
                progress.session['error_msg'] = "Failed to generate report: {}".format(
                    simple_error(error))
                progress.session.save()

        # if no error, check result flag (false means user canceled)
        else:
            session.commit()
            success_url = self.request.route_url('report_output.view', uuid=output.uuid)
            session.close()
            if progress:
                progress.session.load()
                progress.session['complete'] = True
                progress.session['success_url'] = success_url
                progress.session.save()

    def download(self):
        report = self.get_instance()
        path = report.filepath(self.rattail_config)
        return self.file_response(path)

    def configure_get_simple_settings(self):
        config = self.rattail_config
        return [

            # generating
            {'section': 'tailbone',
             'option': 'reporting.choosing_uses_form',
             'type': bool},
        ]

    @classmethod
    def defaults(cls, config):
        cls._defaults(config)
        cls._report_output_defaults(config)

    @classmethod
    def _report_output_defaults(cls, config):
        url_prefix = cls.get_url_prefix()
        permission_prefix = cls.get_permission_prefix()

        # generate report (accept custom params, truly create)
        config.add_route('generate_specific_report',
                         '{}/new/{{type_key}}'.format(url_prefix))
        config.add_view(cls, attr='generate', route_name='generate_specific_report',
                        permission='{}.create'.format(permission_prefix))


@colander.deferred
def valid_report_type(node, kw):
    valid_report_types = kw['valid_report_types']

    def validate(node, value):
        # we just need to provide possible values, and let core validator
        # handle the rest
        oneof = colander.OneOf(valid_report_types)
        return oneof(node, value)

    return validate


class NewReport(colander.Schema):

    report_type = colander.SchemaNode(colander.String(),
                                      validator=valid_report_type)


class ProblemReportView(MasterView):
    """
    Master view for problem reports
    """
    model_title = "Problem Report"
    model_key = ('system_key', 'problem_key')
    route_prefix = 'problem_reports'
    url_prefix = '/reports/problems'

    creatable = False
    deletable = False
    filterable = False
    pageable = False
    executable = True

    labels = {
        'system_key': "System",
        'days': "Schedule",
    }

    grid_columns = [
        'system_key',
        # 'problem_key',
        'problem_title',
        'email_recipients',
    ]

    def __init__(self, request):
        super(ProblemReportView, self).__init__(request)

        app = self.get_rattail_app()
        self.problem_handler = app.get_problem_report_handler()
        # TODO: deprecate / remove this
        self.handler = self.problem_handler

    def normalize(self, report, keep_report=True):
        data = self.problem_handler.normalize_problem_report(
            report, include_schedule=True, include_recipients=True)
        if keep_report:
            data['_report'] = report
        return data

    def get_data(self, session=None):
        data = []

        reports = self.handler.get_all_problem_reports()
        organized = self.handler.organize_problem_reports(reports)

        for system_key, reports in six.iteritems(organized):
            for report in six.itervalues(reports):
                data.append(self.normalize(report))

        return data

    def configure_grid(self, g):
        super(ProblemReportView, self).configure_grid(g)

        g.set_renderer('email_recipients', self.render_email_recipients)

        g.set_searchable('problem_title')

        g.set_link('problem_key')
        g.set_link('problem_title')

    def get_instance(self):
        system_key = self.request.matchdict['system_key']
        problem_key = self.request.matchdict['problem_key']
        return self.get_instance_for_key((system_key, problem_key),
                                         None)

    def get_instance_for_key(self, key, session):
        report = self.handler.get_problem_report(*key)
        if report:
            return self.normalize(report)
        raise self.notfound()

    def get_instance_title(self, report_info):
        return report_info['problem_title']

    def make_form_schema(self):
        return ProblemReportSchema()

    def configure_form(self, f):
        super(ProblemReportView, self).configure_form(f)

        # email_*
        if self.editing:
            f.remove('email_key',
                     'email_recipients')
        else:
            f.set_renderer('email_key', self.render_email_key)
            f.set_renderer('email_recipients', self.render_email_recipients)

        # enabled
        f.set_type('enabled', 'boolean')

        # days
        f.set_renderer('days', self.render_days)
        f.set_widget('days', DaysWidget())
        f.set_vuejs_field_converter('days', self.convert_vuejs_days)
        f.set_helptext('days', "NB. enabling a given day means you want the "
                       "report to be available that morning (assuming that "
                       "reports run overnight)")

        # only allow edit of certain fields
        if self.editing:
            editable = ('enabled', 'days')
            for field in f:
                if field not in editable:
                    f.set_readonly(field)

    def convert_vuejs_days(self, days):
        days = dict(days)
        for key in days:
            if days[key] is colander.null:
                days[key] = 'null'
        return days

    def render_email_recipients(self, report_info, field):
        recips = report_info['email_recipients']
        return ', '.join(recips)

    def render_days(self, report_info, field):
        g = self.get_grid_factory()('days', [],
                                    columns=['weekday_name', 'enabled'],
                                    labels={'weekday_name': "Weekday"})
        return HTML.literal(g.render_buefy_table_element(data_prop='weekdaysData'))

    def template_kwargs_view(self, **kwargs):
        kwargs = super(ProblemReportView, self).template_kwargs_view(**kwargs)
        report_info = kwargs['instance']

        data = []
        for i in range(7):
            data.append({
                'weekday': i,
                'weekday_name': calendar.day_name[i],
                'enabled': "Yes" if report_info['day{}'.format(i)] else "No",
            })
        kwargs['weekdays_data'] = data

        return kwargs

    def save_edit_form(self, form):
        app = self.get_rattail_app()
        session = self.Session()
        data = form.validated
        report = self.get_instance()
        key = '{}.{}'.format(report['system_key'],
                             report['problem_key'])

        app.save_setting(session, 'rattail.problems.{}.enabled'.format(key),
                         six.text_type(data['enabled']).lower())

        for i in range(7):
            daykey = 'day{}'.format(i)
            app.save_setting(session, 'rattail.problems.{}.{}'.format(key, daykey),
                             six.text_type(data['days'][daykey]).lower())

    def execute_instance(self, report_info, user, progress=None, **kwargs):
        report = report_info['_report']
        problems = self.handler.run_problem_report(report, progress=progress,
                                                   force=True)
        return "Report found {} problems".format(len(problems))


class ProblemReportDays(colander.MappingSchema):

    day0 = colander.SchemaNode(colander.Boolean(),
                               title=calendar.day_abbr[0])
    day1 = colander.SchemaNode(colander.Boolean(),
                               title=calendar.day_abbr[1])
    day2 = colander.SchemaNode(colander.Boolean(),
                               title=calendar.day_abbr[2])
    day3 = colander.SchemaNode(colander.Boolean(),
                               title=calendar.day_abbr[3])
    day4 = colander.SchemaNode(colander.Boolean(),
                               title=calendar.day_abbr[4])
    day5 = colander.SchemaNode(colander.Boolean(),
                               title=calendar.day_abbr[5])
    day6 = colander.SchemaNode(colander.Boolean(),
                               title=calendar.day_abbr[6])


class ProblemReportSchema(colander.MappingSchema):

    system_key = colander.SchemaNode(colander.String(),
                                     missing=colander.null)

    problem_key = colander.SchemaNode(colander.String(),
                                     missing=colander.null)

    problem_title = colander.SchemaNode(colander.String(),
                                     missing=colander.null)

    description = colander.SchemaNode(colander.String(),
                                     missing=colander.null)

    email_key = colander.SchemaNode(colander.String(),
                                     missing=colander.null)

    email_recipients = colander.SchemaNode(colander.String(),
                                           missing=colander.null)

    enabled = colander.SchemaNode(colander.Boolean())

    days = ProblemReportDays()


class DaysWidget(dfwidget.Widget):
    template = 'problem_report_days'

    def serialize(self, field, cstruct, **kw):
        if cstruct in (colander.null, None):
            cstruct = ""
        readonly = kw.get("readonly", self.readonly)
        template = self.template
        values = dict(kw)
        if 'day_labels' not in values:
            values['day_labels'] = self.get_day_labels()
        values = self.get_template_values(field, cstruct, values)
        return field.renderer(template, **values)

    def get_day_labels(self):
        labels = {}
        for i in range(7):
            labels[i] = {'name': calendar.day_name[i],
                         'abbr': calendar.day_abbr[i]}
        return labels

    def deserialize(self, field, pstruct):
        from deform.compat import string_types
        if pstruct is colander.null:
            return colander.null
        elif not isinstance(pstruct, string_types):
            raise colander.Invalid(field.schema, "Pstruct is not a string")
        pstruct = json.loads(pstruct)
        return pstruct


def add_routes(config):
    config.add_route('reports.ordering',        '/reports/ordering')
    config.add_route('reports.inventory',       '/reports/inventory')


def defaults(config, **kwargs):
    base = globals()

    # TODO: not in love with this pattern, but works for now
    add_routes(config)
    OrderingWorksheet = kwargs.get('OrderingWorksheet', base['OrderingWorksheet'])
    config.add_view(OrderingWorksheet, route_name='reports.ordering',
                    renderer='/reports/ordering.mako')
    InventoryWorksheet = kwargs.get('InventoryWorksheet', base['InventoryWorksheet'])
    config.add_view(InventoryWorksheet, route_name='reports.inventory',
                    renderer='/reports/inventory.mako')

    ReportOutputView = kwargs.get('ReportOutputView', base['ReportOutputView'])
    ReportOutputView.defaults(config)

    ProblemReportView = kwargs.get('ProblemReportView', base['ProblemReportView'])
    ProblemReportView.defaults(config)


def includeme(config):
    defaults(config)
