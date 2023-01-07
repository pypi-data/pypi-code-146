from .protocol import Symbol


class EuArm7Functions:
    EntryArm7 = Symbol(
        [0x0],
        [0x2380000],
        None,
        (
            "The entrypoint for the ARM7 CPU. This is like the 'main' function for the"
            " ARM7 subsystem.\n\nNo params."
        ),
    )


class EuArm7Data:
    pass


class EuArm7Section:
    name = "arm7"
    description = (
        "The ARM7 binary.\n\nThis is the secondary binary that gets loaded when the"
        " game is launched.\n\nSpeaking generally, this is the program run by the"
        " Nintendo DS's secondary ARM7TDMI CPU, which handles the audio engine, the"
        " touch screen, Wi-Fi functions, cryptography, and more."
    )
    loadaddress = 0x2380000
    length = 0x27080
    functions = EuArm7Functions
    data = EuArm7Data


class EuArm9Functions:
    EntryArm9 = Symbol(
        [0x800],
        [0x2000800],
        None,
        (
            "The entrypoint for the ARM9 CPU. This is like the 'main' function for the"
            " ARM9 subsystem.\n\nNo params."
        ),
    )

    InitMemAllocTable = Symbol(
        [0xDE0],
        [0x2000DE0],
        None,
        (
            "Initializes MEMORY_ALLOCATION_TABLE.\n\nSets up the default memory arena,"
            " sets the default memory allocator parameters (calls"
            " SetMemAllocatorParams(0, 0)), and does some other stuff.\n\nNo params."
        ),
    )

    SetMemAllocatorParams = Symbol(
        [0xE70],
        [0x2000E70],
        None,
        (
            "Sets global parameters for the memory allocator.\n\nThis includes"
            " MEMORY_ALLOCATION_ARENA_GETTERS and some other stuff.\n\nDungeon mode"
            " uses the default arena getters. Ground mode uses its own arena getters,"
            " which are defined in overlay 11 and set (by calling this function) at the"
            " start of GroundMainLoop.\n\nr0: GetAllocArena function pointer"
            " (GetAllocArenaDefault is used if null)\nr1: GetFreeArena function pointer"
            " (GetFreeArenaDefault is used if null)"
        ),
    )

    GetAllocArenaDefault = Symbol(
        [0xEC0],
        [0x2000EC0],
        None,
        (
            "The default function for retrieving the arena for memory allocations. This"
            " function always just returns the initial arena pointer.\n\nr0: initial"
            " memory arena pointer, or null\nr1: flags (see MemAlloc)\nreturn: memory"
            " arena pointer, or null"
        ),
    )

    GetFreeArenaDefault = Symbol(
        [0xEC4],
        [0x2000EC4],
        None,
        (
            "The default function for retrieving the arena for memory freeing. This"
            " function always just returns the initial arena pointer.\n\nr0: initial"
            " memory arena pointer, or null\nr1: pointer to free\nreturn: memory arena"
            " pointer, or null"
        ),
    )

    InitMemArena = Symbol(
        [0xEC8],
        [0x2000EC8],
        None,
        (
            "Initializes a new memory arena with the given specifications, and records"
            " it in the global MEMORY_ALLOCATION_TABLE.\n\nr0: arena struct to be"
            " initialized\nr1: memory region to be owned by the arena, as {pointer,"
            " length}\nr2: pointer to block metadata array for the arena to use\nr3:"
            " maximum number of blocks that the arena can hold"
        ),
    )

    MemAllocFlagsToBlockType = Symbol(
        [0xF44],
        [0x2000F44],
        None,
        (
            "Converts the internal alloc flags bitfield (struct mem_block field 0x4) to"
            " the block type bitfield (struct mem_block field 0x0).\n\nr0: internal"
            " alloc flags\nreturn: block type flags"
        ),
    )

    FindAvailableMemBlock = Symbol(
        [0xF88],
        [0x2000F88],
        None,
        (
            "Searches through the given memory arena for a block with enough free"
            " space.\n\nBlocks are searched in reverse order. For object allocations"
            " (i.e., not arenas), the block with the smallest amount of free space that"
            " still suffices is returned. For arena allocations, the first satisfactory"
            " block found is returned.\n\nr0: memory arena to search\nr1: internal"
            " alloc flags\nr2: amount of space needed, in bytes\nreturn: index of the"
            " located block in the arena's block array, or -1 if nothing is available"
        ),
    )

    SplitMemBlock = Symbol(
        [0x1070],
        [0x2001070],
        None,
        (
            "Given a memory block at a given index, splits off another memory block of"
            " the specified size from the end.\n\nSince blocks are stored in an array"
            " on the memory arena struct, this is essentially an insertion operation,"
            " plus some processing on the block being split and its child.\n\nr0:"
            " memory arena\nr1: block index\nr2: internal alloc flags\nr3: number of"
            " bytes to split off\nstack[0]: user alloc flags (to assign to the new"
            " block)\nreturn: the newly split-off memory block"
        ),
    )

    MemAlloc = Symbol(
        [0x1170],
        [0x2001170],
        None,
        (
            "Allocates some memory on the heap, returning a pointer to the starting"
            " address.\n\nMemory allocation is done with region-based memory"
            " management. See MEMORY_ALLOCATION_TABLE for more information.\n\nThis"
            " function is just a wrapper around MemLocateSet.\n\nr0: length in"
            " bytes\nr1: flags (see the comment on struct"
            " mem_block::user_flags)\nreturn: pointer"
        ),
    )

    MemFree = Symbol(
        [0x1188],
        [0x2001188],
        None,
        (
            "Frees heap-allocated memory.\n\nThis function is just a wrapper around"
            " MemLocateUnset.\n\nr0: pointer"
        ),
    )

    MemArenaAlloc = Symbol(
        [0x119C],
        [0x200119C],
        None,
        (
            "Allocates some memory on the heap and creates a new global memory arena"
            " with it.\n\nThe actual allocation part works similarly to the normal"
            " MemAlloc.\n\nr0: desired parent memory arena, or null\nr1: length of the"
            " arena in bytes\nr2: maximum number of blocks that the arena can hold\nr3:"
            " flags (see MemAlloc)\nreturn: memory arena pointer"
        ),
    )

    CreateMemArena = Symbol(
        [0x1280],
        [0x2001280],
        None,
        (
            "Creates a new memory arena within a given block of memory.\n\nThis is"
            " essentially a wrapper around InitMemArena, accounting for the space"
            " needed by the arena metadata.\n\nr0: memory region in which to create the"
            " arena, as {pointer, length}\nr1: maximum number of blocks that the arena"
            " can hold\nreturn: memory arena pointer"
        ),
    )

    MemLocateSet = Symbol(
        [0x1390],
        [0x2001390],
        None,
        (
            "The implementation for MemAlloc.\n\nAt a high level, memory is allocated"
            " by choosing a memory arena, looking through blocks in the memory arena"
            " until a free one that's large enough is found, then splitting off a new"
            " memory block of the needed size.\n\nThis function is not fallible, i.e.,"
            " it hangs the whole program on failure, so callers can assume it never"
            " fails.\n\nThe name for this function comes from the error message logged"
            " on failure, and it reflects what the function does: locate an available"
            " block of memory and set it up for the caller.\n\nr0: desired memory arena"
            " for allocation, or null (MemAlloc passes null)\nr1: length in bytes\nr2:"
            " flags (see MemAlloc)\nreturn: pointer to allocated memory"
        ),
    )

    MemLocateUnset = Symbol(
        [0x1638],
        [0x2001638],
        None,
        (
            "The implementation for MemFree.\n\nAt a high level, memory is freed by"
            " locating the pointer in its memory arena (searching block-by-block) and"
            " emptying the block so it's available for future allocations, and merging"
            " it with neighboring blocks if they're available.\n\nr0: desired memory"
            " arena for freeing, or null (MemFree passes null)\nr1: pointer to free"
        ),
    )

    RoundUpDiv256 = Symbol(
        [0x1894],
        [0x2001894],
        None,
        (
            "Divide a number by 256 and round up to the nearest integer.\n\nr0:"
            " number\nreturn: number // 256"
        ),
    )

    MultiplyByFixedPoint = Symbol(
        [0x1A54],
        [0x2001A54],
        None,
        (
            "Multiply a signed integer x by a signed binary fixed-point multiplier (8"
            " fraction bits).\n\nr0: x\nr1: multiplier\nreturn: x * multiplier"
        ),
    )

    UMultiplyByFixedPoint = Symbol(
        [0x1B0C],
        [0x2001B0C],
        None,
        (
            "Multiplies an unsigned integer x by an unsigned binary fixed-point"
            " multiplier (8 fraction bits).\n\nr0: x\nr1: multiplier\nreturn: x *"
            " multiplier"
        ),
    )

    GetRngSeed = Symbol(
        [0x222C], [0x200222C], None, "Get the current value of PRNG_SEQUENCE_NUM."
    )

    SetRngSeed = Symbol(
        [0x223C],
        [0x200223C],
        None,
        "Seed PRNG_SEQUENCE_NUM to a given value.\n\nr0: seed",
    )

    Rand16Bit = Symbol(
        [0x224C],
        [0x200224C],
        None,
        (
            "Computes a pseudorandom 16-bit integer using the general-purpose"
            " PRNG.\n\nNote that much of dungeon mode uses its own (slightly"
            " higher-quality) PRNG within overlay 29. See overlay29.yml for more"
            " information.\n\nRandom numbers are generated with a linear congruential"
            " generator (LCG), using a modulus of 2^16, a multiplier of 109, and an"
            " increment of 1021. I.e., the recurrence relation is `x = (109*x_prev +"
            " 1021) % 2^16`.\n\nThe LCG has a hard-coded seed of 13452 (0x348C), but"
            " can be seeded with a call to SetRngSeed.\n\nreturn: pseudorandom int on"
            " the interval [0, 65535]"
        ),
    )

    RandInt = Symbol(
        [0x2274],
        [0x2002274],
        None,
        (
            "Compute a pseudorandom integer under a given maximum value using the"
            " general-purpose PRNG.\n\nThis function relies on a single call to"
            " Rand16Bit. Even though it takes a 32-bit integer as input, the number of"
            " unique outcomes is capped at 2^16.\n\nr0: high\nreturn: pseudorandom"
            " integer on the interval [0, high - 1]"
        ),
    )

    RandRange = Symbol(
        [0x228C],
        [0x200228C],
        None,
        (
            "Compute a pseudorandom value between two integers using the"
            " general-purpose PRNG.\n\nThis function relies on a single call to"
            " Rand16Bit. Even though it takes 32-bit integers as input, the number of"
            " unique outcomes is capped at 2^16.\n\nr0: x\nr1: y\nreturn: pseudorandom"
            " integer on the interval [x, y - 1]"
        ),
    )

    Rand32Bit = Symbol(
        [0x22AC],
        [0x20022AC],
        None,
        (
            "Computes a random 32-bit integer using the general-purpose PRNG. The upper"
            " and lower 16 bits are each generated with a separate call to Rand16Bit"
            " (so this function advances the PRNG twice).\n\nreturn: pseudorandom int"
            " on the interval [0, 4294967295]"
        ),
    )

    RandIntSafe = Symbol(
        [0x22F8],
        [0x20022F8],
        None,
        (
            "Same as RandInt, except explicitly masking out the upper 16 bits of the"
            " output from Rand16Bit (which should be zero anyway).\n\nr0: high\nreturn:"
            " pseudorandom integer on the interval [0, high - 1]"
        ),
    )

    RandRangeSafe = Symbol(
        [0x2318],
        [0x2002318],
        None,
        (
            "Like RandRange, except reordering the inputs as needed, and explicitly"
            " masking out the upper 16 bits of the output from Rand16Bit (which should"
            " be zero anyway).\n\nr0: x\nr1: y\nreturn: pseudorandom integer on the"
            " interval [min(x, y), max(x, y) - 1]"
        ),
    )

    WaitForever = Symbol(
        [0x2438],
        [0x2002438],
        None,
        (
            "Sets some program state and calls WaitForInterrupt in an infinite"
            " loop.\n\nThis is called on fatal errors to hang the program"
            " indefinitely.\n\nNo params."
        ),
    )

    InterruptMasterDisable = Symbol(
        [0x30CC],
        [0x20030CC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: previous state",
    )

    InterruptMasterEnable = Symbol(
        [0x30E4],
        [0x20030E4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: previous state",
    )

    InitMemAllocTableVeneer = Symbol(
        [0x321C],
        [0x200321C],
        None,
        (
            "Likely a linker-generated veneer for InitMemAllocTable.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nNo"
            " params."
        ),
    )

    ZInit8 = Symbol([0x3228], [0x2003228], None, "Zeroes an 8-byte buffer.\n\nr0: ptr")

    PointsToZero = Symbol(
        [0x3238],
        [0x2003238],
        None,
        "Checks whether a pointer points to zero.\n\nr0: ptr\nreturn: bool",
    )

    MemZero = Symbol(
        [0x3250], [0x2003250], None, "Zeroes a buffer.\n\nr0: ptr\nr1: len"
    )

    MemZero16 = Symbol(
        [0x326C],
        [0x200326C],
        None,
        "Zeros a buffer of 16-bit values.\n\nr0: ptr\nr1: len (# bytes)",
    )

    MemZero32 = Symbol(
        [0x3288],
        [0x2003288],
        None,
        "Zeros a buffer of 32-bit values.\n\nr0: ptr\nr1: len (# bytes)",
    )

    MemsetSimple = Symbol(
        [0x32A4],
        [0x20032A4],
        None,
        (
            "A simple implementation of the memset(3) C library function.\n\nThis"
            " function was probably manually implemented by the developers. See Memset"
            " for what's probably the real libc function.\n\nr0: ptr\nr1: value\nr2:"
            " len (# bytes)"
        ),
    )

    Memset32 = Symbol(
        [0x32BC],
        [0x20032BC],
        None,
        (
            "Fills a buffer of 32-bit values with a given value.\n\nr0: ptr\nr1:"
            " value\nr2: len (# bytes)"
        ),
    )

    MemcpySimple = Symbol(
        [0x32D4],
        [0x20032D4],
        None,
        (
            "A simple implementation of the memcpy(3) C library function.\n\nThis"
            " function was probably manually implemented by the developers. See Memcpy"
            " for what's probably the real libc function.\n\nThis function copies from"
            " src to dst in backwards byte order, so this is safe to call for"
            " overlapping src and dst if src <= dst.\n\nr0: dest\nr1: src\nr2: n"
        ),
    )

    Memcpy16 = Symbol(
        [0x32F0],
        [0x20032F0],
        None,
        (
            "Copies 16-bit values from one buffer to another.\n\nr0: dest\nr1: src\nr2:"
            " n (# bytes)"
        ),
    )

    Memcpy32 = Symbol(
        [0x330C],
        [0x200330C],
        None,
        (
            "Copies 32-bit values from one buffer to another.\n\nr0: dest\nr1: src\nr2:"
            " n (# bytes)"
        ),
    )

    TaskProcBoot = Symbol(
        [0x3328],
        [0x2003328],
        None,
        (
            "Probably related to booting the game?\n\nThis function prints the debug"
            " message 'task proc boot'.\n\nNo params."
        ),
    )

    EnableAllInterrupts = Symbol(
        [0x3608],
        [0x2003608],
        None,
        (
            "Sets the Interrupt Master Enable (IME) register to 1, which enables all"
            " CPU interrupts (if enabled in the Interrupt Enable (IE) register).\n\nSee"
            " https://problemkaputt.de/gbatek.htm#dsiomaps.\n\nreturn: old value in the"
            " IME register"
        ),
    )

    GetTime = Symbol(
        [0x37B4],
        [0x20037B4],
        None,
        (
            "Seems to get the current (system?) time as an IEEE 754 floating-point"
            " number.\n\nreturn: current time (maybe in seconds?)"
        ),
    )

    DisableAllInterrupts = Symbol(
        [0x3824],
        [0x2003824],
        None,
        (
            "Sets the Interrupt Master Enable (IME) register to 0, which disables all"
            " CPU interrupts (even if enabled in the Interrupt Enable (IE)"
            " register).\n\nSee"
            " https://problemkaputt.de/gbatek.htm#dsiomaps.\n\nreturn: old value in the"
            " IME register"
        ),
    )

    SoundResume = Symbol(
        [0x3CC4],
        [0x2003CC4],
        None,
        (
            "Probably resumes the sound player if paused?\n\nThis function prints the"
            " debug string 'sound resume'."
        ),
    )

    CardPullOutWithStatus = Symbol(
        [0x3D2C],
        [0x2003D2C],
        None,
        (
            "Probably aborts the program with some status code? It seems to serve a"
            " similar purpose to the exit(3) function.\n\nThis function prints the"
            " debug string 'card pull out %d' with the status code.\n\nr0: status code"
        ),
    )

    CardPullOut = Symbol(
        [0x3D70],
        [0x2003D70],
        None,
        (
            "Sets some global flag that probably triggers system exit?\n\nThis function"
            " prints the debug string 'card pull out'.\n\nNo params."
        ),
    )

    CardBackupError = Symbol(
        [0x3D94],
        [0x2003D94],
        None,
        (
            "Sets some global flag that maybe indicates a save error?\n\nThis function"
            " prints the debug string 'card backup error'.\n\nNo params."
        ),
    )

    HaltProcessDisp = Symbol(
        [0x3DB8],
        [0x2003DB8],
        None,
        (
            "Maybe halts the process display?\n\nThis function prints the debug string"
            " 'halt process disp %d' with the status code.\n\nr0: status code"
        ),
    )

    OverlayIsLoaded = Symbol(
        [0x3ED0],
        [0x2003ED0],
        None,
        (
            "Checks if an overlay with a certain group ID is currently loaded.\n\nSee"
            " the LOADED_OVERLAY_GROUP_* data symbols or enum overlay_group_id in the C"
            " headers for a mapping between group ID and overlay number.\n\nr0: group"
            " ID of the overlay to check. A group ID of 0 denotes no overlay, and the"
            " return value will always be true in this case.\nreturn: bool"
        ),
    )

    LoadOverlay = Symbol(
        [0x40AC],
        [0x20040AC],
        None,
        (
            "Loads an overlay from ROM by its group ID.\n\nSee the"
            " LOADED_OVERLAY_GROUP_* data symbols or enum overlay_group_id in the C"
            " headers for a mapping between group ID and overlay number.\n\nr0: group"
            " ID of the overlay to load"
        ),
    )

    UnloadOverlay = Symbol(
        [0x4868],
        [0x2004868],
        None,
        (
            "Unloads an overlay from ROM by its group ID.\n\nSee the"
            " LOADED_OVERLAY_GROUP_* data symbols or enum overlay_group_id in the C"
            " headers for a mapping between group ID and overlay number.\n\nr0: group"
            " ID of the overlay to unload\nothers: ?"
        ),
    )

    EuclideanNorm = Symbol(
        [0x5050, 0x50B0],
        [0x2005050, 0x20050B0],
        None,
        (
            "Computes the Euclidean norm of a two-component integer array, sort of like"
            " hypotf(3).\n\nr0: integer array [x, y]\nreturn: sqrt(x*x + y*y)"
        ),
    )

    ClampComponentAbs = Symbol(
        [0x5110],
        [0x2005110],
        None,
        (
            "Clamps the absolute values in a two-component integer array.\n\nGiven an"
            " integer array [x, y] and a maximum absolute value M, clamps each element"
            " of the array to M such that the output array is [min(max(x, -M), M),"
            " min(max(y, -M), M)].\n\nr0: 2-element integer array, will be mutated\nr1:"
            " max absolute value"
        ),
    )

    GetHeldButtons = Symbol(
        [0x61EC],
        [0x20061EC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: controller\nr1:"
            " btn_ptr\nreturn: any_activated"
        ),
    )

    GetPressedButtons = Symbol(
        [0x625C],
        [0x200625C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: controller\nr1:"
            " btn_ptr\nreturn: any_activated"
        ),
    )

    GetReleasedStylus = Symbol(
        [0x6C1C],
        [0x2006C1C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: stylus_ptr\nreturn:"
            " any_activated"
        ),
    )

    KeyWaitInit = Symbol(
        [0x6DA4],
        [0x2006DA4],
        None,
        (
            "Implements (most of?) SPECIAL_PROC_KEY_WAIT_INIT (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    DataTransferInit = Symbol(
        [0x8168],
        [0x2008168],
        None,
        (
            "Initializes data transfer mode to get data from the ROM cartridge.\n\nNo"
            " params."
        ),
    )

    DataTransferStop = Symbol(
        [0x8194],
        [0x2008194],
        None,
        (
            "Finalizes data transfer from the ROM cartridge.\n\nThis function must"
            " always be called if DataTransferInit was called, or the game will"
            " crash.\n\nNo params."
        ),
    )

    FileInitVeneer = Symbol(
        [0x8204],
        [0x2008204],
        None,
        (
            "Likely a linker-generated veneer for FileInit.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " file_stream pointer"
        ),
    )

    FileOpen = Symbol(
        [0x8210],
        [0x2008210],
        None,
        (
            "Opens a file from the ROM file system at the given path, sort of like C's"
            " fopen(3) library function.\n\nr0: file_stream pointer\nr1: file path"
            " string"
        ),
    )

    FileGetSize = Symbol(
        [0x8244],
        [0x2008244],
        None,
        "Gets the size of an open file.\n\nr0: file_stream pointer\nreturn: file size",
    )

    FileRead = Symbol(
        [0x8254],
        [0x2008254],
        None,
        (
            "Reads the contents of a file into the given buffer, and moves the file"
            " cursor accordingly.\n\nData transfer mode must have been initialized"
            " (with DataTransferInit) prior to calling this function. This function"
            " looks like it's doing something akin to calling read(2) or fread(3) in a"
            " loop until all the bytes have been successfully read.\n\nr0: file_stream"
            " pointer\nr1: [output] buffer\nr2: number of bytes to read\nreturn: number"
            " of bytes read"
        ),
    )

    FileSeek = Symbol(
        [0x82A8],
        [0x20082A8],
        None,
        (
            "Sets a file stream's position indicator.\n\nThis function has the a"
            " similar API to the fseek(3) library function from C, including using the"
            " same codes for the `whence` parameter:\n- SEEK_SET=0\n- SEEK_CUR=1\n-"
            " SEEK_END=2\n\nr0: file_stream pointer\nr1: offset\nr2: whence"
        ),
    )

    FileClose = Symbol(
        [0x82C4],
        [0x20082C4],
        None,
        (
            "Closes a file.\n\nData transfer mode must have been initialized (with"
            " DataTransferInit) prior to calling this function.\n\nNote: It is possible"
            " to keep a file stream open even if data transfer mode has been stopped,"
            " in which case the file stream can be used again if data transfer mode is"
            " reinitialized.\n\nr0: file_stream pointer"
        ),
    )

    UnloadFile = Symbol(
        [0x8BD4],
        [0x2008BD4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: addr_ptr",
    )

    LoadFileFromRom = Symbol(
        [0x8C3C],
        [0x2008C3C],
        None,
        (
            "Loads a file from ROM by filepath into a heap-allocated buffer.\n\nr0:"
            " [output] pointer to an IO struct {ptr, len}\nr1: file path string"
            " pointer\nr2: flags"
        ),
    )

    GetDebugFlag1 = Symbol(
        [0xC198],
        [0x200C198],
        None,
        "Just returns 0 in the final binary.\n\nr0: flag ID\nreturn: flag value",
    )

    SetDebugFlag1 = Symbol(
        [0xC1A0],
        [0x200C1A0],
        None,
        "A no-op in the final binary.\n\nr0: flag ID\nr1: flag value",
    )

    AppendProgPos = Symbol(
        [0xC1A8],
        [0x200C1A8],
        None,
        (
            "Write a base message into a string and append the file name and line"
            " number to the end in the format 'file = '%s'  line = %5d\n'.\n\nIf no"
            " program position info is given, 'ProgPos info NULL\n' is appended"
            " instead.\n\nr0: [output] str\nr1: program position info\nr2: base"
            " message\nreturn: number of characters printed, excluding the"
            " null-terminator"
        ),
    )

    DebugPrintTrace = Symbol(
        [0xC1F4],
        [0x200C1F4],
        None,
        (
            "Would log a printf format string tagged with the file name and line number"
            " in the debug binary.\n\nThis still constructs the string, but doesn't"
            " actually do anything with it in the final binary.\n\nIf message is a null"
            " pointer, the string '  Print  ' is used instead.\n\nr0: message\nr1:"
            " program position info (can be null)"
        ),
    )

    DebugPrint0 = Symbol(
        [0xC250, 0xC284],
        [0x200C250, 0x200C284],
        None,
        (
            "Would log a printf format string in the debug binary.\n\nThis still"
            " constructs the string with Vsprintf, but doesn't actually do anything"
            " with it in the final binary.\n\nr0: format\n...: variadic"
        ),
    )

    GetDebugFlag2 = Symbol(
        [0xC2BC],
        [0x200C2BC],
        None,
        "Just returns 0 in the final binary.\n\nr0: flag ID\nreturn: flag value",
    )

    SetDebugFlag2 = Symbol(
        [0xC2C4],
        [0x200C2C4],
        None,
        "A no-op in the final binary.\n\nr0: flag ID\nr1: flag value",
    )

    DebugPrint = Symbol(
        [0xC2C8],
        [0x200C2C8],
        None,
        (
            "Would log a printf format string in the debug binary. A no-op in the final"
            " binary.\n\nr0: log level\nr1: format\n...: variadic"
        ),
    )

    FatalError = Symbol(
        [0xC2E4],
        [0x200C2E4],
        None,
        (
            "Logs some debug messages, then hangs the process.\n\nThis function is"
            " called in lots of places to bail on a fatal error. Looking at the static"
            " data callers use to fill in the program position info is informative, as"
            " it tells you the original file name (probably from the standard __FILE__"
            " macro) and line number (probably from the standard __LINE__ macro) in the"
            " source code.\n\nr0: program position info\nr1: format\n...: variadic"
        ),
    )

    OpenAllPackFiles = Symbol(
        [0xC364],
        [0x200C364],
        None,
        (
            "Open the 6 files at PACK_FILE_PATHS_TABLE into PACK_FILE_OPENED. Called"
            " during game initialisation.\n\nNo params."
        ),
    )

    GetFileLengthInPackWithPackNb = Symbol(
        [0xC3C4],
        [0x200C3C4],
        None,
        (
            "Call GetFileLengthInPack after looking up the global Pack archive by its"
            " number\n\nr0: pack file number\nr1: file number\nreturn: size of the file"
            " in bytes from the Pack Table of Content"
        ),
    )

    LoadFileInPackWithPackId = Symbol(
        [0xC3E4],
        [0x200C3E4],
        None,
        (
            "Call LoadFileInPack after looking up the global Pack archive by its"
            " identifier\n\nr0: pack file identifier\nr1: [output] target buffer\nr2:"
            " file index\nreturn: number of read bytes (identical to the length of the"
            " pack from the Table of Content)"
        ),
    )

    AllocAndLoadFileInPack = Symbol(
        [0xC410],
        [0x200C410],
        None,
        (
            "Allocate a file and load a file from the pack archive inside.\nThe data"
            " pointed by the pointer in the output need to be freed once is not needed"
            " anymore.\n\nr0: pack file identifier\nr1: file index\nr2: [output] result"
            " struct (will contain length and pointer)\nr3: allocation flags"
        ),
    )

    OpenPackFile = Symbol(
        [0xC468],
        [0x200C468],
        None,
        (
            "Open a Pack file, to be read later. Initialise the output"
            " structure.\n\nr0: [output] pack file struct\nr1: file name"
        ),
    )

    GetFileLengthInPack = Symbol(
        [0xC4FC],
        [0x200C4FC],
        None,
        (
            "Get the length of a file entry from a Pack archive\n\nr0: pack file"
            " struct\nr1: file index\nreturn: size of the file in bytes from the Pack"
            " Table of Content"
        ),
    )

    LoadFileInPack = Symbol(
        [0xC50C],
        [0x200C50C],
        None,
        (
            "Load the indexed file from the Pack archive, itself loaded from the"
            " ROM.\n\nr0: pack file struct\nr1: [output] target buffer\nr2: file"
            " index\nreturn: number of read bytes (identical to the length of the pack"
            " from the Table of Content)"
        ),
    )

    GetDamageSource = Symbol(
        [0xCADC],
        [0x200CADC],
        None,
        (
            "Gets the damage source for a given move-item combination.\n\nIf there's no"
            " item, the source is the move ID. If the item is an orb, return"
            " DAMAGE_SOURCE_ORB_ITEM. Otherwise, return"
            " DAMAGE_SOURCE_NON_ORB_ITEM.\n\nr0: move ID\nr1: item ID\nreturn: damage"
            " source"
        ),
    )

    GetItemCategoryVeneer = Symbol(
        [0xCB78],
        [0x200CB78],
        None,
        (
            "Likely a linker-generated veneer for GetItemCategory.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " Item ID\nreturn: Category ID"
        ),
    )

    GetItemMoveId16 = Symbol(
        [0xCB84],
        [0x200CB84],
        None,
        (
            "Wraps GetItemMoveId, ensuring that the return value is 16-bit.\n\nr0: item"
            " ID\nreturn: move ID"
        ),
    )

    IsThrownItem = Symbol(
        [0xCB98],
        [0x200CB98],
        None,
        (
            "Checks if a given item ID is a thrown item (CATEGORY_THROWN_LINE or"
            " CATEGORY_THROWN_ARC).\n\nr0: item ID\nreturn: bool"
        ),
    )

    IsNotMoney = Symbol(
        [0xCBB4],
        [0x200CBB4],
        None,
        "Checks if an item ID is not ITEM_POKE.\n\nr0: item ID\nreturn: bool",
    )

    IsEdible = Symbol(
        [0xCBD4],
        [0x200CBD4],
        None,
        (
            "Checks if an item has an item category of CATEGORY_BERRIES_SEEDS_VITAMINS"
            " or CATEGORY_FOOD_GUMMIES.\n\nr0: item ID\nreturn: bool"
        ),
    )

    IsHM = Symbol(
        [0xCBF8],
        [0x200CBF8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: bool",
    )

    IsGummi = Symbol(
        [0xCC7C],
        [0x200CC7C],
        None,
        "Checks if an item is a Gummi.\n\nr0: item ID\nreturn: bool",
    )

    IsAuraBow = Symbol(
        [0xCC9C],
        [0x200CC9C],
        None,
        (
            "Checks if an item is one of the aura bows received at the start of the"
            " game.\n\nr0: item ID\nreturn: bool"
        ),
    )

    InitItem = Symbol(
        [0xCF24],
        [0x200CF24],
        None,
        (
            "Initialize an item struct with the given information.\n\nThis will resolve"
            " the quantity based on the item type. For Poké, the quantity code will"
            " always be set to 1. For thrown items, the quantity code will be randomly"
            " generated on the range of valid quantities for that item type. For"
            " non-stackable items, the quantity code will always be set to 0."
            " Otherwise, the quantity will be assigned from the quantity"
            " argument.\n\nr0: pointer to item to initialize\nr1: item ID\nr2:"
            " quantity\nr3: sticky flag"
        ),
    )

    InitStandardItem = Symbol(
        [0xCFE0],
        [0x200CFE0],
        None,
        (
            "Wrapper around InitItem with quantity set to 0.\n\nr0: pointer to item to"
            " initialize\nr1: item ID\nr2: sticky flag"
        ),
    )

    GetDisplayedBuyPrice = Symbol(
        [0xD158],
        [0x200D158],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item\nreturn: buy price",
    )

    GetDisplayedSellPrice = Symbol(
        [0xD1A0],
        [0x200D1A0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item\nreturn: sell price",
    )

    GetActualBuyPrice = Symbol(
        [0xD1E8],
        [0x200D1E8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item\nreturn: buy price",
    )

    GetActualSellPrice = Symbol(
        [0xD230],
        [0x200D230],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item\nreturn: sell price",
    )

    FindItemInInventory = Symbol(
        [0xD300],
        [0x200D300],
        None,
        (
            "Returns x if item_id is at position x in the bag\nReturns 0x8000+x if"
            " item_id is at position x in storage\nReturns -1 if item is not"
            " found\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " item_id\nreturn: inventory index"
        ),
    )

    SprintfStatic = Symbol(
        [
            0xD6BC,
            0xE808,
            0x13800,
            0x177C4,
            0x17ADC,
            0x2378C,
            0x239B0,
            0x3822C,
            0x39734,
            0x3AC6C,
            0x3D2A0,
            0x41A48,
            0x42DA0,
            0x52750,
            0x54DDC,
            0x60D64,
        ],
        [
            0x200D6BC,
            0x200E808,
            0x2013800,
            0x20177C4,
            0x2017ADC,
            0x202378C,
            0x20239B0,
            0x203822C,
            0x2039734,
            0x203AC6C,
            0x203D2A0,
            0x2041A48,
            0x2042DA0,
            0x2052750,
            0x2054DDC,
            0x2060D64,
        ],
        None,
        (
            "Functionally the same as Sprintf, just defined statically in many"
            " different places.\n\nSince this is essentially just a wrapper around"
            " vsprintf(3), this function was probably statically defined in a header"
            " somewhere and included in a bunch of different places. See the actual"
            " Sprintf for the one in libc.\n\nr0: str\nr1: format\n...:"
            " variadic\nreturn: number of characters printed, excluding the"
            " null-terminator"
        ),
    )

    ItemZInit = Symbol(
        [0xD8A4], [0x200D8A4], None, "Zero-initializes an item struct.\n\nr0: item"
    )

    WriteItemsToSave = Symbol(
        [0xD9E4],
        [0x200D9E4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: start_address\nr1:"
            " total_length\nreturn: ?"
        ),
    )

    ReadItemsFromSave = Symbol(
        [0xDCCC],
        [0x200DCCC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: start_address\nr1:"
            " total_length\nreturn: ?"
        ),
    )

    IsItemAvailableInDungeonGroup = Symbol(
        [0xE094],
        [0x200E094],
        None,
        (
            "Checks one specific bit from table [NA]2094D34\n\nNote: unverified, ported"
            " from Irdkwia's notes\n\nr0: dungeon ID\nr1: item ID\nreturn: bool"
        ),
    )

    GetItemIdFromList = Symbol(
        [0xE0DC],
        [0x200E0DC],
        None,
        (
            "category_num and item_num are numbers in range 0-10000\n\nNote:"
            " unverified, ported from Irdkwia's notes\n\nr0: list_id\nr1:"
            " category_num\nr2: item_num\nreturn: item ID"
        ),
    )

    NormalizeTreasureBox = Symbol(
        [0xE280],
        [0x200E280],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn:"
            " normalized item ID"
        ),
    )

    RemoveEmptyItems = Symbol(
        [0xE698],
        [0x200E698],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: list_pointer\nr1: size",
    )

    LoadItemPspi2n = Symbol(
        [0xE760],
        [0x200E760],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GetExclusiveItemType = Symbol(
        [0xE830],
        [0x200E830],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: ?",
    )

    GetExclusiveItemOffsetEnsureValid = Symbol(
        [0xE84C],
        [0x200E84C],
        None,
        (
            "Gets the exclusive item offset, which is the item ID relative to that of"
            " the first exclusive item, the Prism Ruff.\n\nIf the given item ID is not"
            " a valid item ID, ITEM_PLAIN_SEED (0x55) is returned. This is a bug, since"
            " 0x55 is the valid exclusive item offset for the Icy Globe.\n\nr0: item"
            " ID\nreturn: offset"
        ),
    )

    IsItemValid = Symbol(
        [0xE890],
        [0x200E890],
        None,
        "Checks if an item ID is valid(?).\n\nr0: item ID\nreturn: bool",
    )

    GetExclusiveItemParameter = Symbol(
        [0xE8B8],
        [0x200E8B8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: ?",
    )

    GetItemCategory = Symbol(
        [0xE8D8],
        [0x200E8D8],
        None,
        (
            "Returns the category of the specified item\n\nr0: Item ID\nreturn: Item"
            " category"
        ),
    )

    EnsureValidItem = Symbol(
        [0xE8F8],
        [0x200E8F8],
        None,
        (
            "Checks if the given item ID is valid (using IsItemValid). If so, return"
            " the given item ID. Otherwise, return ITEM_PLAIN_SEED.\n\nr0: item"
            " ID\nreturn: valid item ID"
        ),
    )

    GetItemName = Symbol(
        [0xE934],
        [0x200E934],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: item"
            " name"
        ),
    )

    GetItemNameFormatted = Symbol(
        [0xE954],
        [0x200E954],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output] name\nr1:"
            " item_id\nr2: flag\nr3: flag2"
        ),
    )

    GetItemBuyPrice = Symbol(
        [0xEA60],
        [0x200EA60],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: buy"
            " price"
        ),
    )

    GetItemSellPrice = Symbol(
        [0xEA80],
        [0x200EA80],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: sell"
            " price"
        ),
    )

    GetItemSpriteId = Symbol(
        [0xEAA0],
        [0x200EAA0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn:"
            " sprite ID"
        ),
    )

    GetItemPaletteId = Symbol(
        [0xEAC0],
        [0x200EAC0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn:"
            " palette ID"
        ),
    )

    GetItemActionName = Symbol(
        [0xEAE0],
        [0x200EAE0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn:"
            " action name ID"
        ),
    )

    GetThrownItemQuantityLimit = Symbol(
        [0xEB00],
        [0x200EB00],
        None,
        (
            "Get the minimum or maximum quantity for a given thrown item ID.\n\nr0:"
            " item ID\nr1: 0 for minimum, 1 for maximum\nreturn: minimum/maximum"
            " quantity for the given item ID"
        ),
    )

    GetItemMoveId = Symbol(
        [0xEB28],
        [0x200EB28],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: move ID",
    )

    TestItemFlag0xE = Symbol(
        [0xEB48],
        [0x200EB48],
        None,
        (
            "Tests bit 7 if r1 is 0, bit 6 if r1 is 1, bit 5 otherwise\n\nNote:"
            " unverified, ported from Irdkwia's notes\n\nr0: item ID\nr1:"
            " bit_id\nreturn: bool"
        ),
    )

    IsItemInTimeDarkness = Symbol(
        [0xEBD8],
        [0x200EBD8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: bool",
    )

    IsItemValidVeneer = Symbol(
        [0xEC00],
        [0x200EC00],
        None,
        (
            "Likely a linker-generated veneer for IsItemValid.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " item ID\nreturn: bool"
        ),
    )

    SetGold = Symbol(
        [0xED80],
        [0x200ED80],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: new value",
    )

    GetGold = Symbol(
        [0xEDA4],
        [0x200EDA4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: value",
    )

    SetMoneyCarried = Symbol(
        [0xEDC4],
        [0x200EDC4],
        None,
        (
            "Sets the amount of money the player is carrying, clamping the value to the"
            " range [0, MAX_MONEY_CARRIED].\n\nr0: new value"
        ),
    )

    GetCurrentBagCapacity = Symbol(
        [0xEE2C],
        [0x200EE2C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: bag capacity",
    )

    IsBagFull = Symbol(
        [0xEE68],
        [0x200EE68],
        None,
        (
            "Implements SPECIAL_PROC_IS_BAG_FULL (see"
            " ScriptSpecialProcessCall).\n\nreturn: bool"
        ),
    )

    GetNbItemsInBag = Symbol(
        [0xEEA4],
        [0x200EEA4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: # items",
    )

    CountNbItemsOfTypeInBag = Symbol(
        [0xEEF4],
        [0x200EEF4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: count",
    )

    CountItemTypeInBag = Symbol(
        [0xEF30],
        [0x200EF30],
        None,
        (
            "Implements SPECIAL_PROC_COUNT_ITEM_TYPE_IN_BAG (see"
            " ScriptSpecialProcessCall).\n\nIrdkwia's notes: Count also"
            " stackable\n\nr0: item ID\nreturn: number of items of the specified ID in"
            " the bag"
        ),
    )

    IsItemInBag = Symbol(
        [0xEF88],
        [0x200EF88],
        None,
        "Checks if an item is in the player's bag.\n\nr0: item ID\nreturn: bool",
    )

    IsItemWithFlagsInBag = Symbol(
        [0xEFC8],
        [0x200EFC8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nr1:"
            " flags\nreturn: bool"
        ),
    )

    IsItemInTreasureBoxes = Symbol(
        [0xF014],
        [0x200F014],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: bool",
    )

    IsHeldItemInBag = Symbol(
        [0xF074],
        [0x200F074],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item\nreturn: bool",
    )

    IsItemForSpecialSpawnInBag = Symbol(
        [0xF0F8],
        [0x200F0F8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: bool",
    )

    HasStorableItems = Symbol(
        [0xF18C],
        [0x200F18C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: bool",
    )

    GetItemIndex = Symbol(
        [0xF1F4],
        [0x200F1F4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_ptr\nreturn: index",
    )

    GetEquivItemIndex = Symbol(
        [0xF234],
        [0x200F234],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_ptr\nreturn: index",
    )

    GetEquippedThrowableItem = Symbol(
        [0xF2B0],
        [0x200F2B0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: index",
    )

    GetFirstUnequippedItemOfType = Symbol(
        [0xF314],
        [0x200F314],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: index",
    )

    CopyItemAtIdx = Symbol(
        [0xF388],
        [0x200F388],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: index\nr1: [output]"
            " item_ptr\nreturn: exists"
        ),
    )

    GetItemAtIdx = Symbol(
        [0xF3F0],
        [0x200F3F0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: index\nreturn: item"
            " pointer"
        ),
    )

    RemoveEmptyItemsInBag = Symbol(
        [0xF418],
        [0x200F418],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    RemoveItemNoHole = Symbol(
        [0xF438],
        [0x200F438],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: index\nreturn: ?",
    )

    RemoveItem = Symbol(
        [0xF4AC],
        [0x200F4AC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: index",
    )

    RemoveHeldItemNoHole = Symbol(
        [0xF4FC],
        [0x200F4FC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: held_index",
    )

    RemoveItemByIdAndStackNoHole = Symbol(
        [0xF57C],
        [0x200F57C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_ptr\nreturn: ?",
    )

    RemoveEquivItem = Symbol(
        [0xF600],
        [0x200F600],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_ptr\nreturn: ?",
    )

    RemoveEquivItemNoHole = Symbol(
        [0xF6A8],
        [0x200F6A8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_ptr\nreturn: ?",
    )

    DecrementStackItem = Symbol(
        [0xF73C],
        [0x200F73C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_ptr\nreturn: ?",
    )

    RemoveItemNoHoleCheck = Symbol(
        [0xF7C0],
        [0x200F7C0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: index\nreturn: ?",
    )

    RemoveFirstUnequippedItemOfType = Symbol(
        [0xF840],
        [0x200F840],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: ?",
    )

    RemoveAllItems = Symbol(
        [0xF850],
        [0x200F850],
        None,
        (
            "WARNING! Does not remove from party items\n\nNote: unverified, ported from"
            " Irdkwia's notes"
        ),
    )

    RemoveAllItemsStartingAt = Symbol(
        [0xF884],
        [0x200F884],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: index",
    )

    SpecialProcAddItemToBag = Symbol(
        [0xF8F4],
        [0x200F8F4],
        None,
        (
            "Implements SPECIAL_PROC_ADD_ITEM_TO_BAG (see"
            " ScriptSpecialProcessCall).\n\nr0: pointer to an owned_item\nreturn: bool"
        ),
    )

    AddItemToBagNoHeld = Symbol(
        [0xF91C],
        [0x200F91C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_str\nreturn: ?",
    )

    AddItemToBag = Symbol(
        [0xF92C],
        [0x200F92C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item_str\nr1:"
            " held_by\nreturn: ?"
        ),
    )

    ScriptSpecialProcess0x39 = Symbol(
        [0xFDFC],
        [0x200FDFC],
        None,
        "Implements SPECIAL_PROC_0x39 (see ScriptSpecialProcessCall).\n\nreturn: bool",
    )

    CountItemTypeInStorage = Symbol(
        [0xFF8C],
        [0x200FF8C],
        None,
        (
            "Implements SPECIAL_PROC_COUNT_ITEM_TYPE_IN_STORAGE (see"
            " ScriptSpecialProcessCall).\n\nr0: pointer to an owned_item\nreturn:"
            " number of items of the specified ID in storage"
        ),
    )

    RemoveItemsTypeInStorage = Symbol(
        [0x1028C],
        [0x201028C],
        None,
        (
            "Probably? Implements SPECIAL_PROC_0x2A (see"
            " ScriptSpecialProcessCall).\n\nr0: pointer to an owned_item\nreturn: bool"
        ),
    )

    AddItemToStorage = Symbol(
        [0x103C4],
        [0x20103C4],
        None,
        (
            "Implements SPECIAL_PROC_ADD_ITEM_TO_STORAGE (see"
            " ScriptSpecialProcessCall).\n\nr0: pointer to an owned_item\nreturn: bool"
        ),
    )

    SetMoneyStored = Symbol(
        [0x107CC],
        [0x20107CC],
        None,
        (
            "Sets the amount of money the player has stored in the Duskull Bank,"
            " clamping the value to the range [0, MAX_MONEY_STORED].\n\nr0: new value"
        ),
    )

    GetKecleonItems1 = Symbol(
        [0x10AF4], [0x2010AF4], None, "Note: unverified, ported from Irdkwia's notes"
    )

    GetKecleonItems2 = Symbol(
        [0x10E00], [0x2010E00], None, "Note: unverified, ported from Irdkwia's notes"
    )

    GetExclusiveItemOffset = Symbol(
        [0x10EE8],
        [0x2010EE8],
        None,
        (
            "Gets the exclusive item offset, which is the item ID relative to that of"
            " the first exclusive item, the Prism Ruff.\n\nr0: item ID\nreturn: offset"
        ),
    )

    ApplyExclusiveItemStatBoosts = Symbol(
        [0x10F0C],
        [0x2010F0C],
        None,
        (
            "Applies stat boosts from an exclusive item.\n\nr0: item ID\nr1: pointer to"
            " attack stat to modify\nr2: pointer to special attack stat to modify\nr3:"
            " pointer to defense stat to modify\nstack[0]: pointer to special defense"
            " stat to modify"
        ),
    )

    SetExclusiveItemEffect = Symbol(
        [0x11028],
        [0x2011028],
        None,
        (
            "Sets the bit for an exclusive item effect.\n\nr0: pointer to the effects"
            " bitvector to modify\nr1: exclusive item effect ID"
        ),
    )

    ExclusiveItemEffectFlagTest = Symbol(
        [0x1104C],
        [0x201104C],
        None,
        (
            "Tests the exclusive item bitvector for a specific exclusive item"
            " effect.\n\nr0: the effects bitvector to test\nr1: exclusive item effect"
            " ID\nreturn: bool"
        ),
    )

    IsExclusiveItemIdForMonster = Symbol(
        [0x1106C],
        [0x201106C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nr1: monster"
            " ID\nr2: type ID 1\nr3: type ID 2\nreturn: bool"
        ),
    )

    IsExclusiveItemForMonster = Symbol(
        [0x1113C],
        [0x201113C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item\nr1: monster"
            " ID\nr2: type ID 1\nr3: type ID 2\nreturn: bool"
        ),
    )

    BagHasExclusiveItemTypeForMonster = Symbol(
        [0x11180],
        [0x2011180],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: excl_type\nr1:"
            " monster ID\nr2: type ID 1\nr3: type ID 2\nreturn: item ID"
        ),
    )

    ProcessGinsengOverworld = Symbol(
        [0x116A0],
        [0x20116A0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: target\nr1: [output]"
            " move ID\nr2: [output] move boost\nreturn: boost"
        ),
    )

    ApplyGummiBoostsGroundMode = Symbol(
        [0x11944],
        [0x2011944],
        None,
        (
            "Applies the IQ boosts from eating a Gummi to the target monster.\n\nr0:"
            " Pointer to something\nr1: Pointer to something\nr2: Pointer to"
            " something\nr3: Pointer to something\nstack[0]: ?\nstack[1]: ?\nstack[2]:"
            " Pointer to a buffer to store some result into"
        ),
    )

    LoadSynthBin = Symbol(
        [0x12B88], [0x2012B88], None, "Note: unverified, ported from Irdkwia's notes"
    )

    CloseSynthBin = Symbol(
        [0x12BDC], [0x2012BDC], None, "Note: unverified, ported from Irdkwia's notes"
    )

    GetSynthItem = Symbol(
        [0x132F8], [0x20132F8], None, "Note: unverified, ported from Irdkwia's notes"
    )

    LoadWazaP = Symbol(
        [0x1346C], [0x201346C], None, "Note: unverified, ported from Irdkwia's notes"
    )

    LoadWazaP2 = Symbol(
        [0x13494], [0x2013494], None, "Note: unverified, ported from Irdkwia's notes"
    )

    UnloadCurrentWazaP = Symbol(
        [0x134BC], [0x20134BC], None, "Note: unverified, ported from Irdkwia's notes"
    )

    GetMoveName = Symbol(
        [0x134FC],
        [0x20134FC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: move"
            " name"
        ),
    )

    FormatMoveString = Symbol(
        [0x13520],
        [0x2013520],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: string_buffer\nr1:"
            " move\nr2: type_print"
        ),
    )

    FormatMoveStringMore = Symbol(
        [0x13828],
        [0x2013828],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ???\nr1: ???\nr2:"
            " move\nr3: type_print"
        ),
    )

    InitMove = Symbol(
        [0x13860],
        [0x2013860],
        None,
        (
            "Initializes a move info struct.\n\nThis sets f_exists and f_enabled_for_ai"
            " on the flags, the ID to the given ID, the PP to the max PP for the move"
            " ID, and the ginseng boost to 0.\n\nr0: pointer to move to initialize\nr1:"
            " move ID"
        ),
    )

    GetInfoMoveCheckId = Symbol(
        [0x13890],
        [0x2013890],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nr1: move ID",
    )

    GetInfoMoveGround = Symbol(
        [0x138D0],
        [0x20138D0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: ground move\nr1: move ID",
    )

    GetMoveTargetAndRange = Symbol(
        [0x138E8],
        [0x20138E8],
        None,
        (
            "Gets the move target-and-range field. See struct move_target_and_range in"
            " the C headers.\n\nr0: move pointer\nr1: AI flag (every move has two"
            " target-and-range fields, one for players and one for AI)\nreturn: move"
            " target and range"
        ),
    )

    GetMoveType = Symbol(
        [0x1390C],
        [0x201390C],
        None,
        "Gets the type of a move\n\nr0: Pointer to move data\nreturn: Type of the move",
    )

    GetMovesetLevelUpPtr = Symbol(
        [0x1392C],
        [0x201392C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn: ?",
    )

    IsInvalidMoveset = Symbol(
        [0x13974],
        [0x2013974],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_id\nreturn: bool",
    )

    GetMovesetHmTmPtr = Symbol(
        [0x1399C],
        [0x201399C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn: ?",
    )

    GetMovesetEggPtr = Symbol(
        [0x139E8],
        [0x20139E8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn: ?",
    )

    GetMoveAiWeight = Symbol(
        [0x13A34],
        [0x2013A34],
        None,
        (
            "Gets the AI weight of a move\n\nr0: Pointer to move data\nreturn: AI"
            " weight of the move"
        ),
    )

    GetMoveNbStrikes = Symbol(
        [0x13A54],
        [0x2013A54],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nreturn: # strikes",
    )

    GetMoveBasePower = Symbol(
        [0x13A74],
        [0x2013A74],
        None,
        (
            "Gets the base power of a move from the move data table.\n\nr0: move"
            " pointer\nreturn: base power"
        ),
    )

    GetMoveBasePowerGround = Symbol(
        [0x13A94],
        [0x2013A94],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ground_move\nreturn:"
            " base power"
        ),
    )

    GetMoveAccuracyOrAiChance = Symbol(
        [0x13AB4],
        [0x2013AB4],
        None,
        (
            "Gets one of the two accuracy values of a move or its"
            " ai_condition_random_chance field.\n\nr0: Move pointer\nr1: 0 to get the"
            " move's first accuracy1 field, 1 to get its accuracy2, 2 to get its"
            " ai_condition_random_chance.\nreturn: Move's accuracy1, accuracy2 or"
            " ai_condition_random_chance"
        ),
    )

    GetMoveBasePp = Symbol(
        [0x13AD8],
        [0x2013AD8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nreturn: base PP",
    )

    GetMaxPp = Symbol(
        [0x13AF8],
        [0x2013AF8],
        None,
        (
            "Gets the maximum PP for a given move.\n\nIrkdwia's notes:"
            " GetMovePPWithBonus\n\nr0: move pointer\nreturn: max PP for the given"
            " move, capped at 99"
        ),
    )

    GetMoveMaxGinsengBoost = Symbol(
        [0x13B78],
        [0x2013B78],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nreturn: max"
            " ginseng boost"
        ),
    )

    GetMoveMaxGinsengBoostGround = Symbol(
        [0x13B98],
        [0x2013B98],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ground_move\nreturn:"
            " max ginseng boost"
        ),
    )

    GetMoveCritChance = Symbol(
        [0x13BB8],
        [0x2013BB8],
        None,
        (
            "Gets the critical hit chance of a move.\n\nr0: move pointer\nreturn:"
            " critical hit chance"
        ),
    )

    IsThawingMove = Symbol(
        [0x13BD8],
        [0x2013BD8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nreturn: bool",
    )

    IsAffectedByTaunt = Symbol(
        [0x13BF8],
        [0x2013BF8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nBased on struct"
            " move_data, maybe this should be IsUsableWhileTaunted?\n\nr0:"
            " move\nreturn: bool"
        ),
    )

    GetMoveRangeId = Symbol(
        [0x13C18],
        [0x2013C18],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nreturn: range ID",
    )

    GetMoveActualAccuracy = Symbol(
        [0x13C38],
        [0x2013C38],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn:"
            " accuracy"
        ),
    )

    GetMoveBasePowerFromId = Symbol(
        [0x13C90],
        [0x2013C90],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: base"
            " power"
        ),
    )

    IsMoveRangeString19 = Symbol(
        [0x13CAC],
        [0x2013CAC],
        None,
        (
            "Returns whether a move's range string is 19 ('User').\n\nr0: Move"
            " pointer\nreturn: True if the move's range string field has a value of 19."
        ),
    )

    GetMoveMessageFromId = Symbol(
        [0x13CD8],
        [0x2013CD8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID?\nreturn: string",
    )

    GetNbMoves = Symbol(
        [0x13D0C],
        [0x2013D0C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_str\nreturn:"
            " # moves"
        ),
    )

    GetMovesetIdx = Symbol(
        [0x13D54, 0x148AC],
        [0x2013D54, 0x20148AC],
        None,
        (
            "Returns the move position in the moveset if it is found, -1"
            " otherwise\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " moveset_str\nr1: move ID\nreturn: ?"
        ),
    )

    IsReflectedByMagicCoat = Symbol(
        [0x13DB0],
        [0x2013DB0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    CanBeSnatched = Symbol(
        [0x13DCC],
        [0x2013DCC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    FailsWhileMuzzled = Symbol(
        [0x13DE8],
        [0x2013DE8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nCalled IsMouthMove in"
            " Irdkwia's notes, which presumably is relevant to the Muzzled"
            " status.\n\nr0: move ID\nreturn: bool"
        ),
    )

    IsSoundMove = Symbol(
        [0x13E04],
        [0x2013E04],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nreturn: bool",
    )

    IsRecoilMove = Symbol(
        [0x13EBC],
        [0x2013EBC],
        None,
        (
            "Checks if the given move is a recoil move (affected by Reckless).\n\nr0:"
            " move ID\nreturn: bool"
        ),
    )

    AllManip1 = Symbol(
        [0x14288], [0x2014288], None, "Note: unverified, ported from Irdkwia's notes"
    )

    AllManip2 = Symbol(
        [0x142B0], [0x20142B0], None, "Note: unverified, ported from Irdkwia's notes"
    )

    ManipMoves1v1 = Symbol(
        [0x14344], [0x2014344], None, "Note: unverified, ported from Irdkwia's notes"
    )

    ManipMoves1v2 = Symbol(
        [0x143E4], [0x20143E4], None, "Note: unverified, ported from Irdkwia's notes"
    )

    ManipMoves2v1 = Symbol(
        [0x1454C], [0x201454C], None, "Note: unverified, ported from Irdkwia's notes"
    )

    ManipMoves2v2 = Symbol(
        [0x145EC], [0x20145EC], None, "Note: unverified, ported from Irdkwia's notes"
    )

    DungeonMoveToGroundMove = Symbol(
        [0x14754],
        [0x2014754],
        None,
        (
            "Converts a struct move to a struct ground_move.\n\nr0: [output]"
            " ground_move\nr1: move"
        ),
    )

    GroundToDungeonMoveset = Symbol(
        [0x1478C],
        [0x201478C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output]"
            " moveset_dun_str\nr1: moveset_str"
        ),
    )

    DungeonToGroundMoveset = Symbol(
        [0x14820],
        [0x2014820],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output]"
            " moveset_str\nr1: moveset_dun_str"
        ),
    )

    GetInfoGroundMoveset = Symbol(
        [0x14860],
        [0x2014860],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_str\nr1:"
            " moves_id"
        ),
    )

    FindFirstFreeMovesetIdx = Symbol(
        [0x14908],
        [0x2014908],
        None,
        (
            "Returns the first position of an empty move in the moveset if it is found,"
            " -1 otherwise\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " moveset_str\nreturn: index"
        ),
    )

    LearnMoves = Symbol(
        [0x14954],
        [0x2014954],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_str\nr1:"
            " moves_id"
        ),
    )

    CopyMoveTo = Symbol(
        [0x14AF4],
        [0x2014AF4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: write_info\nr1:"
            " buffer_write"
        ),
    )

    CopyMoveFrom = Symbol(
        [0x14B2C],
        [0x2014B2C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info\nr1:"
            " buffer_read"
        ),
    )

    CopyMovesetTo = Symbol(
        [0x14B64],
        [0x2014B64],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: write_info\nr1:"
            " buffer_write"
        ),
    )

    CopyMovesetFrom = Symbol(
        [0x14B94],
        [0x2014B94],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info\nr1:"
            " buffer_read"
        ),
    )

    Is2TurnsMove = Symbol(
        [0x14D0C],
        [0x2014D0C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    IsRegularAttackOrProjectile = Symbol(
        [0x14D94],
        [0x2014D94],
        None,
        (
            "Checks if a move ID is MOVE_REGULAR_ATTACK or MOVE_PROJECTILE.\n\nr0: move"
            " ID\nreturn: bool"
        ),
    )

    IsPunchMove = Symbol(
        [0x14DC0],
        [0x2014DC0],
        None,
        (
            "Checks if the given move is a punch move (affected by Iron Fist).\n\nr0:"
            " move ID\nreturn: bool"
        ),
    )

    IsHealingWishOrLunarDance = Symbol(
        [0x14E00],
        [0x2014E00],
        None,
        (
            "Checks if a move ID is MOVE_HEALING_WISH or MOVE_LUNAR_DANCE.\n\nr0: move"
            " ID\nreturn: bool"
        ),
    )

    IsCopyingMove = Symbol(
        [0x14E2C],
        [0x2014E2C],
        None,
        (
            "Checks if a move ID is MOVE_MIMIC, MOVE_SKETCH, or MOVE_COPYCAT.\n\nr0:"
            " move ID\nreturn: bool"
        ),
    )

    IsTrappingMove = Symbol(
        [0x14E64],
        [0x2014E64],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    IsOneHitKoMove = Symbol(
        [0x14EA8],
        [0x2014EA8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    IsNot2TurnsMoveOrSketch = Symbol(
        [0x14EE0],
        [0x2014EE0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    IsRealMove = Symbol(
        [0x14F0C],
        [0x2014F0C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    IsMovesetValid = Symbol(
        [0x14FA0],
        [0x2014FA0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_str\nreturn:"
            " bool"
        ),
    )

    IsRealMoveInTimeDarkness = Symbol(
        [0x1500C],
        [0x201500C],
        None,
        (
            "Seed Flare isn't a real move in Time/Darkness\n\nNote: unverified, ported"
            " from Irdkwia's notes\n\nr0: move ID\nreturn: bool"
        ),
    )

    IsMovesetValidInTimeDarkness = Symbol(
        [0x150AC],
        [0x20150AC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_str\nreturn:"
            " bool"
        ),
    )

    GetFirstNotRealMoveInTimeDarkness = Symbol(
        [0x150CC],
        [0x20150CC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_str\nreturn:"
            " index"
        ),
    )

    IsSameMove = Symbol(
        [0x151F4],
        [0x20151F4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_dun_str\nr1:"
            " move_data_dun_str\nreturn: bool"
        ),
    )

    GetMoveCategory = Symbol(
        [0x15270],
        [0x2015270],
        None,
        (
            "Gets a move's category (physical, special, status).\n\nr0: move"
            " ID\nreturn: move category enum"
        ),
    )

    GetPpIncrease = Symbol(
        [0x1528C],
        [0x201528C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nr1: IQ"
            " skills bitvector\nreturn: PP increase"
        ),
    )

    OpenWaza = Symbol(
        [0x1533C],
        [0x201533C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: waza_id",
    )

    SelectWaza = Symbol(
        [0x153A4],
        [0x20153A4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: waza_id",
    )

    ManipBgmPlayback = Symbol(
        [0x18F40],
        [0x2018F40],
        None,
        (
            "Uncertain. More like bgm1&2 end\n\nNote: unverified, ported from Irdkwia's"
            " notes"
        ),
    )

    SoundDriverReset = Symbol(
        [0x19164],
        [0x2019164],
        None,
        "Uncertain.\n\nNote: unverified, ported from Irdkwia's notes",
    )

    LoadDseFile = Symbol(
        [0x19428],
        [0x2019428],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output] iovec\nr1:"
            " filename\nreturn: bytes read"
        ),
    )

    PlaySeLoad = Symbol(
        [0x19610], [0x2019610], None, "Note: unverified, ported from Irdkwia's notes"
    )

    PlayBgm = Symbol(
        [0x19954], [0x2019954], None, "Note: unverified, ported from Irdkwia's notes"
    )

    StopBgm = Symbol(
        [0x19BC4], [0x2019BC4], None, "Note: unverified, ported from Irdkwia's notes"
    )

    ChangeBgm = Symbol(
        [0x19CEC], [0x2019CEC], None, "Note: unverified, ported from Irdkwia's notes"
    )

    PlayBgm2 = Symbol(
        [0x19E20], [0x2019E20], None, "Note: unverified, ported from Irdkwia's notes"
    )

    StopBgm2 = Symbol(
        [0x1A084], [0x201A084], None, "Note: unverified, ported from Irdkwia's notes"
    )

    ChangeBgm2 = Symbol(
        [0x1A184], [0x201A184], None, "Note: unverified, ported from Irdkwia's notes"
    )

    PlayME = Symbol(
        [0x1A264], [0x201A264], None, "Note: unverified, ported from Irdkwia's notes"
    )

    StopME = Symbol(
        [0x1A4A8],
        [0x201A4A8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: fade_out",
    )

    PlaySe = Symbol(
        [0x1A598], [0x201A598], None, "Note: unverified, ported from Irdkwia's notes"
    )

    PlaySeFullSpec = Symbol(
        [0x1A708], [0x201A708], None, "Note: unverified, ported from Irdkwia's notes"
    )

    SeChangeVolume = Symbol(
        [0x1A8C4], [0x201A8C4], None, "Note: unverified, ported from Irdkwia's notes"
    )

    SeChangePan = Symbol(
        [0x1A99C], [0x201A99C], None, "Note: unverified, ported from Irdkwia's notes"
    )

    StopSe = Symbol(
        [0x1AA80], [0x201AA80], None, "Note: unverified, ported from Irdkwia's notes"
    )

    DeleteWanTableEntry = Symbol(
        [0x1D278],
        [0x201D278],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: wan_table_ptr\nr1:"
            " wan_id"
        ),
    )

    FindWanTableEntry = Symbol(
        [0x1D370],
        [0x201D370],
        None,
        (
            "Appears to search in the given table (in practice always seems to be"
            " LOADED_WAN_TABLE_PTR) for an entry with the given file name.\n\nr0: table"
            " pointer\nr1: file name\nreturn: index of the found file, if found, or -1"
            " if not found"
        ),
    )

    GetLoadedWanTableEntry = Symbol(
        [0x1D3D0],
        [0x201D3D0],
        None,
        (
            "wan_id = -1 if it is not loaded\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: wan_table_ptr\nr1: bin_file_id\nr2: file_id\nreturn: wan_id"
        ),
    )

    LoadWanTableEntry = Symbol(
        [0x1D478],
        [0x201D478],
        None,
        (
            "Appears to load data from the given file (in practice always seems to be"
            " animation data), using previously loaded data in the given table (see"
            " FindWanTableEntry) if possible.\n\nr0: table pointer\nr1: file name\nr2:"
            " flags\nreturn: table index of the loaded data"
        ),
    )

    ReplaceWanFromBinFile = Symbol(
        [0x1D720],
        [0x201D720],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: wan_table_ptr\nr1:"
            " wan_id\nr2: bin_file_id\nr3: file_id\nstack[0]: compressed"
        ),
    )

    DeleteWanTableEntryVeneer = Symbol(
        [0x1D7C8],
        [0x201D7C8],
        None,
        (
            "Likely a linker-generated veneer for DeleteWanTableEntry.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " wan_table_ptr\nr1: wan_id"
        ),
    )

    LoadWteFromRom = Symbol(
        [0x1DEE8],
        [0x201DEE8],
        None,
        (
            "Loads a SIR0-wrapped WTE file from ROM, and returns a handle to it\n\nr0:"
            " [output] pointer to wte handle\nr1: file path string\nr2: load file flags"
        ),
    )

    LoadWteFromFileDirectory = Symbol(
        [0x1DF60],
        [0x201DF60],
        None,
        (
            "Loads a SIR0-wrapped WTE file from a file directory, and returns a handle"
            " to it\n\nr0: [output] pointer to wte handle\nr1: file directory id\nr2:"
            " file index\nr3: malloc flags"
        ),
    )

    UnloadWte = Symbol(
        [0x1DFB4],
        [0x201DFB4],
        None,
        (
            "Frees the buffer used to store the WTE data in the handle, and sets both"
            " pointers to null\n\nr0: pointer to wte handle"
        ),
    )

    LoadWtuFromBin = Symbol(
        [0x1E050],
        [0x201E050],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: bin_file_id\nr1:"
            " file_id\nr2: load_type\nreturn: ?"
        ),
    )

    ProcessWte = Symbol(
        [0x1E14C],
        [0x201E14C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: header_ptr\nr1:"
            " unk_pal\nr2: unk_tex\nr3: unk_tex_param"
        ),
    )

    HandleSir0Translation = Symbol(
        [0x1F550],
        [0x201F550],
        None,
        (
            "Translates the offsets in a SIR0 file into NDS memory addresses, changes"
            " the magic number to SirO (opened), and returns a pointer to the first"
            " pointer specified in the SIR0 header (beginning of the"
            " data).\n\nIrkdiwa's notes:\n  ret_code = 0 if it wasn't a SIR0 file\n "
            " ret_code = 1 if it has been transformed in SIRO file\n  ret_code = 2 if"
            " it was already a SIRO file\n  [output] contains a pointer to the header"
            " of the SIRO file if ret_code = 1 or 2\n  [output] contains a pointer"
            " which is exactly the same as the sir0_ptr if ret_code = 0\n\nr0: [output]"
            " double pointer to beginning of data\nr1: pointer to source file"
            " buffer\nreturn: return code"
        ),
    )

    ConvertPointersSir0 = Symbol(
        [0x1F5D0],
        [0x201F5D0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: sir0_ptr",
    )

    HandleSir0TranslationVeneer = Symbol(
        [0x1F628],
        [0x201F628],
        None,
        (
            "Likely a linker-generated veneer for HandleSir0Translation.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " [output] double pointer to beginning of data\nr1: pointer to source file"
            " buffer\nreturn: return code"
        ),
    )

    DecompressAtNormalVeneer = Symbol(
        [0x1F65C],
        [0x201F65C],
        None,
        (
            "Likely a linker-generated veneer for DecompressAtNormal.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " addr_decomp\nr1: expected_size\nr2: AT pointer\nreturn: ?"
        ),
    )

    DecompressAtNormal = Symbol(
        [0x1F668],
        [0x201F668],
        None,
        (
            "Overwrites r3 probably passed to match DecompressAtHalf's"
            " definition.\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " addr_decomp\nr1: expected_size\nr2: AT pointer\nreturn: ?"
        ),
    )

    DecompressAtHalf = Symbol(
        [0x1FAAC],
        [0x201FAAC],
        None,
        (
            "Same as DecompressAtNormal, except it stores each nibble as a byte\nand"
            " adds the high nibble (r3).\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: addr_decomp\nr1: expected_size\nr2: AT pointer\nr3:"
            " high_nibble\nreturn: ?"
        ),
    )

    DecompressAtFromMemoryPointerVeneer = Symbol(
        [0x1FFE8],
        [0x201FFE8],
        None,
        (
            "Likely a linker-generated veneer for DecompressAtFromMemoryPointer.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " addr_decomp\nr1: expected_size\nr2: AT pointer\nreturn: ?"
        ),
    )

    DecompressAtFromMemoryPointer = Symbol(
        [0x1FFF4],
        [0x201FFF4],
        None,
        (
            "Overwrites r3 probably passed to match DecompressAtHalf's"
            " definition.\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " addr_decomp\nr1: expected_size\nr2: AT pointer\nreturn: ?"
        ),
    )

    WriteByteFromMemoryPointer = Symbol(
        [0x2050C],
        [0x202050C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: byte",
    )

    GetAtSize = Symbol(
        [0x20588],
        [0x2020588],
        None,
        (
            "Doesn't work for AT3PX and AT4PN\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: AT pointer\nr1: ?\nreturn: ?"
        ),
    )

    GetLanguageType = Symbol(
        [0x20688],
        [0x2020688],
        None,
        (
            "Gets the language type.\n\nThis is the value backing the special"
            " LANGUAGE_TYPE script variable.\n\nreturn: language type"
        ),
    )

    GetLanguage = Symbol(
        [0x206B0],
        [0x20206B0],
        None,
        (
            "Gets the single-byte language ID of the current program.\n\nThe language"
            " ID appears to be used to index some global tables.\n\nreturn: language ID"
        ),
    )

    StrcmpTag = Symbol(
        [0x20A20],
        [0x2020A20],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: s1\nr1: s2\nreturn: bool",
    )

    StoiTag = Symbol(
        [0x20A64],
        [0x2020A64],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: s\nreturn: int",
    )

    AnalyzeText = Symbol(
        [0x20F20],
        [0x2020F20],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nreturn: ?",
    )

    PreprocessString = Symbol(
        [0x225EC],
        [0x20225EC],
        None,
        (
            "An enhanced sprintf, which recognizes certain tags and replaces them with"
            " appropiate game values.\nThis function can also be used to simply insert"
            " values passed within the preprocessor args\n\nThe tags utilized for this"
            " function are lowercase, it might produce uppercase tags\nthat only are"
            " used when the text is being typewrited into a message box\n\nIrdkwia's"
            " notes: MenuCreateOptionString\n\nr0: [output] formatted string\nr1:"
            " maximum capacity of the output buffer\nr2: input format string\nr3:"
            " preprocessor flags\nstack[0]: pointer to preprocessor args"
        ),
    )

    PreprocessStringFromMessageId = Symbol(
        [0x237B4],
        [0x20237B4],
        None,
        (
            "Calls PreprocessString after resolving the given message ID to a"
            " string.\n\nr0: [output] formatted string\nr1: maximum capacity of the"
            " output buffer\nr2: message ID\nr3: preprocessor flags\nstack[0]: pointer"
            " to preprocessor args"
        ),
    )

    InitPreprocessorArgs = Symbol(
        [0x238B4],
        [0x20238B4],
        None,
        "Initializes a struct preprocess_args.\n\nr0: preprocessor args pointer",
    )

    SetStringAccuracy = Symbol(
        [0x245C0], [0x20245C0], None, "Note: unverified, ported from Irdkwia's notes"
    )

    SetStringPower = Symbol(
        [0x24688], [0x2024688], None, "Note: unverified, ported from Irdkwia's notes"
    )

    SetQuestionMarks = Symbol(
        [0x253B0],
        [0x20253B0],
        None,
        (
            "Fills the buffer with the string '???'\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: buffer"
        ),
    )

    StrcpySimple = Symbol(
        [0x253CC],
        [0x20253CC],
        None,
        (
            "A simple implementation of the strcpy(3) C library function.\n\nThis"
            " function was probably manually implemented by the developers. See Strcpy"
            " for what's probably the real libc function.\n\nr0: dest\nr1: src"
        ),
    )

    StrncpySimple = Symbol(
        [0x253E8],
        [0x20253E8],
        None,
        (
            "A simple implementation of the strncpy(3) C library function.\n\nThis"
            " function was probably manually implemented by the developers. See Strncpy"
            " for what's probably the real libc function.\n\nr0: dest\nr1: src\nr2: n"
        ),
    )

    StrncpySimpleNoPad = Symbol(
        [0x2543C],
        [0x202543C],
        None,
        (
            "Similar to StrncpySimple, but does not zero-pad the end of dest beyond the"
            " null-terminator.\n\nr0: dest\nr1: src\nr2: n"
        ),
    )

    StrncmpSimple = Symbol(
        [0x25478],
        [0x2025478],
        None,
        (
            "A simple implementation of the strncmp(3) C library function.\n\nThis"
            " function was probably manually implemented by the developers. See Strncmp"
            " for what's probably the real libc function.\n\nr0: s1\nr1: s2\nr2:"
            " n\nreturn: comparison value"
        ),
    )

    StrncpySimpleNoPadSafe = Symbol(
        [0x254C0],
        [0x20254C0],
        None,
        (
            "Like StrncpySimpleNoPad, except there's a useless check on that each"
            " character is less than 0x100 (which is impossible for the result of a"
            " ldrb instruction).\n\nr0: dest\nr1: src\nr2: n"
        ),
    )

    SpecialStrcpy = Symbol(
        [0x254FC],
        [0x20254FC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dst\nr1: src",
    )

    GetStringFromFile = Symbol(
        [0x25A54],
        [0x2025A54],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: Buffer\nr1: String ID",
    )

    LoadStringFile = Symbol(
        [0x25AE4],
        [0x2025AE4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GetStringFromFileVeneer = Symbol(
        [0x25B84],
        [0x2025B84],
        None,
        (
            "Likely a linker-generated veneer for GetStringFromFile.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " Buffer\nr1: String ID"
        ),
    )

    StringFromMessageId = Symbol(
        [0x25B90],
        [0x2025B90],
        None,
        (
            "Gets the string corresponding to a given message ID.\n\nr0: message"
            " ID\nreturn: string from the string files with the given message ID"
        ),
    )

    CopyStringFromMessageId = Symbol(
        [0x25BD8],
        [0x2025BD8],
        None,
        (
            "Gets the string corresponding to a given message ID and copies it to the"
            " buffer specified in r0.\n\nThis function won't write more than <buffer"
            " length> bytes.\n\nr0: Buffer\nr1: String ID\nr2: Buffer length"
        ),
    )

    LoadTblTalk = Symbol(
        [0x25C08],
        [0x2025C08],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GetTalkLine = Symbol(
        [0x25C58],
        [0x2025C58],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0:"
            " personality_index\nr1: group_id\nr2: restrictions\nreturn: ?"
        ),
    )

    SetScreenWindowsColor = Symbol(
        [0x27D5C],
        [0x2027D5C],
        None,
        (
            "Sets the palette of the frames of windows in the specified screen\n\nr0:"
            " palette index\nr1: is upper screen"
        ),
    )

    SetBothScreensWindowsColor = Symbol(
        [0x27D74],
        [0x2027D74],
        None,
        (
            "Sets the palette of the frames of windows in both screens\n\nr0: palette"
            " index"
        ),
    )

    GetDialogBoxField0xC = Symbol(
        [0x28630],
        [0x2028630],
        None,
        (
            "Gets field_0xc from the dialog box of the given ID.\n\nr0:"
            " dbox_id\nreturn: field_0xc"
        ),
    )

    Arm9LoadUnkFieldNa0x2029EC8 = Symbol(
        [0x2A1BC],
        [0x202A1BC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id",
    )

    Arm9StoreUnkFieldNa0x2029ED8 = Symbol(
        [0x2A1CC],
        [0x202A1CC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nr1: value",
    )

    CreateNormalMenu = Symbol(
        [0x2B3E0],
        [0x202B3E0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0:"
            " layout_struct_ptr\nr1: menu_flags\nr2: additional_info_ptr\nr3:"
            " menu_struct_ptr\nstack[0]: option_id\nreturn: menu_id"
        ),
    )

    FreeNormalMenu = Symbol(
        [0x2B7B8],
        [0x202B7B8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id",
    )

    IsNormalMenuActive = Symbol(
        [0x2B7E4],
        [0x202B7E4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id\nreturn: bool",
    )

    GetNormalMenuResult = Symbol(
        [0x2B870],
        [0x202B870],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id\nreturn: ?",
    )

    CreateAdvancedMenu = Symbol(
        [0x2BD14],
        [0x202BD14],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0:"
            " layout_struct_ptr\nr1: menu_flags\nr2: additional_info_ptr\nr3:"
            " entry_function\nstack[0]: nb_options\nstack[1]: nb_opt_pp\nreturn:"
            " menu_id"
        ),
    )

    FreeAdvancedMenu = Symbol(
        [0x2BF38],
        [0x202BF38],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id",
    )

    IsAdvancedMenuActive = Symbol(
        [0x2BFD0],
        [0x202BFD0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id\nreturn: bool",
    )

    GetAdvancedMenuCurrentOption = Symbol(
        [0x2BFF0],
        [0x202BFF0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id\nreturn: ?",
    )

    GetAdvancedMenuResult = Symbol(
        [0x2C004],
        [0x202C004],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id\nreturn: ?",
    )

    CreateDBox = Symbol(
        [0x2F3A4],
        [0x202F3A4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0:"
            " layout_struct_ptr\nreturn: dbox_id"
        ),
    )

    FreeDBox = Symbol(
        [0x2F43C],
        [0x202F43C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id",
    )

    IsDBoxActive = Symbol(
        [0x2F474],
        [0x202F474],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id\nreturn: bool",
    )

    ShowMessageInDBox = Symbol(
        [0x2F4A8],
        [0x202F4A8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id\nr1:"
            " preprocessor flags (see PreprocessString)\nr2: string_id\nr3: pointer to"
            " preprocessor args (see PreprocessString)"
        ),
    )

    ShowDBox = Symbol(
        [0x2F698],
        [0x202F698],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id",
    )

    CreatePortraitBox = Symbol(
        [0x2F8A0],
        [0x202F8A0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ???\nr1: ???\nr2:"
            " ???\nreturn: dbox_id"
        ),
    )

    FreePortraitBox = Symbol(
        [0x2F944],
        [0x202F944],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id",
    )

    ShowPortraitBox = Symbol(
        [0x2F984],
        [0x202F984],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id\nr1:"
            " portrait_ptr"
        ),
    )

    HidePortraitBox = Symbol(
        [0x2F9D0],
        [0x202F9D0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id",
    )

    IsMenuOptionActive = Symbol(
        [0x32768],
        [0x2032768],
        None,
        (
            "Called whenever a menu option is selected. Returns whether the option is"
            " active or not.\n\nr0: ?\nReturn: True if the menu option is enabled,"
            " false otherwise."
        ),
    )

    ShowKeyboard = Symbol(
        [0x36AE4],
        [0x2036AE4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: MessageID\nr1:"
            " buffer1\nr2: ???\nr3: buffer2\nreturn: ?"
        ),
    )

    GetKeyboardStatus = Symbol(
        [0x36FD0],
        [0x2036FD0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    GetKeyboardStringResult = Symbol(
        [0x37858],
        [0x2037858],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    PrintMoveOptionMenu = Symbol(
        [0x405BC],
        [0x20405BC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    PrintIqSkillsMenu = Symbol(
        [0x41D3C],
        [0x2041D3C],
        None,
        (
            "Draws the IQ skills menu for a certain monster.\n\nr0: Monster"
            " species\nr1: Pointer to bitarray where the enabled skills will be written"
            " when enabling or disabling them in the menu\nr2: Monster IQ\nr3: True if"
            " the monster is blinded"
        ),
    )

    GetNotifyNote = Symbol(
        [0x487BC],
        [0x20487BC],
        None,
        "Returns the current value of NOTIFY_NOTE.\n\nreturn: bool",
    )

    SetNotifyNote = Symbol(
        [0x487CC], [0x20487CC], None, "Sets NOTIFY_NOTE to the given value.\n\nr0: bool"
    )

    InitMainTeamAfterQuiz = Symbol(
        [0x48AE0],
        [0x2048AE0],
        None,
        (
            "Implements SPECIAL_PROC_INIT_MAIN_TEAM_AFTER_QUIZ (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    ScriptSpecialProcess0x3 = Symbol(
        [0x48D28],
        [0x2048D28],
        None,
        "Implements SPECIAL_PROC_0x3 (see ScriptSpecialProcessCall).\n\nNo params.",
    )

    ScriptSpecialProcess0x4 = Symbol(
        [0x48DA0],
        [0x2048DA0],
        None,
        "Implements SPECIAL_PROC_0x4 (see ScriptSpecialProcessCall).\n\nNo params.",
    )

    ReadStringSave = Symbol(
        [0x48ED0],
        [0x2048ED0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer",
    )

    CheckStringSave = Symbol(
        [0x48EEC],
        [0x2048EEC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nreturn: bool",
    )

    WriteSaveFile = Symbol(
        [0x49190],
        [0x2049190],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: save_info\nr1:"
            " buffer\nr2: size\nreturn: status code"
        ),
    )

    ReadSaveFile = Symbol(
        [0x491EC],
        [0x20491EC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: save_info\nr1:"
            " buffer\nr2: size\nreturn: status code"
        ),
    )

    CalcChecksum = Symbol(
        [0x49240],
        [0x2049240],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nr1: size",
    )

    CheckChecksum = Symbol(
        [0x49268],
        [0x2049268],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nr1:"
            " size\nreturn: check_ok"
        ),
    )

    NoteSaveBase = Symbol(
        [0x492A0],
        [0x20492A0],
        None,
        (
            "Probably related to saving or quicksaving?\n\nThis function prints the"
            " debug message 'NoteSave Base %d %d' with some values. It's also the only"
            " place where GetRngSeed is called.\n\nr0: Irdkwia's notes: state"
            " ID\nothers: ?\nreturn: status code"
        ),
    )

    WriteQuickSaveInfo = Symbol(
        [0x49564],
        [0x2049564],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nr1: size",
    )

    ReadSaveHeader = Symbol(
        [0x49588], [0x2049588], None, "Note: unverified, ported from Irdkwia's notes"
    )

    NoteLoadBase = Symbol(
        [0x496A8],
        [0x20496A8],
        None,
        (
            "Probably related to loading a save file or quicksave?\n\nThis function"
            " prints the debug message 'NoteLoad Base %d' with some value. It's also"
            " the only place where SetRngSeed is called.\n\nreturn: status code"
        ),
    )

    ReadQuickSaveInfo = Symbol(
        [0x49960],
        [0x2049960],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nr1:"
            " size\nreturn: status code"
        ),
    )

    GetGameMode = Symbol(
        [0x4B2F8],
        [0x204B2F8],
        None,
        "Gets the value of GAME_MODE.\n\nreturn: game mode",
    )

    InitScriptVariableValues = Symbol(
        [0x4B384],
        [0x204B384],
        None,
        (
            "Initialize the script variable values table (SCRIPT_VARS_VALUES).\n\nThe"
            " whole table is first zero-initialized. Then, all script variable values"
            " are first initialized to their defaults, after which some of them are"
            " overwritten with other hard-coded values.\n\nNo params."
        ),
    )

    InitEventFlagScriptVars = Symbol(
        [0x4B63C],
        [0x204B63C],
        None,
        (
            "Initializes an assortment of event flag script variables (see the code for"
            " an exhaustive list).\n\nNo params."
        ),
    )

    ZinitScriptVariable = Symbol(
        [0x4B76C],
        [0x204B76C],
        None,
        (
            "Zero-initialize the values of the given script variable.\n\nr0: pointer to"
            " the local variable table (only needed if id >= VAR_LOCAL0)\nr1: script"
            " variable ID"
        ),
    )

    LoadScriptVariableRaw = Symbol(
        [0x4B7D4],
        [0x204B7D4],
        None,
        (
            "Loads a script variable descriptor for a given ID.\n\nr0: [output] script"
            " variable descriptor pointer\nr1: pointer to the local variable table"
            " (doesn't need to be valid; just controls the output value pointer)\nr2:"
            " script variable ID"
        ),
    )

    LoadScriptVariableValue = Symbol(
        [0x4B824],
        [0x204B824],
        None,
        (
            "Loads the value of a script variable.\n\nr0: pointer to the local variable"
            " table (only needed if id >= VAR_LOCAL0)\nr1: script variable ID\nreturn:"
            " value"
        ),
    )

    LoadScriptVariableValueAtIndex = Symbol(
        [0x4B9B0],
        [0x204B9B0],
        None,
        (
            "Loads the value of a script variable at some index (for script variables"
            " that are arrays).\n\nr0: pointer to the local variable table (only needed"
            " if id >= VAR_LOCAL0)\nr1: script variable ID\nr2: value index for the"
            " given script var\nreturn: value"
        ),
    )

    SaveScriptVariableValue = Symbol(
        [0x4BB58],
        [0x204BB58],
        None,
        (
            "Saves the given value to a script variable.\n\nr0: pointer to local"
            " variable table (only needed if id >= VAR_LOCAL0)\nr1: script variable"
            " ID\nr2: value to save"
        ),
    )

    SaveScriptVariableValueAtIndex = Symbol(
        [0x4BCC0],
        [0x204BCC0],
        None,
        (
            "Saves the given value to a script variable at some index (for script"
            " variables that are arrays).\n\nr0: pointer to local variable table (only"
            " needed if id >= VAR_LOCAL0)\nr1: script variable ID\nr2: value index for"
            " the given script var\nr3: value to save"
        ),
    )

    LoadScriptVariableValueSum = Symbol(
        [0x4BE38],
        [0x204BE38],
        None,
        (
            "Loads the sum of all values of a given script variable (for script"
            " variables that are arrays).\n\nr0: pointer to the local variable table"
            " (only needed if id >= VAR_LOCAL0)\nr1: script variable ID\nreturn: sum of"
            " values"
        ),
    )

    LoadScriptVariableValueBytes = Symbol(
        [0x4BE9C],
        [0x204BE9C],
        None,
        (
            "Loads some number of bytes from the value of a given script"
            " variable.\n\nr0: script variable ID\nr1: [output] script variable value"
            " bytes\nr2: number of bytes to load"
        ),
    )

    SaveScriptVariableValueBytes = Symbol(
        [0x4BF04],
        [0x204BF04],
        None,
        (
            "Saves some number of bytes to the given script variable.\n\nr0: script"
            " variable ID\nr1: bytes to save\nr2: number of bytes"
        ),
    )

    ScriptVariablesEqual = Symbol(
        [0x4BF50],
        [0x204BF50],
        None,
        (
            "Checks if two script variables have equal values. For arrays, compares"
            " elementwise for the length of the first variable.\n\nr0: pointer to the"
            " local variable table (only needed if id >= VAR_LOCAL0)\nr1: script"
            " variable ID 1\nr2: script variable ID 2\nreturn: true if values are"
            " equal, false otherwise"
        ),
    )

    EventFlagBackup = Symbol(
        [0x4C51C],
        [0x204C51C],
        None,
        (
            "Saves event flag script variables (see the code for an exhaustive list) to"
            " their respective BACKUP script variables, but only in certain game"
            " modes.\n\nThis function prints the debug string 'EventFlag BackupGameMode"
            " %d' with the game mode.\n\nNo params."
        ),
    )

    DumpScriptVariableValues = Symbol(
        [0x4C740],
        [0x204C740],
        None,
        (
            "Runs EventFlagBackup, then copies the script variable values table"
            " (SCRIPT_VARS_VALUES) to the given pointer.\n\nr0: destination pointer for"
            " the data dump\nreturn: always 1"
        ),
    )

    RestoreScriptVariableValues = Symbol(
        [0x4C768],
        [0x204C768],
        None,
        (
            "Restores the script variable values table (SCRIPT_VARS_VALUES) with the"
            " given data. The source data is assumed to be exactly 1024 bytes in"
            " length.\n\nIrdkwia's notes: CheckCorrectVersion\n\nr0: raw data to copy"
            " to the values table\nreturn: whether the restored value for VAR_VERSION"
            " is equal to its default value"
        ),
    )

    InitScenarioScriptVars = Symbol(
        [0x4C7C0],
        [0x204C7C0],
        None,
        (
            "Initializes most of the SCENARIO_* script variables (except"
            " SCENARIO_TALK_BIT_FLAG for some reason). Also initializes the"
            " PLAY_OLD_GAME variable.\n\nNo params."
        ),
    )

    SetScenarioScriptVar = Symbol(
        [0x4C950],
        [0x204C950],
        None,
        (
            "Sets the given SCENARIO_* script variable with a given pair of values"
            " [val0, val1].\n\nIn the special case when the ID is VAR_SCENARIO_MAIN,"
            " and the set value is different from the old one, the REQUEST_CLEAR_COUNT"
            " script variable will be set to 0.\n\nr0: script variable ID\nr1:"
            " val0\nr2: val1"
        ),
    )

    GetSpecialEpisodeType = Symbol(
        [0x4CC24],
        [0x204CC24],
        None,
        (
            "Gets the special episode type from the SPECIAL_EPISODE_TYPE script"
            " variable.\n\nreturn: special episode type"
        ),
    )

    HasPlayedOldGame = Symbol(
        [0x4CDA8],
        [0x204CDA8],
        None,
        "Returns the value of the VAR_PLAY_OLD_GAME script variable.\n\nreturn: bool",
    )

    GetPerformanceFlagWithChecks = Symbol(
        [0x4CDCC],
        [0x204CDCC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: flag_id\nreturn: ?",
    )

    GetScenarioBalance = Symbol(
        [0x4CECC],
        [0x204CECC],
        None,
        (
            "Returns the current SCENARIO_BALANCE value.\n\nThe exact value returned"
            " depends on multiple factors:\n- If the first special episode is active,"
            " returns 1\n- If a different special episode is active, returns 3\n- If"
            " the SCENARIO_BALANCE_DEBUG variable is >= 0, returns its value\n- In all"
            " other cases, the value of the SCENARIO_BALANCE_FLAG variable is"
            " returned\n\nreturn: Current SCENARIO_BALANCE value."
        ),
    )

    ScenarioFlagBackup = Symbol(
        [0x4CFF0],
        [0x204CFF0],
        None,
        (
            "Saves scenario flag script variables (SCENARIO_SELECT,"
            " SCENARIO_MAIN_BIT_FLAG) to their respective BACKUP script variables, but"
            " only in certain game modes.\n\nThis function prints the debug string"
            " 'ScenarioFlag BackupGameMode %d' with the game mode.\n\nNo params."
        ),
    )

    InitWorldMapScriptVars = Symbol(
        [0x4D0C0],
        [0x204D0C0],
        None,
        (
            "Initializes the WORLD_MAP_* script variable values (IDs 0x55-0x57).\n\nNo"
            " params."
        ),
    )

    InitDungeonListScriptVars = Symbol(
        [0x4D1C8],
        [0x204D1C8],
        None,
        (
            "Initializes the DUNGEON_*_LIST script variable values (IDs"
            " 0x4f-0x54).\n\nNo params."
        ),
    )

    SetDungeonConquest = Symbol(
        [0x4D270],
        [0x204D270],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nr1:"
            " bit_value"
        ),
    )

    CheckDungeonOpen = Symbol(
        [0x4D2D4],
        [0x204D2D4],
        None,
        (
            "Related to dungeon open list\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: dungeon ID\nreturn: status code?"
        ),
    )

    GlobalProgressAlloc = Symbol(
        [0x4D440],
        [0x204D440],
        None,
        (
            "Allocates a new global progress struct.\n\nThis updates the global pointer"
            " and returns a copy of that pointer.\n\nreturn: pointer to a newly"
            " allocated global progress struct"
        ),
    )

    ResetGlobalProgress = Symbol(
        [0x4D468],
        [0x204D468],
        None,
        "Zero-initializes the global progress struct.\n\nNo params.",
    )

    SetMonsterFlag1 = Symbol(
        [0x4D484],
        [0x204D484],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID",
    )

    GetMonsterFlag1 = Symbol(
        [0x4D4C0],
        [0x204D4C0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn: ?",
    )

    SetMonsterFlag2 = Symbol(
        [0x4D4FC],
        [0x204D4FC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID",
    )

    HasMonsterBeenAttackedInDungeons = Symbol(
        [0x4D540],
        [0x204D540],
        None,
        (
            "Checks whether the specified monster has been attacked by the player at"
            " some point in their adventure during an exploration.\n\nThe check is"
            " performed using the result of passing the ID to FemaleToMaleForm.\n\nr0:"
            " Monster ID\nreturn: True if the specified mosnter (after converting its"
            " ID through FemaleToMaleForm) has been attacked by the player before,"
            " false otherwise."
        ),
    )

    SetDungeonTipShown = Symbol(
        [0x4D588],
        [0x204D588],
        None,
        "Marks a dungeon tip as already shown to the player\n\nr0: Dungeon tip ID",
    )

    GetDungeonTipShown = Symbol(
        [0x4D5C8],
        [0x204D5C8],
        None,
        (
            "Checks if a dungeon tip has already been shown before or not.\n\nr0:"
            " Dungeon tip ID\nreturn: True if the tip has been shown before, false"
            " otherwise."
        ),
    )

    SetMaxReachedFloor = Symbol(
        [0x4D614],
        [0x204D614],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nr1: max"
            " floor"
        ),
    )

    GetMaxReachedFloor = Symbol(
        [0x4D630],
        [0x204D630],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn:"
            " max floor"
        ),
    )

    IncrementNbAdventures = Symbol(
        [0x4D650],
        [0x204D650],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GetNbAdventures = Symbol(
        [0x4D684],
        [0x204D684],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: # adventures",
    )

    CanMonsterSpawn = Symbol(
        [0x4D698],
        [0x204D698],
        None,
        (
            "Always returns true.\n\nThis function seems to be a debug switch that the"
            " developers may have used to disable the random enemy spawn. \nIf it"
            " returned false, the call to SpawnMonster inside"
            " TrySpawnMonsterAndTickSpawnCounter would not be executed.\n\nr0: monster"
            " ID\nreturn: bool (always true)"
        ),
    )

    IncrementExclusiveMonsterCounts = Symbol(
        [0x4D6A0],
        [0x204D6A0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID",
    )

    CopyProgressInfoTo = Symbol(
        [0x4D6F8],
        [0x204D6F8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: write_info\nothers: ?",
    )

    CopyProgressInfoFromScratchTo = Symbol(
        [0x4D880],
        [0x204D880],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: start_address\nr1:"
            " total_length\nreturn: ?"
        ),
    )

    CopyProgressInfoFrom = Symbol(
        [0x4D8B8],
        [0x204D8B8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info",
    )

    CopyProgressInfoFromScratchFrom = Symbol(
        [0x4DA80],
        [0x204DA80],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: start_address\nr1:"
            " total_length"
        ),
    )

    SetPortraitMonsterId = Symbol(
        [0x4DB0C],
        [0x204DB0C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: portrait_ptr\nr1:"
            " monster ID"
        ),
    )

    SetPortraitExpressionId = Symbol(
        [0x4DB2C],
        [0x204DB2C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: portrait_ptr\nr1:"
            " expression_id"
        ),
    )

    SetPortraitUnknownAttr = Symbol(
        [0x4DB3C],
        [0x204DB3C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: portrait_ptr\nr1: attr",
    )

    SetPortraitAttrStruct = Symbol(
        [0x4DB80],
        [0x204DB80],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: portrait_ptr\nr1:"
            " attr_ptr"
        ),
    )

    LoadPortrait = Symbol(
        [0x4DBF4],
        [0x204DBF4],
        None,
        (
            "If buffer_portrait is null, it only checks if it exists\n\nNote:"
            " unverified, ported from Irdkwia's notes\n\nr0: portrait_ptr\nr1:"
            " buffer_portrait\nreturn: exists"
        ),
    )

    GetNbFloors = Symbol(
        [0x4F8B4],
        [0x204F8B4],
        None,
        (
            "Returns the number of floors of the given dungeon.\n\nThe result is"
            " hardcoded for certain dungeons, such as dojo mazes.\n\nr0: Dungeon"
            " ID\nreturn: Number of floors"
        ),
    )

    GetNbFloorsPlusOne = Symbol(
        [0x4F8EC],
        [0x204F8EC],
        None,
        (
            "Returns the number of floors of the given dungeon + 1.\n\nr0: Dungeon"
            " ID\nreturn: Number of floors + 1"
        ),
    )

    GetDungeonGroup = Symbol(
        [0x4F900],
        [0x204F900],
        None,
        (
            "Returns the dungeon group associated to the given dungeon.\n\nFor IDs"
            " greater or equal to dungeon_id::DUNGEON_NORMAL_FLY_MAZE, returns"
            " dungeon_group_id::DGROUP_MAROWAK_DOJO.\n\nr0: Dungeon ID\nreturn:"
            " Group ID"
        ),
    )

    GetNbPrecedingFloors = Symbol(
        [0x4F918],
        [0x204F918],
        None,
        (
            "Given a dungeon ID, returns the total amount of floors summed by all the"
            " previous dungeons in its group.\n\nThe value is normally pulled from"
            " dungeon_data_list_entry::n_preceding_floors_group, except for dungeons"
            " with an ID >= dungeon_id::DUNGEON_NORMAL_FLY_MAZE, for which this"
            " function always returns 0.\n\nr0: Dungeon ID\nreturn: Number of preceding"
            " floors of the dungeon"
        ),
    )

    GetNbFloorsDungeonGroup = Symbol(
        [0x4F930],
        [0x204F930],
        None,
        (
            "Returns the total amount of floors among all the dungeons in the dungeon"
            " group of the specified dungeon.\n\nr0: Dungeon ID\nreturn: Total number"
            " of floors in the group of the specified dungeon"
        ),
    )

    DungeonFloorToGroupFloor = Symbol(
        [0x4F984],
        [0x204F984],
        None,
        (
            "Given a dungeon ID and a floor number, returns a struct with the"
            " corresponding dungeon group and floor number in that group.\n\nThe"
            " function normally uses the data in mappa_s.bin to calculate the result,"
            " but there's some dungeons (such as dojo mazes) that have hardcoded return"
            " values.\n\nIrdkwia's notes:\n  [r1]: dungeon_id\n  [r1+1]:"
            " dungeon_floor_id\n  [r0]: group_id\n  [r0+1]: group_floor_id\n\nr0:"
            " (output) Struct containing the dungeon group and floor group\nr1: Struct"
            " containing the dungeon ID and floor number"
        ),
    )

    GetGroundNameId = Symbol(
        [0x4FC90], [0x204FC90], None, "Note: unverified, ported from Irdkwia's notes"
    )

    SetAdventureLogStructLocation = Symbol(
        [0x4FD5C],
        [0x204FD5C],
        None,
        (
            "Sets the location of the adventure log struct in memory.\n\nSets it in a"
            " static memory location (At 0x22AB69C [US], 0x22ABFDC [EU], 0x22ACE58"
            " [JP])\n\nNo params."
        ),
    )

    SetAdventureLogDungeonFloor = Symbol(
        [0x4FD74],
        [0x204FD74],
        None,
        "Sets the current dungeon floor pair.\n\nr0: struct dungeon_floor_pair",
    )

    GetAdventureLogDungeonFloor = Symbol(
        [0x4FD94],
        [0x204FD94],
        None,
        "Gets the current dungeon floor pair.\n\nreturn: struct dungeon_floor_pair",
    )

    ClearAdventureLogStruct = Symbol(
        [0x4FDA8],
        [0x204FDA8],
        None,
        "Clears the adventure log structure.\n\nNo params.",
    )

    SetAdventureLogCompleted = Symbol(
        [0x4FED4],
        [0x204FED4],
        None,
        "Marks one of the adventure log entry as completed.\n\nr0: entry ID",
    )

    IsAdventureLogNotEmpty = Symbol(
        [0x4FEFC],
        [0x204FEFC],
        None,
        (
            "Checks if at least one of the adventure log entries is"
            " completed.\n\nreturn: bool"
        ),
    )

    GetAdventureLogCompleted = Symbol(
        [0x4FF34],
        [0x204FF34],
        None,
        "Checks if one adventure log entry is completed.\n\nr0: entry ID\nreturn: bool",
    )

    IncrementNbDungeonsCleared = Symbol(
        [0x4FF60],
        [0x204FF60],
        None,
        (
            "Increments by 1 the number of dungeons cleared.\n\nImplements"
            " SPECIAL_PROC_0x3A (see ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    GetNbDungeonsCleared = Symbol(
        [0x4FFA4],
        [0x204FFA4],
        None,
        (
            "Gets the number of dungeons cleared.\n\nreturn: the number of dungeons"
            " cleared"
        ),
    )

    IncrementNbFriendRescues = Symbol(
        [0x4FFB8],
        [0x204FFB8],
        None,
        "Increments by 1 the number of successful friend rescues.\n\nNo params.",
    )

    GetNbFriendRescues = Symbol(
        [0x50000],
        [0x2050000],
        None,
        (
            "Gets the number of successful friend rescues.\n\nreturn: the number of"
            " successful friend rescues"
        ),
    )

    IncrementNbEvolutions = Symbol(
        [0x50014],
        [0x2050014],
        None,
        "Increments by 1 the number of evolutions.\n\nNo params.",
    )

    GetNbEvolutions = Symbol(
        [0x5005C],
        [0x205005C],
        None,
        "Gets the number of evolutions.\n\nreturn: the number of evolutions",
    )

    IncrementNbSteals = Symbol(
        [0x50070],
        [0x2050070],
        None,
        (
            "Leftover from Time & Darkness. Does not do anything.\n\nCalls to this"
            " matches the ones for incrementing the number of successful steals in Time"
            " & Darkness.\n\nNo params."
        ),
    )

    IncrementNbEggsHatched = Symbol(
        [0x50074],
        [0x2050074],
        None,
        "Increments by 1 the number of eggs hatched.\n\nNo params.",
    )

    GetNbEggsHatched = Symbol(
        [0x500B0],
        [0x20500B0],
        None,
        "Gets the number of eggs hatched.\n\nreturn: the number of eggs hatched",
    )

    GetNbPokemonJoined = Symbol(
        [0x500C4],
        [0x20500C4],
        None,
        (
            "Gets the number of different pokémon that joined.\n\nreturn: the number of"
            " different pokémon that joined"
        ),
    )

    GetNbMovesLearned = Symbol(
        [0x500D8],
        [0x20500D8],
        None,
        (
            "Gets the number of different moves learned.\n\nreturn: the number of"
            " different moves learned"
        ),
    )

    SetVictoriesOnOneFloor = Symbol(
        [0x500EC],
        [0x20500EC],
        None,
        "Sets the record of victories on one floor.\n\nr0: the new record of victories",
    )

    GetVictoriesOnOneFloor = Symbol(
        [0x50120],
        [0x2050120],
        None,
        "Gets the record of victories on one floor.\n\nreturn: the record of victories",
    )

    SetPokemonJoined = Symbol(
        [0x50134], [0x2050134], None, "Marks one pokémon as joined.\n\nr0: monster ID"
    )

    SetPokemonBattled = Symbol(
        [0x50190], [0x2050190], None, "Marks one pokémon as battled.\n\nr0: monster ID"
    )

    GetNbPokemonBattled = Symbol(
        [0x501EC],
        [0x20501EC],
        None,
        (
            "Gets the number of different pokémon that battled against you.\n\nreturn:"
            " the number of different pokémon that battled against you"
        ),
    )

    IncrementNbBigTreasureWins = Symbol(
        [0x50200],
        [0x2050200],
        None,
        (
            "Increments by 1 the number of big treasure wins.\n\nImplements"
            " SPECIAL_PROC_0x3B (see ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    SetNbBigTreasureWins = Symbol(
        [0x50220],
        [0x2050220],
        None,
        (
            "Sets the number of big treasure wins.\n\nr0: the new number of big"
            " treasure wins"
        ),
    )

    GetNbBigTreasureWins = Symbol(
        [0x50258],
        [0x2050258],
        None,
        (
            "Gets the number of big treasure wins.\n\nreturn: the number of big"
            " treasure wins"
        ),
    )

    SetNbRecycled = Symbol(
        [0x5026C],
        [0x205026C],
        None,
        "Sets the number of items recycled.\n\nr0: the new number of items recycled",
    )

    GetNbRecycled = Symbol(
        [0x502A4],
        [0x20502A4],
        None,
        "Gets the number of items recycled.\n\nreturn: the number of items recycled",
    )

    IncrementNbSkyGiftsSent = Symbol(
        [0x502B8],
        [0x20502B8],
        None,
        (
            "Increments by 1 the number of sky gifts sent.\n\nImplements"
            " SPECIAL_PROC_SEND_SKY_GIFT_TO_GUILDMASTER (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    SetNbSkyGiftsSent = Symbol(
        [0x502D8],
        [0x20502D8],
        None,
        "Sets the number of Sky Gifts sent.\n\nreturn: the number of Sky Gifts sent",
    )

    GetNbSkyGiftsSent = Symbol(
        [0x50310],
        [0x2050310],
        None,
        "Gets the number of Sky Gifts sent.\n\nreturn: the number of Sky Gifts sent",
    )

    ComputeSpecialCounters = Symbol(
        [0x50324],
        [0x2050324],
        None,
        (
            "Computes the counters from the bit fields in the adventure log, as they"
            " are not updated automatically when bit fields are altered.\n\nAffects"
            " GetNbPokemonJoined, GetNbMovesLearned, GetNbPokemonBattled and"
            " GetNbItemAcquired.\n\nNo params."
        ),
    )

    RecruitSpecialPokemonLog = Symbol(
        [0x5057C],
        [0x205057C],
        None,
        (
            "Marks a specified special pokémon as recruited in the adventure"
            " log.\n\nIrdkwia's notes: Useless in Sky\n\nr0: monster ID"
        ),
    )

    IncrementNbFainted = Symbol(
        [0x505E8],
        [0x20505E8],
        None,
        "Increments by 1 the number of times you fainted.\n\nNo params.",
    )

    GetNbFainted = Symbol(
        [0x50624],
        [0x2050624],
        None,
        (
            "Gets the number of times you fainted.\n\nreturn: the number of times you"
            " fainted"
        ),
    )

    SetItemAcquired = Symbol(
        [0x50638], [0x2050638], None, "Marks one specific item as acquired.\n\nr0: item"
    )

    GetNbItemAcquired = Symbol(
        [0x50704],
        [0x2050704],
        None,
        "Gets the number of items acquired.\n\nreturn: the number of items acquired",
    )

    SetChallengeLetterCleared = Symbol(
        [0x50758],
        [0x2050758],
        None,
        "Sets a challenge letter as cleared.\n\nr0: challenge ID",
    )

    GetSentryDutyGamePoints = Symbol(
        [0x507DC],
        [0x20507DC],
        None,
        (
            "Gets the points for the associated rank in the footprints minigame.\n\nr0:"
            " the rank (range 0-4, 1st to 5th)\nreturn: points"
        ),
    )

    SetSentryDutyGamePoints = Symbol(
        [0x507F4],
        [0x20507F4],
        None,
        (
            "Sets a new record in the footprints minigame.\n\nr0: points\nreturn: the"
            " rank (range 0-4, 1st to 5th; -1 if out of ranking)"
        ),
    )

    CopyLogTo = Symbol(
        [0x50884],
        [0x2050884],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: write_info",
    )

    CopyLogFrom = Symbol(
        [0x50A70],
        [0x2050A70],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info",
    )

    GetAbilityString = Symbol(
        [0x50C54],
        [0x2050C54],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nr1: ability ID",
    )

    GetAbilityDescStringId = Symbol(
        [0x50C74],
        [0x2050C74],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ability ID\nreturn:"
            " string ID"
        ),
    )

    GetTypeStringId = Symbol(
        [0x50C88],
        [0x2050C88],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: type ID\nreturn:"
            " string ID"
        ),
    )

    CopyBitsTo = Symbol(
        [0x50CF8],
        [0x2050CF8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: write_info\nr1:"
            " buffer_write\nr2: nb_bits"
        ),
    )

    CopyBitsFrom = Symbol(
        [0x50D78],
        [0x2050D78],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info\nr1:"
            " buffer_read\nr2: nb_bits"
        ),
    )

    StoreDefaultTeamName = Symbol(
        [0x50E04],
        [0x2050E04],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GetTeamNameCheck = Symbol(
        [0x50E48],
        [0x2050E48],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer",
    )

    GetTeamName = Symbol(
        [0x50EB4],
        [0x2050EB4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer",
    )

    SetTeamName = Symbol(
        [0x50ECC],
        [0x2050ECC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer",
    )

    SubFixedPoint = Symbol(
        [0x51248],
        [0x2051248],
        None,
        (
            "Compute the subtraction of two decimal fixed-point numbers (16 fraction"
            " bits).\n\nNumbers are in the format {16-bit integer part, 16-bit"
            " thousandths}, where the integer part is the lower word. Probably used"
            " primarily for belly.\n\nr0: number\nr1: decrement\nreturn: max(number -"
            " decrement, 0)"
        ),
    )

    BinToDecFixedPoint = Symbol(
        [0x51358],
        [0x2051358],
        None,
        (
            "Convert a binary fixed-point number (16 fraction bits) to the decimal"
            " fixed-point number (16 fraction bits) used for belly calculations."
            " Thousandths are floored.\n\nIf <data> holds the raw binary data, a binary"
            " fixed-point number (16 fraction bits) has the value ((unsigned)data) *"
            " 2^-16), and the decimal fixed-point number (16 fraction bits) used for"
            " belly has the value (data & 0xffff) + (data >> 16)/1000.\n\nr0: pointer"
            " p, where ((const unsigned *)p)[1] is the fractional number in binary"
            " fixed-point format to convert\nreturn: fractional number in decimal"
            " fixed-point format"
        ),
    )

    CeilFixedPoint = Symbol(
        [0x5139C],
        [0x205139C],
        None,
        (
            "Compute the ceiling of a decimal fixed-point number (16 fraction"
            " bits).\n\nNumbers are in the format {16-bit integer part, 16-bit"
            " thousandths}, where the integer part is the lower word. Probably used"
            " primarily for belly.\n\nr0: number\nreturn: ceil(number)"
        ),
    )

    DungeonGoesUp = Symbol(
        [0x515C0],
        [0x20515C0],
        None,
        (
            "Returns whether the specified dungeon is considered as going upward or"
            " not\n\nr0: dungeon id\nreturn: bool"
        ),
    )

    GetTurnLimit = Symbol(
        [0x515E8],
        [0x20515E8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn:"
            " turn limit"
        ),
    )

    DoesNotSaveWhenEntering = Symbol(
        [0x51600],
        [0x2051600],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    TreasureBoxDropsEnabled = Symbol(
        [0x51628],
        [0x2051628],
        None,
        (
            "Checks if enemy Treasure Box drops are enabled in the dungeon.\n\nr0:"
            " dungeon ID\nreturn: bool"
        ),
    )

    IsLevelResetDungeon = Symbol(
        [0x51650],
        [0x2051650],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    GetMaxItemsAllowed = Symbol(
        [0x51678],
        [0x2051678],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn:"
            " max items allowed"
        ),
    )

    IsMoneyAllowed = Symbol(
        [0x51690],
        [0x2051690],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    GetMaxRescueAttempts = Symbol(
        [0x516B8],
        [0x20516B8],
        None,
        (
            "Returns the maximum rescue attempts allowed in the specified"
            " dungeon.\n\nr0: dungeon id\nreturn: Max rescue attempts, or -1 if rescues"
            " are disabled."
        ),
    )

    IsRecruitingAllowed = Symbol(
        [0x516D0],
        [0x20516D0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    GetLeaderChangeFlag = Symbol(
        [0x516F8],
        [0x20516F8],
        None,
        (
            "Returns true if the flag that allows changing leaders is set in the"
            " restrictions of the specified dungeon\n\nr0: dungeon id\nreturn: True if"
            " the restrictions of the current dungeon allow changing leaders, false"
            " otherwise."
        ),
    )

    GetUnknownDungeonOption = Symbol(
        [0x51720],
        [0x2051720],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: ?",
    )

    CanEnemyEvolve = Symbol(
        [0x51738],
        [0x2051738],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    GetMaxMembersAllowed = Symbol(
        [0x51760],
        [0x2051760],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn:"
            " max members allowed"
        ),
    )

    IsIqEnabled = Symbol(
        [0x51778],
        [0x2051778],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    IsTrapInvisibleWhenAttacking = Symbol(
        [0x517A0],
        [0x20517A0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    JoinedAtRangeCheck = Symbol(
        [0x517C8],
        [0x20517C8],
        None,
        (
            "Returns whether a certain joined_at field value is between"
            " dungeon_id::DUNGEON_JOINED_AT_BIDOOF and"
            " dungeon_id::DUNGEON_DUMMY_0xE3.\n\nIrdkwia's notes:"
            " IsSupportPokemon\n\nr0: joined_at id\nreturn: bool"
        ),
    )

    IsDojoDungeon = Symbol(
        [0x517E8],
        [0x20517E8],
        None,
        (
            "Checks if the given dungeon is a Marowak Dojo dungeon.\n\nr0: dungeon"
            " ID\nreturn: bool"
        ),
    )

    IsFutureDungeon = Symbol(
        [0x51804],
        [0x2051804],
        None,
        (
            "Checks if the given dungeon is a dungeon in the future arc of the main"
            " story.\n\nr0: dungeon ID\nreturn: bool"
        ),
    )

    IsSpecialEpisodeDungeon = Symbol(
        [0x51820],
        [0x2051820],
        None,
        (
            "Checks if the given dungeon is a special episode dungeon.\n\nr0: dungeon"
            " ID\nreturn: bool"
        ),
    )

    RetrieveFromItemList1 = Symbol(
        [0x5183C],
        [0x205183C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon_info\nr1:"
            " ?\nreturn: ?"
        ),
    )

    IsForbiddenFloor = Symbol(
        [0x518A0],
        [0x20518A0],
        None,
        (
            "Related to missions floors forbidden\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: dungeon_info\nothers: ?\nreturn: bool"
        ),
    )

    Copy16BitsFrom = Symbol(
        [0x51924],
        [0x2051924],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info\nr1:"
            " buffer_read"
        ),
    )

    RetrieveFromItemList2 = Symbol(
        [0x519B4],
        [0x20519B4],
        None,
        (
            "Same as RetrieveFromItemList1, except there is one more"
            " comparison\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " dungeon_info"
        ),
    )

    IsInvalidForMission = Symbol(
        [0x51A14],
        [0x2051A14],
        None,
        (
            "It's a guess\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " dungeon_id\nreturn: bool"
        ),
    )

    IsExpEnabledInDungeon = Symbol(
        [0x51A54],
        [0x2051A54],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon_id\nreturn: bool",
    )

    IsSkyExclusiveDungeon = Symbol(
        [0x51A7C],
        [0x2051A7C],
        None,
        (
            "Also the dungeons where Giratina has its Origin Form\n\nNote: unverified,"
            " ported from Irdkwia's notes\n\nr0: dungeon_id\nreturn: bool"
        ),
    )

    JoinedAtRangeCheck2 = Symbol(
        [0x51A98],
        [0x2051A98],
        None,
        (
            "Returns whether a certain joined_at field value is equal to"
            " dungeon_id::DUNGEON_BEACH or is between dungeon_id::DUNGEON_DUMMY_0xEC"
            " and dungeon_id::DUNGEON_DUMMY_0xF0.\n\nIrdkwia's notes:"
            " IsSEPokemon\n\nr0: joined_at id\nreturn: bool"
        ),
    )

    GetBagCapacity = Symbol(
        [0x51B0C],
        [0x2051B0C],
        None,
        (
            "Returns the player's bag capacity for a given point in the game.\n\nr0:"
            " scenario_balance\nreturn: bag capacity"
        ),
    )

    GetBagCapacitySpecialEpisode = Symbol(
        [0x51B1C],
        [0x2051B1C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: se_type\nreturn: bag"
            " capacity"
        ),
    )

    GetRankUpEntry = Symbol(
        [0x51B2C],
        [0x2051B2C],
        None,
        (
            "Gets the rank up data for the specified rank.\n\nr0: rank index\nreturn:"
            " struct rankup_table_entry*"
        ),
    )

    GetBgRegionArea = Symbol(
        [0x521C4],
        [0x20521C4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: offset\nr1:"
            " subregion_id\nr2: region_id\nreturn: ?"
        ),
    )

    LoadMonsterMd = Symbol(
        [0x52690],
        [0x2052690],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GetNameRaw = Symbol(
        [0x526CC],
        [0x20526CC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dst_ptr\nr1: id",
    )

    GetName = Symbol(
        [0x52708],
        [0x2052708],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dst_ptr\nr1: id\nr2:"
            " color_id"
        ),
    )

    GetNameWithGender = Symbol(
        [0x52778],
        [0x2052778],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dst_ptr\nr1: id\nr2:"
            " color_id"
        ),
    )

    GetSpeciesString = Symbol(
        [0x52838],
        [0x2052838],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dst_ptr\nr1: id",
    )

    GetNameString = Symbol(
        [0x52A00],
        [0x2052A00],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: name",
    )

    GetSpriteIndex = Symbol(
        [0x52A24, 0x52A40, 0x52A5C],
        [0x2052A24, 0x2052A40, 0x2052A5C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: sprite index",
    )

    GetDexNumber = Symbol(
        [0x52A78],
        [0x2052A78],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: dex number",
    )

    GetCategoryString = Symbol(
        [0x52A94],
        [0x2052A94],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: category",
    )

    GetMonsterGender = Symbol(
        [0x52AE0],
        [0x2052AE0],
        None,
        (
            "Returns the gender field of a monster given its ID.\n\nr0: monster"
            " id\nreturn: monster gender"
        ),
    )

    GetBodySize = Symbol(
        [0x52AFC],
        [0x2052AFC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: body size",
    )

    GetSpriteSize = Symbol(
        [0x52B18],
        [0x2052B18],
        None,
        (
            "Returns the sprite size of the specified monster. If the size is between 1"
            " and 6, 6 will be returned.\n\nr0: monster id\nreturn: sprite size"
        ),
    )

    GetSpriteFileSize = Symbol(
        [0x52B54],
        [0x2052B54],
        None,
        (
            "Returns the sprite file size of the specified monster.\n\nr0: monster"
            " id\nreturn: sprite file size"
        ),
    )

    GetShadowSize = Symbol(
        [0x52B74],
        [0x2052B74],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: shadow size",
    )

    GetSpeedStatus = Symbol(
        [0x52B90],
        [0x2052B90],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: speed status",
    )

    GetMovementType = Symbol(
        [0x52BAC],
        [0x2052BAC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: movement"
            " type"
        ),
    )

    GetRegenSpeed = Symbol(
        [0x52BC8],
        [0x2052BC8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: regen speed",
    )

    GetCanMoveFlag = Symbol(
        [0x52BEC],
        [0x2052BEC],
        None,
        (
            "Returns the flag that determines if a monster can move in dungeons.\n\nr0:"
            " Monster ID\nreturn: 'Can move' flag"
        ),
    )

    GetChanceAsleep = Symbol(
        [0x52C18],
        [0x2052C18],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: chance"
            " asleep"
        ),
    )

    GetLowKickMultiplier = Symbol(
        [0x52C34],
        [0x2052C34],
        None,
        (
            "Gets the Low Kick (and Grass Knot) damage multiplier (i.e., weight) for"
            " the given species.\n\nr0: monster ID\nreturn: multiplier as a binary"
            " fixed-point number with 8 fraction bits."
        ),
    )

    GetSize = Symbol(
        [0x52C50],
        [0x2052C50],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: size",
    )

    GetBaseHp = Symbol(
        [0x52C6C],
        [0x2052C6C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: base HP",
    )

    CanThrowItems = Symbol(
        [0x52C88],
        [0x2052C88],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: bool",
    )

    CanEvolve = Symbol(
        [0x52CB4],
        [0x2052CB4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: bool",
    )

    GetMonsterPreEvolution = Symbol(
        [0x52CE0],
        [0x2052CE0],
        None,
        (
            "Returns the pre-evolution id of a monster given its ID.\n\nr0: monster"
            " id\nreturn: ID of the monster that evolves into the one specified in r0"
        ),
    )

    GetBaseOffensiveStat = Symbol(
        [0x52CFC],
        [0x2052CFC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nr1: stat"
            " index\nreturn: base attack/special attack stat"
        ),
    )

    GetBaseDefensiveStat = Symbol(
        [0x52D1C],
        [0x2052D1C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nr1: stat"
            " index\nreturn: base defense/special defense stat"
        ),
    )

    GetType = Symbol(
        [0x52D3C],
        [0x2052D3C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nr1: type index (0"
            " for primary type or 1 for secondary type)\nreturn: type"
        ),
    )

    GetAbility = Symbol(
        [0x52D5C],
        [0x2052D5C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nr1: ability index"
            " (0 for primary ability or 1 for secondary ability)\nreturn: ability"
        ),
    )

    GetRecruitRate2 = Symbol(
        [0x52D7C],
        [0x2052D7C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: recruit"
            " rate 2"
        ),
    )

    GetRecruitRate1 = Symbol(
        [0x52D98],
        [0x2052D98],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: recruit"
            " rate 1"
        ),
    )

    GetExp = Symbol(
        [0x52DB4],
        [0x2052DB4],
        None,
        (
            "Base Formula = ((Level-1)*ExpYield)//10+ExpYield\nNote: Defeating an enemy"
            " without using a move will divide this amount by 2\n\nNote: unverified,"
            " ported from Irdkwia's notes\n\nr0: id\nr1: level\nreturn: exp"
        ),
    )

    GetEvoParameters = Symbol(
        [0x52DE8],
        [0x2052DE8],
        None,
        (
            "Bx\nHas something to do with evolution\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: [output] struct_evo_param\nr1: id"
        ),
    )

    GetTreasureBoxChances = Symbol(
        [0x52E18],
        [0x2052E18],
        None,
        (
            "Has something to do with bytes 3C-3E\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: id\nr1: [output] struct_chances"
        ),
    )

    GetIqGroup = Symbol(
        [0x52E60],
        [0x2052E60],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: IQ group",
    )

    GetSpawnThreshold = Symbol(
        [0x52E7C],
        [0x2052E7C],
        None,
        (
            "Returns the spawn threshold of the given monster ID\n\nThe spawn threshold"
            " determines the minimum SCENARIO_BALANCE_FLAG value required by a monster"
            " to spawn in dungeons.\n\nr0: monster id\nreturn: Spawn threshold"
        ),
    )

    NeedsItemToSpawn = Symbol(
        [0x52E98],
        [0x2052E98],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: bool",
    )

    GetExclusiveItem = Symbol(
        [0x52EC4],
        [0x2052EC4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nr1: determines"
            " which exclusive item\nreturn: exclusive item"
        ),
    )

    GetFamilyIndex = Symbol(
        [0x52EF0],
        [0x2052EF0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: family index",
    )

    LoadM2nAndN2m = Symbol(
        [0x52F0C],
        [0x2052F0C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    IsNotNickname = Symbol(
        [0x5332C],
        [0x205332C],
        None,
        (
            "Checks if the string_buffer matches the name of the species\n\nNote:"
            " unverified, ported from Irdkwia's notes\n\nr0: string_buffer\nr1: monster"
            " ID\nreturn: bool"
        ),
    )

    GetLvlStats = Symbol(
        [0x53B18],
        [0x2053B18],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output] level"
            " stats\nr1: monster ID\nr2: level"
        ),
    )

    GetEvoFamily = Symbol(
        [0x5414C],
        [0x205414C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: monster_str\nr1:"
            " evo_family_str\nreturn: nb_family"
        ),
    )

    GetEvolutions = Symbol(
        [0x54204],
        [0x2054204],
        None,
        (
            "Returns a list of all the possible evolutions for a given monster"
            " id.\n\nr0: Monster id\nr1: [Output] Array that will hold the list of"
            " monster ids the specified monster can evolve into\nr2: True to skip the"
            " check that prevents returning monsters with a different sprite size than"
            " the current one\nr3: True to skip the check that prevents Shedinja from"
            " being counted as a potential evolution\nreturn: Number of possible"
            " evolutions for the specified monster id"
        ),
    )

    ShuffleHiddenPower = Symbol(
        [0x54344],
        [0x2054344],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dmons_addr",
    )

    GetBaseForm = Symbol(
        [0x543A0],
        [0x20543A0],
        None,
        (
            "Checks if the specified monster ID corresponds to any of the pokémon that"
            " have multiple forms and returns the ID of the base form if so. If it"
            " doesn't, the same ID is returned.\n\nSome of the pokémon included in the"
            " check are Castform, Unown, Deoxys, Cherrim, Shaymin, and Giratina\n\nr0:"
            " Monster ID\nreturn: ID of the base form of the specified monster, or the"
            " same if the specified monster doesn't have a base form."
        ),
    )

    GetBaseFormBurmyWormadamShellosGastrodonCherrim = Symbol(
        [0x545CC],
        [0x20545CC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: base form",
    )

    GetBaseFormCastformCherrimDeoxys = Symbol(
        [0x54714],
        [0x2054714],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: base form",
    )

    GetAllBaseForms = Symbol(
        [0x547E0],
        [0x20547E0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: base form",
    )

    GetDexNumberVeneer = Symbol(
        [0x547F0],
        [0x20547F0],
        None,
        (
            "Likely a linker-generated veneer for GetDexNumber.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " id\nreturn: dex number"
        ),
    )

    GetMonsterIdFromSpawnEntry = Symbol(
        [0x547FC],
        [0x20547FC],
        None,
        (
            "Returns the monster ID of the specified monster spawn entry\n\nr0: Pointer"
            " to the monster spawn entry\nreturn: monster_spawn_entry::id"
        ),
    )

    SetMonsterId = Symbol(
        [0x5481C],
        [0x205481C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: mons_spawn_str\nr1:"
            " monster ID"
        ),
    )

    SetMonsterLevelAndId = Symbol(
        [0x54824],
        [0x2054824],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: mons_spawn_str\nr1:"
            " level\nr2: monster ID"
        ),
    )

    GetMonsterLevelFromSpawnEntry = Symbol(
        [0x54834],
        [0x2054834],
        None,
        (
            "Returns the level of the specified monster spawn entry.\n\nr0: pointer to"
            " the monster spawn entry\nreturn: uint8_t"
        ),
    )

    GetMonsterGenderVeneer = Symbol(
        [0x54ADC],
        [0x2054ADC],
        None,
        (
            "Likely a linker-generated veneer for GetMonsterGender.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " monster id\nreturn: monster gender"
        ),
    )

    IsMonsterValid = Symbol(
        [0x54AE8],
        [0x2054AE8],
        None,
        "Checks if an monster ID is valid.\n\nr0: monster ID\nreturn: bool",
    )

    IsUnown = Symbol(
        [0x54E04],
        [0x2054E04],
        None,
        "Checks if a monster ID is an Unown.\n\nr0: monster ID\nreturn: bool",
    )

    IsShaymin = Symbol(
        [0x54E20],
        [0x2054E20],
        None,
        "Checks if a monster ID is a Shaymin form.\n\nr0: monster ID\nreturn: bool",
    )

    IsCastform = Symbol(
        [0x54E50],
        [0x2054E50],
        None,
        "Checks if a monster ID is a Castform form.\n\nr0: monster ID\nreturn: bool",
    )

    IsCherrim = Symbol(
        [0x54EA8],
        [0x2054EA8],
        None,
        "Checks if a monster ID is a Cherrim form.\n\nr0: monster ID\nreturn: bool",
    )

    IsDeoxys = Symbol(
        [0x54EF0],
        [0x2054EF0],
        None,
        "Checks if a monster ID is a Deoxys form.\n\nr0: monster ID\nreturn: bool",
    )

    GetSecondFormIfValid = Symbol(
        [0x54F20],
        [0x2054F20],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn:"
            " second form"
        ),
    )

    FemaleToMaleForm = Symbol(
        [0x54F5C],
        [0x2054F5C],
        None,
        (
            "Returns the ID of the first form of the specified monster if the specified"
            " ID corresponds to a secondary form with female gender and the first form"
            " has male gender. If those conditions don't meet, returns the same ID"
            " unchanged.\n\nr0: Monster ID\nreturn: ID of the male form of the monster"
            " if the requirements meet, same ID otherwise."
        ),
    )

    GetBaseFormCastformDeoxysCherrim = Symbol(
        [0x54FA0],
        [0x2054FA0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: base form",
    )

    BaseFormsEqual = Symbol(
        [0x55054],
        [0x2055054],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id1\nr1: id2\nreturn:"
            " if the base forms are the same"
        ),
    )

    DexNumbersEqual = Symbol(
        [0x55140],
        [0x2055140],
        None,
        (
            "Each Unown is considered as different\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: id1\nr1: id2\nreturn: bool"
        ),
    )

    GendersEqual = Symbol(
        [0x551C8],
        [0x20551C8],
        None,
        (
            "Checks if the genders for two monster IDs are equal.\n\nr0: id1\nr1:"
            " id2\nreturn: bool"
        ),
    )

    GendersEqualNotGenderless = Symbol(
        [0x551F4],
        [0x20551F4],
        None,
        (
            "Checks if the genders for two monster IDs are equal. Always returns false"
            " if either gender is GENDER_GENDERLESS.\n\nr0: id1\nr1: id2\nreturn: bool"
        ),
    )

    IsMonsterOnTeam = Symbol(
        [0x554C4],
        [0x20554C4],
        None,
        (
            "Checks if a given monster is on the exploration team (not necessarily the"
            " active party)?\n\nIrdkwia's notes:\n  recruit_strategy=0: strict"
            " equality\n  recruit_strategy=1: relative equality\n\nr0: monster ID\nr1:"
            " recruit_strategy\nreturn: bool"
        ),
    )

    GetNbRecruited = Symbol(
        [0x555F0],
        [0x20555F0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: recruit_str",
    )

    GetMember = Symbol(
        [0x55924],
        [0x2055924],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: member_idx\nreturn: ?",
    )

    GetHeroStrIdIfExists = Symbol(
        [0x559CC],
        [0x20559CC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    GetPartnerStrIdIfExists = Symbol(
        [0x559F8],
        [0x20559F8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    GetFirstTeamMemberStrIdIfExists = Symbol(
        [0x55A24],
        [0x2055A24],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    GetSecondTeamMemberStrIdIfExists = Symbol(
        [0x55A68],
        [0x2055A68],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    GetThirdTeamMemberStrIdIfExists = Symbol(
        [0x55AAC],
        [0x2055AAC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    GetHeroData = Symbol(
        [0x55AEC],
        [0x2055AEC],
        None,
        (
            "Returns the ground monster data of the hero (first slot in Chimecho"
            " Assembly)\n\nreturn: Monster data"
        ),
    )

    GetPartnerData = Symbol(
        [0x55B14],
        [0x2055B14],
        None,
        (
            "Returns the ground monster data of the partner (second slot in Chimecho"
            " Assembly)\n\nreturn: Monster data"
        ),
    )

    GetFirstTeamMemberData = Symbol(
        [0x55B40],
        [0x2055B40],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: Monster data",
    )

    GetSecondTeamMemberData = Symbol(
        [0x55B88],
        [0x2055B88],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: Monster data",
    )

    GetThirdTeamMemberData = Symbol(
        [0x55BD0],
        [0x2055BD0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: Monster data",
    )

    GetFirstEmptyRecruitSlot = Symbol(
        [0x55CE0],
        [0x2055CE0],
        None,
        (
            "Returns -1 if there is none\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: ?\nreturn: ?"
        ),
    )

    CheckTeamMemberField8 = Symbol(
        [0x565E0],
        [0x20565E0],
        None,
        (
            "Checks if a value obtained from team_member::field_0x8 is equal to certain"
            " values.\n\nThis is known to return true for some or all of the guest"
            " monsters.\n\nr0: Value read from team_member::field_0x8\nreturn: True if"
            " the value is equal to 0x55AA or 0x5AA5"
        ),
    )

    IsMonsterIdInNormalRange = Symbol(
        [0x56610],
        [0x2056610],
        None,
        (
            "Checks if a monster ID is in the range [0, 554], meaning it's before the"
            " special story monster IDs and secondary gender IDs.\n\nr0: monster"
            " ID\nreturn: bool"
        ),
    )

    GetTeamMemberData = Symbol(
        [0x56708],
        [0x2056708],
        None,
        (
            "Returns a struct containing information about a team member.\n\nIrdkwia's"
            " notes (note the discrepancy): GetEquivalentTeamID\n  r0: str_id\n "
            " return: team_id, -1 if not in team\n\nr0: Index\nreturn: Pointer to"
            " struct containing team member information"
        ),
    )

    GetTeamMember = Symbol(
        [0x56738],
        [0x2056738],
        None,
        (
            "Null pointer if -1\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " team_id\nreturn: team member"
        ),
    )

    SetTeamSetupHeroAndPartnerOnly = Symbol(
        [0x56D48],
        [0x2056D48],
        None,
        (
            "Implements SPECIAL_PROC_SET_TEAM_SETUP_HERO_AND_PARTNER_ONLY (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    SetTeamSetupHeroOnly = Symbol(
        [0x56E2C],
        [0x2056E2C],
        None,
        (
            "Implements SPECIAL_PROC_SET_TEAM_SETUP_HERO_ONLY (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    GetPartyMembers = Symbol(
        [0x56F9C],
        [0x2056F9C],
        None,
        (
            "Appears to get the team's active party members. Implements most of"
            " SPECIAL_PROC_IS_TEAM_SETUP_SOLO (see ScriptSpecialProcessCall).\n\nr0:"
            " [output] Array of 4 2-byte values (they seem to be indexes of some sort)"
            " describing each party member, which will be filled in by the function."
            " The input can be a null pointer if the party members aren't"
            " needed\nreturn: Number of party members"
        ),
    )

    RefillTeam = Symbol(
        [0x580D4],
        [0x20580D4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    ClearItem = Symbol(
        [0x5856C],
        [0x205856C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: team_id\nr1: check",
    )

    ChangeGiratinaFormIfSkyDungeon = Symbol(
        [0x58954],
        [0x2058954],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID",
    )

    CanLearnIqSkill = Symbol(
        [0x59054],
        [0x2059054],
        None,
        (
            "Returns whether an IQ skill can be learned with a given IQ amount or"
            " not.\n\nIf the specified amount is 0, it always returns false.\n\nr0: IQ"
            " amount\nr1: IQ skill\nreturn: True if the specified skill can be learned"
            " with the specified IQ amount."
        ),
    )

    GetLearnableIqSkills = Symbol(
        [0x59080],
        [0x2059080],
        None,
        (
            "Determines the list of IQ skills that a given monster can learn given its"
            " IQ value.\n\nThe list of skills is written in the array specified in r0."
            " The array has 69 slots in total. Unused slots are set to 0.\n\nr0:"
            " (output) Array where the list of skills will be written\nr1: Monster"
            " species\nr2: Monster IQ\nreturn: Amount of skills written to the output"
            " array"
        ),
    )

    DisableIqSkill = Symbol(
        [0x59120],
        [0x2059120],
        None,
        (
            "Disables an IQ skill.\n\nr0: Pointer to the bitarray containing the list"
            " of enabled IQ skills\nr1: ID of the skill to disable"
        ),
    )

    EnableIqSkill = Symbol(
        [0x59170],
        [0x2059170],
        None,
        (
            "Enables an IQ skill and disables any other skills that are incompatible"
            " with it.\n\nr0: Pointer to the bitarray containing the list of enabled IQ"
            " skills\nr1: ID of the skill to enable"
        ),
    )

    GetSpeciesIqSkill = Symbol(
        [0x591E4],
        [0x20591E4],
        None,
        (
            "Gets the <index>th skill on the list of IQ skills that a given monster"
            " species can learn.\n\nr0: Species ID\nr1: Index (starting at 0)\nreturn:"
            " IQ skill ID"
        ),
    )

    IqSkillFlagTest = Symbol(
        [0x59280],
        [0x2059280],
        None,
        (
            "Tests whether an IQ skill with a given ID is active.\n\nr0: IQ skill"
            " bitvector to test\nr1: IQ skill ID\nreturn: bool"
        ),
    )

    GetNextIqSkill = Symbol(
        [0x592A0],
        [0x20592A0],
        None,
        (
            "Returns the next IQ skill that a given monster will learn given its"
            " current IQ value, or IQ_NONE if the monster won't learn any more"
            " skills.\n\nr0: Monster ID\nr1: Monster IQ\nreturn: ID of the next skill"
            " learned by the monster, or IQ_NONE if the monster won't learn any more"
            " skills."
        ),
    )

    GetExplorerMazeMonster = Symbol(
        [0x59474],
        [0x2059474],
        None,
        (
            "Returns the data of a monster sent into the Explorer Dojo using the"
            " 'exchange teams' option.\n\nr0: Entry number (0-3)\nreturn: Ground"
            " monster data of the specified entry"
        ),
    )

    WriteMonsterInfoToSave = Symbol(
        [0x59494],
        [0x2059494],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: start_address\nr1:"
            " total_length\nreturn: ?"
        ),
    )

    ReadMonsterInfoFromSave = Symbol(
        [0x595A0],
        [0x20595A0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: start_address\nr1:"
            " total_length"
        ),
    )

    WriteMonsterToSave = Symbol(
        [0x596B0],
        [0x20596B0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: write_info\nr1:"
            " ground_monster"
        ),
    )

    ReadMonsterFromSave = Symbol(
        [0x597C0],
        [0x20597C0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info\nr1:"
            " ground_monster"
        ),
    )

    GetEvolutionPossibilities = Symbol(
        [0x59E94],
        [0x2059E94],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ground_monster\nr1:"
            " evo_struct_addr"
        ),
    )

    GetMonsterEvoStatus = Symbol(
        [0x5A58C],
        [0x205A58C],
        None,
        (
            "evo_status = 0: Not possible now\nevo_status = 1: Possible now\nevo_status"
            " = 2: No further\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " ground_monster\nreturn: evo_status"
        ),
    )

    GetSosMailCount = Symbol(
        [0x5BCF8],
        [0x205BCF8],
        None,
        (
            "Implements SPECIAL_PROC_GET_SOS_MAIL_COUNT (see"
            " ScriptSpecialProcessCall).\n\nr0: ?\nr1: some flag?\nreturn: SOS mail"
            " count"
        ),
    )

    IsMissionValid = Symbol(
        [0x5CDBC],
        [0x205CDBC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: mission\nreturn: bool",
    )

    GenerateMission = Symbol(
        [0x5D5A0],
        [0x205D5A0],
        None,
        (
            "Attempts to generate a random mission.\n\nr0: Pointer to something\nr1:"
            " Pointer to the struct where the data of the generated mission will be"
            " written to\nreturn: MISSION_GENERATION_SUCCESS if the mission was"
            " successfully generated, MISSION_GENERATION_FAILURE if it failed and"
            " MISSION_GENERATION_GLOBAL_FAILURE if it failed and the game shouldn't try"
            " to generate more."
        ),
    )

    GenerateDailyMissions = Symbol(
        [0x5E94C],
        [0x205E94C],
        None,
        (
            "Generates the missions displayed on the Job Bulletin Board and the Outlaw"
            " Notice Board.\n\nNo params."
        ),
    )

    DungeonRequestsDone = Symbol(
        [0x5F120],
        [0x205F120],
        None,
        (
            "Seems to return the number of missions completed.\n\nPart of the"
            " implementation for SPECIAL_PROC_DUNGEON_HAD_REQUEST_DONE (see"
            " ScriptSpecialProcessCall).\n\nr0: ?\nr1: some flag?\nreturn: number of"
            " missions completed"
        ),
    )

    DungeonRequestsDoneWrapper = Symbol(
        [0x5F18C],
        [0x205F18C],
        None,
        (
            "Calls DungeonRequestsDone with the second argument set to false.\n\nr0:"
            " ?\nreturn: number of mission completed"
        ),
    )

    AnyDungeonRequestsDone = Symbol(
        [0x5F19C],
        [0x205F19C],
        None,
        (
            "Calls DungeonRequestsDone with the second argument set to true, and"
            " converts the integer output to a boolean.\n\nr0: ?\nreturn: bool: whether"
            " the number of missions completed is greater than 0"
        ),
    )

    GetAcceptedMission = Symbol(
        [0x5F454],
        [0x205F454],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: mission_id\nreturn:"
            " mission"
        ),
    )

    GetMissionByTypeAndDungeon = Symbol(
        [0x5F728],
        [0x205F728],
        None,
        (
            "Returns the position on the mission list of the first mission of the"
            " specified type that takes place in the specified dungeon.\n\nIf the type"
            " of the mission has a subtype, the subtype of the checked mission must"
            " match the one in [r2] too for it to be returned.\n\nr0: Position on the"
            " mission list where the search should start. Missions before this position"
            " on the list will be ignored.\nr1: Mission type\nr2: Pointer to some"
            " struct that contains the subtype of the mission to check on its first"
            " byte\nr3: Dungeon ID\nreturn: Index of the first mission that meets the"
            " specified requirements, or -1 if there aren't any missions that do so."
        ),
    )

    CheckAcceptedMissionByTypeAndDungeon = Symbol(
        [0x5F820],
        [0x205F820],
        None,
        (
            "Returns true if there are any accepted missions on the mission list that"
            " are of the specified type and take place in the specified dungeon.\n\nIf"
            " the type of the mission has a subtype, the subtype of the checked mission"
            " must match the one in [r2] too for it to be returned.\n\nr0: Mission"
            " type\nr1: Pointer to some struct that contains the subtype of the mission"
            " to check on its first byte\nr2: Dungeon ID\nreturn: True if at least one"
            " mission meets the specified requirements, false otherwise."
        ),
    )

    GenerateAllPossibleMonstersList = Symbol(
        [0x5FAD4],
        [0x205FAD4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    DeleteAllPossibleMonstersList = Symbol(
        [0x5FB40],
        [0x205FB40],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GenerateAllPossibleDungeonsList = Symbol(
        [0x5FB70],
        [0x205FB70],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    DeleteAllPossibleDungeonsList = Symbol(
        [0x5FC1C],
        [0x205FC1C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GenerateAllPossibleDeliverList = Symbol(
        [0x5FC4C],
        [0x205FC4C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    DeleteAllPossibleDeliverList = Symbol(
        [0x5FC88],
        [0x205FC88],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    ClearMissionData = Symbol(
        [0x5FD34],
        [0x205FD34],
        None,
        (
            "Given a mission struct, clears some of it fields.\n\nIn particular,"
            " mission::status is set to mission_status::MISSION_STATUS_INVALID,"
            " mission::dungeon_id is set to -1, mission::floor is set to 0 and"
            " mission::reward_type is set to"
            " mission_reward_type::MISSION_REWARD_MONEY.\n\nr0: Pointer to the mission"
            " to clear"
        ),
    )

    IsMonsterMissionAllowed = Symbol(
        [0x62D90],
        [0x2062D90],
        None,
        (
            "Checks if the specified monster is contained in the"
            " MISSION_BANNED_MONSTERS array.\n\nThe function converts the ID by calling"
            " GetBaseForm and FemaleToMaleForm first.\n\nr0: Monster ID\nreturn: False"
            " if the monster ID (after converting it) is contained in"
            " MISSION_BANNED_MONSTERS, true if it isn't."
        ),
    )

    CanMonsterBeUsedForMissionWrapper = Symbol(
        [0x62DD4],
        [0x2062DD4],
        None,
        (
            "Calls CanMonsterBeUsedForMission with r1 = 1.\n\nr0: Monster ID\nreturn:"
            " Result of CanMonsterBeUsedForMission"
        ),
    )

    CanMonsterBeUsedForMission = Symbol(
        [0x62DE4],
        [0x2062DE4],
        None,
        (
            "Returns whether a certain monster can be used (probably as the client or"
            " as the target) when generating a mission.\n\nExcluded monsters include"
            " those that haven't been fought in dungeons yet, the second form of"
            " certain monsters and, if PERFOMANCE_PROGRESS_FLAG[9] is 0, monsters in"
            " MISSION_BANNED_STORY_MONSTERS, the species of the player and the species"
            " of the partner.\n\nr0: Monster ID\nr1: True to exclude monsters in the"
            " MISSION_BANNED_MONSTERS array, false to allow them\nreturn: True if the"
            " specified monster can be part of a mission"
        ),
    )

    IsMonsterMissionAllowedStory = Symbol(
        [0x62E60],
        [0x2062E60],
        None,
        (
            "Checks if the specified monster should be allowed to be part of a mission"
            " (probably as the client or the target), accounting for the progress on"
            " the story.\n\nIf PERFOMANCE_PROGRESS_FLAG[9] is true, the function"
            " returns true.\nIf it isn't, the function checks if the specified monster"
            " is contained in the MISSION_BANNED_STORY_MONSTERS array, or if it"
            " corresponds to the ID of the player or the partner.\n\nThe function"
            " converts the ID by calling GetBaseForm and FemaleToMaleForm first.\n\nr0:"
            " Monster ID\nreturn: True if PERFOMANCE_PROGRESS_FLAG[9] is true, false if"
            " it isn't and the monster ID (after converting it) is contained in"
            " MISSION_BANNED_STORY_MONSTERS or if it's the ID of the player or the"
            " partner, true otherwise."
        ),
    )

    CanSendItem = Symbol(
        [0x63158],
        [0x2063158],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nr1:"
            " to_sky\nreturn: bool"
        ),
    )

    IsAvailableItem = Symbol(
        [0x637D8],
        [0x20637D8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: bool",
    )

    GetAvailableItemDeliveryList = Symbol(
        [0x63824],
        [0x2063824],
        None,
        (
            "Uncertain.\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " item_buffer\nreturn: nb_items"
        ),
    )

    GetActorMatchingStorageId = Symbol(
        [0x65D14],
        [0x2065D14],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: actor_id\nreturn:"
            " storage ID"
        ),
    )

    ScriptSpecialProcess0x3D = Symbol(
        [0x65ECC],
        [0x2065ECC],
        None,
        "Implements SPECIAL_PROC_0x3D (see ScriptSpecialProcessCall).\n\nNo params.",
    )

    ScriptSpecialProcess0x3E = Symbol(
        [0x65EDC],
        [0x2065EDC],
        None,
        "Implements SPECIAL_PROC_0x3E (see ScriptSpecialProcessCall).\n\nNo params.",
    )

    ScriptSpecialProcess0x17 = Symbol(
        [0x65FC4],
        [0x2065FC4],
        None,
        "Implements SPECIAL_PROC_0x17 (see ScriptSpecialProcessCall).\n\nNo params.",
    )

    ItemAtTableIdx = Symbol(
        [0x66074],
        [0x2066074],
        None,
        (
            "Gets info about the item at a given item table (not sure what this table"
            " is...) index.\n\nUsed by SPECIAL_PROC_COUNT_TABLE_ITEM_TYPE_IN_BAG and"
            " friends (see ScriptSpecialProcessCall).\n\nr0: table index\nr1: [output]"
            " pointer to an owned_item"
        ),
    )

    DungeonSwapIdToIdx = Symbol(
        [0x6AAAC],
        [0x206AAAC],
        None,
        (
            "Converts a dungeon ID to its corresponding index in DUNGEON_SWAP_ID_TABLE,"
            " or -1 if not found.\n\nr0: dungeon ID\nreturn: index"
        ),
    )

    DungeonSwapIdxToId = Symbol(
        [0x6AAE8],
        [0x206AAE8],
        None,
        (
            "Converts an index in DUNGEON_SWAP_ID_TABLE to the corresponding dungeon"
            " ID, or DUNGEON_DUMMY_0xFF if the index is -1.\n\nr0: index\nreturn:"
            " dungeon ID"
        ),
    )

    ResumeBgm = Symbol(
        [0x6DD54],
        [0x206DD54],
        None,
        "Uncertain.\n\nNote: unverified, ported from Irdkwia's notes",
    )

    FlushChannels = Symbol(
        [0x70A0C], [0x2070A0C], None, "Note: unverified, ported from Irdkwia's notes"
    )

    UpdateChannels = Symbol(
        [0x74824],
        [0x2074824],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    WaitForInterrupt = Symbol(
        [0x7BFC8],
        [0x207BFC8],
        None,
        (
            "Presumably blocks until the program receives an interrupt.\n\nThis just"
            " calls (in Ghidra terminology) coproc_moveto_Wait_for_interrupt(0). See"
            " https://en.wikipedia.org/wiki/ARM_architecture_family#Coprocessors.\n\nNo"
            " params."
        ),
    )

    FileInit = Symbol(
        [0x7F77C],
        [0x207F77C],
        None,
        (
            "Initializes a file_stream structure for file I/O.\n\nThis function must"
            " always be called before opening a file.\n\nr0: file_stream pointer"
        ),
    )

    Abs = Symbol(
        [0x868F4],
        [0x20868F4],
        None,
        "Takes the absolute value of an integer.\n\nr0: x\nreturn: abs(x)",
    )

    Mbtowc = Symbol(
        [0x87554],
        [0x2087554],
        None,
        (
            "The mbtowc(3) C library function.\n\nr0: pwc\nr1: s\nr2: n\nreturn: number"
            " of consumed bytes, or -1 on failure"
        ),
    )

    TryAssignByte = Symbol(
        [0x8758C],
        [0x208758C],
        None,
        (
            "Assign a byte to the target of a pointer if the pointer is"
            " non-null.\n\nr0: pointer\nr1: value\nreturn: true on success, false on"
            " failure"
        ),
    )

    TryAssignByteWrapper = Symbol(
        [0x875A0],
        [0x20875A0],
        None,
        (
            "Wrapper around TryAssignByte.\n\nAccesses the TryAssignByte function with"
            " a weird chain of pointer dereferences.\n\nr0: pointer\nr1: value\nreturn:"
            " true on success, false on failure"
        ),
    )

    Wcstombs = Symbol(
        [0x875BC],
        [0x20875BC],
        None,
        (
            "The wcstombs(3) C library function.\n\nr0: dest\nr1: src\nr2: n\nreturn:"
            " characters converted"
        ),
    )

    Memcpy = Symbol(
        [0x87634],
        [0x2087634],
        None,
        "The memcpy(3) C library function.\n\nr0: dest\nr1: src\nr2: n",
    )

    Memmove = Symbol(
        [0x87654],
        [0x2087654],
        None,
        (
            "The memmove(3) C library function.\n\nThe implementation is nearly the"
            " same as Memcpy, but it copies bytes from back to front if src <"
            " dst.\n\nr0: dest\nr1: src\nr2: n"
        ),
    )

    Memset = Symbol(
        [0x876A0],
        [0x20876A0],
        None,
        (
            "The memset(3) C library function.\n\nThis is just a wrapper around"
            " MemsetInternal that returns the pointer at the end.\n\nr0: s\nr1: c (int,"
            " but must be a single-byte value)\nr2: n\nreturn: s"
        ),
    )

    Memchr = Symbol(
        [0x876B4],
        [0x20876B4],
        None,
        (
            "The memchr(3) C library function.\n\nr0: s\nr1: c\nr2: n\nreturn: pointer"
            " to first occurrence of c in s, or a null pointer if no match"
        ),
    )

    Memcmp = Symbol(
        [0x876E0],
        [0x20876E0],
        None,
        (
            "The memcmp(3) C library function.\n\nr0: s1\nr1: s2\nr2: n\nreturn:"
            " comparison value"
        ),
    )

    MemsetInternal = Symbol(
        [0x87720],
        [0x2087720],
        None,
        (
            "The actual memory-setting implementation for the memset(3) C library"
            " function.\n\nThis function is optimized to set bytes in 4-byte chunks for"
            " n >= 32, correctly handling any unaligned bytes at the front/back. In"
            " this case, it also further optimizes by unrolling a for loop to set 8"
            " 4-byte values at once (effectively a 32-byte chunk).\n\nr0: s\nr1: c"
            " (int, but must be a single-byte value)\nr2: n"
        ),
    )

    VsprintfInternalSlice = Symbol(
        [0x8900C],
        [0x208900C],
        None,
        (
            "This is what implements the bulk of VsprintfInternal.\n\nThe"
            " __vsprintf_internal in the modern-day version of glibc relies on"
            " __vfprintf_internal; this function has a slightly different interface,"
            " but it serves a similar role.\n\nr0: function pointer to append to the"
            " string being built (VsprintfInternal uses TryAppendToSlice)\nr1: string"
            " buffer slice\nr2: format\nr3: ap\nreturn: number of characters printed,"
            " excluding the null-terminator"
        ),
    )

    TryAppendToSlice = Symbol(
        [0x89830],
        [0x2089830],
        None,
        (
            "Best-effort append the given data to a slice. If the slice's capacity is"
            " reached, any remaining data will be truncated.\n\nr0: slice pointer\nr1:"
            " buffer of data to append\nr2: number of bytes in the data buffer\nreturn:"
            " true"
        ),
    )

    VsprintfInternal = Symbol(
        [0x89874],
        [0x2089874],
        None,
        (
            "This is what implements Vsprintf. It's akin to __vsprintf_internal in the"
            " modern-day version of glibc (in fact, it's probably an older version of"
            " this).\n\nr0: str\nr1: maxlen (Vsprintf passes UINT32_MAX for this)\nr2:"
            " format\nr3: ap\nreturn: number of characters printed, excluding the"
            " null-terminator"
        ),
    )

    Vsprintf = Symbol(
        [0x898DC],
        [0x20898DC],
        None,
        (
            "The vsprintf(3) C library function.\n\nr0: str\nr1: format\nr2:"
            " ap\nreturn: number of characters printed, excluding the null-terminator"
        ),
    )

    Snprintf = Symbol(
        [0x898F4],
        [0x20898F4],
        None,
        (
            "The snprintf(3) C library function.\n\nThis calls VsprintfInternal"
            " directly, so it's presumably the real snprintf.\n\nr0: str\nr1: n\nr2:"
            " format\n...: variadic\nreturn: number of characters printed, excluding"
            " the null-terminator"
        ),
    )

    Sprintf = Symbol(
        [0x8991C],
        [0x208991C],
        None,
        (
            "The sprintf(3) C library function.\n\nThis calls VsprintfInternal"
            " directly, so it's presumably the real sprintf.\n\nr0: str\nr1:"
            " format\n...: variadic\nreturn: number of characters printed, excluding"
            " the null-terminator"
        ),
    )

    Strlen = Symbol(
        [0x89A10],
        [0x2089A10],
        None,
        "The strlen(3) C library function.\n\nr0: s\nreturn: length of s",
    )

    Strcpy = Symbol(
        [0x89A2C],
        [0x2089A2C],
        None,
        (
            "The strcpy(3) C library function.\n\nThis function is optimized to copy"
            " characters in aligned 4-byte chunks if possible, correctly handling any"
            " unaligned bytes at the front/back.\n\nr0: dest\nr1: src"
        ),
    )

    Strncpy = Symbol(
        [0x89AF4],
        [0x2089AF4],
        None,
        "The strncpy(3) C library function.\n\nr0: dest\nr1: src\nr2: n",
    )

    Strcat = Symbol(
        [0x89B44],
        [0x2089B44],
        None,
        "The strcat(3) C library function.\n\nr0: dest\nr1: src",
    )

    Strncat = Symbol(
        [0x89B74],
        [0x2089B74],
        None,
        "The strncat(3) C library function.\n\nr0: dest\nr1: src\nr2: n",
    )

    Strcmp = Symbol(
        [0x89BC4],
        [0x2089BC4],
        None,
        (
            "The strcmp(3) C library function.\n\nSimilarly to Strcpy, this function is"
            " optimized to compare characters in aligned 4-byte chunks if"
            " possible.\n\nr0: s1\nr1: s2\nreturn: comparison value"
        ),
    )

    Strncmp = Symbol(
        [0x89CD8],
        [0x2089CD8],
        None,
        (
            "The strncmp(3) C library function.\n\nr0: s1\nr1: s2\nr2: n\nreturn:"
            " comparison value"
        ),
    )

    Strchr = Symbol(
        [0x89D0C],
        [0x2089D0C],
        None,
        (
            "The strchr(3) C library function.\n\nr0: string\nr1: c\nreturn: pointer to"
            " the located byte c, or null pointer if no match"
        ),
    )

    Strcspn = Symbol(
        [0x89D48],
        [0x2089D48],
        None,
        (
            "The strcspn(3) C library function.\n\nr0: string\nr1: stopset\nreturn:"
            " offset of the first character in string within stopset"
        ),
    )

    Strstr = Symbol(
        [0x89E08],
        [0x2089E08],
        None,
        (
            "The strstr(3) C library function.\n\nr0: haystack\nr1: needle\nreturn:"
            " pointer into haystack where needle starts, or null pointer if no match"
        ),
    )

    Wcslen = Symbol(
        [0x8B780],
        [0x208B780],
        None,
        "The wcslen(3) C library function.\n\nr0: ws\nreturn: length of ws",
    )

    AddFloat = Symbol(
        [0x8F050],
        [0x208F050],
        None,
        (
            "This appears to be the libgcc implementation of __addsf3 (not sure which"
            " gcc version), which implements the addition operator for IEEE 754"
            " floating-point numbers.\n\nr0: a\nr1: b\nreturn: a + b"
        ),
    )

    DivideFloat = Symbol(
        [0x8F5CC],
        [0x208F5CC],
        None,
        (
            "This appears to be the libgcc implementation of __divsf3 (not sure which"
            " gcc version), which implements the division operator for IEEE 754"
            " floating-point numbers.\n\nr0: dividend\nr1: divisor\nreturn: dividend /"
            " divisor"
        ),
    )

    FloatToDouble = Symbol(
        [0x8F984],
        [0x208F984],
        None,
        (
            "This appears to be the libgcc implementation of __extendsfdf2 (not sure"
            " which gcc version), which implements the float to double cast operation"
            " for IEEE 754 floating-point numbers.\n\nr0: float\nreturn: (double)float"
        ),
    )

    FloatToInt = Symbol(
        [0x8FA08],
        [0x208FA08],
        None,
        (
            "This appears to be the libgcc implementation of __fixsfsi (not sure which"
            " gcc version), which implements the float to int cast operation for IEEE"
            " 754 floating-point numbers. The output saturates if the input is out of"
            " the representable range for the int type.\n\nr0: float\nreturn:"
            " (int)float"
        ),
    )

    IntToFloat = Symbol(
        [0x8FA3C],
        [0x208FA3C],
        None,
        (
            "This appears to be the libgcc implementation of __floatsisf (not sure"
            " which gcc version), which implements the int to float cast operation for"
            " IEEE 754 floating-point numbers.\n\nr0: int\nreturn: (float)int"
        ),
    )

    UIntToFloat = Symbol(
        [0x8FA84],
        [0x208FA84],
        None,
        (
            "This appears to be the libgcc implementation of __floatunsisf (not sure"
            " which gcc version), which implements the unsigned int to float cast"
            " operation for IEEE 754 floating-point numbers.\n\nr0: uint\nreturn:"
            " (float)uint"
        ),
    )

    MultiplyFloat = Symbol(
        [0x8FACC],
        [0x208FACC],
        None,
        (
            "This appears to be the libgcc implementation of __mulsf3 (not sure which"
            " gcc version), which implements the multiplication operator for IEEE 754"
            " floating-point numbers."
        ),
    )

    Sqrtf = Symbol(
        [0x8FCAC],
        [0x208FCAC],
        None,
        "The sqrtf(3) C library function.\n\nr0: x\nreturn: sqrt(x)",
    )

    SubtractFloat = Symbol(
        [0x8FD9C],
        [0x208FD9C],
        None,
        (
            "This appears to be the libgcc implementation of __subsf3 (not sure which"
            " gcc version), which implements the subtraction operator for IEEE 754"
            " floating-point numbers.\n\nr0: a\nr1: b\nreturn: a - b"
        ),
    )

    DivideInt = Symbol(
        [0x9023C],
        [0x209023C],
        None,
        (
            "This appears to be the libgcc implementation of __divsi3 (not sure which"
            " gcc version), which implements the division operator for signed"
            " ints.\n\nThe return value is a 64-bit integer, with the quotient"
            " (dividend / divisor) in the lower 32 bits and the remainder (dividend %"
            " divisor) in the upper 32 bits. In accordance with the Procedure Call"
            " Standard for the Arm Architecture (see"
            " https://github.com/ARM-software/abi-aa/blob/60a8eb8c55e999d74dac5e368fc9d7e36e38dda4/aapcs32/aapcs32.rst#result-return),"
            " this means that the quotient is returned in r0 and the remainder is"
            " returned in r1.\n\nr0: dividend\nr1: divisor\nreturn: (quotient) |"
            " (remainder << 32)"
        ),
    )

    DivideUInt = Symbol(
        [0x90448],
        [0x2090448],
        None,
        (
            "This appears to be the libgcc implementation of __udivsi3 (not sure which"
            " gcc version), which implements the division operator for unsigned"
            " ints.\n\nThe return value is a 64-bit integer, with the quotient"
            " (dividend / divisor) in the lower 32 bits and the remainder (dividend %"
            " divisor) in the upper 32 bits. In accordance with the Procedure Call"
            " Standard for the Arm Architecture (see"
            " https://github.com/ARM-software/abi-aa/blob/60a8eb8c55e999d74dac5e368fc9d7e36e38dda4/aapcs32/aapcs32.rst#result-return),"
            " this means that the quotient is returned in r0 and the remainder is"
            " returned in r1.\nNote: This function falls through to"
            " DivideUIntNoZeroCheck.\n\nr0: dividend\nr1: divisor\nreturn: (quotient) |"
            " (remainder << 32)"
        ),
    )

    DivideUIntNoZeroCheck = Symbol(
        [0x90450],
        [0x2090450],
        None,
        (
            "Subsidiary function to DivideUInt. Skips the initial check for divisor =="
            " 0.\n\nThe return value is a 64-bit integer, with the quotient (dividend /"
            " divisor) in the lower 32 bits and the remainder (dividend % divisor) in"
            " the upper 32 bits. In accordance with the Procedure Call Standard for the"
            " Arm Architecture (see"
            " https://github.com/ARM-software/abi-aa/blob/60a8eb8c55e999d74dac5e368fc9d7e36e38dda4/aapcs32/aapcs32.rst#result-return),"
            " this means that the quotient is returned in r0 and the remainder is"
            " returned in r1.\nThis function appears to only be called"
            " internally.\n\nr0: dividend\nr1: divisor\nreturn: (quotient) | (remainder"
            " << 32)"
        ),
    )


class EuArm9Data:
    ARM9_HEADER = Symbol(
        [0x0], [0x2000000], 0x800, "Note: unverified, ported from Irdkwia's notes"
    )

    SDK_STRINGS = Symbol(
        [0xBA0], [0x2000BA0], 0xCC, "Note: unverified, ported from Irdkwia's notes"
    )

    DEFAULT_MEMORY_ARENA_SIZE = Symbol(
        [0xE58],
        [0x2000E58],
        0x4,
        "Length in bytes of the default memory allocation arena, 1991680.",
    )

    DAMAGE_SOURCE_CODE_ORB_ITEM = Symbol(
        None,
        None,
        None,
        "The damage source value for any item in CATEGORY_ORBS, 0x262.",
    )

    DAMAGE_SOURCE_CODE_NON_ORB_ITEM = Symbol(
        None,
        None,
        None,
        "The damage source value for any item not in CATEGORY_ORBS, 0x263.",
    )

    AURA_BOW_ID_LAST = Symbol(
        [0xCCBC], [0x200CCBC], 0x4, "Highest item ID of the aura bows."
    )

    NUMBER_OF_ITEMS = Symbol(
        [0xE88C, 0xE930], [0x200E88C, 0x200E930], 0x4, "Number of items in the game."
    )

    MAX_MONEY_CARRIED = Symbol(
        [0xEDF8],
        [0x200EDF8],
        0x4,
        "Maximum amount of money the player can carry, 99999.",
    )

    MAX_MONEY_STORED = Symbol(
        [0x107F8],
        [0x20107F8],
        0x4,
        "Maximum amount of money the player can store in the Duskull Bank, 9999999.",
    )

    DIALOG_BOX_LIST_PTR = Symbol(
        None, None, None, "Hard-coded pointer to DIALOG_BOX_LIST."
    )

    SCRIPT_VARS_VALUES_PTR = Symbol(
        [0x4B630, 0x4B81C, 0x4C764, 0x4C7BC],
        [0x204B630, 0x204B81C, 0x204C764, 0x204C7BC],
        0x4,
        "Hard-coded pointer to SCRIPT_VARS_VALUES.",
    )

    MONSTER_ID_LIMIT = Symbol(
        [0x54818],
        [0x2054818],
        0x4,
        "One more than the maximum valid monster ID (0x483).",
    )

    MAX_RECRUITABLE_TEAM_MEMBERS = Symbol(
        [0x555B4, 0x559C8],
        [0x20555B4, 0x20559C8],
        0x4,
        (
            "555, appears to be the maximum number of members recruited to an"
            " exploration team, at least for the purposes of some checks that need to"
            " iterate over all team members."
        ),
    )

    CART_REMOVED_IMG_DATA = Symbol([0x92EE4], [0x2092EE4], 0x2000, "")

    AVAILABLE_ITEMS_IN_GROUP_TABLE = Symbol(
        [0x95130],
        [0x2095130],
        0x3200,
        (
            "100*0x80\nLinked to the dungeon group id\n\nNote: unverified, ported from"
            " Irdkwia's notes"
        ),
    )

    ARM9_UNKNOWN_TABLE__NA_2097FF8 = Symbol(
        [0x98444],
        [0x2098444],
        0x40,
        "16*0x4 (0x2+0x2)\n\nNote: unverified, ported from Irdkwia's notes",
    )

    KECLEON_SHOP_ITEM_TABLE_LISTS_1 = Symbol(
        [0x98504],
        [0x2098504],
        0x10,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: enum item_id[4]",
    )

    KECLEON_SHOP_ITEM_TABLE_LISTS_2 = Symbol(
        [0x98514],
        [0x2098514],
        0x10,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: enum item_id[4]",
    )

    EXCLUSIVE_ITEM_STAT_BOOST_DATA = Symbol(
        [0x9852C],
        [0x209852C],
        0x3C,
        (
            "Contains stat boost effects for different exclusive item classes.\n\nEach"
            " 4-byte entry contains the boost data for (attack, special attack,"
            " defense, special defense), 1 byte each, for a specific exclusive item"
            " class, indexed according to the stat boost data index list.\n\ntype:"
            " struct exclusive_item_stat_boost_entry[15]"
        ),
    )

    EXCLUSIVE_ITEM_ATTACK_BOOSTS = Symbol(
        [0x9852C], [0x209852C], 0x39, "EXCLUSIVE_ITEM_STAT_BOOST_DATA, offset by 0"
    )

    EXCLUSIVE_ITEM_SPECIAL_ATTACK_BOOSTS = Symbol(
        [0x9852D], [0x209852D], 0x39, "EXCLUSIVE_ITEM_STAT_BOOST_DATA, offset by 1"
    )

    EXCLUSIVE_ITEM_DEFENSE_BOOSTS = Symbol(
        [0x9852E], [0x209852E], 0x39, "EXCLUSIVE_ITEM_STAT_BOOST_DATA, offset by 2"
    )

    EXCLUSIVE_ITEM_SPECIAL_DEFENSE_BOOSTS = Symbol(
        [0x9852F], [0x209852F], 0x39, "EXCLUSIVE_ITEM_STAT_BOOST_DATA, offset by 3"
    )

    EXCLUSIVE_ITEM_EFFECT_DATA = Symbol(
        [0x98568],
        [0x2098568],
        0x778,
        (
            "Contains special effects for each exclusive item.\n\nEach entry is 2"
            " bytes, with the first entry corresponding to the first exclusive item"
            " (Prism Ruff). The first byte is the exclusive item effect ID, and the"
            " second byte is an index into other data tables (related to the more"
            " generic stat boosting effects for specific monsters).\n\ntype: struct"
            " exclusive_item_effect_entry[956]"
        ),
    )

    EXCLUSIVE_ITEM_STAT_BOOST_DATA_INDEXES = Symbol(
        [0x98569], [0x2098569], 0x777, "EXCLUSIVE_ITEM_EFFECT_DATA, offset by 1"
    )

    RECYCLE_SHOP_ITEM_LIST = Symbol(
        [0x98D10], [0x2098D10], 0x360, "Note: unverified, ported from Irdkwia's notes"
    )

    TYPE_SPECIFIC_EXCLUSIVE_ITEMS = Symbol(
        [0x99070],
        [0x2099070],
        0x88,
        (
            "Lists of type-specific exclusive items (silk, dust, gem, globe) for each"
            " type.\n\ntype: struct item_id_16[17][4]"
        ),
    )

    RECOIL_MOVE_LIST = Symbol(
        [0x991B8],
        [0x20991B8],
        0x16,
        (
            "Null-terminated list of all the recoil moves, as 2-byte move IDs.\n\ntype:"
            " struct move_id_16[11]"
        ),
    )

    PUNCH_MOVE_LIST = Symbol(
        [0x991CE],
        [0x20991CE],
        0x20,
        (
            "Null-terminated list of all the punch moves, as 2-byte move IDs.\n\ntype:"
            " struct move_id_16[16]"
        ),
    )

    MOVE_POWER_STARS_TABLE = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int[6]",
    )

    MOVE_ACCURACY_STARS_TABLE = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int[8]",
    )

    PARTNER_TALK_KIND_TABLE = Symbol(
        [0x9D268],
        [0x209D268],
        0x58,
        (
            "Table of values for the PARTNER_TALK_KIND script variable.\n\ntype: struct"
            " partner_talk_kind_table_entry[11]"
        ),
    )

    SCRIPT_VARS_LOCALS = Symbol(
        [0x9D450],
        [0x209D450],
        0x40,
        (
            "List of special 'local' variables available to the script engine. There"
            " are 4 16-byte entries.\n\nEach entry has the same structure as an entry"
            " in SCRIPT_VARS.\n\ntype: struct script_local_var_table"
        ),
    )

    SCRIPT_VARS = Symbol(
        [0x9DDF4],
        [0x209DDF4],
        0x730,
        (
            "List of predefined global variables that track game state, which are"
            " available to the script engine. There are 115 16-byte entries.\n\nThese"
            " variables underpin the various ExplorerScript global variables you can"
            " use in the SkyTemple SSB debugger.\n\ntype: struct script_var_table"
        ),
    )

    HARDCODED_PORTRAIT_DATA_TABLE = Symbol(
        [0x9E598],
        [0x209E598],
        0xC0,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " portrait_data_entry[32]"
        ),
    )

    WONDER_MAIL_BITS_MAP = Symbol(
        [0x9E66C],
        [0x209E66C],
        0x20,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: uint8_t[32]",
    )

    WONDER_MAIL_BITS_SWAP = Symbol(
        [0x9E68C],
        [0x209E68C],
        0x24,
        (
            "Last 2 bytes are unused\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\ntype: uint8_t[36]"
        ),
    )

    ARM9_UNKNOWN_TABLE__NA_209E12C = Symbol(
        [0x9E6B0],
        [0x209E6B0],
        0x38,
        "52*0x2 + 2 bytes unused\n\nNote: unverified, ported from Irdkwia's notes",
    )

    ARM9_UNKNOWN_TABLE__NA_209E164 = Symbol(
        [0x9E6E8],
        [0x209E6E8],
        0x100,
        "256*0x1\n\nNote: unverified, ported from Irdkwia's notes",
    )

    ARM9_UNKNOWN_TABLE__NA_209E280 = Symbol(
        [0x9E804],
        [0x209E804],
        0x20,
        "32*0x1\n\nNote: unverified, ported from Irdkwia's notes",
    )

    WONDER_MAIL_ENCRYPTION_TABLE = Symbol(
        [0x9E824],
        [0x209E824],
        0x100,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: uint8_t[256]",
    )

    DUNGEON_DATA_LIST = Symbol(
        [0x9E924],
        [0x209E924],
        0x2D0,
        (
            "Data about every dungeon in the game.\n\nThis is an array of 180 dungeon"
            " data list entry structs. Each entry is 4 bytes, and contains floor count"
            " information along with an index into the bulk of the dungeon's data in"
            " mappa_s.bin.\n\nSee the struct definitions and End45's dungeon data"
            " document for more info.\n\ntype: struct dungeon_data_list_entry[180]"
        ),
    )

    ADVENTURE_LOG_ENCOUNTERS_MONSTER_IDS = Symbol(
        [0x9EBF4],
        [0x209EBF4],
        0x4C,
        (
            "List of monster IDs with a corresponding milestone in the Adventure"
            " Log.\n\ntype: struct monster_id_16[38]"
        ),
    )

    ARM9_UNKNOWN_DATA__NA_209E6BC = Symbol(
        [0x9EC40], [0x209EC40], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    TACTIC_NAME_STRING_IDS = Symbol(
        [0x9EC44],
        [0x209EC44],
        0x18,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[12]",
    )

    STATUS_NAME_STRING_IDS = Symbol(
        [0x9EC5C],
        [0x209EC5C],
        0xCC,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[102]",
    )

    DUNGEON_RETURN_STATUS_TABLE = Symbol(
        [0x9ED28],
        [0x209ED28],
        0x16C,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " dungeon_return_status[91]"
        ),
    )

    STATUSES_FULL_DESCRIPTION_STRING_IDS = Symbol(
        [0x9EE94],
        [0x209EE94],
        0x19C,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " status_description[103]"
        ),
    )

    ARM9_UNKNOWN_DATA__NA_209EAAC = Symbol(
        [0x9F030], [0x209F030], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_FLOOR_RANKS_AND_ITEM_LISTS_1 = Symbol(
        [0x9F034], [0x209F034], 0xC64, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_FLOORS_FORBIDDEN = Symbol(
        [0x9FC98],
        [0x209FC98],
        0xC8,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " mission_floors_forbidden[100]"
        ),
    )

    MISSION_FLOOR_RANKS_AND_ITEM_LISTS_2 = Symbol(
        [0x9FD60], [0x209FD60], 0x12F8, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_FLOOR_RANKS_PTRS = Symbol(
        [0xA1058],
        [0x20A1058],
        0x190,
        (
            "Uses MISSION_FLOOR_RANKS_AND_ITEM_LISTS\n\nNote: unverified, ported from"
            " Irdkwia's notes"
        ),
    )

    DUNGEON_RESTRICTIONS = Symbol(
        [0xA11E8],
        [0x20A11E8],
        0xC00,
        (
            "Data related to dungeon restrictions for every dungeon in the"
            " game.\n\nThis is an array of 256 dungeon restriction structs. Each entry"
            " is 12 bytes, and contains information about restrictions within the given"
            " dungeon.\n\nSee the struct definitions and End45's dungeon data document"
            " for more info.\n\ntype: struct dungeon_restriction[256]"
        ),
    )

    SPECIAL_BAND_STAT_BOOST = Symbol(
        [0xA1DF0], [0x20A1DF0], 0x2, "Stat boost value for the Special Band."
    )

    MUNCH_BELT_STAT_BOOST = Symbol(
        [0xA1E00], [0x20A1E00], 0x2, "Stat boost value for the Munch Belt."
    )

    GUMMI_STAT_BOOST = Symbol(
        [0xA1E0C],
        [0x20A1E0C],
        0x2,
        "Stat boost value if a stat boost occurs when eating normal Gummis.",
    )

    MIN_IQ_EXCLUSIVE_MOVE_USER = Symbol([0xA1E10], [0x20A1E10], 0x4, "")

    WONDER_GUMMI_IQ_GAIN = Symbol(
        [0xA1E14], [0x20A1E14], 0x2, "IQ gain when ingesting wonder gummis."
    )

    AURA_BOW_STAT_BOOST = Symbol(
        [0xA1E1C], [0x20A1E1C], 0x2, "Stat boost value for the aura bows."
    )

    MIN_IQ_ITEM_MASTER = Symbol([0xA1E28], [0x20A1E28], 0x4, "")

    DEF_SCARF_STAT_BOOST = Symbol(
        [0xA1E2C], [0x20A1E2C], 0x2, "Stat boost value for the Defense Scarf."
    )

    POWER_BAND_STAT_BOOST = Symbol(
        [0xA1E30], [0x20A1E30], 0x2, "Stat boost value for the Power Band."
    )

    WONDER_GUMMI_STAT_BOOST = Symbol(
        [0xA1E34],
        [0x20A1E34],
        0x2,
        "Stat boost value if a stat boost occurs when eating Wonder Gummis.",
    )

    ZINC_BAND_STAT_BOOST = Symbol(
        [0xA1E38], [0x20A1E38], 0x2, "Stat boost value for the Zinc Band."
    )

    EGG_HP_BONUS = Symbol(
        [0xA1E3C], [0x20A1E3C], 0x2, "Note: unverified, ported from Irdkwia's notes"
    )

    EVOLUTION_HP_BONUS = Symbol(
        [0xA1E48], [0x20A1E48], 0x2, "Note: unverified, ported from Irdkwia's notes"
    )

    EVOLUTION_PHYSICAL_STAT_BONUSES = Symbol(
        [0xA1E54],
        [0x20A1E54],
        0x4,
        "0x2: Atk + 0x2: Def\n\nNote: unverified, ported from Irdkwia's notes",
    )

    EGG_STAT_BONUSES = Symbol(
        [0xA1E60],
        [0x20A1E60],
        0x8,
        (
            "0x2: Atk + 0x2: SpAtk + 0x2: Def + 0x2: SpDef\n\nNote: unverified, ported"
            " from Irdkwia's notes"
        ),
    )

    EVOLUTION_SPECIAL_STAT_BONUSES = Symbol(
        [0xA1E68],
        [0x20A1E68],
        0x4,
        "0x2: SpAtk + 0x2: SpDef\n\nNote: unverified, ported from Irdkwia's notes",
    )

    FORBIDDEN_FORGOT_MOVE_LIST = Symbol(
        [0xA1E9C],
        [0x20A1E9C],
        0x12,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " forbidden_forgot_move_entry[3]"
        ),
    )

    TACTICS_UNLOCK_LEVEL_TABLE = Symbol(
        [0xA1EC4], [0x20A1EC4], 0x18, "type: int16_t[12]"
    )

    CLIENT_LEVEL_TABLE = Symbol(
        [0xA1EFC],
        [0x20A1EFC],
        0x20,
        (
            "Still a guess\n\nNote: unverified, ported from Irdkwia's notes\n\ntype:"
            " int16_t[16]"
        ),
    )

    OUTLAW_LEVEL_TABLE = Symbol(
        [0xA1F1C],
        [0x20A1F1C],
        0x20,
        (
            "Table of 2-byte outlaw levels for outlaw missions, indexed by mission"
            " rank.\n\ntype: int16_t[16]"
        ),
    )

    OUTLAW_MINION_LEVEL_TABLE = Symbol(
        [0xA1F3C],
        [0x20A1F3C],
        0x20,
        (
            "Table of 2-byte outlaw minion levels for outlaw hideout missions, indexed"
            " by mission rank.\n\ntype: int16_t[16]"
        ),
    )

    HIDDEN_POWER_BASE_POWER_TABLE = Symbol(
        [0xA1F5C],
        [0x20A1F5C],
        0x28,
        (
            "Still a guess\n\nNote: unverified, ported from Irdkwia's notes\n\ntype:"
            " int[10]"
        ),
    )

    VERSION_EXCLUSIVE_MONSTERS = Symbol(
        [0xA1F84],
        [0x20A1F84],
        0x5C,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " version_exclusive_monster[23]"
        ),
    )

    IQ_SKILL_RESTRICTIONS = Symbol(
        [0xA1FE0],
        [0x20A1FE0],
        0x8A,
        (
            "Table of 2-byte values for each IQ skill that represent a group. IQ skills"
            " in the same group can not be enabled at the same time.\n\ntype:"
            " int16_t[69]"
        ),
    )

    SECONDARY_TERRAIN_TYPES = Symbol(
        [0xA206C],
        [0x20A206C],
        0xC8,
        (
            "The type of secondary terrain for each dungeon in the game.\n\nThis is an"
            " array of 200 bytes. Each byte is an enum corresponding to one"
            " dungeon.\n\ntype: struct secondary_terrain_type_8[200]"
        ),
    )

    SENTRY_DUTY_MONSTER_IDS = Symbol(
        [0xA2134],
        [0x20A2134],
        0xCC,
        (
            "Table of monster IDs usable in the sentry duty minigame.\n\ntype: struct"
            " monster_id_16[102]"
        ),
    )

    IQ_SKILLS = Symbol(
        [0xA2200],
        [0x20A2200],
        0x114,
        (
            "Table of 4-byte values for each IQ skill that represent the required IQ"
            " value to unlock a skill.\n\ntype: int[69]"
        ),
    )

    IQ_GROUP_SKILLS = Symbol(
        [0xA2314], [0x20A2314], 0x190, "Irdkwia's notes: 25*16*0x1"
    )

    MONEY_QUANTITY_TABLE = Symbol(
        [0xA24A4],
        [0x20A24A4],
        0x190,
        (
            "Table that maps money quantity codes (as recorded in, e.g., struct item)"
            " to actual amounts.\n\ntype: int[100]"
        ),
    )

    ARM9_UNKNOWN_TABLE__NA_20A20B0 = Symbol(
        [0xA2634],
        [0x20A2634],
        0x200,
        "256*0x2\n\nNote: unverified, ported from Irdkwia's notes",
    )

    IQ_GUMMI_GAIN_TABLE = Symbol([0xA2834], [0x20A2834], 0x288, "type: int16_t[18][18]")

    GUMMI_BELLY_RESTORE_TABLE = Symbol(
        [0xA2ABC], [0x20A2ABC], 0x288, "type: int16_t[18][18]"
    )

    BAG_CAPACITY_TABLE_SPECIAL_EPISODES = Symbol(
        [0xA2D44],
        [0x20A2D44],
        0x14,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: uint32_t[5]",
    )

    BAG_CAPACITY_TABLE = Symbol(
        [0xA2D58],
        [0x20A2D58],
        0x20,
        (
            "Array of 4-byte integers containing the bag capacity for each bag"
            " level.\n\ntype: uint32_t[8]"
        ),
    )

    SPECIAL_EPISODE_MAIN_CHARACTERS = Symbol(
        [0xA2D78], [0x20A2D78], 0xC8, "type: struct monster_id_16[100]"
    )

    GUEST_MONSTER_DATA = Symbol(
        [0xA2E40],
        [0x20A2E40],
        0x288,
        (
            "Data for guest monsters that join you during certain story"
            " dungeons.\n\nArray of 18 36-byte entries.\n\nSee the struct definitions"
            " and End45's dungeon data document for more info.\n\ntype: struct"
            " guest_monster[18]"
        ),
    )

    RANK_UP_TABLE = Symbol([0xA30C8], [0x20A30C8], 0xD0, "")

    DS_DOWNLOAD_TEAMS = Symbol(
        [0xA3198],
        [0x20A3198],
        0x70,
        (
            "Seems like this is just a collection of null-terminated lists concatenated"
            " together.\n\nNote: unverified, ported from Irdkwia's notes\n\nstruct"
            " monster_id_16[56]"
        ),
    )

    ARM9_UNKNOWN_PTR__NA_20A2C84 = Symbol(
        [0xA3208], [0x20A3208], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    UNOWN_SPECIES_ADDITIONAL_CHARS = Symbol(
        [0xA320C],
        [0x20A320C],
        0x80,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: enum monster_id[28]",
    )

    MONSTER_SPRITE_DATA = Symbol([0xA332C], [0x20A332C], 0x4B0, "")

    REMOTE_STRINGS = Symbol(
        [0xA4140], [0x20A4140], 0x2C, "Note: unverified, ported from Irdkwia's notes"
    )

    RANK_STRINGS_1 = Symbol(
        [0xA416C], [0x20A416C], 0x30, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_MENU_STRING_IDS_1 = Symbol(
        [0xA419C],
        [0x20A419C],
        0x10,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[8]",
    )

    RANK_STRINGS_2 = Symbol(
        [0xA41AC], [0x20A41AC], 0x30, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_MENU_STRING_IDS_2 = Symbol(
        [0xA41DC],
        [0x20A41DC],
        0x10,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[8]",
    )

    RANK_STRINGS_3 = Symbol(
        [0xA41EC], [0x20A41EC], 0xB4, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_DUNGEON_UNLOCK_TABLE = Symbol(
        [0xA42AC],
        [0x20A42AC],
        0x6,
        (
            "Irdkwia's notes: SpecialDungeonMissions\n\ntype: struct"
            " dungeon_unlock_entry[3]"
        ),
    )

    NO_SEND_ITEM_TABLE = Symbol(
        [0xA42B2],
        [0x20A42B2],
        0x6,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: struct item_id_16[3]",
    )

    ARM9_UNKNOWN_TABLE__NA_20A3CC8 = Symbol(
        [0xA42C8],
        [0x20A42C8],
        0x1C,
        (
            "14*0x2\nLinked to ARM9_UNKNOWN_TABLE__NA_20A3CE4\n\nNote: unverified,"
            " ported from Irdkwia's notes"
        ),
    )

    ARM9_UNKNOWN_TABLE__NA_20A3CE4 = Symbol(
        [0xA42E4],
        [0x20A42E4],
        0x10,
        "8*0x2\n\nNote: unverified, ported from Irdkwia's notes",
    )

    ARM9_UNKNOWN_FUNCTION_TABLE__NA_20A3CF4 = Symbol(
        [0xA42F4],
        [0x20A42F4],
        0x20,
        "Could be related to missions\n\nNote: unverified, ported from Irdkwia's notes",
    )

    MISSION_BANNED_STORY_MONSTERS = Symbol(
        [0xA4314],
        [0x20A4314],
        0x2A,
        (
            "Null-terminated list of monster IDs that can't be used (probably as"
            " clients or targets) when generating missions before a certain point in"
            " the story.\n\nTo be precise, PERFOMANCE_PROGRESS_FLAG[9] must be enabled"
            " so these monsters can appear as mission clients.\n\ntype: struct"
            " monster_id_16[length / 2]"
        ),
    )

    ITEM_DELIVERY_TABLE = Symbol(
        [0xA433E],
        [0x20A433E],
        0x2E,
        (
            "Maybe it is the Item table used for Item Deliveries\n\nNote: unverified,"
            " ported from Irdkwia's notes\n\ntype: struct item_id_16[23]"
        ),
    )

    MISSION_RANK_POINTS = Symbol(
        [0xA436C],
        [0x20A436C],
        0x40,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int[16]",
    )

    MISSION_BANNED_MONSTERS = Symbol(
        [0xA43AC],
        [0x20A43AC],
        0xF8,
        (
            "Null-terminated list of monster IDs that can't be used (probably as"
            " clients or targets) when generating missions.\n\ntype: struct"
            " monster_id_16[124]"
        ),
    )

    MISSION_STRING_IDS = Symbol(
        [0xA44A4],
        [0x20A44A4],
        0x788,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[964]",
    )

    LEVEL_LIST = Symbol(
        [0xA4CEC], [0x20A4CEC], 0x2470, "Note: unverified, ported from Irdkwia's notes"
    )

    EVENTS = Symbol(
        [0xA5BD8],
        [0x20A5BD8],
        0x1584,
        (
            "Table of levels for the script engine, in which scenes can take place."
            " There are a version-dependent number of 12-byte entries.\n\ntype: struct"
            " script_level[length / 12]"
        ),
    )

    ARM9_UNKNOWN_TABLE__NA_20A68BC = Symbol(
        [0xA715C],
        [0x20A715C],
        0xC,
        "6*0x2\n\nNote: unverified, ported from Irdkwia's notes",
    )

    DEMO_TEAMS = Symbol(
        [0xA7168],
        [0x20A7168],
        0x48,
        (
            "18*0x4 (Hero ID 0x2, Partner ID 0x2)\n\nNote: unverified, ported from"
            " Irdkwia's notes"
        ),
    )

    ACTOR_LIST = Symbol(
        [0xA71B0], [0x20A71B0], 0x28F8, "Note: unverified, ported from Irdkwia's notes"
    )

    ENTITIES = Symbol(
        [0xA8890],
        [0x20A8890],
        0x1218,
        (
            "Table of entities for the script engine, which can move around and do"
            " things within a scene. There are 386 12-byte entries.\n\ntype: struct"
            " script_entity[386]"
        ),
    )

    JOB_D_BOX_LAYOUT_1 = Symbol(
        [0xA9AB8], [0x20A9AB8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_1 = Symbol(
        [0xA9AC8], [0x20A9AC8], 0x20, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_2 = Symbol(
        [0xA9AE8], [0x20A9AE8], 0x20, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_3 = Symbol(
        [0xA9B58], [0x20A9B58], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_4 = Symbol(
        [0xA9B70], [0x20A9B70], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_5 = Symbol(
        [0xA9B88], [0x20A9B88], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_6 = Symbol(
        [0xA9BA0], [0x20A9BA0], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_7 = Symbol(
        [0xA9BB8], [0x20A9BB8], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_8 = Symbol(
        [0xA9BD0], [0x20A9BD0], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_9 = Symbol(
        [0xA9BE8], [0x20A9BE8], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_10 = Symbol(
        [0xA9C00], [0x20A9C00], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_11 = Symbol(
        [0xA9C18], [0x20A9C18], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_12 = Symbol(
        [0xA9C30], [0x20A9C30], 0x20, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_13 = Symbol(
        [0xA9C50], [0x20A9C50], 0x20, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_D_BOX_LAYOUT_2 = Symbol(
        [0xA9C70], [0x20A9C70], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_SWAP_ID_TABLE = Symbol(
        [0xA9C80],
        [0x20A9C80],
        0xD4,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " dungeon_id_8[212]"
        ),
    )

    MAP_MARKER_PLACEMENTS = Symbol(
        [0xA9D70],
        [0x20A9D70],
        0x9B0,
        (
            "The map marker position of each dungeon on the Wonder Map.\n\nThis is an"
            " array of 310 map marker structs. Each entry is 8 bytes, and contains"
            " positional information about a dungeon on the map.\n\nSee the struct"
            " definitions and End45's dungeon data document for more info.\n\ntype:"
            " struct map_marker[310]"
        ),
    )

    ARM9_UNKNOWN_TABLE__NA_20A9FB0 = Symbol(
        [0xAA850],
        [0x20AA850],
        0x4974,
        "4701*0x4\n\nNote: unverified, ported from Irdkwia's notes",
    )

    ARM9_UNKNOWN_TABLE__NA_20AE924 = Symbol(
        [0xAF1C4],
        [0x20AF1C4],
        0x2D4,
        "724*0x1\n\nNote: unverified, ported from Irdkwia's notes",
    )

    MEMORY_ALLOCATION_ARENA_GETTERS = Symbol(
        [0xAF7A0],
        [0x20AF7A0],
        0x8,
        (
            "Functions to get the desired memory arena for allocating and freeing heap"
            " memory.\n\ntype: struct mem_arena_getters"
        ),
    )

    PRNG_SEQUENCE_NUM = Symbol(
        [0xAF7CC],
        [0x20AF7CC],
        0x2,
        (
            "[Runtime] The current PRNG sequence number for the general-purpose PRNG."
            " See Rand16Bit for more information on how the general-purpose PRNG works."
        ),
    )

    LOADED_OVERLAY_GROUP_0 = Symbol(
        [0xAFAD0],
        [0x20AFAD0],
        0x4,
        (
            "[Runtime] The overlay group ID of the overlay currently loaded in slot 0."
            " A group ID of 0 denotes no overlay.\n\nOverlay group IDs that can be"
            " loaded in slot 0:\n- 0x06 (overlay 3)\n- 0x07 (overlay 6)\n- 0x08"
            " (overlay 4)\n- 0x09 (overlay 5)\n- 0x0A (overlay 7)\n- 0x0B (overlay"
            " 8)\n- 0x0C (overlay 9)\n- 0x10 (overlay 12)\n- 0x11 (overlay 13)\n- 0x12"
            " (overlay 14)\n- 0x13 (overlay 15)\n- 0x14 (overlay 16)\n- 0x15 (overlay"
            " 17)\n- 0x16 (overlay 18)\n- 0x17 (overlay 19)\n- 0x18 (overlay 20)\n-"
            " 0x19 (overlay 21)\n- 0x1A (overlay 22)\n- 0x1B (overlay 23)\n- 0x1C"
            " (overlay 24)\n- 0x1D (overlay 25)\n- 0x1E (overlay 26)\n- 0x1F (overlay"
            " 27)\n- 0x20 (overlay 28)\n- 0x21 (overlay 30)\n- 0x22 (overlay 31)\n-"
            " 0x23 (overlay 32)\n- 0x24 (overlay 33)\n\ntype: enum overlay_group_id"
        ),
    )

    LOADED_OVERLAY_GROUP_1 = Symbol(
        [0xAFAD4],
        [0x20AFAD4],
        0x4,
        (
            "[Runtime] The overlay group ID of the overlay currently loaded in slot 1."
            " A group ID of 0 denotes no overlay.\n\nOverlay group IDs that can be"
            " loaded in slot 1:\n- 0x4 (overlay 1)\n- 0x5 (overlay 2)\n- 0xD (overlay"
            " 11)\n- 0xE (overlay 29)\n- 0xF (overlay 34)\n\ntype: enum"
            " overlay_group_id"
        ),
    )

    LOADED_OVERLAY_GROUP_2 = Symbol(
        [0xAFAD8],
        [0x20AFAD8],
        0x4,
        (
            "[Runtime] The overlay group ID of the overlay currently loaded in slot 2."
            " A group ID of 0 denotes no overlay.\n\nOverlay group IDs that can be"
            " loaded in slot 2:\n- 0x1 (overlay 0)\n- 0x2 (overlay 10)\n- 0x3 (overlay"
            " 35)\n\ntype: enum overlay_group_id"
        ),
    )

    PACK_FILE_OPENED = Symbol(
        [0xAFF54],
        [0x20AFF54],
        0x4,
        (
            "[Runtime] A pointer to the 6 opened Pack files (listed at"
            " PACK_FILE_PATHS_TABLE)\n\ntype: struct pack_file_opened*"
        ),
    )

    PACK_FILE_PATHS_TABLE = Symbol(
        [0xAFF58],
        [0x20AFF58],
        0x18,
        (
            "List of pointers to path strings to all known pack files.\nThe game uses"
            " this table to load its resources when launching dungeon mode.\n\ntype:"
            " char*[6]"
        ),
    )

    GAME_STATE_VALUES = Symbol([0xAFF70], [0x20AFF70], None, "[Runtime]")

    BAG_ITEMS_PTR_MIRROR = Symbol(
        [0xAFF70],
        [0x20AFF70],
        0x4,
        (
            "[Runtime] Probably a mirror of ram.yml::BAG_ITEMS_PTR?\n\nNote:"
            " unverified, ported from Irdkwia's notes"
        ),
    )

    ITEM_DATA_TABLE_PTRS = Symbol(
        [0xAFF78],
        [0x20AFF78],
        0xC,
        (
            "[Runtime] List of pointers to various item data tables.\n\nThe first two"
            " pointers are definitely item-related (although the order appears to be"
            " flipped between EU/NA?). Not sure about the third pointer."
        ),
    )

    DUNGEON_MOVE_TABLES = Symbol(
        [0xAFFA8],
        [0x20AFFA8],
        None,
        (
            "[Runtime] Seems to be some sort of region (a table of tables?) that holds"
            " pointers to various important tables related to moves."
        ),
    )

    MOVE_DATA_TABLE_PTR = Symbol(
        [0xAFFB0],
        [0x20AFFB0],
        0x4,
        (
            "[Runtime] Points to the contents of the move data table loaded from"
            " waza_p.bin\n\ntype: struct move_data_table*"
        ),
    )

    LOADED_WAN_TABLE_PTR = Symbol(
        None,
        None,
        None,
        "pointer to a wan table\n\nNote: unverified, ported from Irdkwia's notes",
    )

    LANGUAGE_INFO_DATA = Symbol([0xB05A8], [0x20B05A8], None, "[Runtime]")

    TBL_TALK_GROUP_STRING_ID_START = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[6]",
    )

    KEYBOARD_STRING_IDS = Symbol(
        [0xB0718],
        [0x20B0718],
        0x3C,
        "30*0x2\n\nNote: unverified, ported from Irdkwia's notes\n\ntype: int16_t[30]",
    )

    NOTIFY_NOTE = Symbol(
        [0xB0814],
        [0x20B0814],
        0x1,
        "[Runtime] Flag related to saving and loading state?\n\ntype: bool",
    )

    DEFAULT_HERO_ID = Symbol(
        [0xB0818],
        [0x20B0818],
        0x2,
        (
            "The default monster ID for the hero (0x4: Charmander)\n\ntype: struct"
            " monster_id_16"
        ),
    )

    DEFAULT_PARTNER_ID = Symbol(
        [0xB081A],
        [0x20B081A],
        0x2,
        (
            "The default monster ID for the partner (0x1: Bulbasaur)\n\ntype: struct"
            " monster_id_16"
        ),
    )

    GAME_MODE = Symbol([0xB088C], [0x20B088C], 0x1, "[Runtime]\n\ntype: uint8_t")

    GLOBAL_PROGRESS_PTR = Symbol(
        [0xB0890], [0x20B0890], 0x4, "[Runtime]\n\ntype: struct global_progress*"
    )

    ADVENTURE_LOG_PTR = Symbol(
        [0xB0894], [0x20B0894], 0x4, "[Runtime]\n\ntype: struct adventure_log*"
    )

    ITEM_TABLES_PTRS_1 = Symbol(
        [0xB1264],
        [0x20B1264],
        0x68,
        "Irdkwia's notes: 26*0x4, uses MISSION_FLOOR_RANKS_AND_ITEM_LISTS",
    )

    UNOWN_SPECIES_ADDITIONAL_CHAR_PTR_TABLE = Symbol(
        [0xB12F4],
        [0x20B12F4],
        0x70,
        (
            "Uses UNOWN_SPECIES_ADDITIONAL_CHARS\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\ntype: enum monster_id*[28]"
        ),
    )

    PARTY_MONSTERS_PTR = Symbol(
        [0xB1364], [0x20B1364], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_LIST_PTR = Symbol(
        [0xB13BC], [0x20B13BC], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    REMOTE_STRING_PTR_TABLE = Symbol(
        [0xB13C0],
        [0x20B13C0],
        0x1C,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: const char*[7]",
    )

    RANK_STRING_PTR_TABLE = Symbol(
        [0xB13DC],
        [0x20B13DC],
        0x40,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: const char*[16]",
    )

    SMD_EVENTS_FUN_TABLE = Symbol(
        [0xB14D4],
        [0x20B14D4],
        0x1FC,
        (
            "Irdkwia's notes: named DSEEventFunctionPtrTable with length 0x3C0 (note"
            " the disagreement), 240*0x4."
        ),
    )

    MUSIC_DURATION_LOOKUP_TABLE_1 = Symbol(
        [0xB1894],
        [0x20B1894],
        0x100,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[128]",
    )

    MUSIC_DURATION_LOOKUP_TABLE_2 = Symbol(
        [0xB1994],
        [0x20B1994],
        0x200,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int32_t[128]",
    )

    JUICE_BAR_NECTAR_IQ_GAIN = Symbol(
        [0x118B8], [0x20118B8], 0x1, "IQ gain when ingesting nectar at the Juice Bar."
    )

    TEXT_SPEED = Symbol([0x20DF0], [0x2020DF0], None, "Controls text speed.")

    HERO_START_LEVEL = Symbol(
        [0x48B9C], [0x2048B9C], None, "Starting level of the hero."
    )

    PARTNER_START_LEVEL = Symbol(
        [0x48C0C], [0x2048C0C], None, "Starting level of the partner."
    )


class EuArm9Section:
    name = "arm9"
    description = (
        "The main ARM9 binary.\n\nThis is the main binary that gets loaded when the"
        " game is launched, and contains the core code that runs the game, low level"
        " facilities such as memory allocation, compression, other external"
        " dependencies (such as linked functions from libc and libgcc), and the"
        " functions and tables necessary to load overlays and dispatch execution to"
        " them.\n\nSpeaking generally, this is the program run by the Nintendo DS's"
        " main ARM946E-S CPU, which handles all gameplay mechanisms and graphics"
        " rendering."
    )
    loadaddress = 0x2000000
    length = 0xB7D38
    functions = EuArm9Functions
    data = EuArm9Data


class EuItcmFunctions:
    GetKeyN2MSwitch = Symbol(
        [0x1434],
        [0x20B50F4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: key\nr1: switch",
    )

    GetKeyN2M = Symbol(
        [0x1468],
        [0x20B5128],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: key\nreturn: monster ID",
    )

    GetKeyN2MBaseForm = Symbol(
        [0x14D4],
        [0x20B5194],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: key\nreturn: monster ID",
    )

    GetKeyM2NSwitch = Symbol(
        [0x150C],
        [0x20B51CC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nr1: switch",
    )

    GetKeyM2N = Symbol(
        [0x1540],
        [0x20B5200],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn: key",
    )

    GetKeyM2NBaseForm = Symbol(
        [0x15AC],
        [0x20B526C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn: key",
    )

    ShouldMonsterRunAwayVariationOutlawCheck = Symbol(
        [0x2390],
        [0x20B6050],
        None,
        (
            "Calls ShouldMonsterRunAwayVariation. If the result is true, returns true."
            " Otherwise, returns true only if the monster's behavior field is equal to"
            " monster_behavior::BEHAVIOR_FLEEING_OUTLAW.\n\nr0: Entity pointer\nr1:"
            " ?\nreturn: True if ShouldMonsterRunAway returns true or the monster is a"
            " fleeing outlaw"
        ),
    )

    AiMovement = Symbol(
        [0x23C4],
        [0x20B6084],
        None,
        (
            "Used by the AI to determine the direction in which a monster should"
            " move\n\nr0: Entity pointer\nr1: ?"
        ),
    )

    CalculateAiTargetPos = Symbol(
        [0x32C8],
        [0x20B6F88],
        None,
        (
            "Calculates the target position of an AI-controlled monster and stores it"
            " in the monster's ai_target_pos field\n\nr0: Entity pointer"
        ),
    )

    ChooseAiMove = Symbol(
        [0x3658],
        [0x20B7318],
        None,
        (
            "Determines if an AI-controlled monster will use a move and which one it"
            " will use\n\nr0: Entity pointer"
        ),
    )


class EuItcmData:
    MEMORY_ALLOCATION_TABLE = Symbol(
        [0x0],
        [0x20B3CC0],
        0x40,
        (
            "[Runtime] Keeps track of all active heap allocations.\n\nThe memory"
            " allocator in the ARM9 binary uses region-based memory management (see"
            " https://en.wikipedia.org/wiki/Region-based_memory_management). The heap"
            " is broken up into smaller contiguous chunks called arenas (struct"
            " mem_arena), which are in turn broken up into chunks referred to as blocks"
            " (struct mem_block). Most of the time, an allocation results in a block"
            " being split off from a free part of an existing memory arena.\n\nNote:"
            " This symbol isn't actually part of the ITCM, it gets created at runtime"
            " on the spot in RAM that used to contain the code that was moved to the"
            " ITCM.\n\ntype: struct mem_alloc_table"
        ),
    )

    DEFAULT_MEMORY_ARENA = Symbol(
        [0x4],
        [0x20B3CC4],
        0x1C,
        (
            "[Runtime] The default memory allocation arena. This is part of"
            " MEMORY_ALLOCATION_TABLE, but is also referenced on its own by various"
            " functions.\n\nNote: This symbol isn't actually part of the ITCM, it gets"
            " created at runtime on the spot in RAM that used to contain the code that"
            " was moved to the ITCM.\n\ntype: struct mem_arena"
        ),
    )

    DEFAULT_MEMORY_ARENA_BLOCKS = Symbol(
        [0x40],
        [0x20B3D00],
        0x1800,
        (
            "[Runtime] The block array for DEFAULT_MEMORY_ARENA.\n\nNote: This symbol"
            " isn't actually part of the ITCM, it gets created at runtime on the spot"
            " in RAM that used to contain the code that was moved to the ITCM.\n\ntype:"
            " struct mem_block[256]"
        ),
    )


class EuItcmSection:
    name = "itcm"
    description = (
        "The instruction TCM (tightly-coupled memory) and the corresponding region in"
        " the ARM9 binary.\n\nThe ITCM is a special area of low-latency memory meant"
        " for performance-critical routines. It's similar to an instruction cache, but"
        " more predictable. See the ARMv5 Architecture Reference Manual, Chapter B7"
        " (https://developer.arm.com/documentation/ddi0100/i).\n\nThe Nintendo DS ITCM"
        " region is located at 0x0-0x7FFF in memory, but the 32 KiB segment is mirrored"
        " throughout the 16 MiB block from 0x0-0x1FFFFFF. The Explorers of Sky code"
        " seems to reference only the mirror at 0x1FF8000, the closest one to main"
        " memory.\n\nIn Explorers of Sky, a fixed region of the ARM9 binary appears to"
        " be loaded in the ITCM at all times, and seems to contain functions related to"
        " the dungeon AI, among other things. The ITCM has a max capacity of 0x8000,"
        " although not all of it is used."
    )
    loadaddress = 0x20B3CC0
    length = 0x4000
    functions = EuItcmFunctions
    data = EuItcmData


class EuMove_effectsFunctions:
    DoMoveDamage = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage.\nRelevant moves: Many!\n\nThis just wraps"
            " DealDamage with a multiplier of 1 (i.e., the fixed-point number"
            " 0x100).\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3: item"
            " ID\nreturn: whether or not damage was dealt"
        ),
    )

    DoMoveIronTail = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Iron Tail\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageMultihitUntilMiss = Symbol(
        [0xA4],
        [0x23268CC],
        None,
        (
            "Move effect: Deal multihit damage until a strike misses\nRelevant moves:"
            " Ice Ball, Rollout\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveYawn = Symbol(
        [0x104],
        [0x232692C],
        None,
        (
            "Move effect: Yawn\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSleep = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Put target enemies to sleep\nRelevant moves: Lovely Kiss,"
            " Sing, Spore, Grasswhistle, Hypnosis, Sleep Powder, Dark Void\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveNightmare = Symbol(
        [0x17C],
        [0x23269A4],
        None,
        (
            "Move effect: Nightmare\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMorningSun = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Morning Sun\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveVitalThrow = Symbol(
        [0x1F4],
        [0x2326A1C],
        None,
        (
            "Move effect: Vital Throw\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDig = Symbol(
        [0x204],
        [0x2326A2C],
        None,
        (
            "Move effect: Dig\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSweetScent = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Sweet Scent\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveCharm = Symbol(
        [0x2E8],
        [0x2326B10],
        None,
        (
            "Move effect: Charm\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRainDance = Symbol(
        [0x310],
        [0x2326B38],
        None,
        (
            "Move effect: Rain Dance\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHail = Symbol(
        [0x36C],
        [0x2326B94],
        None,
        (
            "Move effect: Hail\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHealStatus = Symbol(
        [0x3C8],
        [0x2326BF0],
        None,
        (
            "Move effect: Heal the team's status conditions\nRelevant moves:"
            " Aromatherapy, Heal Bell, Refresh\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveBubble = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Bubble\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveEncore = Symbol(
        [0x44C],
        [0x2326C74],
        None,
        (
            "Move effect: Encore\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRage = Symbol(
        [0x460],
        [0x2326C88],
        None,
        (
            "Move effect: Rage\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSuperFang = Symbol(
        [0x4A4],
        [0x2326CCC],
        None,
        (
            "Move effect: Super Fang\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePainSplit = Symbol(
        [0x55C],
        [0x2326D84],
        None,
        (
            "Move effect: Pain Split\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveTorment = Symbol(
        [0x648],
        [0x2326E70],
        None,
        (
            "Move effect: Torment\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveStringShot = Symbol(
        [0x790],
        [0x2326FB8],
        None,
        (
            "Move effect: String Shot\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSwagger = Symbol(
        [0x7A8],
        [0x2326FD0],
        None,
        (
            "Move effect: Swagger\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSnore = Symbol(
        [0x7E4],
        [0x232700C],
        None,
        (
            "Move effect: Snore\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveScreech = Symbol(
        [0x888],
        [0x23270B0],
        None,
        (
            "Move effect: Screech\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageCringe30 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage with a 30% chance (ROCK_SLIDE_CRINGE_CHANCE) of"
            " inflicting the cringe status on the defender.\nRelevant moves: Rock"
            " Slide, Astonish, Iron Head, Dark Pulse, Air Slash, Zen Headbutt, Dragon"
            " Rush\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3: item"
            " ID\nreturn: whether or not damage was dealt"
        ),
    )

    DoMoveWeatherBall = Symbol(
        [0x91C],
        [0x2327144],
        None,
        (
            "Move effect: Weather Ball\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveWhirlpool = Symbol(
        [0x990],
        [0x23271B8],
        None,
        (
            "Move effect: Whirlpool\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFakeTears = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Fake Tears\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSpite = Symbol(
        [0xA4C],
        [0x2327274],
        None,
        (
            "Move effect: Spite\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFocusEnergy = Symbol(
        [0xAFC],
        [0x2327324],
        None,
        (
            "Move effect: Focus Energy\nRelevant moves: Focus Energy,"
            " MOVE_TAG_0x1AC\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSmokescreen = Symbol(
        [0xB0C],
        [0x2327334],
        None,
        (
            "Move effect: Smokescreen\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMirrorMove = Symbol(
        [0xB48],
        [0x2327370],
        None,
        (
            "Move effect: Mirror Move\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveOverheat = Symbol(
        [0xB6C],
        [0x2327394],
        None,
        (
            "Move effect: Overheat\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveAuroraBeam = Symbol(
        [0xBD0],
        [0x23273F8],
        None,
        (
            "Move effect: Aurora Beam\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMemento = Symbol(
        [0xC4C],
        [0x2327474],
        None,
        (
            "Move effect: Memento\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveOctazooka = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Octazooka\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFlatter = Symbol(
        [0xD28],
        [0x2327550],
        None,
        (
            "Move effect: Flatter\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveWillOWisp = Symbol(
        [0xD64],
        [0x232758C],
        None,
        (
            "Move effect: Will-O-Wisp\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveReturn = Symbol(
        [0xE00],
        [0x2327628],
        None,
        (
            "Move effect: Return\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveGrudge = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Grudge\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveCounter = Symbol(
        [0xEF4],
        [0x232771C],
        None,
        (
            "Move effect: Give the user the Counter status\nRelevant moves: Pursuit,"
            " Counter, Payback\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageBurn10FlameWheel = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage with a 10% chance (FLAME_WHEEL_BURN_CHANCE) of"
            " burning the defender.\nRelevant moves: Flame Wheel, Lava Plume\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveDamageBurn10 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage with a 10% chance (FLAMETHROWER_BURN_CHANCE) of"
            " burning the defender.\nRelevant moves: Flamethrower, Fire Blast, Heat"
            " Wave, Ember, Fire Punch\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveExpose = Symbol(
        [0x1018],
        [0x2327840],
        None,
        (
            "Move effect: Expose all Ghost-type enemies, and reset evasion"
            " boosts\nRelevant moves: Odor Sleuth, Foresight\n\nr0: attacker"
            " pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn: whether the"
            " move was successfully used"
        ),
    )

    DoMoveDoubleTeam = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Double Team\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveGust = Symbol(
        [0x1060],
        [0x2327888],
        None,
        (
            "Move effect: Gust\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBoostDefense1 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Boost the user's defense by one stage\nRelevant moves:"
            " Harden, Withdraw\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveParalyze = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Paralyze the defender if possible\nRelevant moves: Disable,"
            " Stun Spore, Glare\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBoostAttack1 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Boost the user's attack by one stage\nRelevant moves:"
            " Sharpen, Howl, Meditate\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveRazorWind = Symbol(
        [0x10F8],
        [0x2327920],
        None,
        (
            "Move effect: Razor Wind\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBide = Symbol(
        [0x1188],
        [0x23279B0],
        None,
        (
            "Move effect: Give the user the Bide status\nRelevant moves: Bide, Revenge,"
            " Avalanche\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBideUnleash = Symbol(
        [0x11CC],
        [0x23279F4],
        None,
        (
            "Move effect: Unleashes the Bide status\nRelevant moves: Bide (unleashing),"
            " Revenge (unleashing), Avalanche (unleashing)\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveCrunch = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage with a 20% chance (CRUNCH_LOWER_DEFENSE_CHANCE)"
            " of lowering the defender's defense.\nRelevant moves: Crunch, Shadow Ball"
            " via Nature Power\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether or not damage was dealt"
        ),
    )

    DoMoveDamageCringe20 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage with a 20% chance (BITE_CRINGE_CHANCE) of"
            " inflicting the cringe status on the defender.\nRelevant moves: Bite,"
            " Needle Arm, Stomp, Rolling Kick\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDamageParalyze20 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage with a 20% chance (THUNDER_PARALYZE_CHANCE) of"
            " paralyzing the defender.\nRelevant moves: Thunder, ThunderPunch, Force"
            " Palm, Discharge\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether or not damage was dealt"
        ),
    )

    DoMoveEndeavor = Symbol(
        [0x13CC],
        [0x2327BF4],
        None,
        (
            "Move effect: Endeavor\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFacade = Symbol(
        [0x148C],
        [0x2327CB4],
        None,
        (
            "Move effect: Facade\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageLowerSpeed20 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage with a 20% chance (CONSTRICT_LOWER_SPEED_CHANCE)"
            " of lowering the defender's speed.\nRelevant moves: Constrict,"
            " Bubblebeam\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether or not damage was dealt"
        ),
    )

    DoMoveBrickBreak = Symbol(
        [0x1538],
        [0x2327D60],
        None,
        (
            "Move effect: Brick Break\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDamageLowerSpeed100 = Symbol(
        [0x15A8],
        [0x2327DD0],
        None,
        (
            "Move effect: Deal damage and lower the defender's speed.\nRelevant moves:"
            " Rock Tomb, Icy Wind, Mud Shot\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveFocusPunch = Symbol(
        [0x160C],
        [0x2327E34],
        None,
        (
            "Move effect: Focus Punch\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDamageDrain = Symbol(
        [0x1698],
        [0x2327EC0],
        None,
        (
            "Move effect: Deal draining damage, healing the attacker by a proportion of"
            " the damage dealt.\nRelevant moves: Giga Drain, Leech Life, Mega Drain,"
            " Drain Punch\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether or not damage was dealt"
        ),
    )

    DoMoveReversal = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage with a higher multiplier the lower the attacker's"
            " HP is.\nRelevant moves: Reversal, Flail\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveSmellingSalt = Symbol(
        [0x188C],
        [0x23280B4],
        None,
        (
            "Move effect: SmellingSalt\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMetalSound = Symbol(
        [0x18F4],
        [0x232811C],
        None,
        (
            "Move effect: Metal Sound\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTickle = Symbol(
        [0x1928],
        [0x2328150],
        None,
        (
            "Move effect: Tickle\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveShadowHold = Symbol(
        [0x1984],
        [0x23281AC],
        None,
        (
            "Move effect: Inflict the Shadow Hold status on the defender\nRelevant"
            " moves: Spider Web, Mean Look\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveHaze = Symbol(
        [0x1998],
        [0x23281C0],
        None,
        (
            "Move effect: Haze\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageMultihitFatigue = Symbol(
        [0x19AC],
        [0x23281D4],
        None,
        (
            "Move effect: Deal multihit damage, then confuse the attacker\nRelevant"
            " moves: Outrage, Petal Dance\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDamageWeightDependent = Symbol(
        [0x19F8],
        [0x2328220],
        None,
        (
            "Move effect: Deal damage, multiplied by a weight-dependent"
            " factor.\nRelevant moves: Low Kick, Grass Knot\n\nr0: attacker"
            " pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn: whether or"
            " not damage was dealt"
        ),
    )

    DoMoveDamageBoostAllStats = Symbol(
        [0x1A44],
        [0x232826C],
        None,
        (
            "Move effect: Deal damage, with a 20% (SILVER_WIND_BOOST_CHANCE) to boost"
            " the user's attack, special attack, defense, special defense, and"
            " speed.\nRelevant moves: Silver Wind, AncientPower, Ominous Wind\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveSynthesis = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Synthesis\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBoostSpeed1 = Symbol(
        [0x1B68],
        [0x2328390],
        None,
        (
            "Move effect: Boost the team's movement speed by one stage\nRelevant moves:"
            " Agility, Speed Boost (item effect), MOVE_TAG_0x1AA, Tailwind\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveRapidSpin = Symbol(
        [0x1B80],
        [0x23283A8],
        None,
        (
            "Move effect: Rapid Spin\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSureShot = Symbol(
        [0x1BEC],
        [0x2328414],
        None,
        (
            "Move effect: Give the user the Sure-Shot status\nRelevant moves: Mind"
            " Reader, Lock-On\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveCosmicPower = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Cosmic Power\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSkyAttack = Symbol(
        [0x1C68],
        [0x2328490],
        None,
        (
            "Move effect: Sky Attack\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageFreeze15 = Symbol(
        [0x1D34],
        [0x232855C],
        None,
        (
            "Move effect: Deal damage with a 15% chance (POWDER_SNOW_FREEZE_CHANCE) of"
            " freezing the defender.\nRelevant moves: Powder Snow, Blizzard, Ice Punch,"
            " Ice Beam\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether or not damage was dealt"
        ),
    )

    DoMoveMeteorMash = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Meteor Mash\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveEndure = Symbol(
        [0x1E24],
        [0x232864C],
        None,
        (
            "Move effect: Endure\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveLowerSpeed1 = Symbol(
        [0x1E34],
        [0x232865C],
        None,
        (
            "Move effect: Lower the defender's defense by one stage\nRelevant moves:"
            " Scary Face, Cotton Spore\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDamageConfuse10 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage with a 10% chance (PSYBEAM_CONFUSE_CHANCE) of"
            " confusing the defender.\nRelevant moves: Psybeam, Signal Beam, Confusion,"
            " Chatter, Rock Climb\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePsywave = Symbol(
        [0x1EB8],
        [0x23286E0],
        None,
        (
            "Move effect: Psywave\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageLowerDefensiveStatVariable = Symbol(
        [0x1F1C],
        [0x2328744],
        None,
        (
            "Move effect: Deal damage with some chance of lowering one of the"
            " defender's defensive stats.\nRelevant moves: Psychic, Acid, Seed Flare,"
            " Earth Power, Bug Buzz, Flash Cannon\n\nNote that this move effect handler"
            " has a slightly different parameter list than all the others. Which"
            " defensive stat is lowered, the chance of lowering, and the number of"
            " stages to lower are all specified as arguments by the caller.\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: stat index for the"
            " defensive stat to lower\nstack[0]: number of defensive stat stages to"
            " lower\nstack[1]: percentage chance of lowering the defensive"
            " stat\nstack[2]: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePsychoBoost = Symbol(
        [0x1FA4],
        [0x23287CC],
        None,
        (
            "Move effect: Psycho Boost\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveUproar = Symbol(
        [0x2014],
        [0x232883C],
        None,
        (
            "Move effect: Uproar\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveWaterSpout = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Water Spout\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMovePsychUp = Symbol(
        [0x20D8],
        [0x2328900],
        None,
        (
            "Move effect: Psych Up\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageWithRecoil = Symbol(
        [0x2178],
        [0x23289A0],
        None,
        (
            "Move effect: Deals damage, inflicting recoil damage on the"
            " attacker.\nRelevant moves: Submission, Take Down, Volt Tackle, Wood"
            " Hammer, Brave Bird\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: bool, whether or not damage was dealt"
        ),
    )

    EntityIsValidMoveEffects = Symbol(
        [0x2250, 0x461C, 0x6748, 0x8468],
        [0x2328A78, 0x232AE44, 0x232CF70, 0x232EC90],
        None,
        "See overlay29.yml::EntityIsValid",
    )

    DoMoveRecoverHp = Symbol(
        [0x2274],
        [0x2328A9C],
        None,
        (
            "Move effect: Recover 50% of the user's max HP\nRelevant moves: Recover,"
            " Slack Off\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveEarthquake = Symbol(
        [0x22B8],
        [0x2328AE0],
        None,
        (
            "Move effect: Earthquake\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    GetNaturePowerVariant = Symbol(
        [0x2318],
        [0x2328B40],
        None,
        (
            "Gets the nature power variant for the current dungeon, based on the"
            " tileset ID.\n\nreturn: nature power variant"
        ),
    )

    DoMoveNaturePower = Symbol(
        [0x2354],
        [0x2328B7C],
        None,
        (
            "Move effect: Nature Power\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move (unused)\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveDamageParalyze10 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage with a 10% chance (LICK_PARALZYE_CHANCE) of"
            " paralyzing the defender.\nRelevant moves: Lick, Spark, Body Slam,"
            " DragonBreath\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSelfdestruct = Symbol(
        [0x241C],
        [0x2328C44],
        None,
        (
            "Move effect: Selfdestruct\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveShadowBall = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Shadow Ball\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveCharge = Symbol(
        [0x250C],
        [0x2328D34],
        None,
        (
            "Move effect: Charge\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveThunderbolt = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Thunderbolt\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMist = Symbol(
        [0x25D8],
        [0x2328E00],
        None,
        (
            "Move effect: Mist\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFissure = Symbol(
        [0x25E8],
        [0x2328E10],
        None,
        (
            "Move effect: Fissure\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageCringe10 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage with a 10% chance (EXTRASENSORY_CRINGE_CHANCE) to"
            " inflict the cringe status on the defender.\nRelevant moves: Extrasensory,"
            " Hyper Fang, Bone Club\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSafeguard = Symbol(
        [0x276C],
        [0x2328F94],
        None,
        (
            "Move effect: Safeguard\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveAbsorb = Symbol(
        [0x277C],
        [0x2328FA4],
        None,
        (
            "Move effect: Absorb\n\nThis is essentially identical to DoMoveDamageDrain,"
            " except the ordering of the instructions is slightly different enough to"
            " introduce subtle variations in functionality.\n\nr0: attacker"
            " pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn: whether or"
            " not damage was dealt"
        ),
    )

    DefenderAbilityIsActiveMoveEffects = Symbol(
        [0x2878, 0x4158, 0x6018, 0x8038],
        [0x23290A0, 0x232A980, 0x232C840, 0x232E860],
        None,
        "See overlay29.yml::DefenderAbilityIsActive",
    )

    DoMoveSkillSwap = Symbol(
        [0x28DC],
        [0x2329104],
        None,
        (
            "Move effect: Skill Swap\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSketch = Symbol(
        [0x29D8],
        [0x2329200],
        None,
        (
            "Move effect: Sketch\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHeadbutt = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Headbutt\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDoubleEdge = Symbol(
        [0x2B74],
        [0x232939C],
        None,
        (
            "Move effect: Double-Edge\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSandstorm = Symbol(
        [0x2C3C],
        [0x2329464],
        None,
        (
            "Move effect: Sandstorm\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveLowerAccuracy1 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Lower the defender's accuracy by one stage\nRelevant moves:"
            " Sand-Attack, Kinesis, Flash\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDamagePoison40 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage with a 40% chance (SMOG_POISON_CHANCE) of"
            " poisoning the defender.\nRelevant moves: Smog, Cross Poison, Gunk Shot,"
            " Poison Jab\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether or not damage was dealt"
        ),
    )

    DoMoveGrowth = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Growth\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSacredFire = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Sacred Fire\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveOhko = Symbol(
        [0x2DCC],
        [0x23295F4],
        None,
        (
            "Move effect: Possibly one-hit KO the defender\nRelevant moves: Sheer Cold,"
            " Guillotine\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSolarBeam = Symbol(
        [0x2EB8],
        [0x23296E0],
        None,
        (
            "Move effect: SolarBeam\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSonicBoom = Symbol(
        None,
        None,
        None,
        (
            "Move effect: SonicBoom\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFly = Symbol(
        [0x3028],
        [0x2329850],
        None,
        (
            "Move effect: Fly\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveExplosion = Symbol(
        [0x30B8],
        [0x23298E0],
        None,
        (
            "Move effect: Explosion\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDive = Symbol(
        [0x3110],
        [0x2329938],
        None,
        (
            "Move effect: Dive\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveWaterfall = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Waterfall\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageLowerAccuracy40 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage with a 40% chance"
            " (MUDDY_WATER_LOWER_ACCURACY_CHANCE) of lowering the defender's"
            " accuracy.\nRelevant moves: Muddy Water, Mud Bomb, Mirror Shot\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether or not damage was dealt"
        ),
    )

    DoMoveStockpile = Symbol(
        [0x32B8],
        [0x2329AE0],
        None,
        (
            "Move effect: Stockpile\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveTwister = Symbol(
        [0x3310],
        [0x2329B38],
        None,
        (
            "Move effect: Twister\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveTwineedle = Symbol(
        [0x33A0],
        [0x2329BC8],
        None,
        (
            "Move effect: Twineedle\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRecoverHpTeam = Symbol(
        [0x3438],
        [0x2329C60],
        None,
        (
            "Move effect: Recover 25% HP for all team members\nRelevant moves:"
            " Softboiled, Milk Drink\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMinimize = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Minimize\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSeismicToss = Symbol(
        [0x349C],
        [0x2329CC4],
        None,
        (
            "Move effect: Seismic Toss\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveConfuse = Symbol(
        [0x3610],
        [0x2329E38],
        None,
        (
            "Move effect: Confuse target enemies if possible.\nRelevant moves: Confuse"
            " Ray, Supersonic, Sweet Kiss, Teeter Dance, Totter (item effect)\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveTaunt = Symbol(
        [0x3628],
        [0x2329E50],
        None,
        (
            "Move effect: Taunt\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMoonlight = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Moonlight\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHornDrill = Symbol(
        [0x367C],
        [0x2329EA4],
        None,
        (
            "Move effect: Horn Drill\n\nThis is exactly the same as DoMoveOhko, except"
            " there's a call to SubstitutePlaceholderStringTags at the end.\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveSwordsDance = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Swords Dance\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveConversion = Symbol(
        [0x3798],
        [0x2329FC0],
        None,
        (
            "Move effect: Conversion\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveConversion2 = Symbol(
        [0x38A8],
        [0x232A0D0],
        None,
        (
            "Move effect: Conversion 2\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveHelpingHand = Symbol(
        [0x38B8],
        [0x232A0E0],
        None,
        (
            "Move effect: Helping Hand\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveBoostDefense2 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Boost the defender's defense stat by two stages\nRelevant"
            " moves: Iron Defense, Acid Armor, Barrier\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveWarp = Symbol(
        [0x393C],
        [0x232A164],
        None,
        (
            "Move effect: Warp the target to another tile on the floor\nRelevant moves:"
            " Teleport, Warp (item effect), MOVE_TAG_0x1A8\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveThundershock = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Thundershock\n\nThis is identical to DoMoveDamageParalyze10,"
            " except it uses a different data symbol for the paralysis chance (but it's"
            " still 10%).\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveThunderWave = Symbol(
        [0x39C0],
        [0x232A1E8],
        None,
        (
            "Move effect: Thunder Wave\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveZapCannon = Symbol(
        [0x3A34],
        [0x232A25C],
        None,
        (
            "Move effect: Zap Cannon\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBlock = Symbol(
        [0x3A98],
        [0x232A2C0],
        None,
        (
            "Move effect: Block\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePoison = Symbol(
        [0x3AAC],
        [0x232A2D4],
        None,
        (
            "Move effect: Poison the defender if possible\nRelevant moves: Poison Gas,"
            " PoisonPowder\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveToxic = Symbol(
        [0x3AC4],
        [0x232A2EC],
        None,
        (
            "Move effect: Toxic\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePoisonFang = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Poison Fang\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDamagePoison18 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage with an 18% chance (POISON_STING_POISON_CHANCE)"
            " to poison the defender.\nRelevant moves: Poison Sting, Sludge, Sludge"
            " Bomb\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3: item"
            " ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveJumpKick = Symbol(
        [0x3BB4],
        [0x232A3DC],
        None,
        (
            "Move effect: Jump Kick\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBounce = Symbol(
        [0x3CE0],
        [0x232A508],
        None,
        (
            "Move effect: Bounce\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHiJumpKick = Symbol(
        [0x3DAC],
        [0x232A5D4],
        None,
        (
            "Move effect: Hi Jump Kick\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTriAttack = Symbol(
        [0x3ED8],
        [0x232A700],
        None,
        (
            "Move effect: Tri Attack\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSwapItems = Symbol(
        [0x3F94],
        [0x232A7BC],
        None,
        (
            "Move effect: Swaps the held items of the attacker and defender.\nRelevant"
            " moves: Trick, Switcheroo\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTripleKick = Symbol(
        [0x41BC],
        [0x232A9E4],
        None,
        (
            "Move effect: Triple Kick\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSport = Symbol(
        [0x41F8],
        [0x232AA20],
        None,
        (
            "Move effect: Activate the relevant sport condition (Mud Sport, Water"
            " Sport) on the floor\nRelevant moves: Mud Sport, Water Sport\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveMudSlap = Symbol(
        [0x4224],
        [0x232AA4C],
        None,
        (
            "Move effect: Mud-Slap\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageStealItem = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage and steal the defender's item if"
            " possible.\nRelevant moves: Thief, Covet\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveAmnesia = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Amnesia\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveNightShade = Symbol(
        [0x42BC],
        [0x232AAE4],
        None,
        (
            "Move effect: Night Shade\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveGrowl = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Growl\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSurf = Symbol(
        [0x438C],
        [0x232ABB4],
        None,
        (
            "Move effect: Surf\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRolePlay = Symbol(
        [0x43CC],
        [0x232ABF4],
        None,
        (
            "Move effect: Role Play\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSunnyDay = Symbol(
        [0x4464],
        [0x232AC8C],
        None,
        (
            "Move effect: Sunny Day\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveLowerDefense1 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Lower the defender's defense by one stage\nRelevant moves:"
            " Tail Whip, Leer\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveWish = Symbol(
        [0x44F0],
        [0x232AD18],
        None,
        (
            "Move effect: Wish\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFakeOut = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Fake Out\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSleepTalk = Symbol(
        [0x456C],
        [0x232AD94],
        None,
        (
            "Move effect: Sleep Talk\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePayDay = Symbol(
        [0x4584],
        [0x232ADAC],
        None,
        (
            "Move effect: Pay Day\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveAssist = Symbol(
        [0x4640],
        [0x232AE68],
        None,
        (
            "Move effect: Assist\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRest = Symbol(
        [0x4658],
        [0x232AE80],
        None,
        (
            "Move effect: Rest\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveIngrain = Symbol(
        [0x46C4],
        [0x232AEEC],
        None,
        (
            "Move effect: Ingrain\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSwallow = Symbol(
        [0x46D4],
        [0x232AEFC],
        None,
        (
            "Move effect: Swallow\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveCurse = Symbol(
        [0x472C],
        [0x232AF54],
        None,
        (
            "Move effect: Curse\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSuperpower = Symbol(
        [0x4768],
        [0x232AF90],
        None,
        (
            "Move effect: Superpower\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSteelWing = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Steel Wing\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSpitUp = Symbol(
        [0x4884],
        [0x232B0AC],
        None,
        (
            "Move effect: Spit Up\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDynamicPunch = Symbol(
        [0x48CC],
        [0x232B0F4],
        None,
        (
            "Move effect: DynamicPunch\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveKnockOff = Symbol(
        [0x4930],
        [0x232B158],
        None,
        (
            "Move effect: Knock Off\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSplash = Symbol(
        [0x4B30],
        [0x232B358],
        None,
        (
            "Move effect: Splash\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSetDamage = Symbol(
        [0x4E88],
        [0x232B6B0],
        None,
        (
            "Move effect: Give the user the Set Damage status\nRelevant moves: Doom"
            " Desire, Future Sight\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBellyDrum = Symbol(
        [0x4E98],
        [0x232B6C0],
        None,
        (
            "Move effect: Belly Drum\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveLightScreen = Symbol(
        [0x4F4C],
        [0x232B774],
        None,
        (
            "Move effect: Light Screen\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSecretPower = Symbol(
        [0x4F5C],
        [0x232B784],
        None,
        (
            "Move effect: Secret Power\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDamageConfuse30 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage with a 30% chance (DIZZY_PUNCH_CONFUSE_CHANCE) to"
            " confuse the defender.\nRelevant moves: Dizzy Punch, Water Pulse\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveBulkUp = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Bulk Up\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePause = Symbol(
        [0x51E4],
        [0x232BA0C],
        None,
        (
            "Move effect: Inflicts the Paused status on the defender\nRelevant moves:"
            " Imprison, Observer (item effect), MOVE_TAG_0x1AD\n\nr0: attacker"
            " pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn: whether the"
            " move was successfully used"
        ),
    )

    DoMoveFeatherDance = Symbol(
        None,
        None,
        None,
        (
            "Move effect: FeatherDance\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveBeatUp = Symbol(
        [0x5268],
        [0x232BA90],
        None,
        (
            "Move effect: Beat Up\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBlastBurn = Symbol(
        [0x535C],
        [0x232BB84],
        None,
        (
            "Move effect: Blast Burn\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveCrushClaw = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Crush Claw\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBlazeKick = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Blaze Kick\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePresent = Symbol(
        [0x54B0],
        [0x232BCD8],
        None,
        (
            "Move effect: Present\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveEruption = Symbol(
        [0x55AC],
        [0x232BDD4],
        None,
        (
            "Move effect: Eruption\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveTransform = Symbol(
        [0x5690],
        [0x232BEB8],
        None,
        (
            "Move effect: Transform\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePoisonTail = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Poison Tail\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveBlowback = Symbol(
        [0x5744],
        [0x232BF6C],
        None,
        (
            "Move effect: Blows the defender back\nRelevant moves: Whirlwind, Roar,"
            " Blowback (item effect)\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveCamouflage = Symbol(
        [0x575C],
        [0x232BF84],
        None,
        (
            "Move effect: Camouflage\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveTailGlow = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Tail Glow\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageConstrict10 = Symbol(
        [0x582C],
        [0x232C054],
        None,
        (
            "Move effect: Deal damage with a 10% (WHIRLPOOL_CONSTRICT_CHANCE) chance to"
            " constrict, and with a damage multiplier dependent on the move"
            " used.\nRelevant moves: Clamp, Bind, Sand Tomb, Fire Spin, Magma"
            " Storm\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3: item"
            " ID\nreturn: whether or not damage was dealt"
        ),
    )

    DoMovePerishSong = Symbol(
        [0x58E8],
        [0x232C110],
        None,
        (
            "Move effect: Perish Song\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveWrap = Symbol(
        [0x58FC],
        [0x232C124],
        None,
        (
            "Move effect: Wrap\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSpikes = Symbol(
        [0x590C],
        [0x232C134],
        None,
        (
            "Move effect: Spikes\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMagnitude = Symbol(
        [0x597C],
        [0x232C1A4],
        None,
        (
            "Move effect: Magnitude\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMagicCoat = Symbol(
        [0x5A04],
        [0x232C22C],
        None,
        (
            "Move effect: Magic Coat\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveProtect = Symbol(
        [0x5A14],
        [0x232C23C],
        None,
        (
            "Move effect: Try to give the user the Protect status\nRelevant moves:"
            " Protect, Detect\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDefenseCurl = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Defense Curl\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDecoy = Symbol(
        [0x5A44],
        [0x232C26C],
        None,
        (
            "Move effect: Inflict the Decoy status on the target\nRelevant moves:"
            " Follow Me, Substitute, Decoy Maker (item effect)\n\nr0: attacker"
            " pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn: whether the"
            " move was successfully used"
        ),
    )

    DoMoveMistBall = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Mist Ball\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDestinyBond = Symbol(
        [0x5AE4],
        [0x232C30C],
        None,
        (
            "Move effect: Destiny Bond\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMirrorCoat = Symbol(
        [0x5B18],
        [0x232C340],
        None,
        (
            "Move effect: Mirror Coat\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveCalmMind = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Calm Mind\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHiddenPower = Symbol(
        [0x5B6C],
        [0x232C394],
        None,
        (
            "Move effect: Hidden Power\n\nThis is exactly the same as DoMoveDamage"
            " (both are wrappers around DealDamage), except this function always"
            " returns true.\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMetalClaw = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Metal Claw\n\n Note that this move effect handler has a"
            " slightly different parameter list than all the others. Which offensive"
            " stat is boosted is specified by the caller.\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: stat index for the offensive stat to"
            " boost\nstack[0]: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveAttract = Symbol(
        [0x5C18],
        [0x232C440],
        None,
        (
            "Move effect: Attract\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveCopycat = Symbol(
        [0x5C8C],
        [0x232C4B4],
        None,
        (
            "Move effect: The attacker uses the move last used by enemy it's"
            " facing.\nRelevant moves: Mimic, Copycat\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveFrustration = Symbol(
        [0x5D94],
        [0x232C5BC],
        None,
        (
            "Move effect: Frustration\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveLeechSeed = Symbol(
        [0x5E7C],
        [0x232C6A4],
        None,
        (
            "Move effect: Leech Seed\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMetronome = Symbol(
        [0x5EAC],
        [0x232C6D4],
        None,
        (
            "Move effect: Metronome\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDreamEater = Symbol(
        [0x5F0C],
        [0x232C734],
        None,
        (
            "Move effect: Dream Eater\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSnatch = Symbol(
        [0x607C],
        [0x232C8A4],
        None,
        (
            "Move effect: Snatch\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRecycle = Symbol(
        [0x608C],
        [0x232C8B4],
        None,
        (
            "Move effect: Recycle\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveReflect = Symbol(
        [0x61C0],
        [0x232C9E8],
        None,
        (
            "Move effect: Reflect\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDragonRage = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Dragon Rage\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDragonDance = Symbol(
        [0x6270],
        [0x232CA98],
        None,
        (
            "Move effect: Dragon Dance\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSkullBash = Symbol(
        [0x62AC],
        [0x232CAD4],
        None,
        (
            "Move effect: Skull Bash\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageLowerSpecialDefense50 = Symbol(
        [0x633C],
        [0x232CB64],
        None,
        (
            "Move effect: Deal damage with a 50%"
            " (LUSTER_PURGE_LOWER_SPECIAL_DEFENSE_CHANCE) chance to lower special"
            " defense.\nRelevant moves: Luster Purge, Energy Ball, Focus Blast\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveStruggle = Symbol(
        [0x63EC],
        [0x232CC14],
        None,
        (
            "Move effect: Struggle\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRockSmash = Symbol(
        [0x64C4],
        [0x232CCEC],
        None,
        (
            "Move effect: Rock Smash\nRelevant moves: Rock Smash,"
            " MOVE_UNNAMED_0x169\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSeeTrap = Symbol(
        [0x6548],
        [0x232CD70],
        None,
        (
            "Move effect: See-Trap (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTakeaway = Symbol(
        [0x6558],
        [0x232CD80],
        None,
        (
            "Move effect: Takeaway (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveRebound = Symbol(
        [0x676C],
        [0x232CF94],
        None,
        (
            "Move effect: Rebound (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSwitchPositions = Symbol(
        [0x6780],
        [0x232CFA8],
        None,
        (
            "Move effect: Switches the user's position with positions of other monsters"
            " in the room.\nRelevant moves: Baton Pass, Switcher (item effect)\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveStayAway = Symbol(
        [0x67A8],
        [0x232CFD0],
        None,
        (
            "Move effect: Stay Away (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveCleanse = Symbol(
        [0x67C0],
        [0x232CFE8],
        None,
        (
            "Move effect: Cleanse (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSiesta = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Siesta (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTwoEdge = Symbol(
        [0x6938],
        [0x232D160],
        None,
        (
            "Move effect: Two-Edge (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveNoMove = Symbol(
        [0x6A60],
        [0x232D288],
        None,
        (
            "Move effect: No-Move (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveScan = Symbol(
        [0x6A74],
        [0x232D29C],
        None,
        (
            "Move effect: Scan (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMovePowerEars = Symbol(
        [0x6A84],
        [0x232D2AC],
        None,
        (
            "Move effect: Power-Ears (item effect)\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveTransfer = Symbol(
        [0x6A94],
        [0x232D2BC],
        None,
        (
            "Move effect: Transfer (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSlowDown = Symbol(
        [0x6C5C],
        [0x232D484],
        None,
        (
            "Move effect: Slow Down (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSearchlight = Symbol(
        [0x6C74],
        [0x232D49C],
        None,
        (
            "Move effect: Searchlight (item effect)\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMovePetrify = Symbol(
        [0x6C84],
        [0x232D4AC],
        None,
        (
            "Move effect: Petrifies the target\nRelevant moves: Petrify (item effect),"
            " MOVE_TAG_0x1A9\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePounce = Symbol(
        [0x6C94],
        [0x232D4BC],
        None,
        (
            "Move effect: Pounce (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTrawl = Symbol(
        [0x6CA8],
        [0x232D4D0],
        None,
        (
            "Move effect: Trawl (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveEscape = Symbol(
        [0x6CB8],
        [0x232D4E0],
        None,
        (
            "Move effect: Escape (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDrought = Symbol(
        [0x6D50],
        [0x232D578],
        None,
        (
            "Move effect: Drought (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTrapBuster = Symbol(
        [0x6D60],
        [0x232D588],
        None,
        (
            "Move effect: Trap Buster (item effect)\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveWildCall = Symbol(
        [0x6F0C],
        [0x232D734],
        None,
        (
            "Move effect: Wild Call (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveInvisify = Symbol(
        [0x6FD8],
        [0x232D800],
        None,
        (
            "Move effect: Invisify (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveOneShot = Symbol(
        [0x6FEC],
        [0x232D814],
        None,
        (
            "Move effect: One-Shot (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveHpGauge = Symbol(
        [0x7088],
        [0x232D8B0],
        None,
        (
            "Move effect: HP Gauge (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveVacuumCut = Symbol(
        [0x7098],
        [0x232D8C0],
        None,
        (
            "Move effect: Vacuum Cut\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveReviver = Symbol(
        [0x70C4],
        [0x232D8EC],
        None,
        (
            "Move effect: Reviver (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveShocker = Symbol(
        [0x70DC],
        [0x232D904],
        None,
        (
            "Move effect: Shocker (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveEcho = Symbol(
        [0x70F4],
        [0x232D91C],
        None,
        (
            "Move effect: Echo (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveFamish = Symbol(
        [0x719C],
        [0x232D9C4],
        None,
        (
            "Move effect: Famish (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveOneRoom = Symbol(
        [0x71BC],
        [0x232D9E4],
        None,
        (
            "Move effect: One-Room (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveFillIn = Symbol(
        [0x71CC],
        [0x232D9F4],
        None,
        (
            "Move effect: Fill-In (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTrapper = Symbol(
        [0x7338],
        [0x232DB60],
        None,
        (
            "Move effect: Trapper (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveItemize = Symbol(
        [0x7390],
        [0x232DBB8],
        None,
        (
            "Move effect: Itemize (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveHurl = Symbol(
        [0x7424],
        [0x232DC4C],
        None,
        (
            "Move effect: Hurls the target\nRelevant moves: Strength, Hurl (item"
            " effect), Fling\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMobile = Symbol(
        [0x7434],
        [0x232DC5C],
        None,
        (
            "Move effect: Mobile (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSeeStairs = Symbol(
        [0x7444],
        [0x232DC6C],
        None,
        (
            "Move effect: See Stairs (item effect)\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveLongToss = Symbol(
        [0x7454],
        [0x232DC7C],
        None,
        (
            "Move effect: Long Toss (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMovePierce = Symbol(
        [0x7464],
        [0x232DC8C],
        None,
        (
            "Move effect: Pierce (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoHammerArm = Symbol(
        [0x7474],
        [0x232DC9C],
        None,
        (
            "Move effect: Hammer Arm\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveAquaRing = Symbol(
        [0x74B8],
        [0x232DCE0],
        None,
        (
            "Move effect: Aqua Ring\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveGastroAcid = Symbol(
        [0x74C8],
        [0x232DCF0],
        None,
        (
            "Move effect: Gastro Acid\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveHealingWish = Symbol(
        [0x74E0],
        [0x232DD08],
        None,
        (
            "Move effect: Healing Wish\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveCloseCombat = Symbol(
        [0x7530],
        [0x232DD58],
        None,
        (
            "Move effect: Close Combat\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveLuckyChant = Symbol(
        [0x75B0],
        [0x232DDD8],
        None,
        (
            "Move effect: Lucky Chant\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveGuardSwap = Symbol(
        [0x75C0],
        [0x232DDE8],
        None,
        (
            "Move effect: Guard Swap\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHealOrder = Symbol(
        [0x7620],
        [0x232DE48],
        None,
        (
            "Move effect: Heal Order\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHealBlock = Symbol(
        [0x7648],
        [0x232DE70],
        None,
        (
            "Move effect: Heal Block\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveThunderFang = Symbol(
        [0x7660],
        [0x232DE88],
        None,
        (
            "Move effect: Thunder Fang\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDefog = Symbol(
        [0x76F4],
        [0x232DF1C],
        None,
        (
            "Move effect: Defog\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveTrumpCard = Symbol(
        [0x77A8],
        [0x232DFD0],
        None,
        (
            "Move effect: Trump Card\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveIceFang = Symbol(
        [0x7868],
        [0x232E090],
        None,
        (
            "Move effect: Ice Fang\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePsychoShift = Symbol(
        [0x78F8],
        [0x232E120],
        None,
        (
            "Move effect: Psycho Shift\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveEmbargo = Symbol(
        [0x7918],
        [0x232E140],
        None,
        (
            "Move effect: Embargo\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBrine = Symbol(
        [0x7930],
        [0x232E158],
        None,
        (
            "Move effect: Deal damage, with a 2x multiplier if the defender is at or"
            " below half HP.\nRelevant moves: Brine, Assurance\n\nr0: attacker"
            " pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn: whether the"
            " move was successfully used"
        ),
    )

    DoMoveNaturalGift = Symbol(
        [0x7980],
        [0x232E1A8],
        None,
        (
            "Move effect: Natural Gift\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveGyroBall = Symbol(
        [0x7A40],
        [0x232E268],
        None,
        (
            "Move effect: Gyro Ball\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveShadowForce = Symbol(
        [0x7AA8],
        [0x232E2D0],
        None,
        (
            "Move effect: Shadow Force\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveGravity = Symbol(
        [0x7B44],
        [0x232E36C],
        None,
        (
            "Move effect: Gravity\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveStealthRock = Symbol(
        [0x7B54],
        [0x232E37C],
        None,
        (
            "Move effect: Stealth Rock\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveChargeBeam = Symbol(
        [0x7BC4],
        [0x232E3EC],
        None,
        (
            "Move effect: Charge Beam\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDamageEatItem = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deals damage, and eats any beneficial items the defender is"
            " holding.\nRelevant moves: Pluck, Bug Bite\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveAcupressure = Symbol(
        [0x7CE8],
        [0x232E510],
        None,
        (
            "Move effect: Acupressure\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMagnetRise = Symbol(
        [0x7E6C],
        [0x232E694],
        None,
        (
            "Move effect: Magnet Rise\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveToxicSpikes = Symbol(
        [0x7E7C],
        [0x232E6A4],
        None,
        (
            "Move effect: Toxic Spikes\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveLastResort = Symbol(
        [0x7EEC],
        [0x232E714],
        None,
        (
            "Move effect: Last Resort\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTrickRoom = Symbol(
        [0x7F90],
        [0x232E7B8],
        None,
        (
            "Move effect: Trick Room\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveWorrySeed = Symbol(
        [0x7FC4],
        [0x232E7EC],
        None,
        (
            "Move effect: Worry Seed\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageHpDependent = Symbol(
        [0x809C],
        [0x232E8C4],
        None,
        (
            "Move effect: Deal damage, with a multiplier dependent on the defender's"
            " current HP.\nRelevant moves: Wring Out, Crush Grip\n\nr0: attacker"
            " pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn: whether the"
            " move was successfully used"
        ),
    )

    DoMoveHeartSwap = Symbol(
        [0x8150],
        [0x232E978],
        None,
        (
            "Move effect: Heart Swap\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRoost = Symbol(
        [0x81E0],
        [0x232EA08],
        None,
        (
            "Move effect: Roost\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePowerSwap = Symbol(
        [0x829C],
        [0x232EAC4],
        None,
        (
            "Move effect: Power Swap\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePowerTrick = Symbol(
        [0x82FC],
        [0x232EB24],
        None,
        (
            "Move effect: Power Trick\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveFeint = Symbol(
        [0x8310],
        [0x232EB38],
        None,
        (
            "Move effect: Feint\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFlareBlitz = Symbol(
        [0x8348],
        [0x232EB70],
        None,
        (
            "Move effect: Flare Blitz\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDefendOrder = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Defend Order\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveFireFang = Symbol(
        [0x84D0],
        [0x232ECF8],
        None,
        (
            "Move effect: Fire Fang\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveLunarDance = Symbol(
        [0x8580],
        [0x232EDA8],
        None,
        (
            "Move effect: Lunar Dance\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMiracleEye = Symbol(
        [0x85E8],
        [0x232EE10],
        None,
        (
            "Move effect: Miracle Eye\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveWakeUpSlap = Symbol(
        [0x8618],
        [0x232EE40],
        None,
        (
            "Move effect: Wake-Up Slap\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMetalBurst = Symbol(
        [0x86A4],
        [0x232EECC],
        None,
        (
            "Move effect: Metal Burst\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveHeadSmash = Symbol(
        [0x86B8],
        [0x232EEE0],
        None,
        (
            "Move effect: Head Smash\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveCaptivate = Symbol(
        [0x8778],
        [0x232EFA0],
        None,
        (
            "Move effect: Captivate\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveLeafStorm = Symbol(
        [0x883C],
        [0x232F064],
        None,
        (
            "Move effect: Leaf Storm\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDracoMeteor = Symbol(
        [0x8894],
        [0x232F0BC],
        None,
        (
            "Move effect: Draco Meteor\n\nNote that this move effect handler has an"
            " extra parameter that can be used to disable the special attack"
            " drop.\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3: item"
            " ID\nr4: disable special attack drop\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveRockPolish = Symbol(
        [0x88F8],
        [0x232F120],
        None,
        (
            "Move effect: Rock Polish\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveNastyPlot = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Nasty Plot\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveTag0x1AB = Symbol(
        None,
        None,
        None,
        (
            "Move effect: MOVE_TAG_0x1AB\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTag0x1A6 = Symbol(
        [0x8968],
        [0x232F190],
        None,
        (
            "Move effect: MOVE_TAG_0x1A6\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTag0x1A7 = Symbol(
        [0x89AC],
        [0x232F1D4],
        None,
        (
            "Move effect: MOVE_TAG_0x1A7\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )


class EuMove_effectsData:
    LUNAR_DANCE_PP_RESTORATION = Symbol(
        None, None, None, "The amount of PP restored by Lunar Dance (999)."
    )


class EuMove_effectsSection:
    name = "move_effects"
    description = (
        "Move effect handlers for individual moves, called by ExecuteMoveEffect (and"
        " also the Metronome and Nature Power tables).\n\nThis subregion contains only"
        " the move effect handlers themselves, and not necessarily all the utility"
        " functions used by the move effect handlers (such as the damage calculation"
        " functions). These supporting utilities are in the main overlay29 block."
    )
    loadaddress = 0x2326828
    length = 0x8A24
    functions = EuMove_effectsFunctions
    data = EuMove_effectsData


class EuOverlay0Functions:
    pass


class EuOverlay0Data:
    TOP_MENU_MUSIC_ID = Symbol(
        [0x15F4], [0x22BE9B4], None, "Music ID to play in the top menu."
    )


class EuOverlay0Section:
    name = "overlay0"
    description = (
        "Likely contains supporting data and code related to the top menu.\n\nThis is"
        " loaded together with overlay 1 while in the top menu. Since it's in overlay"
        " group 2 (together with overlay 10, which is another 'data' overlay), this"
        " overlay probably plays a similar role. It mentions several files from the"
        " BACK folder that are known backgrounds for the top menu."
    )
    loadaddress = 0x22BD3C0
    length = 0x60880
    functions = EuOverlay0Functions
    data = EuOverlay0Data


class EuOverlay1Functions:
    CreateMainMenus = Symbol(
        [0x7B88],
        [0x23318C8],
        None,
        (
            "Prepares the top menu and sub menu, adding the different options that"
            " compose them.\n\nContains multiple calls to AddMainMenuOption and"
            " AddSubMenuOption. Some of them are conditionally executed depending on"
            " which options should be unlocked.\n\nNo params."
        ),
    )

    AddMainMenuOption = Symbol(
        [0x7FFC],
        [0x2331D3C],
        None,
        (
            "Adds an option to the top menu.\n\nThis function is called for each one of"
            " the options in the top menu. It loops the MAIN_MENU data field, if the"
            " specified action ID does not exist there, the option won't be"
            " added.\n\nr0: Action ID\nr1: True if the option should be enabled, false"
            " otherwise"
        ),
    )

    AddSubMenuOption = Symbol(
        [0x80D4],
        [0x2331E14],
        None,
        (
            "Adds an option to the 'Other' submenu on the top menu.\n\nThis function is"
            " called for each one of the options in the submenu. It loops the SUBMENU"
            " data field, if the specified action ID does not exist there, the option"
            " won't be added.\n\nr0: Action ID\nr1: True if the option should be"
            " enabled, false otherwise"
        ),
    )


class EuOverlay1Data:
    PRINTS_STRINGS = Symbol(
        [0x11B38], [0x233B878], 0x1E8, "Note: unverified, ported from Irdkwia's notes"
    )

    PRINTS_STRUCT = Symbol(
        [0x11D20],
        [0x233BA60],
        0x1F0,
        "62*0x8\n\nNote: unverified, ported from Irdkwia's notes",
    )

    OVERLAY1_D_BOX_LAYOUT_1 = Symbol(
        [0x11F24], [0x233BC64], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY1_D_BOX_LAYOUT_2 = Symbol(
        [0x11F34], [0x233BC74], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY1_D_BOX_LAYOUT_3 = Symbol(
        [0x11F44], [0x233BC84], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY1_D_BOX_LAYOUT_4 = Symbol(
        [0x11F54], [0x233BC94], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    CONTINUE_CHOICE = Symbol([0x11F74], [0x233BCB4], 0x20, "")

    SUBMENU = Symbol([0x11F94], [0x233BCD4], 0x48, "")

    MAIN_MENU = Symbol([0x11FDC], [0x233BD1C], 0xA0, "")

    OVERLAY1_D_BOX_LAYOUT_5 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY1_D_BOX_LAYOUT_6 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY1_D_BOX_LAYOUT_7 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    MAIN_MENU_CONFIRM = Symbol([0x12158], [0x233BE98], 0x18, "")

    OVERLAY1_D_BOX_LAYOUT_8 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY1_D_BOX_LAYOUT_9 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    MAIN_DEBUG_MENU_1 = Symbol([0x1221C], [0x233BF5C], 0x60, "")

    OVERLAY1_D_BOX_LAYOUT_10 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    MAIN_DEBUG_MENU_2 = Symbol([0x1229C], [0x233BFDC], 0x38, "")


class EuOverlay1Section:
    name = "overlay1"
    description = (
        "Likely controls the top menu.\n\nThis is loaded together with overlay 0 while"
        " in the top menu. Since it's in overlay group 1 (together with other 'main'"
        " overlays like overlay 11 and overlay 29), this is probably the"
        " controller.\n\nSeems to contain code related to Wi-Fi rescue. It mentions"
        " several files from the GROUND and BACK folders."
    )
    loadaddress = 0x2329D40
    length = 0x12C80
    functions = EuOverlay1Functions
    data = EuOverlay1Data


class EuOverlay10Functions:
    SprintfStatic = Symbol(
        [0x9CC, 0x4DD4],
        [0x22BDD8C, 0x22C2194],
        None,
        (
            "Statically defined copy of sprintf(3) in overlay 10. See arm9.yml for more"
            " information.\n\nr0: str\nr1: format\n...: variadic\nreturn: number of"
            " characters printed, excluding the null-terminator"
        ),
    )

    GetEffectAnimation = Symbol(
        [0x3420],
        [0x22C07E0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: anim_id\nreturn:"
            " effect animation pointer"
        ),
    )

    GetMoveAnimation = Symbol(
        [0x3434],
        [0x22C07F4],
        None,
        (
            "Get the move animation corresponding to the given move ID.\n\nr0:"
            " move_id\nreturn: move animation pointer"
        ),
    )

    GetSpecialMonsterMoveAnimation = Symbol(
        [0x3448],
        [0x22C0808],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ent_id\nreturn:"
            " special monster move animation pointer"
        ),
    )

    GetTrapAnimation = Symbol(
        [0x345C],
        [0x22C081C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: trap_id\nreturn: trap"
            " animation"
        ),
    )

    GetItemAnimation1 = Symbol(
        [0x3470],
        [0x22C0830],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item_id\nreturn:"
            " first field of the item animation info"
        ),
    )

    GetItemAnimation2 = Symbol(
        [0x3484],
        [0x22C0844],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item_id\nreturn:"
            " second field of the item animation info"
        ),
    )

    GetMoveAnimationSpeed = Symbol(
        [0x3498],
        [0x22C0858],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: move_id\nreturn:"
            " anim_ent_ptr (This might be a mistake? It seems to be an integer, not a"
            " pointer)"
        ),
    )

    CheckEndDungeon = Symbol(
        [0x5E24],
        [0x22C31E4],
        None,
        (
            "Do the stuff when you lose in a dungeon.\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: End condition code? Seems to control what tasks"
            " get run and what transition happens when the dungeon ends\nreturn: return"
            " code?"
        ),
    )


class EuOverlay10Data:
    FIRST_DUNGEON_WITH_MONSTER_HOUSE_TRAPS = Symbol(
        [0x79A4],
        [0x22C4D64],
        0x1,
        (
            "The first dungeon that can have extra traps spawn in Monster Houses, Dark"
            " Hill\n\ntype: struct dungeon_id_8"
        ),
    )

    BAD_POISON_DAMAGE_COOLDOWN = Symbol(
        [0x79AC],
        [0x22C4D6C],
        0x2,
        "The number of turns between passive bad poison (toxic) damage.",
    )

    PROTEIN_STAT_BOOST = Symbol(
        [0x79B8],
        [0x22C4D78],
        0x2,
        "The permanent attack boost from ingesting a Protein.",
    )

    WATERFALL_CRINGE_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Waterfall inflicting the cringe status, as a percentage (30%).",
    )

    AURORA_BEAM_LOWER_ATTACK_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Aurora Beam halving attack, as a percentage (60%).",
    )

    SPAWN_CAP_NO_MONSTER_HOUSE = Symbol(
        [0x79C8],
        [0x22C4D88],
        0x2,
        (
            "The maximum number of enemies that can spawn on a floor without a monster"
            " house (15)."
        ),
    )

    OREN_BERRY_DAMAGE = Symbol(
        [0x79D0], [0x22C4D90], 0x2, "Damage dealt by eating an Oren Berry."
    )

    IRON_TAIL_LOWER_DEFENSE_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Iron Tail lowering defense, as a percentage (30%).",
    )

    TWINEEDLE_POISON_CHANCE = Symbol(
        None, None, None, "The chance of Twineedle poisoning, as a percentage (20%)."
    )

    EXTRASENSORY_CRINGE_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Extrasensory (and others, see DoMoveDamageCringe10)"
            " inflicting the cringe status, as a percentage (10%)."
        ),
    )

    ROCK_SLIDE_CRINGE_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Rock Slide (and others, see DoMoveDamageCringe30) inflicting"
            " the cringe status, as a percentage (30%)"
        ),
    )

    CRUNCH_LOWER_DEFENSE_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Crunch (and others, see DoMoveDamageLowerDef20) lowering"
            " defense, as a percentage (20%)."
        ),
    )

    UNOWN_STONE_DROP_CHANCE = Symbol(
        [0x7A0C],
        [0x22C4DCC],
        0x2,
        "The chance of an Unown dropping an Unown stone, as a percentage (21%).",
    )

    SITRUS_BERRY_HP_RESTORATION = Symbol(
        [0x7A10],
        [0x22C4DD0],
        0x2,
        "The amount of HP restored by eating a Sitrus Berry.",
    )

    MUDDY_WATER_LOWER_ACCURACY_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Muddy Water (and others, see DoMoveDamageLowerAccuracy40)"
            " lowering accuracy, as a percentage (40%)."
        ),
    )

    SILVER_WIND_BOOST_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Silver Wind (and others, see DoMoveDamageBoostAllStats)"
            " boosting all stats, as a percentage (20%)."
        ),
    )

    POISON_TAIL_POISON_CHANCE = Symbol(
        None, None, None, "The chance of Poison Tail poisoning, as a percentage (10%)."
    )

    THUNDERSHOCK_PARALYZE_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Thundershock paralyzing, as a percentage (10%).",
    )

    BOUNCE_PARALYZE_CHANCE = Symbol(
        None, None, None, "The chance of Bounce paralyzing, as a percentage (30%)"
    )

    HEADBUTT_CRINGE_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Headbutt inflicting the cringe status, as a percentage (25%).",
    )

    FIRE_FANG_CRINGE_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Fire Fang inflicting the cringe status, as a percentage (25%).",
    )

    SACRED_FIRE_BURN_CHANCE = Symbol(
        None, None, None, "The chance of Sacred Fire burning, as a percentage (50%)."
    )

    WHIRLPOOL_CONSTRICTION_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Whirlpool inflicting the constriction status, as a"
            " percentage (10%)."
        ),
    )

    EXP_ELITE_EXP_BOOST = Symbol(
        [0x7A40],
        [0x22C4E00],
        0x2,
        "The percentage increase in experience from the Exp. Elite IQ skill",
    )

    MONSTER_HOUSE_MAX_NON_MONSTER_SPAWNS = Symbol(
        [0x7A44],
        [0x22C4E04],
        0x2,
        (
            "The maximum number of extra non-monster spawns (items/traps) in a Monster"
            " House, 7"
        ),
    )

    HEAL_ORDER_HP_RESTORATION = Symbol(
        None, None, None, "The amount of HP restored by Heal Order (40)."
    )

    STEEL_WING_BOOST_DEFENSE_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Steel Wing boosting defense, as a percentage (20%).",
    )

    GOLD_THORN_POWER = Symbol(
        [0x7A68], [0x22C4E28], 0x2, "Attack power for Golden Thorns."
    )

    SPAWN_COOLDOWN = Symbol(
        [0x7A74],
        [0x22C4E34],
        0x2,
        "The number of turns between enemy spawns under normal conditions.",
    )

    MIST_BALL_LOWER_SPECIAL_ATTACK_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Mist Ball lowering special attack, as a percentage (50%).",
    )

    CHARGE_BEAM_BOOST_SPECIAL_ATTACK_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Charge Beam boosting special attack, as a percentage (40%).",
    )

    ORAN_BERRY_FULL_HP_BOOST = Symbol(
        [0x7A8C],
        [0x22C4E4C],
        0x2,
        "The permanent HP boost from eating an Oran Berry at full HP (0).",
    )

    LIFE_SEED_HP_BOOST = Symbol(
        [0x7A90], [0x22C4E50], 0x2, "The permanent HP boost from eating a Life Seed."
    )

    OCTAZOOKA_LOWER_ACCURACY_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Octazooka lowering accuracy, as a percentage (60%).",
    )

    LUSTER_PURGE_LOWER_SPECIAL_DEFENSE_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Luster Purge (and others, see"
            " DoMoveDamageLowerSpecialDefense50) lowering special defense, as a"
            " percentage (50%)."
        ),
    )

    CONSTRICT_LOWER_SPEED_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Constrict (and others, see DoMoveDamageLowerSpeed20)"
            " lowering speed, as a percentage (20%)."
        ),
    )

    ICE_FANG_FREEZE_CHANCE = Symbol(
        None, None, None, "The chance of Ice Fang freezing, as a percentage (15%)."
    )

    SMOG_POISON_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Smog (and others, see DoMoveDamagePoison40) poisoning, as a"
            " percentage (40%)."
        ),
    )

    LICK_PARALYZE_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Lick (and others, see DoMoveDamageParalyze10) paralyzing, as"
            " a percentage (10%)."
        ),
    )

    THUNDER_FANG_PARALYZE_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Thunder Fang paralyzing, as a percentage (10%).",
    )

    BITE_CRINGE_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Bite (and others, see DoMoveDamageCringe20) inflicting the"
            " cringe status, as a percentage (20%)"
        ),
    )

    SKY_ATTACK_CRINGE_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Sky Attack inflicting the cringe status, as a percentage (25%).",
    )

    ICE_FANG_CRINGE_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Ice Fang inflicting the cringe status, as a percentage (25%).",
    )

    BLAZE_KICK_BURN_CHANCE = Symbol(
        None, None, None, "The chance of Blaze Kick burning, as a percentage (10%)."
    )

    FLAMETHROWER_BURN_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Flamethrower (and others, see DoMoveDamageBurn10) burning,"
            " as a percentage (10%)."
        ),
    )

    DIZZY_PUNCH_CONFUSE_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Dizzy Punch (and others, see DoMoveDamageConfuse30)"
            " confusing, as a percentage (30%)."
        ),
    )

    SECRET_POWER_EFFECT_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Secret Power inflicting an effect, as a percentage (30%).",
    )

    METAL_CLAW_BOOST_ATTACK_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Metal Claw boosting attack, as a percentage (20%).",
    )

    SONICBOOM_FIXED_DAMAGE = Symbol(
        None, None, None, "The amount of fixed damage dealt by SonicBoom (20)."
    )

    EXCLUSIVE_ITEM_EXP_BOOST = Symbol(
        [0x7B24],
        [0x22C4EE4],
        0x2,
        "The percentage increase in experience from exp-boosting exclusive items.",
    )

    AFTERMATH_CHANCE = Symbol(
        [0x7B2C],
        [0x22C4EEC],
        0x2,
        "The chance of the Aftermath ability activating, as a percentage (50%).",
    )

    INTIMIDATOR_ACTIVATION_CHANCE = Symbol(
        [0x7B50],
        [0x22C4F10],
        0x2,
        "The percentage chance that Intimidator will activate.",
    )

    ORAN_BERRY_HP_RESTORATION = Symbol(
        [0x7B84], [0x22C4F44], 0x2, "The amount of HP restored by eating a Oran Berry."
    )

    SITRUS_BERRY_FULL_HP_BOOST = Symbol(
        [0x7B8C],
        [0x22C4F4C],
        0x2,
        "The permanent HP boost from eating a Sitrus Berry at full HP.",
    )

    SNORE_CRINGE_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Snore inflicting the cringe status, as a percentage (30%).",
    )

    METEOR_MASH_BOOST_ATTACK_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Meteor Mash boosting attack, as a percentage (20%).",
    )

    CRUSH_CLAW_LOWER_DEFENSE_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Crush Claw lowering defense, as a percentage (50%).",
    )

    BURN_DAMAGE_COOLDOWN = Symbol(
        [0x7BA8], [0x22C4F68], 0x2, "The number of turns between passive burn damage."
    )

    SHADOW_BALL_LOWER_SPECIAL_DEFENSE_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Shadow Ball lowering special defense, as a percentage (20%).",
    )

    STICK_POWER = Symbol([0x7BBC], [0x22C4F7C], 0x2, "Attack power for Sticks.")

    BUBBLE_LOWER_SPEED_CHANCE = Symbol(
        None, None, None, "The chance of Bubble lowering speed, as a percentage (10%)."
    )

    POWDER_SNOW_FREEZE_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Powder Snow (and others, see DoMoveDamageFreeze15) freezing,"
            " as a percentage (15%)."
        ),
    )

    POISON_STING_POISON_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Poison Sting (and others, see DoMoveDamagePoison18)"
            " poisoning, as a percentage (18%)."
        ),
    )

    SPAWN_COOLDOWN_THIEF_ALERT = Symbol(
        [0x7BD8],
        [0x22C4F98],
        0x2,
        (
            "The number of turns between enemy spawns when the Thief Alert condition is"
            " active."
        ),
    )

    POISON_FANG_POISON_CHANCE = Symbol(
        None, None, None, "The chance of Poison Fang poisoning, as a percentage (30%)."
    )

    THUNDER_PARALYZE_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Thunder (and others, see DoMoveDamageParalyze20) paralyzing,"
            " as a percentage (20%)"
        ),
    )

    THUNDERBOLT_PARALYZE_CHANCE = Symbol(
        None, None, None, "The chance of Thunderbolt paralyzing, as a percentage (15%)."
    )

    MONSTER_HOUSE_MAX_MONSTER_SPAWNS = Symbol(
        [0x7BF8],
        [0x22C4FB8],
        0x2,
        (
            "The maximum number of monster spawns in a Monster House, 30, but"
            " multiplied by 2/3 for some reason (so the actual maximum is 45)"
        ),
    )

    TWISTER_CRINGE_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Twister inflicting the cringe status, as a percentage (10%).",
    )

    SPEED_BOOST_TURNS = Symbol(
        [0x7C04],
        [0x22C4FC4],
        0x2,
        (
            "Number of turns (250) after which Speed Boost will trigger and increase"
            " speed by one stage."
        ),
    )

    FAKE_OUT_CRINGE_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Fake Out inflicting the cringe status, as a percentage (35%).",
    )

    THUNDER_FANG_CRINGE_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Thunder Fang inflicting the cringe status, as a percentage"
            " (25%)."
        ),
    )

    FLARE_BLITZ_BURN_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Flare Blitz burning, as a percentage (25%). This value is"
            " also used for the Fire Fang burn chance."
        ),
    )

    FLAME_WHEEL_BURN_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Flame Wheel (and others, see DoMoveDamageBurn10FlameWheel)"
            " burning, as a percentage (10%)."
        ),
    )

    PSYBEAM_CONFUSE_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Psybeam (and others, see DoMoveDamageConfuse10) confusing,"
            " as a percentage (10%)."
        ),
    )

    TRI_ATTACK_STATUS_CHANCE = Symbol(
        None,
        None,
        None,
        (
            "The chance of Tri Attack inflicting any status condition, as a percentage"
            " (20%)."
        ),
    )

    MIRACLE_CHEST_EXP_BOOST = Symbol(
        [0x7C30],
        [0x22C4FF0],
        0x2,
        "The percentage increase in experience from the Miracle Chest item",
    )

    WONDER_CHEST_EXP_BOOST = Symbol(
        [0x7C34],
        [0x22C4FF4],
        0x2,
        "The percentage increase in experience from the Wonder Chest item",
    )

    SPAWN_CAP_WITH_MONSTER_HOUSE = Symbol(
        [0x7C3C],
        [0x22C4FFC],
        0x2,
        (
            "The maximum number of enemies that can spawn on a floor with a monster"
            " house, not counting those in the monster house (4)."
        ),
    )

    POISON_DAMAGE_COOLDOWN = Symbol(
        [0x7C40], [0x22C5000], 0x2, "The number of turns between passive poison damage."
    )

    GEO_PEBBLE_DAMAGE = Symbol(
        [0x7C4C], [0x22C500C], 0x2, "Damage dealt by Geo Pebbles."
    )

    GRAVELEROCK_DAMAGE = Symbol(
        [0x7C50], [0x22C5010], 0x2, "Damage dealt by Gravelerocks."
    )

    RARE_FOSSIL_DAMAGE = Symbol(
        [0x7C54], [0x22C5014], 0x2, "Damage dealt by Rare Fossils."
    )

    GINSENG_CHANCE_3 = Symbol(
        [0x7C58],
        [0x22C5018],
        0x2,
        (
            "The percentage chance for...something to be set to 3 in a calculation"
            " related to the Ginseng boost."
        ),
    )

    ZINC_STAT_BOOST = Symbol(
        [0x7C5C],
        [0x22C501C],
        0x2,
        "The permanent special defense boost from ingesting a Zinc.",
    )

    IRON_STAT_BOOST = Symbol(
        [0x7C60],
        [0x22C5020],
        0x2,
        "The permanent defense boost from ingesting an Iron.",
    )

    CALCIUM_STAT_BOOST = Symbol(
        [0x7C64],
        [0x22C5024],
        0x2,
        "The permanent special attack boost from ingesting a Calcium.",
    )

    DRAGON_RAGE_FIXED_DAMAGE = Symbol(
        None, None, None, "The amount of fixed damage dealt by Dragon Rage (30)."
    )

    CORSOLA_TWIG_POWER = Symbol(
        [0x7C70], [0x22C5030], 0x2, "Attack power for Corsola Twigs."
    )

    CACNEA_SPIKE_POWER = Symbol(
        [0x7C74], [0x22C5034], 0x2, "Attack power for Cacnea Spikes."
    )

    GOLD_FANG_POWER = Symbol([0x7C78], [0x22C5038], 0x2, "Attack power for Gold Fangs.")

    SILVER_SPIKE_POWER = Symbol(
        [0x7C7C], [0x22C503C], 0x2, "Attack power for Silver Spikes."
    )

    IRON_THORN_POWER = Symbol(
        [0x7C80], [0x22C5040], 0x2, "Attack power for Iron Thorns."
    )

    HEALING_WISH_HP_RESTORATION = Symbol(
        None,
        None,
        None,
        (
            "The amount of HP restored by Healing Wish (999). This also applies to"
            " Lunar Dance."
        ),
    )

    FACADE_DAMAGE_MULTIPLIER = Symbol(
        None,
        None,
        None,
        (
            "The Facade damage multiplier for users with a status condition, as a"
            " binary fixed-point number with 8 fraction bits (0x200 -> 2x)."
        ),
    )

    IMPRISON_TURN_RANGE = Symbol(
        None,
        None,
        None,
        (
            "The turn range for the Paused status inflicted by Imprison, [3,"
            " 6).\n\ntype: int16_t[2]"
        ),
    )

    SLEEP_TURN_RANGE = Symbol(
        [0x7CB8],
        [0x22C5078],
        0x4,
        (
            "Appears to control the range of turns for which the sleep condition can"
            " last.\n\nThe first two bytes are the low value of the range, and the"
            " later two bytes are the high value."
        ),
    )

    NIGHTMARE_TURN_RANGE = Symbol(
        None,
        None,
        None,
        (
            "The turn range for the Nightmare status inflicted by Nightmare, [4,"
            " 8).\n\ntype: int16_t[2]"
        ),
    )

    REST_TURN_RANGE = Symbol(
        None,
        None,
        None,
        (
            "The turn range for the Napping status inflicted by Rest, [1, 4).\n\ntype:"
            " int16_t[2]"
        ),
    )

    SPORT_CONDITION_TURN_RANGE = Symbol(
        None,
        None,
        None,
        (
            "The turn range for the sport conditions activated by Mud Sport and Water"
            " Sport, [10, 12).\n\ntype: int16_t[2]"
        ),
    )

    SURE_SHOT_TURN_RANGE = Symbol(
        None,
        None,
        None,
        (
            "The turn range for the Sure Shot status inflicted by Mind Reader and"
            " Lock-On, [10, 12).\n\ntype: int16_t[2]"
        ),
    )

    SMOKESCREEN_TURN_RANGE = Symbol(
        None,
        None,
        None,
        (
            "The turn range for the Whiffer status inflicted by Smokescreen, [1,"
            " 4).\n\ntype: int16_t[2]"
        ),
    )

    POWER_PITCHER_DAMAGE_MULTIPLIER = Symbol(
        [0x7D90],
        [0x22C5150],
        0x4,
        (
            "The multiplier for projectile damage from Power Pitcher (1.5), as a binary"
            " fixed-point number (8 fraction bits)"
        ),
    )

    AIR_BLADE_DAMAGE_MULTIPLIER = Symbol(
        [0x7DDC],
        [0x22C519C],
        0x4,
        (
            "The multiplier for damage from the Air Blade (1.5), as a binary"
            " fixed-point number (8 fraction bits)"
        ),
    )

    HIDDEN_STAIRS_SPAWN_CHANCE_MULTIPLIER = Symbol(
        [0x7DE8],
        [0x22C51A8],
        0x4,
        (
            "The hidden stairs spawn chance multiplier (~1.2) as a binary fixed-point"
            " number (8 fraction bits), if applicable. See"
            " ShouldBoostHiddenStairsSpawnChance in overlay 29."
        ),
    )

    YAWN_TURN_RANGE = Symbol(
        None,
        None,
        None,
        (
            "The turn range for the Yawning status inflicted by Yawn, [2, 2].\n\ntype:"
            " int16_t[2]"
        ),
    )

    SPEED_BOOST_TURN_RANGE = Symbol(
        [0x7E20],
        [0x22C51E0],
        0x4,
        (
            "Appears to control the range of turns for which a speed boost can"
            " last.\n\nThe first two bytes are the low value of the range, and the"
            " later two bytes are the high value."
        ),
    )

    SYNTHESIS_HP_RESTORATION_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Maps each weather type (by index, see enum weather_id) to the"
            " corresponding HP restoration value for Synthesis.\n\ntype: int16_t[8]"
        ),
    )

    ROOST_HP_RESTORATION_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Maps each weather type (by index, see enum weather_id) to the"
            " corresponding HP restoration value for Roost.\n\nEvery entry in this"
            " table is 40.\n\ntype: int16_t[8]"
        ),
    )

    MOONLIGHT_HP_RESTORATION_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Maps each weather type (by index, see enum weather_id) to the"
            " corresponding HP restoration value for Moonlight.\n\ntype: int16_t[8]"
        ),
    )

    MORNING_SUN_HP_RESTORATION_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Maps each weather type (by index, see enum weather_id) to the"
            " corresponding HP restoration value for Morning Sun.\n\ntype: int16_t[8]"
        ),
    )

    WEATHER_ATTRIBUTE_TABLE = Symbol(
        [0x8204],
        [0x22C55C4],
        0x30,
        (
            "Maps each weather type (by index, see enum weather_id) to the"
            " corresponding Weather Ball type and Castform form.\n\ntype: struct"
            " weather_attributes[8]"
        ),
    )

    OFFENSIVE_STAT_STAGE_MULTIPLIERS = Symbol(
        [0x8330],
        [0x22C56F0],
        0x54,
        (
            "Table of multipliers for offensive stats (attack/special attack) for each"
            " stage 0-20, as binary fixed-point numbers (8 fraction bits)"
        ),
    )

    DEFENSIVE_STAT_STAGE_MULTIPLIERS = Symbol(
        [0x8384],
        [0x22C5744],
        0x54,
        (
            "Table of multipliers for defensive stats (defense/special defense) for"
            " each stage 0-20, as binary fixed-point numbers (8 fraction bits)"
        ),
    )

    NATURE_POWER_TABLE = Symbol(
        [0x83D8],
        [0x22C5798],
        0x78,
        (
            "Maps enum nature_power_variant to the associated move ID and effect"
            " handler.\n\ntype: struct wildcard_move_desc[15]"
        ),
    )

    APPLES_AND_BERRIES_ITEM_IDS = Symbol(
        [0x8450],
        [0x22C5810],
        0x84,
        (
            "Table of item IDs for Apples and Berries, which trigger the exclusive item"
            " effect EXCLUSIVE_EFF_RECOVER_HP_FROM_APPLES_AND_BERRIES.\n\ntype: struct"
            " item_id_16[66]"
        ),
    )

    RECRUITMENT_LEVEL_BOOST_TABLE = Symbol(
        [0x85FC],
        [0x22C59BC],
        0xCC,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[102]",
    )

    NATURAL_GIFT_ITEM_TABLE = Symbol(
        [0x86C8],
        [0x22C5A88],
        0xCC,
        (
            "Maps items to their type and base power if used with Natural Gift.\n\nAny"
            " item not listed in this table explicitly will be Normal type with a base"
            " power of 1 when used with Natural Gift.\n\ntype: struct"
            " natural_gift_item_info[34]"
        ),
    )

    RANDOM_MUSIC_ID_TABLE = Symbol(
        [0x8794],
        [0x22C5B54],
        0xF0,
        (
            "Table of music IDs for dungeons with a random assortment of music"
            " tracks.\n\nThis is a table with 30 rows, each with 4 2-byte music IDs."
            " Each row contains the possible music IDs for a given group, from which"
            " the music track will be selected randomly.\n\ntype: struct"
            " music_id_16[30][4]"
        ),
    )

    SHOP_ITEM_CHANCES = Symbol(
        [0x8884],
        [0x22C5C44],
        0x120,
        "8 * 6 * 3 * 0x2\n\nNote: unverified, ported from Irdkwia's notes",
    )

    MALE_ACCURACY_STAGE_MULTIPLIERS = Symbol(
        [0x89A4],
        [0x22C5D64],
        0x54,
        (
            "Table of multipliers for the accuracy stat for males for each stage 0-20,"
            " as binary fixed-point numbers (8 fraction bits)"
        ),
    )

    MALE_EVASION_STAGE_MULTIPLIERS = Symbol(
        [0x89F8],
        [0x22C5DB8],
        0x54,
        (
            "Table of multipliers for the evasion stat for males for each stage 0-20,"
            " as binary fixed-point numbers (8 fraction bits)"
        ),
    )

    FEMALE_ACCURACY_STAGE_MULTIPLIERS = Symbol(
        [0x8A4C],
        [0x22C5E0C],
        0x54,
        (
            "Table of multipliers for the accuracy stat for females for each stage"
            " 0-20, as binary fixed-point numbers (8 fraction bits)"
        ),
    )

    FEMALE_EVASION_STAGE_MULTIPLIERS = Symbol(
        [0x8AA0],
        [0x22C5E60],
        0x54,
        (
            "Table of multipliers for the evasion stat for females for each stage 0-20,"
            " as binary fixed-point numbers (8 fraction bits)"
        ),
    )

    MUSIC_ID_TABLE = Symbol(
        [0x8AF4],
        [0x22C5EB4],
        0x154,
        (
            "List of music IDs used in dungeons with a single music track.\n\nThis is"
            " an array of 170 2-byte music IDs, and is indexed into by the music value"
            " in the floor properties struct for a given floor. Music IDs with the"
            " highest bit set (0x8000) are indexes into the"
            " RANDOM_MUSIC_ID_TABLE.\n\ntype: struct music_id_16[170] (or not a music"
            " ID if the highest bit is set)"
        ),
    )

    TYPE_MATCHUP_TABLE = Symbol(
        [0x8C48],
        [0x22C6008],
        0x288,
        (
            "Table of type matchups.\n\nEach row corresponds to the type matchups of a"
            " specific attack type, with each entry within the row specifying the"
            " type's effectiveness against a target type.\n\ntype: struct"
            " type_matchup_table"
        ),
    )

    FIXED_ROOM_MONSTER_SPAWN_STATS_TABLE = Symbol(
        [0x8ED0],
        [0x22C6290],
        0x4A4,
        (
            "Table of stats for monsters that can spawn in fixed rooms, pointed into by"
            " the FIXED_ROOM_MONSTER_SPAWN_TABLE.\n\nThis is an array of 99 12-byte"
            " entries containing stat spreads for one monster entry each.\n\ntype:"
            " struct fixed_room_monster_spawn_stats_entry[99]"
        ),
    )

    METRONOME_TABLE = Symbol(
        [0x9374],
        [0x22C6734],
        0x540,
        (
            "Something to do with the moves that Metronome can turn into.\n\ntype:"
            " struct wildcard_move_desc[168]"
        ),
    )

    TILESET_PROPERTIES = Symbol(
        [0x98B4], [0x22C6C74], 0x954, "type: struct tileset_property[199]"
    )

    FIXED_ROOM_PROPERTIES_TABLE = Symbol(
        [0xA208],
        [0x22C75C8],
        0xC00,
        (
            "Table of properties for fixed rooms.\n\nThis is an array of 256 12-byte"
            " entries containing properties for a given fixed room ID.\n\nSee the"
            " struct definitions and End45's dungeon data document for more"
            " info.\n\ntype: struct fixed_room_properties_entry[256]"
        ),
    )

    TRAP_ANIMATION_INFO = Symbol(
        [0xAFE8],
        [0x22C83A8],
        0x34,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " trap_animation[26]"
        ),
    )

    ITEM_ANIMATION_INFO = Symbol(
        [0xB01C],
        [0x22C83DC],
        0x15E0,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " item_animation[1400]"
        ),
    )

    MOVE_ANIMATION_INFO = Symbol(
        [0xC5FC], [0x22C99BC], 0x34C8, "type: struct move_animation[563]"
    )

    EFFECT_ANIMATION_INFO = Symbol(
        [0xFAC4],
        [0x22CCE84],
        0x4C90,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " effect_animation[700]"
        ),
    )

    SPECIAL_MONSTER_MOVE_ANIMATION_INFO = Symbol(
        [0x14754],
        [0x22D1B14],
        0xADF4,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " special_monster_move_animation[7422]"
        ),
    )


class EuOverlay10Section:
    name = "overlay10"
    description = (
        "Appears to be used both during ground mode and dungeon mode. With dungeon"
        " mode, whereas overlay 29 contains the main dungeon engine, this overlay seems"
        " to contain routines and data for dungeon mechanics."
    )
    loadaddress = 0x22BD3C0
    length = 0x1F7A0
    functions = EuOverlay10Functions
    data = EuOverlay10Data


class EuOverlay11Functions:
    FuncThatCallsCommandParsing = Symbol([0xF24], [0x22DDAA4], None, "")

    ScriptCommandParsing = Symbol([0x1B24], [0x22DE6A4], None, "")

    SsbLoad2 = Symbol([0x84BC], [0x22E503C], None, "")

    StationLoadHanger = Symbol([0x8994], [0x22E5514], None, "")

    ScriptStationLoadTalk = Symbol([0x91A4], [0x22E5D24], None, "")

    SsbLoad1 = Symbol([0x9B10], [0x22E6690], None, "")

    ScriptSpecialProcessCall = Symbol(
        [0xAED8],
        [0x22E7A58],
        None,
        (
            "Processes calls to the OPCODE_PROCESS_SPECIAL script opcode.\n\nr0: some"
            " struct containing a callback of some sort, only used for special process"
            " ID 18\nr1: special process ID\nr2: first argument, if relevant? Probably"
            " corresponds to the second parameter of OPCODE_PROCESS_SPECIAL\nr3: second"
            " argument, if relevant? Probably corresponds to the third parameter of"
            " OPCODE_PROCESS_SPECIAL\nreturn: return value of the special process if it"
            " has one, otherwise 0"
        ),
    )

    GetSpecialRecruitmentSpecies = Symbol(
        [0xBDFC],
        [0x22E897C],
        None,
        (
            "Returns an entry from RECRUITMENT_TABLE_SPECIES.\n\nNote: This indexes"
            " without doing bounds checking.\n\nr0: index into"
            " RECRUITMENT_TABLE_SPECIES\nreturn: enum monster_id"
        ),
    )

    PrepareMenuAcceptTeamMember = Symbol(
        [0xBE40],
        [0x22E89C0],
        None,
        (
            "Implements SPECIAL_PROC_PREPARE_MENU_ACCEPT_TEAM_MEMBER (see"
            " ScriptSpecialProcessCall).\n\nr0: index into RECRUITMENT_TABLE_SPECIES"
        ),
    )

    InitRandomNpcJobs = Symbol(
        [0xBEE4],
        [0x22E8A64],
        None,
        (
            "Implements SPECIAL_PROC_INIT_RANDOM_NPC_JOBS (see"
            " ScriptSpecialProcessCall).\n\nr0: job type? 0 is a random NPC job, 1 is a"
            " bottle mission\nr1: ?"
        ),
    )

    GetRandomNpcJobType = Symbol(
        [0xBF7C],
        [0x22E8AFC],
        None,
        (
            "Implements SPECIAL_PROC_GET_RANDOM_NPC_JOB_TYPE (see"
            " ScriptSpecialProcessCall).\n\nreturn: job type?"
        ),
    )

    GetRandomNpcJobSubtype = Symbol(
        [0xBF94],
        [0x22E8B14],
        None,
        (
            "Implements SPECIAL_PROC_GET_RANDOM_NPC_JOB_SUBTYPE (see"
            " ScriptSpecialProcessCall).\n\nreturn: job subtype?"
        ),
    )

    GetRandomNpcJobStillAvailable = Symbol(
        [0xBFB0],
        [0x22E8B30],
        None,
        (
            "Implements SPECIAL_PROC_GET_RANDOM_NPC_JOB_STILL_AVAILABLE (see"
            " ScriptSpecialProcessCall).\n\nreturn: bool"
        ),
    )

    AcceptRandomNpcJob = Symbol(
        [0xC018],
        [0x22E8B98],
        None,
        (
            "Implements SPECIAL_PROC_ACCEPT_RANDOM_NPC_JOB (see"
            " ScriptSpecialProcessCall).\n\nreturn: bool"
        ),
    )

    GroundMainLoop = Symbol(
        [0xC534],
        [0x22E90B4],
        None,
        (
            "Appears to be the main loop for ground mode.\n\nBased on debug print"
            " statements and general code structure, it seems contain a core loop, and"
            " dispatches to various functions in response to different events.\n\nr0:"
            " mode, which is stored globally and used in switch statements for"
            " dispatch\nreturn: return code"
        ),
    )

    GetAllocArenaGround = Symbol(
        [0xD11C],
        [0x22E9C9C],
        None,
        (
            "The GetAllocArena function used for ground mode. See SetMemAllocatorParams"
            " for more information.\n\nr0: initial memory arena pointer, or null\nr1:"
            " flags (see MemAlloc)\nreturn: memory arena pointer, or null"
        ),
    )

    GetFreeArenaGround = Symbol(
        [0xD180],
        [0x22E9D00],
        None,
        (
            "The GetFreeArena function used for ground mode. See SetMemAllocatorParams"
            " for more information.\n\nr0: initial memory arena pointer, or null\nr1:"
            " pointer to free\nreturn: memory arena pointer, or null"
        ),
    )

    GroundMainReturnDungeon = Symbol(
        [0xD1D4],
        [0x22E9D54],
        None,
        (
            "Implements SPECIAL_PROC_RETURN_DUNGEON (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    GroundMainNextDay = Symbol(
        [0xD1F8],
        [0x22E9D78],
        None,
        (
            "Implements SPECIAL_PROC_NEXT_DAY (see ScriptSpecialProcessCall).\n\nNo"
            " params."
        ),
    )

    JumpToTitleScreen = Symbol(
        [0xD39C],
        [0x22E9F1C],
        None,
        (
            "Implements SPECIAL_PROC_JUMP_TO_TITLE_SCREEN and SPECIAL_PROC_0x1A (see"
            " ScriptSpecialProcessCall).\n\nr0: int, argument value for"
            " SPECIAL_PROC_JUMP_TO_TITLE_SCREEN and -1 for SPECIAL_PROC_0x1A\nreturn:"
            " bool (but note that the special process ignores this and always"
            " returns 0)"
        ),
    )

    ReturnToTitleScreen = Symbol(
        [0xD454],
        [0x22E9FD4],
        None,
        (
            "Implements SPECIAL_PROC_RETURN_TO_TITLE_SCREEN (see"
            " ScriptSpecialProcessCall).\n\nr0: fade duration\nreturn: bool (but note"
            " that the special process ignores this and always returns 0)"
        ),
    )

    ScriptSpecialProcess0x16 = Symbol(
        [0xD4B4],
        [0x22EA034],
        None,
        "Implements SPECIAL_PROC_0x16 (see ScriptSpecialProcessCall).\n\nr0: bool",
    )

    LoadBackgroundAttributes = Symbol(
        [0xF900],
        [0x22EC480],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output]"
            " bg_attr_str\nr1: bg_id"
        ),
    )

    LoadMapType10 = Symbol(
        [0x10AE4],
        [0x22ED664],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output]"
            " buffer_ptr\nr1: map_id\nr2: dungeon_info_str\nr3: additional_info"
        ),
    )

    LoadMapType11 = Symbol(
        [0x11004],
        [0x22EDB84],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output]"
            " buffer_ptr\nr1: map_id\nr2: dungeon_info_str\nr3: additional_info"
        ),
    )

    GetSpecialLayoutBackground = Symbol(
        [0x15380],
        [0x22F1F00],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: bg_id\nr1:"
            " dungeon_info_str\nr2: additional_info\nr3: copy_fixed_room_layout"
        ),
    )

    SetAnimDataFields = Symbol(
        [0x1863C],
        [0x22F51BC],
        None,
        "Sets some fields on the animation struct?\n\nr0: animation pointer\nr1: ?",
    )

    SetAnimDataFieldsWrapper = Symbol(
        [0x1877C],
        [0x22F52FC],
        None,
        "Calls SetAnimDataFields with the second argument right-shifted by 16.",
    )

    InitAnimDataFromOtherAnimData = Symbol(
        [0x18A84],
        [0x22F5604],
        None,
        (
            "Appears to partially copy some animation data into another animation"
            " struct, plus doing extra initialization on the destination struct.\n\nr0:"
            " dst\nr1: src"
        ),
    )

    SetAnimDataFields2 = Symbol(
        [0x19108],
        [0x22F5C88],
        None,
        (
            "Sets some fields on the animation struct, based on the params?\n\nr0:"
            " animation pointer\nr1: flags\nr2: ?"
        ),
    )

    LoadObjectAnimData = Symbol(
        [0x1AC80],
        [0x22F7800],
        None,
        (
            "Loads the animation (WAN) data for a given object index?\n\nr0: animation"
            " pointer\nr1: object index\nr2: flags"
        ),
    )

    InitAnimDataFromOtherAnimDataVeneer = Symbol(
        None,
        None,
        None,
        (
            "Likely a linker-generated veneer for InitAnimDataFromOtherAnimData.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " dst\nr1: src"
        ),
    )

    AnimRelatedFunction = Symbol(
        None,
        None,
        None,
        (
            "Does more stuff related to animations...probably?\n\nr0: animation"
            " pointer?\nothers: ?"
        ),
    )

    SprintfStatic = Symbol(
        [0x2CCE8],
        [0x2309868],
        None,
        (
            "Statically defined copy of sprintf(3) in overlay 11. See arm9.yml for more"
            " information.\n\nr0: str\nr1: format\n...: variadic\nreturn: number of"
            " characters printed, excluding the null-terminator"
        ),
    )

    StatusUpdate = Symbol(
        [0x378F8],
        [0x2314478],
        None,
        (
            "Implements SPECIAL_PROC_STATUS_UPDATE (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )


class EuOverlay11Data:
    OVERLAY11_UNKNOWN_TABLE__NA_2316A38 = Symbol(
        None,
        None,
        None,
        (
            "Multiple entries are pointers to the string 'script.c'\n\nNote:"
            " unverified, ported from Irdkwia's notes\n\ntype: undefined4[40]"
        ),
    )

    SCRIPT_COMMAND_PARSING_DATA = Symbol(
        None, None, None, "Used by ScriptCommandParsing somehow"
    )

    SCRIPT_OP_CODE_NAMES = Symbol(
        None,
        None,
        None,
        (
            "Opcode name strings pointed to by entries in SCRIPT_OP_CODES"
            " (script_opcode::name)"
        ),
    )

    SCRIPT_OP_CODES = Symbol(
        [0x3C470],
        [0x2318FF0],
        0xBF8,
        (
            "Table of opcodes for the script engine. There are 383 8-byte"
            " entries.\n\nThese opcodes underpin the various ExplorerScript functions"
            " you can call in the SkyTemple SSB debugger.\n\ntype: struct"
            " script_opcode_table"
        ),
    )

    OVERLAY11_DEBUG_STRINGS = Symbol(
        None,
        None,
        None,
        "Strings used with various debug printing functions throughout the overlay",
    )

    C_ROUTINE_NAMES = Symbol(
        None,
        None,
        None,
        (
            "Common routine name strings pointed to by entries in C_ROUTINES"
            " (common_routine::name)"
        ),
    )

    C_ROUTINES = Symbol(
        [0x40688],
        [0x231D208],
        None,
        (
            "Common routines used within the unionall.ssb script (the master script)."
            " There are 701 8-byte entries.\n\nThese routines underpin the"
            " ExplorerScript coroutines you can call in the SkyTemple SSB"
            " debugger.\n\ntype: struct common_routine_table"
        ),
    )

    GROUND_WEATHER_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " ground_weather_entry[12]"
        ),
    )

    GROUND_WAN_FILES_TABLE = Symbol(
        [0x41CA0],
        [0x231E820],
        0x10BC,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: char[343][12]",
    )

    OBJECTS = Symbol(
        [0x42D5C],
        [0x231F8DC],
        0x1AAC,
        (
            "Table of objects for the script engine, which can be placed in scenes."
            " There are a version-dependent number of 12-byte entries.\n\ntype: struct"
            " script_object[length / 12]"
        ),
    )

    RECRUITMENT_TABLE_LOCATIONS = Symbol(
        [0x44844],
        [0x23213C4],
        0x16,
        (
            "Table of dungeon IDs corresponding to entries in"
            " RECRUITMENT_TABLE_SPECIES.\n\ntype: struct dungeon_id_16[22]"
        ),
    )

    RECRUITMENT_TABLE_LEVELS = Symbol(
        [0x4485C],
        [0x23213DC],
        0x2C,
        (
            "Table of levels for recruited Pokémon, corresponding to entries in"
            " RECRUITMENT_TABLE_SPECIES.\n\ntype: int16_t[22]"
        ),
    )

    RECRUITMENT_TABLE_SPECIES = Symbol(
        [0x44888],
        [0x2321408],
        0x2C,
        (
            "Table of Pokémon recruited at special locations, such as at the ends of"
            " certain dungeons (e.g., Dialga or the Seven Treasures legendaries) or"
            " during a cutscene (e.g., Cresselia and Manaphy).\n\nInterestingly, this"
            " includes both Heatran genders. It also includes Darkrai for some"
            " reason?\n\ntype: struct monster_id_16[22]"
        ),
    )

    LEVEL_TILEMAP_LIST = Symbol(
        [0x44CDC],
        [0x232185C],
        0x288,
        (
            "Irdkwia's notes: FIXED_FLOOR_GROUND_ASSOCIATION\n\ntype: struct"
            " level_tilemap_list_entry[81]"
        ),
    )

    OVERLAY11_OVERLAY_LOAD_TABLE = Symbol(
        [0x4701C],
        [0x2323B9C],
        0x150,
        (
            "The overlays that can be loaded while this one is loaded.\n\nEach entry is"
            " 16 bytes, consisting of:\n- overlay group ID (see arm9.yml or enum"
            " overlay_group_id in the C headers for a mapping between group ID and"
            " overlay number)\n- function pointer to entry point\n- function pointer to"
            " destructor\n- possibly function pointer to frame-update"
            " function?\n\ntype: struct overlay_load_entry[21]"
        ),
    )

    UNIONALL_RAM_ADDRESS = Symbol([0x48C64], [0x23257E4], None, "[Runtime]")

    GROUND_STATE_MAP = Symbol([0x48C80], [0x2325800], None, "[Runtime]")

    GROUND_STATE_PTRS = Symbol(
        [0x48CB4],
        [0x2325834],
        0x18,
        (
            "Host pointers to multiple structure used for performing an overworld"
            " scene\n\ntype: struct main_ground_data"
        ),
    )


class EuOverlay11Section:
    name = "overlay11"
    description = (
        "The script engine.\n\nThis is the 'main' overlay of ground mode. The script"
        " engine is what runs the ground mode scripts contained in the SCRIPT folder,"
        " which are written in a custom scripting language. These scripts encode things"
        " like cutscenes, screen transitions, ground mode events, and tons of other"
        " things related to ground mode."
    )
    loadaddress = 0x22DCB80
    length = 0x48E40
    functions = EuOverlay11Functions
    data = EuOverlay11Data


class EuOverlay12Functions:
    pass


class EuOverlay12Data:
    pass


class EuOverlay12Section:
    name = "overlay12"
    description = "Unused; all zeroes."
    loadaddress = 0x238AC80
    length = 0x20
    functions = EuOverlay12Functions
    data = EuOverlay12Data


class EuOverlay13Functions:
    EntryOverlay13 = Symbol(
        [0x0],
        [0x238AC80],
        None,
        (
            "Main function of this overlay.\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nNo params."
        ),
    )

    ExitOverlay13 = Symbol(
        [0x50],
        [0x238ACD0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    Overlay13SwitchFunctionNa238A1C8 = Symbol(
        [0x88],
        [0x238AD08],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: int?",
    )

    Overlay13SwitchFunctionNa238A574 = Symbol(
        [0x434],
        [0x238B0B4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GetPersonality = Symbol(
        [0x1C68],
        [0x238C8E8],
        None,
        (
            "Returns the personality obtained after answering all the questions.\n\nThe"
            " value to return is determined by checking the points obtained for each"
            " the personalities and returning the one with the highest amount of"
            " points.\n\nreturn: Personality (0-15)"
        ),
    )

    GetOptionStringFromID = Symbol(
        [0x1CB0],
        [0x238C930],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes. The first parameter and the"
            " return value point to the same string (which is passed directly into"
            " PreprocessString as the first argument), so I'm not sure why they're"
            " named differently... Seems like a mistake?\n\nr0: menu_id\nr1:"
            " option_id\nreturn: process"
        ),
    )

    WaitForNextStep = Symbol(
        [0x1D0C],
        [0x238C98C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: switch_case",
    )


class EuOverlay13Data:
    QUIZ_BORDER_COLOR_TABLE = Symbol(
        [0x1ED0], [0x238CB50], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    PORTRAIT_ATTRIBUTES = Symbol(
        [0x1ED4], [0x238CB54], 0x8, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_MALE_FEMALE_BOOST_TABLE = Symbol(
        [0x1EDC], [0x238CB5C], 0x8, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY13_UNKNOWN_STRUCT__NA_238C024 = Symbol(
        [0x1EE4], [0x238CB64], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_D_BOX_LAYOUT_1 = Symbol(
        [0x1EF4], [0x238CB74], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_D_BOX_LAYOUT_2 = Symbol(
        [0x1F04], [0x238CB84], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_D_BOX_LAYOUT_3 = Symbol(
        [0x1F14], [0x238CB94], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_D_BOX_LAYOUT_4 = Symbol(
        [0x1F24], [0x238CBA4], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_MENU_1 = Symbol(
        [0x1F34], [0x238CBB4], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    STARTERS_PARTNER_IDS = Symbol(
        [0x1F4C], [0x238CBCC], 0x2A, "type: struct monster_id_16[21]"
    )

    STARTERS_HERO_IDS = Symbol(
        [0x1F78], [0x238CBF8], 0x40, "type: struct monster_id_16[32]"
    )

    STARTERS_TYPE_INCOMPATIBILITY_TABLE = Symbol(
        [0x1FB8], [0x238CC38], 0x54, "Note: unverified, ported from Irdkwia's notes"
    )

    STARTERS_STRINGS = Symbol(
        [0x200C], [0x238CC8C], 0x60, "Irdkwia's notes: InsightsStringIDs"
    )

    QUIZ_QUESTION_STRINGS = Symbol([0x206C], [0x238CCEC], 0x84, "0x2 * (66 questions)")

    QUIZ_ANSWER_STRINGS = Symbol(
        [0x20F0], [0x238CD70], 0x160, "0x2 * (175 answers + null-terminator)"
    )

    QUIZ_ANSWER_POINTS = Symbol(
        [0x2250],
        [0x238CED0],
        0xAE0,
        "0x10 * (174 answers?)\n\nNote: unverified, ported from Irdkwia's notes",
    )

    OVERLAY13_RESERVED_SPACE = Symbol(
        [0x2D50], [0x238D9D0], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY13_UNKNOWN_POINTER__NA_238CEA0 = Symbol(
        [0x2D60], [0x238D9E0], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY13_UNKNOWN_POINTER__NA_238CEA4 = Symbol(
        [0x2D64], [0x238D9E4], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY13_UNKNOWN_POINTER__NA_238CEA8 = Symbol(
        [0x2D68], [0x238D9E8], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_D_BOX_LAYOUT_5 = Symbol(
        [0x2D6C], [0x238D9EC], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_D_BOX_LAYOUT_6 = Symbol(
        [0x2D7C], [0x238D9FC], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_DEBUG_MENU = Symbol(
        [0x2D8C], [0x238DA0C], 0x48, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY13_UNKNOWN_STRUCT__NA_238CF14 = Symbol(
        [0x2DD4], [0x238DA54], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_QUESTION_ANSWER_ASSOCIATIONS = Symbol(
        [0x2DE4],
        [0x238DA64],
        0x84,
        "0x2 * (66 questions)\n\nNote: unverified, ported from Irdkwia's notes",
    )


class EuOverlay13Section:
    name = "overlay13"
    description = (
        "Controls the personality test, including the available partners and playable"
        " Pokémon. The actual personality test questions are stored in the MESSAGE"
        " folder."
    )
    loadaddress = 0x238AC80
    length = 0x2E80
    functions = EuOverlay13Functions
    data = EuOverlay13Data


class EuOverlay14Functions:
    SentrySetupState = Symbol(
        [0x0],
        [0x238AC80],
        None,
        (
            "Allocates and initializes the sentry duty struct.\n\nPossibly the"
            " entrypoint of this overlay?\n\nr0: controls initial game state? If 2, the"
            " minigame starts in state 4 rather than state 6.\nreturn: always 1"
        ),
    )

    SentryUpdateDisplay = Symbol(
        [0xCBC],
        [0x238B93C],
        None,
        (
            "Seems to update various parts of the display, such as the round"
            " number.\n\nNo params."
        ),
    )

    SentrySetExitingState = Symbol(
        [0x1598],
        [0x238C218],
        None,
        (
            "Sets the completion state to exiting, triggering the minigame to run its"
            " exit sequence.\n\nNo params."
        ),
    )

    SentryRunState = Symbol(
        [0x16BC],
        [0x238C33C],
        None,
        (
            "Run the minigame according to the current game state, or handle the"
            " transition to a new state if one has been set.\n\nThe game is implemented"
            " using the state machine programming pattern. This function appears to"
            " contain the top-level code for running a single 'turn' of the state"
            " machine, although presumably there's a higher level game engine that's"
            " calling this function in a loop somewhere.\n\nreturn: return code for the"
            " engine driving the minigame? Seems like 1 to keep going and 4 to stop"
        ),
    )

    SentrySetStateIntermediate = Symbol(
        [0x2088],
        [0x238CD08],
        None,
        (
            "Queues up a new intermediate game state to transition to, where the"
            " transition handler will be called immediately by SentryRunState after the"
            " current state handler has returned.\n\nr0: new state"
        ),
    )

    SentryState0 = Symbol([0x20A8], [0x238CD28], None, "No params.")

    SentryState1 = Symbol([0x20CC], [0x238CD4C], None, "No params.")

    SentryState2 = Symbol([0x2124], [0x238CDA4], None, "No params.")

    SentryState3 = Symbol([0x2148], [0x238CDC8], None, "No params.")

    SentryState4 = Symbol([0x2270], [0x238CEF0], None, "No params.")

    SentryStateExit = Symbol(
        None, None, None, "State 0x5: Exit (wraps SentrySetExitingState).\n\nNo params."
    )

    SentryState6 = Symbol([0x22A0], [0x238CF20], None, "No params.")

    SentryState7 = Symbol(
        [0x22C4],
        [0x238CF44],
        None,
        (
            "This state corresponds to when Loudred tells you the instructions for the"
            " minigame (STRING_ID_SENTRY_INSTRUCTIONS).\n\nNo params."
        ),
    )

    SentryState8 = Symbol([0x22DC], [0x238CF5C], None, "No params.")

    SentryState9 = Symbol([0x2300], [0x238CF80], None, "No params.")

    SentryStateA = Symbol(
        [0x2324],
        [0x238CFA4],
        None,
        (
            "This state corresponds to when Loudred alerts you that someone is coming"
            " (STRING_ID_SENTRY_HERE_COMES).\n\nNo params."
        ),
    )

    SentryStateB = Symbol([0x233C], [0x238CFBC], None, "No params.")

    SentryStateGenerateChoices = Symbol(
        [0x2354],
        [0x238CFD4],
        None,
        "State 0xC: Generate the four choices for a round.\n\nNo params.",
    )

    SentryStateGetUserChoice = Symbol(
        [0x2954],
        [0x238D5D4],
        None,
        "State 0xD: Wait for the player to select an answer.\n\nNo params.",
    )

    SentryStateFinalizeRound = Symbol(
        [0x2E84],
        [0x238DB04],
        None,
        (
            "State 0xE: Deal with the bookkeeping after the player has made a final"
            " choice for the round.\n\nThis includes things like incrementing the round"
            " counter. It also appears to check the final point count on the last round"
            " to determine the player's overall performance.\n\nNo params."
        ),
    )

    SentryStateF = Symbol([0x31C8], [0x238DE48], None, "No params.")

    SentryState10 = Symbol([0x31E0], [0x238DE60], None, "No params.")

    SentryState11 = Symbol(
        [0x3258],
        [0x238DED8],
        None,
        (
            "This state corresponds to when the partner tells you to try again after"
            " the player makes a wrong selection for the first time"
            " (STRING_ID_SENTRY_TRY_AGAIN).\n\nNo params."
        ),
    )

    SentryState12 = Symbol([0x3270], [0x238DEF0], None, "No params.")

    SentryState13 = Symbol(
        [0x32A8],
        [0x238DF28],
        None,
        (
            "This state corresponds to when Loudred tells you that you're out of time"
            " (STRING_ID_SENTRY_OUT_OF_TIME).\n\nNo params."
        ),
    )

    SentryState14 = Symbol(
        [0x32D0],
        [0x238DF50],
        None,
        (
            "This state corresponds to when the player is shouting their guess"
            " (STRING_ID_SENTRY_FOOTPRINT_IS_6EE), and when Loudred tells the visitor"
            " to come in (STRING_ID_SENTRY_COME_IN_6EF).\n\nNo params."
        ),
    )

    SentryState15 = Symbol([0x32E8], [0x238DF68], None, "No params.")

    SentryState16 = Symbol([0x3328], [0x238DFA8], None, "No params.")

    SentryState17 = Symbol(
        [0x3380],
        [0x238E000],
        None,
        (
            "This state corresponds to when Loudred tells the player that they chose"
            " the wrong answer (STRING_ID_SENTRY_WRONG,"
            " STRING_ID_SENTRY_BUCK_UP).\n\nNo params."
        ),
    )

    SentryState18 = Symbol([0x33F8], [0x238E078], None, "No params.")

    SentryState19 = Symbol(
        [0x3430],
        [0x238E0B0],
        None,
        (
            "This state seems to be similar to state 0x14, when the player is shouting"
            " their guess (STRING_ID_SENTRY_FOOTPRINT_IS_6EC), and when Loudred tells"
            " the visitor to come in (STRING_ID_SENTRY_COME_IN_6ED), but used in a"
            " different context (different state transitions to and from this"
            " state).\n\nNo params."
        ),
    )

    SentryState1A = Symbol([0x3448], [0x238E0C8], None, "No params.")

    SentryStateFinalizePoints = Symbol(
        [0x3488],
        [0x238E108],
        None,
        (
            "State 0x1B: Apply any modifiers to the player's point total, such as"
            " granting 2000 bonus points for 100% correctness.\n\nNo params."
        ),
    )

    SentryState1C = Symbol(
        [0x3518],
        [0x238E198],
        None,
        (
            "This state corresponds to when Loudred tells the player that they chose"
            " the correct answer ('Yep! Looks like you're right!').\n\nNo params."
        ),
    )

    SentryState1D = Symbol([0x355C], [0x238E1DC], None, "No params.")

    SentryState1E = Symbol(
        [0x35C0],
        [0x238E240],
        None,
        (
            "This state corresponds to one of the possible dialogue options when you've"
            " finished all the rounds (STRING_ID_SENTRY_KEEP_YOU_WAITING,"
            " STRING_ID_SENTRY_THATLL_DO_IT).\n\nNo params."
        ),
    )

    SentryState1F = Symbol([0x35D8], [0x238E258], None, "No params.")

    SentryState20 = Symbol(
        [0x3654],
        [0x238E2D4],
        None,
        (
            "This state corresponds to one of the possible dialogue options when you've"
            " finished all the rounds (STRING_ID_SENTRY_NO_MORE_VISITORS,"
            " STRING_ID_SENTRY_THATS_ALL).\n\nNo params."
        ),
    )

    SentryState21 = Symbol([0x366C], [0x238E2EC], None, "No params.")


class EuOverlay14Data:
    SENTRY_DUTY_STRUCT_SIZE = Symbol(
        None, None, None, "Number of bytes in the sentry duty struct (14548)."
    )

    SENTRY_LOUDRED_MONSTER_ID = Symbol(
        None, None, None, "Monster ID for Loudred, used as the speaker ID for dialog."
    )

    STRING_ID_SENTRY_TOP_SESSIONS = Symbol(
        None,
        None,
        None,
        "String ID 0x6D9:\n Here are the rankings for the\ntop sentry sessions.",
    )

    STRING_ID_SENTRY_INSTRUCTIONS = Symbol(
        None,
        None,
        None,
        (
            "String ID 0x6D8:\n Look at the footprint on the top\nscreen, OK? Then"
            " identify the Pokémon![C]\n You can get only [CS:V]two wrong[CR],"
            " OK?\n[partner] will keep an eye on things!"
        ),
    )

    STRING_ID_SENTRY_HERE_COMES = Symbol(
        None,
        None,
        None,
        (
            "String ID 0x6DA:\n Here comes a Pokémon! Check\nits footprint and tell me"
            " what it is!"
        ),
    )

    STRING_ID_SENTRY_WHOSE_FOOTPRINT = Symbol(
        None, None, None, "String ID 0x6DB:\n Whose footprint is this?[W:60]"
    )

    STRING_ID_SENTRY_TRY_AGAIN = Symbol(
        None, None, None, "String ID 0x6EB:\n Huh? I don't think so. Try again!"
    )

    STRING_ID_SENTRY_OUT_OF_TIME = Symbol(
        None,
        None,
        None,
        "String ID 0x6DC:\n [se_play:0][W:30]Out of time! Pick up the pace![W:75]",
    )

    STRING_ID_SENTRY_FOOTPRINT_IS_6EE = Symbol(
        None,
        None,
        None,
        (
            "String ID 0x6EE:\n The footprint is [kind:]'s!\nThe footprint is"
            " [kind:]'s![W:60]"
        ),
    )

    STRING_ID_SENTRY_COME_IN_6EF = Symbol(
        None, None, None, "String ID 0x6EF:\n Heard ya! Come in, visitor![W:30]"
    )

    STRING_ID_SENTRY_WRONG = Symbol(
        None,
        None,
        None,
        "String ID 0x6F1:\n ......[se_play:0][W:30]Huh?! Looks wrong to me![W:50]",
    )

    STRING_ID_SENTRY_BUCK_UP = Symbol(
        None,
        None,
        None,
        (
            "String ID 0x6F2 (and also used as Loudred's speaker ID after subtracting"
            " 0x5B0):\n The correct answer is\n[kind:]! Buck up! And snap to"
            " it![se_play:0][W:120]"
        ),
    )

    STRING_ID_SENTRY_FOOTPRINT_IS_6EC = Symbol(
        None,
        None,
        None,
        (
            "String ID 0x6EC:\n The footprint is [kind:]'s!\nThe footprint is"
            " [kind:]'s![W:60]"
        ),
    )

    STRING_ID_SENTRY_COME_IN_6ED = Symbol(
        None, None, None, "String ID 0x6ED:\n Heard ya! Come in, visitor![W:30]"
    )

    STRING_ID_SENTRY_KEEP_YOU_WAITING = Symbol(
        None, None, None, "String ID 0x6F3:\n [se_play:0]Sorry to keep you waiting."
    )

    STRING_ID_SENTRY_THATLL_DO_IT = Symbol(
        None,
        None,
        None,
        (
            "String ID 0x6F4:\n [partner] and [hero]![C]\n That'll do it! Now get back"
            " here!"
        ),
    )

    SENTRY_CHATOT_MONSTER_ID = Symbol(
        None, None, None, "Monster ID for Chatot, used as the speaker ID for dialog."
    )

    STRING_ID_SENTRY_NO_MORE_VISITORS = Symbol(
        None,
        None,
        None,
        "String ID 0x6F5:\n [se_play:0]No more visitors! No more\nvisitors! ♪",
    )

    STRING_ID_SENTRY_THATS_ALL = Symbol(
        None,
        None,
        None,
        (
            "String ID 0x6F6:\n OK, got that![C]\n Hey, [partner] and\n[hero]![C]\n"
            " That's all for today! Now get\nback here!"
        ),
    )

    SENTRY_GROVYLE_MONSTER_ID = Symbol(
        None,
        None,
        None,
        (
            "Monster ID for Grovyle, which appears to be explicitly excluded when"
            " generating species choices."
        ),
    )

    FOOTPRINT_DEBUG_MENU = Symbol([0x39C0], [0x238E640], 0x48, "")

    SENTRY_DUTY_PTR = Symbol(None, None, None, "Pointer to the SENTRY_DUTY_STRUCT.")

    SENTRY_DUTY_STATE_HANDLER_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Null-terminated table of handler functions for the different states in the"
            " state machine. See SentryRunState.\n\ntype: state_handler_fn_t[35]"
        ),
    )


class EuOverlay14Section:
    name = "overlay14"
    description = "Runs the sentry duty minigame."
    loadaddress = 0x238AC80
    length = 0x3B40
    functions = EuOverlay14Functions
    data = EuOverlay14Data


class EuOverlay15Functions:
    pass


class EuOverlay15Data:
    BANK_MAIN_MENU = Symbol([0xF40], [0x238BBC0], 0x28, "")

    BANK_D_BOX_LAYOUT_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    BANK_D_BOX_LAYOUT_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    BANK_D_BOX_LAYOUT_3 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    BANK_D_BOX_LAYOUT_4 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    BANK_D_BOX_LAYOUT_5 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY15_RESERVED_SPACE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY15_UNKNOWN_POINTER__NA_238B180 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )


class EuOverlay15Section:
    name = "overlay15"
    description = "Controls the Duskull Bank."
    loadaddress = 0x238AC80
    length = 0x1080
    functions = EuOverlay15Functions
    data = EuOverlay15Data


class EuOverlay16Functions:
    pass


class EuOverlay16Data:
    EVO_MENU_CONFIRM = Symbol([0x2BCC], [0x238D84C], 0x18, "Irdkwia's notes: 3*0x8")

    EVO_SUBMENU = Symbol([0x2BE4], [0x238D864], 0x20, "Irdkwia's notes: 4*0x8")

    EVO_MAIN_MENU = Symbol([0x2C04], [0x238D884], 0x20, "Irdkwia's notes: 4*0x8")

    EVO_MENU_STRING_IDS = Symbol(
        None, None, None, "26*0x2\n\nNote: unverified, ported from Irdkwia's notes"
    )

    EVO_D_BOX_LAYOUT_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    EVO_D_BOX_LAYOUT_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    EVO_D_BOX_LAYOUT_3 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    EVO_D_BOX_LAYOUT_4 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    EVO_D_BOX_LAYOUT_5 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    EVO_D_BOX_LAYOUT_6 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    EVO_D_BOX_LAYOUT_7 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY16_RESERVED_SPACE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY16_UNKNOWN_POINTER__NA_238CE40 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY16_UNKNOWN_POINTER__NA_238CE58 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )


class EuOverlay16Section:
    name = "overlay16"
    description = "Controls Luminous Spring."
    loadaddress = 0x238AC80
    length = 0x2D20
    functions = EuOverlay16Functions
    data = EuOverlay16Data


class EuOverlay17Functions:
    pass


class EuOverlay17Data:
    ASSEMBLY_D_BOX_LAYOUT_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    ASSEMBLY_D_BOX_LAYOUT_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    ASSEMBLY_D_BOX_LAYOUT_3 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    ASSEMBLY_D_BOX_LAYOUT_4 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    ASSEMBLY_D_BOX_LAYOUT_5 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    ASSEMBLY_MENU_CONFIRM = Symbol([0x1A44], [0x238C6C4], 0x18, "")

    ASSEMBLY_MAIN_MENU_1 = Symbol([0x1A5C], [0x238C6DC], 0x18, "")

    ASSEMBLY_MAIN_MENU_2 = Symbol([0x1A74], [0x238C6F4], 0x20, "")

    ASSEMBLY_SUBMENU_1 = Symbol([0x1A94], [0x238C714], 0x28, "")

    ASSEMBLY_SUBMENU_2 = Symbol([0x1ABC], [0x238C73C], 0x30, "")

    ASSEMBLY_SUBMENU_3 = Symbol([0x1AEC], [0x238C76C], 0x30, "")

    ASSEMBLY_SUBMENU_4 = Symbol([0x1B1C], [0x238C79C], 0x38, "")

    ASSEMBLY_SUBMENU_5 = Symbol([0x1B54], [0x238C7D4], 0x38, "")

    ASSEMBLY_SUBMENU_6 = Symbol([0x1B8C], [0x238C80C], 0x38, "")

    ASSEMBLY_SUBMENU_7 = Symbol([0x1BC4], [0x238C844], 0x40, "")

    OVERLAY17_FUNCTION_POINTER_TABLE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY17_RESERVED_SPACE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY17_UNKNOWN_POINTER__NA_238BE00 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY17_UNKNOWN_POINTER__NA_238BE04 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY17_UNKNOWN_POINTER__NA_238BE08 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )


class EuOverlay17Section:
    name = "overlay17"
    description = "Controls the Chimecho Assembly."
    loadaddress = 0x238AC80
    length = 0x1CE0
    functions = EuOverlay17Functions
    data = EuOverlay17Data


class EuOverlay18Functions:
    pass


class EuOverlay18Data:
    OVERLAY18_D_BOX_LAYOUT_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_3 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_4 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_5 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_6 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_7 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_8 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_9 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_10 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_11 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    MOVES_MENU_CONFIRM = Symbol([0x31E0], [0x238DE60], 0x18, "")

    MOVES_SUBMENU_1 = Symbol([0x31F8], [0x238DE78], 0x20, "")

    MOVES_SUBMENU_2 = Symbol([0x3218], [0x238DE98], 0x20, "")

    MOVES_MAIN_MENU = Symbol([0x3238], [0x238DEB8], 0x20, "")

    MOVES_SUBMENU_3 = Symbol([0x3258], [0x238DED8], 0x28, "")

    MOVES_SUBMENU_4 = Symbol([0x3280], [0x238DF00], 0x30, "")

    MOVES_SUBMENU_5 = Symbol([0x32B0], [0x238DF30], 0x48, "")

    MOVES_SUBMENU_6 = Symbol([0x32F8], [0x238DF78], 0x48, "")

    MOVES_SUBMENU_7 = Symbol([0x3340], [0x238DFC0], 0x48, "")

    OVERLAY18_FUNCTION_POINTER_TABLE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_RESERVED_SPACE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_UNKNOWN_POINTER__NA_238D620 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_UNKNOWN_POINTER__NA_238D624 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_UNKNOWN_POINTER__NA_238D628 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )


class EuOverlay18Section:
    name = "overlay18"
    description = "Controls the Electivire Link Shop."
    loadaddress = 0x238AC80
    length = 0x3500
    functions = EuOverlay18Functions
    data = EuOverlay18Data


class EuOverlay19Functions:
    GetBarItem = Symbol(
        [0x0],
        [0x238AC80],
        None,
        (
            "Gets the struct bar_item from BAR_AVAILABLE_ITEMS with the specified item"
            " ID.\n\nr0: item ID\nreturn: struct bar_item*"
        ),
    )

    GetRecruitableMonsterAll = Symbol(
        [0x84],
        [0x238AD04],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: int?",
    )

    GetRecruitableMonsterList = Symbol(
        [0x134],
        [0x238ADB4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: int?",
    )

    GetRecruitableMonsterListRestricted = Symbol(
        [0x1DC],
        [0x238AE5C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: int?",
    )


class EuOverlay19Data:
    OVERLAY19_UNKNOWN_TABLE__NA_238DAE0 = Symbol(
        None, None, None, "4*0x2\n\nNote: unverified, ported from Irdkwia's notes"
    )

    BAR_UNLOCKABLE_DUNGEONS_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " dungeon_id_16[6]"
        ),
    )

    BAR_RECRUITABLE_MONSTER_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " monster_id_16[108]"
        ),
    )

    BAR_AVAILABLE_ITEMS = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: struct bar_item[66]",
    )

    OVERLAY19_UNKNOWN_STRING_IDS__NA_238E178 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY19_UNKNOWN_STRUCT__NA_238E1A4 = Symbol(
        None, None, None, "5*0x8\n\nNote: unverified, ported from Irdkwia's notes"
    )

    OVERLAY19_UNKNOWN_STRING_IDS__NA_238E1CC = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    BAR_D_BOX_LAYOUT_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    BAR_D_BOX_LAYOUT_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    BAR_D_BOX_LAYOUT_3 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    BAR_MENU_CONFIRM_1 = Symbol([0x40BC], [0x238ED3C], 0x18, "")

    BAR_MENU_CONFIRM_2 = Symbol([0x40D4], [0x238ED54], 0x18, "")

    OVERLAY19_UNKNOWN_STRING_IDS__NA_238E238 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    BAR_MAIN_MENU = Symbol([0x4104], [0x238ED84], 0x20, "")

    BAR_SUBMENU_1 = Symbol([0x4124], [0x238EDA4], 0x20, "")

    BAR_SUBMENU_2 = Symbol([0x4144], [0x238EDC4], 0x30, "")

    OVERLAY19_RESERVED_SPACE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY19_UNKNOWN_POINTER__NA_238E360 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY19_UNKNOWN_POINTER__NA_238E364 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )


class EuOverlay19Section:
    name = "overlay19"
    description = "Controls Spinda's Juice Bar."
    loadaddress = 0x238AC80
    length = 0x4220
    functions = EuOverlay19Functions
    data = EuOverlay19Data


class EuOverlay2Functions:
    pass


class EuOverlay2Data:
    pass


class EuOverlay2Section:
    name = "overlay2"
    description = (
        "Controls the Nintendo WFC Settings interface, accessed from the top menu"
        " (Other > Nintendo WFC > Nintendo WFC Settings). Presumably contains code for"
        " Nintendo Wi-Fi setup."
    )
    loadaddress = 0x2329D40
    length = 0x2AFC0
    functions = EuOverlay2Functions
    data = EuOverlay2Data


class EuOverlay20Functions:
    pass


class EuOverlay20Data:
    OVERLAY20_UNKNOWN_POINTER__NA_238CF7C = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_MENU_CONFIRM_1 = Symbol([0x2E44], [0x238DAC4], 0x18, "")

    RECYCLE_MENU_CONFIRM_2 = Symbol([0x2E5C], [0x238DADC], 0x18, "")

    RECYCLE_SUBMENU_1 = Symbol([0x2E74], [0x238DAF4], 0x18, "")

    RECYCLE_SUBMENU_2 = Symbol([0x2E8C], [0x238DB0C], 0x20, "")

    RECYCLE_MAIN_MENU_1 = Symbol([0x2EAC], [0x238DB2C], 0x28, "")

    OVERLAY20_UNKNOWN_TABLE__NA_238D014 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT_3 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT_4 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT_5 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT_6 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_MAIN_MENU_2 = Symbol([0x2F48], [0x238DBC8], 0x20, "")

    RECYCLE_D_BOX_LAYOUT_7 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT_8 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT_9 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT1_0 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT1_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_MAIN_MENU_3 = Symbol([0x2FB8], [0x238DC38], 0x18, "")

    OVERLAY20_RESERVED_SPACE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY20_UNKNOWN_POINTER__NA_238D120 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY20_UNKNOWN_POINTER__NA_238D124 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY20_UNKNOWN_POINTER__NA_238D128 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY20_UNKNOWN_POINTER__NA_238D12C = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )


class EuOverlay20Section:
    name = "overlay20"
    description = "Controls the Recycle Shop."
    loadaddress = 0x238AC80
    length = 0x3000
    functions = EuOverlay20Functions
    data = EuOverlay20Data


class EuOverlay21Functions:
    pass


class EuOverlay21Data:
    SWAP_SHOP_D_BOX_LAYOUT_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SWAP_SHOP_MENU_CONFIRM = Symbol([0x28F8], [0x238D578], 0x18, "")

    SWAP_SHOP_SUBMENU_1 = Symbol([0x2910], [0x238D590], 0x18, "")

    SWAP_SHOP_SUBMENU_2 = Symbol([0x2928], [0x238D5A8], 0x20, "")

    SWAP_SHOP_MAIN_MENU_1 = Symbol([0x2948], [0x238D5C8], 0x20, "")

    SWAP_SHOP_MAIN_MENU_2 = Symbol([0x2968], [0x238D5E8], 0x28, "")

    SWAP_SHOP_SUBMENU_3 = Symbol([0x2990], [0x238D610], 0x30, "")

    OVERLAY21_UNKNOWN_STRING_IDS = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SWAP_SHOP_D_BOX_LAYOUT_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SWAP_SHOP_D_BOX_LAYOUT_3 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SWAP_SHOP_D_BOX_LAYOUT_4 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SWAP_SHOP_D_BOX_LAYOUT_5 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SWAP_SHOP_D_BOX_LAYOUT_6 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SWAP_SHOP_D_BOX_LAYOUT_7 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SWAP_SHOP_D_BOX_LAYOUT_8 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SWAP_SHOP_D_BOX_LAYOUT_9 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY21_JP_STRING = Symbol(None, None, None, "合成：")

    OVERLAY21_RESERVED_SPACE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY21_UNKNOWN_POINTER__NA_238CF40 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY21_UNKNOWN_POINTER__NA_238CF44 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )


class EuOverlay21Section:
    name = "overlay21"
    description = "Controls the Croagunk Swap Shop."
    loadaddress = 0x238AC80
    length = 0x2E20
    functions = EuOverlay21Functions
    data = EuOverlay21Data


class EuOverlay22Functions:
    pass


class EuOverlay22Data:
    SHOP_D_BOX_LAYOUT_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_D_BOX_LAYOUT_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY22_UNKNOWN_STRUCT__NA_238E85C = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_MENU_CONFIRM = Symbol([0x4728], [0x238F3A8], 0x18, "")

    SHOP_MAIN_MENU_1 = Symbol([0x4740], [0x238F3C0], 0x20, "")

    SHOP_MAIN_MENU_2 = Symbol([0x4760], [0x238F3E0], 0x20, "")

    SHOP_MAIN_MENU_3 = Symbol([0x4780], [0x238F400], 0x30, "")

    OVERLAY22_UNKNOWN_STRING_IDS = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_D_BOX_LAYOUT_3 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_D_BOX_LAYOUT_4 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_D_BOX_LAYOUT_5 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_D_BOX_LAYOUT_6 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_D_BOX_LAYOUT_7 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_D_BOX_LAYOUT_8 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_D_BOX_LAYOUT_9 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_D_BOX_LAYOUT_10 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY22_RESERVED_SPACE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY22_UNKNOWN_POINTER__NA_238EC60 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY22_UNKNOWN_POINTER__NA_238EC64 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY22_UNKNOWN_POINTER__NA_238EC68 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY22_UNKNOWN_POINTER__NA_238EC6C = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY22_UNKNOWN_POINTER__NA_238EC70 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )


class EuOverlay22Section:
    name = "overlay22"
    description = "Controls the Kecleon Shop in Treasure Town."
    loadaddress = 0x238AC80
    length = 0x4B40
    functions = EuOverlay22Functions
    data = EuOverlay22Data


class EuOverlay23Functions:
    pass


class EuOverlay23Data:
    OVERLAY23_UNKNOWN_VALUE__NA_238D2E8 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY23_UNKNOWN_VALUE__NA_238D2EC = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY23_UNKNOWN_STRUCT__NA_238D2F0 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    STORAGE_MENU_CONFIRM = Symbol([0x31BC], [0x238DE3C], 0x18, "")

    STORAGE_MAIN_MENU_1 = Symbol([0x31D4], [0x238DE54], 0x20, "")

    STORAGE_MAIN_MENU_2 = Symbol([0x31F4], [0x238DE74], 0x20, "")

    STORAGE_MAIN_MENU_3 = Symbol([0x3214], [0x238DE94], 0x20, "")

    STORAGE_MAIN_MENU_4 = Symbol([0x3234], [0x238DEB4], 0x28, "")

    OVERLAY23_UNKNOWN_STRING_IDS = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    STORAGE_D_BOX_LAYOUT_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    STORAGE_D_BOX_LAYOUT_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    STORAGE_D_BOX_LAYOUT_3 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    STORAGE_D_BOX_LAYOUT_4 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    STORAGE_D_BOX_LAYOUT_5 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    STORAGE_D_BOX_LAYOUT_6 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    STORAGE_D_BOX_LAYOUT_7 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    STORAGE_D_BOX_LAYOUT_8 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY23_RESERVED_SPACE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY23_UNKNOWN_POINTER__NA_238D8A0 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )


class EuOverlay23Section:
    name = "overlay23"
    description = (
        "Controls Kangaskhan Storage (both in Treasure Town and via Kangaskhan Rocks)."
    )
    loadaddress = 0x238AC80
    length = 0x3780
    functions = EuOverlay23Functions
    data = EuOverlay23Data


class EuOverlay24Functions:
    pass


class EuOverlay24Data:
    OVERLAY24_UNKNOWN_STRUCT__NA_238C508 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY24_UNKNOWN_STRUCT__NA_238C514 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DAYCARE_MENU_CONFIRM = Symbol([0x23E0], [0x238D060], 0x18, "")

    DAYCARE_MAIN_MENU = Symbol([0x23F8], [0x238D078], 0x20, "")

    OVERLAY24_UNKNOWN_STRING_IDS = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DAYCARE_D_BOX_LAYOUT_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DAYCARE_D_BOX_LAYOUT_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DAYCARE_D_BOX_LAYOUT_3 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DAYCARE_D_BOX_LAYOUT_4 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DAYCARE_D_BOX_LAYOUT_5 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY24_RESERVED_SPACE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY24_UNKNOWN_POINTER__NA_238C600 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )


class EuOverlay24Section:
    name = "overlay24"
    description = "Controls the Chansey Day Care."
    loadaddress = 0x238AC80
    length = 0x24E0
    functions = EuOverlay24Functions
    data = EuOverlay24Data


class EuOverlay25Functions:
    pass


class EuOverlay25Data:
    OVERLAY25_UNKNOWN_STRUCT__NA_238B498 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_D_BOX_LAYOUT_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_MENU_CONFIRM = Symbol([0x1374], [0x238BFF4], 0x18, "")

    APPRAISAL_MAIN_MENU = Symbol([0x138C], [0x238C00C], 0x20, "")

    APPRAISAL_SUBMENU = Symbol([0x13AC], [0x238C02C], 0x20, "")

    OVERLAY25_UNKNOWN_STRING_IDS = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_D_BOX_LAYOUT_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_D_BOX_LAYOUT_3 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_D_BOX_LAYOUT_4 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_D_BOX_LAYOUT_5 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_D_BOX_LAYOUT_6 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_D_BOX_LAYOUT_7 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_D_BOX_LAYOUT_8 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY25_RESERVED_SPACE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY25_UNKNOWN_POINTER__NA_238B5E0 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )


class EuOverlay25Section:
    name = "overlay25"
    description = "Controls Xatu Appraisal."
    loadaddress = 0x238AC80
    length = 0x14C0
    functions = EuOverlay25Functions
    data = EuOverlay25Data


class EuOverlay26Functions:
    pass


class EuOverlay26Data:
    OVERLAY26_UNKNOWN_TABLE__NA_238AE20 = Symbol(
        None,
        None,
        None,
        "0x6 + 11*0xC + 0x2\n\nNote: unverified, ported from Irdkwia's notes",
    )

    OVERLAY26_RESERVED_SPACE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY26_UNKNOWN_POINTER__NA_238AF60 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY26_UNKNOWN_POINTER__NA_238AF64 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY26_UNKNOWN_POINTER__NA_238AF68 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY26_UNKNOWN_POINTER__NA_238AF6C = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY26_UNKNOWN_POINTER5__NA_238AF70 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )


class EuOverlay26Section:
    name = "overlay26"
    description = (
        "Related to mission completion. It's loaded when the dungeon completion summary"
        " is shown upon exiting a dungeon, and during the cutscenes where you collect"
        " mission rewards from clients."
    )
    loadaddress = 0x238AC80
    length = 0xE40
    functions = EuOverlay26Functions
    data = EuOverlay26Data


class EuOverlay27Functions:
    pass


class EuOverlay27Data:
    OVERLAY27_UNKNOWN_VALUE__NA_238C948 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY27_UNKNOWN_VALUE__NA_238C94C = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY27_UNKNOWN_STRUCT__NA_238C950 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DISCARD_ITEMS_MENU_CONFIRM = Symbol([0x281C], [0x238D49C], 0x18, "")

    DISCARD_ITEMS_SUBMENU_1 = Symbol([0x2834], [0x238D4B4], 0x20, "")

    DISCARD_ITEMS_SUBMENU_2 = Symbol([0x2854], [0x238D4D4], 0x20, "")

    DISCARD_ITEMS_MAIN_MENU = Symbol([0x2874], [0x238D4F4], 0x28, "")

    OVERLAY27_UNKNOWN_STRING_IDS = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DISCARD_D_BOX_LAYOUT_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DISCARD_D_BOX_LAYOUT_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DISCARD_D_BOX_LAYOUT_3 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DISCARD_D_BOX_LAYOUT_4 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DISCARD_D_BOX_LAYOUT_5 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DISCARD_D_BOX_LAYOUT_6 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DISCARD_D_BOX_LAYOUT_7 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DISCARD_D_BOX_LAYOUT_8 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY27_RESERVED_SPACE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY27_UNKNOWN_POINTER__NA_238CE80 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY27_UNKNOWN_POINTER__NA_238CE84 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )


class EuOverlay27Section:
    name = "overlay27"
    description = "Controls the special episode item discard menu."
    loadaddress = 0x238AC80
    length = 0x2D60
    functions = EuOverlay27Functions
    data = EuOverlay27Data


class EuOverlay28Functions:
    pass


class EuOverlay28Data:
    pass


class EuOverlay28Section:
    name = "overlay28"
    description = "Controls the staff credits sequence."
    loadaddress = 0x238AC80
    length = 0xC60
    functions = EuOverlay28Functions
    data = EuOverlay28Data


class EuOverlay29Functions:
    DungeonAlloc = Symbol(
        [0x281C],
        [0x22DF39C],
        None,
        (
            "Allocates a new dungeon struct.\n\nThis updates the master dungeon pointer"
            " and returns a copy of that pointer.\n\nreturn: pointer to a newly"
            " allocated dungeon struct"
        ),
    )

    GetDungeonPtrMaster = Symbol(
        [0x2840],
        [0x22DF3C0],
        None,
        (
            "Returns the master dungeon pointer (a global, see"
            " DUNGEON_PTR_MASTER).\n\nreturn: pointer to a newly allocated dungeon"
            " struct"
        ),
    )

    DungeonZInit = Symbol(
        [0x2850],
        [0x22DF3D0],
        None,
        (
            "Zero-initializes the dungeon struct pointed to by the master dungeon"
            " pointer.\n\nNo params."
        ),
    )

    DungeonFree = Symbol(
        [0x2870],
        [0x22DF3F0],
        None,
        (
            "Frees the dungeons struct pointer to by the master dungeon pointer, and"
            " nullifies the pointer.\n\nNo params."
        ),
    )

    RunDungeon = Symbol(
        [0x2CF8],
        [0x22DF878],
        None,
        (
            "Called at the start of a dungeon. Initializes the dungeon struct from"
            " specified dungeon data. Includes a loop that does not break until the"
            " dungeon is cleared, and another one inside it that runs until the current"
            " floor ends.\n\nr0: Pointer to the struct containing info used to"
            " initialize the dungeon. See type dungeon_init for details.\nr1: Pointer"
            " to the dungeon data struct that will be used during the dungeon."
        ),
    )

    EntityIsValid = Symbol(
        [
            0x4114,
            0x57DC,
            0x5DC7,
            0x7118,
            0x75E8,
            0xD424,
            0x10438,
            0x10BF0,
            0x12178,
            0x135D4,
            0x143C4,
            0x190C8,
            0x1A0E0,
            0x1B19C,
            0x20818,
            0x22338,
            0x23F90,
            0x268E4,
            0x28664,
            0x29438,
            0x29AB0,
            0x2BDA4,
            0x2CE68,
            0x327E4,
            0x32EFC,
            0x34EF0,
            0x35794,
            0x38FF8,
            0x3CC14,
            0x3CD2C,
            0x3DE6C,
            0x3F074,
            0x40AB0,
            0x42CC0,
            0x43458,
            0x43AE4,
            0x44064,
            0x4464C,
            0x49508,
            0x52700,
            0x57E6C,
            0x58F98,
            0x5BCF8,
            0x68B5C,
            0x69704,
            0x6BC24,
            0x6D8FC,
            0x71E50,
            0x72CA0,
        ],
        [
            0x22E0C94,
            0x22E235C,
            0x22E2947,
            0x22E3C98,
            0x22E4168,
            0x22E9FA4,
            0x22ECFB8,
            0x22ED770,
            0x22EECF8,
            0x22F0154,
            0x22F0F44,
            0x22F5C48,
            0x22F6C60,
            0x22F7D1C,
            0x22FD398,
            0x22FEEB8,
            0x2300B10,
            0x2303464,
            0x23051E4,
            0x2305FB8,
            0x2306630,
            0x2308924,
            0x23099E8,
            0x230F364,
            0x230FA7C,
            0x2311A70,
            0x2312314,
            0x2315B78,
            0x2319794,
            0x23198AC,
            0x231A9EC,
            0x231BBF4,
            0x231D630,
            0x231F840,
            0x231FFD8,
            0x2320664,
            0x2320BE4,
            0x23211CC,
            0x2326088,
            0x232F280,
            0x23349EC,
            0x2335B18,
            0x2338878,
            0x23456DC,
            0x2346284,
            0x23487A4,
            0x234A47C,
            0x234E9D0,
            0x234F820,
        ],
        None,
        (
            "Checks if an entity pointer points to a valid entity (not entity type 0,"
            " which represents no entity).\n\nr0: entity pointer\nreturn: bool"
        ),
    )

    GetFloorType = Symbol(
        [0x4170],
        [0x22E0CF0],
        None,
        (
            "Get the current floor type.\n\nFloor types:\n  0 appears to mean the"
            " current floor is 'normal'\n  1 appears to mean the current floor is a"
            " fixed floor\n  2 means the current floor has a rescue point\n\nreturn:"
            " floor type"
        ),
    )

    TryForcedLoss = Symbol(
        [0x43E0],
        [0x22E0F60],
        None,
        (
            "Attempts to trigger a forced loss of the type specified in"
            " dungeon::forced_loss_reason.\n\nr0: if true, the function will not check"
            " for the end of the floor condition and will skip other (unknown) actions"
            " in case of forced loss.\nreturn: true if the forced loss happens, false"
            " otherwise"
        ),
    )

    IsBossFight = Symbol(
        [0x4624],
        [0x22E11A4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0:"
            " fixed_room_id\nreturn: bool"
        ),
    )

    IsCurrentFixedRoomBossFight = Symbol(
        [0x4640],
        [0x22E11C0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: bool",
    )

    IsMarowakTrainingMaze = Symbol(
        [0x4660],
        [0x22E11E0],
        None,
        (
            "Check if the current dungeon is one of the training mazes in Marowak Dojo"
            " (this excludes Final Maze).\n\nreturn: bool"
        ),
    )

    FixedRoomIsSubstituteRoom = Symbol(
        [0x468C],
        [0x22E120C],
        None,
        (
            "Checks if the current fixed room is the 'substitute room' (ID"
            " 0x6E).\n\nreturn: bool"
        ),
    )

    StoryRestrictionsEnabled = Symbol(
        [0x46E8],
        [0x22E1268],
        None,
        (
            "Returns true if certain special restrictions are enabled.\n\nIf true, you"
            " will get kicked out of the dungeon if a team member that passes the"
            " arm9::JoinedAtRangeCheck2 check faints.\n\nreturn:"
            " !dungeon::nonstory_flag || dungeon::hidden_land_flag"
        ),
    )

    GetScenarioBalanceVeneer = Symbol(
        [0x471C],
        [0x22E129C],
        None,
        (
            "Likely a linker-generated veneer for GetScenarioBalance.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-"
        ),
    )

    FadeToBlack = Symbol(
        [0x4728],
        [0x22E12A8],
        None,
        "Fades the screen to black across several frames.\n\nNo params.",
    )

    GetTileAtEntity = Symbol(
        [0x53E8],
        [0x22E1F68],
        None,
        (
            "Returns a pointer to the tile where an entity is located.\n\nr0: pointer"
            " to entity\nreturns: pointer to tile"
        ),
    )

    SpawnTrap = Symbol(
        [0x6020],
        [0x22E2BA0],
        None,
        (
            "Spawns a trap on the floor. Fails if there are more than 64 traps already"
            " on the floor.\n\nThis modifies the appropriate fields on the dungeon"
            " struct, initializing new entries in the entity table and the trap info"
            " list.\n\nr0: trap ID\nr1: position\nr2: team (see struct trap::team)\nr3:"
            " flags (see struct trap::team)\nreturn: entity pointer for the newly added"
            " trap, or null on failure"
        ),
    )

    SpawnItemEntity = Symbol(
        [0x60D4],
        [0x22E2C54],
        None,
        (
            "Spawns a blank item entity on the floor. Fails if there are more than 64"
            " items already on the floor.\n\nThis initializes a new entry in the entity"
            " table and points it to the corresponding slot in the item info"
            " list.\n\nr0: position\nreturn: entity pointer for the newly added item,"
            " or null on failure"
        ),
    )

    CanSeeTarget = Symbol(
        [0x650C],
        [0x22E308C],
        None,
        (
            "Checks if a given monster can see another monster.\n\nCalls"
            " IsPositionActuallyInSight. Also checks if the user is blinded, if the"
            " target is invisible, etc.\nThis function is almost the same as"
            " CanTargetEntity, the only difference is that the latter calls"
            " IsPositionInSight instead.\n\nr0: User entity pointer\nr1: Target entity"
            " pointer\nreturn: True if the user can see the target, false otherwise"
        ),
    )

    CanTargetEntity = Symbol(
        [0x65D0],
        [0x22E3150],
        None,
        (
            "Checks if a monster can target another entity when controlled by the"
            " AI.\nMore specifically, it checks if the target is invisible, if the user"
            " can see invisible monsters, if the user is blinded and if the target"
            " position is in sight from the position of the user (this last check is"
            " done by calling IsPositionInSight with the user's and the target's"
            " position).\nThis function is almost the same as CanSeeTarget, the only"
            " difference is that the latter calls IsPositionActuallyInSight"
            " instead.\n\nr0: User entity pointer\nr1: Target entity pointer\nreturn:"
            " True if the user can target the target, false otherwise"
        ),
    )

    CanTargetPosition = Symbol(
        [0x6714],
        [0x22E3294],
        None,
        (
            "Checks if a monster can target a position. This function just calls"
            " IsPositionInSight using the position of the user as the origin.\n\nr0:"
            " Entity pointer\nr1: Target position\nreturn: True if the specified"
            " monster can target the target position, false otherwise."
        ),
    )

    GetTeamMemberIndex = Symbol(
        [0x67F8],
        [0x22E3378],
        None,
        (
            "Given a pointer to an entity, returns its index on the entity list, or"
            " null if the entity can't be found on the first 4 slots of the"
            " list.\n\nr0: Pointer to the entity to find\nreturn: Index of the"
            " specified entity on the entity list, or null if it's not on the first 4"
            " slots."
        ),
    )

    SubstitutePlaceholderStringTags = Symbol(
        [0x6898],
        [0x22E3418],
        None,
        (
            "Replaces instances of a given placeholder tag by the string representation"
            " of the given entity.\n\nFrom the eos-move-effects docs (which are"
            " somewhat nebulous): 'Replaces the string at StringID [r0] by the string"
            " representation of the target [r1] (aka its name). Any message with the"
            " string manipulator '[string:StringID]' will use that string'.\n\nThe game"
            " uses various placeholder tags in its strings, which you can read about"
            " here: https://textbox.skytemple.org/.\n\nr0: string ID (unclear what this"
            " means)\nr1: entity pointer\nr2: ?"
        ),
    )

    UpdateMapSurveyorFlag = Symbol(
        [0x6BDC],
        [0x22E375C],
        None,
        (
            "Sets the Map Surveyor flag in the dungeon struct to true if a team member"
            " has Map Surveyor, sets it to false otherwise.\n\nThis function has two"
            " variants: in the EU ROM, it will return true if the flag was changed. The"
            " NA version will return the new value of the flag instead.\n\nreturn: bool"
        ),
    )

    PointCameraToMonster = Symbol(
        [0x6C84],
        [0x22E3804],
        None,
        "Points the camera to the specified monster.\n\nr0: Entity pointer\nr1: ?",
    )

    UpdateCamera = Symbol(
        [0x6CF4],
        [0x22E3874],
        None,
        (
            "Called every frame. Sets the camera to the right coordinates depending on"
            " the monster it points to.\n\nIt also takes care of updating the minimap,"
            " checking which elements should be shown on it, as well as whether the"
            " screen should be black due to the blinker status.\n\nr0: ?"
        ),
    )

    ItemIsActive = Symbol(
        [
            0x713C,
            0x12148,
            0x197D0,
            0x23744,
            0x26578,
            0x2BDC8,
            0x2E8D0,
            0x3246C,
            0x33704,
            0x34F14,
            0x35AD8,
            0x3901C,
            0x6BBD0,
        ],
        [
            0x22E3CBC,
            0x22EECC8,
            0x22F6350,
            0x23002C4,
            0x23030F8,
            0x2308948,
            0x230B450,
            0x230EFEC,
            0x2310284,
            0x2311A94,
            0x2312658,
            0x2315B9C,
            0x2348750,
        ],
        None,
        (
            "Checks if a monster is holding a certain item that isn't disabled by"
            " Klutz.\n\nr0: entity pointer\nr1: item ID\nreturn: bool"
        ),
    )

    GetVisibilityRange = Symbol(
        [0x716C],
        [0x22E3CEC],
        None,
        (
            "Returns dungeon::display_data::visibility_range. If the visibility range"
            " is 0, returns 2 instead.\n\nreturn: Visibility range of the current"
            " floor, or 2 if the visibility is 0."
        ),
    )

    UpdateStatusIconFlags = Symbol(
        [0x78E4],
        [0x22E4464],
        None,
        (
            "Sets a monster's status_icon_flags bitfield according to its current"
            " status effects. Does not affect a Sudowoodo in the 'permanent sleep'"
            " state (statuses::sleep == 0x7F).\n\nSome of the status effect in"
            " monster::statuses are used as an index to access an array, where every"
            " group of 8 bytes represents a bitmask. All masks are added in a bitwise"
            " OR and then stored in monster::status_icon.\n\nAlso sets icon flags for"
            " statuses::exposed, statuses::grudge, critical HP and lowered stats with"
            " explicit checks, and applies the effect of the Identifier Orb (see"
            " dungeon::identify_orb_flag).\n\nr0: entity pointer"
        ),
    )

    ShowPpRestoreEffect = Symbol(
        [0x8794],
        [0x22E5314],
        None,
        (
            "Displays the graphical effect on a monster that just recovered PP.\n\nr0:"
            " entity pointer"
        ),
    )

    LoadMappaFileAttributes = Symbol(
        [0xADEC],
        [0x22E796C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nThis function processes"
            " the spawn list of the current floor, checking which species can spawn,"
            " capping the amount of spawnable species on the floor to 14, randomly"
            " choosing which 14 species will spawn and ensuring that the sprite size of"
            " all the species combined does not exceed the maximum of 0x58000 bytes"
            " (352 KB). Kecleon and the Decoy are always included in the random"
            " selection.\n\nr0: quick_saved\nr1: ???\nr2: special_process"
        ),
    )

    IsOnMonsterSpawnList = Symbol(
        [0xBB7C],
        [0x22E86FC],
        None,
        (
            "Returns true if the specified monster is included in the floor's monster"
            " spawn list (the modified list after a maximum of 14 different species"
            " were chosen, not the raw list read from the mappa file).\n\nr0: Monster"
            " ID\nreturn: bool"
        ),
    )

    GetMonsterIdToSpawn = Symbol(
        [0xBBD0],
        [0x22E8750],
        None,
        (
            "Get the id of the monster to be randomly spawned.\n\nr0: the spawn weight"
            " to use (0 for normal, 1 for monster house)\nreturn: monster ID"
        ),
    )

    GetMonsterLevelToSpawn = Symbol(
        [0xBC88],
        [0x22E8808],
        None,
        (
            "Get the level of the monster to be spawned, given its id.\n\nr0: monster"
            " ID\nreturn: Level of the monster to be spawned, or 1 if the specified ID"
            " can't be found on the floor's spawn table."
        ),
    )

    GetDirectionTowardsPosition = Symbol(
        [0xCE50],
        [0x22E99D0],
        None,
        (
            "Gets the direction in which a monster should move to go from the origin"
            " position to the target position\n\nr0: Origin position\nr1: Target"
            " position\nreturn: Direction in which to move to reach the target position"
            " from the origin position"
        ),
    )

    GetChebyshevDistance = Symbol(
        [0xCEBC],
        [0x22E9A3C],
        None,
        (
            "Returns the Chebyshev distance between two positions. Calculated as"
            " max(abs(x0-x1), abs(y0-y1)).\n\nr0: Position A\nr1: Position B\nreturn:"
            " Chebyshev Distance between position A and position B"
        ),
    )

    IsPositionActuallyInSight = Symbol(
        [0xCEFC],
        [0x22E9A7C],
        None,
        (
            "Checks if a given target position is in sight from a given origin"
            " position.\nIf the origin position is on a hallway or r2 is true, checks"
            " if both positions are within <dungeon::display_data::visibility_range>"
            " tiles of each other.\nIf the origin position is on a room, checks that"
            " the target position is within the boundaries of said room.\n\nr0: Origin"
            " position\nr1: Target position\nr2: True to assume the entity standing on"
            " the origin position has the dropeye status\nreturn: True if the target"
            " position is in sight from the origin position"
        ),
    )

    IsPositionInSight = Symbol(
        [0xCFD4],
        [0x22E9B54],
        None,
        (
            "Checks if a given target position is in sight from a given origin"
            " position.\nThere's multiple factors that affect this check, but"
            " generally, it's true if both positions are in the same room (by checking"
            " if the target position is within the boundaries of the room where the"
            " origin position is) or within 2 tiles of each other.\n\nr0: Origin"
            " position\nr1: Target position\nr2: True to assume the entity standing on"
            " the origin position has the dropeye status\nreturn: True if the target"
            " position is in sight from the origin position"
        ),
    )

    GetLeader = Symbol(
        [0xD3B0],
        [0x22E9F30],
        None,
        (
            "Gets the pointer to the entity that is currently leading the team, or null"
            " if none of the first 4 entities is a valid monster with its"
            " is_team_leader flag set. It also sets LEADER_PTR to the result before"
            " returning it.\n\nreturn: Pointer to the current leader of the team or"
            " null if there's no valid leader."
        ),
    )

    GetLeaderMonster = Symbol(
        [0xD448],
        [0x22E9FC8],
        None,
        "Returns a pointer to the monster data of the current leader.\n\nNo params.",
    )

    TickStatusTurnCounter = Symbol(
        [0xD874],
        [0x22EA3F4],
        None,
        (
            "Ticks down a turn counter for a status condition. If the counter equals"
            " 0x7F, it will not be decreased.\n\nr0: pointer to the status turn"
            " counter\nreturn: new counter value"
        ),
    )

    AdvanceFrame = Symbol(
        [0xDE10],
        [0x22EA990],
        None,
        (
            "Advances one frame. Does not return until the next frame starts.\n\nr0: ?"
            " - Unused by the function"
        ),
    )

    GenerateDungeonRngSeed = Symbol(
        [0xE7B0],
        [0x22EB330],
        None,
        (
            "Generates a seed with which to initialize the dungeon PRNG.\n\nThe seed is"
            " calculated by starting with a different seed, the 'preseed' x0 (defaults"
            " to 1, but can be set by other functions). The preseed is iterated twice"
            " with the same recurrence relation used in the primary LCG to generate two"
            " pseudorandom 32-bit numbers x1 and x2. The output seed is then computed"
            " as\n  seed = (x1 & 0xFF0000) | (x2 >> 0x10) | 1\nThe value x1 is then"
            " saved as the new preseed.\n\nThis method of seeding the dungeon PRNG"
            " appears to be used only sometimes, depending on certain flags in the data"
            " for a given dungeon.\n\nreturn: RNG seed"
        ),
    )

    GetDungeonRngPreseed = Symbol(
        [0xE7FC],
        [0x22EB37C],
        None,
        (
            "Gets the current preseed stored in the global dungeon PRNG state. See"
            " GenerateDungeonRngSeed for more information.\n\nreturn: current dungeon"
            " RNG preseed"
        ),
    )

    SetDungeonRngPreseed = Symbol(
        [0xE80C],
        [0x22EB38C],
        None,
        (
            "Sets the preseed in the global dungeon PRNG state. See"
            " GenerateDungeonRngSeed for more information.\n\nr0: preseed"
        ),
    )

    InitDungeonRng = Symbol(
        [0xE81C],
        [0x22EB39C],
        None,
        (
            "Initialize (or reinitialize) the dungeon PRNG with a given seed. The"
            " primary LCG and the five secondary LCGs are initialized jointly, and with"
            " the same seed.\n\nr0: seed"
        ),
    )

    DungeonRand16Bit = Symbol(
        [0xE850],
        [0x22EB3D0],
        None,
        (
            "Computes a pseudorandom 16-bit integer using the dungeon PRNG.\n\nNote"
            " that the dungeon PRNG is only used in dungeon mode (as evidenced by these"
            " functions being in overlay 29). The game uses another lower-quality PRNG"
            " (see arm9.yml) for other needs.\n\nRandom numbers are generated with a"
            " linear congruential generator (LCG). The game actually maintains 6"
            " separate sequences that can be used for generation: a primary LCG and 5"
            " secondary LCGs. The generator used depends on parameters set on the"
            " global PRNG state.\n\nAll dungeon LCGs have a modulus of 2^32 and a"
            " multiplier of 1566083941 (see DUNGEON_PRNG_LCG_MULTIPLIER). The primary"
            " LCG uses an increment of 1, while the secondary LCGs use an increment of"
            " 2531011 (see DUNGEON_PRNG_LCG_INCREMENT_SECONDARY). So, for example, the"
            " primary LCG uses the recurrence relation:\n  x = (1566083941*x_prev + 1)"
            " % 2^32\n\nSince the dungeon LCGs generate 32-bit integers rather than"
            " 16-bit, the primary LCG yields 16-bit values by taking the upper 16 bits"
            " of the computed 32-bit value. The secondary LCGs yield 16-bit values by"
            " taking the lower 16 bits of the computed 32-bit value.\n\nAll of the"
            " dungeon LCGs have a hard-coded default seed of 1, but in practice the"
            " seed is set with a call to InitDungeonRng during dungeon"
            " initialization.\n\nreturn: pseudorandom int on the interval [0, 65535]"
        ),
    )

    DungeonRandInt = Symbol(
        [0xE8C8],
        [0x22EB448],
        None,
        (
            "Compute a pseudorandom integer under a given maximum value using the"
            " dungeon PRNG.\n\nr0: high\nreturn: pseudorandom integer on the interval"
            " [0, high - 1]"
        ),
    )

    DungeonRandRange = Symbol(
        [0xE8F0],
        [0x22EB470],
        None,
        (
            "Compute a pseudorandom value between two integers using the dungeon"
            " PRNG.\n\nr0: x\nr1: y\nreturn: pseudorandom integer on the interval"
            " [min(x, y), max(x, y) - 1]"
        ),
    )

    DungeonRandOutcome = Symbol(
        [0xE950, 0xE980],
        [0x22EB4D0, 0x22EB500],
        None,
        (
            "Returns the result of a possibly biased coin flip (a Bernoulli random"
            " variable) with some success probability p, using the dungeon PRNG.\n\nr0:"
            " success percentage (100*p)\nreturn: true with probability p, false with"
            " probability (1-p)"
        ),
    )

    CalcStatusDuration = Symbol(
        [0xE9B0],
        [0x22EB530],
        None,
        (
            "Seems to calculate the duration of a volatile status on a monster.\n\nr0:"
            " entity pointer\nr1: pointer to a turn range (an array of two shorts"
            " {lower, higher})\nr2: flag for whether or not to factor in the Self Curer"
            " IQ skill and the Natural Cure ability\nreturn: number of turns for the"
            " status condition"
        ),
    )

    DungeonRngUnsetSecondary = Symbol(
        [0xEA64],
        [0x22EB5E4],
        None,
        (
            "Sets the dungeon PRNG to use the primary LCG for subsequent random number"
            " generation, and also resets the secondary LCG index back to 0.\n\nSimilar"
            " to DungeonRngSetPrimary, but DungeonRngSetPrimary doesn't modify the"
            " secondary LCG index if it was already set to something other than"
            " 0.\n\nNo params."
        ),
    )

    DungeonRngSetSecondary = Symbol(
        [0xEA7C],
        [0x22EB5FC],
        None,
        (
            "Sets the dungeon PRNG to use one of the 5 secondary LCGs for subsequent"
            " random number generation.\n\nr0: secondary LCG index"
        ),
    )

    DungeonRngSetPrimary = Symbol(
        [0xEA94],
        [0x22EB614],
        None,
        (
            "Sets the dungeon PRNG to use the primary LCG for subsequent random number"
            " generation.\n\nNo params."
        ),
    )

    ChangeDungeonMusic = Symbol(
        [0xEC44],
        [0x22EB7C4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: music ID",
    )

    TrySwitchPlace = Symbol(
        [0xEFA8],
        [0x22EBB28],
        None,
        (
            "The user entity attempts to switch places with the target entity (i.e. by"
            " the effect of the Switcher Orb). \n\nThe function checks for the Suction"
            " Cups ability for both the user and the target, and for the Mold Breaker"
            " ability on the user.\n\nr0: pointer to user entity\nr1: pointer to target"
            " entity"
        ),
    )

    ClearMonsterActionFields = Symbol(
        [0xF224],
        [0x22EBDA4],
        None,
        (
            "Clears the fields related to AI in the monster's data struct, setting them"
            " all to 0.\nSpecifically, monster::action::action_id,"
            " monster::action::action_use_idx and monster::action::field_0xA are"
            " cleared.\n\nr0: Pointer to the monster's action field"
        ),
    )

    SetMonsterActionFields = Symbol(
        [0xF238],
        [0x22EBDB8],
        None,
        (
            "Sets some the fields related to AI in the monster's data"
            " struct.\nSpecifically, monster::action::action_id,"
            " monster::action::action_use_idx and monster::action::field_0xA. The last"
            " 2 are always set to 0.\n\nr0: Pointer to the monster's action field\nr1:"
            " Value to set monster::action::action_id to."
        ),
    )

    SetActionPassTurnOrWalk = Symbol(
        [0xF24C],
        [0x22EBDCC],
        None,
        (
            "Sets a monster's action to action::ACTION_PASS_TURN or"
            " action::ACTION_WALK, depending on the result of GetCanMoveFlag for the"
            " monster's ID.\n\nr0: Pointer to the monster's action field\nr1:"
            " Monster ID"
        ),
    )

    GetItemAction = Symbol(
        [0xF408],
        [0x22EBF88],
        None,
        (
            "Returns the action ID that corresponds to an item given its ID.\n\nThe"
            " action is based on the category of the item (see ITEM_CATEGORY_ACTIONS),"
            " unless the specified ID is 0x16B, in which case ACTION_UNK_35 is"
            " returned.\nSome items can have unexpected actions, such as thrown items,"
            " which have ACTION_NOTHING. This is done to prevent duplicate actions from"
            " being listed in the menu (since items always have a 'throw' option),"
            " since a return value of ACTION_NOTHING prevents the option from showing"
            " up in the menu.\n\nr0: Item ID\nreturn: Action ID associated with the"
            " specified item"
        ),
    )

    AddDungeonSubMenuOption = Symbol(
        [0xF64C],
        [0x22EC1CC],
        None,
        (
            "Adds an option to the list of actions that can be taken on a pokémon, item"
            " or move to the currently active sub-menu on dungeon mode (team, moves,"
            " items, etc.).\n\nr0: Action ID\nr1: True if the option should be enabled,"
            " false otherwise"
        ),
    )

    DisableDungeonSubMenuOption = Symbol(
        [0xF724],
        [0x22EC2A4],
        None,
        (
            "Disables an option that was addeed to a dungeon sub-menu.\n\nr0: Action ID"
            " of the option that should be disabled"
        ),
    )

    SetActionRegularAttack = Symbol(
        [0xFA80],
        [0x22EC600],
        None,
        (
            "Sets a monster's action to action::ACTION_REGULAR_ATTACK, with a specified"
            " direction.\n\nr0: Pointer to the monster's action field\nr1: Direction in"
            " which to use the move. Gets stored in monster::action::direction."
        ),
    )

    SetActionUseMoveAi = Symbol(
        [0xFAEC],
        [0x22EC66C],
        None,
        (
            "Sets a monster's action to action::ACTION_USE_MOVE_AI, with a specified"
            " direction and move index.\n\nr0: Pointer to the monster's action"
            " field\nr1: Index of the move to use (0-3). Gets stored in"
            " monster::action::action_use_idx.\nr2: Direction in which to use the move."
            " Gets stored in monster::action::direction."
        ),
    )

    RunFractionalTurn = Symbol(
        [0xFB38],
        [0x22EC6B8],
        None,
        (
            "The main function which executes the actions that take place in a"
            " fractional turn. Called in a loop by RunDungeon while IsFloorOver returns"
            " false.\n\nr0: first loop flag (true when the function is first called"
            " during a floor)"
        ),
    )

    RunLeaderTurn = Symbol(
        [0x10138],
        [0x22ECCB8],
        None,
        (
            "Handles the leader's turn. Includes a movement speed check that might"
            " cause it to return early if the leader isn't fast enough to act in this"
            " fractional turn. If that check (and some others) pass, the function does"
            " not return until the leader performs an action.\n\nr0: ?\nreturn: true if"
            " the leader has performed an action"
        ),
    )

    TrySpawnMonsterAndActivatePlusMinus = Symbol(
        [0x1050C],
        [0x22ED08C],
        None,
        (
            "Called at the beginning of RunFractionalTurn. Executed only if"
            " FRACTIONAL_TURN_SEQUENCE[fractional_turn * 2] is not 0.\n\nFirst it calls"
            " TrySpawnMonsterAndTickSpawnCounter, then tries to activate the Plus and"
            " Minus abilities for both allies and enemies, and finally calls"
            " TryForcedLoss.\n\nNo params."
        ),
    )

    IsFloorOver = Symbol(
        [0x10618],
        [0x22ED198],
        None,
        (
            "Checks if the current floor should end, and updates"
            " dungeon::floor_loop_status if required.\nIf the player has been defeated,"
            " sets dungeon::floor_loop_status to"
            " floor_loop_status::FLOOR_LOOP_LEADER_FAINTED.\nIf dungeon::end_floor_flag"
            " is 1 or 2, sets dungeon::floor_loop_status to"
            " floor_loop_status::FLOOR_LOOP_NEXT_FLOOR.\n\nreturn: true if the current"
            " floor should end"
        ),
    )

    DecrementWindCounter = Symbol(
        [0x10978],
        [0x22ED4F8],
        None,
        (
            "Decrements dungeon::wind_turns and displays a wind warning message if"
            " required.\n\nNo params."
        ),
    )

    SetForcedLossReason = Symbol(
        [0x10E38],
        [0x22ED9B8],
        None,
        (
            "Sets dungeon::forced_loss_reason to the specified value\n\nr0: Forced loss"
            " reason"
        ),
    )

    GetForcedLossReason = Symbol(
        [0x10E4C],
        [0x22ED9CC],
        None,
        "Returns dungeon::forced_loss_reason\n\nreturn: forced_loss_reason",
    )

    BindTrapToTile = Symbol(
        [0x11688],
        [0x22EE208],
        None,
        (
            "Sets the given tile's associated object to be the given trap, and sets the"
            " visibility of the trap.\n\nr0: tile pointer\nr1: entity pointer\nr2:"
            " visibility flag"
        ),
    )

    SpawnEnemyTrapAtPos = Symbol(
        [0x117A0],
        [0x22EE320],
        None,
        (
            "A convenience wrapper around SpawnTrap and BindTrapToTile. Always passes 0"
            " for the team parameter (making it an enemy trap).\n\nr0: trap ID\nr1: x"
            " position\nr2: y position\nr3: flags\nstack[0]: visibility flag"
        ),
    )

    DebugRecruitingEnabled = Symbol(
        [0x138A0],
        [0x22F0420],
        None,
        (
            "Always returns true. Called by SpecificRecruitCheck.\n\nSeems to be a"
            " function used during development to disable recruiting. If it returns"
            " false, SpecificRecruitCheck will also return false.\n\nreturn: true"
        ),
    )

    GetLeaderAction = Symbol(
        [0x149C0],
        [0x22F1540],
        None,
        (
            "Returns a pointer to the action data of the current leader (field 0x4A on"
            " its monster struct).\n\nNo params."
        ),
    )

    SetLeaderAction = Symbol(
        [0x14D10],
        [0x22F1890],
        None,
        (
            "Sets the leader's action field depending on the inputs given by the"
            " player.\n\nThis function also accounts for other special situations that"
            " can force a certain action, such as when the leader is running. The"
            " function also takes care of opening the main menu when X is pressed.\nThe"
            " function generally doesn't return until the player has an action"
            " set.\n\nNo params."
        ),
    )

    ChangeLeader = Symbol(
        [0x17770],
        [0x22F42F0],
        None,
        (
            "Tries to change the current leader to the monster specified by"
            " dungeon::new_leader.\n\nAccounts for situations that can prevent changing"
            " leaders, such as having stolen from a Kecleon shop. If one of those"
            " situations prevents changing leaders, prints the corresponding message to"
            " the message log.\n\nNo params."
        ),
    )

    ResetDamageData = Symbol(
        [0x1AC50],
        [0x22F77D0],
        None,
        (
            "Zeroes the damage data struct, which is output by the damage calculation"
            " function.\n\nr0: damage data pointer"
        ),
    )

    DungeonGetTotalSpriteFileSize = Symbol(
        [0x1AEA0],
        [0x22F7A20],
        None,
        (
            "Checks Castform and Cherrim\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: monster ID\nreturn: sprite file size"
        ),
    )

    DungeonGetSpriteIndex = Symbol(
        [0x1B1C0],
        [0x22F7D40],
        None,
        (
            "Gets the sprite index of the specified monster on this floor\n\nr0:"
            " Monster ID\nreturn: Sprite index of the specified monster ID"
        ),
    )

    JoinedAtRangeCheck2Veneer = Symbol(
        [0x1B1E0],
        [0x22F7D60],
        None,
        (
            "Likely a linker-generated veneer for arm9::JoinedAtRangeCheck2.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nNo"
            " params."
        ),
    )

    FloorNumberIsEven = Symbol(
        [0x1B1EC],
        [0x22F7D6C],
        None,
        (
            "Checks if the current dungeon floor number is even (probably to determine"
            " whether an enemy spawn should be female).\n\nHas a special check to"
            " return false for Labyrinth Cave B10F (the Gabite boss fight).\n\nreturn:"
            " bool"
        ),
    )

    GetKecleonIdToSpawnByFloor = Symbol(
        [0x1B224],
        [0x22F7DA4],
        None,
        (
            "If the current floor number is even, returns female Kecleon's id (0x3D7),"
            " otherwise returns male Kecleon's id (0x17F).\n\nreturn: monster ID"
        ),
    )

    StoreSpriteFileIndexBothGenders = Symbol(
        [0x1B244],
        [0x22F7DC4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nr1: file ID",
    )

    LoadMonsterSpriteInner = Symbol(
        [0x1B30C],
        [0x22F7E8C],
        None,
        "This is called by LoadMonsterSprite a bunch of times.\n\nr0: monster ID",
    )

    SwapMonsterWanFileIndex = Symbol(
        [0x1B40C],
        [0x22F7F8C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: src_id\nr1: dst_id",
    )

    LoadMonsterSprite = Symbol(
        [0x1B48C],
        [0x22F800C],
        None,
        (
            "Loads the sprite of the specified monster to use it in a"
            " dungeon.\n\nIrdkwia's notes: Handles Castform/Cherrim/Deoxys\n\nr0:"
            " monster ID\nr1: ?"
        ),
    )

    DeleteMonsterSpriteFile = Symbol(
        [0x1B5A0],
        [0x22F8120],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID",
    )

    DeleteAllMonsterSpriteFiles = Symbol(
        [0x1B63C],
        [0x22F81BC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    EuFaintCheck = Symbol(
        [0x1BD68],
        [0x22F88E8],
        None,
        (
            "This function is exclusive to the EU ROM. Seems to perform a check to see"
            " if the monster who just fainted was a team member who should cause the"
            " minimap to be updated (or something like that, maybe related to the Map"
            " Surveyor IQ skill) and if it passes, updates the minimap.\nThe function"
            " ends by calling another 2 functions. In US ROMs, calls to EUFaintCheck"
            " are replaced by calls to those two functions. This seems to indicate that"
            " this function fixes some edge case glitch that can happen when a team"
            " member faints.\n\nr0: False if the fainted entity was a team member\nr1:"
            " True to set an unknown byte in the RAM to 1"
        ),
    )

    HandleFaint = Symbol(
        [0x1BDB8],
        [0x22F8938],
        None,
        (
            "Handles a fainted pokémon (reviving does not count as fainting).\n\nr0:"
            " Fainted entity\nr1: Damage source (move ID or greater than the max move"
            " id for other causes)\nr2: Entity responsible of the fainting"
        ),
    )

    UpdateAiTargetPos = Symbol(
        [0x1CFD0],
        [0x22F9B50],
        None,
        (
            "Given a monster, updates its target_pos field based on its current"
            " position and the direction in which it plans to attack.\n\nr0: Entity"
            " pointer"
        ),
    )

    SetMonsterTypeAndAbility = Symbol(
        [0x1D020],
        [0x22F9BA0],
        None,
        (
            "Checks Forecast ability\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: target entity pointer"
        ),
    )

    TryActivateSlowStart = Symbol(
        [0x1D0C8],
        [0x22F9C48],
        None,
        (
            "Runs a check over all monsters on the field for the ability Slow Start,"
            " and lowers the speed of those who have it.\n\nNo params"
        ),
    )

    TryActivateArtificialWeatherAbilities = Symbol(
        [0x1D164],
        [0x22F9CE4],
        None,
        (
            "Runs a check over all monsters on the field for abilities that affect the"
            " weather and changes the floor's weather accordingly.\n\nNo params"
        ),
    )

    GetMonsterApparentId = Symbol(
        [0x1D294],
        [0x22F9E14],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: target entity"
            " pointer\nr1: current_id\nreturn: ?"
        ),
    )

    DefenderAbilityIsActive = Symbol(
        [0x1D558, 0x258B8, 0x2E834, 0x35A74, 0x46C4C, 0x568CC],
        [0x22FA0D8, 0x2302438, 0x230B3B4, 0x23125F4, 0x23237CC, 0x233344C],
        None,
        (
            "Checks if a defender has an active ability that isn't disabled by an"
            " attacker's Mold Breaker.\n\nThere are two versions of this function,"
            " which share the same logic but have slightly different assembly. This is"
            " probably due to differences in compiler optimizations at different"
            " addresses.\n\nr0: attacker pointer\nr1: defender pointer\nr2: ability ID"
            " to check on the defender\nr3: flag for whether the attacker's ability is"
            " enabled\nreturn: bool"
        ),
    )

    IsMonster = Symbol(
        [
            0x1D5AC,
            0x2590C,
            0x2E888,
            0x33874,
            0x3C990,
            0x3E8B4,
            0x3F1F8,
            0x46CA0,
            0x714E0,
        ],
        [
            0x22FA12C,
            0x230248C,
            0x230B408,
            0x23103F4,
            0x2319510,
            0x231B434,
            0x231BD78,
            0x2323820,
            0x234E060,
        ],
        None,
        (
            "Checks if an entity is a monster (entity type 1).\n\nr0: entity"
            " pointer\nreturn: bool"
        ),
    )

    TryActivateTruant = Symbol(
        [0x1D67C],
        [0x22FA1FC],
        None,
        (
            "Checks if an entity has the ability Truant, and if so tries to apply the"
            " pause status to it.\n\nr0: pointer to entity"
        ),
    )

    TryPointCameraToMonster = Symbol(
        [0x1D740],
        [0x22FA2C0],
        None,
        (
            "Attempts to place the camera on top of the specified monster.\n\nIf the"
            " camera is already on top of the specified entity, the function does"
            " nothing.\n\nr0: Entity pointer. Must be a monster, otherwise the function"
            " does nothing.\nr1: ?\nr2: ?"
        ),
    )

    RestorePpAllMovesSetFlags = Symbol(
        [0x1D900],
        [0x22FA480],
        None,
        (
            "Restores PP for all moves, clears flags move::f_consume_2_pp,"
            " move::flags2_unk5 and move::flags2_unk7, and sets flag"
            " move::f_consume_pp.\nCalled when a monster is revived.\n\nr0: pointer to"
            " entity whose moves will be restored"
        ),
    )

    ShouldMonsterHeadToStairs = Symbol(
        [0x1E2BC],
        [0x22FAE3C],
        None,
        (
            "Checks if a given monster should try to reach the stairs when controlled"
            " by the AI\n\nr0: Entity pointer\nreturn: True if the monster should try"
            " to reach the stairs, false otherwise"
        ),
    )

    MewSpawnCheck = Symbol(
        [0x1E47C],
        [0x22FAFFC],
        None,
        (
            "If the monster id parameter is 0x97 (Mew), returns false if either"
            " dungeon::mew_cannot_spawn or the second parameter are true.\n\nCalled"
            " before spawning an enemy, appears to be checking if Mew can spawn on the"
            " current floor.\n\nr0: monster id\nr1: return false if the monster id is"
            " Mew\nreturn: bool"
        ),
    )

    ExclusiveItemEffectIsActive = Symbol(
        [
            0x1EB24,
            0x23DD4,
            0x2E8AC,
            0x337A0,
            0x34F44,
            0x386CC,
            0x3D688,
            0x3E75C,
            0x47800,
            0x568A8,
            0x6BC00,
            0x6C330,
        ],
        [
            0x22FB6A4,
            0x2300954,
            0x230B42C,
            0x2310320,
            0x2311AC4,
            0x231524C,
            0x231A208,
            0x231B2DC,
            0x2324380,
            0x2333428,
            0x2348780,
            0x2348EB0,
        ],
        None,
        (
            "Checks if a monster is a team member under the effects of a certain"
            " exclusive item effect.\n\nr0: entity pointer\nr1: exclusive item effect"
            " ID\nreturn: bool"
        ),
    )

    GetTeamMemberWithIqSkill = Symbol(
        [0x1EE84],
        [0x22FBA04],
        None,
        (
            "Returns an entity pointer to the first team member which has the specified"
            " iq skill.\n\nr0: iq skill id\nreturn: pointer to entity"
        ),
    )

    TeamMemberHasEnabledIqSkill = Symbol(
        [0x1EEF0],
        [0x22FBA70],
        None,
        (
            "Returns true if any team member has the specified iq skill.\n\nr0: iq"
            " skill id\nreturn: bool"
        ),
    )

    TeamLeaderIqSkillIsEnabled = Symbol(
        [0x1EF0C],
        [0x22FBA8C],
        None,
        (
            "Returns true the leader has the specified iq skill.\n\nr0: iq skill"
            " id\nreturn: bool"
        ),
    )

    HasSuperEffectiveMoveAgainstUser = Symbol(
        [0x1EF98],
        [0x22FBB18],
        None,
        (
            "Checks if the target has at least one super effective move against the"
            " user.\n\nr0: User\nr1: Target\nr2: If true, moves with a max Ginseng"
            " boost != 99 will be ignored\nreturn: True if the target has at least one"
            " super effective move against the user, false otherwise."
        ),
    )

    CheckSpawnThreshold = Symbol(
        [0x1F478],
        [0x22FBFF8],
        None,
        (
            "Checks if a given monster ID can spawn in dungeons.\n\nThe function"
            " returns true if the monster's spawn threshold value is <="
            " SCENARIO_BALANCE_FLAG\n\nr0: monster ID\nreturn: True if the monster can"
            " spawn, false otherwise"
        ),
    )

    HasLowHealth = Symbol(
        [0x1F49C],
        [0x22FC01C],
        None,
        (
            "Checks if the entity passed is a valid monster, and if it's at low health"
            " (below 25% rounded down)\n\nr0: entity pointer\nreturn: bool"
        ),
    )

    AreEntitiesAdjacent = Symbol(
        [0x1F504],
        [0x22FC084],
        None,
        (
            "Checks whether two entities are adjacent or not.\n\nThe function checks"
            " all 8 possible directions.\n\nr0: First entity\nr1: Second"
            " entity\nreturn: True if both entities are adjacent, false otherwise."
        ),
    )

    IsSpecialStoryAlly = Symbol(
        [0x1F94C],
        [0x22FC4CC],
        None,
        (
            "Checks if a monster is a special story ally.\n\nThis is a hard-coded check"
            " that looks at the monster's 'Joined At' field. If the value is in the"
            " range [DUNGEON_JOINED_AT_BIDOOF, DUNGEON_DUMMY_0xE3], this check will"
            " return true.\n\nr0: monster pointer\nreturn: bool"
        ),
    )

    IsExperienceLocked = Symbol(
        [0x1F96C],
        [0x22FC4EC],
        None,
        (
            "Checks if a monster does not gain experience.\n\nThis basically just"
            " inverts IsSpecialStoryAlly, with the exception of also checking for the"
            " 'Joined At' field being DUNGEON_CLIENT (is this set for mission"
            " clients?).\n\nr0: monster pointer\nreturn: bool"
        ),
    )

    InitTeam = Symbol(
        [0x20388],
        [0x22FCF08],
        None,
        "Seems to initialize the team when entering a dungeon.\n\nr0: ?",
    )

    SpawnMonster = Symbol(
        [0x20F00],
        [0x22FDA80],
        None,
        (
            "Spawns the given monster on a tile.\n\nr0: pointer to struct"
            " spawned_monster_data\nr1: if true, the monster cannot spawn asleep,"
            " otherwise it will randomly be asleep\nreturn: pointer to entity"
        ),
    )

    InitTeamMember = Symbol(
        [0x21230],
        [0x22FDDB0],
        None,
        (
            "Initializes a team member. Run at the start of each floor in a"
            " dungeon.\n\nr0: Monster ID\nr1: X position\nr2: Y position\nr3: Pointer"
            " to the struct containing the data of the team member to"
            " initialize\nstack[0]: ?\nstack[1]: ?\nstack[2]: ?\nstack[3]:"
            " ?\nstack[4]: ?"
        ),
    )

    InitMonster = Symbol(
        [0x21C3C],
        [0x22FE7BC],
        None,
        (
            "Initializes a monster struct.\n\nr0: pointer to monster to initialize\nr1:"
            " some flag"
        ),
    )

    ExecuteMonsterAction = Symbol(
        [0x2235C],
        [0x22FEEDC],
        None,
        (
            "Executes the set action for the specified monster. Used for both AI"
            " actions and player-inputted actions. If the action is not ACTION_NOTHING,"
            " ACTION_PASS_TURN, ACTION_WALK or ACTION_UNK_4, the monster's"
            " already_acted field is set to true. Includes a switch based on the action"
            " ID that performs the action, although some of them aren't handled by said"
            " swtich.\n\nr0: Pointer to monster entity"
        ),
    )

    HasStatusThatPreventsActing = Symbol(
        [0x23074],
        [0x22FFBF4],
        None,
        (
            "Returns true if the monster has any status problem that prevents it from"
            " acting\n\nr0: Entity pointer\nreturn: True if the specified monster can't"
            " act because of a status problem, false otherwise."
        ),
    )

    CalcSpeedStage = Symbol(
        [0x23CA0],
        [0x2300820],
        None,
        (
            "Calculates the speed stage of a monster from its speed up/down counters."
            " The second parameter is the weight of each counter (how many stages it"
            " will add/remove), but appears to be always 1. \nTakes modifiers into"
            " account (paralysis, snowy weather, Time Tripper). Deoxys-speed,"
            " Shaymin-sky and enemy Kecleon during a thief alert get a flat +1"
            " always.\n\nThe calculated speed stage is both returned and saved in the"
            " monster's statuses struct.\n\nr0: pointer to entity\nr1: speed counter"
            " weight\nreturn: speed stage"
        ),
    )

    CalcSpeedStageWrapper = Symbol(
        [0x23DF8],
        [0x2300978],
        None,
        (
            "Calls CalcSpeedStage with a speed counter weight of 1.\n\nr0: pointer to"
            " entity\nreturn: speed stage"
        ),
    )

    GetNumberOfAttacks = Symbol(
        [0x23E08],
        [0x2300988],
        None,
        (
            "Returns the number of attacks that a monster can do in one turn (1 or"
            " 2).\n\nChecks for the abilities Swift Swim, Chlorophyll, Unburden, and"
            " for exclusive items.\n\nr0: pointer to entity\nreturns: int"
        ),
    )

    GetMonsterName = Symbol(
        [0x24010],
        [0x2300B90],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nr1: TargetInfo",
    )

    SprintfStatic = Symbol(
        [0x24174],
        [0x2300CF4],
        None,
        (
            "Statically defined copy of sprintf(3) in overlay 29. See arm9.yml for more"
            " information.\n\nr0: str\nr1: format\n...: variadic\nreturn: number of"
            " characters printed, excluding the null-terminator"
        ),
    )

    IsMonsterCornered = Symbol(
        [0x24FC4],
        [0x2301B44],
        None,
        (
            "True if the given monster is cornered (it can't move in any"
            " direction)\n\nr0: Entity pointer\nreturn: True if the monster can't move"
            " in any direction, false otherwise."
        ),
    )

    CanAttackInDirection = Symbol(
        [0x250E0],
        [0x2301C60],
        None,
        (
            "Returns whether a monster can attack in a given direction.\nThe check"
            " fails if the destination tile is impassable, contains a monster that"
            " isn't of type entity_type::ENTITY_MONSTER or if the monster can't"
            " directly move from the current tile into the destination tile.\n\nr0:"
            " Entity pointer\nr1: Direction\nreturn: True if the monster can attack"
            " into the tile adjacent to them in the specified direction, false"
            " otherwise."
        ),
    )

    CanAiMonsterMoveInDirection = Symbol(
        [0x251A4],
        [0x2301D24],
        None,
        (
            "Checks whether an AI-controlled monster can move in the specified"
            " direction.\nAccounts for walls, other monsters on the target position and"
            " IQ skills that might prevent a monster from moving into a specific"
            " location, such as House Avoider, Trap Avoider or Lava Evader.\n\nr0:"
            " Entity pointer\nr1: Direction\nr2: (output) True if movement was not"
            " possible because there was another monster on the target tile, false"
            " otherwise.\nreturn: True if the monster can move in the specified"
            " direction, false otherwise."
        ),
    )

    ShouldMonsterRunAway = Symbol(
        [0x25464],
        [0x2301FE4],
        None,
        (
            "Checks if a monster should run away from other monsters\n\nr0: Entity"
            " pointer\nreturn: True if the monster should run away, false otherwise"
        ),
    )

    ShouldMonsterRunAwayVariation = Symbol(
        [0x25554],
        [0x23020D4],
        None,
        (
            "Calls ShouldMonsterRunAway and returns its result. It also calls another"
            " function if the result was true.\n\nr0: Entity pointer\nr1: ?\nreturn:"
            " Result of the call to ShouldMonsterRunAway"
        ),
    )

    NoGastroAcidStatus = Symbol(
        [0x25B88],
        [0x2302708],
        None,
        (
            "Checks if a monster does not have the Gastro Acid status.\n\nr0: entity"
            " pointer\nreturn: bool"
        ),
    )

    AbilityIsActive = Symbol(
        [0x25BBC],
        [0x230273C],
        None,
        (
            "Checks if a monster has a certain ability that isn't disabled by Gastro"
            " Acid.\n\nr0: entity pointer\nr1: ability ID\nreturn: bool"
        ),
    )

    AbilityIsActiveVeneer = Symbol(
        [0x25C24],
        [0x23027A4],
        None,
        (
            "Likely a linker-generated veneer for AbilityIsActive.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " entity pointer\nr1: ability ID\nreturn: bool"
        ),
    )

    AbilityIsActiveAnyEntity = Symbol(
        [0x25C30],
        [0x23027B0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: user entity"
            " pointer\nr1: ability ID\nreturn: bool"
        ),
    )

    LevitateIsActive = Symbol(
        [0x25CC4],
        [0x2302844],
        None,
        (
            "Checks if a monster is levitating (has the effect of Levitate and Gravity"
            " is not active).\n\nr0: pointer to entity\nreturn: bool"
        ),
    )

    MonsterIsType = Symbol(
        [0x25CFC],
        [0x230287C],
        None,
        (
            "Checks if a monster is a given type.\n\nr0: entity pointer\nr1: type"
            " ID\nreturn: bool"
        ),
    )

    IsTypeAffectedByGravity = Symbol(
        [0x25D34],
        [0x23028B4],
        None,
        (
            "Checks if Gravity is active and that the given type is affected (i.e.,"
            " Flying type).\n\nr0: target entity pointer (unused)\nr1: type ID\nreturn:"
            " bool"
        ),
    )

    HasTypeAffectedByGravity = Symbol(
        [0x25D58],
        [0x23028D8],
        None,
        (
            "Checks if Gravity is active and that the given monster is of an affected"
            " type (i.e., Flying type).\n\nr0: target entity pointer\nr1: type"
            " ID\nreturn: bool"
        ),
    )

    CanSeeInvisibleMonsters = Symbol(
        [0x25D98],
        [0x2302918],
        None,
        (
            "Returns whether a certain monster can see other invisible monsters.\nTo be"
            " precise, this function returns true if the monster is holding Goggle"
            " Specs or if it has the status status::STATUS_EYEDROPS.\n\nr0: Entity"
            " pointer\nreturn: True if the monster can see invisible monsters."
        ),
    )

    HasDropeyeStatus = Symbol(
        [0x25DFC],
        [0x230297C],
        None,
        (
            "Returns whether a certain monster is under the effect of"
            " status::STATUS_DROPEYE.\n\nr0: Entity pointer\nreturn: True if the"
            " monster has dropeye status."
        ),
    )

    IqSkillIsEnabled = Symbol(
        [0x25E2C],
        [0x23029AC],
        None,
        (
            "Checks if a monster has a certain IQ skill enabled.\n\nr0: entity"
            " pointer\nr1: IQ skill ID\nreturn: bool"
        ),
    )

    UpdateIqSkills = Symbol(
        [0x25E68],
        [0x23029E8],
        None,
        (
            "Updates the IQ skill flags of a monster.\n\nIf the monster is a team"
            " member, copies monster::iq_skill_menu_flags to monster::iq_skill_flags."
            " If the monster is an enemy, enables all the IQ skills it can learn"
            " (except a few that are only enabled in enemies that have a certain amount"
            " of IQ).\nIf the monster is an enemy, it also sets its tactic to"
            " TACTIC_GO_AFTER_FOES.\nCalled after exiting the IQ skills menu or after"
            " an enemy spawns.\n\nr0: monster pointer"
        ),
    )

    GetMoveTypeForMonster = Symbol(
        [0x26128],
        [0x2302CA8],
        None,
        (
            "Check the type of a move when used by a certain monster. Accounts for"
            " special cases such as Hidden Power, Weather Ball, the regular"
            " attack...\n\nr0: Entity pointer\nr1: Pointer to move data\nreturn: Type"
            " of the move"
        ),
    )

    GetMovePower = Symbol(
        [0x261C8],
        [0x2302D48],
        None,
        (
            "Gets the power of a move, factoring in Ginseng/Space Globe boosts.\n\nr0:"
            " user pointer\nr1: move pointer\nreturn: move power"
        ),
    )

    AddExpSpecial = Symbol(
        [0x263E8],
        [0x2302F68],
        None,
        (
            "Adds to a monster's experience points, subject to experience boosting"
            " effects.\n\nThis function appears to be called only under special"
            " circumstances. Possibly when granting experience from damage (e.g., Joy"
            " Ribbon)?\n\nInterestingly, the parameter in r0 isn't actually used. This"
            " might be a compiler optimization to avoid shuffling registers, since this"
            " function might be called alongside lots of other functions that have both"
            " the attacker and defender as the first two arguments.\n\nr0: attacker"
            " pointer\nr1: defender pointer\nr2: base experience gain, before boosts"
        ),
    )

    EnemyEvolution = Symbol(
        [0x265A8],
        [0x2303128],
        None,
        (
            "Checks if the specified enemy should evolve because it just defeated an"
            " ally, and if so, attempts to evolve it.\n\nr0: Pointer to the enemy to"
            " check"
        ),
    )

    TryDecreaseLevel = Symbol(
        [0x26E34],
        [0x23039B4],
        None,
        (
            "Decrease the target monster's level if possible.\n\nr0: user entity"
            " pointer\nr1: target entity pointer\nr2: number of levels to"
            " decrease\nreturn: success flag"
        ),
    )

    LevelUp = Symbol(
        [0x26EE8],
        [0x2303A68],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: user entity"
            " pointer\nr1: target entity pointer\nr2: message flag?\nr3: ?\nreturn:"
            " success flag?"
        ),
    )

    EvolveMonster = Symbol(
        [0x27B28],
        [0x23046A8],
        None,
        (
            "Makes the specified monster evolve into the specified species.\n\nr0:"
            " Pointer to the entity to evolve\nr1: ?\nr2: Species to evolve into"
        ),
    )

    GetSleepAnimationId = Symbol(
        [0x28960],
        [0x23054E0],
        None,
        (
            "Returns the animation id to be applied to a monster that has the sleep,"
            " napping, nightmare or bide status.\n\nReturns a different animation for"
            " sudowoodo and for monsters with infinite sleep turns (0x7F).\n\nr0:"
            " pointer to entity\nreturn: animation ID"
        ),
    )

    DisplayActions = Symbol(
        [0x28E8C],
        [0x2305A0C],
        None,
        (
            "Graphically displays any pending actions that have happened but haven't"
            " been shown on screen yet. All actions are displayed at the same time. For"
            " example, this delayed display system is used to display multiple monsters"
            " moving at once even though they take turns sequentially.\n\nr0: Pointer"
            " to an entity. Can be null.\nreturns: Seems to be true if there were any"
            " pending actions to display."
        ),
    )

    EndFrozenClassStatus = Symbol(
        [0x2A104],
        [0x2306C84],
        None,
        (
            "Cures the target's freeze, shadow hold, ingrain, petrified, constriction"
            " or wrap (both as user and as target) status due to the action of the"
            " user.\n\nr0: pointer to user\nr1: pointer to target\nr2: if true, the"
            " event will be printed to the log"
        ),
    )

    EndCringeClassStatus = Symbol(
        [0x2A280],
        [0x2306E00],
        None,
        (
            "Cures the target's cringe, confusion, cowering, pause, taunt, encore or"
            " infatuated status due to the action of the user, and prints the event to"
            " the log.\n\nr0: pointer to user\nr1: pointer to target"
        ),
    )

    RunMonsterAi = Symbol(
        [0x2C1EC],
        [0x2308D6C],
        None,
        (
            "Runs the AI for a single monster to determine whether the monster can act"
            " and which action it should perform if so\n\nr0: Pointer to monster\nr1: ?"
        ),
    )

    ApplyDamage = Symbol(
        [0x2CE8C],
        [0x2309A0C],
        None,
        (
            "Applies damage to a monster. Displays the damage animation, lowers its"
            " health and handles reviving if applicable.\nThe EU version has some"
            " additional checks related to printing fainting messages under specific"
            " circumstances.\n\nr0: Attacker pointer\nr1: Defender pointer\nr2: Pointer"
            " to the damage_data struct that contains info about the damage to"
            " deal\nr3: ?\nstack[0]: ?\nstack[1]: Damage source\nreturn: True if the"
            " target fainted (reviving does not count as fainting)"
        ),
    )

    AftermathCheck = Symbol(
        [0x2E900],
        [0x230B480],
        None,
        (
            "Checks if the defender has the Aftermath ability and tries to activate it"
            " if so (50% chance).\n\nThe ability won't trigger if the damage source is"
            " DAMAGE_SOURCE_EXPLOSION.\n\nr0: Attacker pointer\nr1: Defender"
            " pointer\nr2: Damage source\nreturn: True if Aftermath was activated,"
            " false if it wasn't"
        ),
    )

    GetTypeMatchupBothTypes = Symbol(
        [0x2E980],
        [0x230B500],
        None,
        (
            "Gets the type matchup for a given combat interaction, accounting for both"
            " of the user's types.\n\nCalls GetTypeMatchup twice and combines the"
            " result.\n\nr0: attacker pointer\nr1: defender pointer\nr2: attack"
            " type\nreturn: enum type_matchup"
        ),
    )

    GetTypeMatchup = Symbol(
        [0x2EB4C],
        [0x230B6CC],
        None,
        (
            "Gets the type matchup for a given combat interaction.\n\nNote that the"
            " actual monster's types on the attacker and defender pointers are not"
            " used; the pointers are only used to check conditions. The actual type"
            " matchup table lookup is done solely using the attack and target type"
            " parameters.\n\nThis factors in some conditional effects like exclusive"
            " items, statuses, etc. There's some weirdness with the Ghost type; see the"
            " comment for struct type_matchup_table.\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: target type index (0 the target's first type, 1 for"
            " the target's second type)\nr3: attack type\nreturn: enum type_matchup"
        ),
    )

    CalcDamage = Symbol(
        [0x2FAA0],
        [0x230C620],
        None,
        (
            "Probably the damage calculation function.\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: attack type\nr3: attack power\nstack[0]: crit"
            " chance\nstack[1]: [output] struct containing info about the damage"
            " calculation\nstack[2]: damage multiplier (as a binary fixed-point number"
            " with 8 fraction bits)\nstack[3]: move ID\nstack[4]: ?"
        ),
    )

    CalcRecoilDamageFixed = Symbol(
        [0x31080],
        [0x230DC00],
        None,
        (
            "Appears to calculate recoil damage to a monster.\n\nThis function wraps"
            " CalcDamageFixed using the monster as both the attacker and the defender,"
            " after doing some basic checks (like if the monster is already at 0 HP)"
            " and applying a boost from the Reckless ability if applicable.\n\nr0:"
            " entity pointer\nr1: fixed damage\nr2: ?\nr3: [output] struct containing"
            " info about the damage calculation\nstack[0]: move ID (interestingly, this"
            " doesn't seem to be used by the function)\nstack[1]: attack"
            " type\nstack[2]: damage source\nstack[3]: damage message\nothers: ?"
        ),
    )

    CalcDamageFixed = Symbol(
        [0x31134],
        [0x230DCB4],
        None,
        (
            "Appears to calculate damage from a fixed-damage effect.\n\nr0: attacker"
            " pointer\nr1: defender pointer\nr2: fixed damage\nr3: ?\nstack[0]:"
            " [output] struct containing info about the damage calculation\nstack[1]:"
            " attack type\nstack[2]: move category\nstack[3]: damage source\nstack[4]:"
            " damage message\nothers: ?"
        ),
    )

    CalcDamageFixedNoCategory = Symbol(
        [0x3129C],
        [0x230DE1C],
        None,
        (
            "A wrapper around CalcDamageFixed with the move category set to"
            " none.\n\nr0: attacker pointer\nr1: defender pointer\nr2: fixed"
            " damage\nstack[0]: [output] struct containing info about the damage"
            " calculation\nstack[1]: attack type\nstack[2]: damage source\nstack[3]:"
            " damage message\nothers: ?"
        ),
    )

    CalcDamageFixedWrapper = Symbol(
        [0x312E8],
        [0x230DE68],
        None,
        (
            "A wrapper around CalcDamageFixed.\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: fixed damage\nstack[0]: [output] struct containing info"
            " about the damage calculation\nstack[1]: attack type\nstack[2]: move"
            " category\nstack[3]: damage source\nstack[4]: damage message\nothers: ?"
        ),
    )

    ResetDamageCalcScratchSpace = Symbol(
        [0x3141C],
        [0x230DF9C],
        None,
        (
            "CalcDamage seems to use scratch space of some kind, which this function"
            " zeroes.\n\nNo params."
        ),
    )

    SpecificRecruitCheck = Symbol(
        [0x31A08],
        [0x230E588],
        None,
        (
            "Checks if a specific monster can be recruited. Called by"
            " RecruitCheck.\n\nWill return false if dungeon::recruiting_enabled is"
            " false, if the monster is Mew and dungeon::dungeon_objective is"
            " OBJECTIVE_RESCUE or if the monster is any of the special Deoxys forms or"
            " any of the 3 regis.\nIf this function returns false, RecruitCheck will"
            " return false as well.\n\nr0: Monster ID\nreturn: True if the monster can"
            " be recruited"
        ),
    )

    RecruitCheck = Symbol(
        [0x31AC4],
        [0x230E644],
        None,
        (
            "Determines if a defeated enemy will attempt to join the team\n\nr0: user"
            " entity pointer\nr1: target entity pointer\nreturn: True if the target"
            " will attempt to join the team"
        ),
    )

    TryRecruit = Symbol(
        [0x31F58],
        [0x230EAD8],
        None,
        (
            "Asks the player if they would like to recruit the enemy that was just"
            " defeated and handles the recruitment if they accept.\n\nr0: user entity"
            " pointer\nr1: monster to recruit entity pointer\nreturn: True if the"
            " monster was recruited, false if it wasn't"
        ),
    )

    TrySpawnMonsterAndTickSpawnCounter = Symbol(
        [0x325B0],
        [0x230F130],
        None,
        (
            "First ticks up the spawn counter, and if it's equal or greater than the"
            " spawn cooldown, it will try to spawn an enemy if the number of enemies is"
            " below the spawn cap.\n\nIf the spawn counter is greater than 900, it will"
            " instead perform the special spawn caused by the ability Illuminate.\n\nNo"
            " params."
        ),
    )

    AuraBowIsActive = Symbol(
        [0x335BC],
        [0x231013C],
        None,
        (
            "Checks if a monster is holding an aura bow that isn't disabled by"
            " Klutz.\n\nr0: entity pointer\nreturn: bool"
        ),
    )

    ExclusiveItemOffenseBoost = Symbol(
        [0x3366C],
        [0x23101EC],
        None,
        (
            "Gets the exclusive item boost for attack/special attack for a"
            " monster\n\nr0: entity pointer\nr1: move category index (0 for physical, 1"
            " for special)\nreturn: boost"
        ),
    )

    ExclusiveItemDefenseBoost = Symbol(
        [0x3367C],
        [0x23101FC],
        None,
        (
            "Gets the exclusive item boost for defense/special defense for a"
            " monster\n\nr0: entity pointer\nr1: move category index (0 for physical, 1"
            " for special)\nreturn: boost"
        ),
    )

    TeamMemberHasExclusiveItemEffectActive = Symbol(
        [0x33734],
        [0x23102B4],
        None,
        (
            "Checks if any team member is under the effects of a certain exclusive item"
            " effect.\n\nr0: exclusive item effect ID\nreturn: bool"
        ),
    )

    TrySpawnEnemyItemDrop = Symbol(
        [0x338CC],
        [0x231044C],
        None,
        (
            "Determine what item a defeated enemy should drop, if any, then (probably?)"
            " spawn that item underneath them.\n\nThis function is called at the time"
            " when an enemy is defeated from ApplyDamage.\n\nr0: attacker entity (who"
            " defeated the enemy)\nr1: defender entity (who was defeated)"
        ),
    )

    TickNoSlipCap = Symbol(
        [0x33A84],
        [0x2310604],
        None,
        (
            "Checks if the entity is a team member and holds the No-Slip Cap, and if so"
            " attempts to make one item in the bag sticky.\n\nr0: pointer to entity"
        ),
    )

    TickStatusAndHealthRegen = Symbol(
        [0x34F68],
        [0x2311AE8],
        None,
        (
            "Applies the natural HP regen effect by taking modifiers into account"
            " (Poison Heal, Heal Ribbon, weather-related regen). Then it ticks down"
            " counters for volatile status effects, and heals them if the counter"
            " reached zero.\n\nr0: pointer to entity"
        ),
    )

    InflictSleepStatusSingle = Symbol(
        [0x35704],
        [0x2312284],
        None,
        (
            "This is called by TryInflictSleepStatus.\n\nr0: entity pointer\nr1: number"
            " of turns"
        ),
    )

    TryInflictSleepStatus = Symbol(
        [0x357B8],
        [0x2312338],
        None,
        (
            "Inflicts the Sleep status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2:"
            " number of turns\nr3: flag to log a message on failure"
        ),
    )

    TryInflictNightmareStatus = Symbol(
        [0x35B2C],
        [0x23126AC],
        None,
        (
            "Inflicts the Nightmare status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2:"
            " number of turns"
        ),
    )

    TryInflictNappingStatus = Symbol(
        [0x35C40],
        [0x23127C0],
        None,
        (
            "Inflicts the Napping status condition (from Rest) on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2:"
            " number of turns"
        ),
    )

    TryInflictYawningStatus = Symbol(
        [0x35D50],
        [0x23128D0],
        None,
        (
            "Inflicts the Yawning status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2:"
            " number of turns"
        ),
    )

    TryInflictSleeplessStatus = Symbol(
        [0x35E60],
        [0x23129E0],
        None,
        (
            "Inflicts the Sleepless status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer"
        ),
    )

    TryInflictPausedStatus = Symbol(
        [0x35F4C],
        [0x2312ACC],
        None,
        (
            "Inflicts the Paused status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2:"
            " ?\nr3: number of turns\nstack[0]: flag to log a message on"
            " failure\nstack[1]: flag to only perform the check for inflicting without"
            " actually inflicting\nreturn: Whether or not the status could be inflicted"
        ),
    )

    TryInflictInfatuatedStatus = Symbol(
        [0x3608C],
        [0x2312C0C],
        None,
        (
            "Inflicts the Infatuated status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: flag"
            " to log a message on failure\nr3: flag to only perform the check for"
            " inflicting without actually inflicting\nreturn: Whether or not the status"
            " could be inflicted"
        ),
    )

    TryInflictBurnStatus = Symbol(
        [0x36218],
        [0x2312D98],
        None,
        (
            "Inflicts the Burn status condition on a target monster if possible.\n\nr0:"
            " user entity pointer\nr1: target entity pointer\nr2: flag to apply some"
            " special effect alongside the burn?\nr3: flag to log a message on"
            " failure\nstack[0]: flag to only perform the check for inflicting without"
            " actually inflicting\nreturn: Whether or not the status could be inflicted"
        ),
    )

    TryInflictBurnStatusWholeTeam = Symbol(
        [0x364F8],
        [0x2313078],
        None,
        (
            "Inflicts the Burn status condition on all team members if possible.\n\nNo"
            " params."
        ),
    )

    TryInflictPoisonedStatus = Symbol(
        [0x36544],
        [0x23130C4],
        None,
        (
            "Inflicts the Poisoned status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: flag"
            " to log a message on failure\nr3: flag to only perform the check for"
            " inflicting without actually inflicting\nreturn: Whether or not the status"
            " could be inflicted"
        ),
    )

    TryInflictBadlyPoisonedStatus = Symbol(
        [0x3681C],
        [0x231339C],
        None,
        (
            "Inflicts the Badly Poisoned status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: flag"
            " to log a message on failure\nr3: flag to only perform the check for"
            " inflicting without actually inflicting\nreturn: Whether or not the status"
            " could be inflicted"
        ),
    )

    TryInflictFrozenStatus = Symbol(
        [0x36AD8],
        [0x2313658],
        None,
        (
            "Inflicts the Frozen status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: flag"
            " to log a message on failure"
        ),
    )

    TryInflictConstrictionStatus = Symbol(
        [0x36D00],
        [0x2313880],
        None,
        (
            "Inflicts the Constriction status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2:"
            " animation ID\nr3: flag to log a message on failure"
        ),
    )

    TryInflictShadowHoldStatus = Symbol(
        [0x36E58],
        [0x23139D8],
        None,
        (
            "Inflicts the Shadow Hold (AKA Immobilized) status condition on a target"
            " monster if possible.\n\nr0: user entity pointer\nr1: target entity"
            " pointer\nr2: flag to log a message on failure"
        ),
    )

    TryInflictIngrainStatus = Symbol(
        [0x37010],
        [0x2313B90],
        None,
        (
            "Inflicts the Ingrain status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer"
        ),
    )

    TryInflictWrappedStatus = Symbol(
        [0x370D4],
        [0x2313C54],
        None,
        (
            "Inflicts the Wrapped status condition on a target monster if"
            " possible.\n\nThis also gives the user the Wrap status (Wrapped around"
            " foe).\n\nr0: user entity pointer\nr1: target entity pointer"
        ),
    )

    FreeOtherWrappedMonsters = Symbol(
        [0x372D0],
        [0x2313E50],
        None,
        (
            "Frees from the wrap status all monsters which are wrapped by/around the"
            " monster passed as parameter.\n\nr0: pointer to entity"
        ),
    )

    TryInflictPetrifiedStatus = Symbol(
        [0x3734C],
        [0x2313ECC],
        None,
        (
            "Inflicts the Petrified status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer"
        ),
    )

    LowerOffensiveStat = Symbol(
        [0x374DC],
        [0x231405C],
        None,
        (
            "Lowers the specified offensive stat on the target monster.\n\nr0: user"
            " entity pointer\nr1: target entity pointer\nr2: stat index\nr3: number of"
            " stages\nstack[0]: ?\nstack[1]: ?"
        ),
    )

    LowerDefensiveStat = Symbol(
        [0x376F4],
        [0x2314274],
        None,
        (
            "Lowers the specified defensive stat on the target monster.\n\nr0: user"
            " entity pointer\nr1: target entity pointer\nr2: stat index\nr3: number of"
            " stages\nstack[0]: ?\nstack[1]: ?"
        ),
    )

    BoostOffensiveStat = Symbol(
        [0x3787C],
        [0x23143FC],
        None,
        (
            "Boosts the specified offensive stat on the target monster.\n\nr0: user"
            " entity pointer\nr1: target entity pointer\nr2: stat index\nr3: number of"
            " stages"
        ),
    )

    BoostDefensiveStat = Symbol(
        [0x379E8],
        [0x2314568],
        None,
        (
            "Boosts the specified defensive stat on the target monster.\n\nr0: user"
            " entity pointer\nr1: target entity pointer\nr2: stat index\nr3: number of"
            " stages"
        ),
    )

    ApplyOffensiveStatMultiplier = Symbol(
        [0x37C20],
        [0x23147A0],
        None,
        (
            "Applies a multiplier to the specified offensive stat on the target"
            " monster.\n\nThis affects struct"
            " monster_stat_modifiers::offensive_multipliers, for moves like Charm and"
            " Memento.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: stat"
            " index\nr3: multiplier\nstack[0]: ?"
        ),
    )

    ApplyDefensiveStatMultiplier = Symbol(
        [0x37E44],
        [0x23149C4],
        None,
        (
            "Applies a multiplier to the specified defensive stat on the target"
            " monster.\n\nThis affects struct"
            " monster_stat_modifiers::defensive_multipliers, for moves like"
            " Screech.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: stat"
            " index\nr3: multiplier\nstack[0]: ?"
        ),
    )

    BoostHitChanceStat = Symbol(
        [0x37FC4],
        [0x2314B44],
        None,
        (
            "Boosts the specified hit chance stat (accuracy or evasion) on the target"
            " monster.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: stat"
            " index"
        ),
    )

    LowerHitChanceStat = Symbol(
        [0x3810C],
        [0x2314C8C],
        None,
        (
            "Lowers the specified hit chance stat (accuracy or evasion) on the target"
            " monster.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: stat"
            " index\nr3: ? (Irdkwia's notes say this is the number of stages, but I'm"
            " pretty sure that's incorrect)"
        ),
    )

    TryInflictCringeStatus = Symbol(
        [0x382C8],
        [0x2314E48],
        None,
        (
            "Inflicts the Cringe status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: flag"
            " to log a message on failure\nr3: flag to only perform the check for"
            " inflicting without actually inflicting\nreturn: Whether or not the status"
            " could be inflicted"
        ),
    )

    TryInflictParalysisStatus = Symbol(
        [0x38424],
        [0x2314FA4],
        None,
        (
            "Inflicts the Paralysis status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: flag"
            " to log a message on failure\nr3: flag to only perform the check for"
            " inflicting without actually inflicting\nreturn: Whether or not the status"
            " could be inflicted"
        ),
    )

    BoostSpeed = Symbol(
        [0x386F0],
        [0x2315270],
        None,
        (
            "Boosts the speed of the target monster.\n\nIf the number of turns"
            " specified is 0, a random turn count will be selected using the default"
            " SPEED_BOOST_TURN_RANGE.\n\nr0: user entity pointer\nr1: target entity"
            " pointer\nr2: number of stages\nr3: number of turns\nstack[0]: flag to log"
            " a message on failure"
        ),
    )

    BoostSpeedOneStage = Symbol(
        [0x3881C],
        [0x231539C],
        None,
        (
            "A wrapper around BoostSpeed with the number of stages set to 1.\n\nr0:"
            " user entity pointer\nr1: target entity pointer\nr2: number of turns\nr3:"
            " flag to log a message on failure"
        ),
    )

    LowerSpeed = Symbol(
        [0x38834],
        [0x23153B4],
        None,
        (
            "Lowers the speed of the target monster.\n\nr0: user entity pointer\nr1:"
            " target entity pointer\nr2: number of stages\nr3: flag to log a message on"
            " failure"
        ),
    )

    TrySealMove = Symbol(
        [0x3899C],
        [0x231551C],
        None,
        (
            "Seals one of the target monster's moves. The move to be sealed is randomly"
            " selected.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: flag"
            " to log a message on failure\nreturn: Whether or not a move was sealed"
        ),
    )

    BoostOrLowerSpeed = Symbol(
        [0x38B0C],
        [0x231568C],
        None,
        (
            "Randomly boosts or lowers the speed of the target monster by one stage"
            " with equal probability.\n\nr0: user entity pointer\nr1: target entity"
            " pointer"
        ),
    )

    ResetHitChanceStat = Symbol(
        [0x38B6C],
        [0x23156EC],
        None,
        (
            "Resets the specified hit chance stat (accuracy or evasion) back to normal"
            " on the target monster.\n\nr0: user entity pointer\nr1: target entity"
            " pointer\nr2: stat index\nr3: ?"
        ),
    )

    TryActivateQuickFeet = Symbol(
        [0x38CFC],
        [0x231587C],
        None,
        (
            "Activate the Quick Feet ability on the defender, if the monster has it and"
            " it's active.\n\nr0: attacker pointer\nr1: defender pointer\nreturn: bool,"
            " whether or not the ability was activated"
        ),
    )

    TryInflictConfusedStatus = Symbol(
        [0x38E18],
        [0x2315998],
        None,
        (
            "Inflicts the Confused status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: flag"
            " to log a message on failure\nr3: flag to only perform the check for"
            " inflicting without actually inflicting\nreturn: Whether or not the status"
            " could be inflicted"
        ),
    )

    TryInflictCoweringStatus = Symbol(
        [0x3904C],
        [0x2315BCC],
        None,
        (
            "Inflicts the Cowering status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: flag"
            " to log a message on failure\nr3: flag to only perform the check for"
            " inflicting without actually inflicting\nreturn: Whether or not the status"
            " could be inflicted"
        ),
    )

    TryRestoreHp = Symbol(
        [0x3914C],
        [0x2315CCC],
        None,
        (
            "Restore HP of the target monster if possible.\n\nr0: user entity"
            " pointer\nr1: target entity pointer\nr2: HP to restore\nreturn: success"
            " flag"
        ),
    )

    TryIncreaseHp = Symbol(
        [0x391C4],
        [0x2315D44],
        None,
        (
            "Restore HP and possibly boost max HP of the target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: HP"
            " to restore\nr3: max HP boost\nstack[0]: flag to log a message on"
            " failure\nreturn: Success flag"
        ),
    )

    RevealItems = Symbol(
        [0x394F0],
        [0x2316070],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: user entity"
            " pointer\nr1: target entity pointer"
        ),
    )

    RevealStairs = Symbol(
        [0x39580],
        [0x2316100],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: user entity"
            " pointer\nr1: target entity pointer"
        ),
    )

    RevealEnemies = Symbol(
        [0x3963C],
        [0x23161BC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: user entity"
            " pointer\nr1: target entity pointer"
        ),
    )

    TryInflictLeechSeedStatus = Symbol(
        [0x396CC],
        [0x231624C],
        None,
        (
            "Inflicts the Leech Seed status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: flag"
            " to log a message on failure\nr3: flag to only perform the check for"
            " inflicting without actually inflicting\nreturn: Whether or not the status"
            " could be inflicted"
        ),
    )

    TryInflictDestinyBond = Symbol(
        [0x39930],
        [0x23164B0],
        None,
        (
            "Inflicts the Destiny Bond status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer"
        ),
    )

    IsBlinded = Symbol(
        [0x3B6C4],
        [0x2318244],
        None,
        (
            "Returns true if the monster has the blinded status (see"
            " statuses::blinded), or if it is not the leader and is holding Y-Ray"
            " Specs.\n\nr0: pointer to entity\nr1: flag for whether to check for the"
            " held item\nreturn: bool"
        ),
    )

    RestoreMovePP = Symbol(
        [0x3BB00],
        [0x2318680],
        None,
        (
            "Restores the PP of all the target's moves by the specified amount.\n\nr0:"
            " user entity pointer\nr1: target entity pointer\nr2: PP to restore\nr3:"
            " flag to suppress message logging"
        ),
    )

    SetReflectDamageCountdownTo4 = Symbol(
        [0x3C2A0],
        [0x2318E20],
        None,
        (
            "Sets the monster's reflect damage countdown to a global value"
            " (0x4).\n\nr0: pointer to entity"
        ),
    )

    HasConditionalGroundImmunity = Symbol(
        [0x3C92C],
        [0x23194AC],
        None,
        (
            "Checks if a monster is currently immune to Ground-type moves for reasons"
            " other than typing and ability.\n\nThis includes checks for Gravity and"
            " Magnet Rise.\n\nr0: entity pointer\nreturn: bool"
        ),
    )

    Conversion2IsActive = Symbol(
        [0x3D6F4],
        [0x231A274],
        None,
        (
            "Checks if the monster is under the effect of Conversion 2 (its type was"
            " changed).\n\nReturns 1 if the effects is a status, 2 if it comes from an"
            " exclusive item, 0 otherwise.\n\nr0: pointer to entity\nreturn: int"
        ),
    )

    AiConsiderMove = Symbol(
        [0x3D760],
        [0x231A2E0],
        None,
        (
            "The AI uses this function to check if a move has any potential targets, to"
            " calculate the list of potential targets and to calculate the move's"
            " special weight.\nThis weight will be higher if the pokémon has weak-type"
            " picker and the target is weak to the move (allies only, enemies always"
            " get a result of 1 even if the move is super effective). More things could"
            " affect the result.\nThis function also sets the flag can_be_used on the"
            " ai_possible_move struct if it makes sense to use it.\nMore research is"
            " needed. There's more documentation about this special weight. Does all"
            " the documented behavior happen in this function?\n\nr0: ai_possible_move"
            " struct for this move\nr1: Entity pointer\nr2: Move pointer\nreturn:"
            " Move's calculated special weight"
        ),
    )

    TryAddTargetToAiTargetList = Symbol(
        [0x3DE90],
        [0x231AA10],
        None,
        (
            "Checks if the specified target is eligible to be targeted by the AI and if"
            " so adds it to the list of targets. This function also fills an array that"
            " seems to contain the directions in which the user should turn to look at"
            " each of the targets in the list, as well as a third unknown array.\n\nr0:"
            " Number of existing targets in the list\nr1: Move's AI range field\nr2:"
            " User entity pointer\nr3: Target entity pointer\nstack[0]: Move"
            " pointer\nstack[1]: check_all_conditions parameter to pass to"
            " IsAiTargetEligible\nreturn: New number of targets in the target list"
        ),
    )

    IsAiTargetEligible = Symbol(
        [0x3DF84],
        [0x231AB04],
        None,
        (
            "Checks if a given target is eligible to be targeted by the AI with a"
            " certain move\n\nr0: Move's AI range field\nr1: User entity pointer\nr2:"
            " Target entity pointer\nr3: Move pointer\nstack[0]: True to check all the"
            " possible move_ai_condition values, false to only check for"
            " move_ai_condition::AI_CONDITION_RANDOM (if the move has a different ai"
            " condition, the result will be false).\nreturn: True if the target is"
            " eligible, false otherwise"
        ),
    )

    IsTargetInRange = Symbol(
        [0x3E574],
        [0x231B0F4],
        None,
        (
            "Returns true if the target is within range of the user's move, false"
            " otherwise.\n\nIf the user does not have Course Checker, it simply checks"
            " if the distance between user and target is less or equal than the move"
            " range.\nOtherwise, it will iterate through all tiles in the direction"
            " specified, checking for walls or other monsters in the way, and return"
            " false if they are found.\n\nr0: user pointer\nr1: target pointer\nr2:"
            " direction ID\nr3: move range (in number of tiles)"
        ),
    )

    ShouldUsePp = Symbol(
        [0x3E680],
        [0x231B200],
        None,
        (
            "Checks if a monster should use PP when using a move. It also displays the"
            " corresponding animation if PP Saver triggers and prints the required"
            " messages to the message log.\n\nr0: entity pointer\nreturn: True if the"
            " monster should not use PP, false if it should."
        ),
    )

    GetEntityMoveTargetAndRange = Symbol(
        [0x3EB8C],
        [0x231B70C],
        None,
        (
            "Gets the move target-and-range field when used by a given entity. See"
            " struct move_target_and_range in the C headers.\n\nr0: entity pointer\nr1:"
            " move pointer\nr2: AI flag (same as GetMoveTargetAndRange)\nreturn: move"
            " target and range"
        ),
    )

    IsInSpawnList = Symbol(
        [0x3F2DC],
        [0x231BE5C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: spawn_list_ptr\nr1:"
            " monster ID\nreturn: bool"
        ),
    )

    ChangeShayminForme = Symbol(
        [0x3F3CC],
        [0x231BF4C],
        None,
        (
            "forme:\n  1: change from Land to Sky\n  2: change from Sky to"
            " Land\nresult:\n  0: not Shaymin\n  1: not correct Forme\n  2: frozen\n "
            " 3: ok\n\nNote: unverified, ported from Irdkwia's notes\n\nr0: Target\nr1:"
            " forme\nreturn: result"
        ),
    )

    ApplyItemEffect = Symbol(
        [0x3F56C],
        [0x231C0EC],
        None,
        (
            "Seems to apply an item's effect via a giant switch statement?\n\nr3:"
            " attacker pointer\nstack[0]: defender pointer\nstack[1]: thrown item"
            " pointer\nothers: ?"
        ),
    )

    ViolentSeedBoost = Symbol(
        [0x40D04],
        [0x231D884],
        None,
        (
            "Applies the Violent Seed boost to an entity.\n\nr0: attacker pointer\nr1:"
            " defender pointer"
        ),
    )

    ApplyGummiBoostsDungeonMode = Symbol(
        [0x40FA8],
        [0x231DB28],
        None,
        (
            "Applies the IQ and possible stat boosts from eating a Gummi to the target"
            " monster.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: Gummi"
            " type ID\nr3: Stat boost amount, if a random stat boost occurs"
        ),
    )

    GetMaxPpWrapper = Symbol(
        [0x428D8],
        [0x231F458],
        None,
        (
            "Gets the maximum PP for a given move. A wrapper around the function in the"
            " ARM 9 binary.\n\nr0: move pointer\nreturn: max PP for the given move,"
            " capped at 99"
        ),
    )

    MoveIsNotPhysical = Symbol(
        [0x42900],
        [0x231F480],
        None,
        "Checks if a move isn't a physical move.\n\nr0: move ID\nreturn: bool",
    )

    TryPounce = Symbol(
        [0x43B08],
        [0x2320688],
        None,
        (
            "Makes the target monster execute the Pounce action in a given direction if"
            " possible.\n\nIf the direction ID is 8, the target will pounce in the"
            " direction it's currently facing.\n\nr0: user entity pointer\nr1: target"
            " entity pointer\nr2: direction ID"
        ),
    )

    TryBlowAway = Symbol(
        [0x43CC8],
        [0x2320848],
        None,
        (
            "Blows away the target monster in a given direction if possible.\n\nr0:"
            " user entity pointer\nr1: target entity pointer\nr2: direction ID"
        ),
    )

    TryExplosion = Symbol(
        [0x44670],
        [0x23211F0],
        None,
        (
            "Creates an explosion if possible.\n\nThe target monster is considered the"
            " source of the explosion.\n\nr0: user entity pointer\nr1: target entity"
            " pointer\nr2: coordinates where the explosion should take place"
            " (unverified)\nr3: ?\nstack[0]: ?\nstack[1]: damage source (normally"
            " DAMAGE_SOURCE_EXPLOSION)"
        ),
    )

    TryWarp = Symbol(
        [0x44BF0],
        [0x2321770],
        None,
        (
            "Makes the target monster warp if possible.\n\nr0: user entity pointer\nr1:"
            " target entity pointer\nr2: warp type\nr3: position (if warp type is"
            " position-based)"
        ),
    )

    MoveHitCheck = Symbol(
        [0x47B30],
        [0x23246B0],
        None,
        (
            "Determines if a move used hits or misses the target. It gets called twice"
            " per target, once with r3 = false and a second time with r3 = true.\n\nr0:"
            " Attacker\nr1: Defender\nr2: Pointer to move data\nr3: True if the move's"
            " first accuracy (accuracy1) should be used, false if its second accuracy"
            " (accuracy2) should be used instead.\nreturns: True if the move hits,"
            " false if it misses."
        ),
    )

    IsHyperBeamVariant = Symbol(
        [0x4841C],
        [0x2324F9C],
        None,
        (
            "Checks if a move is a Hyper Beam variant that requires a a turn to"
            " recharge.\n\nInclude moves: Frenzy Plant, Hydro Cannon, Hyper Beam, Blast"
            " Burn, Rock Wrecker, Giga Impact, Roar of Time\n\nr0: move\nreturn: bool"
        ),
    )

    HasMaxGinsengBoost99 = Symbol(
        [0x48680],
        [0x2325200],
        None,
        (
            "Checks if a move has a max Ginseng boost value of 99\n\nr0: Move\nreturn:"
            " True if the move's max Ginseng boost is 99, false otherwise."
        ),
    )

    DungeonRandOutcomeUserTargetInteraction = Symbol(
        [0x4881C],
        [0x232539C],
        None,
        (
            "Like DungeonRandOutcome, but specifically for user-target"
            " interactions.\n\nThis modifies the underlying random process depending on"
            " factors like Serene Grace, and whether or not either entity has"
            " fainted.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: base"
            " success percentage (100*p). 0 is treated specially and guarantees"
            " success.\nreturns: True if the random check passed, false otherwise."
        ),
    )

    DungeonRandOutcomeUserAction = Symbol(
        [0x48908],
        [0x2325488],
        None,
        (
            "Like DungeonRandOutcome, but specifically for user actions.\n\nThis"
            " modifies the underlying random process to factor in Serene Grace (and"
            " checks whether the user is a valid entity).\n\nr0: entity pointer\nr1:"
            " base success percentage (100*p). 0 is treated specially and guarantees"
            " success.\nreturns: True if the random check passed, false otherwise."
        ),
    )

    CanAiUseMove = Symbol(
        [0x4895C],
        [0x23254DC],
        None,
        (
            "Checks if an AI-controlled monster can use a move.\nWill return false if"
            " the any of the flags move::f_exists, move::f_subsequent_in_link_chain or"
            " move::f_disabled is true. The function does not check if the flag"
            " move::f_enabled_for_ai is set. This function also returns true if the"
            " call to CanMonsterUseMove is true.\nThe function contains a loop that is"
            " supposed to check other moves after the specified one, but the loop"
            " breaks after it finds a move that isn't linked, which is always true"
            " given the checks in place at the start of the function.\n\nr0: Entity"
            " pointer\nr1: Move index\nr2: extra_checks parameter when calling"
            " CanMonsterUseMove\nreturn: True if the AI can use the move (not"
            " accounting for move::f_enabled_for_ai)"
        ),
    )

    CanMonsterUseMove = Symbol(
        [0x48A0C],
        [0x232558C],
        None,
        (
            "Checks if a monster can use the given move.\nWill always return true for"
            " the regular attack. Will return false if the move if the flag"
            " move::f_disabled is true, if the flag move::f_sealed is true. More things"
            " will be checked if the extra_checks parameter is true.\n\nr0: Entity"
            " pointer\nr1: Move pointer\nr2: True to check whether the move is out of"
            " PP, whether it can be used under the taunted status and whether the"
            " encore status prevents using the move\nreturn: True if the monster can"
            " use the move, false otherwise."
        ),
    )

    UpdateMovePp = Symbol(
        [0x48C74],
        [0x23257F4],
        None,
        (
            "Updates the PP of any moves that were used by a monster, if PP should be"
            " consumed.\n\nr0: entity pointer\nr1: flag for whether or not PP should be"
            " consumed"
        ),
    )

    GetDamageSourceWrapper = Symbol(
        [0x48D2C],
        [0x23258AC],
        None,
        (
            "Wraps GetDamageSource (in arm9) for a move info struct rather than a move"
            " ID.\n\nr0: move info pointer\nr1: item ID\nreturn: damage source"
        ),
    )

    LowerSshort = Symbol(
        [0x48D4C],
        [0x23258CC],
        None,
        (
            "Gets the lower 2 bytes of a 4-byte number and interprets it as a signed"
            " short.\n\nr0: 4-byte number x\nreturn: (short) x"
        ),
    )

    GetMoveAnimationId = Symbol(
        [0x499F8],
        [0x2326578],
        None,
        (
            "Returns the move animation ID that should be played for a move.\nIt"
            " contains a check for weather ball. After that, if the parameter"
            " should_play_alternative_animation is false, the move ID is returned. If"
            " it's true, there's a bunch of manual ID checks that result on a certain"
            " hardcoded return value.\n\nr0: Move ID\nr1: Apparent weather for the"
            " monster who used the move\nr2: Result of"
            " ShouldMovePlayADifferentAnimation\nreturn: Move animation ID"
        ),
    )

    ShouldMovePlayAlternativeAnimation = Symbol(
        [0x49B60],
        [0x23266E0],
        None,
        (
            "Checks whether a moved used by a monster should play its alternative"
            " animation. Includes checks for Curse, Snore, Sleep Talk, Solar Beam and"
            " 2-turn moves.\n\nr0: Pointer to the entity that used the move\nr1: Move"
            " pointer\nreturn: True if the move should play its alternative animation"
        ),
    )

    ExecuteMoveEffect = Symbol(
        [0x52724],
        [0x232F2A4],
        None,
        (
            "Handles the effects that happen after a move is used. Includes a loop that"
            " is run for each target, mutiple ability checks and the giant switch"
            " statement that executes the effect of the move used given its ID.\n\nr0:"
            " pointer to some struct\nr1: attacker pointer\nr2: pointer to move"
            " data\nr3: ?\nstack[0]: ?"
        ),
    )

    DoMoveDamageInlined = Symbol(
        [0x56930],
        [0x23334B0],
        None,
        (
            "Exactly the same as DoMoveDamage, except it appears DealDamage was"
            " inlined.\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether or not damage was dealt"
        ),
    )

    DealDamage = Symbol(
        [0x569E0],
        [0x2333560],
        None,
        (
            "Deals damage from a move or item used by an attacking monster on a"
            " defending monster.\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: damage multiplier (as a binary fixed-point number with 8"
            " fraction bits)\nstack[0]: item ID\nreturn: amount of damage dealt"
        ),
    )

    CalcDamageProjectile = Symbol(
        [0x56B0C],
        [0x233368C],
        None,
        (
            "Appears to calculate damage from a variable-damage projectile.\n\nr0:"
            " entity pointer 1?\nr1: entity pointer 2?\nr2: move pointer\nr3: move"
            " power\nstack[0]: damage multiplier (as a binary fixed-point number with 8"
            " fraction bits)\nstack[1]: item ID of the projectile\nreturn: Calculated"
            " damage"
        ),
    )

    CalcDamageFinal = Symbol(
        [0x56C2C],
        [0x23337AC],
        None,
        (
            "Last function called by DealDamage to determine the final damage dealt by"
            " the move. The result of this call is the return value of DealDamage."
            " \n\nr0: Attacker pointer\nr1: Defender pointer\nr2: Move pointer\nr3:"
            " [output] struct containing info about the damage calculation\nstack[0]:"
            " Damage source\nreturn: Calculated damage"
        ),
    )

    StatusCheckerCheck = Symbol(
        [0x56F34],
        [0x2333AB4],
        None,
        (
            "Determines if using a given move against its intended targets would be"
            " redundant because all of them already have the effect caused by said"
            " move.\n\nr0: Pointer to the entity that is considering using the"
            " move\nr1: Move pointer\nreturn: True if it makes sense to use the move,"
            " false if it would be redundant given the effects it causes and the"
            " effects that all the targets already have."
        ),
    )

    GetApparentWeather = Symbol(
        [0x58BC8],
        [0x2335748],
        None,
        (
            "Get the weather, as experienced by a specific entity.\n\nr0: entity"
            " pointer\nreturn: weather ID"
        ),
    )

    TryWeatherFormChange = Symbol(
        [0x59030],
        [0x2335BB0],
        None,
        (
            "Tries to change a monster into one of its weather-related alternative"
            " forms. Applies to Castform and Cherrim, and checks for their unique"
            " abilities.\n\nr0: pointer to entity"
        ),
    )

    ActivateSportCondition = Symbol(
        [0x5930C],
        [0x2335E8C],
        None,
        (
            "Activates the Mud Sport or Water Sport condition on the dungeon floor for"
            " some number of turns.\n\nr0: water sport flag (false for Mud Sport, true"
            " for Water Sport)"
        ),
    )

    DigitCount = Symbol(
        [0x59530],
        [0x23360B0],
        None,
        (
            "Counts the number of digits in a nonnegative integer.\n\nIf the number is"
            " negative, it is cast to a uint16_t before counting digits.\n\nr0:"
            " int\nreturn: number of digits in int"
        ),
    )

    LoadTextureUi = Symbol(
        [0x59580],
        [0x2336100],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    DisplayNumberTextureUi = Symbol(
        [0x5974C],
        [0x23362CC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: x position\nr1: y"
            " position\nr2: number\nr3: ally_mode\nreturn: xsize"
        ),
    )

    DisplayCharTextureUi = Symbol(
        [0x59854],
        [0x23363D4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: call_back_str\nr1: x"
            " position\nr2: y position\nr3: char_id\nstack[0]: ?\nreturn: ?"
        ),
    )

    DisplayUi = Symbol(
        [0x598DC],
        [0x233645C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GetTile = Symbol(
        [0x5A14C],
        [0x2336CCC],
        None,
        (
            "Get the tile at some position. If the coordinates are out of bounds,"
            " returns a default tile.\n\nr0: x position\nr1: y position\nreturn: tile"
            " pointer"
        ),
    )

    GetTileSafe = Symbol(
        [0x5A1B4],
        [0x2336D34],
        None,
        (
            "Get the tile at some position. If the coordinates are out of bounds,"
            " returns a pointer to a copy of the default tile.\n\nr0: x position\nr1: y"
            " position\nreturn: tile pointer"
        ),
    )

    IsFullFloorFixedRoom = Symbol(
        [0x5A224],
        [0x2336DA4],
        None,
        (
            "Checks if the current fixed room on the dungeon generation info"
            " corresponds to a fixed, full-floor layout.\n\nThe first non-full-floor"
            " fixed room is 0xA5, which is for Sealed Chambers.\n\nreturn: bool"
        ),
    )

    GetStairsRoom = Symbol(
        [0x5A478],
        [0x2336FF8],
        None,
        "Returns the index of the room that contains the stairs\n\nreturn: Room index",
    )

    GetRandomSpawnMonsterID = Symbol(
        [0x5BFE8],
        [0x2338B68],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: monster ID?",
    )

    GravityIsActive = Symbol(
        [0x5C3E0],
        [0x2338F60],
        None,
        "Checks if gravity is active on the floor.\n\nreturn: bool",
    )

    ShouldBoostKecleonShopSpawnChance = Symbol(
        [0x5C510],
        [0x2339090],
        None,
        (
            "Gets the boost_kecleon_shop_spawn_chance field on the dungeon"
            " struct.\n\nreturn: bool"
        ),
    )

    SetShouldBoostKecleonShopSpawnChance = Symbol(
        [0x5C528],
        [0x23390A8],
        None,
        (
            "Sets the boost_kecleon_shop_spawn_chance field on the dungeon struct to"
            " the given value.\n\nr0: bool to set the flag to"
        ),
    )

    UpdateShouldBoostKecleonShopSpawnChance = Symbol(
        [0x5C540],
        [0x23390C0],
        None,
        (
            "Sets the boost_kecleon_shop_spawn_chance field on the dungeon struct"
            " depending on if a team member has the exclusive item effect for more"
            " kecleon shops.\n\nNo params."
        ),
    )

    IsSecretBazaar = Symbol(
        [0x5C614],
        [0x2339194],
        None,
        "Checks if the current floor is the Secret Bazaar.\n\nreturn: bool",
    )

    ShouldBoostHiddenStairsSpawnChance = Symbol(
        [0x5C63C],
        [0x23391BC],
        None,
        (
            "Gets the boost_hidden_stairs_spawn_chance field on the dungeon"
            " struct.\n\nreturn: bool"
        ),
    )

    SetShouldBoostHiddenStairsSpawnChance = Symbol(
        [0x5C654],
        [0x23391D4],
        None,
        (
            "Sets the boost_hidden_stairs_spawn_chance field on the dungeon struct to"
            " the given value.\n\nr0: bool to set the flag to"
        ),
    )

    UpdateShouldBoostHiddenStairsSpawnChance = Symbol(
        [0x5C66C],
        [0x23391EC],
        None,
        (
            "Sets the boost_hidden_stairs_spawn_chance field on the dungeon struct"
            " depending on if a team member has the exclusive item effect for more"
            " hidden stairs.\n\nNo params."
        ),
    )

    IsSecretRoom = Symbol(
        [0x5C6AC],
        [0x233922C],
        None,
        (
            "Checks if the current floor is the Secret Room fixed floor (from hidden"
            " stairs).\n\nreturn: bool"
        ),
    )

    IsSecretFloor = Symbol(
        [0x5C6D4],
        [0x2339254],
        None,
        (
            "Checks if the current floor is a secret bazaar or a secret"
            " room.\n\nreturn: bool"
        ),
    )

    GetDungeonGenInfoUnk0C = Symbol(
        [0x5C8D0], [0x2339450], None, "return: dungeon_generation_info::field_0xc"
    )

    GetMinimapData = Symbol(
        [0x5D168],
        [0x2339CE8],
        None,
        (
            "Returns a pointer to the minimap_display_data struct in the dungeon"
            " struct.\n\nreturn: minimap_display_data*"
        ),
    )

    SetMinimapDataE447 = Symbol(
        [0x5E268],
        [0x233ADE8],
        None,
        (
            "Sets minimap_display_data::field_0xE447 to the specified value\n\nr0:"
            " Value to set the field to"
        ),
    )

    GetMinimapDataE447 = Symbol(
        [0x5E280],
        [0x233AE00],
        None,
        (
            "Exclusive to the EU ROM. Returns"
            " minimap_display_data::field_0xE447.\n\nreturn:"
            " minimap_display_data::field_0xE447"
        ),
    )

    SetMinimapDataE448 = Symbol(
        [0x5E294],
        [0x233AE14],
        None,
        (
            "Sets minimap_display_data::field_0xE448 to the specified value\n\nr0:"
            " Value to set the field to"
        ),
    )

    LoadFixedRoomDataVeneer = Symbol(
        [0x5E688],
        [0x233B208],
        None,
        (
            "Likely a linker-generated veneer for LoadFixedRoomData.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nNo"
            " params."
        ),
    )

    IsNormalFloor = Symbol(
        [0x5E6B8],
        [0x233B238],
        None,
        (
            "Checks if the current floor is a normal layout.\n\n'Normal' means any"
            " layout that is NOT one of the following:\n- Hidden stairs floors\n-"
            " Golden Chamber\n- Challenge Request floor\n- Outlaw hideout\n- Treasure"
            " Memo floor\n- Full-room fixed floors (ID < 0xA5) [0xA5 == Sealed"
            " Chamber]\n\nreturn: bool"
        ),
    )

    GenerateFloor = Symbol(
        [0x5E73C],
        [0x233B2BC],
        None,
        (
            "This is the master function that generates the dungeon floor.\n\nVery"
            " loosely speaking, this function first tries to generate a valid floor"
            " layout. Then it tries to spawn entities in a valid configuration."
            " Finally, it performs cleanup and post-processing depending on the"
            " dungeon.\n\nIf a spawn configuration is invalid, the entire floor layout"
            " is scrapped and regenerated. If the generated floor layout is invalid 10"
            " times in a row, or a valid spawn configuration isn't generated within 10"
            " attempts, the generation algorithm aborts and the default one-room"
            " Monster House floor is generated as a fallback.\n\nNo params."
        ),
    )

    GetTileTerrain = Symbol(
        [0x5EEDC],
        [0x233BA5C],
        None,
        "Gets the terrain type of a tile.\n\nr0: tile pointer\nreturn: terrain ID",
    )

    DungeonRand100 = Symbol(
        [0x5EEE8],
        [0x233BA68],
        None,
        (
            "Compute a pseudorandom integer on the interval [0, 100) using the dungeon"
            " PRNG.\n\nreturn: pseudorandom integer"
        ),
    )

    ClearHiddenStairs = Symbol(
        [0x5EEF8],
        [0x233BA78],
        None,
        (
            "Clears the tile (terrain and spawns) on which Hidden Stairs are spawned,"
            " if applicable.\n\nNo params."
        ),
    )

    FlagHallwayJunctions = Symbol(
        [0x5EF70],
        [0x233BAF0],
        None,
        (
            "Sets the junction flag (bit 3 of the terrain flags) on any hallway"
            " junction tiles in some range [x0, x1), [y0, y1). This leaves tiles within"
            " rooms untouched.\n\nA hallway tile is considered a junction if it has at"
            " least 3 cardinal neighbors with open terrain.\n\nr0: x0\nr1: y0\nr2:"
            " x1\nr3: y1"
        ),
    )

    GenerateStandardFloor = Symbol(
        [0x5F08C],
        [0x233BC0C],
        None,
        (
            "Generate a standard floor with the given parameters.\n\nBroadly speaking,"
            " a standard floor is generated as follows:\n1. Generating the grid\n2."
            " Creating a room or hallway anchor in each grid cell\n3. Creating hallways"
            " between grid cells\n4. Generating special features (maze room, Kecleon"
            " shop, Monster House, extra hallways, room imperfections, secondary"
            " structures)\n\nr0: grid size x\nr1: grid size y\nr2: floor properties"
        ),
    )

    GenerateOuterRingFloor = Symbol(
        [0x5F1F4],
        [0x233BD74],
        None,
        (
            "Generates a floor layout with a 4x2 grid of rooms, surrounded by an outer"
            " ring of hallways.\n\nr0: floor properties"
        ),
    )

    GenerateCrossroadsFloor = Symbol(
        [0x5F680],
        [0x233C200],
        None,
        (
            "Generates a floor layout with a mesh of hallways on the interior 3x2 grid,"
            " surrounded by a boundary of rooms protruding from the interior like"
            " spikes, excluding the corner cells.\n\nr0: floor properties"
        ),
    )

    GenerateLineFloor = Symbol(
        [0x5FAE0],
        [0x233C660],
        None,
        (
            "Generates a floor layout with 5 grid cells in a horizontal line.\n\nr0:"
            " floor properties"
        ),
    )

    GenerateCrossFloor = Symbol(
        [0x5FC40],
        [0x233C7C0],
        None,
        (
            "Generates a floor layout with 5 rooms arranged in a cross ('plus sign')"
            " formation.\n\nr0: floor properties"
        ),
    )

    GenerateBeetleFloor = Symbol(
        [0x5FDD8],
        [0x233C958],
        None,
        (
            "Generates a floor layout in a 'beetle' formation, which is created by"
            " taking a 3x3 grid of rooms, connecting the rooms within each row, and"
            " merging the central column into one big room.\n\nr0: floor properties"
        ),
    )

    MergeRoomsVertically = Symbol(
        [0x5FF94],
        [0x233CB14],
        None,
        (
            "Merges two vertically stacked rooms into one larger room.\n\nr0: x grid"
            " coordinate of the rooms to merge\nr1: y grid coordinate of the upper"
            " room\nr2: dy, where the lower room has a y grid coordinate of y+dy\nr3:"
            " grid to update"
        ),
    )

    GenerateOuterRoomsFloor = Symbol(
        [0x600E0],
        [0x233CC60],
        None,
        (
            "Generates a floor layout with a ring of rooms on the grid boundary and"
            " nothing in the interior.\n\nNote that this function is bugged, and won't"
            " properly connect all the rooms together for grid_size_x < 4.\n\nr0: grid"
            " size x\nr1: grid size y\nr2: floor properties"
        ),
    )

    IsNotFullFloorFixedRoom = Symbol(
        [0x60374],
        [0x233CEF4],
        None,
        (
            "Checks if a fixed room ID does not correspond to a fixed, full-floor"
            " layout.\n\nThe first non-full-floor fixed room is 0xA5, which is for"
            " Sealed Chambers.\n\nr0: fixed room ID\nreturn: bool"
        ),
    )

    GenerateFixedRoom = Symbol(
        [0x60390],
        [0x233CF10],
        None,
        (
            "Handles fixed room generation if the floor contains a fixed room.\n\nr0:"
            " fixed room ID\nr1: floor properties\nreturn: bool"
        ),
    )

    GenerateOneRoomMonsterHouseFloor = Symbol(
        [0x607D8],
        [0x233D358],
        None,
        (
            "Generates a floor layout with just a large, one-room Monster"
            " House.\n\nThis is the default layout if dungeon generation fails.\n\nNo"
            " params."
        ),
    )

    GenerateTwoRoomsWithMonsterHouseFloor = Symbol(
        [0x608A8],
        [0x233D428],
        None,
        (
            "Generate a floor layout with two rooms (left and right), one of which is a"
            " Monster House.\n\nNo params."
        ),
    )

    GenerateExtraHallways = Symbol(
        [0x60A4C],
        [0x233D5CC],
        None,
        (
            "Generate extra hallways on the floor via a series of random walks.\n\nEach"
            " random walk starts from a random tile in a random room, leaves the room"
            " in a random cardinal direction, and from there tunnels through obstacles"
            " through a series of random turns, leaving open terrain in its wake. The"
            " random walk stops when it reaches open terrain, goes out of bounds, or"
            " reaches an impassable obstruction.\n\nr0: grid to update\nr1: grid size"
            " x\nr2: grid size y\nr3: number of extra hallways to generate"
        ),
    )

    GetGridPositions = Symbol(
        [0x60FE8],
        [0x233DB68],
        None,
        (
            "Get the grid cell positions for a given set of floor grid"
            " dimensions.\n\nr0: [output] pointer to array of the starting x"
            " coordinates of each grid column\nr1: [output] pointer to array of the"
            " starting y coordinates of each grid row\nr2: grid size x\nr3: grid size y"
        ),
    )

    InitDungeonGrid = Symbol(
        [0x61068],
        [0x233DBE8],
        None,
        (
            "Initialize a dungeon grid with defaults.\n\nThe grid is an array of grid"
            " cells stored in column-major order (such that grid cells with the same x"
            " value are stored contiguously), with a fixed column size of 15. If the"
            " grid size in the y direction is less than this, the last (15 -"
            " grid_size_y) entries of each column will be uninitialized.\n\nNote that"
            " the grid size arguments define the maximum size of the grid from a"
            " programmatic standpoint. However, grid cells can be invalidated if they"
            " exceed the configured floor size in the dungeon generation status struct."
            " Thus, the dimensions of the ACTIVE grid can be smaller.\n\nr0: [output]"
            " grid (expected to have space for at least (15*(grid_size_x-1) +"
            " grid_size_y) dungeon grid cells)\nr1: grid size x\nr2: grid size y"
        ),
    )

    AssignRooms = Symbol(
        [0x61168],
        [0x233DCE8],
        None,
        (
            "Randomly selects a subset of grid cells to become rooms.\n\nThe given"
            " number of grid cells will become rooms. If any of the selected grid cells"
            " are invalid, fewer rooms will be generated. The number of rooms assigned"
            " will always be at least 2 and never exceed 36.\n\nCells not marked as"
            " rooms will become hallway anchors. A hallway anchor is a single tile in a"
            " non-room grid cell to which hallways will be connected later, thus"
            " 'anchoring' hallway generation.\n\nr0: grid to update\nr1: grid size"
            " x\nr2: grid size y\nr3: number of rooms; if positive, a random value"
            " between [n_rooms, n_rooms+2] will be used. If negative, |n_rooms| will be"
            " used exactly."
        ),
    )

    CreateRoomsAndAnchors = Symbol(
        [0x6137C],
        [0x233DEFC],
        None,
        (
            "Creates rooms and hallway anchors in each grid cell as designated by"
            " AssignRooms.\n\nThis function creates a rectangle of open terrain for"
            " each room (with some margin relative to the grid cell border). A single"
            " open tile is created in hallway anchor cells, and a hallway anchor"
            " indicator is set for later reference.\n\nr0: grid to update\nr1: grid"
            " size x\nr2: grid size y\nr3: array of the starting x coordinates of each"
            " grid column\nstack[0]: array of the starting y coordinates of each grid"
            " row\nstack[1]: room bitflags; only uses bit 2 (mask: 0b100), which"
            " enables room imperfections"
        ),
    )

    GenerateSecondaryStructures = Symbol(
        [0x616D8],
        [0x233E258],
        None,
        (
            "Try to generate secondary structures in flagged rooms.\n\nIf a valid room"
            " with no special features is flagged to have a secondary structure, try to"
            " generate a random one in the room, based on the result of a dice roll:\n "
            " 0: no secondary structure\n  1: maze, or a central water/lava 'plus sign'"
            " as fallback, or a single water/lava tile in the center as a second"
            " fallback\n  2: checkerboard pattern of water/lava\n  3: central pool of"
            " water/lava\n  4: central 'island' with items and a Warp Tile, surrounded"
            " by a 'moat' of water/lava\n  5: horizontal or vertical divider of"
            " water/lava splitting the room in two\n\nIf the room isn't the right"
            " shape, dimension, or otherwise doesn't support the selected secondary"
            " structure, it is left untouched.\n\nr0: grid to update\nr1: grid size"
            " x\nr2: grid size y"
        ),
    )

    AssignGridCellConnections = Symbol(
        [0x620C0],
        [0x233EC40],
        None,
        (
            "Randomly assigns connections between adjacent grid cells.\n\nConnections"
            " are created via a random walk with momentum, starting from the grid cell"
            " at (cursor x, cursor y). A connection is drawn in a random direction from"
            " the current cursor, and this process is repeated a certain number of"
            " times (the 'floor connectivity' specified in the floor properties). The"
            " direction of the random walk has 'momentum'; there's a 50% chance it will"
            " be the same as the previous step (or rotated counterclockwise if on the"
            " boundary). This helps to reduce the number of dead ends and forks in the"
            " road caused by the random walk 'doubling back' on itself.\n\nIf dead ends"
            " are disabled in the floor properties, there is an additional phase to"
            " remove dead end hallway anchors (only hallway anchors, not rooms) by"
            " drawing additional connections. Note that the actual implementation"
            " contains a bug: the grid cell validity checks use the wrong index, so"
            " connections may be drawn to invalid cells.\n\nr0: grid to update\nr1:"
            " grid size x\nr2: grid size y\nr3: cursor x\nstack[0]: cursor y\nstack[1]:"
            " floor properties"
        ),
    )

    CreateGridCellConnections = Symbol(
        [0x624A0],
        [0x233F020],
        None,
        (
            "Create grid cell connections either by creating hallways or merging"
            " rooms.\n\nWhen creating a hallway connecting a hallway anchor, the exact"
            " anchor coordinates are used as the endpoint. When creating a hallway"
            " connecting a room, a random point on the room edge facing the hallway is"
            " used as the endpoint. The grid cell boundaries are used as the middle"
            " coordinates for kinks (see CreateHallway).\n\nIf room merging is enabled,"
            " there is a 9.75% chance that two connected rooms will be merged into a"
            " single larger room (9.75% comes from two 5% rolls, one for each of the"
            " two rooms being merged). A room can only participate in a merge"
            " once.\n\nr0: grid to update\nr1: grid size x\nr2: grid size y\nr3: array"
            " of the starting x coordinates of each grid column\nstack[0]: array of the"
            " starting y coordinates of each grid row\nstack[1]: disable room merging"
            " flag"
        ),
    )

    GenerateRoomImperfections = Symbol(
        [0x62D98],
        [0x233F918],
        None,
        (
            "Attempt to generate room imperfections for each room in the floor layout,"
            " if enabled.\n\nEach room has a 40% chance of having imperfections if its"
            " grid cell is flagged to allow room imperfections. Imperfections are"
            " generated by randomly growing the walls of the room inwards for a certain"
            " number of iterations, starting from the corners.\n\nr0: grid to"
            " update\nr1: grid size x\nr2: grid size y"
        ),
    )

    CreateHallway = Symbol(
        [0x63184],
        [0x233FD04],
        None,
        (
            "Create a hallway between two points.\n\nIf the two points share no"
            " coordinates in common (meaning the line connecting them is diagonal), a"
            " 'kinked' hallway is created, with the kink at a specified 'middle'"
            " coordinate (in practice the grid cell boundary). For example, with a"
            " kinked horizontal hallway, there are two horizontal lines extending out"
            " from the endpoints, connected by a vertical line on the middle x"
            " coordinate.\n\nIf a hallway would intersect with an existing open tile"
            " (like an existing hallway), the hallway will only be created up to the"
            " point where it intersects with the open tile.\n\nr0: x0\nr1: y0\nr2:"
            " x1\nr3: y1\nstack[0]: vertical flag (true for vertical hallway, false for"
            " horizontal)\nstack[1]: middle x coordinate for kinked horizontal"
            " hallways\nstack[2]: middle y coordinate for kinked vertical hallways"
        ),
    )

    EnsureConnectedGrid = Symbol(
        [0x63488],
        [0x2340008],
        None,
        (
            "Ensure the grid forms a connected graph (all valid cells are reachable) by"
            " adding hallways to unreachable grid cells.\n\nIf a grid cell cannot be"
            " connected for some reason, remove it entirely.\n\nr0: grid to update\nr1:"
            " grid size x\nr2: grid size y\nr3: array of the starting x coordinates of"
            " each grid column\nstack[0]: array of the starting y coordinates of each"
            " grid row"
        ),
    )

    SetTerrainObstacleChecked = Symbol(
        [0x63964],
        [0x23404E4],
        None,
        (
            "Set the terrain of a specific tile to be an obstacle (wall or secondary"
            " terrain).\n\nSecondary terrain (water/lava) can only be placed in the"
            " specified room. If the tile room index does not match, a wall will be"
            " placed instead.\n\nr0: tile pointer\nr1: use secondary terrain flag (true"
            " for water/lava, false for wall)\nr2: room index"
        ),
    )

    FinalizeJunctions = Symbol(
        [0x639A0],
        [0x2340520],
        None,
        (
            "Finalizes junction tiles by setting the junction flag (bit 3 of the"
            " terrain flags) and ensuring open terrain.\n\nNote that this"
            " implementation is slightly buggy. This function scans tiles"
            " left-to-right, top-to-bottom, and identifies junctions as any open,"
            " non-hallway tile (room_index != 0xFF) adjacent to an open, hallway tile"
            " (room_index == 0xFF). This interacts poorly with hallway anchors"
            " (room_index == 0xFE). This function sets the room index of any hallway"
            " anchors to 0xFF within the same loop, so a hallway anchor may or may not"
            " be identified as a junction depending on the orientation of connected"
            " hallways.\n\nFor example, in the following configuration, the 'o' tile"
            " would be marked as a junction because the neighboring hallway tile to its"
            " left comes earlier in iteration, while the 'o' tile still has the room"
            " index 0xFE, causing the algorithm to mistake it for a room tile:\n "
            " xxxxx\n  ---ox\n  xxx|x\n  xxx|x\nHowever, in the following"
            " configuration, the 'o' tile would NOT be marked as a junction because it"
            " comes earlier in iteration than any of its neighboring hallway tiles, so"
            " its room index is set to 0xFF before it can be marked as a junction. This"
            " is actually the ONLY possible configuration where a hallway anchor will"
            " not be marked as a junction.\n  xxxxx\n  xo---\n  x|xxx\n  x|xxx\n\nNo"
            " params."
        ),
    )

    GenerateKecleonShop = Symbol(
        [0x63C4C],
        [0x23407CC],
        None,
        (
            "Possibly generate a Kecleon shop on the floor.\n\nA Kecleon shop will be"
            " generated with a probability determined by the Kecleon shop spawn chance"
            " parameter. A Kecleon shop will be generated in a random room that is"
            " valid, connected, has no other special features, and has dimensions of at"
            " least 5x4. Kecleon shops will occupy the entire room interior, leaving a"
            " one tile margin from the room walls.\n\nr0: grid to update\nr1: grid size"
            " x\nr2: grid size y\nr3: Kecleon shop spawn chance (percentage from 0-100)"
        ),
    )

    GenerateMonsterHouse = Symbol(
        [0x64000],
        [0x2340B80],
        None,
        (
            "Possibly generate a Monster House on the floor.\n\nA Monster House will be"
            " generated with a probability determined by the Monster House spawn chance"
            " parameter, and only if the current floor can support one (no"
            " non-Monster-House outlaw missions or special floor types). A Monster"
            " House will be generated in a random room that is valid, connected, and is"
            " not a merged or maze room.\n\nr0: grid to update\nr1: grid size x\nr2:"
            " grid size y\nr3: Monster House spawn chance (percentage from 0-100)"
        ),
    )

    GenerateMazeRoom = Symbol(
        [0x64288],
        [0x2340E08],
        None,
        (
            "Possibly generate a maze room on the floor.\n\nA maze room will be"
            " generated with a probability determined by the maze room chance"
            " parameter. A maze will be generated in a random room that is valid,"
            " connected, has odd dimensions, and has no other features.\n\nr0: grid to"
            " update\nr1: grid size x\nr2: grid size y\nr3: maze room chance"
            " (percentage from 0-100)"
        ),
    )

    GenerateMaze = Symbol(
        [0x644BC],
        [0x234103C],
        None,
        (
            "Generate a maze room within a given grid cell.\n\nA 'maze' is generated"
            " within the room using a series of random walks to place obstacle terrain"
            " (walls or secondary terrain) in a maze-like arrangement. 'Maze lines'"
            " (see GenerateMazeLine) are generated using every other tile around the"
            " room's border, as well as every other interior tile, as a starting point."
            " This ensures that there are stripes of walkable open terrain surrounded"
            " by stripes of obstacles (the maze walls).\n\nr0: grid cell pointer\nr1:"
            " use secondary terrain flag (true for water/lava, false for walls)"
        ),
    )

    GenerateMazeLine = Symbol(
        [0x64738],
        [0x23412B8],
        None,
        (
            "Generate a 'maze line' from a given starting point, within the given"
            " bounds.\n\nA 'maze line' is a random walk starting from (x0, y0). The"
            " random walk proceeds with a stride of 2 in a random direction, laying"
            " down obstacles as it goes. The random walk terminates when it gets"
            " trapped and there are no more neighboring tiles that are open and"
            " in-bounds.\n\nr0: x0\nr1: y0\nr2: xmin\nr3: ymin\nstack[0]:"
            " xmax\nstack[1]: ymax\nstack[2]: use secondary terrain flag (true for"
            " water/lava, false for walls)\nstack[3]: room index"
        ),
    )

    SetSpawnFlag5 = Symbol(
        [0x648E0],
        [0x2341460],
        None,
        "Set spawn flag 5 (0b100000 or 0x20) on all tiles in a room.\n\nr0: grid cell",
    )

    IsNextToHallway = Symbol(
        [0x64934],
        [0x23414B4],
        None,
        (
            "Checks if a tile position is either in a hallway or next to one.\n\nr0:"
            " x\nr1: y\nreturn: bool"
        ),
    )

    ResolveInvalidSpawns = Symbol(
        [0x649D8],
        [0x2341558],
        None,
        (
            "Resolve invalid spawn flags on tiles.\n\nSpawn flags can be invalid due to"
            " terrain. For example, traps can't spawn on obstacles. Spawn flags can"
            " also be invalid due to multiple being set on a single tile, in which case"
            " one will take precedence. For example, stair spawns trump trap"
            " spawns.\n\nNo params."
        ),
    )

    ConvertSecondaryTerrainToChasms = Symbol(
        [0x64A70],
        [0x23415F0],
        None,
        "Converts all secondary terrain tiles (water/lava) to chasms.\n\nNo params.",
    )

    EnsureImpassableTilesAreWalls = Symbol(
        [0x64ADC],
        [0x234165C],
        None,
        "Ensures all tiles with the impassable flag are walls.\n\nNo params.",
    )

    InitializeTile = Symbol(
        [0x64B38], [0x23416B8], None, "Initialize a tile struct.\n\nr0: tile pointer"
    )

    ResetFloor = Symbol(
        [0x64B70],
        [0x23416F0],
        None,
        (
            "Resets the floor in preparation for a floor generation attempt.\n\nResets"
            " all tiles, resets the border to be impassable, and clears entity"
            " spawns.\n\nNo params."
        ),
    )

    PosIsOutOfBounds = Symbol(
        [0x64D10],
        [0x2341890],
        None,
        (
            "Checks if a position (x, y) is out of bounds on the map: !((0 <= x <= 55)"
            " && (0 <= y <= 31)).\n\nr0: x\nr1: y\nreturn: bool"
        ),
    )

    ShuffleSpawnPositions = Symbol(
        [0x64D48],
        [0x23418C8],
        None,
        (
            "Randomly shuffle an array of spawn positions.\n\nr0: spawn position array"
            " containing bytes {x1, y1, x2, y2, ...}\nr1: number of (x, y) pairs in the"
            " spawn position array"
        ),
    )

    SpawnNonEnemies = Symbol(
        [0x64DB0],
        [0x2341930],
        None,
        (
            "Spawn all non-enemy entities, which includes stairs, items, traps, and the"
            " player.\n\nMost entities are spawned randomly on a subset of permissible"
            " tiles.\n\nStairs are spawned if they don't already exist on the floor,"
            " and hidden stairs of the specified type are also spawned if configured as"
            " long as there are at least 2 floors left in the dungeon. Stairs can spawn"
            " on any tile that has open terrain, is in a room, isn't in a Kecleon shop,"
            " doesn't already have an enemy spawn, isn't a hallway junction, and isn't"
            " a special tile like a Key door.\n\nItems are spawned both normally in"
            " rooms, as well as in walls and Monster Houses. Normal items can spawn on"
            " any tile that has open terrain, is in a room, isn't in a Kecleon shop or"
            " Monster House, isn't a hallway junction, and isn't a special tile like a"
            " Key door. Buried items can spawn on any wall tile. Monster House items"
            " can spawn on any Monster House tile that isn't in a Kecleon shop and"
            " isn't a hallway junction.\n\nTraps are similarly spawned both normally in"
            " rooms, as well as in Monster Houses. Normal traps can spawn on any tile"
            " that has open terrain, is in a room, isn't in a Kecleon shop, doesn't"
            " already have an item or enemy spawn, and isn't a special tile like a Key"
            " door. Monster House traps follow the same conditions as Monster House"
            " items.\n\nThe player can spawn on any tile that has open terrain, is in a"
            " room, isn't in a Kecleon shop, isn't a hallway junction, doesn't already"
            " have an item, enemy, or trap spawn, and isn't a special tile like a Key"
            " door.\n\nr0: floor properties\nr1: empty Monster House flag. An empty"
            " Monster House is one with no items or traps, and only a small number of"
            " enemies."
        ),
    )

    SpawnEnemies = Symbol(
        [0x654D4],
        [0x2342054],
        None,
        (
            "Spawn all enemies, which includes normal enemies and those in Monster"
            " Houses.\n\nNormal enemies can spawn on any tile that has open terrain,"
            " isn't in a Kecleon shop, doesn't already have another entity spawn, and"
            " isn't a special tile like a Key door.\n\nMonster House enemies can spawn"
            " on any Monster House tile that isn't in a Kecleon shop, isn't where the"
            " player spawns, and isn't a special tile like a Key door.\n\nr0: floor"
            " properties\nr1: empty Monster House flag. An empty Monster House is one"
            " with no items or traps, and only a small number of enemies."
        ),
    )

    SetSecondaryTerrainOnWall = Symbol(
        [0x657D0],
        [0x2342350],
        None,
        (
            "Set a specific tile to have secondary terrain (water/lava), but only if"
            " it's a passable wall.\n\nr0: tile pointer"
        ),
    )

    GenerateSecondaryTerrainFormations = Symbol(
        [0x65810],
        [0x2342390],
        None,
        (
            "Generate secondary terrain (water/lava) formations.\n\nThis includes"
            " 'rivers' that flow from top-to-bottom (or bottom-to-top), as well as"
            " 'lakes' both standalone and after rivers. Water/lava formations will"
            " never cut through rooms, but they can pass through rooms to the opposite"
            " side.\n\nRivers are generated by a top-down or bottom-up random walk that"
            " ends when existing secondary terrain is reached or the walk goes out of"
            " bounds. Some rivers also end prematurely in a lake. Lakes are a large"
            " collection of secondary terrain generated around a central point.\n\nr0:"
            " bit index to test in the floor properties room flag bitvector (formations"
            " are only generated if the bit is set)\nr1: floor properties"
        ),
    )

    StairsAlwaysReachable = Symbol(
        [0x65ED0],
        [0x2342A50],
        None,
        (
            "Checks that the stairs are reachable from every walkable tile on the"
            " floor.\n\nThis runs a graph traversal algorithm that is very similar to"
            " breadth-first search (the order in which nodes are visited is slightly"
            " different), starting from the stairs. If any tile is walkable but wasn't"
            " reached by the traversal algorithm, then the stairs must not be reachable"
            " from that tile.\n\nr0: x coordinate of the stairs\nr1: y coordinate of"
            " the stairs\nr2: flag to always return true, but set a special bit on all"
            " walkable tiles that aren't reachable from the stairs\nreturn: bool"
        ),
    )

    ConvertWallsToChasms = Symbol(
        [0x665AC], [0x234312C], None, "Converts all wall tiles to chasms.\n\nNo params."
    )

    ResetInnerBoundaryTileRows = Symbol(
        [0x66BE0],
        [0x2343760],
        None,
        (
            "Reset the inner boundary tile rows (y == 1 and y == 30) to their initial"
            " state of all wall tiles, with impassable walls at the edges (x == 0 and x"
            " == 55).\n\nNo params."
        ),
    )

    ResetImportantSpawnPositions = Symbol(
        [0x66CCC],
        [0x234384C],
        None,
        (
            "Resets important spawn positions (the player, stairs, and hidden stairs)"
            " back to their default values.\n\nr0: dungeon generation info pointer (a"
            " field on the dungeon struct)"
        ),
    )

    SpawnStairs = Symbol(
        [0x66CF0],
        [0x2343870],
        None,
        (
            "Spawn stairs at the given location.\n\nIf the hidden stairs type is"
            " something other than HIDDEN_STAIRS_NONE, hidden stairs of the specified"
            " type will be spawned instead of normal stairs.\n\nIf spawning normal"
            " stairs and the current floor is a rescue floor, the room containing the"
            " stairs will be converted into a Monster House.\n\nIf attempting to spawn"
            " hidden stairs but the spawn is blocked, the floor generation status's"
            " hidden stairs spawn position will be updated, but it won't be transferred"
            " to the dungeon generation info struct.\n\nr0: position (two-byte array"
            " for {x, y})\nr1: dungeon generation info pointer (a field on the dungeon"
            " struct)\nr2: hidden stairs type"
        ),
    )

    GetHiddenStairsType = Symbol(
        [0x66E00],
        [0x2343980],
        None,
        (
            "Gets the hidden stairs type for a given floor.\n\nThis function reads the"
            " floor properties and resolves any randomness (such as"
            " HIDDEN_STAIRS_RANDOM_SECRET_BAZAAR_OR_SECRET_ROOM and the"
            " floor_properties::hidden_stairs_spawn_chance) into a concrete hidden"
            " stairs type.\n\nr0: dungeon generation info pointer\nr1: floor properties"
            " pointer\nreturn: enum hidden_stairs_type"
        ),
    )

    ResetHiddenStairsSpawn = Symbol(
        [0x66F6C],
        [0x2343AEC],
        None,
        (
            "Resets hidden stairs spawn information for the floor. This includes the"
            " position on the floor generation status as well as the flag indicating"
            " whether the spawn was blocked.\n\nNo params."
        ),
    )

    LoadFixedRoomData = Symbol(
        [0x67DF4],
        [0x2344974],
        None,
        (
            "Loads fixed room data from BALANCE/fixed.bin into the buffer pointed to by"
            " FIXED_ROOM_DATA_PTR.\n\nNo params."
        ),
    )

    LoadFixedRoom = Symbol(
        [0x67E84], [0x2344A04], None, "Note: unverified, ported from Irdkwia's notes"
    )

    OpenFixedBin = Symbol(
        [0x680B8],
        [0x2344C38],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    CloseFixedBin = Symbol(
        [0x680EC],
        [0x2344C6C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    AreOrbsAllowed = Symbol(
        [0x68110],
        [0x2344C90],
        None,
        (
            "Checks if orbs are usable in the given fixed room.\n\nAlways true if not a"
            " full-floor fixed room.\n\nr0: fixed room ID\nreturn: bool"
        ),
    )

    AreTileJumpsAllowed = Symbol(
        [0x68140],
        [0x2344CC0],
        None,
        (
            "Checks if tile jumps (warping, being blown away, and leaping) are allowed"
            " in the given fixed room.\n\nAlways true if not a full-floor fixed"
            " room.\n\nr0: fixed room ID\nreturn: bool"
        ),
    )

    AreTrawlOrbsAllowed = Symbol(
        [0x68170],
        [0x2344CF0],
        None,
        (
            "Checks if Trawl Orbs work in the given fixed room.\n\nAlways true if not a"
            " full-floor fixed room.\n\nr0: fixed room ID\nreturn: bool"
        ),
    )

    AreOrbsAllowedVeneer = Symbol(
        [0x681A0],
        [0x2344D20],
        None,
        (
            "Likely a linker-generated veneer for InitMemAllocTable.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " fixed room ID\nreturn: bool"
        ),
    )

    AreLateGameTrapsEnabled = Symbol(
        [0x681AC],
        [0x2344D2C],
        None,
        (
            "Check if late-game traps (Summon, Pitfall, and Pokémon traps) work in the"
            " given fixed room.\n\nOr disabled? This function, which Irdkwia's notes"
            " label as a disable check, check the struct field labeled in End's notes"
            " as an enable flag.\n\nr0: fixed room ID\nreturn: bool"
        ),
    )

    AreMovesEnabled = Symbol(
        [0x681C4],
        [0x2344D44],
        None,
        (
            "Checks if moves (excluding the regular attack) are usable in the given"
            " fixed room.\n\nr0: fixed room ID\nreturn: bool"
        ),
    )

    IsRoomIlluminated = Symbol(
        [0x681DC],
        [0x2344D5C],
        None,
        (
            "Checks if the given fixed room is fully illuminated.\n\nr0: fixed room"
            " ID\nreturn: bool"
        ),
    )

    GetMatchingMonsterId = Symbol(
        [0x681F4],
        [0x2344D74],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nr1:"
            " ?\nr2: ?\nreturn: monster ID"
        ),
    )

    GenerateItemExplicit = Symbol(
        [0x68418],
        [0x2344F98],
        None,
        (
            "Initializes an item struct with the given information.\n\nThis calls"
            " InitStandardItem, then explicitly sets the quantity and stickiness. If"
            " quantity == 0 for Poké, GenerateCleanItem is used instead.\n\nr0: pointer"
            " to item to initialize\nr1: item ID\nr2: quantity\nr3: sticky flag"
        ),
    )

    GenerateAndSpawnItem = Symbol(
        [0x68494],
        [0x2345014],
        None,
        (
            "A convenience function that generates an item with GenerateItemExplicit,"
            " then spawns it with SpawnItem.\n\nIf the check-in-bag flag is set and the"
            " player's bag already contains an item with the given ID, a Reviver Seed"
            " will be spawned instead.\n\nIt seems like this function is only ever"
            " called in one place, with an item ID of 0x49 (Reviver Seed).\n\nr0: item"
            " ID\nr1: x position\nr2: y position\nr3: quantity\nstack[0]: sticky"
            " flag\nstack[1]: check-in-bag flag"
        ),
    )

    IsHiddenStairsFloor = Symbol(
        [0x68570],
        [0x23450F0],
        None,
        (
            "Checks if the current floor is either the Secret Bazaar or a Secret"
            " Room.\n\nreturn: bool"
        ),
    )

    GenerateStandardItem = Symbol(
        [0x68C34],
        [0x23457B4],
        None,
        (
            "Wrapper around GenerateItem with quantity set to 0\n\nr0: pointer to item"
            " to initialize\nr1: item ID\nr2: stickiness type"
        ),
    )

    GenerateCleanItem = Symbol(
        [0x68C48],
        [0x23457C8],
        None,
        (
            "Wrapper around GenerateItem with quantity set to 0 and stickiness type set"
            " to SPAWN_STICKY_NEVER.\n\nr0: pointer to item to initialize\nr1: item ID"
        ),
    )

    SpawnItem = Symbol(
        [0x695A0],
        [0x2346120],
        None,
        (
            "Spawns an item on the floor. Fails if there are more than 64 items already"
            " on the floor.\n\nThis calls SpawnItemEntity, fills in the item info"
            " struct, sets the entity to be visible, binds the entity to the tile it"
            " occupies, updates the n_items counter on the dungeon struct, and various"
            " other bits of bookkeeping.\n\nr0: position\nr1: item pointer\nr2: some"
            " flag?\nreturn: success flag"
        ),
    )

    SpawnEnemyItemDropWrapper = Symbol(
        [0x69AA8],
        [0x2346628],
        None,
        (
            "Wraps SpawnEnemyItemDrop in a more convenient interface.\n\nr0:"
            " entity\nr1: position\nr2: item\nr3: ?"
        ),
    )

    SpawnEnemyItemDrop = Symbol(
        [0x69B44],
        [0x23466C4],
        None,
        (
            "Appears to spawn an enemy item drop at a specified location, with a log"
            " message.\n\nr0: entity\nr1: item entity\nr2: item info\nr3: ?\nstack[0]:"
            " pointer to int16_t[2] for x/y direction (corresponding to"
            " DIRECTIONS_XY)\nstack[1]: ?"
        ),
    )

    TryGenerateUnownStoneDrop = Symbol(
        [0x6A0CC],
        [0x2346C4C],
        None,
        (
            "Determine if a defeated monster should drop a Unown Stone, and generate"
            " the item if so.\n\nChecks that the current dungeon isn't a Marowak Dojo"
            " training maze, and that the monster is an Unown. If so, there's a 21%"
            " chance that an Unown Stone will be generated.\n\nr0: [output] item\nr1:"
            " monster ID\nreturn: whether or not an Unown Stone was generated"
        ),
    )

    HasHeldItem = Symbol(
        [0x6A850],
        [0x23473D0],
        None,
        (
            "Checks if a monster has a certain held item.\n\nr0: entity pointer\nr1:"
            " item ID\nreturn: bool"
        ),
    )

    GenerateMoneyQuantity = Symbol(
        [0x6A8A0],
        [0x2347420],
        None,
        (
            "Set the quantity code on an item (assuming it's Poké), given some maximum"
            " acceptable money amount.\n\nr0: item pointer\nr1: max money amount"
            " (inclusive)"
        ),
    )

    CheckTeamItemsFlags = Symbol(
        [0x6AC4C],
        [0x23477CC],
        None,
        (
            "Checks whether any of the items in the bag or any of the items carried by"
            " team members has any of the specified flags set in its flags"
            " field.\n\nr0: Flag(s) to check (0 = f_exists, 1 = f_in_shop, 2 ="
            " f_unpaid, etc.)\nreturn: True if any of the items of the team has the"
            " specified flags set, false otherwise."
        ),
    )

    GenerateItem = Symbol(
        [0x6B344],
        [0x2347EC4],
        None,
        (
            "Initializes an item struct with the given information.\n\nThis wraps"
            " InitItem, but with extra logic to resolve the item's stickiness. It also"
            " calls GenerateMoneyQuantity for Poké.\n\nr0: pointer to item to"
            " initialize\nr1: item ID\nr2: quantity\nr3: stickiness type (enum"
            " gen_item_stickiness)"
        ),
    )

    CheckActiveChallengeRequest = Symbol(
        [0x6D1CC],
        [0x2349D4C],
        None,
        (
            "Checks if there's an active challenge request on the current"
            " dungeon.\n\nreturn: True if there's an active challenge request on the"
            " current dungeon in the list of missions."
        ),
    )

    IsOutlawOrChallengeRequestFloor = Symbol(
        [0x6D244],
        [0x2349DC4],
        None,
        (
            "Checks if the current floor is an active mission destination of type"
            " MISSION_TAKE_ITEM_FROM_OUTLAW, MISSION_ARREST_OUTLAW or"
            " MISSION_CHALLENGE_REQUEST.\n\nreturn: bool"
        ),
    )

    IsDestinationFloor = Symbol(
        [0x6D288],
        [0x2349E08],
        None,
        "Checks if the current floor is a mission destination floor.\n\nreturn: bool",
    )

    IsCurrentMissionType = Symbol(
        [0x6D29C],
        [0x2349E1C],
        None,
        (
            "Checks if the current floor is an active mission destination of a given"
            " type (and any subtype).\n\nr0: mission type\nreturn: bool"
        ),
    )

    IsCurrentMissionTypeExact = Symbol(
        [0x6D2D0],
        [0x2349E50],
        None,
        (
            "Checks if the current floor is an active mission destination of a given"
            " type and subtype.\n\nr0: mission type\nr1: mission subtype\nreturn: bool"
        ),
    )

    IsOutlawMonsterHouseFloor = Symbol(
        [0x6D30C],
        [0x2349E8C],
        None,
        (
            "Checks if the current floor is a mission destination for a Monster House"
            " outlaw mission.\n\nreturn: bool"
        ),
    )

    IsGoldenChamber = Symbol(
        [0x6D330],
        [0x2349EB0],
        None,
        "Checks if the current floor is a Golden Chamber floor.\n\nreturn: bool",
    )

    IsLegendaryChallengeFloor = Symbol(
        [0x6D354],
        [0x2349ED4],
        None,
        (
            "Checks if the current floor is a boss floor for a Legendary Challenge"
            " Letter mission.\n\nreturn: bool"
        ),
    )

    IsJirachiChallengeFloor = Symbol(
        [0x6D394],
        [0x2349F14],
        None,
        (
            "Checks if the current floor is the boss floor in Star Cave Pit for"
            " Jirachi's Challenge Letter mission.\n\nreturn: bool"
        ),
    )

    IsDestinationFloorWithMonster = Symbol(
        [0x6D3CC],
        [0x2349F4C],
        None,
        (
            "Checks if the current floor is a mission destination floor with a special"
            " monster.\n\nSee FloorHasMissionMonster for details.\n\nreturn: bool"
        ),
    )

    LoadMissionMonsterSprites = Symbol(
        [0x6D478],
        [0x2349FF8],
        None,
        (
            "Loads the sprites of monsters that appear on the current floor because of"
            " a mission, if applicable.\n\nThis includes monsters to be rescued,"
            " outlaws and its minions.\n\nNo params."
        ),
    )

    MissionTargetEnemyIsDefeated = Symbol(
        [0x6D4F0],
        [0x234A070],
        None,
        (
            "Checks if the target enemy of the mission on the current floor has been"
            " defeated.\n\nreturn: bool"
        ),
    )

    SetMissionTargetEnemyDefeated = Symbol(
        [0x6D510],
        [0x234A090],
        None,
        (
            "Set the flag for whether or not the target enemy of the current mission"
            " has been defeated.\n\nr0: new flag value"
        ),
    )

    IsDestinationFloorWithFixedRoom = Symbol(
        [0x6D524],
        [0x234A0A4],
        None,
        (
            "Checks if the current floor is a mission destination floor with a fixed"
            " room.\n\nThe entire floor can be a fixed room layout, or it can just"
            " contain a Sealed Chamber.\n\nreturn: bool"
        ),
    )

    GetItemToRetrieve = Symbol(
        [0x6D54C],
        [0x234A0CC],
        None,
        (
            "Get the ID of the item that needs to be retrieve on the current floor for"
            " a mission, if one exists.\n\nreturn: item ID"
        ),
    )

    GetItemToDeliver = Symbol(
        [0x6D570],
        [0x234A0F0],
        None,
        (
            "Get the ID of the item that needs to be delivered to a mission client on"
            " the current floor, if one exists.\n\nreturn: item ID"
        ),
    )

    GetSpecialTargetItem = Symbol(
        [0x6D59C],
        [0x234A11C],
        None,
        (
            "Get the ID of the special target item for a Sealed Chamber or Treasure"
            " Memo mission on the current floor.\n\nreturn: item ID"
        ),
    )

    IsDestinationFloorWithItem = Symbol(
        [0x6D5E4],
        [0x234A164],
        None,
        (
            "Checks if the current floor is a mission destination floor with a special"
            " item.\n\nThis excludes missions involving taking an item from an"
            " outlaw.\n\nreturn: bool"
        ),
    )

    IsDestinationFloorWithHiddenOutlaw = Symbol(
        [0x6D644],
        [0x234A1C4],
        None,
        (
            "Checks if the current floor is a mission destination floor with a 'hidden"
            " outlaw' that behaves like a normal enemy.\n\nreturn: bool"
        ),
    )

    IsDestinationFloorWithFleeingOutlaw = Symbol(
        [0x6D668],
        [0x234A1E8],
        None,
        (
            "Checks if the current floor is a mission destination floor with a 'fleeing"
            " outlaw' that runs away.\n\nreturn: bool"
        ),
    )

    GetMissionTargetEnemy = Symbol(
        [0x6D6A0],
        [0x234A220],
        None,
        (
            "Get the monster ID of the target enemy to be defeated on the current floor"
            " for a mission, if one exists.\n\nreturn: monster ID"
        ),
    )

    GetMissionEnemyMinionGroup = Symbol(
        [0x6D6B8],
        [0x234A238],
        None,
        (
            "Get the monster ID of the specified minion group on the current floor for"
            " a mission, if it exists.\n\nNote that a single minion group can"
            " correspond to multiple actual minions of the same species. There can be"
            " up to 2 minion groups.\n\nr0: minion group index (0-indexed)\nreturn:"
            " monster ID"
        ),
    )

    SetTargetMonsterNotFoundFlag = Symbol(
        [0x6D744],
        [0x234A2C4],
        None,
        (
            "Sets dungeon::target_monster_not_found_flag to the specified value.\n\nr0:"
            " Value to set the flag to"
        ),
    )

    GetTargetMonsterNotFoundFlag = Symbol(
        [0x6D758],
        [0x234A2D8],
        None,
        (
            "Gets the value of dungeon::target_monster_not_found_flag.\n\nreturn:"
            " dungeon::target_monster_not_found_flag"
        ),
    )

    FloorHasMissionMonster = Symbol(
        [0x6D7C8],
        [0x234A348],
        None,
        (
            "Checks if a given floor is a mission destination with a special monster,"
            " either a target to rescue or an enemy to defeat.\n\nMission types with a"
            " monster on the destination floor:\n- Rescue client\n- Rescue target\n-"
            " Escort to target\n- Deliver item\n- Search for target\n- Take item from"
            " outlaw\n- Arrest outlaw\n- Challenge Request\n\nr0: mission destination"
            " info pointer\nreturn: bool"
        ),
    )

    GenerateMissionEggMonster = Symbol(
        [0x6D920],
        [0x234A4A0],
        None,
        (
            "Generates the monster ID in the egg from the given mission. Uses the base"
            " form of the monster.\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: mission struct"
        ),
    )

    LogMessageByIdWithPopupCheckUser = Symbol(
        [0x6F324],
        [0x234BEA4],
        None,
        (
            "Logs a message in the message log alongside a message popup, if the user"
            " hasn't fainted.\n\nr0: user entity pointer\nr1: message ID"
        ),
    )

    LogMessageWithPopupCheckUser = Symbol(
        [0x6F364],
        [0x234BEE4],
        None,
        (
            "Logs a message in the message log alongside a message popup, if the user"
            " hasn't fainted.\n\nr0: user entity pointer\nr1: message string"
        ),
    )

    LogMessageByIdQuiet = Symbol(
        [0x6F39C],
        [0x234BF1C],
        None,
        (
            "Logs a message in the message log (but without a message popup).\n\nr0:"
            " user entity pointer\nr1: message ID"
        ),
    )

    LogMessageQuiet = Symbol(
        [0x6F3C0],
        [0x234BF40],
        None,
        (
            "Logs a message in the message log (but without a message popup).\n\nr0:"
            " user entity pointer\nr1: message string"
        ),
    )

    LogMessageByIdWithPopupCheckUserTarget = Symbol(
        [0x6F3D0],
        [0x234BF50],
        None,
        (
            "Logs a message in the message log alongside a message popup, if some user"
            " check passes and the target hasn't fainted.\n\nr0: user entity"
            " pointer\nr1: target entity pointer\nr2: message ID"
        ),
    )

    LogMessageWithPopupCheckUserTarget = Symbol(
        [0x6F424],
        [0x234BFA4],
        None,
        (
            "Logs a message in the message log alongside a message popup, if some user"
            " check passes and the target hasn't fainted.\n\nr0: user entity"
            " pointer\nr1: target entity pointer\nr2: message string"
        ),
    )

    LogMessageByIdQuietCheckUserTarget = Symbol(
        [0x6F470],
        [0x234BFF0],
        None,
        (
            "Logs a message in the message log (but without a message popup), if some"
            " user check passes and the target hasn't fainted.\n\nr0: user entity"
            " pointer\nr1: target entity pointer\nr2: message ID"
        ),
    )

    LogMessageByIdWithPopupCheckUserUnknown = Symbol(
        [0x6F4C4],
        [0x234C044],
        None,
        (
            "Logs a message in the message log alongside a message popup, if the user"
            " hasn't fainted and some other unknown check.\n\nr0: user entity"
            " pointer\nr1: ?\nr2: message ID"
        ),
    )

    LogMessageByIdWithPopup = Symbol(
        [0x6F518],
        [0x234C098],
        None,
        (
            "Logs a message in the message log alongside a message popup.\n\nr0: user"
            " entity pointer\nr1: message ID"
        ),
    )

    LogMessageWithPopup = Symbol(
        [0x6F53C],
        [0x234C0BC],
        None,
        (
            "Logs a message in the message log alongside a message popup.\n\nr0: user"
            " entity pointer\nr1: message string"
        ),
    )

    LogMessage = Symbol(
        [0x6F588],
        [0x234C108],
        None,
        (
            "Logs a message in the message log.\n\nr0: user entity pointer\nr1: message"
            " string\nr2: bool, whether or not to present a message popup"
        ),
    )

    LogMessageById = Symbol(
        [0x6F794],
        [0x234C314],
        None,
        (
            "Logs a message in the message log.\n\nr0: user entity pointer\nr1: message"
            " ID\nr2: bool, whether or not to present a message popup"
        ),
    )

    OpenMessageLog = Symbol(
        [0x6FBDC], [0x234C75C], None, "Opens the message log window.\n\nr0: ?\nr1: ?"
    )

    RunDungeonMode = Symbol(
        [0x6FFA8],
        [0x234CB28],
        None,
        (
            "This appears to be the top-level function for running dungeon mode.\n\nIt"
            " gets called by some code in overlay 10 right after doing the dungeon fade"
            " transition, and once it exits, the dungeon results are processed.\n\nThis"
            " function is presumably in charge of allocating the dungeon struct,"
            " setting it up, launching the dungeon engine, etc."
        ),
    )

    DisplayDungeonTip = Symbol(
        [0x70F70],
        [0x234DAF0],
        None,
        (
            "Checks if a given dungeon tip should be displayed at the start of a floor"
            " and if so, displays it. Called up to 4 times at the start of each new"
            " floor, with a different r0 parameter each time.\n\nr0: Pointer to the"
            " message_tip struct of the message that should be displayed\nr1: True to"
            " log the message in the message log"
        ),
    )

    SetBothScreensWindowColorToDefault = Symbol(
        [0x70FE0],
        [0x234DB60],
        None,
        (
            "This changes the palettes of windows in both screens to an appropiate"
            " value depending on the playthrough\nIf you're in a special episode, they"
            " turn green , otherwise, they turn blue or pink depending on your"
            " character's sex\n\nNo params"
        ),
    )

    GetPersonalityIndex = Symbol(
        [0x7106C],
        [0x234DBEC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: monster"
            " pointer\nreturn: ?"
        ),
    )

    DisplayMessage = Symbol(
        [0x712D8],
        [0x234DE58],
        None,
        (
            "Displays a message in a dialogue box that optionally waits for player"
            " input before closing.\n\nr0: ?\nr1: ID of the string to display\nr2: True"
            " to wait for player input before closing the dialogue box, false to close"
            " it automatically once all the characters get printed."
        ),
    )

    DisplayMessage2 = Symbol(
        [0x7132C], [0x234DEAC], None, "Very similar to DisplayMessage"
    )

    YesNoMenu = Symbol(
        [0x71598],
        [0x234E118],
        None,
        (
            "Opens a menu where the user can choose 'Yes' or 'No' and waits for input"
            " before returning.\n\nr0: ?\nr1: ID of the string to display in the"
            " textbox\nr2: Option that the cursor will be on by default. 0 for 'Yes', 1"
            " for 'No'\nr3: ?\nreturn: True if the user chooses 'Yes', false if the"
            " user chooses 'No'"
        ),
    )

    DisplayMessageInternal = Symbol(
        [0x71610],
        [0x234E190],
        None,
        (
            "Called by DisplayMessage. Seems to be the function that handles the"
            " display of the dialogue box. It won't return until all the characters"
            " have been written and after the player manually closes the dialogue box"
            " (if the corresponding parameter was set).\n\nr0: ID of the string to"
            " display\nr1: True to wait for player input before closing the dialogue"
            " box, false to close it automatically once all the characters get"
            " printed.\nr2: ? (r0 in DisplayMessage)\nr3: ?\nstack[0]: ?\nstack[1]: ?"
        ),
    )

    OpenMenu = Symbol(
        [0x71E74], [0x234E9F4], None, "Note: unverified, ported from Irdkwia's notes"
    )

    OthersMenuLoop = Symbol(
        [0x7384C],
        [0x23503CC],
        None,
        (
            "Called on each frame while the in-dungeon 'others' menu is open.\n\nIt"
            " contains a switch to determine whether an option has been chosen or not"
            " and a second switch that determines what to do depending on which option"
            " was chosen.\n\nreturn: int (Actually, this is probably some sort of enum"
            " shared by all the MenuLoop functions)"
        ),
    )

    OthersMenu = Symbol(
        [0x73AB0],
        [0x2350630],
        None,
        (
            "Called when the in-dungeon 'others' menu is open. Does not return until"
            " the menu is closed.\n\nreturn: Always 0"
        ),
    )


class EuOverlay29Data:
    DUNGEON_STRUCT_SIZE = Symbol(
        [0x2838, 0x286C],
        [0x22DF3B8, 0x22DF3EC],
        0x4,
        "Size of the dungeon struct (0x2CB14)",
    )

    MAX_HP_CAP = Symbol(
        [0x7C00, 0x356F4, 0x3C334],
        [0x22E4780, 0x2312274, 0x2318EB4],
        0x4,
        "The maximum amount of HP a monster can have (999).",
    )

    OFFSET_OF_DUNGEON_FLOOR_PROPERTIES = Symbol(
        [0xB828, 0x5EECC],
        [0x22E83A8, 0x233BA4C],
        0x4,
        "Offset of the floor properties field in the dungeon struct (0x286B2)",
    )

    SPAWN_RAND_MAX = Symbol(
        [0xBC80],
        [0x22E8800],
        0x4,
        (
            "Equal to 10,000 (0x2710). Used as parameter for DungeonRandInt to generate"
            " the random number which determines the entity to spawn."
        ),
    )

    DUNGEON_PRNG_LCG_MULTIPLIER = Symbol(
        [0xE7F8, 0xE8BC],
        [0x22EB378, 0x22EB43C],
        0x4,
        (
            "The multiplier shared by all of the dungeon PRNG's LCGs, 1566083941"
            " (0x5D588B65)."
        ),
    )

    DUNGEON_PRNG_LCG_INCREMENT_SECONDARY = Symbol(
        [0xE8C4],
        [0x22EB444],
        0x4,
        (
            "The increment for the dungeon PRNG's secondary LCGs, 2531011 (0x269EC3)."
            " This happens to be the same increment that the Microsoft Visual C++"
            " runtime library uses in its implementation of the rand() function."
        ),
    )

    KECLEON_FEMALE_ID = Symbol(
        [0x1B23C],
        [0x22F7DBC],
        0x4,
        "0x3D7 (983). Used when spawning Kecleon on an even numbered floor.",
    )

    KECLEON_MALE_ID = Symbol(
        [0x1B240],
        [0x22F7DC0],
        0x4,
        "0x17F (383). Used when spawning Kecleon on an odd numbered floor.",
    )

    MSG_ID_SLOW_START = Symbol(
        [0x1D15C],
        [0x22F9CDC],
        0x4,
        (
            "ID of the message printed when a monster has the ability Slow Start at the"
            " beginning of the floor."
        ),
    )

    EXPERIENCE_POINT_GAIN_CAP = Symbol(
        [0x26574],
        [0x23030F4],
        0x4,
        (
            "A cap on the experience that can be given to a monster in one call to"
            " AddExpSpecial"
        ),
    )

    JUDGMENT_MOVE_ID = Symbol(
        [0x3034C],
        [0x230CECC],
        0x4,
        "Move ID for Judgment (0x1D3)\n\ntype: enum move_id",
    )

    REGULAR_ATTACK_MOVE_ID = Symbol(
        [0x30350],
        [0x230CED0],
        0x4,
        "Move ID for the regular attack (0x163)\n\ntype: enum move_id",
    )

    DEOXYS_ATTACK_ID = Symbol(
        [0x30354],
        [0x230CED4],
        0x4,
        "Monster ID for Deoxys in Attack Forme (0x1A3)\n\ntype: enum monster_id",
    )

    DEOXYS_SPEED_ID = Symbol(
        [0x30358],
        [0x230CED8],
        0x4,
        "Monster ID for Deoxys in Speed Forme (0x1A5)\n\ntype: enum monster_id",
    )

    GIRATINA_ALTERED_ID = Symbol(
        [0x3035C],
        [0x230CEDC],
        0x4,
        "Monster ID for Giratina in Altered Forme (0x211)\n\ntype: enum monster_id",
    )

    PUNISHMENT_MOVE_ID = Symbol(
        [0x30360],
        [0x230CEE0],
        0x4,
        "Move ID for Punishment (0x1BD)\n\ntype: enum move_id",
    )

    OFFENSE_STAT_MAX = Symbol(
        [0x30390],
        [0x230CF10],
        0x4,
        (
            "Cap on an attacker's modified offense (attack or special attack) stat"
            " after boosts. Used during damage calculation."
        ),
    )

    PROJECTILE_MOVE_ID = Symbol(
        [0x30F70, 0x405E0],
        [0x230DAF0, 0x231D160],
        0x4,
        "The move ID of the special 'projectile' move (0x195)\n\ntype: enum move_id",
    )

    BELLY_LOST_PER_TURN = Symbol(
        [0x34950],
        [0x23114D0],
        0x4,
        (
            "The base value by which belly is decreased every turn.\n\nIts raw value is"
            " 0x199A, which encodes a binary fixed-point number (16 fraction bits) with"
            " value (0x199A * 2^-16), and is the closest approximation to 0.1"
            " representable in this number format."
        ),
    )

    MONSTER_HEAL_HP_MAX = Symbol(
        None, None, None, "The maximum amount of HP a monster can have (999)."
    )

    MOVE_TARGET_AND_RANGE_SPECIAL_USER_HEALING = Symbol(
        [0x3EC14],
        [0x231B794],
        0x4,
        (
            "The move target and range code for special healing moves that target just"
            " the user (0x273).\n\ntype: struct move_target_and_range (+ padding)"
        ),
    )

    PLAIN_SEED_VALUE = Symbol(
        [0x40628], [0x231D1A8], 0x4, "Some value related to the Plain Seed (0xBE9)."
    )

    MAX_ELIXIR_PP_RESTORATION = Symbol(
        [0x4062C],
        [0x231D1AC],
        0x4,
        "The amount of PP restored per move by ingesting a Max Elixir (0x3E7).",
    )

    SLIP_SEED_VALUE = Symbol(
        [0x40A94], [0x231D614], 0x4, "Some value related to the Slip Seed (0xC75)."
    )

    ROCK_WRECKER_MOVE_ID = Symbol(
        None, None, None, "The move ID for Rock Wrecker (453)."
    )

    CASTFORM_NORMAL_FORM_MALE_ID = Symbol(
        [0x592F8], [0x2335E78], 0x4, "Castform's male normal form ID (0x17B)"
    )

    CASTFORM_NORMAL_FORM_FEMALE_ID = Symbol(
        [0x592FC], [0x2335E7C], 0x4, "Castform's female normal form ID (0x3D3)"
    )

    CHERRIM_SUNSHINE_FORM_MALE_ID = Symbol(
        [0x59300], [0x2335E80], 0x4, "Cherrim's male sunshine form ID (0x1CD)"
    )

    CHERRIM_OVERCAST_FORM_FEMALE_ID = Symbol(
        [0x59304], [0x2335E84], 0x4, "Cherrim's female overcast form ID (0x424)"
    )

    CHERRIM_SUNSHINE_FORM_FEMALE_ID = Symbol(
        [0x59308], [0x2335E88], 0x4, "Cherrim's female sunshine form ID (0x425)"
    )

    FLOOR_GENERATION_STATUS_PTR = Symbol(
        [
            0x5EED0,
            0x5EF6C,
            0x5F1F0,
            0x5F67C,
            0x5FADC,
            0x5FC3C,
            0x5FDD4,
            0x5FF90,
            0x60370,
            0x607D0,
            0x60FE4,
            0x61164,
            0x61374,
            0x616D4,
            0x620BC,
            0x63FF4,
            0x64280,
            0x64734,
            0x654C0,
            0x657C8,
            0x661DC,
            0x66574,
            0x66844,
            0x66BD8,
            0x66CC8,
            0x66DFC,
            0x66F8C,
        ],
        [
            0x233BA50,
            0x233BAEC,
            0x233BD70,
            0x233C1FC,
            0x233C65C,
            0x233C7BC,
            0x233C954,
            0x233CB10,
            0x233CEF0,
            0x233D350,
            0x233DB64,
            0x233DCE4,
            0x233DEF4,
            0x233E254,
            0x233EC3C,
            0x2340B74,
            0x2340E00,
            0x23412B4,
            0x2342040,
            0x2342348,
            0x2342D5C,
            0x23430F4,
            0x23433C4,
            0x2343758,
            0x2343848,
            0x234397C,
            0x2343B0C,
        ],
        0x4,
        (
            "Pointer to the global FLOOR_GENERATION_STATUS\n\ntype: struct"
            " floor_generation_status*"
        ),
    )

    OFFSET_OF_DUNGEON_N_NORMAL_ITEM_SPAWNS = Symbol(
        [0x5EED8, 0x654C8],
        [0x233BA58, 0x2342048],
        0x4,
        (
            "Offset of the (number of base items + 1) field on the dungeon struct"
            " (0x12AFA)"
        ),
    )

    DUNGEON_GRID_COLUMN_BYTES = Symbol(
        [
            0x5F678,
            0x5FAD8,
            0x5FDD0,
            0x5FF8C,
            0x6036C,
            0x607D4,
            0x60A48,
            0x60FDC,
            0x61160,
            0x61378,
            0x616D0,
            0x620B8,
            0x6249C,
            0x62D94,
            0x63178,
            0x63960,
            0x63FF8,
            0x64284,
            0x644B8,
            0x66530,
        ],
        [
            0x233C1F8,
            0x233C658,
            0x233C950,
            0x233CB0C,
            0x233CEEC,
            0x233D354,
            0x233D5C8,
            0x233DB5C,
            0x233DCE0,
            0x233DEF8,
            0x233E250,
            0x233EC38,
            0x233F01C,
            0x233F914,
            0x233FCF8,
            0x23404E0,
            0x2340B78,
            0x2340E04,
            0x2341038,
            0x23430B0,
        ],
        0x4,
        (
            "The number of bytes in one column of the dungeon grid cell array, 450,"
            " which corresponds to a column of 15 grid cells."
        ),
    )

    DEFAULT_MAX_POSITION = Symbol(
        [0x63FFC],
        [0x2340B7C],
        0x4,
        (
            "A large number (9999) to use as a default position for keeping track of"
            " min/max position values"
        ),
    )

    OFFSET_OF_DUNGEON_GUARANTEED_ITEM_ID = Symbol(
        [0x654C4, 0x68EE4],
        [0x2342044, 0x2345A64],
        0x4,
        "Offset of the guaranteed item ID field in the dungeon struct (0x2C9E8)",
    )

    FIXED_ROOM_TILE_SPAWN_TABLE = Symbol(
        [0x73E5C],
        [0x23509DC],
        0x2C,
        (
            "Table of tiles that can spawn in fixed rooms, pointed into by the"
            " FIXED_ROOM_TILE_SPAWN_TABLE.\n\nThis is an array of 11 4-byte entries"
            " containing info about one tile each. Info includes the trap ID if a trap,"
            " room ID, and flags.\n\ntype: struct fixed_room_tile_spawn_entry[11]"
        ),
    )

    TREASURE_BOX_1_ITEM_IDS = Symbol(
        [0x73E88],
        [0x2350A08],
        0x18,
        (
            "Item IDs for variant 1 of each of the treasure box items"
            " (ITEM_*_BOX_1).\n\ntype: struct item_id_16[12]"
        ),
    )

    FIXED_ROOM_REVISIT_OVERRIDES = Symbol(
        [0x73EA0],
        [0x2350A20],
        0x100,
        (
            "Table of fixed room IDs, which if nonzero, overrides the normal fixed room"
            " ID for a floor (which is used to index the table) if the dungeon has"
            " already been cleared previously.\n\nOverrides are used to substitute"
            " different fixed room data for things like revisits to story"
            " dungeons.\n\ntype: struct fixed_room_id_8[256]"
        ),
    )

    FIXED_ROOM_MONSTER_SPAWN_TABLE = Symbol(
        [0x73FA0],
        [0x2350B20],
        0x1E0,
        (
            "Table of monsters that can spawn in fixed rooms, pointed into by the"
            " FIXED_ROOM_ENTITY_SPAWN_TABLE.\n\nThis is an array of 120 4-byte entries"
            " containing info about one monster each. Info includes the monster ID,"
            " stats, and behavior type.\n\ntype: struct"
            " fixed_room_monster_spawn_entry[120]"
        ),
    )

    FIXED_ROOM_ITEM_SPAWN_TABLE = Symbol(
        [0x74180],
        [0x2350D00],
        0x1F8,
        (
            "Table of items that can spawn in fixed rooms, pointed into by the"
            " FIXED_ROOM_ENTITY_SPAWN_TABLE.\n\nThis is an array of 63 8-byte entries"
            " containing one item ID each.\n\ntype: struct"
            " fixed_room_item_spawn_entry[63]"
        ),
    )

    FIXED_ROOM_ENTITY_SPAWN_TABLE = Symbol(
        [0x74378],
        [0x2350EF8],
        0xC9C,
        (
            "Table of entities (items, monsters, tiles) that can spawn in fixed rooms,"
            " which is indexed into by the main data structure for each fixed"
            " room.\n\nThis is an array of 269 entries. Each entry contains 3 pointers"
            " (one into FIXED_ROOM_ITEM_SPAWN_TABLE, one into"
            " FIXED_ROOM_MONSTER_SPAWN_TABLE, and one into"
            " FIXED_ROOM_TILE_SPAWN_TABLE), and represents the entities that can spawn"
            " on one specific tile in a fixed room.\n\ntype: struct"
            " fixed_room_entity_spawn_entry[269]"
        ),
    )

    STATUS_ICON_ARRAY_MUZZLED = Symbol(
        [0x75248],
        [0x2351DC8],
        0x10,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::muzzled * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_MAGNET_RISE = Symbol(
        [0x75258],
        [0x2351DD8],
        0x10,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::magnet_rise * 8. See UpdateStatusIconFlags for"
            " details."
        ),
    )

    STATUS_ICON_ARRAY_MIRACLE_EYE = Symbol(
        [0x75278],
        [0x2351DF8],
        0x18,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::miracle_eye * 8. See UpdateStatusIconFlags for"
            " details."
        ),
    )

    STATUS_ICON_ARRAY_LEECH_SEED = Symbol(
        [0x75288],
        [0x2351E08],
        0x18,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::leech_seed * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_LONG_TOSS = Symbol(
        [0x752A0],
        [0x2351E20],
        0x18,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::long_toss * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_BLINDED = Symbol(
        [0x752F8],
        [0x2351E78],
        0x28,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::blinded * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_BURN = Symbol(
        [0x75320],
        [0x2351EA0],
        0x28,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::burn * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_SURE_SHOT = Symbol(
        [0x75348],
        [0x2351EC8],
        0x28,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::sure_shot * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_INVISIBLE = Symbol(
        [0x75370],
        [0x2351EF0],
        0x28,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::invisible * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_SLEEP = Symbol(
        [0x75398],
        [0x2351F18],
        0x40,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::sleep * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_CURSE = Symbol(
        [0x753C8],
        [0x2351F48],
        0x38,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::curse * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_FREEZE = Symbol(
        [0x75400],
        [0x2351F80],
        0x40,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::freeze * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_CRINGE = Symbol(
        [0x75440],
        [0x2351FC0],
        0x40,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::cringe * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_BIDE = Symbol(
        [0x75480],
        [0x2352000],
        0x70,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::bide * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_REFLECT = Symbol(
        [0x75580],
        [0x2352100],
        0x90,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::reflect * 8. See UpdateStatusIconFlags for details."
        ),
    )

    DIRECTIONS_XY = Symbol(
        [0x757A8],
        [0x2352328],
        0x20,
        (
            "An array mapping each direction index to its x and y"
            " displacements.\n\nDirections start with 0=down and proceed"
            " counterclockwise (see enum direction_id). Displacements for x and y are"
            " interleaved and encoded as 2-byte signed integers. For example, the first"
            " two integers are [0, 1], which correspond to the x and y displacements"
            " for the 'down' direction (positive y means down)."
        ),
    )

    ITEM_CATEGORY_ACTIONS = Symbol(
        [0x7609C],
        [0x2352C1C],
        0x20,
        (
            "Action ID associated with each item category. Used by"
            " GetItemAction.\n\nEach entry is 2 bytes long."
        ),
    )

    FRACTIONAL_TURN_SEQUENCE = Symbol(
        [0x76342],
        [0x2352EC2],
        0xFA,
        (
            "Read by certain functions that are called by RunFractionalTurn to see if"
            " they should be executed.\n\nArray is accessed via a pointer added to some"
            " multiple of fractional_turn, so that if the resulting memory location is"
            " zero, the function returns."
        ),
    )

    BELLY_DRAIN_IN_WALLS_INT = Symbol(
        [0x767F4],
        [0x2353374],
        0x2,
        (
            "The additional amount by which belly is decreased every turn when inside"
            " walls (integer part)"
        ),
    )

    BELLY_DRAIN_IN_WALLS_THOUSANDTHS = Symbol(
        [0x767F6],
        [0x2353376],
        0x2,
        (
            "The additional amount by which belly is decreased every turn when inside"
            " walls (fractional thousandths)"
        ),
    )

    SPATK_STAT_IDX = Symbol(
        [0x76B74],
        [0x23536F4],
        0x4,
        (
            "The index (1) of the special attack entry in internal stat structs, such"
            " as the stat modifier array for a monster."
        ),
    )

    ATK_STAT_IDX = Symbol(
        [0x76B78],
        [0x23536F8],
        0x4,
        (
            "The index (0) of the attack entry in internal stat structs, such as the"
            " stat modifier array for a monster."
        ),
    )

    MAP_COLOR_TABLE = Symbol(
        None,
        None,
        None,
        (
            "In order: white, black, red, green, blue, magenta, dark pink, chartreuse,"
            " light orange\n\nNote: unverified, ported from Irdkwia's notes\n\ntype:"
            " struct rgb[9]"
        ),
    )

    CORNER_CARDINAL_NEIGHBOR_IS_OPEN = Symbol(
        [0x770A4],
        [0x2353C24],
        0x20,
        (
            "An array mapping each (corner index, neighbor direction index) to whether"
            " or not that neighbor is expected to be open floor.\n\nCorners start with"
            " 0=top-left and proceed clockwise. Directions are enumerated as with"
            " DIRECTIONS_XY. The array is indexed by i=(corner_index * N_DIRECTIONS +"
            " direction). An element of 1 (0) means that starting from the specified"
            " corner of a room, moving in the specified direction should lead to an"
            " open floor tile (non-open terrain like a wall).\n\nNote that this array"
            " is only used for the cardinal directions. The elements at odd indexes are"
            " unused and unconditionally set to 0.\n\nThis array is used by the dungeon"
            " generation algorithm when generating room imperfections. See"
            " GenerateRoomImperfections."
        ),
    )

    DUNGEON_PTR = Symbol(
        [0x775B8],
        [0x2354138],
        0x4,
        (
            "[Runtime] Pointer to the dungeon struct in dungeon mode.\n\nThis is a"
            " 'working copy' of DUNGEON_PTR_MASTER. The main dungeon engine uses this"
            " pointer (or rather pointers to this pointer) when actually running"
            " dungeon mode.\n\ntype: struct dungeon*"
        ),
    )

    DUNGEON_PTR_MASTER = Symbol(
        [0x775BC],
        [0x235413C],
        0x4,
        (
            "[Runtime] Pointer to the dungeon struct in dungeon mode.\n\nThis is a"
            " 'master copy' of the dungeon pointer. The game uses this pointer when"
            " doing low-level memory work (allocation, freeing, zeroing). The normal"
            " DUNGEON_PTR is used for most other dungeon mode work.\n\ntype: struct"
            " dungeon*"
        ),
    )

    LEADER_PTR = Symbol(
        [0x775DC],
        [0x235415C],
        0x4,
        "[Runtime] Pointer to the current leader of the team.\n\ntype: struct entity*",
    )

    DUNGEON_PRNG_STATE = Symbol(
        [0x775F0],
        [0x2354170],
        0x14,
        (
            "[Runtime] The global PRNG state for dungeon mode, not including the"
            " current values in the secondary sequences.\n\nThis struct holds state for"
            " the primary LCG, as well as the current configuration controlling which"
            " LCG to use when generating random numbers. See DungeonRand16Bit for more"
            " information on how the dungeon PRNG works.\n\ntype: struct prng_state"
        ),
    )

    DUNGEON_PRNG_STATE_SECONDARY_VALUES = Symbol(
        [0x77604],
        [0x2354184],
        0x14,
        (
            "[Runtime] An array of 5 integers corresponding to the last value generated"
            " for each secondary LCG sequence.\n\nBased on the assembly, this appears"
            " to be its own global array, separate from DUNGEON_PRNG_STATE."
        ),
    )

    EXCL_ITEM_EFFECTS_WEATHER_ATK_SPEED_BOOST = Symbol(
        [0x77630],
        [0x23541B0],
        0x8,
        (
            "Array of IDs for exclusive item effects that increase attack speed with"
            " certain weather conditions."
        ),
    )

    EXCL_ITEM_EFFECTS_WEATHER_MOVE_SPEED_BOOST = Symbol(
        [0x77638],
        [0x23541B8],
        0x8,
        (
            "Array of IDs for exclusive item effects that increase movement speed with"
            " certain weather conditions."
        ),
    )

    EXCL_ITEM_EFFECTS_WEATHER_NO_STATUS = Symbol(
        [0x77640],
        [0x23541C0],
        0x8,
        (
            "Array of IDs for exclusive item effects that grant status immunity with"
            " certain weather conditions."
        ),
    )

    EXCL_ITEM_EFFECTS_EVASION_BOOST = Symbol(
        [0x77790],
        [0x2354310],
        0x8,
        (
            "Array of IDs for exclusive item effects that grant an evasion boost with"
            " certain weather conditions."
        ),
    )

    DEFAULT_TILE = Symbol(
        [0x777BC],
        [0x235433C],
        0x14,
        (
            "The default tile struct.\n\nThis is just a struct full of zeroes, but is"
            " used as a fallback in various places where a 'default' tile is needed,"
            " such as when a grid index is out of range.\n\ntype: struct tile"
        ),
    )

    HIDDEN_STAIRS_SPAWN_BLOCKED = Symbol(
        [0x77824],
        [0x23543A4],
        0x1,
        (
            "[Runtime] A flag for when Hidden Stairs could normally have spawned on the"
            " floor but didn't.\n\nThis is set either when the Hidden Stairs just"
            " happen not to spawn by chance, or when the current floor is a rescue or"
            " mission destination floor.\n\nThis appears to be part of a larger"
            " (8-byte?) struct. It seems like this value is at least followed by 3"
            " bytes of padding and a 4-byte integer field."
        ),
    )

    FIXED_ROOM_DATA_PTR = Symbol(
        [0x7782C],
        [0x23543AC],
        0x4,
        (
            "[Runtime] Pointer to decoded fixed room data loaded from the"
            " BALANCE/fixed.bin file."
        ),
    )

    NECTAR_IQ_BOOST = Symbol(
        [0x40264], [0x231CDE4], None, "IQ boost from ingesting Nectar."
    )


class EuOverlay29Section:
    name = "overlay29"
    description = (
        "The dungeon engine.\n\nThis is the 'main' overlay of dungeon mode. It controls"
        " most things that happen in a Mystery Dungeon, such as dungeon layout"
        " generation, dungeon menus, enemy AI, and generally just running each turn"
        " while within a dungeon."
    )
    loadaddress = 0x22DCB80
    length = 0x77900
    functions = EuOverlay29Functions
    data = EuOverlay29Data


class EuOverlay3Functions:
    pass


class EuOverlay3Data:
    pass


class EuOverlay3Section:
    name = "overlay3"
    description = "Controls the Friend Rescue submenu within the top menu."
    loadaddress = 0x233D200
    length = 0xA160
    functions = EuOverlay3Functions
    data = EuOverlay3Data


class EuOverlay30Functions:
    pass


class EuOverlay30Data:
    OVERLAY30_JP_STRING_1 = Symbol([0x3864], [0x2386C84], 0xC, "みさき様")

    OVERLAY30_JP_STRING_2 = Symbol([0x3870], [0x2386C90], 0xC, "やよい様")


class EuOverlay30Section:
    name = "overlay30"
    description = "Controls quicksaving in dungeons."
    loadaddress = 0x2383420
    length = 0x38A0
    functions = EuOverlay30Functions
    data = EuOverlay30Data


class EuOverlay31Functions:
    EntryOverlay31 = Symbol(
        [0x0],
        [0x2383420],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    DungeonMenuSwitch = Symbol(
        [0x2A0],
        [0x23836C0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: appears to be an"
            " index of some sort, probably the menu index based on the function name?"
        ),
    )

    MovesMenu = Symbol(
        [0x29A0],
        [0x2385DC0],
        None,
        (
            "Displays a menu showing the moves of a monster. Does not return until the"
            " menu is closed.\n\nThis function does not get called when opening the"
            " leader's move menu.\n\nr0: Pointer to an action struct containing the"
            " index of the monster whose moves will be checked in the action_use_idx"
            " field."
        ),
    )

    HandleMovesMenu = Symbol(
        [0x2BE4],
        [0x2386004],
        None,
        (
            "Handles the different options on the moves menu. Does not return until the"
            " menu is closed.\n\nThis function also takes care of updating the fields"
            " in the action_data struct it receives when a menu option is"
            " chosen.\n\nr0: Pointer to pointer to the entity that opened the menu. The"
            " chosen action will be written on its action field.\nr1: ?\nr2: ?\nr3:"
            " Index of the monster whose moves are going to be displayed on the menu."
            " Unused.\nreturn: True if the menu was closed without selecting anything,"
            " false if an option was chosen."
        ),
    )

    TeamMenu = Symbol(
        [0x4850],
        [0x2387C70],
        None,
        (
            "Called when the in-dungeon 'team' menu is open. Does not return until the"
            " menu is closed.\n\nNote that selecting certain options in this menu (such"
            " as viewing the details or the moves of a pokémon) counts as switching to"
            " a different menu, which causes the function to return.\n\nr0: Pointer to"
            " the leader's entity struct\nreturn: ?"
        ),
    )

    RestMenu = Symbol(
        [0x5F90],
        [0x23893B0],
        None,
        (
            "Called when the in-dungeon 'rest' menu is open. Does not return until the"
            " menu is closed.\n\nNo params."
        ),
    )

    RecruitmentSearchMenuLoop = Symbol(
        [0x6408],
        [0x2389828],
        None,
        (
            "Called on each frame while the in-dungeon 'recruitment search' menu is"
            " open.\n\nreturn: int (Actually, this is probably some sort of enum shared"
            " by all the MenuLoop functions)"
        ),
    )

    HelpMenuLoop = Symbol(
        [0x6A00],
        [0x2389E20],
        None,
        (
            "Called on each frame while the in-dungeon 'help' menu is open.\n\nThe menu"
            " is still considered open while one of the help pages is being viewed, so"
            " this function keeps being called even after choosing an"
            " option.\n\nreturn: int (Actually, this is probably some sort of enum"
            " shared by all the MenuLoop functions)"
        ),
    )


class EuOverlay31Data:
    DUNGEON_D_BOX_LAYOUT_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_3 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_4 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_MAIN_MENU = Symbol([0x75D8], [0x238A9F8], 0x40, "")

    OVERLAY31_UNKNOWN_STRING_IDS = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_STRUCT__NA_2389E30 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_5 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_6 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_7 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_SUBMENU_1 = Symbol([0x7674], [0x238AA94], 0x20, "")

    DUNGEON_SUBMENU_2 = Symbol([0x7694], [0x238AAB4], 0x20, "")

    DUNGEON_SUBMENU_3 = Symbol([0x76B4], [0x238AAD4], 0x20, "")

    DUNGEON_SUBMENU_4 = Symbol([0x76D4], [0x238AAF4], 0x20, "")

    OVERLAY31_UNKNOWN_STRUCT__NA_2389EF0 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_8 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_9 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_10 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_11 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_12 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_13 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_JP_STRING = Symbol(None, None, None, "\n\n----　 初期ポジション=%d　----- \n")

    DUNGEON_D_BOX_LAYOUT_14 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_15 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_16 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_17 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_18 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_19 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_STRUCT__NA_2389FE8 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_20 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_21 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_22 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_23 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_24 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_25 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_SUBMENU_5 = Symbol([0x7920], [0x238AD40], 0x18, "")

    DUNGEON_D_BOX_LAYOUT_26 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_STRUCT__NA_238A144 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_27 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_28 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_STRUCT__NA_238A190 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_SUBMENU_6 = Symbol([0x79A4], [0x238ADC4], 0x48, "")

    DUNGEON_D_BOX_LAYOUT_29 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_30 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_31 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_32 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_RESERVED_SPACE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A260 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_VALUE__NA_238A264 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A268 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A26C = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A270 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A274 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A278 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A27C = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A280 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A284 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A288 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A28C = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )


class EuOverlay31Section:
    name = "overlay31"
    description = "Controls the dungeon menu (during dungeon mode)."
    loadaddress = 0x2383420
    length = 0x7AA0
    functions = EuOverlay31Functions
    data = EuOverlay31Data


class EuOverlay32Functions:
    pass


class EuOverlay32Data:
    pass


class EuOverlay32Section:
    name = "overlay32"
    description = "Unused; all zeroes."
    loadaddress = 0x2383420
    length = 0x20
    functions = EuOverlay32Functions
    data = EuOverlay32Data


class EuOverlay33Functions:
    pass


class EuOverlay33Data:
    pass


class EuOverlay33Section:
    name = "overlay33"
    description = "Unused; all zeroes."
    loadaddress = 0x2383420
    length = 0x20
    functions = EuOverlay33Functions
    data = EuOverlay33Data


class EuOverlay34Functions:
    ExplorersOfSkyMain = Symbol(
        None,
        None,
        None,
        (
            "The main function for Explorers of Sky.\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: probably a game mode ID?\nreturn: probably a"
            " return code?"
        ),
    )


class EuOverlay34Data:
    OVERLAY34_UNKNOWN_STRUCT__NA_22DD014 = Symbol(
        None,
        None,
        None,
        "1*0x4 + 3*0x4\n\nNote: unverified, ported from Irdkwia's notes",
    )

    START_MENU_CONFIRM = Symbol([0xD4C], [0x22DD8CC], 0x18, "Irdkwia's notes: 3*0x8")

    OVERLAY34_UNKNOWN_STRUCT__NA_22DD03C = Symbol(
        None,
        None,
        None,
        "1*0x4 + 3*0x4\n\nNote: unverified, ported from Irdkwia's notes",
    )

    DUNGEON_DEBUG_MENU = Symbol([0xD74], [0x22DD8F4], 0x28, "Irdkwia's notes: 5*0x8")

    OVERLAY34_RESERVED_SPACE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY34_UNKNOWN_POINTER__NA_22DD080 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY34_UNKNOWN_POINTER__NA_22DD084 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY34_UNKNOWN_POINTER__NA_22DD088 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY34_UNKNOWN_POINTER__NA_22DD08C = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY34_UNKNOWN_POINTER__NA_22DD090 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )


class EuOverlay34Section:
    name = "overlay34"
    description = (
        "Related to launching the game.\n\nThere are mention in the strings of logos"
        " like the ESRB logo. This only seems to be loaded during the ESRB rating"
        " splash screen, so this is likely the sole purpose of this overlay."
    )
    loadaddress = 0x22DCB80
    length = 0xDC0
    functions = EuOverlay34Functions
    data = EuOverlay34Data


class EuOverlay35Functions:
    pass


class EuOverlay35Data:
    pass


class EuOverlay35Section:
    name = "overlay35"
    description = "Unused; all zeroes."
    loadaddress = 0x22BD3C0
    length = 0x20
    functions = EuOverlay35Functions
    data = EuOverlay35Data


class EuOverlay4Functions:
    pass


class EuOverlay4Data:
    pass


class EuOverlay4Section:
    name = "overlay4"
    description = "Controls the Trade Items submenu within the top menu."
    loadaddress = 0x233D200
    length = 0x2BE0
    functions = EuOverlay4Functions
    data = EuOverlay4Data


class EuOverlay5Functions:
    pass


class EuOverlay5Data:
    pass


class EuOverlay5Section:
    name = "overlay5"
    description = "Controls the Trade Team submenu within the top menu."
    loadaddress = 0x233D200
    length = 0x3240
    functions = EuOverlay5Functions
    data = EuOverlay5Data


class EuOverlay6Functions:
    pass


class EuOverlay6Data:
    pass


class EuOverlay6Section:
    name = "overlay6"
    description = "Controls the Wonder Mail S submenu within the top menu."
    loadaddress = 0x233D200
    length = 0x2460
    functions = EuOverlay6Functions
    data = EuOverlay6Data


class EuOverlay7Functions:
    pass


class EuOverlay7Data:
    pass


class EuOverlay7Section:
    name = "overlay7"
    description = (
        "Controls the Nintendo WFC submenu within the top menu (under 'Other')."
    )
    loadaddress = 0x233D200
    length = 0x3300
    functions = EuOverlay7Functions
    data = EuOverlay7Data


class EuOverlay8Functions:
    pass


class EuOverlay8Data:
    pass


class EuOverlay8Section:
    name = "overlay8"
    description = (
        "Controls the Send Demo Dungeon submenu within the top menu (under 'Other')."
    )
    loadaddress = 0x233D200
    length = 0x2620
    functions = EuOverlay8Functions
    data = EuOverlay8Data


class EuOverlay9Functions:
    pass


class EuOverlay9Data:
    TOP_MENU_RETURN_MUSIC_ID = Symbol(
        [0xE80],
        [0x233E080],
        None,
        "Song playing in the main menu when returning from the Sky Jukebox.",
    )


class EuOverlay9Section:
    name = "overlay9"
    description = "Controls the Sky Jukebox."
    loadaddress = 0x233D200
    length = 0x2D80
    functions = EuOverlay9Functions
    data = EuOverlay9Data


class EuRamFunctions:
    pass


class EuRamData:
    DUNGEON_COLORMAP_PTR = Symbol(
        [0x1BA634],
        [0x21BA634],
        0x4,
        (
            "Pointer to a colormap used to render colors in a dungeon.\n\nThe colormap"
            " is a list of 4-byte RGB colors of the form {R, G, B, padding}, which the"
            " game indexes into when rendering colors. Some weather conditions modify"
            " the colormap, which is how the color scheme changes when it's, e.g.,"
            " raining."
        ),
    )

    DUNGEON_STRUCT = Symbol(
        [0x1BA674],
        [0x21BA674],
        0x2CB14,
        (
            "The dungeon context struct used for tons of stuff in dungeon mode. See"
            " struct dungeon in the C headers.\n\nThis struct never seems to be"
            " referenced directly, and is instead usually accessed via DUNGEON_PTR in"
            " overlay 29.\n\ntype: struct dungeon"
        ),
    )

    MOVE_DATA_TABLE = Symbol(
        [0x211D0C],
        [0x2211D0C],
        0x38C6,
        (
            "The move data table loaded directly from /BALANCE/waza_p.bin. See struct"
            " move_data_table in the C headers.\n\nPointed to by MOVE_DATA_TABLE_PTR in"
            " the ARM 9 binary.\n\ntype: struct move_data_table"
        ),
    )

    FRAMES_SINCE_LAUNCH = Symbol(
        [0x2A3E8C, 0x2A3EDC],
        [0x22A3E8C, 0x22A3EDC],
        0x4,
        (
            "Starts at 0 when the game is first launched, and continuously ticks up"
            " once per frame while the game is running."
        ),
    )

    BAG_ITEMS = Symbol(
        [0x2A4164],
        [0x22A4164],
        0x12C,
        (
            "Array of item structs within the player's bag.\n\nWhile the game only"
            " allows a maximum of 48 items during normal play, it seems to read up to"
            " 50 item slots if filled.\n\ntype: struct item[50]"
        ),
    )

    BAG_ITEMS_PTR = Symbol([0x2A44E8], [0x22A44E8], 0x4, "Pointer to BAG_ITEMS.")

    STORAGE_ITEMS = Symbol(
        [0x2A44EE],
        [0x22A44EE],
        0x7D0,
        (
            "Array of item IDs in the player's item storage.\n\nFor stackable items,"
            " the quantities are stored elsewhere, in STORAGE_ITEM_QUANTITIES.\n\ntype:"
            " struct item_id_16[1000]"
        ),
    )

    STORAGE_ITEM_QUANTITIES = Symbol(
        [0x2A4CBE],
        [0x22A4CBE],
        0x7D0,
        (
            "Array of 1000 2-byte (unsigned) quantities corresponding to the item IDs"
            " in STORAGE_ITEMS.\n\nIf the corresponding item ID is not a stackable"
            " item, the entry in this array is unused, and will be 0."
        ),
    )

    KECLEON_SHOP_ITEMS_PTR = Symbol(
        [0x2A5490], [0x22A5490], 0x4, "Pointer to KECLEON_SHOP_ITEMS."
    )

    KECLEON_SHOP_ITEMS = Symbol(
        [0x2A5494],
        [0x22A5494],
        0x20,
        (
            "Array of up to 8 items in the Kecleon Shop.\n\nIf there are fewer than 8"
            " items, the array is expected to be null-terminated.\n\ntype: struct"
            " bulk_item[8]"
        ),
    )

    UNUSED_KECLEON_SHOP_ITEMS = Symbol(
        [0x2A54B4],
        [0x22A54B4],
        0x20,
        (
            "Seems to be another array like KECLEON_SHOP_ITEMS, but don't actually"
            " appear to be used by the Kecleon Shop."
        ),
    )

    KECLEON_WARES_ITEMS_PTR = Symbol(
        [0x2A54D4], [0x22A54D4], 0x4, "Pointer to KECLEON_WARES_ITEMS."
    )

    KECLEON_WARES_ITEMS = Symbol(
        [0x2A54D8],
        [0x22A54D8],
        0x10,
        (
            "Array of up to 4 items in Kecleon Wares.\n\nIf there are fewer than 4"
            " items, the array is expected to be null-terminated.\n\ntype: struct"
            " bulk_item[4]"
        ),
    )

    UNUSED_KECLEON_WARES_ITEMS = Symbol(
        [0x2A54E8],
        [0x22A54E8],
        0x10,
        (
            "Seems to be another array like KECLEON_WARES_ITEMS, but don't actually"
            " appear to be used by Kecleon Wares."
        ),
    )

    MONEY_CARRIED = Symbol(
        [0x2A54F8],
        [0x22A54F8],
        0x4,
        "The amount of money the player is currently carrying.",
    )

    MONEY_STORED = Symbol(
        [0x2A5504],
        [0x22A5504],
        0x4,
        "The amount of money the player currently has stored in the Duskull Bank.",
    )

    DIALOG_BOX_LIST = Symbol(None, None, None, "Array of allocated dialog box structs.")

    LAST_NEW_MOVE = Symbol(
        [0x2AB78C],
        [0x22AB78C],
        0x8,
        (
            "Move struct of the last new move introduced when learning a new move."
            " Persists even after the move selection is made in the menu.\n\ntype:"
            " struct move"
        ),
    )

    SCRIPT_VARS_VALUES = Symbol(
        [0x2AB9EC],
        [0x22AB9EC],
        0x400,
        (
            "The table of game variable values. Its structure is determined by"
            " SCRIPT_VARS.\n\nNote that with the script variable list defined in"
            " SCRIPT_VARS, the used length of this table is actually only 0x2B4."
            " However, the real length of this table is 0x400 based on the game"
            " code.\n\ntype: struct script_var_value_table"
        ),
    )

    BAG_LEVEL = Symbol(
        [0x2ABA9C],
        [0x22ABA9C],
        0x1,
        (
            "The player's bag level, which determines the bag capacity. This indexes"
            " directly into the BAG_CAPACITY_TABLE in the ARM9 binary."
        ),
    )

    DEBUG_SPECIAL_EPISODE_NUMBER = Symbol(
        [0x2ABDEC],
        [0x22ABDEC],
        0x1,
        (
            "The number of the special episode currently being played.\n\nThis backs"
            " the EXECUTE_SPECIAL_EPISODE_TYPE script variable.\n\ntype: struct"
            " special_episode_type_8"
        ),
    )

    PENDING_DUNGEON_ID = Symbol(
        [0x2ABE3C],
        [0x22ABE3C],
        0x1,
        (
            "The ID of the selected dungeon when setting off from the"
            " overworld.\n\nControls the text and map location during the 'map"
            " cutscene' just before entering a dungeon, as well as the actual dungeon"
            " loaded afterwards.\n\ntype: struct dungeon_id_8"
        ),
    )

    PENDING_STARTING_FLOOR = Symbol(
        [0x2ABE3D],
        [0x22ABE3D],
        0x1,
        (
            "The floor number to start from in the dungeon specified by"
            " PENDING_DUNGEON_ID."
        ),
    )

    PLAY_TIME_SECONDS = Symbol(
        [0x2ABFD4], [0x22ABFD4], 0x4, "The player's total play time in seconds."
    )

    PLAY_TIME_FRAME_COUNTER = Symbol(
        [0x2ABFD8],
        [0x22ABFD8],
        0x1,
        (
            "Counts from 0-59 in a loop, with the play time being incremented by 1"
            " second with each rollover."
        ),
    )

    TEAM_NAME = Symbol(
        [0x2AC258],
        [0x22AC258],
        0xC,
        (
            "The team name.\n\nA null-terminated string, with a maximum length of 10."
            " Presumably encoded with the ANSI/Shift JIS encoding the game typically"
            " uses.\n\nThis is presumably part of a larger struct, together with other"
            " nearby data."
        ),
    )

    TEAM_MEMBER_LIST = Symbol(
        [0x2AC720],
        [0x22AC720],
        0x936C,
        (
            "List of all team members and persistent information about them.\n\nAppears"
            " to be ordered in chronological order of recruitment. The first five"
            " entries appear to be fixed:\n  1. Hero\n  2. Partner\n  3. Grovyle\n  4."
            " Dusknoir\n  5. Celebi\nSubsequent entries are normal recruits.\n\nIf a"
            " member is released, all subsequent members will be shifted up (so there"
            " should be no gaps in the list).\n\ntype: struct ground_monster[555]"
        ),
    )

    TEAM_ACTIVE_ROSTER = Symbol(
        [0x2B5A8C],
        [0x22B5A8C],
        0x2D8,
        (
            "List of all currently active team members and relevant information about"
            " them.\n\nListed in team order. The first four entries correspond to the"
            " team in normal modes of play. The last three entries are always for"
            " Grovyle, Dusknoir, and Celebi (in that order).\n\nThis struct is updated"
            " relatively infrequently. For example, in dungeon mode, it's typically"
            " only updated at the start of the floor; refer to DUNGEON_STRUCT instead"
            " for live data.\n\ntype: struct team_member[7]"
        ),
    )

    FRAMES_SINCE_LAUNCH_TIMES_THREE = Symbol(
        [0x2BA304],
        [0x22BA304],
        0x4,
        (
            "Starts at 0 when the game is first launched, and ticks up by 3 per frame"
            " while the game is running."
        ),
    )

    SENTRY_DUTY_STRUCT = Symbol(None, None, None, "")

    TURNING_ON_THE_SPOT_FLAG = Symbol(
        [0x37D5A6],
        [0x237D5A6],
        0x1,
        "[Runtime] Flag for whether the player is turning on the spot (pressing Y).",
    )

    METRONOME_NEXT_INDEX = Symbol(
        None,
        None,
        None,
        "[Runtime] The index into METRONOME_TABLE for the next usage of Metronome.",
    )

    FLOOR_GENERATION_STATUS = Symbol(
        [0x37DBBC],
        [0x237DBBC],
        0x40,
        (
            "[Runtime] Status data related to generation of the current floor in a"
            " dungeon.\n\nThis data is populated as the dungeon floor is"
            " generated.\n\ntype: struct floor_generation_status"
        ),
    )


class EuRamSection:
    name = "ram"
    description = (
        "Main memory.\nData in this file aren't located in the ROM itself, and are"
        " instead constructs loaded at runtime.\n\nMore specifically, this file is a"
        " dumping ground for addresses that are useful to know about, but don't fall in"
        " the address ranges of any of the other files. Dynamically loaded constructs"
        " that do fall within the address range of a relevant binary should be listed"
        " in the corresponding YAML file of that binary, since it still has direct"
        " utility when reverse-engineering that particular binary."
    )
    loadaddress = 0x2000000
    length = 0x400000
    functions = EuRamFunctions
    data = EuRamData


class EuSections:
    arm7 = EuArm7Section

    arm9 = EuArm9Section

    itcm = EuItcmSection

    move_effects = EuMove_effectsSection

    overlay0 = EuOverlay0Section

    overlay1 = EuOverlay1Section

    overlay10 = EuOverlay10Section

    overlay11 = EuOverlay11Section

    overlay12 = EuOverlay12Section

    overlay13 = EuOverlay13Section

    overlay14 = EuOverlay14Section

    overlay15 = EuOverlay15Section

    overlay16 = EuOverlay16Section

    overlay17 = EuOverlay17Section

    overlay18 = EuOverlay18Section

    overlay19 = EuOverlay19Section

    overlay2 = EuOverlay2Section

    overlay20 = EuOverlay20Section

    overlay21 = EuOverlay21Section

    overlay22 = EuOverlay22Section

    overlay23 = EuOverlay23Section

    overlay24 = EuOverlay24Section

    overlay25 = EuOverlay25Section

    overlay26 = EuOverlay26Section

    overlay27 = EuOverlay27Section

    overlay28 = EuOverlay28Section

    overlay29 = EuOverlay29Section

    overlay3 = EuOverlay3Section

    overlay30 = EuOverlay30Section

    overlay31 = EuOverlay31Section

    overlay32 = EuOverlay32Section

    overlay33 = EuOverlay33Section

    overlay34 = EuOverlay34Section

    overlay35 = EuOverlay35Section

    overlay4 = EuOverlay4Section

    overlay5 = EuOverlay5Section

    overlay6 = EuOverlay6Section

    overlay7 = EuOverlay7Section

    overlay8 = EuOverlay8Section

    overlay9 = EuOverlay9Section

    ram = EuRamSection
