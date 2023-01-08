from typing import Protocol, Optional, TypeVar, List, Generic, no_type_check
from dataclasses import dataclass

A = TypeVar("A")
B = TypeVar("B")


@dataclass
class Symbol(Generic[A, B]):
    # Either a list of at least one address or None if not defined for the region.
    addresses: A
    # Like addresses but memory-absolute
    absolute_addresses: A
    # None for most functions. Data fields should generally have a length defined.
    length: B
    description: str

    @property
    @no_type_check
    def address(self) -> int:
        """First / main address. Raises an IndexError/TypeError if no address is defined.
        """
        return self.addresses[0]

    @property
    @no_type_check
    def absolute_address(self) -> int:
        """First / main address (absolute). Raises an IndexError/TypeError if no address is defined.
        """
        return self.absolute_addresses[0]


T = TypeVar("T")
U = TypeVar("U")
L = TypeVar("L")


class SectionProtocol(Protocol[T, U, L]):
    name: str
    description: str
    loadaddress: L
    length: int
    functions: T
    data: U


class Arm7FunctionsProtocol(Protocol):
    EntryArm7: Symbol[
        Optional[List[int]],
        None,
    ]


class Arm7DataProtocol(Protocol):
    pass


Arm7Protocol = SectionProtocol[
    Arm7FunctionsProtocol,
    Arm7DataProtocol,
    Optional[int],
]


