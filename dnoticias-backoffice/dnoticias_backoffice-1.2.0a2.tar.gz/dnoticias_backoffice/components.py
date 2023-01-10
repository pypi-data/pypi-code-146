from slippers.templatetags.slippers import register_components


def load_backoffice_slippers():
    register_components({
        "form_input": "components/forms/input.html",
        "form_input_code": "components/forms/input_code.html",
        "form_switch": "components/forms/switch.html",
        "form_switch_label": "components/forms/switch_label.html",
        "form_checkbox": "components/forms/checkbox.html",
        "form_quill": "components/forms/wysiwyg_input.html",
        "form_select2": "components/forms/select2.html",
        "form_dual_listbox": "components/forms/dual_listbox.html",
        "form_image": "components/forms/image.html",
        "form_checklist": "components/forms/checklist.html",
        "form_input_disabled": "components/forms/input_disabled.html",
        "form_select2_actions": "components/forms/select2_actions.html",
        "form_datetime": "components/forms/datetime.html",
        "form_price": "components/forms/price.html",

        "kt_section_title": "components/forms/kt_section_title.html",
        "kt_form_footer": "components/forms/kt_form_footer.html",
        "kt_separator": "components/forms/kt_separator.html",

        "simple_dategroup": "components/simple_forms/date_group.html",
        "simple_switch_label": "components/simple_forms/switch_label.html",
        "input_hidden": "components/simple_forms/input_hidden.html",
        "button": "components/simple_forms/button.html",

        "menu_item": "components/menu_item.html",
        "menu_category": "components/menu_category.html",
    })
