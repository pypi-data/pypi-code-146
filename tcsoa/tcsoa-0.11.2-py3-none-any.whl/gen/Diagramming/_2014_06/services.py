from __future__ import annotations

from tcsoa.gen.Diagramming._2014_06.DNDManagement import CreateConnectionPortsAndConnectResponse, CreateAndPasteResponse, CreateAndPasteInputInfo, CreateConnectionPortsAndConnectInputInfo
from typing import List
from tcsoa.base import TcService


class DNDManagementService(TcService):

    @classmethod
    def createAndPaste(cls, inputData: List[CreateAndPasteInputInfo]) -> CreateAndPasteResponse:
        """
        This operation creates an object of given type and pastes the newly created object onto the paste target
        object.The result of the operation is newly created object and any runtime object as a result of paste
        operation.
        
        Use cases:
        Use Case1: 
        Create a new object and paste it under the paste target. User drags and drops shapes onto the diagram. Shapes
        are mapped to specific types and a mapping file specifies this information. On drag and drop a new object of
        the desired type is created and is pasted on to the diagram root object. When the diagram is for a BOM
        structure the paste operation also returns a resultant runtime object [BOMLine] in addition to the newly
        created object. The runtime/newly created object is mapped to the shape on the diagram.
        
        Use Case2: 
        Connection Management
        
        Use Case2a:
        Create Connection, Ports and establish connection between them. User drags and drops a Connection shape onto
        the diagram and glues the same to Block shapes. Two port objects are created and pasted under the Block objects
        if connected_ToRules is set to allow connection between ports; a Connection object is created and pasted under
        its paste target object. Connection is established between the Connection object and Port objects.
        
        Use Case2b: 
        Create Connection, establish connection between input ports. User drags and drops a Connection shape onto the
        diagram and glues the same to Port shapes. A Connection object is created and pasted under the paste target.
        Connection is established between the Connection object and Port objects if connected_ToRules is set to allow
        connection between ports.
        
        Use Case2c:
        Create Connection, a Port and establish connection between new port, input port. User drags and drops a
        Connection shape onto the diagram and glues the same to a Block shape and a Port shape. A Port object is
        created if connected_ToRules is set to allow connection between ports. A Connection object is created. Port and
        Connection objects are pasted under respective paste targets. Connection is established between the Connection
        object and Port objects.
        
        Use Case2d: 
        Establish connection between existing Connection and Ports. User glues an existing Connection shape to Port
        shapes. Connection is established between the ports if connected_ToRules allows for connections between ports.
        
        Use Case2e: 
        Create new ports and establish connection between existing Connection and the Ports.
        User glues an existing Connection shape to Block shapes. Port objects are created and pasted under respective
        paste target objects if connected_ToRules allows for connections between ports. Connection is established
        between the Port objects and Connection object.
        
        Use Case2f: 
        Create new port and establish connection between existing Connection, Port and newly created Port. User glues
        an existing Connection shape to a Block shape and Port shape. A Port objects is created and pasted under it's
        paste target object if connected_ToRules allows for connections between ports. Connection is established
        between the Port objects and Connection object.
        
        Use Case2g: 
        Establish connection between existing Connection and Blocks. User glues an existing Connection shape to Block
        shapes. Connection is established between the Blocks and Connection object if connected_ToRules allows for
        connection between blocks.
        """
        return cls.execute_soa_method(
            method_name='createAndPaste',
            library='Diagramming',
            service_date='2014_06',
            service_name='DNDManagement',
            params={'inputData': inputData},
            response_cls=CreateAndPasteResponse,
        )

    @classmethod
    def createConnectionPortsAndConnect(cls, inputData: List[CreateConnectionPortsAndConnectInputInfo]) -> CreateConnectionPortsAndConnectResponse:
        """
        This operation creates ports and connection object given the port types, connection type. Pastes the new
        objects under respective paste targets and then connects the connection object to the ports. Connection, one or
        both ports can exist, in that case the missing objects are created and connection is established. Connection
        can also be established directly between blocks.
        
        Use cases:
        Use Case1: 
        Create a new object and paste it under the paste target. User drags and drops shapes onto the diagram. Shapes
        are mapped to specific types and a mapping file specifies this information. On drag and drop a new object of
        the desired type is created and is pasted on to the diagram root object. When the diagram is for a BOM
        structure the paste operation also returns a resultant runtime object [BOMLine] in addition to the newly
        created object. The runtime/newly created object is mapped to the shape on the diagram.
        
        Use Case2: 
        Connection Management
        
        Use Case2a: 
        Create Connection, Ports and establish connection between them. User drags and drops a Connection shape onto
        the diagram and glues the same to Block shapes. Two port objects are created and pasted under the Block objects
        if connected_ToRules is set to allow connection between ports; a Connection object is created and pasted under
        its paste target object. Connection is established between the Connection object and Port objects.
        
        Use Case2b:
        Create Connection, establish connection between input ports. User drags and drops a Connection shape onto the
        diagram and glues the same to Port shapes. A Connection object is created and pasted under the paste target.
        Connection is established between the Connection object and Port objects if connected_ToRules is set to allow
        connection between ports.
        
        Use Case2c: 
        Create Connection, a Port and establish connection between new    port, input port.
        User drags and drops a Connection shape onto the diagram and glues the same to a Block shape and a Port shape.
        A Port object is created if connected_ToRules is set to allow connection between ports. A Connection object is
        created. Port and Connection objects are pasted under respective paste targets. Connection is established
        between the Connection object and Port objects.
        
        Use Case2d: 
        Establish connection between existing Connection and Ports
        User glues an existing Connection shape to Port shapes. Connection is established between the ports if
        connected_ToRules allows for connections between ports.
        
        Use Case2e: 
        Create new ports and establish connection between existing Connection and the Ports.
        User glues an existing Connection shape to Block shapes. Port objects are created and pasted under respective
        paste target objects if connected_ToRules allows for connections between ports. Connection is established
        between the Port objects and Connection object.
        
        Use Case2f: 
        Create new port and establish connection between existing Connection, Port and newly created Port. User glues
        an existing Connection shape to a Block shape and Port shape. A Port objects is created and pasted under it's
        paste target object if connected_ToRules allows for connections between ports. Connection is established
        between the Port objects and Connection object.
        
        Use Case2g: 
        Establish connection between existing Connection and Blocks. User glues an existing Connection shape to Block
        shapes. Connection is established between the Blocks and Connection object if connected_ToRules allows for
        connection between blocks.
        """
        return cls.execute_soa_method(
            method_name='createConnectionPortsAndConnect',
            library='Diagramming',
            service_date='2014_06',
            service_name='DNDManagement',
            params={'inputData': inputData},
            response_cls=CreateConnectionPortsAndConnectResponse,
        )
