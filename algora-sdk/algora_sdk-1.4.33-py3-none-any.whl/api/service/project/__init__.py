"""
Project API.
"""
from algora.api.service.project.synchronous import (
    get_project, get_projects, create_project, update_project, copy_project, delete_project
)
from algora.api.service.project.asynchronous import (
    async_get_project, async_get_projects, async_create_project, async_update_project, async_copy_project,
    async_delete_project
)
