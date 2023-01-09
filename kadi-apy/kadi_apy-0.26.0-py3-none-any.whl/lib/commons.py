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


def add_user(item, user_id, role_name):
    """Add a user."""

    endpoint = item._actions["add_user_role"]
    data = {"role": {"name": role_name}, "user": {"id": user_id}}
    return item._post(endpoint, json=data)


def remove_user(item, user_id):
    """Remove a user."""

    endpoint = f"{item._actions['add_user_role']}/{user_id}"
    return item._delete(endpoint, json=None)


def add_group_role(item, group_id, role_name):
    """Add a group role."""

    endpoint = item._actions["add_group_role"]
    data = {"role": {"name": role_name}, "group": {"id": group_id}}
    return item._post(endpoint, json=data)


def remove_group_role(item, group_id):
    """Remove a group role."""

    endpoint = f"{item._actions['add_group_role']}/{group_id}"
    return item._delete(endpoint, json=None)


def change_group_role(item, group_id, role_name):
    """Change a group role."""

    endpoint = f"{item._actions['add_group_role']}/{group_id}"
    data = {"name": role_name}
    return item._patch(endpoint, json=data)


def add_collection_link(item, collection_id):
    """Add a collection."""

    endpoint = item._actions["link_collection"]
    data = {"id": collection_id}
    return item._post(endpoint, json=data)


def remove_collection_link(item, collection_id):
    """Remove a collection."""

    endpoint = f"{item._actions['link_collection']}/{collection_id}"
    return item._delete(endpoint, json=None)


def add_record_link(item, record_id):
    """Add a record."""

    endpoint = item._actions["link_record"]
    data = {"id": record_id}
    return item._post(endpoint, json=data)


def remove_record_link(item, record_id):
    """Remove a record."""

    endpoint = f"{item._actions['link_record']}/{record_id}"
    return item._delete(endpoint, json=None)


def get_tags(item):
    """Get tags."""

    return item.meta["tags"]


def check_tag(item, tag):
    """Check if a certain tag is already present."""

    for obj in item.get_tags():
        if obj == tag:
            return True
    return False


def add_tag(item, tag):
    """Add a tag."""

    endpoint = item._actions["edit"]
    tags = item.get_tags()
    if item.check_tag(tag):
        return None
    tags.append(tag)
    tags = {"tags": tags}
    return item._patch(endpoint, json=tags)


def remove_tag(item, tag):
    """Remove a tag."""

    endpoint = item._actions["edit"]
    tags = [obj for obj in item.get_tags() if obj != tag]
    tags = {"tags": tags}
    return item._patch(endpoint, json=tags)


def set_attribute(item, attribute, value):
    """Set attribute."""

    endpoint = item._actions["edit"]
    attribute = {attribute: value}
    return item._patch(endpoint, json=attribute)


def export(item, path, export_type="json", pipe=False, **params):
    """Export a resource using a specific export type."""
    response = item._get(
        f"{item.base_path}/{item.id}/export/{export_type}", params=params
    )

    if not pipe and response.status_code == 200:
        with open(path, "wb") as f:
            f.write(response.content)

    return response