class Arm9FunctionsProtocol(Protocol):
    EntryArm9: Symbol[
        Optional[List[int]],
        None,
    ]

    InitMemAllocTable: Symbol[
        Optional[List[int]],
        None,
    ]

    SetMemAllocatorParams: Symbol[
        Optional[List[int]],
        None,
    ]

    GetAllocArenaDefault: Symbol[
        Optional[List[int]],
        None,
    ]

    GetFreeArenaDefault: Symbol[
        Optional[List[int]],
        None,
    ]

    InitMemArena: Symbol[
        Optional[List[int]],
        None,
    ]

    MemAllocFlagsToBlockType: Symbol[
        Optional[List[int]],
        None,
    ]

    FindAvailableMemBlock: Symbol[
        Optional[List[int]],
        None,
    ]

    SplitMemBlock: Symbol[
        Optional[List[int]],
        None,
    ]

    MemAlloc: Symbol[
        Optional[List[int]],
        None,
    ]

    MemFree: Symbol[
        Optional[List[int]],
        None,
    ]

    MemArenaAlloc: Symbol[
        Optional[List[int]],
        None,
    ]

    CreateMemArena: Symbol[
        Optional[List[int]],
        None,
    ]

    MemLocateSet: Symbol[
        Optional[List[int]],
        None,
    ]

    MemLocateUnset: Symbol[
        Optional[List[int]],
        None,
    ]

    RoundUpDiv256: Symbol[
        Optional[List[int]],
        None,
    ]

    UFixedPoint64CmpLt: Symbol[
        Optional[List[int]],
        None,
    ]

    MultiplyByFixedPoint: Symbol[
        Optional[List[int]],
        None,
    ]

    UMultiplyByFixedPoint: Symbol[
        Optional[List[int]],
        None,
    ]

    IntToFixedPoint64: Symbol[
        Optional[List[int]],
        None,
    ]

    FixedPoint64ToInt: Symbol[
        Optional[List[int]],
        None,
    ]

    FixedPoint32To64: Symbol[
        Optional[List[int]],
        None,
    ]

    NegateFixedPoint64: Symbol[
        Optional[List[int]],
        None,
    ]

    FixedPoint64IsZero: Symbol[
        Optional[List[int]],
        None,
    ]

    FixedPoint64IsNegative: Symbol[
        Optional[List[int]],
        None,
    ]

    FixedPoint64CmpLt: Symbol[
        Optional[List[int]],
        None,
    ]

    MultiplyFixedPoint64: Symbol[
        Optional[List[int]],
        None,
    ]

    DivideFixedPoint64: Symbol[
        Optional[List[int]],
        None,
    ]

    UMultiplyFixedPoint64: Symbol[
        Optional[List[int]],
        None,
    ]

    UDivideFixedPoint64: Symbol[
        Optional[List[int]],
        None,
    ]

    AddFixedPoint64: Symbol[
        Optional[List[int]],
        None,
    ]

    ClampedLn: Symbol[
        Optional[List[int]],
        None,
    ]

    GetRngSeed: Symbol[
        Optional[List[int]],
        None,
    ]

    SetRngSeed: Symbol[
        Optional[List[int]],
        None,
    ]

    Rand16Bit: Symbol[
        Optional[List[int]],
        None,
    ]

    RandInt: Symbol[
        Optional[List[int]],
        None,
    ]

    RandRange: Symbol[
        Optional[List[int]],
        None,
    ]

    Rand32Bit: Symbol[
        Optional[List[int]],
        None,
    ]

    RandIntSafe: Symbol[
        Optional[List[int]],
        None,
    ]

    RandRangeSafe: Symbol[
        Optional[List[int]],
        None,
    ]

    WaitForever: Symbol[
        Optional[List[int]],
        None,
    ]

    InterruptMasterDisable: Symbol[
        Optional[List[int]],
        None,
    ]

    InterruptMasterEnable: Symbol[
        Optional[List[int]],
        None,
    ]

    InitMemAllocTableVeneer: Symbol[
        Optional[List[int]],
        None,
    ]

    ZInit8: Symbol[
        Optional[List[int]],
        None,
    ]

    PointsToZero: Symbol[
        Optional[List[int]],
        None,
    ]

    MemZero: Symbol[
        Optional[List[int]],
        None,
    ]

    MemZero16: Symbol[
        Optional[List[int]],
        None,
    ]

    MemZero32: Symbol[
        Optional[List[int]],
        None,
    ]

    MemsetSimple: Symbol[
        Optional[List[int]],
        None,
    ]

    Memset32: Symbol[
        Optional[List[int]],
        None,
    ]

    MemcpySimple: Symbol[
        Optional[List[int]],
        None,
    ]

    Memcpy16: Symbol[
        Optional[List[int]],
        None,
    ]

    Memcpy32: Symbol[
        Optional[List[int]],
        None,
    ]

    TaskProcBoot: Symbol[
        Optional[List[int]],
        None,
    ]

    EnableAllInterrupts: Symbol[
        Optional[List[int]],
        None,
    ]

    GetTime: Symbol[
        Optional[List[int]],
        None,
    ]

    DisableAllInterrupts: Symbol[
        Optional[List[int]],
        None,
    ]

    SoundResume: Symbol[
        Optional[List[int]],
        None,
    ]

    CardPullOutWithStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    CardPullOut: Symbol[
        Optional[List[int]],
        None,
    ]

    CardBackupError: Symbol[
        Optional[List[int]],
        None,
    ]

    HaltProcessDisp: Symbol[
        Optional[List[int]],
        None,
    ]

    OverlayIsLoaded: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadOverlay: Symbol[
        Optional[List[int]],
        None,
    ]

    UnloadOverlay: Symbol[
        Optional[List[int]],
        None,
    ]

    EuclideanNorm: Symbol[
        Optional[List[int]],
        None,
    ]

    ClampComponentAbs: Symbol[
        Optional[List[int]],
        None,
    ]

    GetHeldButtons: Symbol[
        Optional[List[int]],
        None,
    ]

    GetPressedButtons: Symbol[
        Optional[List[int]],
        None,
    ]

    GetReleasedStylus: Symbol[
        Optional[List[int]],
        None,
    ]

    KeyWaitInit: Symbol[
        Optional[List[int]],
        None,
    ]

    DataTransferInit: Symbol[
        Optional[List[int]],
        None,
    ]

    DataTransferStop: Symbol[
        Optional[List[int]],
        None,
    ]

    FileInitVeneer: Symbol[
        Optional[List[int]],
        None,
    ]

    FileOpen: Symbol[
        Optional[List[int]],
        None,
    ]

    FileGetSize: Symbol[
        Optional[List[int]],
        None,
    ]

    FileRead: Symbol[
        Optional[List[int]],
        None,
    ]

    FileSeek: Symbol[
        Optional[List[int]],
        None,
    ]

    FileClose: Symbol[
        Optional[List[int]],
        None,
    ]

    UnloadFile: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadFileFromRom: Symbol[
        Optional[List[int]],
        None,
    ]

    GetDebugFlag1: Symbol[
        Optional[List[int]],
        None,
    ]

    SetDebugFlag1: Symbol[
        Optional[List[int]],
        None,
    ]

    AppendProgPos: Symbol[
        Optional[List[int]],
        None,
    ]

    DebugPrintTrace: Symbol[
        Optional[List[int]],
        None,
    ]

    DebugPrint0: Symbol[
        Optional[List[int]],
        None,
    ]

    GetDebugFlag2: Symbol[
        Optional[List[int]],
        None,
    ]

    SetDebugFlag2: Symbol[
        Optional[List[int]],
        None,
    ]

    DebugPrint: Symbol[
        Optional[List[int]],
        None,
    ]

    FatalError: Symbol[
        Optional[List[int]],
        None,
    ]

    OpenAllPackFiles: Symbol[
        Optional[List[int]],
        None,
    ]

    GetFileLengthInPackWithPackNb: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadFileInPackWithPackId: Symbol[
        Optional[List[int]],
        None,
    ]

    AllocAndLoadFileInPack: Symbol[
        Optional[List[int]],
        None,
    ]

    OpenPackFile: Symbol[
        Optional[List[int]],
        None,
    ]

    GetFileLengthInPack: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadFileInPack: Symbol[
        Optional[List[int]],
        None,
    ]

    GetDamageSource: Symbol[
        Optional[List[int]],
        None,
    ]

    GetItemCategoryVeneer: Symbol[
        Optional[List[int]],
        None,
    ]

    GetItemMoveId16: Symbol[
        Optional[List[int]],
        None,
    ]

    IsThrownItem: Symbol[
        Optional[List[int]],
        None,
    ]

    IsNotMoney: Symbol[
        Optional[List[int]],
        None,
    ]

    IsEdible: Symbol[
        Optional[List[int]],
        None,
    ]

    IsHM: Symbol[
        Optional[List[int]],
        None,
    ]

    IsGummi: Symbol[
        Optional[List[int]],
        None,
    ]

    IsAuraBow: Symbol[
        Optional[List[int]],
        None,
    ]

    InitItem: Symbol[
        Optional[List[int]],
        None,
    ]

    InitStandardItem: Symbol[
        Optional[List[int]],
        None,
    ]

    GetDisplayedBuyPrice: Symbol[
        Optional[List[int]],
        None,
    ]

    GetDisplayedSellPrice: Symbol[
        Optional[List[int]],
        None,
    ]

    GetActualBuyPrice: Symbol[
        Optional[List[int]],
        None,
    ]

    GetActualSellPrice: Symbol[
        Optional[List[int]],
        None,
    ]

    FindItemInInventory: Symbol[
        Optional[List[int]],
        None,
    ]

    SprintfStatic: Symbol[
        Optional[List[int]],
        None,
    ]

    ItemZInit: Symbol[
        Optional[List[int]],
        None,
    ]

    WriteItemsToSave: Symbol[
        Optional[List[int]],
        None,
    ]

    ReadItemsFromSave: Symbol[
        Optional[List[int]],
        None,
    ]

    IsItemAvailableInDungeonGroup: Symbol[
        Optional[List[int]],
        None,
    ]

    GetItemIdFromList: Symbol[
        Optional[List[int]],
        None,
    ]

    NormalizeTreasureBox: Symbol[
        Optional[List[int]],
        None,
    ]

    RemoveEmptyItems: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadItemPspi2n: Symbol[
        Optional[List[int]],
        None,
    ]

    GetExclusiveItemType: Symbol[
        Optional[List[int]],
        None,
    ]

    GetExclusiveItemOffsetEnsureValid: Symbol[
        Optional[List[int]],
        None,
    ]

    IsItemValid: Symbol[
        Optional[List[int]],
        None,
    ]

    GetExclusiveItemParameter: Symbol[
        Optional[List[int]],
        None,
    ]

    GetItemCategory: Symbol[
        Optional[List[int]],
        None,
    ]

    EnsureValidItem: Symbol[
        Optional[List[int]],
        None,
    ]

    GetItemName: Symbol[
        Optional[List[int]],
        None,
    ]

    GetItemNameFormatted: Symbol[
        Optional[List[int]],
        None,
    ]

    GetItemBuyPrice: Symbol[
        Optional[List[int]],
        None,
    ]

    GetItemSellPrice: Symbol[
        Optional[List[int]],
        None,
    ]

    GetItemSpriteId: Symbol[
        Optional[List[int]],
        None,
    ]

    GetItemPaletteId: Symbol[
        Optional[List[int]],
        None,
    ]

    GetItemActionName: Symbol[
        Optional[List[int]],
        None,
    ]

    GetThrownItemQuantityLimit: Symbol[
        Optional[List[int]],
        None,
    ]

    GetItemMoveId: Symbol[
        Optional[List[int]],
        None,
    ]

    TestItemFlag0xE: Symbol[
        Optional[List[int]],
        None,
    ]

    IsItemInTimeDarkness: Symbol[
        Optional[List[int]],
        None,
    ]

    IsItemValidVeneer: Symbol[
        Optional[List[int]],
        None,
    ]

    SetGold: Symbol[
        Optional[List[int]],
        None,
    ]

    GetGold: Symbol[
        Optional[List[int]],
        None,
    ]

    SetMoneyCarried: Symbol[
        Optional[List[int]],
        None,
    ]

    GetCurrentBagCapacity: Symbol[
        Optional[List[int]],
        None,
    ]

    IsBagFull: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbItemsInBag: Symbol[
        Optional[List[int]],
        None,
    ]

    CountNbItemsOfTypeInBag: Symbol[
        Optional[List[int]],
        None,
    ]

    CountItemTypeInBag: Symbol[
        Optional[List[int]],
        None,
    ]

    IsItemInBag: Symbol[
        Optional[List[int]],
        None,
    ]

    IsItemWithFlagsInBag: Symbol[
        Optional[List[int]],
        None,
    ]

    IsItemInTreasureBoxes: Symbol[
        Optional[List[int]],
        None,
    ]

    IsHeldItemInBag: Symbol[
        Optional[List[int]],
        None,
    ]

    IsItemForSpecialSpawnInBag: Symbol[
        Optional[List[int]],
        None,
    ]

    HasStorableItems: Symbol[
        Optional[List[int]],
        None,
    ]

    GetItemIndex: Symbol[
        Optional[List[int]],
        None,
    ]

    GetEquivItemIndex: Symbol[
        Optional[List[int]],
        None,
    ]

    GetEquippedThrowableItem: Symbol[
        Optional[List[int]],
        None,
    ]

    GetFirstUnequippedItemOfType: Symbol[
        Optional[List[int]],
        None,
    ]

    CopyItemAtIdx: Symbol[
        Optional[List[int]],
        None,
    ]

    GetItemAtIdx: Symbol[
        Optional[List[int]],
        None,
    ]

    RemoveEmptyItemsInBag: Symbol[
        Optional[List[int]],
        None,
    ]

    RemoveItemNoHole: Symbol[
        Optional[List[int]],
        None,
    ]

    RemoveItem: Symbol[
        Optional[List[int]],
        None,
    ]

    RemoveHeldItemNoHole: Symbol[
        Optional[List[int]],
        None,
    ]

    RemoveItemByIdAndStackNoHole: Symbol[
        Optional[List[int]],
        None,
    ]

    RemoveEquivItem: Symbol[
        Optional[List[int]],
        None,
    ]

    RemoveEquivItemNoHole: Symbol[
        Optional[List[int]],
        None,
    ]

    DecrementStackItem: Symbol[
        Optional[List[int]],
        None,
    ]

    RemoveItemNoHoleCheck: Symbol[
        Optional[List[int]],
        None,
    ]

    RemoveFirstUnequippedItemOfType: Symbol[
        Optional[List[int]],
        None,
    ]

    RemoveAllItems: Symbol[
        Optional[List[int]],
        None,
    ]

    RemoveAllItemsStartingAt: Symbol[
        Optional[List[int]],
        None,
    ]

    SpecialProcAddItemToBag: Symbol[
        Optional[List[int]],
        None,
    ]

    AddItemToBagNoHeld: Symbol[
        Optional[List[int]],
        None,
    ]

    AddItemToBag: Symbol[
        Optional[List[int]],
        None,
    ]

    ScriptSpecialProcess0x39: Symbol[
        Optional[List[int]],
        None,
    ]

    CountItemTypeInStorage: Symbol[
        Optional[List[int]],
        None,
    ]

    RemoveItemsTypeInStorage: Symbol[
        Optional[List[int]],
        None,
    ]

    AddItemToStorage: Symbol[
        Optional[List[int]],
        None,
    ]

    SetMoneyStored: Symbol[
        Optional[List[int]],
        None,
    ]

    GetKecleonItems1: Symbol[
        Optional[List[int]],
        None,
    ]

    GetKecleonItems2: Symbol[
        Optional[List[int]],
        None,
    ]

    GetExclusiveItemOffset: Symbol[
        Optional[List[int]],
        None,
    ]

    ApplyExclusiveItemStatBoosts: Symbol[
        Optional[List[int]],
        None,
    ]

    SetExclusiveItemEffect: Symbol[
        Optional[List[int]],
        None,
    ]

    ExclusiveItemEffectFlagTest: Symbol[
        Optional[List[int]],
        None,
    ]

    IsExclusiveItemIdForMonster: Symbol[
        Optional[List[int]],
        None,
    ]

    IsExclusiveItemForMonster: Symbol[
        Optional[List[int]],
        None,
    ]

    BagHasExclusiveItemTypeForMonster: Symbol[
        Optional[List[int]],
        None,
    ]

    ProcessGinsengOverworld: Symbol[
        Optional[List[int]],
        None,
    ]

    ApplyGummiBoostsGroundMode: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadSynthBin: Symbol[
        Optional[List[int]],
        None,
    ]

    CloseSynthBin: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSynthItem: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadWazaP: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadWazaP2: Symbol[
        Optional[List[int]],
        None,
    ]

    UnloadCurrentWazaP: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveName: Symbol[
        Optional[List[int]],
        None,
    ]

    FormatMoveString: Symbol[
        Optional[List[int]],
        None,
    ]

    FormatMoveStringMore: Symbol[
        Optional[List[int]],
        None,
    ]

    InitMove: Symbol[
        Optional[List[int]],
        None,
    ]

    GetInfoMoveCheckId: Symbol[
        Optional[List[int]],
        None,
    ]

    GetInfoMoveGround: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveTargetAndRange: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveType: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMovesetLevelUpPtr: Symbol[
        Optional[List[int]],
        None,
    ]

    IsInvalidMoveset: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMovesetHmTmPtr: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMovesetEggPtr: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveAiWeight: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveNbStrikes: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveBasePower: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveBasePowerGround: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveAccuracyOrAiChance: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveBasePp: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMaxPp: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveMaxGinsengBoost: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveMaxGinsengBoostGround: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveCritChance: Symbol[
        Optional[List[int]],
        None,
    ]

    IsThawingMove: Symbol[
        Optional[List[int]],
        None,
    ]

    IsAffectedByTaunt: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveRangeId: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveActualAccuracy: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveBasePowerFromId: Symbol[
        Optional[List[int]],
        None,
    ]

    IsMoveRangeString19: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveMessageFromId: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbMoves: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMovesetIdx: Symbol[
        Optional[List[int]],
        None,
    ]

    IsReflectedByMagicCoat: Symbol[
        Optional[List[int]],
        None,
    ]

    CanBeSnatched: Symbol[
        Optional[List[int]],
        None,
    ]

    FailsWhileMuzzled: Symbol[
        Optional[List[int]],
        None,
    ]

    IsSoundMove: Symbol[
        Optional[List[int]],
        None,
    ]

    IsRecoilMove: Symbol[
        Optional[List[int]],
        None,
    ]

    AllManip1: Symbol[
        Optional[List[int]],
        None,
    ]

    AllManip2: Symbol[
        Optional[List[int]],
        None,
    ]

    ManipMoves1v1: Symbol[
        Optional[List[int]],
        None,
    ]

    ManipMoves1v2: Symbol[
        Optional[List[int]],
        None,
    ]

    ManipMoves2v1: Symbol[
        Optional[List[int]],
        None,
    ]

    ManipMoves2v2: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonMoveToGroundMove: Symbol[
        Optional[List[int]],
        None,
    ]

    GroundToDungeonMoveset: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonToGroundMoveset: Symbol[
        Optional[List[int]],
        None,
    ]

    GetInfoGroundMoveset: Symbol[
        Optional[List[int]],
        None,
    ]

    FindFirstFreeMovesetIdx: Symbol[
        Optional[List[int]],
        None,
    ]

    LearnMoves: Symbol[
        Optional[List[int]],
        None,
    ]

    CopyMoveTo: Symbol[
        Optional[List[int]],
        None,
    ]

    CopyMoveFrom: Symbol[
        Optional[List[int]],
        None,
    ]

    CopyMovesetTo: Symbol[
        Optional[List[int]],
        None,
    ]

    CopyMovesetFrom: Symbol[
        Optional[List[int]],
        None,
    ]

    Is2TurnsMove: Symbol[
        Optional[List[int]],
        None,
    ]

    IsRegularAttackOrProjectile: Symbol[
        Optional[List[int]],
        None,
    ]

    IsPunchMove: Symbol[
        Optional[List[int]],
        None,
    ]

    IsHealingWishOrLunarDance: Symbol[
        Optional[List[int]],
        None,
    ]

    IsCopyingMove: Symbol[
        Optional[List[int]],
        None,
    ]

    IsTrappingMove: Symbol[
        Optional[List[int]],
        None,
    ]

    IsOneHitKoMove: Symbol[
        Optional[List[int]],
        None,
    ]

    IsNot2TurnsMoveOrSketch: Symbol[
        Optional[List[int]],
        None,
    ]

    IsRealMove: Symbol[
        Optional[List[int]],
        None,
    ]

    IsMovesetValid: Symbol[
        Optional[List[int]],
        None,
    ]

    IsRealMoveInTimeDarkness: Symbol[
        Optional[List[int]],
        None,
    ]

    IsMovesetValidInTimeDarkness: Symbol[
        Optional[List[int]],
        None,
    ]

    GetFirstNotRealMoveInTimeDarkness: Symbol[
        Optional[List[int]],
        None,
    ]

    IsSameMove: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveCategory: Symbol[
        Optional[List[int]],
        None,
    ]

    GetPpIncrease: Symbol[
        Optional[List[int]],
        None,
    ]

    OpenWaza: Symbol[
        Optional[List[int]],
        None,
    ]

    SelectWaza: Symbol[
        Optional[List[int]],
        None,
    ]

    ManipBgmPlayback: Symbol[
        Optional[List[int]],
        None,
    ]

    SoundDriverReset: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadDseFile: Symbol[
        Optional[List[int]],
        None,
    ]

    PlaySeLoad: Symbol[
        Optional[List[int]],
        None,
    ]

    PlayBgm: Symbol[
        Optional[List[int]],
        None,
    ]

    StopBgm: Symbol[
        Optional[List[int]],
        None,
    ]

    ChangeBgm: Symbol[
        Optional[List[int]],
        None,
    ]

    PlayBgm2: Symbol[
        Optional[List[int]],
        None,
    ]

    StopBgm2: Symbol[
        Optional[List[int]],
        None,
    ]

    ChangeBgm2: Symbol[
        Optional[List[int]],
        None,
    ]

    PlayME: Symbol[
        Optional[List[int]],
        None,
    ]

    StopME: Symbol[
        Optional[List[int]],
        None,
    ]

    PlaySe: Symbol[
        Optional[List[int]],
        None,
    ]

    PlaySeFullSpec: Symbol[
        Optional[List[int]],
        None,
    ]

    SeChangeVolume: Symbol[
        Optional[List[int]],
        None,
    ]

    SeChangePan: Symbol[
        Optional[List[int]],
        None,
    ]

    StopSe: Symbol[
        Optional[List[int]],
        None,
    ]

    DeleteWanTableEntry: Symbol[
        Optional[List[int]],
        None,
    ]

    FindWanTableEntry: Symbol[
        Optional[List[int]],
        None,
    ]

    GetLoadedWanTableEntry: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadWanTableEntry: Symbol[
        Optional[List[int]],
        None,
    ]

    ReplaceWanFromBinFile: Symbol[
        Optional[List[int]],
        None,
    ]

    DeleteWanTableEntryVeneer: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadWteFromRom: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadWteFromFileDirectory: Symbol[
        Optional[List[int]],
        None,
    ]

    UnloadWte: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadWtuFromBin: Symbol[
        Optional[List[int]],
        None,
    ]

    ProcessWte: Symbol[
        Optional[List[int]],
        None,
    ]

    HandleSir0Translation: Symbol[
        Optional[List[int]],
        None,
    ]

    ConvertPointersSir0: Symbol[
        Optional[List[int]],
        None,
    ]

    HandleSir0TranslationVeneer: Symbol[
        Optional[List[int]],
        None,
    ]

    DecompressAtNormalVeneer: Symbol[
        Optional[List[int]],
        None,
    ]

    DecompressAtNormal: Symbol[
        Optional[List[int]],
        None,
    ]

    DecompressAtHalf: Symbol[
        Optional[List[int]],
        None,
    ]

    DecompressAtFromMemoryPointerVeneer: Symbol[
        Optional[List[int]],
        None,
    ]

    DecompressAtFromMemoryPointer: Symbol[
        Optional[List[int]],
        None,
    ]

    WriteByteFromMemoryPointer: Symbol[
        Optional[List[int]],
        None,
    ]

    GetAtSize: Symbol[
        Optional[List[int]],
        None,
    ]

    GetLanguageType: Symbol[
        Optional[List[int]],
        None,
    ]

    GetLanguage: Symbol[
        Optional[List[int]],
        None,
    ]

    StrcmpTag: Symbol[
        Optional[List[int]],
        None,
    ]

    StoiTag: Symbol[
        Optional[List[int]],
        None,
    ]

    AnalyzeText: Symbol[
        Optional[List[int]],
        None,
    ]

    PreprocessString: Symbol[
        Optional[List[int]],
        None,
    ]

    PreprocessStringFromMessageId: Symbol[
        Optional[List[int]],
        None,
    ]

    InitPreprocessorArgs: Symbol[
        Optional[List[int]],
        None,
    ]

    SetStringAccuracy: Symbol[
        Optional[List[int]],
        None,
    ]

    SetStringPower: Symbol[
        Optional[List[int]],
        None,
    ]

    SetQuestionMarks: Symbol[
        Optional[List[int]],
        None,
    ]

    StrcpySimple: Symbol[
        Optional[List[int]],
        None,
    ]

    StrncpySimple: Symbol[
        Optional[List[int]],
        None,
    ]

    StrncpySimpleNoPad: Symbol[
        Optional[List[int]],
        None,
    ]

    StrncmpSimple: Symbol[
        Optional[List[int]],
        None,
    ]

    StrncpySimpleNoPadSafe: Symbol[
        Optional[List[int]],
        None,
    ]

    SpecialStrcpy: Symbol[
        Optional[List[int]],
        None,
    ]

    GetStringFromFile: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadStringFile: Symbol[
        Optional[List[int]],
        None,
    ]

    GetStringFromFileVeneer: Symbol[
        Optional[List[int]],
        None,
    ]

    StringFromMessageId: Symbol[
        Optional[List[int]],
        None,
    ]

    CopyStringFromMessageId: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadTblTalk: Symbol[
        Optional[List[int]],
        None,
    ]

    GetTalkLine: Symbol[
        Optional[List[int]],
        None,
    ]

    SetScreenWindowsColor: Symbol[
        Optional[List[int]],
        None,
    ]

    SetBothScreensWindowsColor: Symbol[
        Optional[List[int]],
        None,
    ]

    GetDialogBoxField0xC: Symbol[
        Optional[List[int]],
        None,
    ]

    Arm9LoadUnkFieldNa0x2029EC8: Symbol[
        Optional[List[int]],
        None,
    ]

    Arm9StoreUnkFieldNa0x2029ED8: Symbol[
        Optional[List[int]],
        None,
    ]

    CreateNormalMenu: Symbol[
        Optional[List[int]],
        None,
    ]

    FreeNormalMenu: Symbol[
        Optional[List[int]],
        None,
    ]

    IsNormalMenuActive: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNormalMenuResult: Symbol[
        Optional[List[int]],
        None,
    ]

    CreateAdvancedMenu: Symbol[
        Optional[List[int]],
        None,
    ]

    FreeAdvancedMenu: Symbol[
        Optional[List[int]],
        None,
    ]

    IsAdvancedMenuActive: Symbol[
        Optional[List[int]],
        None,
    ]

    GetAdvancedMenuCurrentOption: Symbol[
        Optional[List[int]],
        None,
    ]

    GetAdvancedMenuResult: Symbol[
        Optional[List[int]],
        None,
    ]

    CreateDBox: Symbol[
        Optional[List[int]],
        None,
    ]

    FreeDBox: Symbol[
        Optional[List[int]],
        None,
    ]

    IsDBoxActive: Symbol[
        Optional[List[int]],
        None,
    ]

    ShowMessageInDBox: Symbol[
        Optional[List[int]],
        None,
    ]

    ShowDBox: Symbol[
        Optional[List[int]],
        None,
    ]

    CreatePortraitBox: Symbol[
        Optional[List[int]],
        None,
    ]

    FreePortraitBox: Symbol[
        Optional[List[int]],
        None,
    ]

    ShowPortraitBox: Symbol[
        Optional[List[int]],
        None,
    ]

    HidePortraitBox: Symbol[
        Optional[List[int]],
        None,
    ]

    IsMenuOptionActive: Symbol[
        Optional[List[int]],
        None,
    ]

    ShowKeyboard: Symbol[
        Optional[List[int]],
        None,
    ]

    GetKeyboardStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    GetKeyboardStringResult: Symbol[
        Optional[List[int]],
        None,
    ]

    PrintMoveOptionMenu: Symbol[
        Optional[List[int]],
        None,
    ]

    PrintIqSkillsMenu: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNotifyNote: Symbol[
        Optional[List[int]],
        None,
    ]

    SetNotifyNote: Symbol[
        Optional[List[int]],
        None,
    ]

    InitMainTeamAfterQuiz: Symbol[
        Optional[List[int]],
        None,
    ]

    ScriptSpecialProcess0x3: Symbol[
        Optional[List[int]],
        None,
    ]

    ScriptSpecialProcess0x4: Symbol[
        Optional[List[int]],
        None,
    ]

    ReadStringSave: Symbol[
        Optional[List[int]],
        None,
    ]

    CheckStringSave: Symbol[
        Optional[List[int]],
        None,
    ]

    WriteSaveFile: Symbol[
        Optional[List[int]],
        None,
    ]

    ReadSaveFile: Symbol[
        Optional[List[int]],
        None,
    ]

    CalcChecksum: Symbol[
        Optional[List[int]],
        None,
    ]

    CheckChecksum: Symbol[
        Optional[List[int]],
        None,
    ]

    NoteSaveBase: Symbol[
        Optional[List[int]],
        None,
    ]

    WriteQuickSaveInfo: Symbol[
        Optional[List[int]],
        None,
    ]

    ReadSaveHeader: Symbol[
        Optional[List[int]],
        None,
    ]

    NoteLoadBase: Symbol[
        Optional[List[int]],
        None,
    ]

    ReadQuickSaveInfo: Symbol[
        Optional[List[int]],
        None,
    ]

    GetGameMode: Symbol[
        Optional[List[int]],
        None,
    ]

    InitScriptVariableValues: Symbol[
        Optional[List[int]],
        None,
    ]

    InitEventFlagScriptVars: Symbol[
        Optional[List[int]],
        None,
    ]

    ZinitScriptVariable: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadScriptVariableRaw: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadScriptVariableValue: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadScriptVariableValueAtIndex: Symbol[
        Optional[List[int]],
        None,
    ]

    SaveScriptVariableValue: Symbol[
        Optional[List[int]],
        None,
    ]

    SaveScriptVariableValueAtIndex: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadScriptVariableValueSum: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadScriptVariableValueBytes: Symbol[
        Optional[List[int]],
        None,
    ]

    SaveScriptVariableValueBytes: Symbol[
        Optional[List[int]],
        None,
    ]

    ScriptVariablesEqual: Symbol[
        Optional[List[int]],
        None,
    ]

    EventFlagBackup: Symbol[
        Optional[List[int]],
        None,
    ]

    DumpScriptVariableValues: Symbol[
        Optional[List[int]],
        None,
    ]

    RestoreScriptVariableValues: Symbol[
        Optional[List[int]],
        None,
    ]

    InitScenarioScriptVars: Symbol[
        Optional[List[int]],
        None,
    ]

    SetScenarioScriptVar: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSpecialEpisodeType: Symbol[
        Optional[List[int]],
        None,
    ]

    HasPlayedOldGame: Symbol[
        Optional[List[int]],
        None,
    ]

    GetPerformanceFlagWithChecks: Symbol[
        Optional[List[int]],
        None,
    ]

    GetScenarioBalance: Symbol[
        Optional[List[int]],
        None,
    ]

    ScenarioFlagBackup: Symbol[
        Optional[List[int]],
        None,
    ]

    InitWorldMapScriptVars: Symbol[
        Optional[List[int]],
        None,
    ]

    InitDungeonListScriptVars: Symbol[
        Optional[List[int]],
        None,
    ]

    SetDungeonConquest: Symbol[
        Optional[List[int]],
        None,
    ]

    CheckDungeonOpen: Symbol[
        Optional[List[int]],
        None,
    ]

    GlobalProgressAlloc: Symbol[
        Optional[List[int]],
        None,
    ]

    ResetGlobalProgress: Symbol[
        Optional[List[int]],
        None,
    ]

    SetMonsterFlag1: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMonsterFlag1: Symbol[
        Optional[List[int]],
        None,
    ]

    SetMonsterFlag2: Symbol[
        Optional[List[int]],
        None,
    ]

    HasMonsterBeenAttackedInDungeons: Symbol[
        Optional[List[int]],
        None,
    ]

    SetDungeonTipShown: Symbol[
        Optional[List[int]],
        None,
    ]

    GetDungeonTipShown: Symbol[
        Optional[List[int]],
        None,
    ]

    SetMaxReachedFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMaxReachedFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    IncrementNbAdventures: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbAdventures: Symbol[
        Optional[List[int]],
        None,
    ]

    CanMonsterSpawn: Symbol[
        Optional[List[int]],
        None,
    ]

    IncrementExclusiveMonsterCounts: Symbol[
        Optional[List[int]],
        None,
    ]

    CopyProgressInfoTo: Symbol[
        Optional[List[int]],
        None,
    ]

    CopyProgressInfoFromScratchTo: Symbol[
        Optional[List[int]],
        None,
    ]

    CopyProgressInfoFrom: Symbol[
        Optional[List[int]],
        None,
    ]

    CopyProgressInfoFromScratchFrom: Symbol[
        Optional[List[int]],
        None,
    ]

    SetPortraitMonsterId: Symbol[
        Optional[List[int]],
        None,
    ]

    SetPortraitExpressionId: Symbol[
        Optional[List[int]],
        None,
    ]

    SetPortraitUnknownAttr: Symbol[
        Optional[List[int]],
        None,
    ]

    SetPortraitAttrStruct: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadPortrait: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbFloors: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbFloorsPlusOne: Symbol[
        Optional[List[int]],
        None,
    ]

    GetDungeonGroup: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbPrecedingFloors: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbFloorsDungeonGroup: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonFloorToGroupFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    GetGroundNameId: Symbol[
        Optional[List[int]],
        None,
    ]

    SetAdventureLogStructLocation: Symbol[
        Optional[List[int]],
        None,
    ]

    SetAdventureLogDungeonFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    GetAdventureLogDungeonFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    ClearAdventureLogStruct: Symbol[
        Optional[List[int]],
        None,
    ]

    SetAdventureLogCompleted: Symbol[
        Optional[List[int]],
        None,
    ]

    IsAdventureLogNotEmpty: Symbol[
        Optional[List[int]],
        None,
    ]

    GetAdventureLogCompleted: Symbol[
        Optional[List[int]],
        None,
    ]

    IncrementNbDungeonsCleared: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbDungeonsCleared: Symbol[
        Optional[List[int]],
        None,
    ]

    IncrementNbFriendRescues: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbFriendRescues: Symbol[
        Optional[List[int]],
        None,
    ]

    IncrementNbEvolutions: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbEvolutions: Symbol[
        Optional[List[int]],
        None,
    ]

    IncrementNbSteals: Symbol[
        Optional[List[int]],
        None,
    ]

    IncrementNbEggsHatched: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbEggsHatched: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbPokemonJoined: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbMovesLearned: Symbol[
        Optional[List[int]],
        None,
    ]

    SetVictoriesOnOneFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    GetVictoriesOnOneFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    SetPokemonJoined: Symbol[
        Optional[List[int]],
        None,
    ]

    SetPokemonBattled: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbPokemonBattled: Symbol[
        Optional[List[int]],
        None,
    ]

    IncrementNbBigTreasureWins: Symbol[
        Optional[List[int]],
        None,
    ]

    SetNbBigTreasureWins: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbBigTreasureWins: Symbol[
        Optional[List[int]],
        None,
    ]

    SetNbRecycled: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbRecycled: Symbol[
        Optional[List[int]],
        None,
    ]

    IncrementNbSkyGiftsSent: Symbol[
        Optional[List[int]],
        None,
    ]

    SetNbSkyGiftsSent: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbSkyGiftsSent: Symbol[
        Optional[List[int]],
        None,
    ]

    ComputeSpecialCounters: Symbol[
        Optional[List[int]],
        None,
    ]

    RecruitSpecialPokemonLog: Symbol[
        Optional[List[int]],
        None,
    ]

    IncrementNbFainted: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbFainted: Symbol[
        Optional[List[int]],
        None,
    ]

    SetItemAcquired: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbItemAcquired: Symbol[
        Optional[List[int]],
        None,
    ]

    SetChallengeLetterCleared: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSentryDutyGamePoints: Symbol[
        Optional[List[int]],
        None,
    ]

    SetSentryDutyGamePoints: Symbol[
        Optional[List[int]],
        None,
    ]

    CopyLogTo: Symbol[
        Optional[List[int]],
        None,
    ]

    CopyLogFrom: Symbol[
        Optional[List[int]],
        None,
    ]

    GetAbilityString: Symbol[
        Optional[List[int]],
        None,
    ]

    GetAbilityDescStringId: Symbol[
        Optional[List[int]],
        None,
    ]

    GetTypeStringId: Symbol[
        Optional[List[int]],
        None,
    ]

    CopyBitsTo: Symbol[
        Optional[List[int]],
        None,
    ]

    CopyBitsFrom: Symbol[
        Optional[List[int]],
        None,
    ]

    StoreDefaultTeamName: Symbol[
        Optional[List[int]],
        None,
    ]

    GetTeamNameCheck: Symbol[
        Optional[List[int]],
        None,
    ]

    GetTeamName: Symbol[
        Optional[List[int]],
        None,
    ]

    SetTeamName: Symbol[
        Optional[List[int]],
        None,
    ]

    SubFixedPoint: Symbol[
        Optional[List[int]],
        None,
    ]

    BinToDecFixedPoint: Symbol[
        Optional[List[int]],
        None,
    ]

    CeilFixedPoint: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonGoesUp: Symbol[
        Optional[List[int]],
        None,
    ]

    GetTurnLimit: Symbol[
        Optional[List[int]],
        None,
    ]

    DoesNotSaveWhenEntering: Symbol[
        Optional[List[int]],
        None,
    ]

    TreasureBoxDropsEnabled: Symbol[
        Optional[List[int]],
        None,
    ]

    IsLevelResetDungeon: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMaxItemsAllowed: Symbol[
        Optional[List[int]],
        None,
    ]

    IsMoneyAllowed: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMaxRescueAttempts: Symbol[
        Optional[List[int]],
        None,
    ]

    IsRecruitingAllowed: Symbol[
        Optional[List[int]],
        None,
    ]

    GetLeaderChangeFlag: Symbol[
        Optional[List[int]],
        None,
    ]

    GetUnknownDungeonOption: Symbol[
        Optional[List[int]],
        None,
    ]

    CanEnemyEvolve: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMaxMembersAllowed: Symbol[
        Optional[List[int]],
        None,
    ]

    IsIqEnabled: Symbol[
        Optional[List[int]],
        None,
    ]

    IsTrapInvisibleWhenAttacking: Symbol[
        Optional[List[int]],
        None,
    ]

    JoinedAtRangeCheck: Symbol[
        Optional[List[int]],
        None,
    ]

    IsDojoDungeon: Symbol[
        Optional[List[int]],
        None,
    ]

    IsFutureDungeon: Symbol[
        Optional[List[int]],
        None,
    ]

    IsSpecialEpisodeDungeon: Symbol[
        Optional[List[int]],
        None,
    ]

    RetrieveFromItemList1: Symbol[
        Optional[List[int]],
        None,
    ]

    IsForbiddenFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    Copy16BitsFrom: Symbol[
        Optional[List[int]],
        None,
    ]

    RetrieveFromItemList2: Symbol[
        Optional[List[int]],
        None,
    ]

    IsInvalidForMission: Symbol[
        Optional[List[int]],
        None,
    ]

    IsExpEnabledInDungeon: Symbol[
        Optional[List[int]],
        None,
    ]

    IsSkyExclusiveDungeon: Symbol[
        Optional[List[int]],
        None,
    ]

    JoinedAtRangeCheck2: Symbol[
        Optional[List[int]],
        None,
    ]

    GetBagCapacity: Symbol[
        Optional[List[int]],
        None,
    ]

    GetBagCapacitySpecialEpisode: Symbol[
        Optional[List[int]],
        None,
    ]

    GetRankUpEntry: Symbol[
        Optional[List[int]],
        None,
    ]

    GetBgRegionArea: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadMonsterMd: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNameRaw: Symbol[
        Optional[List[int]],
        None,
    ]

    GetName: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNameWithGender: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSpeciesString: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNameString: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSpriteIndex: Symbol[
        Optional[List[int]],
        None,
    ]

    GetDexNumber: Symbol[
        Optional[List[int]],
        None,
    ]

    GetCategoryString: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMonsterGender: Symbol[
        Optional[List[int]],
        None,
    ]

    GetBodySize: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSpriteSize: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSpriteFileSize: Symbol[
        Optional[List[int]],
        None,
    ]

    GetShadowSize: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSpeedStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMobilityType: Symbol[
        Optional[List[int]],
        None,
    ]

    GetRegenSpeed: Symbol[
        Optional[List[int]],
        None,
    ]

    GetCanMoveFlag: Symbol[
        Optional[List[int]],
        None,
    ]

    GetChanceAsleep: Symbol[
        Optional[List[int]],
        None,
    ]

    GetLowKickMultiplier: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSize: Symbol[
        Optional[List[int]],
        None,
    ]

    GetBaseHp: Symbol[
        Optional[List[int]],
        None,
    ]

    CanThrowItems: Symbol[
        Optional[List[int]],
        None,
    ]

    CanEvolve: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMonsterPreEvolution: Symbol[
        Optional[List[int]],
        None,
    ]

    GetBaseOffensiveStat: Symbol[
        Optional[List[int]],
        None,
    ]

    GetBaseDefensiveStat: Symbol[
        Optional[List[int]],
        None,
    ]

    GetType: Symbol[
        Optional[List[int]],
        None,
    ]

    GetAbility: Symbol[
        Optional[List[int]],
        None,
    ]

    GetRecruitRate2: Symbol[
        Optional[List[int]],
        None,
    ]

    GetRecruitRate1: Symbol[
        Optional[List[int]],
        None,
    ]

    GetExp: Symbol[
        Optional[List[int]],
        None,
    ]

    GetEvoParameters: Symbol[
        Optional[List[int]],
        None,
    ]

    GetTreasureBoxChances: Symbol[
        Optional[List[int]],
        None,
    ]

    GetIqGroup: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSpawnThreshold: Symbol[
        Optional[List[int]],
        None,
    ]

    NeedsItemToSpawn: Symbol[
        Optional[List[int]],
        None,
    ]

    GetExclusiveItem: Symbol[
        Optional[List[int]],
        None,
    ]

    GetFamilyIndex: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadM2nAndN2m: Symbol[
        Optional[List[int]],
        None,
    ]

    IsNotNickname: Symbol[
        Optional[List[int]],
        None,
    ]

    GetLvlStats: Symbol[
        Optional[List[int]],
        None,
    ]

    GetEvoFamily: Symbol[
        Optional[List[int]],
        None,
    ]

    GetEvolutions: Symbol[
        Optional[List[int]],
        None,
    ]

    ShuffleHiddenPower: Symbol[
        Optional[List[int]],
        None,
    ]

    GetBaseForm: Symbol[
        Optional[List[int]],
        None,
    ]

    GetBaseFormBurmyWormadamShellosGastrodonCherrim: Symbol[
        Optional[List[int]],
        None,
    ]

    GetBaseFormCastformCherrimDeoxys: Symbol[
        Optional[List[int]],
        None,
    ]

    GetAllBaseForms: Symbol[
        Optional[List[int]],
        None,
    ]

    GetDexNumberVeneer: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMonsterIdFromSpawnEntry: Symbol[
        Optional[List[int]],
        None,
    ]

    SetMonsterId: Symbol[
        Optional[List[int]],
        None,
    ]

    SetMonsterLevelAndId: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMonsterLevelFromSpawnEntry: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMonsterGenderVeneer: Symbol[
        Optional[List[int]],
        None,
    ]

    IsMonsterValid: Symbol[
        Optional[List[int]],
        None,
    ]

    IsUnown: Symbol[
        Optional[List[int]],
        None,
    ]

    IsShaymin: Symbol[
        Optional[List[int]],
        None,
    ]

    IsCastform: Symbol[
        Optional[List[int]],
        None,
    ]

    IsCherrim: Symbol[
        Optional[List[int]],
        None,
    ]

    IsDeoxys: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSecondFormIfValid: Symbol[
        Optional[List[int]],
        None,
    ]

    FemaleToMaleForm: Symbol[
        Optional[List[int]],
        None,
    ]

    GetBaseFormCastformDeoxysCherrim: Symbol[
        Optional[List[int]],
        None,
    ]

    BaseFormsEqual: Symbol[
        Optional[List[int]],
        None,
    ]

    DexNumbersEqual: Symbol[
        Optional[List[int]],
        None,
    ]

    GendersEqual: Symbol[
        Optional[List[int]],
        None,
    ]

    GendersEqualNotGenderless: Symbol[
        Optional[List[int]],
        None,
    ]

    IsMonsterOnTeam: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNbRecruited: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMember: Symbol[
        Optional[List[int]],
        None,
    ]

    GetHeroStrIdIfExists: Symbol[
        Optional[List[int]],
        None,
    ]

    GetPartnerStrIdIfExists: Symbol[
        Optional[List[int]],
        None,
    ]

    GetFirstTeamMemberStrIdIfExists: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSecondTeamMemberStrIdIfExists: Symbol[
        Optional[List[int]],
        None,
    ]

    GetThirdTeamMemberStrIdIfExists: Symbol[
        Optional[List[int]],
        None,
    ]

    GetHeroData: Symbol[
        Optional[List[int]],
        None,
    ]

    GetPartnerData: Symbol[
        Optional[List[int]],
        None,
    ]

    GetFirstTeamMemberData: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSecondTeamMemberData: Symbol[
        Optional[List[int]],
        None,
    ]

    GetThirdTeamMemberData: Symbol[
        Optional[List[int]],
        None,
    ]

    GetFirstEmptyRecruitSlot: Symbol[
        Optional[List[int]],
        None,
    ]

    CheckTeamMemberField8: Symbol[
        Optional[List[int]],
        None,
    ]

    IsMonsterIdInNormalRange: Symbol[
        Optional[List[int]],
        None,
    ]

    GetTeamMemberData: Symbol[
        Optional[List[int]],
        None,
    ]

    GetTeamMember: Symbol[
        Optional[List[int]],
        None,
    ]

    SetTeamSetupHeroAndPartnerOnly: Symbol[
        Optional[List[int]],
        None,
    ]

    SetTeamSetupHeroOnly: Symbol[
        Optional[List[int]],
        None,
    ]

    GetPartyMembers: Symbol[
        Optional[List[int]],
        None,
    ]

    RefillTeam: Symbol[
        Optional[List[int]],
        None,
    ]

    ClearItem: Symbol[
        Optional[List[int]],
        None,
    ]

    ChangeGiratinaFormIfSkyDungeon: Symbol[
        Optional[List[int]],
        None,
    ]

    CanLearnIqSkill: Symbol[
        Optional[List[int]],
        None,
    ]

    GetLearnableIqSkills: Symbol[
        Optional[List[int]],
        None,
    ]

    DisableIqSkill: Symbol[
        Optional[List[int]],
        None,
    ]

    EnableIqSkill: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSpeciesIqSkill: Symbol[
        Optional[List[int]],
        None,
    ]

    IqSkillFlagTest: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNextIqSkill: Symbol[
        Optional[List[int]],
        None,
    ]

    GetExplorerMazeMonster: Symbol[
        Optional[List[int]],
        None,
    ]

    WriteMonsterInfoToSave: Symbol[
        Optional[List[int]],
        None,
    ]

    ReadMonsterInfoFromSave: Symbol[
        Optional[List[int]],
        None,
    ]

    WriteMonsterToSave: Symbol[
        Optional[List[int]],
        None,
    ]

    ReadMonsterFromSave: Symbol[
        Optional[List[int]],
        None,
    ]

    GetEvolutionPossibilities: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMonsterEvoStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSosMailCount: Symbol[
        Optional[List[int]],
        None,
    ]

    IsMissionValid: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateMission: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateDailyMissions: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonRequestsDone: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonRequestsDoneWrapper: Symbol[
        Optional[List[int]],
        None,
    ]

    AnyDungeonRequestsDone: Symbol[
        Optional[List[int]],
        None,
    ]

    GetAcceptedMission: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMissionByTypeAndDungeon: Symbol[
        Optional[List[int]],
        None,
    ]

    CheckAcceptedMissionByTypeAndDungeon: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateAllPossibleMonstersList: Symbol[
        Optional[List[int]],
        None,
    ]

    DeleteAllPossibleMonstersList: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateAllPossibleDungeonsList: Symbol[
        Optional[List[int]],
        None,
    ]

    DeleteAllPossibleDungeonsList: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateAllPossibleDeliverList: Symbol[
        Optional[List[int]],
        None,
    ]

    DeleteAllPossibleDeliverList: Symbol[
        Optional[List[int]],
        None,
    ]

    ClearMissionData: Symbol[
        Optional[List[int]],
        None,
    ]

    IsMonsterMissionAllowed: Symbol[
        Optional[List[int]],
        None,
    ]

    CanMonsterBeUsedForMissionWrapper: Symbol[
        Optional[List[int]],
        None,
    ]

    CanMonsterBeUsedForMission: Symbol[
        Optional[List[int]],
        None,
    ]

    IsMonsterMissionAllowedStory: Symbol[
        Optional[List[int]],
        None,
    ]

    CanSendItem: Symbol[
        Optional[List[int]],
        None,
    ]

    IsAvailableItem: Symbol[
        Optional[List[int]],
        None,
    ]

    GetAvailableItemDeliveryList: Symbol[
        Optional[List[int]],
        None,
    ]

    GetActorMatchingStorageId: Symbol[
        Optional[List[int]],
        None,
    ]

    ScriptSpecialProcess0x3D: Symbol[
        Optional[List[int]],
        None,
    ]

    ScriptSpecialProcess0x3E: Symbol[
        Optional[List[int]],
        None,
    ]

    ScriptSpecialProcess0x17: Symbol[
        Optional[List[int]],
        None,
    ]

    ItemAtTableIdx: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonSwapIdToIdx: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonSwapIdxToId: Symbol[
        Optional[List[int]],
        None,
    ]

    ResumeBgm: Symbol[
        Optional[List[int]],
        None,
    ]

    FlushChannels: Symbol[
        Optional[List[int]],
        None,
    ]

    UpdateChannels: Symbol[
        Optional[List[int]],
        None,
    ]

    WaitForInterrupt: Symbol[
        Optional[List[int]],
        None,
    ]

    FileInit: Symbol[
        Optional[List[int]],
        None,
    ]

    Abs: Symbol[
        Optional[List[int]],
        None,
    ]

    Mbtowc: Symbol[
        Optional[List[int]],
        None,
    ]

    TryAssignByte: Symbol[
        Optional[List[int]],
        None,
    ]

    TryAssignByteWrapper: Symbol[
        Optional[List[int]],
        None,
    ]

    Wcstombs: Symbol[
        Optional[List[int]],
        None,
    ]

    Memcpy: Symbol[
        Optional[List[int]],
        None,
    ]

    Memmove: Symbol[
        Optional[List[int]],
        None,
    ]

    Memset: Symbol[
        Optional[List[int]],
        None,
    ]

    Memchr: Symbol[
        Optional[List[int]],
        None,
    ]

    Memcmp: Symbol[
        Optional[List[int]],
        None,
    ]

    MemsetInternal: Symbol[
        Optional[List[int]],
        None,
    ]

    VsprintfInternalSlice: Symbol[
        Optional[List[int]],
        None,
    ]

    TryAppendToSlice: Symbol[
        Optional[List[int]],
        None,
    ]

    VsprintfInternal: Symbol[
        Optional[List[int]],
        None,
    ]

    Vsprintf: Symbol[
        Optional[List[int]],
        None,
    ]

    Snprintf: Symbol[
        Optional[List[int]],
        None,
    ]

    Sprintf: Symbol[
        Optional[List[int]],
        None,
    ]

    Strlen: Symbol[
        Optional[List[int]],
        None,
    ]

    Strcpy: Symbol[
        Optional[List[int]],
        None,
    ]

    Strncpy: Symbol[
        Optional[List[int]],
        None,
    ]

    Strcat: Symbol[
        Optional[List[int]],
        None,
    ]

    Strncat: Symbol[
        Optional[List[int]],
        None,
    ]

    Strcmp: Symbol[
        Optional[List[int]],
        None,
    ]

    Strncmp: Symbol[
        Optional[List[int]],
        None,
    ]

    Strchr: Symbol[
        Optional[List[int]],
        None,
    ]

    Strcspn: Symbol[
        Optional[List[int]],
        None,
    ]

    Strstr: Symbol[
        Optional[List[int]],
        None,
    ]

    Wcslen: Symbol[
        Optional[List[int]],
        None,
    ]

    AddFloat: Symbol[
        Optional[List[int]],
        None,
    ]

    DivideFloat: Symbol[
        Optional[List[int]],
        None,
    ]

    FloatToDouble: Symbol[
        Optional[List[int]],
        None,
    ]

    FloatToInt: Symbol[
        Optional[List[int]],
        None,
    ]

    IntToFloat: Symbol[
        Optional[List[int]],
        None,
    ]

    UIntToFloat: Symbol[
        Optional[List[int]],
        None,
    ]

    MultiplyFloat: Symbol[
        Optional[List[int]],
        None,
    ]

    Sqrtf: Symbol[
        Optional[List[int]],
        None,
    ]

    SubtractFloat: Symbol[
        Optional[List[int]],
        None,
    ]

    DivideInt: Symbol[
        Optional[List[int]],
        None,
    ]

    DivideUInt: Symbol[
        Optional[List[int]],
        None,
    ]

    DivideUIntNoZeroCheck: Symbol[
        Optional[List[int]],
        None,
    ]


