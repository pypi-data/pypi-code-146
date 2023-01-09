# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class Applicant(models.Model):
    _inherit = "hr.applicant"
    _description = "Applicant"

    _TEXT_LIMIT_CONTRIBUTION_TEXT = 280
    _TEXT_LIMIT_OTHER_TEXT = 1000

    @api.model
    def _names_order_default(self):
        return 'first_last'

    @api.model
    def _get_names_order(self):
        """Get names order configuration from system parameters.
        You can override this method to read configuration from language,
        country, company or other"""
        return self.env['ir.config_parameter'].sudo().get_param(
            'partner_names_order', self._names_order_default())

    @api.model
    def _get_computed_name(self, lastname, firstname):
        """Compute the 'name' field according to splitted data.
        You can override this method to change the order of lastname and
        firstname the computed name"""
        order = self._get_names_order()
        if order == 'last_first_comma':
            return ", ".join((p for p in (lastname, firstname) if p))
        elif order == 'first_last':
            return " ".join((p for p in (firstname, lastname) if p))
        else:
            return " ".join((p for p in (lastname, firstname) if p))

    @api.multi
    @api.depends("firstname", "lastname")
    def _compute_name(self):
        """Write the 'name' field according to splitted data."""
        for record in self:
            record.partner_name = record._get_computed_name(
                record.lastname, record.firstname,
            )

    @api.multi
    def _inverse_name_after_cleaning_whitespace(self):
        """Clean whitespace in :attr:`~.name` and split it.

        The splitting logic is stored separately in :meth:`~._inverse_name`, so
        submodules can extend that method and get whitespace cleaning for free.
        """
        for record in self:
            # Remove unneeded whitespace
            clean = record._get_whitespace_cleaned_name(record.partner_name)

            # Clean name avoiding infinite recursion
            if record.partner_name != clean:
                record.partner_name = clean

            # Save name in the real fields
            else:
                record._inverse_name()

    @api.model
    def _get_whitespace_cleaned_name(self, name, comma=False):
        """Remove redundant whitespace from :param:`name`.

        Removes leading, trailing and duplicated whitespace.
        """
        try:
            name = " ".join(name.split()) if name else name
        except UnicodeDecodeError:
            # with users coming from LDAP, name can be a str encoded as utf-8
            # this happens with ActiveDirectory for instance, and in that case
            # we get a UnicodeDecodeError during the automatic ASCII -> Unicode
            # conversion that Python does for us.
            # In that case we need to manually decode the string to get a
            # proper unicode string.
            name = ' '.join(name.decode('utf-8').split()) if name else name

        if comma:
            name = name.replace(" ,", ",")
            name = name.replace(", ", ",")
        return name

    @api.model
    def _get_inverse_name(self, name, is_company=False):
        """Compute the inverted name.

        - If the partner is a company, save it in the lastname.
        - Otherwise, make a guess.

        This method can be easily overriden by other submodules.
        You can also override this method to change the order of name's
        attributes

        When this method is called, :attr:`~.name` already has unified and
        trimmed whitespace.
        """
        # Company name goes to the lastname
        if is_company or not name:
            parts = [name or False, False]
        # Guess name splitting
        else:
            order = self._get_names_order()
            # Remove redundant spaces
            name = self._get_whitespace_cleaned_name(
                name, comma=(order == 'last_first_comma'))
            parts = name.split("," if order == 'last_first_comma' else " ", 1)
            if len(parts) > 1:
                if order == 'first_last':
                    parts = [" ".join(parts[1:]), parts[0]]
                else:
                    parts = [parts[0], " ".join(parts[1:])]
            else:
                while len(parts) < 2:
                    parts.append(False)
        return {"lastname": parts[0], "firstname": parts[1]}

    @api.multi
    def _inverse_name(self):
        """Try to revert the effect of :meth:`._compute_name`."""
        for record in self:
            parts = record._get_inverse_name(record.partner_name, False)
            record.lastname = parts['lastname']
            record.firstname = parts['firstname']

    @api.multi
    @api.constrains("firstname", "lastname")
    def _check_name(self):
        """Ensure at least one name is set."""
        for record in self:
            if not (record.firstname or record.lastname):
                raise exceptions.EmptyNamesError(record)

    @api.onchange("firstname", "lastname")
    def _onchange_subnames(self):
        """Avoid recursion when the user changes one of these fields.

        This forces to skip the :attr:`~.name` inversion when the user is
        setting it in a not-inverted way.
        """
        # Modify self's context without creating a new Environment.
        # See https://github.com/odoo/odoo/issues/7472#issuecomment-119503916.
        self.env.context = self.with_context(skip_onchange=True).env.context

    @api.onchange("name")
    def _onchange_name(self):
        """Ensure :attr:`~.name` is inverted in the UI."""
        if self.env.context.get("skip_onchange"):
            # Do not skip next onchange
            self.env.context = (
                self.with_context(skip_onchange=False).env.context)
        else:
            self._inverse_name_after_cleaning_whitespace()

    firstname = fields.Char("First name")
    lastname = fields.Char("Last name")

    # we are overriding the attributes of the field name as per compatibility with partner_firstname functionallity :
    partner_name = fields.Char(
        compute="_compute_name",
        inverse="_inverse_name_after_cleaning_whitespace",
        required=False,
        store=True)

    gender = fields.Selection(
        [("male", _("Male")), ("female", _("Female")), ("not_binary", _("Not binary")),
         ("other", _("Other identities")), ("not_share", _("I prefer do not answer it"))],
        string="Gender"
    )

    url_motivation_letter = fields.Char("Link to Motivation Letter")
    url_cv_doc = fields.Char("Link to CV document")
    able_to_work_in_girona = fields.Selection(
        (('y_close_to', _('Yes, I lives close to Girona')),
         ('y_easy_move', _('Yes, I can usually move to Girona')),
         ('n', _("No, I can't work in Girona"))), string="Can you work in Girona?")
    experience_years = fields.Selection(
        (('0', _('Any experience')),
         ('1_2', _('1-2 years')),
         ('3_5', _('3-5 years')),
         ('5_10', _('5-10 years')),
         ('>10', _('>10 years'))), string="Years of experience in this position")

    # we are overriding the attributes of the field description:
    description = fields.Text(
        string="What can you contribute to the cooperative?", size=_TEXT_LIMIT_CONTRIBUTION_TEXT)

    self_management_experience = fields.Text(
        string='Brief experience in cooperative/associative self-management', size=_TEXT_LIMIT_OTHER_TEXT)
    eco_feminism_experience = fields.Text(
        string='Brief experience in eco-feminism', size=_TEXT_LIMIT_OTHER_TEXT)

    def website_form_input_filter(self, request, values):
        values = super(Applicant, self).website_form_input_filter(
            request, values)
        if ('firstname' in values) or ('lastname in values' in values):
            values.setdefault('name', '%s\'s Application' % self._get_computed_name(
                values.get('lastname', ''), values.get('firstname', '')))
        return values
