import base64
import dataclasses
import datetime
from dateutil.parser import isoparse
import hashlib
import typing

# ZeroTime is the zero time used by default for spin types.
ZeroTime = datetime.datetime(1, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)


# SHA256 creates a sum of the data
def SHA256(b: bytes):
    m = hashlib.sha256()
    m.update(b)
    return m.hexdigest()


""" CitizenName is a helper type for a spin CitizenName """
CitizenName = str
""" KeyType is a helper type for a spin KeyType """
KeyType = str
""" KeyName is a helper type for a spin KeyName """
KeyName = str


@dataclasses.dataclass
class Key:
    """
    Key is a helper class for a spin Key.
    """

    type: KeyType = ""
    citizen: CitizenName = ""
    name: KeyName = ""
    data: str = ""
    meta: str = ""
    created_at: datetime.datetime = ZeroTime
    expires_at: datetime.datetime = ZeroTime

    @staticmethod
    def from_json(j: dict):
        k = Key()
        k.unmarshal_json(j)
        return k

    def unmarshal_json(self, j: dict):
        if "Type" in j:
            self.type = KeyType(j["Type"])
        if "Citizen" in j:
            self.citizen = CitizenName(j["Citizen"])
        if "Name" in j:
            self.name = KeyName(j["Name"])
        if "Data" in j:
            self.data = j["Data"]
        if "Meta" in j:
            self.meta = j["Meta"]
        if "CreatedAt" in j:
            self.created_at = isoparse(j["CreatedAt"])
        if "ExpiresAt" in j:
            self.expires_at = isoparse(j["ExpiresAt"])

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Type"] = self.type
        j["Citizen"] = self.citizen
        j["Name"] = self.name
        j["Data"] = self.data
        j["Meta"] = self.meta
        j["CreatedAt"] = self.created_at.isoformat()
        j["ExpiresAt"] = self.expires_at.isoformat()