class Arm9DataProtocol(Protocol):
    ARM9_HEADER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SDK_STRINGS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DEFAULT_MEMORY_ARENA_SIZE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    LOG_MAX_ARG: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAMAGE_SOURCE_CODE_ORB_ITEM: Symbol[
        Optional[List[int]],
        None,
    ]

    DAMAGE_SOURCE_CODE_NON_ORB_ITEM: Symbol[
        Optional[List[int]],
        None,
    ]

    AURA_BOW_ID_LAST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    NUMBER_OF_ITEMS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MAX_MONEY_CARRIED: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MAX_MONEY_STORED: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DIALOG_BOX_LIST_PTR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SCRIPT_VARS_VALUES_PTR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MONSTER_ID_LIMIT: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MAX_RECRUITABLE_TEAM_MEMBERS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    NATURAL_LOG_VALUE_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    CART_REMOVED_IMG_DATA: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    AVAILABLE_ITEMS_IN_GROUP_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ARM9_UNKNOWN_TABLE__NA_2097FF8: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    KECLEON_SHOP_ITEM_TABLE_LISTS_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    KECLEON_SHOP_ITEM_TABLE_LISTS_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EXCLUSIVE_ITEM_STAT_BOOST_DATA: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EXCLUSIVE_ITEM_ATTACK_BOOSTS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EXCLUSIVE_ITEM_SPECIAL_ATTACK_BOOSTS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EXCLUSIVE_ITEM_DEFENSE_BOOSTS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EXCLUSIVE_ITEM_SPECIAL_DEFENSE_BOOSTS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EXCLUSIVE_ITEM_EFFECT_DATA: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EXCLUSIVE_ITEM_STAT_BOOST_DATA_INDEXES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECYCLE_SHOP_ITEM_LIST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TYPE_SPECIFIC_EXCLUSIVE_ITEMS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECOIL_MOVE_LIST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    PUNCH_MOVE_LIST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MOVE_POWER_STARS_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MOVE_ACCURACY_STARS_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    PARTNER_TALK_KIND_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SCRIPT_VARS_LOCALS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SCRIPT_VARS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    HARDCODED_PORTRAIT_DATA_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    WONDER_MAIL_BITS_MAP: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    WONDER_MAIL_BITS_SWAP: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ARM9_UNKNOWN_TABLE__NA_209E12C: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ARM9_UNKNOWN_TABLE__NA_209E164: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ARM9_UNKNOWN_TABLE__NA_209E280: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    WONDER_MAIL_ENCRYPTION_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_DATA_LIST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ADVENTURE_LOG_ENCOUNTERS_MONSTER_IDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ARM9_UNKNOWN_DATA__NA_209E6BC: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TACTIC_NAME_STRING_IDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STATUS_NAME_STRING_IDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_RETURN_STATUS_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STATUSES_FULL_DESCRIPTION_STRING_IDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ARM9_UNKNOWN_DATA__NA_209EAAC: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MISSION_FLOOR_RANKS_AND_ITEM_LISTS_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MISSION_FLOORS_FORBIDDEN: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MISSION_FLOOR_RANKS_AND_ITEM_LISTS_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MISSION_FLOOR_RANKS_PTRS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_RESTRICTIONS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SPECIAL_BAND_STAT_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MUNCH_BELT_STAT_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    GUMMI_STAT_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MIN_IQ_EXCLUSIVE_MOVE_USER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    WONDER_GUMMI_IQ_GAIN: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    AURA_BOW_STAT_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MIN_IQ_ITEM_MASTER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DEF_SCARF_STAT_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    POWER_BAND_STAT_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    WONDER_GUMMI_STAT_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ZINC_BAND_STAT_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EGG_HP_BONUS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EVOLUTION_HP_BONUS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAMAGE_FORMULA_FLV_SHIFT: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EVOLUTION_PHYSICAL_STAT_BONUSES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAMAGE_FORMULA_CONSTANT_SHIFT: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAMAGE_FORMULA_FLV_DEFICIT_DIVISOR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EGG_STAT_BONUSES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EVOLUTION_SPECIAL_STAT_BONUSES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAMAGE_FORMULA_NON_TEAM_MEMBER_MODIFIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAMAGE_FORMULA_LN_PREFACTOR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAMAGE_FORMULA_AT_PREFACTOR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAMAGE_FORMULA_DEF_PREFACTOR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAMAGE_FORMULA_LN_ARG_PREFACTOR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FORBIDDEN_FORGOT_MOVE_LIST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TACTICS_UNLOCK_LEVEL_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    CLIENT_LEVEL_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OUTLAW_LEVEL_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OUTLAW_MINION_LEVEL_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    HIDDEN_POWER_BASE_POWER_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    VERSION_EXCLUSIVE_MONSTERS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    IQ_SKILL_RESTRICTIONS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SECONDARY_TERRAIN_TYPES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SENTRY_DUTY_MONSTER_IDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    IQ_SKILLS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    IQ_GROUP_SKILLS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MONEY_QUANTITY_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ARM9_UNKNOWN_TABLE__NA_20A20B0: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    IQ_GUMMI_GAIN_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    GUMMI_BELLY_RESTORE_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BAG_CAPACITY_TABLE_SPECIAL_EPISODES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BAG_CAPACITY_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SPECIAL_EPISODE_MAIN_CHARACTERS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    GUEST_MONSTER_DATA: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RANK_UP_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DS_DOWNLOAD_TEAMS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ARM9_UNKNOWN_PTR__NA_20A2C84: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    UNOWN_SPECIES_ADDITIONAL_CHARS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MONSTER_SPRITE_DATA: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    REMOTE_STRINGS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RANK_STRINGS_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MISSION_MENU_STRING_IDS_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RANK_STRINGS_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MISSION_MENU_STRING_IDS_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RANK_STRINGS_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MISSION_DUNGEON_UNLOCK_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    NO_SEND_ITEM_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ARM9_UNKNOWN_TABLE__NA_20A3CC8: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ARM9_UNKNOWN_TABLE__NA_20A3CE4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ARM9_UNKNOWN_FUNCTION_TABLE__NA_20A3CF4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MISSION_BANNED_STORY_MONSTERS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ITEM_DELIVERY_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MISSION_RANK_POINTS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MISSION_BANNED_MONSTERS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MISSION_STRING_IDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    LEVEL_LIST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EVENTS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ARM9_UNKNOWN_TABLE__NA_20A68BC: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DEMO_TEAMS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ACTOR_LIST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ENTITIES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    JOB_D_BOX_LAYOUT_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    JOB_MENU_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    JOB_MENU_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    JOB_MENU_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    JOB_MENU_4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    JOB_MENU_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    JOB_MENU_6: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    JOB_MENU_7: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    JOB_MENU_8: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    JOB_MENU_9: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    JOB_MENU_10: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    JOB_MENU_11: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    JOB_MENU_12: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    JOB_MENU_13: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    JOB_D_BOX_LAYOUT_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_SWAP_ID_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MAP_MARKER_PLACEMENTS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ARM9_UNKNOWN_TABLE__NA_20A9FB0: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ARM9_UNKNOWN_TABLE__NA_20AE924: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MEMORY_ALLOCATION_ARENA_GETTERS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    PRNG_SEQUENCE_NUM: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    LOADED_OVERLAY_GROUP_0: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    LOADED_OVERLAY_GROUP_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    LOADED_OVERLAY_GROUP_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    PACK_FILE_OPENED: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    PACK_FILE_PATHS_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    GAME_STATE_VALUES: Symbol[
        Optional[List[int]],
        None,
    ]

    BAG_ITEMS_PTR_MIRROR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ITEM_DATA_TABLE_PTRS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_MOVE_TABLES: Symbol[
        Optional[List[int]],
        None,
    ]

    MOVE_DATA_TABLE_PTR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    LOADED_WAN_TABLE_PTR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    LANGUAGE_INFO_DATA: Symbol[
        Optional[List[int]],
        None,
    ]

    TBL_TALK_GROUP_STRING_ID_START: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    KEYBOARD_STRING_IDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    NOTIFY_NOTE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DEFAULT_HERO_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DEFAULT_PARTNER_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    GAME_MODE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    GLOBAL_PROGRESS_PTR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ADVENTURE_LOG_PTR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ITEM_TABLES_PTRS_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    UNOWN_SPECIES_ADDITIONAL_CHAR_PTR_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    PARTY_MONSTERS_PTR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MISSION_LIST_PTR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    REMOTE_STRING_PTR_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RANK_STRING_PTR_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SMD_EVENTS_FUN_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MUSIC_DURATION_LOOKUP_TABLE_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MUSIC_DURATION_LOOKUP_TABLE_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    JUICE_BAR_NECTAR_IQ_GAIN: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TEXT_SPEED: Symbol[
        Optional[List[int]],
        None,
    ]

    HERO_START_LEVEL: Symbol[
        Optional[List[int]],
        None,
    ]

    PARTNER_START_LEVEL: Symbol[
        Optional[List[int]],
        None,
    ]


