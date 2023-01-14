import os
from configparser import NoSectionError
from genesys.app.services import svn_service

def rename_asset_task_file(old_blend_file_url, new_blend_file_url):
    source = old_blend_file_url
    destination = new_blend_file_url
    if svn_service.is_svn_url(source):
        svn_service.svn_rename(source, destination, log_message='renamed')

def rename_section(parser, section_from, section_to):
    items = parser.items(section_from)
    parser.add_section(section_to)
    for item in items:
        parser.set(section_to, item[0], item[1])
    parser.remove_section(section_from)

def rename_task_acl_section(old_base_svn_directory, base_svn_directory, acl_parser):
    try:
        source = old_base_svn_directory
        destination = base_svn_directory
        rename_section(acl_parser, source, destination)
    except NoSectionError:
        # FIXME check if renamed version of file exist in acl
        # TODO skip task with same files
        pass