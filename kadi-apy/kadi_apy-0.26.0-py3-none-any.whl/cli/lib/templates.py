# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from kadi_apy.cli.commons import BasicCLIMixin
from kadi_apy.cli.commons import DeleteItemCLIMixin
from kadi_apy.cli.commons import ExportCLIMixin
from kadi_apy.cli.commons import RaiseRequestErrorMixin
from kadi_apy.lib.resources.templates import Template


class CLITemplate(
    BasicCLIMixin, DeleteItemCLIMixin, ExportCLIMixin, Template, RaiseRequestErrorMixin
):
    """Template class to be used in a CLI.

    :param manager: Manager to use for all API requests.
    :type manager: CLIKadiManager
    :param type: Type of the template. Can either be ``record`` or ``extras``.
    :type type: str
    :param data: Dict in case of a record template or a list in case of a extras
        template containing the content for the template.
    :param id: The ID of an existing resource.
    :type id: int, optional
    :param identifier: The unique identifier of a new or existing resource,
        which is only relevant if no ID was given. If present, the identifier will be
        used to check for an existing resource instead. If no existing resource could be
        found or the resource to check does not use a unique identifier, it will be used
        to create a new resource instead, together with the additional metadata.
    :type identifier: str, optional
    :param skip_request: Flag to skip the initial request.
    :type skip_request: bool, optional
    :param create: Flag to determine if a resource should be created in case
        a identifier is given and the resource does not exist.
    :type create: bool, optional
    :param pipe: Flag to indicate if only the id should be printed which can be used for
        piping.
    :type pipe: bool, optional
    :param title: Title of the new resource.
    :type title: str, optional
    :param exit_not_created: Flag to indicate if the function should exit with
        ``sys.exit(1)`` if the resource is not created.
    :type exit_not_created: bool, optional
    """

    def __init__(
        self, pipe=False, title=None, create=False, exit_not_created=False, **kwargs
    ):
        super().__init__(title=title, create=create, **kwargs)

        self._print_item_created(
            title=title,
            pipe=pipe,
            create=create,
            exit_not_created=exit_not_created,
        )

    def set_attribute(self, **kwargs):
        r"""Set attribute using a CLI.

        :param \**kwargs: Dict containing attributes to set.
        :type \**kwargs: dict
        :raises KadiAPYRequestError: If request was not successful.
        """

        # pylint: disable=arguments-differ

        return self._item_set_attribute(**kwargs)

    def delete(self, i_am_sure):
        """Delete the template using a CLI.

        :param i_am_sure: Flag which has to set to ``True`` to delete the template.
        :type i_am_sure: bool
        :raises  KadiAPYInputError: If i_am_sure is not ``True``.
        :raises KadiAPYRequestError: If request was not successful.
        """

        # pylint: disable=arguments-differ

        return self._item_delete(i_am_sure=i_am_sure)