Arm9Protocol = SectionProtocol[
    Arm9FunctionsProtocol,
    Arm9DataProtocol,
    int,
]


class ItcmFunctionsProtocol(Protocol):
    GetKeyN2MSwitch: Symbol[
        List[int],
        None,
    ]

    GetKeyN2M: Symbol[
        List[int],
        None,
    ]

    GetKeyN2MBaseForm: Symbol[
        List[int],
        None,
    ]

    GetKeyM2NSwitch: Symbol[
        List[int],
        None,
    ]

    GetKeyM2N: Symbol[
        List[int],
        None,
    ]

    GetKeyM2NBaseForm: Symbol[
        List[int],
        None,
    ]

    ShouldMonsterRunAwayVariationOutlawCheck: Symbol[
        List[int],
        None,
    ]

    AiMovement: Symbol[
        List[int],
        None,
    ]

    CalculateAiTargetPos: Symbol[
        List[int],
        None,
    ]

    ChooseAiMove: Symbol[
        List[int],
        None,
    ]

    LightningRodStormDrainCheck: Symbol[
        Optional[List[int]],
        None,
    ]


class ItcmDataProtocol(Protocol):
    MEMORY_ALLOCATION_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DEFAULT_MEMORY_ARENA: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DEFAULT_MEMORY_ARENA_BLOCKS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


ItcmProtocol = SectionProtocol[
    ItcmFunctionsProtocol,
    ItcmDataProtocol,
    int,
]


class Move_effectsFunctionsProtocol(Protocol):
    DoMoveDamage: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveIronTail: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageMultihitUntilMiss: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveYawn: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSleep: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveNightmare: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveMorningSun: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveVitalThrow: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDig: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSweetScent: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveCharm: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveRainDance: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveHail: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveHealStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveBubble: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveEncore: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveRage: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSuperFang: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMovePainSplit: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTorment: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveStringShot: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSwagger: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSnore: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveScreech: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageCringe30: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveWeatherBall: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveWhirlpool: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveFakeTears: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSpite: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveFocusEnergy: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSmokescreen: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveMirrorMove: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveOverheat: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveAuroraBeam: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveMemento: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveOctazooka: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveFlatter: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveWillOWisp: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveReturn: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveGrudge: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveCounter: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageBurn10FlameWheel: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageBurn10: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveExpose: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDoubleTeam: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveGust: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveBoostDefense1: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveParalyze: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveBoostAttack1: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveRazorWind: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveBide: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveBideUnleash: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveCrunch: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageCringe20: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageParalyze20: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveEndeavor: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveFacade: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageLowerSpeed20: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveBrickBreak: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageLowerSpeed100: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveFocusPunch: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageDrain: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveReversal: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSmellingSalt: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveMetalSound: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTickle: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveShadowHold: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveHaze: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageMultihitFatigue: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageWeightDependent: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageBoostAllStats: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSynthesis: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveBoostSpeed1: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveRapidSpin: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSureShot: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveCosmicPower: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSkyAttack: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageFreeze15: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveMeteorMash: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveEndure: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveLowerSpeed1: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageConfuse10: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMovePsywave: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageLowerDefensiveStatVariable: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMovePsychoBoost: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveUproar: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveWaterSpout: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMovePsychUp: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageWithRecoil: Symbol[
        Optional[List[int]],
        None,
    ]

    EntityIsValidMoveEffects: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveRecoverHp: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveEarthquake: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNaturePowerVariant: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveNaturePower: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageParalyze10: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSelfdestruct: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveShadowBall: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveCharge: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveThunderbolt: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveMist: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveFissure: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageCringe10: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSafeguard: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveAbsorb: Symbol[
        Optional[List[int]],
        None,
    ]

    DefenderAbilityIsActiveMoveEffects: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSkillSwap: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSketch: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveHeadbutt: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDoubleEdge: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSandstorm: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveLowerAccuracy1: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamagePoison40: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveGrowth: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSacredFire: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveOhko: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSolarBeam: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSonicBoom: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveFly: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveExplosion: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDive: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveWaterfall: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageLowerAccuracy40: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveStockpile: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTwister: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTwineedle: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveRecoverHpTeam: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveMinimize: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSeismicToss: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveConfuse: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTaunt: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveMoonlight: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveHornDrill: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSwordsDance: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveConversion: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveConversion2: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveHelpingHand: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveBoostDefense2: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveWarp: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveThundershock: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveThunderWave: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveZapCannon: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveBlock: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMovePoison: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveToxic: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMovePoisonFang: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamagePoison18: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveJumpKick: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveBounce: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveHiJumpKick: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTriAttack: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSwapItems: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTripleKick: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSport: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveMudSlap: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageStealItem: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveAmnesia: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveNightShade: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveGrowl: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSurf: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveRolePlay: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSunnyDay: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveLowerDefense1: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveWish: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveFakeOut: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSleepTalk: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMovePayDay: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveAssist: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveRest: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveIngrain: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSwallow: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveCurse: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSuperpower: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSteelWing: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSpitUp: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDynamicPunch: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveKnockOff: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSplash: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSetDamage: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveBellyDrum: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveLightScreen: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSecretPower: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageConfuse30: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveBulkUp: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMovePause: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveFeatherDance: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveBeatUp: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveBlastBurn: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveCrushClaw: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveBlazeKick: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMovePresent: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveEruption: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTransform: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMovePoisonTail: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveBlowback: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveCamouflage: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTailGlow: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageConstrict10: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMovePerishSong: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveWrap: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSpikes: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveMagnitude: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveMagicCoat: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveProtect: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDefenseCurl: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDecoy: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveMistBall: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDestinyBond: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveMirrorCoat: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveCalmMind: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveHiddenPower: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveMetalClaw: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveAttract: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveCopycat: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveFrustration: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveLeechSeed: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveMetronome: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDreamEater: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSnatch: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveRecycle: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveReflect: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDragonRage: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDragonDance: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSkullBash: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageLowerSpecialDefense50: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveStruggle: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveRockSmash: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSeeTrap: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTakeaway: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveRebound: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSwitchPositions: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveStayAway: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveCleanse: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSiesta: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTwoEdge: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveNoMove: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveScan: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMovePowerEars: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTransfer: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSlowDown: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSearchlight: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMovePetrify: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMovePounce: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTrawl: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveEscape: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDrought: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTrapBuster: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveWildCall: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveInvisify: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveOneShot: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveHpGauge: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveVacuumCut: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveReviver: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveShocker: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveEcho: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveFamish: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveOneRoom: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveFillIn: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTrapper: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveItemize: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveHurl: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveMobile: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveSeeStairs: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveLongToss: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMovePierce: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveHammerArm: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveAquaRing: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveGastroAcid: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveHealingWish: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveCloseCombat: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveLuckyChant: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveGuardSwap: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveHealOrder: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveHealBlock: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveThunderFang: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDefog: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTrumpCard: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveIceFang: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMovePsychoShift: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveEmbargo: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveBrine: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveNaturalGift: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveGyroBall: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveShadowForce: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveGravity: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveStealthRock: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveChargeBeam: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageEatItem: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveAcupressure: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveMagnetRise: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveToxicSpikes: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveLastResort: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTrickRoom: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveWorrySeed: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageHpDependent: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveHeartSwap: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveRoost: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMovePowerSwap: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMovePowerTrick: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveFeint: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveFlareBlitz: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDefendOrder: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveFireFang: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveLunarDance: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveMiracleEye: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveWakeUpSlap: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveMetalBurst: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveHeadSmash: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveCaptivate: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveLeafStorm: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDracoMeteor: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveRockPolish: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveNastyPlot: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTag0x1AB: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTag0x1A6: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveTag0x1A7: Symbol[
        Optional[List[int]],
        None,
    ]


class Move_effectsDataProtocol(Protocol):
    MAX_HP_CAP_MOVE_EFFECTS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    LUNAR_DANCE_PP_RESTORATION: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Move_effectsProtocol = SectionProtocol[
    Move_effectsFunctionsProtocol,
    Move_effectsDataProtocol,
    Optional[int],
]


class Overlay0FunctionsProtocol(Protocol):
    pass


class Overlay0DataProtocol(Protocol):
    TOP_MENU_MUSIC_ID: Symbol[
        Optional[List[int]],
        None,
    ]


Overlay0Protocol = SectionProtocol[
    Overlay0FunctionsProtocol,
    Overlay0DataProtocol,
    Optional[int],
]


class Overlay1FunctionsProtocol(Protocol):
    CreateMainMenus: Symbol[
        Optional[List[int]],
        None,
    ]

    AddMainMenuOption: Symbol[
        Optional[List[int]],
        None,
    ]

    AddSubMenuOption: Symbol[
        Optional[List[int]],
        None,
    ]


class Overlay1DataProtocol(Protocol):
    PRINTS_STRINGS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    PRINTS_STRUCT: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY1_D_BOX_LAYOUT_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY1_D_BOX_LAYOUT_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY1_D_BOX_LAYOUT_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY1_D_BOX_LAYOUT_4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    CONTINUE_CHOICE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SUBMENU: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MAIN_MENU: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY1_D_BOX_LAYOUT_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY1_D_BOX_LAYOUT_6: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY1_D_BOX_LAYOUT_7: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MAIN_MENU_CONFIRM: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY1_D_BOX_LAYOUT_8: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY1_D_BOX_LAYOUT_9: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MAIN_DEBUG_MENU_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY1_D_BOX_LAYOUT_10: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MAIN_DEBUG_MENU_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay1Protocol = SectionProtocol[
    Overlay1FunctionsProtocol,
    Overlay1DataProtocol,
    Optional[int],
]


class Overlay10FunctionsProtocol(Protocol):
    SprintfStatic: Symbol[
        Optional[List[int]],
        None,
    ]

    GetEffectAnimationField0x19: Symbol[
        Optional[List[int]],
        None,
    ]

    AnimationHasMoreFrames: Symbol[
        Optional[List[int]],
        None,
    ]

    GetEffectAnimation: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveAnimation: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSpecialMonsterMoveAnimation: Symbol[
        Optional[List[int]],
        None,
    ]

    GetTrapAnimation: Symbol[
        Optional[List[int]],
        None,
    ]

    GetItemAnimation1: Symbol[
        Optional[List[int]],
        None,
    ]

    GetItemAnimation2: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveAnimationSpeed: Symbol[
        Optional[List[int]],
        None,
    ]

    CheckEndDungeon: Symbol[
        Optional[List[int]],
        None,
    ]


class Overlay10DataProtocol(Protocol):
    FIRST_DUNGEON_WITH_MONSTER_HOUSE_TRAPS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BAD_POISON_DAMAGE_COOLDOWN: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    PROTEIN_STAT_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    WATERFALL_CRINGE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    AURORA_BEAM_LOWER_ATTACK_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SPAWN_CAP_NO_MONSTER_HOUSE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OREN_BERRY_DAMAGE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    IRON_TAIL_LOWER_DEFENSE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TWINEEDLE_POISON_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EXTRASENSORY_CRINGE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ROCK_SLIDE_CRINGE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    CRUNCH_LOWER_DEFENSE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FOREWARN_FORCED_MISS_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    UNOWN_STONE_DROP_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SITRUS_BERRY_HP_RESTORATION: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MUDDY_WATER_LOWER_ACCURACY_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SILVER_WIND_BOOST_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    POISON_TAIL_POISON_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    THUNDERSHOCK_PARALYZE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BOUNCE_PARALYZE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    HEADBUTT_CRINGE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FIRE_FANG_CRINGE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SACRED_FIRE_BURN_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    WHIRLPOOL_CONSTRICTION_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EXP_ELITE_EXP_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MONSTER_HOUSE_MAX_NON_MONSTER_SPAWNS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    HEAL_ORDER_HP_RESTORATION: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STEEL_WING_BOOST_DEFENSE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    GOLD_THORN_POWER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SPAWN_COOLDOWN: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MIST_BALL_LOWER_SPECIAL_ATTACK_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    CHARGE_BEAM_BOOST_SPECIAL_ATTACK_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ORAN_BERRY_FULL_HP_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    LIFE_SEED_HP_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OCTAZOOKA_LOWER_ACCURACY_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    LUSTER_PURGE_LOWER_SPECIAL_DEFENSE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SUPER_LUCK_CRIT_RATE_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    CONSTRICT_LOWER_SPEED_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ICE_FANG_FREEZE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SMOG_POISON_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    LICK_PARALYZE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    THUNDER_FANG_PARALYZE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BITE_CRINGE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SKY_ATTACK_CRINGE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ICE_FANG_CRINGE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BLAZE_KICK_BURN_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FLAMETHROWER_BURN_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DIZZY_PUNCH_CONFUSE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SECRET_POWER_EFFECT_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    METAL_CLAW_BOOST_ATTACK_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TECHNICIAN_MOVE_POWER_THRESHOLD: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SONICBOOM_FIXED_DAMAGE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EXCLUSIVE_ITEM_EXP_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    AFTERMATH_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SET_DAMAGE_STATUS_DAMAGE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    INTIMIDATOR_ACTIVATION_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TYPE_ADVANTAGE_MASTER_CRIT_RATE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ORAN_BERRY_HP_RESTORATION: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SITRUS_BERRY_FULL_HP_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SNORE_CRINGE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    METEOR_MASH_BOOST_ATTACK_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    CRUSH_CLAW_LOWER_DEFENSE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BURN_DAMAGE_COOLDOWN: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SHADOW_BALL_LOWER_SPECIAL_DEFENSE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STICK_POWER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BUBBLE_LOWER_SPEED_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    POWDER_SNOW_FREEZE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    POISON_STING_POISON_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SPAWN_COOLDOWN_THIEF_ALERT: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    POISON_FANG_POISON_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    THUNDER_PARALYZE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    THUNDERBOLT_PARALYZE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MONSTER_HOUSE_MAX_MONSTER_SPAWNS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TWISTER_CRINGE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SPEED_BOOST_TURNS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FAKE_OUT_CRINGE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    THUNDER_FANG_CRINGE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FLARE_BLITZ_BURN_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FLAME_WHEEL_BURN_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    PSYBEAM_CONFUSE_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TRI_ATTACK_STATUS_CHANCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MIRACLE_CHEST_EXP_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    WONDER_CHEST_EXP_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SPAWN_CAP_WITH_MONSTER_HOUSE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    POISON_DAMAGE_COOLDOWN: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    GEO_PEBBLE_DAMAGE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    GRAVELEROCK_DAMAGE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RARE_FOSSIL_DAMAGE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    GINSENG_CHANCE_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ZINC_STAT_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    IRON_STAT_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    CALCIUM_STAT_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DRAGON_RAGE_FIXED_DAMAGE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    CORSOLA_TWIG_POWER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    CACNEA_SPIKE_POWER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    GOLD_FANG_POWER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SILVER_SPIKE_POWER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    IRON_THORN_POWER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SCOPE_LENS_CRIT_RATE_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    HEALING_WISH_HP_RESTORATION: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MONSTER_BOOSTED_ATTACKS_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FACADE_DAMAGE_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    IMPRISON_TURN_RANGE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SLEEP_TURN_RANGE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    NIGHTMARE_TURN_RANGE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BURN_DAMAGE_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    REST_TURN_RANGE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MATCHUP_SUPER_EFFECTIVE_MULTIPLIER_ERRATIC_PLAYER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MATCHUP_IMMUNE_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SPORT_CONDITION_TURN_RANGE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SURE_SHOT_TURN_RANGE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DETECT_BAND_MOVE_ACCURACY_DROP: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TINTED_LENS_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SMOKESCREEN_TURN_RANGE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SHADOW_FORCE_DAMAGE_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DIG_DAMAGE_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DIVE_DAMAGE_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BOUNCE_DAMAGE_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    POWER_PITCHER_DAMAGE_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    QUICK_DODGER_MOVE_ACCURACY_DROP: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MATCHUP_NOT_VERY_EFFECTIVE_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MATCHUP_SUPER_EFFECTIVE_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MATCHUP_NEUTRAL_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MATCHUP_IMMUNE_MULTIPLIER_ERRATIC_PLAYER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MATCHUP_NOT_VERY_EFFECTIVE_MULTIPLIER_ERRATIC_PLAYER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MATCHUP_NEUTRAL_MULTIPLIER_ERRATIC_PLAYER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    AIR_BLADE_DAMAGE_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    HIDDEN_STAIRS_SPAWN_CHANCE_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    YAWN_TURN_RANGE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SPEED_BOOST_TURN_RANGE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SOLARBEAM_DAMAGE_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SKY_ATTACK_DAMAGE_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RAZOR_WIND_DAMAGE_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FOCUS_PUNCH_DAMAGE_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SKULL_BASH_DAMAGE_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FLY_DAMAGE_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    WEATHER_BALL_TYPE_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    LAST_RESORT_DAMAGE_MULT_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SYNTHESIS_HP_RESTORATION_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ROOST_HP_RESTORATION_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MOONLIGHT_HP_RESTORATION_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MORNING_SUN_HP_RESTORATION_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    REVERSAL_DAMAGE_MULT_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    WATER_SPOUT_DAMAGE_MULT_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    WRING_OUT_DAMAGE_MULT_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ERUPTION_DAMAGE_MULT_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    WEATHER_BALL_DAMAGE_MULT_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    CASTFORM_WEATHER_ATTRIBUTE_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TYPE_MATCHUP_COMBINATOR_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OFFENSIVE_STAT_STAGE_MULTIPLIERS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DEFENSIVE_STAT_STAGE_MULTIPLIERS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    NATURE_POWER_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    APPLES_AND_BERRIES_ITEM_IDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECRUITMENT_LEVEL_BOOST_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    NATURAL_GIFT_ITEM_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RANDOM_MUSIC_ID_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SHOP_ITEM_CHANCES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MALE_ACCURACY_STAGE_MULTIPLIERS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MALE_EVASION_STAGE_MULTIPLIERS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FEMALE_ACCURACY_STAGE_MULTIPLIERS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FEMALE_EVASION_STAGE_MULTIPLIERS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MUSIC_ID_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TYPE_MATCHUP_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FIXED_ROOM_MONSTER_SPAWN_STATS_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    METRONOME_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TILESET_PROPERTIES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FIXED_ROOM_PROPERTIES_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TRAP_ANIMATION_INFO: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ITEM_ANIMATION_INFO: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MOVE_ANIMATION_INFO: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EFFECT_ANIMATION_INFO: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SPECIAL_MONSTER_MOVE_ANIMATION_INFO: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay10Protocol = SectionProtocol[
    Overlay10FunctionsProtocol,
    Overlay10DataProtocol,
    Optional[int],
]


