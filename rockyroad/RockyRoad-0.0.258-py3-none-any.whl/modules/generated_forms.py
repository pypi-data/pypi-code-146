from .module_imports import *


@headers({"Ocp-Apim-Subscription-Key": key})
class Generated_Forms(Consumer):
    """Inteface to generated forms resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    def results(self):
        return self.__Results(self)
    def fields(self):
        return self.__Fields(self)
    def groups(self):
        return self.__Groups(self)
    def forms(self):
        return self.__Forms(self)
    def startup_forms(self):
        return self.__Startup_Forms(self)

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __Fields(Consumer):
        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @http_get("generated/forms/fields")
        def list(self):
            """This call will get a list of all fields"""

        @returns.json
        @json
        @post("generated/forms/fields")
        def insert(self, field: Body):
            """This call will insert a field"""

        @returns.json
        @http_get("generated/forms/fields/{uid}")
        def get(self, uid: str):
            """This call will get a list of all fields based on the criteria"""

        @delete("generated/forms/fields/{uid}")
        def delete(self, uid: str):
            """This call will delete specified info for the specified uid."""

        @json
        @patch("generated/forms/fields/{uid}")
        def update(self, field: Body, uid:str):
            """This call will update the report with the specified parameters."""

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __Groups(Consumer):
        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @http_get("generated/forms/groups")
        def list(self):
            """This call will get a list of all groups"""

        @returns.json
        @json
        @post("generated/forms/groups")
        def insert(self, group: Body):
            """This call will insert a group"""

        @returns.json
        @http_get("generated/forms/groups/{uid}")
        def get(self, uid: str, include_assigned_fields: Query(type=bool) = None):
            """This call will get a group based on the criteria"""

        @delete("generated/forms/groups/{uid}")
        def delete(self, uid: str):
            """This call will delete specified info for the specified uid."""

        @json
        @patch("generated/forms/groups/{uid}")
        def update(self, group: Body, uid:str):
            """This call will update the group with the specified parameters."""

        @returns.json
        @json
        @post("generated/forms/groups/fields/{group_uid}/{field_uid}")
        def assign_field_to_group(self, group_uid: str, field_uid: str, field_instance_visible: Query(type=bool) = None, z_index: Query(type=int) = None):
            """This will assign a field to a group"""

        @delete("generated/forms/groups/fields/{mapped_field_uid}")
        def remove_field_from_group(self, mapped_field_uid: str):
            """This call will remove a field from a group."""

        @json
        @patch("generated/forms/groups/fields/order")
        def order_fields_in_group(self, mapped_fields: Body):
            """This call will update the groups with the specified parameters."""

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __Forms(Consumer):
        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @http_get("generated/forms/types")
        def list_types(self):
            """This call will get a list of all the form types"""
        
        @returns.json
        @http_get("generated/forms/forms")
        def list(self, form_type: Query(type=str) = None):
            """This call will get a list of all forms"""

        @returns.json
        @json
        @post("generated/forms/forms")
        def insert(self, form: Body):
            """This call will insert a form"""

        @returns.json
        @http_get("generated/forms/forms/{form_type}/machine/catalog/{machine_catalog_uid}")
        def get_form_by_machine_catalog(self, machine_catalog_uid: str, form_type:str, include_assigned_fields: Query(type=bool) = None):
            """This call will get a form based on the criteria"""

        @returns.json
        @http_get("generated/forms/forms/{form_type}/machine/model/{model}")
        def get_form_by_model(self, model: str, form_type:str, include_assigned_fields: Query(type=bool) = None):
            """This call will get a form based on the criteria"""

        @returns.json
        @http_get("generated/forms/forms/{form_type}/machine/models")
        def get_models_by_form(self,form_type:str):
            """This call will get the models that have forms by form type"""

        @returns.json
        @http_get("generated/forms/forms/{uid}")
        def get(self, uid: str, include_assigned_fields: Query(type=bool) = None, include_assigned_groups: Query(type=bool) = None):
            """This call will get a list of all forms based on the criteria"""

        @delete("generated/forms/forms/{uid}")
        def delete(self, uid: str):
            """This call will delete specified info for the specified uid."""

        @json
        @patch("generated/forms/forms/{uid}")
        def update(self, form: Body, uid:str):
            """This call will update the form with the specified parameters."""

        @returns.json
        @json
        @post("generated/forms/forms/groups/{form_uid}/{group_uid}")
        def assign_group_to_form(self, group_uid: str, form_uid: str, z_index: Query(type=int) = None):
            """This will assign a group to a form"""

        @delete("generated/forms/forms/groups/{form_uid}/{group_uid}")
        def remove_group_from_form(self, group_uid: str, form_uid: str):
            """This call will remove a group from a form."""

        @json
        @patch("generated/forms/forms/groups/{form_uid}/order")
        def order_groups_in_form(self, groups: Body, form_uid: str):
            """This call will update the forms with the specified parameters."""


    @headers({"Ocp-Apim-Subscription-Key": key})
    class __Results(Consumer):
        """Inteface to PDI Startup Results resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @http_get("generated/form/results")
        def list(self, form_type: Query(type=str) = None
        ):
            """This call will return all the pdi/startup reports."""

        @returns.json
        @json
        @post("generated/form/results")
        def insert(self, reports: Body):
            """This call will create an pdi/startup report with the specified parameters."""

        @returns.json
        @http_get("generated/form/results/current/dealer/{dealer_uid}")
        def get_all_for_dealer(self,
            dealer_uid: str,
            form_type: Query(type=str) = None
        ):
            """This call will return detailed report information for the specified criteria."""

        @returns.json
        @http_get("generated/form/results/{form_type}/dictionary/machine/{machine_uid}")
        def get_report_with_dictionary_by_machine(self,
            machine_uid: str,
            form_type: str
        ):
            """This call will return detailed report information for the specified criteria."""

        @returns.json
        @http_get("generated/form/results/dictionary/{uid}")
        def get_report_with_dictionary(self,
            uid: str
        ):
            """This call will return detailed report information for the specified criteria."""

        @returns.json
        @http_get("generated/form/results/{form_type}/machine/{machine_uid}/exists")
        def report_exists_for_machine(self,
            machine_uid: str,
            form_type: str
        ):
            """This call will return detailed report information for the specified criteria."""

        @returns.json
        @http_get("generated/form/results/{form_type}/machine/{machine_uid}")
        def get_report_by_machine(self,
            machine_uid: str,
            form_type: str
        ):
            """This call will return detailed report information for the specified criteria."""
        @returns.json
        @http_get("generated/form/results/current/dealer/{uid}")
        def get_report(self,
            uid: str
        ):
            """This call will return detailed report information for the specified criteria."""

        @delete("generated/form/results/{uid}")
        def delete(self, uid: str):
            """This call will delete specified info for the specified uid."""

        @json
        @patch("generated/form/results/{uid}")
        def update(self, report: Body, uid:str):
            """This call will update the report with the specified parameters."""

        # @returns.json
        # @multipart
        # @post("inspections/uploadfiles")
        # def addFile(self, uid: Query(type=str), file: Part):
        #     """This call will create an inspection report with the specified parameters."""

        # @http_get("inspections/download-files")
        # def downloadFile(
        #     self,
        #     uid: Query(type=str),
        #     filename: Query(type=str),
        # ):
        #     """This call will download the file associated with the inspection report with the specified uid."""

        # @returns.json
        # @http_get("inspections/list-files")
        # def listFiles(
        #     self,
        #     uid: Query(type=str),
        # ):
        #     """This call will return a list of the files associated with the inspection report for the specified uid."""

       
    @headers({"Ocp-Apim-Subscription-Key": key})
    class __Startup_Forms(Consumer):
        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @http_get("startup/forms")
        def get_forms(self):
            """This call will get a form based on the criteria"""

        @returns.json
        @http_get("generated/form/results/current/dealer/{dealer_uid}")
        def get_all_for_dealer(self,
            dealer_uid: str
        ):
            """This call will return detailed report information for the specified criteria."""
