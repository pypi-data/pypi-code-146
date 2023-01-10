from protmo.ast import *
from protmo.grpc_ast import *


class AstToGrpcAst:
    '''
    Generates multiple ProtoMessage for a given Message
    '''

    def __init__(self, modelMessage: MessageInfo):
        self.messages = []
        has_void = False

        # 1. create message of the model
        protoMsg = ProtoMessage(modelMessage.name)
        for field in modelMessage.fields:
            protoMsg.fields.append(
                ProtoField(
                    field.protoType,
                    field.name,
                    field.tag,
                    field.repeated))
        self.messages.append(protoMsg)

        # 2. create all required messages for the rpc-methods
        for method in modelMessage.rpc_methods:

            # 2.1 create ParameterMessage
            if method.has_params:
                paramMessage = ProtoMessage(
                    modelMessage.name + cap(method.name) + 'Param')
                tag_offset = 1
                if not method.is_static:
                    # add self reference
                    tag_offset += 1
                    paramMessage.fields.append(ProtoField('string', 'self', 1))
                for idx, param in enumerate(method.parameters):
                    tag = idx + tag_offset
                    name = param.name
                    if method.clientSideStreaming:
                        name = 'request'
                    field = ProtoField(
                        param.pythonType, name, tag, repeated=param.repeated)
                    paramMessage.fields.append(field)
                self.messages.append(paramMessage)
            else:
                has_void = True

            # 2.2 create ResultMessage
            if not method.returnType.is_void:
                resultMessage = ProtoMessage(
                    modelMessage.name + cap(method.name) + 'Result')
                field = ProtoField(
                    method.returnType.python_type,
                    'result',
                    1,
                    repeated=method.returnType.repeated)
                resultMessage.fields.append(field)
                self.messages.append(resultMessage)
            else:
                has_void = True

        # 3. create a service for the model
        service = GrpcService(modelMessage.name + 'Methods')
        for method in modelMessage.rpc_methods:

            if not method.has_params:
                param_type = 'Void'
            else:
                param_type = modelMessage.name + cap(method.name) + 'Param'

            if method.returnType.is_void:
                return_type = 'Void'
            else:
                return_type = modelMessage.name + cap(method.name) + 'Result'

            procedure = GrpcProcedure(
                method.name,
                param_type,
                return_type,
                clientSideStreaming=method.clientSideStreaming,
                serverSideStreaming=method.serverSideStreaming
            )
            service.procedures.append(procedure)
        self.service = service if modelMessage.rpc_methods else None

        if has_void:
            void_msg = ProtoMessage('Void')
            void_msg.fields.append(ProtoField('string', 'self', 1))
            self.messages.append(void_msg)
