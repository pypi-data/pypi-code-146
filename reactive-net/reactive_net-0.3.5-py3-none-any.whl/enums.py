from enum import IntEnum


class ReactiveCommand(IntEnum):
    Connect = 0x0
    Call = 0x1
    RemoteOutput = 0x2
    Load = 0x3
    Reset = 0x4
    RegisterEntrypoint = 0x5
    Output = 0x6  # called by software modules in SGX and Native
    RemoteRequest = 0x7

    def has_response(self):
        if self == ReactiveCommand.RemoteOutput:
            return False
        if self == ReactiveCommand.Output:
            return False

        return True


class ReactiveResult(IntEnum):
    Ok = 0x0
    IllegalCommand = 0x1
    IllegalPayload = 0x2
    InternalError = 0x3
    BadRequest = 0x4
    CryptoError = 0x5
    NotAttestedYet = 0x6
    GenericError = 0x7


class ReactiveEntrypoint(IntEnum):
    SetKey = 0x0
    Attest = 0x1
    Disable = 0x2
    HandleInput = 0x3
    HandleHandler = 0x4
