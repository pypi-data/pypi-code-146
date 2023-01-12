#!/usr/bin/python3
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2023, Edouard DUPIN, all right reserved
##
## @license MPL v2.0 (see license file)
##

class KaranageException(Exception):
    def __init__(self, message, error_id, error_message):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
            
        # Now for your custom code...
        self.error_id = error_id
        self.error_message = error_message
    
    def __str__(self):
        return f"{Exception.__str__(self)} Status={self.error_id} message='{self.error_message}'"