class Overlay11FunctionsProtocol(Protocol):
    FuncThatCallsCommandParsing: Symbol[
        Optional[List[int]],
        None,
    ]

    ScriptCommandParsing: Symbol[
        Optional[List[int]],
        None,
    ]

    SsbLoad2: Symbol[
        Optional[List[int]],
        None,
    ]

    StationLoadHanger: Symbol[
        Optional[List[int]],
        None,
    ]

    ScriptStationLoadTalk: Symbol[
        Optional[List[int]],
        None,
    ]

    SsbLoad1: Symbol[
        Optional[List[int]],
        None,
    ]

    ScriptSpecialProcessCall: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSpecialRecruitmentSpecies: Symbol[
        Optional[List[int]],
        None,
    ]

    PrepareMenuAcceptTeamMember: Symbol[
        Optional[List[int]],
        None,
    ]

    InitRandomNpcJobs: Symbol[
        Optional[List[int]],
        None,
    ]

    GetRandomNpcJobType: Symbol[
        Optional[List[int]],
        None,
    ]

    GetRandomNpcJobSubtype: Symbol[
        Optional[List[int]],
        None,
    ]

    GetRandomNpcJobStillAvailable: Symbol[
        Optional[List[int]],
        None,
    ]

    AcceptRandomNpcJob: Symbol[
        Optional[List[int]],
        None,
    ]

    GroundMainLoop: Symbol[
        Optional[List[int]],
        None,
    ]

    GetAllocArenaGround: Symbol[
        Optional[List[int]],
        None,
    ]

    GetFreeArenaGround: Symbol[
        Optional[List[int]],
        None,
    ]

    GroundMainReturnDungeon: Symbol[
        Optional[List[int]],
        None,
    ]

    GroundMainNextDay: Symbol[
        Optional[List[int]],
        None,
    ]

    JumpToTitleScreen: Symbol[
        Optional[List[int]],
        None,
    ]

    ReturnToTitleScreen: Symbol[
        Optional[List[int]],
        None,
    ]

    ScriptSpecialProcess0x16: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadBackgroundAttributes: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadMapType10: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadMapType11: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSpecialLayoutBackground: Symbol[
        Optional[List[int]],
        None,
    ]

    SetAnimDataFields: Symbol[
        Optional[List[int]],
        None,
    ]

    SetAnimDataFieldsWrapper: Symbol[
        Optional[List[int]],
        None,
    ]

    InitAnimDataFromOtherAnimData: Symbol[
        Optional[List[int]],
        None,
    ]

    SetAnimDataFields2: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadObjectAnimData: Symbol[
        Optional[List[int]],
        None,
    ]

    InitAnimDataFromOtherAnimDataVeneer: Symbol[
        Optional[List[int]],
        None,
    ]

    AnimRelatedFunction: Symbol[
        Optional[List[int]],
        None,
    ]

    SprintfStatic: Symbol[
        Optional[List[int]],
        None,
    ]

    StatusUpdate: Symbol[
        Optional[List[int]],
        None,
    ]


class Overlay11DataProtocol(Protocol):
    OVERLAY11_UNKNOWN_TABLE__NA_2316A38: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SCRIPT_COMMAND_PARSING_DATA: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SCRIPT_OP_CODE_NAMES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SCRIPT_OP_CODES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY11_DEBUG_STRINGS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    C_ROUTINE_NAMES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    C_ROUTINES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    GROUND_WEATHER_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    GROUND_WAN_FILES_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OBJECTS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECRUITMENT_TABLE_LOCATIONS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECRUITMENT_TABLE_LEVELS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECRUITMENT_TABLE_SPECIES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    LEVEL_TILEMAP_LIST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY11_OVERLAY_LOAD_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    UNIONALL_RAM_ADDRESS: Symbol[
        Optional[List[int]],
        None,
    ]

    GROUND_STATE_MAP: Symbol[
        Optional[List[int]],
        None,
    ]

    GROUND_STATE_PTRS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay11Protocol = SectionProtocol[
    Overlay11FunctionsProtocol,
    Overlay11DataProtocol,
    Optional[int],
]


class Overlay12FunctionsProtocol(Protocol):
    pass


class Overlay12DataProtocol(Protocol):
    pass


Overlay12Protocol = SectionProtocol[
    Overlay12FunctionsProtocol,
    Overlay12DataProtocol,
    Optional[int],
]


class Overlay13FunctionsProtocol(Protocol):
    EntryOverlay13: Symbol[
        Optional[List[int]],
        None,
    ]

    ExitOverlay13: Symbol[
        Optional[List[int]],
        None,
    ]

    Overlay13SwitchFunctionNa238A1C8: Symbol[
        Optional[List[int]],
        None,
    ]

    Overlay13SwitchFunctionNa238A574: Symbol[
        Optional[List[int]],
        None,
    ]

    GetPersonality: Symbol[
        Optional[List[int]],
        None,
    ]

    GetOptionStringFromID: Symbol[
        Optional[List[int]],
        None,
    ]

    WaitForNextStep: Symbol[
        Optional[List[int]],
        None,
    ]


class Overlay13DataProtocol(Protocol):
    QUIZ_BORDER_COLOR_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    PORTRAIT_ATTRIBUTES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    QUIZ_MALE_FEMALE_BOOST_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY13_UNKNOWN_STRUCT__NA_238C024: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    QUIZ_D_BOX_LAYOUT_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    QUIZ_D_BOX_LAYOUT_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    QUIZ_D_BOX_LAYOUT_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    QUIZ_D_BOX_LAYOUT_4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    QUIZ_MENU_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STARTERS_PARTNER_IDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STARTERS_HERO_IDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STARTERS_TYPE_INCOMPATIBILITY_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STARTERS_STRINGS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    QUIZ_QUESTION_STRINGS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    QUIZ_ANSWER_STRINGS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    QUIZ_ANSWER_POINTS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY13_RESERVED_SPACE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY13_UNKNOWN_POINTER__NA_238CEA0: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY13_UNKNOWN_POINTER__NA_238CEA4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY13_UNKNOWN_POINTER__NA_238CEA8: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    QUIZ_D_BOX_LAYOUT_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    QUIZ_D_BOX_LAYOUT_6: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    QUIZ_DEBUG_MENU: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY13_UNKNOWN_STRUCT__NA_238CF14: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    QUIZ_QUESTION_ANSWER_ASSOCIATIONS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay13Protocol = SectionProtocol[
    Overlay13FunctionsProtocol,
    Overlay13DataProtocol,
    Optional[int],
]


class Overlay14FunctionsProtocol(Protocol):
    SentrySetupState: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryUpdateDisplay: Symbol[
        Optional[List[int]],
        None,
    ]

    SentrySetExitingState: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryRunState: Symbol[
        Optional[List[int]],
        None,
    ]

    SentrySetStateIntermediate: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState0: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState1: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState2: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState3: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState4: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryStateExit: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState6: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState7: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState8: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState9: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryStateA: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryStateB: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryStateGenerateChoices: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryStateGetUserChoice: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryStateFinalizeRound: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryStateF: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState10: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState11: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState12: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState13: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState14: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState15: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState16: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState17: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState18: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState19: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState1A: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryStateFinalizePoints: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState1C: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState1D: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState1E: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState1F: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState20: Symbol[
        Optional[List[int]],
        None,
    ]

    SentryState21: Symbol[
        Optional[List[int]],
        None,
    ]


class Overlay14DataProtocol(Protocol):
    SENTRY_DUTY_STRUCT_SIZE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SENTRY_LOUDRED_MONSTER_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STRING_ID_SENTRY_TOP_SESSIONS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STRING_ID_SENTRY_INSTRUCTIONS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STRING_ID_SENTRY_HERE_COMES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STRING_ID_SENTRY_WHOSE_FOOTPRINT: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STRING_ID_SENTRY_TRY_AGAIN: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STRING_ID_SENTRY_OUT_OF_TIME: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STRING_ID_SENTRY_FOOTPRINT_IS_6EE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STRING_ID_SENTRY_COME_IN_6EF: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STRING_ID_SENTRY_WRONG: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STRING_ID_SENTRY_BUCK_UP: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STRING_ID_SENTRY_FOOTPRINT_IS_6EC: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STRING_ID_SENTRY_COME_IN_6ED: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STRING_ID_SENTRY_KEEP_YOU_WAITING: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STRING_ID_SENTRY_THATLL_DO_IT: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SENTRY_CHATOT_MONSTER_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STRING_ID_SENTRY_NO_MORE_VISITORS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STRING_ID_SENTRY_THATS_ALL: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SENTRY_GROVYLE_MONSTER_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FOOTPRINT_DEBUG_MENU: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SENTRY_DUTY_PTR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SENTRY_DUTY_STATE_HANDLER_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay14Protocol = SectionProtocol[
    Overlay14FunctionsProtocol,
    Overlay14DataProtocol,
    Optional[int],
]


class Overlay15FunctionsProtocol(Protocol):
    pass


class Overlay15DataProtocol(Protocol):
    BANK_MAIN_MENU: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BANK_D_BOX_LAYOUT_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BANK_D_BOX_LAYOUT_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BANK_D_BOX_LAYOUT_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BANK_D_BOX_LAYOUT_4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BANK_D_BOX_LAYOUT_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY15_RESERVED_SPACE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY15_UNKNOWN_POINTER__NA_238B180: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay15Protocol = SectionProtocol[
    Overlay15FunctionsProtocol,
    Overlay15DataProtocol,
    Optional[int],
]


class Overlay16FunctionsProtocol(Protocol):
    pass


class Overlay16DataProtocol(Protocol):
    EVO_MENU_CONFIRM: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EVO_SUBMENU: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EVO_MAIN_MENU: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EVO_MENU_STRING_IDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EVO_D_BOX_LAYOUT_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EVO_D_BOX_LAYOUT_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EVO_D_BOX_LAYOUT_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EVO_D_BOX_LAYOUT_4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EVO_D_BOX_LAYOUT_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EVO_D_BOX_LAYOUT_6: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EVO_D_BOX_LAYOUT_7: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY16_RESERVED_SPACE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY16_UNKNOWN_POINTER__NA_238CE40: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY16_UNKNOWN_POINTER__NA_238CE58: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay16Protocol = SectionProtocol[
    Overlay16FunctionsProtocol,
    Overlay16DataProtocol,
    Optional[int],
]


class Overlay17FunctionsProtocol(Protocol):
    pass


class Overlay17DataProtocol(Protocol):
    ASSEMBLY_D_BOX_LAYOUT_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ASSEMBLY_D_BOX_LAYOUT_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ASSEMBLY_D_BOX_LAYOUT_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ASSEMBLY_D_BOX_LAYOUT_4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ASSEMBLY_D_BOX_LAYOUT_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ASSEMBLY_MENU_CONFIRM: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ASSEMBLY_MAIN_MENU_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ASSEMBLY_MAIN_MENU_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ASSEMBLY_SUBMENU_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ASSEMBLY_SUBMENU_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ASSEMBLY_SUBMENU_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ASSEMBLY_SUBMENU_4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ASSEMBLY_SUBMENU_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ASSEMBLY_SUBMENU_6: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ASSEMBLY_SUBMENU_7: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY17_FUNCTION_POINTER_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY17_RESERVED_SPACE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY17_UNKNOWN_POINTER__NA_238BE00: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY17_UNKNOWN_POINTER__NA_238BE04: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY17_UNKNOWN_POINTER__NA_238BE08: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay17Protocol = SectionProtocol[
    Overlay17FunctionsProtocol,
    Overlay17DataProtocol,
    Optional[int],
]


class Overlay18FunctionsProtocol(Protocol):
    pass


class Overlay18DataProtocol(Protocol):
    OVERLAY18_D_BOX_LAYOUT_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY18_D_BOX_LAYOUT_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY18_D_BOX_LAYOUT_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY18_D_BOX_LAYOUT_4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY18_D_BOX_LAYOUT_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY18_D_BOX_LAYOUT_6: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY18_D_BOX_LAYOUT_7: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY18_D_BOX_LAYOUT_8: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY18_D_BOX_LAYOUT_9: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY18_D_BOX_LAYOUT_10: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY18_D_BOX_LAYOUT_11: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MOVES_MENU_CONFIRM: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MOVES_SUBMENU_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MOVES_SUBMENU_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MOVES_MAIN_MENU: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MOVES_SUBMENU_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MOVES_SUBMENU_4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MOVES_SUBMENU_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MOVES_SUBMENU_6: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MOVES_SUBMENU_7: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY18_FUNCTION_POINTER_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY18_RESERVED_SPACE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY18_UNKNOWN_POINTER__NA_238D620: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY18_UNKNOWN_POINTER__NA_238D624: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY18_UNKNOWN_POINTER__NA_238D628: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay18Protocol = SectionProtocol[
    Overlay18FunctionsProtocol,
    Overlay18DataProtocol,
    Optional[int],
]


class Overlay19FunctionsProtocol(Protocol):
    GetBarItem: Symbol[
        Optional[List[int]],
        None,
    ]

    GetRecruitableMonsterAll: Symbol[
        Optional[List[int]],
        None,
    ]

    GetRecruitableMonsterList: Symbol[
        Optional[List[int]],
        None,
    ]

    GetRecruitableMonsterListRestricted: Symbol[
        Optional[List[int]],
        None,
    ]


class Overlay19DataProtocol(Protocol):
    OVERLAY19_UNKNOWN_TABLE__NA_238DAE0: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BAR_UNLOCKABLE_DUNGEONS_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BAR_RECRUITABLE_MONSTER_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BAR_AVAILABLE_ITEMS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY19_UNKNOWN_STRING_IDS__NA_238E178: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY19_UNKNOWN_STRUCT__NA_238E1A4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY19_UNKNOWN_STRING_IDS__NA_238E1CC: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BAR_D_BOX_LAYOUT_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BAR_D_BOX_LAYOUT_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BAR_D_BOX_LAYOUT_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BAR_MENU_CONFIRM_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BAR_MENU_CONFIRM_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY19_UNKNOWN_STRING_IDS__NA_238E238: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BAR_MAIN_MENU: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BAR_SUBMENU_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BAR_SUBMENU_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY19_RESERVED_SPACE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY19_UNKNOWN_POINTER__NA_238E360: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY19_UNKNOWN_POINTER__NA_238E364: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay19Protocol = SectionProtocol[
    Overlay19FunctionsProtocol,
    Overlay19DataProtocol,
    Optional[int],
]


class Overlay2FunctionsProtocol(Protocol):
    pass


class Overlay2DataProtocol(Protocol):
    pass


Overlay2Protocol = SectionProtocol[
    Overlay2FunctionsProtocol,
    Overlay2DataProtocol,
    Optional[int],
]


class Overlay20FunctionsProtocol(Protocol):
    pass


class Overlay20DataProtocol(Protocol):
    OVERLAY20_UNKNOWN_POINTER__NA_238CF7C: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECYCLE_MENU_CONFIRM_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECYCLE_MENU_CONFIRM_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECYCLE_SUBMENU_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECYCLE_SUBMENU_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECYCLE_MAIN_MENU_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY20_UNKNOWN_TABLE__NA_238D014: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECYCLE_D_BOX_LAYOUT_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECYCLE_D_BOX_LAYOUT_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECYCLE_D_BOX_LAYOUT_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECYCLE_D_BOX_LAYOUT_4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECYCLE_D_BOX_LAYOUT_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECYCLE_D_BOX_LAYOUT_6: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECYCLE_MAIN_MENU_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECYCLE_D_BOX_LAYOUT_7: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECYCLE_D_BOX_LAYOUT_8: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECYCLE_D_BOX_LAYOUT_9: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECYCLE_D_BOX_LAYOUT1_0: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECYCLE_D_BOX_LAYOUT1_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    RECYCLE_MAIN_MENU_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY20_RESERVED_SPACE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY20_UNKNOWN_POINTER__NA_238D120: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY20_UNKNOWN_POINTER__NA_238D124: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY20_UNKNOWN_POINTER__NA_238D128: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY20_UNKNOWN_POINTER__NA_238D12C: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay20Protocol = SectionProtocol[
    Overlay20FunctionsProtocol,
    Overlay20DataProtocol,
    Optional[int],
]


