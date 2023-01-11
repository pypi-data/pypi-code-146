# -*- coding: utf-8 -*-
# Copyright (C) 2016 - 2021 froglogic GmbH.
# Copyright (C) 2022 The Qt Company Ltd.
# All rights reserved.
#
# This file is part of Squish.
#
# Licensees holding a valid Squish License Agreement may use this
# file in accordance with the Squish License Agreement provided with
# the Software.
#
# This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
# WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
# See the LICENSE file in the toplevel directory of this package.
#
# Contact contact@froglogic.com if any conditions of this licensing are
# not clear to you.

import squish

def _flatten(arr):
    out = []
    for item in arr:
        if isinstance(item, (list, tuple)):
            out.extend(_flatten(item))
        else:
            out.append(item)
    return out

class RemoteSystemException( Exception ):
    def __init__( self, message ):
        Exception.__init__(self, message)

class RemoteSystem:
    def __init__( self, host = None, port = None ):
        self = self
        self.connection_handle = -1
        self.host = host
        self.port = port

        if (self.host is not None) and (self.port is None):
            self.port = 4322
        if (self.host is None) and (self.port is not None):
            raise ValueError("Host not specified")

        if (self.host is None) or (self.port is None):
            self.connection_handle = squish._squish_connect_to_remote_system()
        else:
            self.connection_handle = squish._squish_connect_to_remote_system(
                self.host,
                int(self.port))

    def close(self):
        if self.connection_handle >= 0:
            try:
                r = squish._squish_close_remote_system_connection( int(self.connection_handle) )
                self.connection_handle = -1
                return r
            except Exception as e:
                raise RemoteSystemException( str(e) )

    def __del__(self):
        self.close()
        self.host = None
        self.port = None

    def execute(self, cmd, cwd=None, env=None, options=None):
        cwd = cwd or ""
        env = env or {}
        options = options or {}

        cmd = [str(v) for v in _flatten(cmd)]

        cwd = str(cwd)

        env = {k:str(v) for k,v in env.items()}

        result = squish._squish_remote_execute_command(self.connection_handle, cmd, cwd, env, options)

        if int(result["errornr"]) > 0:
            raise RuntimeError(result["errorstr"])

        return (result["exitcode"], result["stdout"], result["stderr"])
        
    def getEnvironmentVariable( self, varname ):
        try:
            return squish._squish_remote_get_environment_variable( self.connection_handle, varname )
        except Exception as e:
            raise RemoteSystemException( str(e) )

    def getOSName( self ):
        try:
            return squish._squish_remote_get_os_name( self.connection_handle )
        except Exception as e:
            raise RemoteSystemException( str(e) )
        
    def listFiles( self, path ):
        try:
            return squish._squish_remote_get_directory_content( self.connection_handle, path )
        except Exception as e:
            raise RemoteSystemException( str(e) )
            
    def stat( self, path, propertyname ):
        try:
            return squish._squish_remote_get_path_property( self.connection_handle, path, propertyname )
        except Exception as e:
            raise RemoteSystemException( str(e) )
            
    def exists( self, path ):
        try:
            return squish._squish_remote_path_exists( self.connection_handle, path )
        except Exception as e:
            raise RemoteSystemException( str(e) )
    
    def deleteFile( self, path ):
        try:
            return squish._squish_remote_delete_file( self.connection_handle, path )
        except Exception as e:
            raise RemoteSystemException( str(e) )

    def deleteDirectory( self, path, recusive = False ):
        try:
            return squish._squish_remote_delete_path( self.connection_handle, path, recusive )
        except Exception as e:
            raise RemoteSystemException( str(e) )
    
    def createDirectory( self, path ):
        try:
            return squish._squish_remote_create_path( self.connection_handle, path, False )
        except Exception as e:
            raise RemoteSystemException( str(e) )
    
    def createPath( self, path ):
        try:
            return squish._squish_remote_create_path( self.connection_handle, path, True )
        except Exception as e:
            raise RemoteSystemException( str(e) )
    
    def rename( self, oldpath, newpath ):
        try:
            return squish._squish_remote_rename_path( self.connection_handle, oldpath, newpath )
        except Exception as e:
            raise RemoteSystemException( str(e) )
    
    def createTextFile( self, path, content, encoding="UTF-8" ):
        try:
            return squish._squish_remote_create_file( self.connection_handle, path, content, encoding )
        except Exception as e:
            raise RemoteSystemException( str(e) )
    
    def upload( self, localpath, remotepath ):
        try:
            return squish._squish_remote_upload_file( self.connection_handle, localpath, remotepath )
        except Exception as e:
            raise RemoteSystemException( str(e) )
    
    def download( self, remotepath, localpath ):
        try:
            return squish._squish_remote_download_file( self.connection_handle, remotepath, localpath )
        except Exception as e:
            raise RemoteSystemException( str(e) )
    
    def copy( self, sourcepath, destpath ):
        try:
            return squish._squish_remote_copy_path( self.connection_handle, sourcepath, destpath )
        except Exception as e:
            raise RemoteSystemException( str(e) )