@dataclasses.dataclass
class PrivateKey:
    key: Key = dataclasses.field(default_factory=Key)
    private: str = ""

    @staticmethod
    def from_json(j: dict):
        k = PrivateKey()
        k.unmarshal_json(j)
        return k

    def unmarshal_json(self, j: dict):
        self.key.unmarshal_json(j)
        if "Private" in j:
            self.private = j["Private"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Key"] = self.key.to_json()
        j["Private"] = self.private
        return j


@dataclasses.dataclass
class KeyWhichRequest:
    public: str = ""
    private: str = ""

    @staticmethod
    def from_json(j: dict):
        r = KeyWhichRequest()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Public" in j:
            self.public = j["Public"]
        if "Private" in j:
            self.private = j["Private"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Public"] = self.public
        j["Private"] = self.private
        return j


@dataclasses.dataclass
class KeyWhichResponse:
    key: typing.Optional[Key] = None
    error: str = ""

    @staticmethod
    def from_json(j: dict):
        r = KeyWhichResponse()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Key" in j and j["Key"] is not None:
            self.key = Key.from_json(j["Key"])
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Key"] = self.key.to_json()
        j["Private"] = self.private
        return j


@dataclasses.dataclass
class KeyTempRequest:
    public: str = ""
    private: str = ""
    duration: int = 0  # nanoseconds

    @staticmethod
    def from_json(j: dict):
        r = KeyTempRequest()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Public" in j:
            self.public = j["Public"]
        if "Private" in j:
            self.private = j["Private"]
        if "Duration" in j:
            self.duration = j["Duration"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Public"] = self.public
        j["Private"] = self.private
        j["Duration"] = self.duration
        return j


@dataclasses.dataclass
class KeyTempResponse:
    key: typing.Optional[Key] = None
    private: str = ""
    error: str = ""

    @staticmethod
    def from_json(j: dict):
        r = KeyTempResponse()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Key" in j and j["Key"] is not None:
            self.key = Key.from_json(j["Key"])
        if "Private" in j:
            self.private = j["Private"]
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Key"] = self.key.to_json()
        j["Private"] = self.private
        j["Duration"] = self.duration
        return j


Path = str
Ref = str
DirEntryType = str

EntryMissing: DirEntryType = ""
EntryDir: DirEntryType = "dir"
EntryFile: DirEntryType = "file"

SeqNotExist = -1
SeqIgnore = 0
SeqBase = 1
MaxBlockSize = 10 * (1024 * 1024)


@dataclasses.dataclass
class DirBlock:
    ref: Ref = ""
    offset: int = 0
    size: int = 0

    @staticmethod
    def from_json(j: dict):
        r = DirBlock()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Ref" in j:
            self.ref = Ref(j["Ref"])
        if "Offset" in j:
            self.offset = j["Offset"]
        if "Size" in j:
            self.size = j["Size"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Ref"] = self.ref
        j["Offset"] = self.offset
        j["Size"] = self.size
        return j


@dataclasses.dataclass
class DirEntry:
    type: DirEntryType = EntryMissing
    blocks: list[DirBlock] = dataclasses.field(default_factory=list)
    citizen: CitizenName = ""
    path: Path = ""
    time: datetime.datetime = ZeroTime
    sequence: int = 0

    @staticmethod
    def from_json(j: dict):
        r = DirEntry()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Type" in j:
            self.type = DirEntryType(j["Type"])
        if "Blocks" in j and j["Blocks"] is not None:
            self.blocks = [DirBlock.from_json(d) for d in j["Blocks"]]
        if "Citizen" in j:
            self.citizen = j["Citizen"]
        if "Path" in j:
            self.path = j["Path"]
        if "Time" in j:
            self.time = isoparse(j["Time"])
        if "Sequence" in j:
            self.sequence = j["Sequence"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Type"] = self.type
        j["Blocks"] = [b.to_json() for b in self.blocks]
        j["Citizen"] = self.citizen
        j["Path"] = self.path
        j["Time"] = self.time.isoformat()
        j["Sequence"] = self.sequence
        return j

    def size(self):
        return sum([b.size for b in self.blocks])


DirOperation = str

MissingDirOperation: DirOperation = ""
PutDirOperation: DirOperation = "put"
DelDirOperation: DirOperation = "del"


@dataclasses.dataclass
class DirOp:
    type: DirOperation = MissingDirOperation
    entry: DirEntry = dataclasses.field(default_factory=DirEntry)  # embedded

    @staticmethod
    def from_json(j: dict):
        r = DirOp()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Type" in j:
            self.type = DirOperation(j["Type"])
        if "Entry" in j:
            self.entry = DirEntry.from_json(j["Entry"])

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Type"] = self.type
        j["Entry"] = self.entry.to_json()
        return j


BitOperation = str

MissingBitOperation = ""
DelBitOperation = "del"
GetBitOperation = "get"
PutBitOperation = "put"


@dataclasses.dataclass
class BitOp:
    type: BitOperation = MissingBitOperation
    ref: Ref = ""
    bytes: bytes = b""

    @staticmethod
    def from_json(j: dict):
        r = BitOp()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Type" in j:
            self.type = BitOperation(j["Type"])
        if "Ref" in j:
            self.ref = Ref(j["Ref"])
        if "Bytes" in j and j["Bytes"] is not None:
            self.bytes = base64.b64decode(j["Bytes"])

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Type"] = self.type
        j["Ref"] = self.ref
        j["Bytes"] = base64.b64encode(self.bytes).decode()
        return j


@dataclasses.dataclass
class RefData:
    ref: Ref = ""
    volatile: bool = False
    duration: int = 0

    @staticmethod
    def from_json(j: dict):
        r = BitOp()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Ref" in j:
            self.ref = Ref(j["Ref"])
        if "Volatile" in j:
            self.ref = Ref(j["Volatile"])
        if "Duration" in j:
            self.duration = j["Duration"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Ref"] = self.ref
        j["Volatile"] = self.volatile
        j["Duration"] = self.duration
        return j


@dataclasses.dataclass
class BitApplyRequest:
    public: str = ""
    private: str = ""
    ops: list[BitOp] = dataclasses.field(default_factory=list)

    @staticmethod
    def from_json(j: dict):
        r = BitApplyRequest()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Public" in j:
            self.public = Ref(j["Public"])
        if "Private" in j:
            self.private = Ref(j["Private"])
        if "Ops" in j and j["Ops"] is not None:
            self.ops = [BitOp.from_json(o) for o in j["Ops"]]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Public"] = self.public
        j["Private"] = self.private
        j["Ops"] = [o.to_json() for o in self.ops]
        return j


@dataclasses.dataclass
class BitApplyOutcome:
    ref_data: RefData = dataclasses.field(default_factory=RefData)
    bytes: bytes = b""
    Error: str = ""

    @staticmethod
    def from_json(j: dict):
        r = BitApplyOutcome()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "RefData" in j:
            self.ref_data = RefData.from_json(j["RefData"])
        if "Bytes" in j and j["Bytes"] is not None:
            self.bytes = base64.b64decode(j["Bytes"])
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        self.ref_data.unmarshal_json(j)
        j["RefData"] = self.ref_data.to_json()
        j["Bytes"] = base64.b64encode(self.bytes).decode()
        j["Error"] = self.error
        return j


@dataclasses.dataclass
class BitApplyResponse:
    outcomes: list[BitApplyOutcome] = dataclasses.field(default_factory=list)
    error: str = ""

    @staticmethod
    def from_json(j: dict):
        r = BitApplyResponse()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Outcomes" in j and j["Outcomes"] is not None:
            self.outcomes = [BitApplyOutcome.from_json(o) for o in j["Outcomes"]]
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Outcomes"] = [o.to_json() for o in self.outcomes]
        j["Error"] = self.error
        return j


@dataclasses.dataclass
class DirApplyRequest:
    public: str = ""
    private: str = ""
    ops: list[DirOp] = dataclasses.field(default_factory=list)

    @staticmethod
    def from_json(j: dict):
        r = DirApplyRequest()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Public" in j:
            self.public = Ref(j["Public"])
        if "Private" in j:
            self.private = Ref(j["Private"])
        if "Ops" in j and j["Ops"] is not None:
            self.ops = [DirOp.from_json(o) for o in j["Ops"]]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Public"] = self.public
        j["Private"] = self.private
        j["Ops"] = [o.to_json() for o in self.ops]
        return j


@dataclasses.dataclass
class DirApplyResponse:
    entries: list[DirEntry] = dataclasses.field(default_factory=list)
    error: str = ""

    @staticmethod
    def from_json(j: dict):
        r = DirApplyResponse()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Entries" in j and j["Entries"] is not None:
            self.entries = [DirEntry.from_json(e) for e in j["Entries"]]
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Entries"] = [e.to_json() for e in self.entries]
        j["Error"] = self.error
        return j


@dataclasses.dataclass
class DirTreeRequest:
    public: str = ""
    private: str = ""
    citizen: CitizenName = ""
    path: Path = ""
    level: int = 0

    @staticmethod
    def from_json(j: dict):
        r = DirTreeRequest()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Public" in j:
            self.public = Ref(j["Public"])
        if "Private" in j:
            self.private = Ref(j["Private"])
        if "Citizen" in j:
            self.citizen = CitizenName(j["CitizenName"])
        if "Path" in j:
            self.path = Path(j["Path"])
        if "Level" in j:
            self.level = j["Level"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Public"] = self.public
        j["Private"] = self.private
        j["Citizen"] = self.citizen
        j["Path"] = self.path
        j["Level"] = self.level
        return j


@dataclasses.dataclass
class DirTreeResponse:
    entries: list[DirEntry] = dataclasses.field(default_factory=list)
    error: str = ""

    @staticmethod
    def from_json(j: dict):
        r = DirTreeResponse()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Entries" in j and j["Entries"] is not None:
            self.entries = [DirEntry.from_json(d) for d in j["Entries"]]
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Entries"] = [e.to_json() for e in self.entries]
        j["Error"] = self.error
        return j