class Overlay21FunctionsProtocol(Protocol):
    pass


class Overlay21DataProtocol(Protocol):
    SWAP_SHOP_D_BOX_LAYOUT_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SWAP_SHOP_MENU_CONFIRM: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SWAP_SHOP_SUBMENU_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SWAP_SHOP_SUBMENU_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SWAP_SHOP_MAIN_MENU_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SWAP_SHOP_MAIN_MENU_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SWAP_SHOP_SUBMENU_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY21_UNKNOWN_STRING_IDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SWAP_SHOP_D_BOX_LAYOUT_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SWAP_SHOP_D_BOX_LAYOUT_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SWAP_SHOP_D_BOX_LAYOUT_4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SWAP_SHOP_D_BOX_LAYOUT_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SWAP_SHOP_D_BOX_LAYOUT_6: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SWAP_SHOP_D_BOX_LAYOUT_7: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SWAP_SHOP_D_BOX_LAYOUT_8: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SWAP_SHOP_D_BOX_LAYOUT_9: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY21_JP_STRING: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY21_RESERVED_SPACE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY21_UNKNOWN_POINTER__NA_238CF40: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY21_UNKNOWN_POINTER__NA_238CF44: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay21Protocol = SectionProtocol[
    Overlay21FunctionsProtocol,
    Overlay21DataProtocol,
    Optional[int],
]


class Overlay22FunctionsProtocol(Protocol):
    pass


class Overlay22DataProtocol(Protocol):
    SHOP_D_BOX_LAYOUT_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SHOP_D_BOX_LAYOUT_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY22_UNKNOWN_STRUCT__NA_238E85C: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SHOP_MENU_CONFIRM: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SHOP_MAIN_MENU_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SHOP_MAIN_MENU_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SHOP_MAIN_MENU_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY22_UNKNOWN_STRING_IDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SHOP_D_BOX_LAYOUT_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SHOP_D_BOX_LAYOUT_4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SHOP_D_BOX_LAYOUT_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SHOP_D_BOX_LAYOUT_6: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SHOP_D_BOX_LAYOUT_7: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SHOP_D_BOX_LAYOUT_8: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SHOP_D_BOX_LAYOUT_9: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SHOP_D_BOX_LAYOUT_10: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY22_RESERVED_SPACE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY22_UNKNOWN_POINTER__NA_238EC60: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY22_UNKNOWN_POINTER__NA_238EC64: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY22_UNKNOWN_POINTER__NA_238EC68: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY22_UNKNOWN_POINTER__NA_238EC6C: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY22_UNKNOWN_POINTER__NA_238EC70: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay22Protocol = SectionProtocol[
    Overlay22FunctionsProtocol,
    Overlay22DataProtocol,
    Optional[int],
]


class Overlay23FunctionsProtocol(Protocol):
    pass


class Overlay23DataProtocol(Protocol):
    OVERLAY23_UNKNOWN_VALUE__NA_238D2E8: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY23_UNKNOWN_VALUE__NA_238D2EC: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY23_UNKNOWN_STRUCT__NA_238D2F0: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STORAGE_MENU_CONFIRM: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STORAGE_MAIN_MENU_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STORAGE_MAIN_MENU_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STORAGE_MAIN_MENU_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STORAGE_MAIN_MENU_4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY23_UNKNOWN_STRING_IDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STORAGE_D_BOX_LAYOUT_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STORAGE_D_BOX_LAYOUT_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STORAGE_D_BOX_LAYOUT_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STORAGE_D_BOX_LAYOUT_4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STORAGE_D_BOX_LAYOUT_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STORAGE_D_BOX_LAYOUT_6: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STORAGE_D_BOX_LAYOUT_7: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STORAGE_D_BOX_LAYOUT_8: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY23_RESERVED_SPACE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY23_UNKNOWN_POINTER__NA_238D8A0: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay23Protocol = SectionProtocol[
    Overlay23FunctionsProtocol,
    Overlay23DataProtocol,
    Optional[int],
]


class Overlay24FunctionsProtocol(Protocol):
    pass


class Overlay24DataProtocol(Protocol):
    OVERLAY24_UNKNOWN_STRUCT__NA_238C508: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY24_UNKNOWN_STRUCT__NA_238C514: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAYCARE_MENU_CONFIRM: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAYCARE_MAIN_MENU: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY24_UNKNOWN_STRING_IDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAYCARE_D_BOX_LAYOUT_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAYCARE_D_BOX_LAYOUT_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAYCARE_D_BOX_LAYOUT_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAYCARE_D_BOX_LAYOUT_4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAYCARE_D_BOX_LAYOUT_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY24_RESERVED_SPACE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY24_UNKNOWN_POINTER__NA_238C600: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay24Protocol = SectionProtocol[
    Overlay24FunctionsProtocol,
    Overlay24DataProtocol,
    Optional[int],
]


class Overlay25FunctionsProtocol(Protocol):
    pass


class Overlay25DataProtocol(Protocol):
    OVERLAY25_UNKNOWN_STRUCT__NA_238B498: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    APPRAISAL_D_BOX_LAYOUT_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    APPRAISAL_MENU_CONFIRM: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    APPRAISAL_MAIN_MENU: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    APPRAISAL_SUBMENU: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY25_UNKNOWN_STRING_IDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    APPRAISAL_D_BOX_LAYOUT_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    APPRAISAL_D_BOX_LAYOUT_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    APPRAISAL_D_BOX_LAYOUT_4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    APPRAISAL_D_BOX_LAYOUT_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    APPRAISAL_D_BOX_LAYOUT_6: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    APPRAISAL_D_BOX_LAYOUT_7: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    APPRAISAL_D_BOX_LAYOUT_8: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY25_RESERVED_SPACE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY25_UNKNOWN_POINTER__NA_238B5E0: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay25Protocol = SectionProtocol[
    Overlay25FunctionsProtocol,
    Overlay25DataProtocol,
    Optional[int],
]


class Overlay26FunctionsProtocol(Protocol):
    pass


class Overlay26DataProtocol(Protocol):
    OVERLAY26_UNKNOWN_TABLE__NA_238AE20: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY26_RESERVED_SPACE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY26_UNKNOWN_POINTER__NA_238AF60: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY26_UNKNOWN_POINTER__NA_238AF64: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY26_UNKNOWN_POINTER__NA_238AF68: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY26_UNKNOWN_POINTER__NA_238AF6C: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY26_UNKNOWN_POINTER5__NA_238AF70: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay26Protocol = SectionProtocol[
    Overlay26FunctionsProtocol,
    Overlay26DataProtocol,
    Optional[int],
]


class Overlay27FunctionsProtocol(Protocol):
    pass


class Overlay27DataProtocol(Protocol):
    OVERLAY27_UNKNOWN_VALUE__NA_238C948: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY27_UNKNOWN_VALUE__NA_238C94C: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY27_UNKNOWN_STRUCT__NA_238C950: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DISCARD_ITEMS_MENU_CONFIRM: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DISCARD_ITEMS_SUBMENU_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DISCARD_ITEMS_SUBMENU_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DISCARD_ITEMS_MAIN_MENU: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY27_UNKNOWN_STRING_IDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DISCARD_D_BOX_LAYOUT_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DISCARD_D_BOX_LAYOUT_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DISCARD_D_BOX_LAYOUT_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DISCARD_D_BOX_LAYOUT_4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DISCARD_D_BOX_LAYOUT_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DISCARD_D_BOX_LAYOUT_6: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DISCARD_D_BOX_LAYOUT_7: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DISCARD_D_BOX_LAYOUT_8: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY27_RESERVED_SPACE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY27_UNKNOWN_POINTER__NA_238CE80: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY27_UNKNOWN_POINTER__NA_238CE84: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay27Protocol = SectionProtocol[
    Overlay27FunctionsProtocol,
    Overlay27DataProtocol,
    Optional[int],
]


class Overlay28FunctionsProtocol(Protocol):
    pass


class Overlay28DataProtocol(Protocol):
    pass


Overlay28Protocol = SectionProtocol[
    Overlay28FunctionsProtocol,
    Overlay28DataProtocol,
    Optional[int],
]


