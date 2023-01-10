from protmo.pm import *
from protmo.ast import *
from protmo.ast_to_grpc_ast import AstToGrpcAst


def create_proto_file(package: str) -> None:

    content = 'syntax = "proto3";\n\n'
    content += f'package {package};\n\n'
    for modelClass in (Message.__subclasses__()):
        msg = MessageInfo(modelClass)
        proto_messages = AstToGrpcAst(msg)
        content += f'\n// {msg.name} ------\n\n'
        content += str(proto_messages.messages[0]) + '\n\n'
        if proto_messages.service:
            content += str(proto_messages.service) + '\n\n'
        for proto_msg in proto_messages.messages[1:]:
            content += str(proto_msg) + '\n\n'

    with open(f'{package}.proto', 'w') as f:
        f.write(content)