class Overlay29FunctionsProtocol(Protocol):
    DungeonAlloc: Symbol[
        Optional[List[int]],
        None,
    ]

    GetDungeonPtrMaster: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonZInit: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonFree: Symbol[
        Optional[List[int]],
        None,
    ]

    RunDungeon: Symbol[
        Optional[List[int]],
        None,
    ]

    EntityIsValid: Symbol[
        Optional[List[int]],
        None,
    ]

    GetFloorType: Symbol[
        Optional[List[int]],
        None,
    ]

    TryForcedLoss: Symbol[
        Optional[List[int]],
        None,
    ]

    IsBossFight: Symbol[
        Optional[List[int]],
        None,
    ]

    IsCurrentFixedRoomBossFight: Symbol[
        Optional[List[int]],
        None,
    ]

    IsMarowakTrainingMaze: Symbol[
        Optional[List[int]],
        None,
    ]

    FixedRoomIsSubstituteRoom: Symbol[
        Optional[List[int]],
        None,
    ]

    StoryRestrictionsEnabled: Symbol[
        Optional[List[int]],
        None,
    ]

    GetScenarioBalanceVeneer: Symbol[
        Optional[List[int]],
        None,
    ]

    FadeToBlack: Symbol[
        Optional[List[int]],
        None,
    ]

    GetTileAtEntity: Symbol[
        Optional[List[int]],
        None,
    ]

    SpawnTrap: Symbol[
        Optional[List[int]],
        None,
    ]

    SpawnItemEntity: Symbol[
        Optional[List[int]],
        None,
    ]

    CanSeeTarget: Symbol[
        Optional[List[int]],
        None,
    ]

    CanTargetEntity: Symbol[
        Optional[List[int]],
        None,
    ]

    CanTargetPosition: Symbol[
        Optional[List[int]],
        None,
    ]

    GetTeamMemberIndex: Symbol[
        Optional[List[int]],
        None,
    ]

    SubstitutePlaceholderStringTags: Symbol[
        Optional[List[int]],
        None,
    ]

    UpdateMapSurveyorFlag: Symbol[
        Optional[List[int]],
        None,
    ]

    PointCameraToMonster: Symbol[
        Optional[List[int]],
        None,
    ]

    UpdateCamera: Symbol[
        Optional[List[int]],
        None,
    ]

    ItemIsActive: Symbol[
        Optional[List[int]],
        None,
    ]

    GetVisibilityRange: Symbol[
        Optional[List[int]],
        None,
    ]

    PlayEffectAnimation: Symbol[
        Optional[List[int]],
        None,
    ]

    UpdateStatusIconFlags: Symbol[
        Optional[List[int]],
        None,
    ]

    PlayEffectAnimation0x171Full: Symbol[
        Optional[List[int]],
        None,
    ]

    PlayEffectAnimation0x171: Symbol[
        Optional[List[int]],
        None,
    ]

    ShowPpRestoreEffect: Symbol[
        Optional[List[int]],
        None,
    ]

    PlayEffectAnimation0x1A9: Symbol[
        Optional[List[int]],
        None,
    ]

    PlayEffectAnimation0x18E: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadMappaFileAttributes: Symbol[
        Optional[List[int]],
        None,
    ]

    IsOnMonsterSpawnList: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMonsterIdToSpawn: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMonsterLevelToSpawn: Symbol[
        Optional[List[int]],
        None,
    ]

    GetDirectionTowardsPosition: Symbol[
        Optional[List[int]],
        None,
    ]

    GetChebyshevDistance: Symbol[
        Optional[List[int]],
        None,
    ]

    IsPositionActuallyInSight: Symbol[
        Optional[List[int]],
        None,
    ]

    IsPositionInSight: Symbol[
        Optional[List[int]],
        None,
    ]

    GetLeader: Symbol[
        Optional[List[int]],
        None,
    ]

    GetLeaderMonster: Symbol[
        Optional[List[int]],
        None,
    ]

    FindNearbyUnoccupiedTile: Symbol[
        Optional[List[int]],
        None,
    ]

    FindClosestUnoccupiedTileWithin2: Symbol[
        Optional[List[int]],
        None,
    ]

    FindFarthestUnoccupiedTileWithin2: Symbol[
        Optional[List[int]],
        None,
    ]

    FindUnoccupiedTileWithin3: Symbol[
        Optional[List[int]],
        None,
    ]

    TickStatusTurnCounter: Symbol[
        Optional[List[int]],
        None,
    ]

    AdvanceFrame: Symbol[
        Optional[List[int]],
        None,
    ]

    SetDungeonRngPreseed23Bit: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateDungeonRngSeed: Symbol[
        Optional[List[int]],
        None,
    ]

    GetDungeonRngPreseed: Symbol[
        Optional[List[int]],
        None,
    ]

    SetDungeonRngPreseed: Symbol[
        Optional[List[int]],
        None,
    ]

    InitDungeonRng: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonRand16Bit: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonRandInt: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonRandRange: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonRandOutcome: Symbol[
        Optional[List[int]],
        None,
    ]

    CalcStatusDuration: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonRngUnsetSecondary: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonRngSetSecondary: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonRngSetPrimary: Symbol[
        Optional[List[int]],
        None,
    ]

    ChangeDungeonMusic: Symbol[
        Optional[List[int]],
        None,
    ]

    TrySwitchPlace: Symbol[
        Optional[List[int]],
        None,
    ]

    ClearMonsterActionFields: Symbol[
        Optional[List[int]],
        None,
    ]

    SetMonsterActionFields: Symbol[
        Optional[List[int]],
        None,
    ]

    SetActionPassTurnOrWalk: Symbol[
        Optional[List[int]],
        None,
    ]

    GetItemAction: Symbol[
        Optional[List[int]],
        None,
    ]

    AddDungeonSubMenuOption: Symbol[
        Optional[List[int]],
        None,
    ]

    DisableDungeonSubMenuOption: Symbol[
        Optional[List[int]],
        None,
    ]

    SetActionRegularAttack: Symbol[
        Optional[List[int]],
        None,
    ]

    SetActionUseMoveAi: Symbol[
        Optional[List[int]],
        None,
    ]

    RunFractionalTurn: Symbol[
        Optional[List[int]],
        None,
    ]

    RunLeaderTurn: Symbol[
        Optional[List[int]],
        None,
    ]

    TrySpawnMonsterAndActivatePlusMinus: Symbol[
        Optional[List[int]],
        None,
    ]

    IsFloorOver: Symbol[
        Optional[List[int]],
        None,
    ]

    DecrementWindCounter: Symbol[
        Optional[List[int]],
        None,
    ]

    SetForcedLossReason: Symbol[
        Optional[List[int]],
        None,
    ]

    GetForcedLossReason: Symbol[
        Optional[List[int]],
        None,
    ]

    BindTrapToTile: Symbol[
        Optional[List[int]],
        None,
    ]

    SpawnEnemyTrapAtPos: Symbol[
        Optional[List[int]],
        None,
    ]

    DebugRecruitingEnabled: Symbol[
        Optional[List[int]],
        None,
    ]

    IsSecretBazaarNpcBehavior: Symbol[
        Optional[List[int]],
        None,
    ]

    GetLeaderAction: Symbol[
        Optional[List[int]],
        None,
    ]

    SetLeaderAction: Symbol[
        Optional[List[int]],
        None,
    ]

    ChangeLeader: Symbol[
        Optional[List[int]],
        None,
    ]

    ResetDamageData: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonGetTotalSpriteFileSize: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonGetSpriteIndex: Symbol[
        Optional[List[int]],
        None,
    ]

    JoinedAtRangeCheck2Veneer: Symbol[
        Optional[List[int]],
        None,
    ]

    FloorNumberIsEven: Symbol[
        Optional[List[int]],
        None,
    ]

    GetKecleonIdToSpawnByFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    StoreSpriteFileIndexBothGenders: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadMonsterSpriteInner: Symbol[
        Optional[List[int]],
        None,
    ]

    SwapMonsterWanFileIndex: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadMonsterSprite: Symbol[
        Optional[List[int]],
        None,
    ]

    DeleteMonsterSpriteFile: Symbol[
        Optional[List[int]],
        None,
    ]

    DeleteAllMonsterSpriteFiles: Symbol[
        Optional[List[int]],
        None,
    ]

    EuFaintCheck: Symbol[
        Optional[List[int]],
        None,
    ]

    HandleFaint: Symbol[
        Optional[List[int]],
        None,
    ]

    UpdateAiTargetPos: Symbol[
        Optional[List[int]],
        None,
    ]

    SetMonsterTypeAndAbility: Symbol[
        Optional[List[int]],
        None,
    ]

    TryActivateSlowStart: Symbol[
        Optional[List[int]],
        None,
    ]

    TryActivateArtificialWeatherAbilities: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMonsterApparentId: Symbol[
        Optional[List[int]],
        None,
    ]

    DefenderAbilityIsActive: Symbol[
        Optional[List[int]],
        None,
    ]

    IsMonster: Symbol[
        Optional[List[int]],
        None,
    ]

    TryActivateTruant: Symbol[
        Optional[List[int]],
        None,
    ]

    TryPointCameraToMonster: Symbol[
        Optional[List[int]],
        None,
    ]

    RestorePpAllMovesSetFlags: Symbol[
        Optional[List[int]],
        None,
    ]

    ShouldMonsterHeadToStairs: Symbol[
        Optional[List[int]],
        None,
    ]

    MewSpawnCheck: Symbol[
        Optional[List[int]],
        None,
    ]

    ExclusiveItemEffectIsActive: Symbol[
        Optional[List[int]],
        None,
    ]

    GetTeamMemberWithIqSkill: Symbol[
        Optional[List[int]],
        None,
    ]

    TeamMemberHasEnabledIqSkill: Symbol[
        Optional[List[int]],
        None,
    ]

    TeamLeaderIqSkillIsEnabled: Symbol[
        Optional[List[int]],
        None,
    ]

    CountMovesOutOfPp: Symbol[
        Optional[List[int]],
        None,
    ]

    HasSuperEffectiveMoveAgainstUser: Symbol[
        Optional[List[int]],
        None,
    ]

    CheckSpawnThreshold: Symbol[
        Optional[List[int]],
        None,
    ]

    HasLowHealth: Symbol[
        Optional[List[int]],
        None,
    ]

    AreEntitiesAdjacent: Symbol[
        Optional[List[int]],
        None,
    ]

    IsSpecialStoryAlly: Symbol[
        Optional[List[int]],
        None,
    ]

    IsExperienceLocked: Symbol[
        Optional[List[int]],
        None,
    ]

    SpawnTeam: Symbol[
        Optional[List[int]],
        None,
    ]

    SpawnInitialMonsters: Symbol[
        Optional[List[int]],
        None,
    ]

    SpawnMonster: Symbol[
        Optional[List[int]],
        None,
    ]

    InitTeamMember: Symbol[
        Optional[List[int]],
        None,
    ]

    InitMonster: Symbol[
        Optional[List[int]],
        None,
    ]

    MarkShopkeeperSpawn: Symbol[
        Optional[List[int]],
        None,
    ]

    SpawnShopkeepers: Symbol[
        Optional[List[int]],
        None,
    ]

    GetOutlawSpawnData: Symbol[
        Optional[List[int]],
        None,
    ]

    ExecuteMonsterAction: Symbol[
        Optional[List[int]],
        None,
    ]

    HasStatusThatPreventsActing: Symbol[
        Optional[List[int]],
        None,
    ]

    IsInvalidSpawnTile: Symbol[
        Optional[List[int]],
        None,
    ]

    CalcSpeedStage: Symbol[
        Optional[List[int]],
        None,
    ]

    CalcSpeedStageWrapper: Symbol[
        Optional[List[int]],
        None,
    ]

    GetNumberOfAttacks: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMonsterName: Symbol[
        Optional[List[int]],
        None,
    ]

    SprintfStatic: Symbol[
        Optional[List[int]],
        None,
    ]

    IsMonsterDrowsy: Symbol[
        Optional[List[int]],
        None,
    ]

    MonsterHasNonvolatileNonsleepStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    MonsterHasImmobilizingStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    MonsterHasAttackInterferingStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    MonsterHasSkillInterferingStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    MonsterHasLeechSeedStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    MonsterHasWhifferStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    IsMonsterVisuallyImpaired: Symbol[
        Optional[List[int]],
        None,
    ]

    IsMonsterMuzzled: Symbol[
        Optional[List[int]],
        None,
    ]

    MonsterHasMiracleEyeStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    MonsterHasNegativeStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    IsMonsterSleeping: Symbol[
        Optional[List[int]],
        None,
    ]

    IsMonsterCornered: Symbol[
        Optional[List[int]],
        None,
    ]

    CanAttackInDirection: Symbol[
        Optional[List[int]],
        None,
    ]

    CanAiMonsterMoveInDirection: Symbol[
        Optional[List[int]],
        None,
    ]

    ShouldMonsterRunAway: Symbol[
        Optional[List[int]],
        None,
    ]

    ShouldMonsterRunAwayVariation: Symbol[
        Optional[List[int]],
        None,
    ]

    NoGastroAcidStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    AbilityIsActive: Symbol[
        Optional[List[int]],
        None,
    ]

    AbilityIsActiveVeneer: Symbol[
        Optional[List[int]],
        None,
    ]

    OtherMonsterAbilityIsActive: Symbol[
        Optional[List[int]],
        None,
    ]

    LevitateIsActive: Symbol[
        Optional[List[int]],
        None,
    ]

    MonsterIsType: Symbol[
        Optional[List[int]],
        None,
    ]

    IsTypeAffectedByGravity: Symbol[
        Optional[List[int]],
        None,
    ]

    HasTypeAffectedByGravity: Symbol[
        Optional[List[int]],
        None,
    ]

    CanSeeInvisibleMonsters: Symbol[
        Optional[List[int]],
        None,
    ]

    HasDropeyeStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    IqSkillIsEnabled: Symbol[
        Optional[List[int]],
        None,
    ]

    UpdateIqSkills: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveTypeForMonster: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMovePower: Symbol[
        Optional[List[int]],
        None,
    ]

    UpdateStateFlags: Symbol[
        Optional[List[int]],
        None,
    ]

    AddExpSpecial: Symbol[
        Optional[List[int]],
        None,
    ]

    EnemyEvolution: Symbol[
        Optional[List[int]],
        None,
    ]

    TryDecreaseLevel: Symbol[
        Optional[List[int]],
        None,
    ]

    LevelUp: Symbol[
        Optional[List[int]],
        None,
    ]

    EvolveMonster: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSleepAnimationId: Symbol[
        Optional[List[int]],
        None,
    ]

    DisplayActions: Symbol[
        Optional[List[int]],
        None,
    ]

    EndFrozenClassStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    EndCringeClassStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    TryTriggerMonsterHouse: Symbol[
        Optional[List[int]],
        None,
    ]

    RunMonsterAi: Symbol[
        Optional[List[int]],
        None,
    ]

    ApplyDamageAndEffects: Symbol[
        Optional[List[int]],
        None,
    ]

    ApplyDamage: Symbol[
        Optional[List[int]],
        None,
    ]

    AftermathCheck: Symbol[
        Optional[List[int]],
        None,
    ]

    GetTypeMatchupBothTypes: Symbol[
        Optional[List[int]],
        None,
    ]

    ScrappyShouldActivate: Symbol[
        Optional[List[int]],
        None,
    ]

    IsTypeIneffectiveAgainstGhost: Symbol[
        Optional[List[int]],
        None,
    ]

    GhostImmunityIsActive: Symbol[
        Optional[List[int]],
        None,
    ]

    GetTypeMatchup: Symbol[
        Optional[List[int]],
        None,
    ]

    CalcTypeBasedDamageEffects: Symbol[
        Optional[List[int]],
        None,
    ]

    CalcDamage: Symbol[
        Optional[List[int]],
        None,
    ]

    CalcRecoilDamageFixed: Symbol[
        Optional[List[int]],
        None,
    ]

    CalcDamageFixed: Symbol[
        Optional[List[int]],
        None,
    ]

    CalcDamageFixedNoCategory: Symbol[
        Optional[List[int]],
        None,
    ]

    CalcDamageFixedWrapper: Symbol[
        Optional[List[int]],
        None,
    ]

    UpdateShopkeeperModeAfterAttack: Symbol[
        Optional[List[int]],
        None,
    ]

    ResetDamageCalcDiagnostics: Symbol[
        Optional[List[int]],
        None,
    ]

    SpecificRecruitCheck: Symbol[
        Optional[List[int]],
        None,
    ]

    RecruitCheck: Symbol[
        Optional[List[int]],
        None,
    ]

    TryRecruit: Symbol[
        Optional[List[int]],
        None,
    ]

    TrySpawnMonsterAndTickSpawnCounter: Symbol[
        Optional[List[int]],
        None,
    ]

    AuraBowIsActive: Symbol[
        Optional[List[int]],
        None,
    ]

    ExclusiveItemOffenseBoost: Symbol[
        Optional[List[int]],
        None,
    ]

    ExclusiveItemDefenseBoost: Symbol[
        Optional[List[int]],
        None,
    ]

    TeamMemberHasExclusiveItemEffectActive: Symbol[
        Optional[List[int]],
        None,
    ]

    TrySpawnEnemyItemDrop: Symbol[
        Optional[List[int]],
        None,
    ]

    TickNoSlipCap: Symbol[
        Optional[List[int]],
        None,
    ]

    TickStatusAndHealthRegen: Symbol[
        Optional[List[int]],
        None,
    ]

    InflictSleepStatusSingle: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictSleepStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictNightmareStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictNappingStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictYawningStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictSleeplessStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictPausedStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictInfatuatedStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictBurnStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictBurnStatusWholeTeam: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictPoisonedStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictBadlyPoisonedStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictFrozenStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictConstrictionStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictShadowHoldStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictIngrainStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictWrappedStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    FreeOtherWrappedMonsters: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictPetrifiedStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    LowerOffensiveStat: Symbol[
        Optional[List[int]],
        None,
    ]

    LowerDefensiveStat: Symbol[
        Optional[List[int]],
        None,
    ]

    BoostOffensiveStat: Symbol[
        Optional[List[int]],
        None,
    ]

    BoostDefensiveStat: Symbol[
        Optional[List[int]],
        None,
    ]

    FlashFireShouldActivate: Symbol[
        Optional[List[int]],
        None,
    ]

    ApplyOffensiveStatMultiplier: Symbol[
        Optional[List[int]],
        None,
    ]

    ApplyDefensiveStatMultiplier: Symbol[
        Optional[List[int]],
        None,
    ]

    BoostHitChanceStat: Symbol[
        Optional[List[int]],
        None,
    ]

    LowerHitChanceStat: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictCringeStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictParalysisStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    BoostSpeed: Symbol[
        Optional[List[int]],
        None,
    ]

    BoostSpeedOneStage: Symbol[
        Optional[List[int]],
        None,
    ]

    LowerSpeed: Symbol[
        Optional[List[int]],
        None,
    ]

    TrySealMove: Symbol[
        Optional[List[int]],
        None,
    ]

    BoostOrLowerSpeed: Symbol[
        Optional[List[int]],
        None,
    ]

    ResetHitChanceStat: Symbol[
        Optional[List[int]],
        None,
    ]

    ExclusiveItemEffectIsActiveWithLogging: Symbol[
        Optional[List[int]],
        None,
    ]

    TryActivateQuickFeet: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictConfusedStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictCoweringStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    TryRestoreHp: Symbol[
        Optional[List[int]],
        None,
    ]

    TryIncreaseHp: Symbol[
        Optional[List[int]],
        None,
    ]

    RevealItems: Symbol[
        Optional[List[int]],
        None,
    ]

    RevealStairs: Symbol[
        Optional[List[int]],
        None,
    ]

    RevealEnemies: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictLeechSeedStatus: Symbol[
        Optional[List[int]],
        None,
    ]

    TryInflictDestinyBond: Symbol[
        Optional[List[int]],
        None,
    ]

    IsBlinded: Symbol[
        Optional[List[int]],
        None,
    ]

    RestoreMovePP: Symbol[
        Optional[List[int]],
        None,
    ]

    SetReflectDamageCountdownTo4: Symbol[
        Optional[List[int]],
        None,
    ]

    HasConditionalGroundImmunity: Symbol[
        Optional[List[int]],
        None,
    ]

    Conversion2IsActive: Symbol[
        Optional[List[int]],
        None,
    ]

    AiConsiderMove: Symbol[
        Optional[List[int]],
        None,
    ]

    TryAddTargetToAiTargetList: Symbol[
        Optional[List[int]],
        None,
    ]

    IsAiTargetEligible: Symbol[
        Optional[List[int]],
        None,
    ]

    IsTargetInRange: Symbol[
        Optional[List[int]],
        None,
    ]

    ShouldUsePp: Symbol[
        Optional[List[int]],
        None,
    ]

    GetEntityMoveTargetAndRange: Symbol[
        Optional[List[int]],
        None,
    ]

    GetEntityNaturalGiftInfo: Symbol[
        Optional[List[int]],
        None,
    ]

    GetEntityWeatherBallType: Symbol[
        Optional[List[int]],
        None,
    ]

    IsInSpawnList: Symbol[
        Optional[List[int]],
        None,
    ]

    ChangeShayminForme: Symbol[
        Optional[List[int]],
        None,
    ]

    ApplyItemEffect: Symbol[
        Optional[List[int]],
        None,
    ]

    ViolentSeedBoost: Symbol[
        Optional[List[int]],
        None,
    ]

    ApplyGummiBoostsDungeonMode: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMaxPpWrapper: Symbol[
        Optional[List[int]],
        None,
    ]

    MoveIsNotPhysical: Symbol[
        Optional[List[int]],
        None,
    ]

    CategoryIsNotPhysical: Symbol[
        Optional[List[int]],
        None,
    ]

    TryPounce: Symbol[
        Optional[List[int]],
        None,
    ]

    TryBlowAway: Symbol[
        Optional[List[int]],
        None,
    ]

    TryExplosion: Symbol[
        Optional[List[int]],
        None,
    ]

    TryWarp: Symbol[
        Optional[List[int]],
        None,
    ]

    MoveHitCheck: Symbol[
        Optional[List[int]],
        None,
    ]

    IsHyperBeamVariant: Symbol[
        Optional[List[int]],
        None,
    ]

    HasMaxGinsengBoost99: Symbol[
        Optional[List[int]],
        None,
    ]

    TwoTurnMoveForcedMiss: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonRandOutcomeUserTargetInteraction: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonRandOutcomeUserAction: Symbol[
        Optional[List[int]],
        None,
    ]

    CanAiUseMove: Symbol[
        Optional[List[int]],
        None,
    ]

    CanMonsterUseMove: Symbol[
        Optional[List[int]],
        None,
    ]

    UpdateMovePp: Symbol[
        Optional[List[int]],
        None,
    ]

    GetDamageSourceWrapper: Symbol[
        Optional[List[int]],
        None,
    ]

    LowerSshort: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMoveAnimationId: Symbol[
        Optional[List[int]],
        None,
    ]

    ShouldMovePlayAlternativeAnimation: Symbol[
        Optional[List[int]],
        None,
    ]

    ExecuteMoveEffect: Symbol[
        Optional[List[int]],
        None,
    ]

    DoMoveDamageInlined: Symbol[
        Optional[List[int]],
        None,
    ]

    DealDamage: Symbol[
        Optional[List[int]],
        None,
    ]

    DealDamageWithTypeAndPowerBoost: Symbol[
        Optional[List[int]],
        None,
    ]

    DealDamageProjectile: Symbol[
        Optional[List[int]],
        None,
    ]

    DealDamageWithType: Symbol[
        Optional[List[int]],
        None,
    ]

    PerformDamageSequence: Symbol[
        Optional[List[int]],
        None,
    ]

    StatusCheckerCheck: Symbol[
        Optional[List[int]],
        None,
    ]

    GetApparentWeather: Symbol[
        Optional[List[int]],
        None,
    ]

    TryWeatherFormChange: Symbol[
        Optional[List[int]],
        None,
    ]

    ActivateSportCondition: Symbol[
        Optional[List[int]],
        None,
    ]

    DigitCount: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadTextureUi: Symbol[
        Optional[List[int]],
        None,
    ]

    DisplayNumberTextureUi: Symbol[
        Optional[List[int]],
        None,
    ]

    DisplayCharTextureUi: Symbol[
        Optional[List[int]],
        None,
    ]

    DisplayUi: Symbol[
        Optional[List[int]],
        None,
    ]

    GetTile: Symbol[
        Optional[List[int]],
        None,
    ]

    GetTileSafe: Symbol[
        Optional[List[int]],
        None,
    ]

    IsFullFloorFixedRoom: Symbol[
        Optional[List[int]],
        None,
    ]

    GetStairsRoom: Symbol[
        Optional[List[int]],
        None,
    ]

    GetRandomSpawnMonsterID: Symbol[
        Optional[List[int]],
        None,
    ]

    NearbyAllyIqSkillIsEnabled: Symbol[
        Optional[List[int]],
        None,
    ]

    ResetGravity: Symbol[
        Optional[List[int]],
        None,
    ]

    GravityIsActive: Symbol[
        Optional[List[int]],
        None,
    ]

    ShouldBoostKecleonShopSpawnChance: Symbol[
        Optional[List[int]],
        None,
    ]

    SetShouldBoostKecleonShopSpawnChance: Symbol[
        Optional[List[int]],
        None,
    ]

    UpdateShouldBoostKecleonShopSpawnChance: Symbol[
        Optional[List[int]],
        None,
    ]

    IsSecretBazaar: Symbol[
        Optional[List[int]],
        None,
    ]

    ShouldBoostHiddenStairsSpawnChance: Symbol[
        Optional[List[int]],
        None,
    ]

    SetShouldBoostHiddenStairsSpawnChance: Symbol[
        Optional[List[int]],
        None,
    ]

    UpdateShouldBoostHiddenStairsSpawnChance: Symbol[
        Optional[List[int]],
        None,
    ]

    IsSecretRoom: Symbol[
        Optional[List[int]],
        None,
    ]

    IsSecretFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    GetDungeonGenInfoUnk0C: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMinimapData: Symbol[
        Optional[List[int]],
        None,
    ]

    SetMinimapDataE447: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMinimapDataE447: Symbol[
        Optional[List[int]],
        None,
    ]

    SetMinimapDataE448: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadFixedRoomDataVeneer: Symbol[
        Optional[List[int]],
        None,
    ]

    IsNormalFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    GetTileTerrain: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonRand100: Symbol[
        Optional[List[int]],
        None,
    ]

    ClearHiddenStairs: Symbol[
        Optional[List[int]],
        None,
    ]

    FlagHallwayJunctions: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateStandardFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateOuterRingFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateCrossroadsFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateLineFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateCrossFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateBeetleFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    MergeRoomsVertically: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateOuterRoomsFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    IsNotFullFloorFixedRoom: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateFixedRoom: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateOneRoomMonsterHouseFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateTwoRoomsWithMonsterHouseFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateExtraHallways: Symbol[
        Optional[List[int]],
        None,
    ]

    GetGridPositions: Symbol[
        Optional[List[int]],
        None,
    ]

    InitDungeonGrid: Symbol[
        Optional[List[int]],
        None,
    ]

    AssignRooms: Symbol[
        Optional[List[int]],
        None,
    ]

    CreateRoomsAndAnchors: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateSecondaryStructures: Symbol[
        Optional[List[int]],
        None,
    ]

    AssignGridCellConnections: Symbol[
        Optional[List[int]],
        None,
    ]

    CreateGridCellConnections: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateRoomImperfections: Symbol[
        Optional[List[int]],
        None,
    ]

    CreateHallway: Symbol[
        Optional[List[int]],
        None,
    ]

    EnsureConnectedGrid: Symbol[
        Optional[List[int]],
        None,
    ]

    SetTerrainObstacleChecked: Symbol[
        Optional[List[int]],
        None,
    ]

    FinalizeJunctions: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateKecleonShop: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateMonsterHouse: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateMazeRoom: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateMaze: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateMazeLine: Symbol[
        Optional[List[int]],
        None,
    ]

    SetSpawnFlag5: Symbol[
        Optional[List[int]],
        None,
    ]

    IsNextToHallway: Symbol[
        Optional[List[int]],
        None,
    ]

    ResolveInvalidSpawns: Symbol[
        Optional[List[int]],
        None,
    ]

    ConvertSecondaryTerrainToChasms: Symbol[
        Optional[List[int]],
        None,
    ]

    EnsureImpassableTilesAreWalls: Symbol[
        Optional[List[int]],
        None,
    ]

    InitializeTile: Symbol[
        Optional[List[int]],
        None,
    ]

    ResetFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    PosIsOutOfBounds: Symbol[
        Optional[List[int]],
        None,
    ]

    ShuffleSpawnPositions: Symbol[
        Optional[List[int]],
        None,
    ]

    MarkNonEnemySpawns: Symbol[
        Optional[List[int]],
        None,
    ]

    MarkEnemySpawns: Symbol[
        Optional[List[int]],
        None,
    ]

    SetSecondaryTerrainOnWall: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateSecondaryTerrainFormations: Symbol[
        Optional[List[int]],
        None,
    ]

    StairsAlwaysReachable: Symbol[
        Optional[List[int]],
        None,
    ]

    ConvertWallsToChasms: Symbol[
        Optional[List[int]],
        None,
    ]

    ResetInnerBoundaryTileRows: Symbol[
        Optional[List[int]],
        None,
    ]

    ResetImportantSpawnPositions: Symbol[
        Optional[List[int]],
        None,
    ]

    SpawnStairs: Symbol[
        Optional[List[int]],
        None,
    ]

    GetHiddenStairsType: Symbol[
        Optional[List[int]],
        None,
    ]

    ResetHiddenStairsSpawn: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadFixedRoomData: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadFixedRoom: Symbol[
        Optional[List[int]],
        None,
    ]

    OpenFixedBin: Symbol[
        Optional[List[int]],
        None,
    ]

    CloseFixedBin: Symbol[
        Optional[List[int]],
        None,
    ]

    AreOrbsAllowed: Symbol[
        Optional[List[int]],
        None,
    ]

    AreTileJumpsAllowed: Symbol[
        Optional[List[int]],
        None,
    ]

    AreTrawlOrbsAllowed: Symbol[
        Optional[List[int]],
        None,
    ]

    AreOrbsAllowedVeneer: Symbol[
        Optional[List[int]],
        None,
    ]

    AreLateGameTrapsEnabled: Symbol[
        Optional[List[int]],
        None,
    ]

    AreMovesEnabled: Symbol[
        Optional[List[int]],
        None,
    ]

    IsRoomIlluminated: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMatchingMonsterId: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateItemExplicit: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateAndSpawnItem: Symbol[
        Optional[List[int]],
        None,
    ]

    IsHiddenStairsFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateStandardItem: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateCleanItem: Symbol[
        Optional[List[int]],
        None,
    ]

    SpawnItem: Symbol[
        Optional[List[int]],
        None,
    ]

    SpawnEnemyItemDropWrapper: Symbol[
        Optional[List[int]],
        None,
    ]

    SpawnEnemyItemDrop: Symbol[
        Optional[List[int]],
        None,
    ]

    TryGenerateUnownStoneDrop: Symbol[
        Optional[List[int]],
        None,
    ]

    HasHeldItem: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateMoneyQuantity: Symbol[
        Optional[List[int]],
        None,
    ]

    CheckTeamItemsFlags: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateItem: Symbol[
        Optional[List[int]],
        None,
    ]

    CheckActiveChallengeRequest: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMissionDestination: Symbol[
        Optional[List[int]],
        None,
    ]

    IsOutlawOrChallengeRequestFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    IsDestinationFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    IsCurrentMissionType: Symbol[
        Optional[List[int]],
        None,
    ]

    IsCurrentMissionTypeExact: Symbol[
        Optional[List[int]],
        None,
    ]

    IsOutlawMonsterHouseFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    IsGoldenChamber: Symbol[
        Optional[List[int]],
        None,
    ]

    IsLegendaryChallengeFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    IsJirachiChallengeFloor: Symbol[
        Optional[List[int]],
        None,
    ]

    IsDestinationFloorWithMonster: Symbol[
        Optional[List[int]],
        None,
    ]

    LoadMissionMonsterSprites: Symbol[
        Optional[List[int]],
        None,
    ]

    MissionTargetEnemyIsDefeated: Symbol[
        Optional[List[int]],
        None,
    ]

    SetMissionTargetEnemyDefeated: Symbol[
        Optional[List[int]],
        None,
    ]

    IsDestinationFloorWithFixedRoom: Symbol[
        Optional[List[int]],
        None,
    ]

    GetItemToRetrieve: Symbol[
        Optional[List[int]],
        None,
    ]

    GetItemToDeliver: Symbol[
        Optional[List[int]],
        None,
    ]

    GetSpecialTargetItem: Symbol[
        Optional[List[int]],
        None,
    ]

    IsDestinationFloorWithItem: Symbol[
        Optional[List[int]],
        None,
    ]

    IsDestinationFloorWithHiddenOutlaw: Symbol[
        Optional[List[int]],
        None,
    ]

    IsDestinationFloorWithFleeingOutlaw: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMissionTargetEnemy: Symbol[
        Optional[List[int]],
        None,
    ]

    GetMissionEnemyMinionGroup: Symbol[
        Optional[List[int]],
        None,
    ]

    SetTargetMonsterNotFoundFlag: Symbol[
        Optional[List[int]],
        None,
    ]

    GetTargetMonsterNotFoundFlag: Symbol[
        Optional[List[int]],
        None,
    ]

    FloorHasMissionMonster: Symbol[
        Optional[List[int]],
        None,
    ]

    GenerateMissionEggMonster: Symbol[
        Optional[List[int]],
        None,
    ]

    LogMessageByIdWithPopupCheckParticipants: Symbol[
        Optional[List[int]],
        None,
    ]

    LogMessageByIdWithPopupCheckUser: Symbol[
        Optional[List[int]],
        None,
    ]

    LogMessageWithPopupCheckUser: Symbol[
        Optional[List[int]],
        None,
    ]

    LogMessageByIdQuiet: Symbol[
        Optional[List[int]],
        None,
    ]

    LogMessageQuiet: Symbol[
        Optional[List[int]],
        None,
    ]

    LogMessageByIdWithPopupCheckUserTarget: Symbol[
        Optional[List[int]],
        None,
    ]

    LogMessageWithPopupCheckUserTarget: Symbol[
        Optional[List[int]],
        None,
    ]

    LogMessageByIdQuietCheckUserTarget: Symbol[
        Optional[List[int]],
        None,
    ]

    LogMessageByIdWithPopupCheckUserUnknown: Symbol[
        Optional[List[int]],
        None,
    ]

    LogMessageByIdWithPopup: Symbol[
        Optional[List[int]],
        None,
    ]

    LogMessageWithPopup: Symbol[
        Optional[List[int]],
        None,
    ]

    LogMessage: Symbol[
        Optional[List[int]],
        None,
    ]

    LogMessageById: Symbol[
        Optional[List[int]],
        None,
    ]

    OpenMessageLog: Symbol[
        Optional[List[int]],
        None,
    ]

    RunDungeonMode: Symbol[
        Optional[List[int]],
        None,
    ]

    DisplayDungeonTip: Symbol[
        Optional[List[int]],
        None,
    ]

    SetBothScreensWindowColorToDefault: Symbol[
        Optional[List[int]],
        None,
    ]

    GetPersonalityIndex: Symbol[
        Optional[List[int]],
        None,
    ]

    DisplayMessage: Symbol[
        Optional[List[int]],
        None,
    ]

    DisplayMessage2: Symbol[
        Optional[List[int]],
        None,
    ]

    YesNoMenu: Symbol[
        Optional[List[int]],
        None,
    ]

    DisplayMessageInternal: Symbol[
        Optional[List[int]],
        None,
    ]

    OpenMenu: Symbol[
        Optional[List[int]],
        None,
    ]

    OthersMenuLoop: Symbol[
        Optional[List[int]],
        None,
    ]

    OthersMenu: Symbol[
        Optional[List[int]],
        None,
    ]


class Overlay29DataProtocol(Protocol):
    DUNGEON_STRUCT_SIZE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MAX_HP_CAP: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OFFSET_OF_DUNGEON_FLOOR_PROPERTIES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SPAWN_RAND_MAX: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_PRNG_LCG_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_PRNG_LCG_INCREMENT_SECONDARY: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    KECLEON_FEMALE_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    KECLEON_MALE_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MSG_ID_SLOW_START: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EXPERIENCE_POINT_GAIN_CAP: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    JUDGMENT_MOVE_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    REGULAR_ATTACK_MOVE_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DEOXYS_ATTACK_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DEOXYS_SPEED_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    GIRATINA_ALTERED_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    PUNISHMENT_MOVE_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OFFENSE_STAT_MAX: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    PROJECTILE_MOVE_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BELLY_LOST_PER_TURN: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MONSTER_HEAL_HP_MAX: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MOVE_TARGET_AND_RANGE_SPECIAL_USER_HEALING: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    PLAIN_SEED_VALUE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MAX_ELIXIR_PP_RESTORATION: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SLIP_SEED_VALUE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ROCK_WRECKER_MOVE_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    CASTFORM_NORMAL_FORM_MALE_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    CASTFORM_NORMAL_FORM_FEMALE_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    CHERRIM_SUNSHINE_FORM_MALE_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    CHERRIM_OVERCAST_FORM_FEMALE_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    CHERRIM_SUNSHINE_FORM_FEMALE_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FLOOR_GENERATION_STATUS_PTR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OFFSET_OF_DUNGEON_N_NORMAL_ITEM_SPAWNS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_GRID_COLUMN_BYTES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DEFAULT_MAX_POSITION: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OFFSET_OF_DUNGEON_GUARANTEED_ITEM_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FIXED_ROOM_TILE_SPAWN_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TREASURE_BOX_1_ITEM_IDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FIXED_ROOM_REVISIT_OVERRIDES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FIXED_ROOM_MONSTER_SPAWN_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FIXED_ROOM_ITEM_SPAWN_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FIXED_ROOM_ENTITY_SPAWN_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STATUS_ICON_ARRAY_MUZZLED: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STATUS_ICON_ARRAY_MAGNET_RISE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STATUS_ICON_ARRAY_MIRACLE_EYE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STATUS_ICON_ARRAY_LEECH_SEED: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STATUS_ICON_ARRAY_LONG_TOSS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STATUS_ICON_ARRAY_BLINDED: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STATUS_ICON_ARRAY_BURN: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STATUS_ICON_ARRAY_SURE_SHOT: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STATUS_ICON_ARRAY_INVISIBLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STATUS_ICON_ARRAY_SLEEP: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STATUS_ICON_ARRAY_CURSE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STATUS_ICON_ARRAY_FREEZE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STATUS_ICON_ARRAY_CRINGE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STATUS_ICON_ARRAY_BIDE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STATUS_ICON_ARRAY_REFLECT: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DIRECTIONS_XY: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DISPLACEMENTS_WITHIN_2_LARGEST_FIRST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DISPLACEMENTS_WITHIN_2_SMALLEST_FIRST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DISPLACEMENTS_WITHIN_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ITEM_CATEGORY_ACTIONS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FRACTIONAL_TURN_SEQUENCE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BELLY_DRAIN_IN_WALLS_INT: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BELLY_DRAIN_IN_WALLS_THOUSANDTHS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAMAGE_MULTIPLIER_0_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAMAGE_MULTIPLIER_1_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAMAGE_MULTIPLIER_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    CLOUDY_DAMAGE_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SOLID_ROCK_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAMAGE_FORMULA_MAX_BASE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    WONDER_GUARD_MULTIPLIER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DAMAGE_FORMULA_MIN_BASE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TYPE_DAMAGE_NEGATING_EXCLUSIVE_ITEM_EFFECTS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SPATK_STAT_IDX: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ATK_STAT_IDX: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ROLLOUT_DAMAGE_MULT_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MAP_COLOR_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    CORNER_CARDINAL_NEIGHBOR_IS_OPEN: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_PTR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_PTR_MASTER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    LEADER_PTR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_PRNG_STATE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_PRNG_STATE_SECONDARY_VALUES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EXCL_ITEM_EFFECTS_WEATHER_ATK_SPEED_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EXCL_ITEM_EFFECTS_WEATHER_MOVE_SPEED_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EXCL_ITEM_EFFECTS_WEATHER_NO_STATUS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EXCL_ITEM_EFFECTS_EVASION_BOOST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DEFAULT_TILE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    HIDDEN_STAIRS_SPAWN_BLOCKED: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FIXED_ROOM_DATA_PTR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    NECTAR_IQ_BOOST: Symbol[
        Optional[List[int]],
        None,
    ]


Overlay29Protocol = SectionProtocol[
    Overlay29FunctionsProtocol,
    Overlay29DataProtocol,
    Optional[int],
]


class Overlay3FunctionsProtocol(Protocol):
    pass


class Overlay3DataProtocol(Protocol):
    pass


Overlay3Protocol = SectionProtocol[
    Overlay3FunctionsProtocol,
    Overlay3DataProtocol,
    Optional[int],
]


class Overlay30FunctionsProtocol(Protocol):
    pass


class Overlay30DataProtocol(Protocol):
    OVERLAY30_JP_STRING_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY30_JP_STRING_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay30Protocol = SectionProtocol[
    Overlay30FunctionsProtocol,
    Overlay30DataProtocol,
    Optional[int],
]


class Overlay31FunctionsProtocol(Protocol):
    EntryOverlay31: Symbol[
        Optional[List[int]],
        None,
    ]

    DungeonMenuSwitch: Symbol[
        Optional[List[int]],
        None,
    ]

    MovesMenu: Symbol[
        Optional[List[int]],
        None,
    ]

    HandleMovesMenu: Symbol[
        Optional[List[int]],
        None,
    ]

    TeamMenu: Symbol[
        Optional[List[int]],
        None,
    ]

    RestMenu: Symbol[
        Optional[List[int]],
        None,
    ]

    RecruitmentSearchMenuLoop: Symbol[
        Optional[List[int]],
        None,
    ]

    HelpMenuLoop: Symbol[
        Optional[List[int]],
        None,
    ]


class Overlay31DataProtocol(Protocol):
    DUNGEON_D_BOX_LAYOUT_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_MAIN_MENU: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_UNKNOWN_STRING_IDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_UNKNOWN_STRUCT__NA_2389E30: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_6: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_7: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_SUBMENU_1: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_SUBMENU_2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_SUBMENU_3: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_SUBMENU_4: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_UNKNOWN_STRUCT__NA_2389EF0: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_8: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_9: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_10: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_11: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_12: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_13: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_JP_STRING: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_14: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_15: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_16: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_17: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_18: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_19: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_UNKNOWN_STRUCT__NA_2389FE8: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_20: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_21: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_22: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_23: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_24: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_25: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_SUBMENU_5: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_26: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_UNKNOWN_STRUCT__NA_238A144: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_27: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_28: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_UNKNOWN_STRUCT__NA_238A190: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_SUBMENU_6: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_29: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_30: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_31: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_D_BOX_LAYOUT_32: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_RESERVED_SPACE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_UNKNOWN_POINTER__NA_238A260: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_UNKNOWN_VALUE__NA_238A264: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_UNKNOWN_POINTER__NA_238A268: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_UNKNOWN_POINTER__NA_238A26C: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_UNKNOWN_POINTER__NA_238A270: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_UNKNOWN_POINTER__NA_238A274: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_UNKNOWN_POINTER__NA_238A278: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_UNKNOWN_POINTER__NA_238A27C: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_UNKNOWN_POINTER__NA_238A280: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_UNKNOWN_POINTER__NA_238A284: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_UNKNOWN_POINTER__NA_238A288: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY31_UNKNOWN_POINTER__NA_238A28C: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay31Protocol = SectionProtocol[
    Overlay31FunctionsProtocol,
    Overlay31DataProtocol,
    Optional[int],
]


class Overlay32FunctionsProtocol(Protocol):
    pass


class Overlay32DataProtocol(Protocol):
    pass


Overlay32Protocol = SectionProtocol[
    Overlay32FunctionsProtocol,
    Overlay32DataProtocol,
    Optional[int],
]


class Overlay33FunctionsProtocol(Protocol):
    pass


class Overlay33DataProtocol(Protocol):
    pass


Overlay33Protocol = SectionProtocol[
    Overlay33FunctionsProtocol,
    Overlay33DataProtocol,
    Optional[int],
]


class Overlay34FunctionsProtocol(Protocol):
    ExplorersOfSkyMain: Symbol[
        Optional[List[int]],
        None,
    ]


class Overlay34DataProtocol(Protocol):
    OVERLAY34_UNKNOWN_STRUCT__NA_22DD014: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    START_MENU_CONFIRM: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY34_UNKNOWN_STRUCT__NA_22DD03C: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_DEBUG_MENU: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY34_RESERVED_SPACE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY34_UNKNOWN_POINTER__NA_22DD080: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY34_UNKNOWN_POINTER__NA_22DD084: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY34_UNKNOWN_POINTER__NA_22DD088: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY34_UNKNOWN_POINTER__NA_22DD08C: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    OVERLAY34_UNKNOWN_POINTER__NA_22DD090: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


Overlay34Protocol = SectionProtocol[
    Overlay34FunctionsProtocol,
    Overlay34DataProtocol,
    Optional[int],
]


class Overlay35FunctionsProtocol(Protocol):
    pass


class Overlay35DataProtocol(Protocol):
    pass


Overlay35Protocol = SectionProtocol[
    Overlay35FunctionsProtocol,
    Overlay35DataProtocol,
    Optional[int],
]


class Overlay4FunctionsProtocol(Protocol):
    pass


class Overlay4DataProtocol(Protocol):
    pass


Overlay4Protocol = SectionProtocol[
    Overlay4FunctionsProtocol,
    Overlay4DataProtocol,
    Optional[int],
]


class Overlay5FunctionsProtocol(Protocol):
    pass


class Overlay5DataProtocol(Protocol):
    pass


Overlay5Protocol = SectionProtocol[
    Overlay5FunctionsProtocol,
    Overlay5DataProtocol,
    Optional[int],
]


class Overlay6FunctionsProtocol(Protocol):
    pass


class Overlay6DataProtocol(Protocol):
    pass


Overlay6Protocol = SectionProtocol[
    Overlay6FunctionsProtocol,
    Overlay6DataProtocol,
    Optional[int],
]


class Overlay7FunctionsProtocol(Protocol):
    pass


class Overlay7DataProtocol(Protocol):
    pass


Overlay7Protocol = SectionProtocol[
    Overlay7FunctionsProtocol,
    Overlay7DataProtocol,
    Optional[int],
]


class Overlay8FunctionsProtocol(Protocol):
    pass


class Overlay8DataProtocol(Protocol):
    pass


Overlay8Protocol = SectionProtocol[
    Overlay8FunctionsProtocol,
    Overlay8DataProtocol,
    Optional[int],
]


class Overlay9FunctionsProtocol(Protocol):
    pass


class Overlay9DataProtocol(Protocol):
    TOP_MENU_RETURN_MUSIC_ID: Symbol[
        Optional[List[int]],
        None,
    ]


Overlay9Protocol = SectionProtocol[
    Overlay9FunctionsProtocol,
    Overlay9DataProtocol,
    Optional[int],
]


class RamFunctionsProtocol(Protocol):
    pass


class RamDataProtocol(Protocol):
    DUNGEON_COLORMAP_PTR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DUNGEON_STRUCT: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MOVE_DATA_TABLE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FRAMES_SINCE_LAUNCH: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BAG_ITEMS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BAG_ITEMS_PTR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STORAGE_ITEMS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    STORAGE_ITEM_QUANTITIES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    KECLEON_SHOP_ITEMS_PTR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    KECLEON_SHOP_ITEMS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    UNUSED_KECLEON_SHOP_ITEMS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    KECLEON_WARES_ITEMS_PTR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    KECLEON_WARES_ITEMS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    UNUSED_KECLEON_WARES_ITEMS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MONEY_CARRIED: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    MONEY_STORED: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DIALOG_BOX_LIST: Symbol[
        Optional[List[int]],
        None,
    ]

    LAST_NEW_MOVE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SCRIPT_VARS_VALUES: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    BAG_LEVEL: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    DEBUG_SPECIAL_EPISODE_NUMBER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    PENDING_DUNGEON_ID: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    PENDING_STARTING_FLOOR: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    PLAY_TIME_SECONDS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    PLAY_TIME_FRAME_COUNTER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TEAM_NAME: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TEAM_MEMBER_LIST: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TEAM_ACTIVE_ROSTER: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FRAMES_SINCE_LAUNCH_TIMES_THREE: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    SENTRY_DUTY_STRUCT: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TURNING_ON_THE_SPOT_FLAG: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ROLLOUT_ICE_BALL_MISSED: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    ROLLOUT_ICE_BALL_SUCCESSIVE_HITS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    TRIPLE_KICK_SUCCESSIVE_HITS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    METRONOME_NEXT_INDEX: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    FLOOR_GENERATION_STATUS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


RamProtocol = SectionProtocol[
    RamFunctionsProtocol,
    RamDataProtocol,
    Optional[int],
]


class AllSymbolsProtocol(Protocol):
    arm7: Arm7Protocol

    arm9: Arm9Protocol

    itcm: ItcmProtocol

    move_effects: Move_effectsProtocol

    overlay0: Overlay0Protocol

    overlay1: Overlay1Protocol

    overlay10: Overlay10Protocol

    overlay11: Overlay11Protocol

    overlay12: Overlay12Protocol

    overlay13: Overlay13Protocol

    overlay14: Overlay14Protocol

    overlay15: Overlay15Protocol

    overlay16: Overlay16Protocol

    overlay17: Overlay17Protocol

    overlay18: Overlay18Protocol

    overlay19: Overlay19Protocol

    overlay2: Overlay2Protocol

    overlay20: Overlay20Protocol

    overlay21: Overlay21Protocol

    overlay22: Overlay22Protocol

    overlay23: Overlay23Protocol

    overlay24: Overlay24Protocol

    overlay25: Overlay25Protocol

    overlay26: Overlay26Protocol

    overlay27: Overlay27Protocol

    overlay28: Overlay28Protocol

    overlay29: Overlay29Protocol

    overlay3: Overlay3Protocol

    overlay30: Overlay30Protocol

    overlay31: Overlay31Protocol

    overlay32: Overlay32Protocol

    overlay33: Overlay33Protocol

    overlay34: Overlay34Protocol

    overlay35: Overlay35Protocol

    overlay4: Overlay4Protocol

    overlay5: Overlay5Protocol

    overlay6: Overlay6Protocol

    overlay7: Overlay7Protocol

    overlay8: Overlay8Protocol

    overlay9: Overlay9Protocol

    ram: RamProtocol
