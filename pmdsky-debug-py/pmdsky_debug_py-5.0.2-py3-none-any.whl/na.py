from .protocol import Symbol


class NaArm7Functions:
    EntryArm7 = Symbol(
        [0x0],
        [0x2380000],
        None,
        (
            "The entrypoint for the ARM7 CPU. This is like the 'main' function for the"
            " ARM7 subsystem.\n\nNo params."
        ),
    )


class NaArm7Data:
    pass


class NaArm7Section:
    name = "arm7"
    description = (
        "The ARM7 binary.\n\nThis is the secondary binary that gets loaded when the"
        " game is launched.\n\nSpeaking generally, this is the program run by the"
        " Nintendo DS's secondary ARM7TDMI CPU, which handles the audio engine, the"
        " touch screen, Wi-Fi functions, cryptography, and more."
    )
    loadaddress = 0x2380000
    length = 0x27080
    functions = NaArm7Functions
    data = NaArm7Data


class NaArm9Functions:
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
        [0xC110],
        [0x200C110],
        None,
        "Just returns 0 in the final binary.\n\nr0: flag ID\nreturn: flag value",
    )

    SetDebugFlag1 = Symbol(
        [0xC118],
        [0x200C118],
        None,
        "A no-op in the final binary.\n\nr0: flag ID\nr1: flag value",
    )

    AppendProgPos = Symbol(
        [0xC120],
        [0x200C120],
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
        [0xC16C],
        [0x200C16C],
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
        [0xC1C8, 0xC1FC],
        [0x200C1C8, 0x200C1FC],
        None,
        (
            "Would log a printf format string in the debug binary.\n\nThis still"
            " constructs the string with Vsprintf, but doesn't actually do anything"
            " with it in the final binary.\n\nr0: format\n...: variadic"
        ),
    )

    GetDebugFlag2 = Symbol(
        [0xC234],
        [0x200C234],
        None,
        "Just returns 0 in the final binary.\n\nr0: flag ID\nreturn: flag value",
    )

    SetDebugFlag2 = Symbol(
        [0xC23C],
        [0x200C23C],
        None,
        "A no-op in the final binary.\n\nr0: flag ID\nr1: flag value",
    )

    DebugPrint = Symbol(
        [0xC240],
        [0x200C240],
        None,
        (
            "Would log a printf format string in the debug binary. A no-op in the final"
            " binary.\n\nr0: log level\nr1: format\n...: variadic"
        ),
    )

    FatalError = Symbol(
        [0xC25C],
        [0x200C25C],
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
        [0xC2DC],
        [0x200C2DC],
        None,
        (
            "Open the 6 files at PACK_FILE_PATHS_TABLE into PACK_FILE_OPENED. Called"
            " during game initialisation.\n\nNo params."
        ),
    )

    GetFileLengthInPackWithPackNb = Symbol(
        [0xC33C],
        [0x200C33C],
        None,
        (
            "Call GetFileLengthInPack after looking up the global Pack archive by its"
            " number\n\nr0: pack file number\nr1: file number\nreturn: size of the file"
            " in bytes from the Pack Table of Content"
        ),
    )

    LoadFileInPackWithPackId = Symbol(
        [0xC35C],
        [0x200C35C],
        None,
        (
            "Call LoadFileInPack after looking up the global Pack archive by its"
            " identifier\n\nr0: pack file identifier\nr1: [output] target buffer\nr2:"
            " file index\nreturn: number of read bytes (identical to the length of the"
            " pack from the Table of Content)"
        ),
    )

    AllocAndLoadFileInPack = Symbol(
        [0xC388],
        [0x200C388],
        None,
        (
            "Allocate a file and load a file from the pack archive inside.\nThe data"
            " pointed by the pointer in the output need to be freed once is not needed"
            " anymore.\n\nr0: pack file identifier\nr1: file index\nr2: [output] result"
            " struct (will contain length and pointer)\nr3: allocation flags"
        ),
    )

    OpenPackFile = Symbol(
        [0xC3E0],
        [0x200C3E0],
        None,
        (
            "Open a Pack file, to be read later. Initialise the output"
            " structure.\n\nr0: [output] pack file struct\nr1: file name"
        ),
    )

    GetFileLengthInPack = Symbol(
        [0xC474],
        [0x200C474],
        None,
        (
            "Get the length of a file entry from a Pack archive\n\nr0: pack file"
            " struct\nr1: file index\nreturn: size of the file in bytes from the Pack"
            " Table of Content"
        ),
    )

    LoadFileInPack = Symbol(
        [0xC484],
        [0x200C484],
        None,
        (
            "Load the indexed file from the Pack archive, itself loaded from the"
            " ROM.\n\nr0: pack file struct\nr1: [output] target buffer\nr2: file"
            " index\nreturn: number of read bytes (identical to the length of the pack"
            " from the Table of Content)"
        ),
    )

    GetDamageSource = Symbol(
        [0xCA54],
        [0x200CA54],
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
        [0xCAF0],
        [0x200CAF0],
        None,
        (
            "Likely a linker-generated veneer for GetItemCategory.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " Item ID\nreturn: Category ID"
        ),
    )

    GetItemMoveId16 = Symbol(
        [0xCAFC],
        [0x200CAFC],
        None,
        (
            "Wraps GetItemMoveId, ensuring that the return value is 16-bit.\n\nr0: item"
            " ID\nreturn: move ID"
        ),
    )

    IsThrownItem = Symbol(
        [0xCB10],
        [0x200CB10],
        None,
        (
            "Checks if a given item ID is a thrown item (CATEGORY_THROWN_LINE or"
            " CATEGORY_THROWN_ARC).\n\nr0: item ID\nreturn: bool"
        ),
    )

    IsNotMoney = Symbol(
        [0xCB2C],
        [0x200CB2C],
        None,
        "Checks if an item ID is not ITEM_POKE.\n\nr0: item ID\nreturn: bool",
    )

    IsEdible = Symbol(
        [0xCB4C],
        [0x200CB4C],
        None,
        (
            "Checks if an item has an item category of CATEGORY_BERRIES_SEEDS_VITAMINS"
            " or CATEGORY_FOOD_GUMMIES.\n\nr0: item ID\nreturn: bool"
        ),
    )

    IsHM = Symbol(
        [0xCB70],
        [0x200CB70],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: bool",
    )

    IsGummi = Symbol(
        [0xCBF4],
        [0x200CBF4],
        None,
        "Checks if an item is a Gummi.\n\nr0: item ID\nreturn: bool",
    )

    IsAuraBow = Symbol(
        [0xCC14],
        [0x200CC14],
        None,
        (
            "Checks if an item is one of the aura bows received at the start of the"
            " game.\n\nr0: item ID\nreturn: bool"
        ),
    )

    InitItem = Symbol(
        [0xCE9C],
        [0x200CE9C],
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
        [0xCF58],
        [0x200CF58],
        None,
        (
            "Wrapper around InitItem with quantity set to 0.\n\nr0: pointer to item to"
            " initialize\nr1: item ID\nr2: sticky flag"
        ),
    )

    GetDisplayedBuyPrice = Symbol(
        [0xD0D0],
        [0x200D0D0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item\nreturn: buy price",
    )

    GetDisplayedSellPrice = Symbol(
        [0xD118],
        [0x200D118],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item\nreturn: sell price",
    )

    GetActualBuyPrice = Symbol(
        [0xD160],
        [0x200D160],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item\nreturn: buy price",
    )

    GetActualSellPrice = Symbol(
        [0xD1A8],
        [0x200D1A8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item\nreturn: sell price",
    )

    FindItemInInventory = Symbol(
        [0xD278],
        [0x200D278],
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
            0xD634,
            0xE990,
            0x13758,
            0x176E4,
            0x17A40,
            0x23590,
            0x2378C,
            0x37F30,
            0x39438,
            0x3A970,
            0x3CFA4,
            0x4174C,
            0x42A84,
            0x52418,
            0x54A60,
            0x609E8,
        ],
        [
            0x200D634,
            0x200E990,
            0x2013758,
            0x20176E4,
            0x2017A40,
            0x2023590,
            0x202378C,
            0x2037F30,
            0x2039438,
            0x203A970,
            0x203CFA4,
            0x204174C,
            0x2042A84,
            0x2052418,
            0x2054A60,
            0x20609E8,
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
        [0xD81C], [0x200D81C], None, "Zero-initializes an item struct.\n\nr0: item"
    )

    WriteItemsToSave = Symbol(
        [0xD95C],
        [0x200D95C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: start_address\nr1:"
            " total_length\nreturn: ?"
        ),
    )

    ReadItemsFromSave = Symbol(
        [0xDC44],
        [0x200DC44],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: start_address\nr1:"
            " total_length\nreturn: ?"
        ),
    )

    IsItemAvailableInDungeonGroup = Symbol(
        [0xE00C],
        [0x200E00C],
        None,
        (
            "Checks one specific bit from table [NA]2094D34\n\nNote: unverified, ported"
            " from Irdkwia's notes\n\nr0: dungeon ID\nr1: item ID\nreturn: bool"
        ),
    )

    GetItemIdFromList = Symbol(
        [0xE054],
        [0x200E054],
        None,
        (
            "category_num and item_num are numbers in range 0-10000\n\nNote:"
            " unverified, ported from Irdkwia's notes\n\nr0: list_id\nr1:"
            " category_num\nr2: item_num\nreturn: item ID"
        ),
    )

    NormalizeTreasureBox = Symbol(
        [0xE1F8],
        [0x200E1F8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn:"
            " normalized item ID"
        ),
    )

    RemoveEmptyItems = Symbol(
        [0xE610],
        [0x200E610],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: list_pointer\nr1: size",
    )

    LoadItemPspi2n = Symbol(
        [0xE6D8],
        [0x200E6D8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GetExclusiveItemType = Symbol(
        [0xE760],
        [0x200E760],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: ?",
    )

    GetExclusiveItemOffsetEnsureValid = Symbol(
        [0xE77C],
        [0x200E77C],
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
        [0xE7C0],
        [0x200E7C0],
        None,
        "Checks if an item ID is valid(?).\n\nr0: item ID\nreturn: bool",
    )

    GetExclusiveItemParameter = Symbol(
        [0xE7E8],
        [0x200E7E8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: ?",
    )

    GetItemCategory = Symbol(
        [0xE808],
        [0x200E808],
        None,
        (
            "Returns the category of the specified item\n\nr0: Item ID\nreturn: Item"
            " category"
        ),
    )

    EnsureValidItem = Symbol(
        [0xE828],
        [0x200E828],
        None,
        (
            "Checks if the given item ID is valid (using IsItemValid). If so, return"
            " the given item ID. Otherwise, return ITEM_PLAIN_SEED.\n\nr0: item"
            " ID\nreturn: valid item ID"
        ),
    )

    GetItemName = Symbol(
        [0xE864],
        [0x200E864],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: item"
            " name"
        ),
    )

    GetItemNameFormatted = Symbol(
        [0xE884],
        [0x200E884],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output] name\nr1:"
            " item_id\nr2: flag\nr3: flag2"
        ),
    )

    GetItemBuyPrice = Symbol(
        [0xE9B8],
        [0x200E9B8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: buy"
            " price"
        ),
    )

    GetItemSellPrice = Symbol(
        [0xE9D8],
        [0x200E9D8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: sell"
            " price"
        ),
    )

    GetItemSpriteId = Symbol(
        [0xE9F8],
        [0x200E9F8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn:"
            " sprite ID"
        ),
    )

    GetItemPaletteId = Symbol(
        [0xEA18],
        [0x200EA18],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn:"
            " palette ID"
        ),
    )

    GetItemActionName = Symbol(
        [0xEA38],
        [0x200EA38],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn:"
            " action name ID"
        ),
    )

    GetThrownItemQuantityLimit = Symbol(
        [0xEA58],
        [0x200EA58],
        None,
        (
            "Get the minimum or maximum quantity for a given thrown item ID.\n\nr0:"
            " item ID\nr1: 0 for minimum, 1 for maximum\nreturn: minimum/maximum"
            " quantity for the given item ID"
        ),
    )

    GetItemMoveId = Symbol(
        [0xEA80],
        [0x200EA80],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: move ID",
    )

    TestItemFlag0xE = Symbol(
        [0xEAA0],
        [0x200EAA0],
        None,
        (
            "Tests bit 7 if r1 is 0, bit 6 if r1 is 1, bit 5 otherwise\n\nNote:"
            " unverified, ported from Irdkwia's notes\n\nr0: item ID\nr1:"
            " bit_id\nreturn: bool"
        ),
    )

    IsItemInTimeDarkness = Symbol(
        [0xEB30],
        [0x200EB30],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: bool",
    )

    IsItemValidVeneer = Symbol(
        [0xEB58],
        [0x200EB58],
        None,
        (
            "Likely a linker-generated veneer for IsItemValid.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " item ID\nreturn: bool"
        ),
    )

    SetGold = Symbol(
        [0xECD8],
        [0x200ECD8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: new value",
    )

    GetGold = Symbol(
        [0xECFC],
        [0x200ECFC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: value",
    )

    SetMoneyCarried = Symbol(
        [0xED1C],
        [0x200ED1C],
        None,
        (
            "Sets the amount of money the player is carrying, clamping the value to the"
            " range [0, MAX_MONEY_CARRIED].\n\nr0: new value"
        ),
    )

    GetCurrentBagCapacity = Symbol(
        [0xED84],
        [0x200ED84],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: bag capacity",
    )

    IsBagFull = Symbol(
        [0xEDC0],
        [0x200EDC0],
        None,
        (
            "Implements SPECIAL_PROC_IS_BAG_FULL (see"
            " ScriptSpecialProcessCall).\n\nreturn: bool"
        ),
    )

    GetNbItemsInBag = Symbol(
        [0xEDFC],
        [0x200EDFC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: # items",
    )

    CountNbItemsOfTypeInBag = Symbol(
        [0xEE4C],
        [0x200EE4C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: count",
    )

    CountItemTypeInBag = Symbol(
        [0xEE88],
        [0x200EE88],
        None,
        (
            "Implements SPECIAL_PROC_COUNT_ITEM_TYPE_IN_BAG (see"
            " ScriptSpecialProcessCall).\n\nIrdkwia's notes: Count also"
            " stackable\n\nr0: item ID\nreturn: number of items of the specified ID in"
            " the bag"
        ),
    )

    IsItemInBag = Symbol(
        [0xEEE0],
        [0x200EEE0],
        None,
        "Checks if an item is in the player's bag.\n\nr0: item ID\nreturn: bool",
    )

    IsItemWithFlagsInBag = Symbol(
        [0xEF20],
        [0x200EF20],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nr1:"
            " flags\nreturn: bool"
        ),
    )

    IsItemInTreasureBoxes = Symbol(
        [0xEF6C],
        [0x200EF6C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: bool",
    )

    IsHeldItemInBag = Symbol(
        [0xEFCC],
        [0x200EFCC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item\nreturn: bool",
    )

    IsItemForSpecialSpawnInBag = Symbol(
        [0xF050],
        [0x200F050],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: bool",
    )

    HasStorableItems = Symbol(
        [0xF0E4],
        [0x200F0E4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: bool",
    )

    GetItemIndex = Symbol(
        [0xF14C],
        [0x200F14C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_ptr\nreturn: index",
    )

    GetEquivItemIndex = Symbol(
        [0xF18C],
        [0x200F18C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_ptr\nreturn: index",
    )

    GetEquippedThrowableItem = Symbol(
        [0xF208],
        [0x200F208],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: index",
    )

    GetFirstUnequippedItemOfType = Symbol(
        [0xF26C],
        [0x200F26C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: index",
    )

    CopyItemAtIdx = Symbol(
        [0xF2E0],
        [0x200F2E0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: index\nr1: [output]"
            " item_ptr\nreturn: exists"
        ),
    )

    GetItemAtIdx = Symbol(
        [0xF348],
        [0x200F348],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: index\nreturn: item"
            " pointer"
        ),
    )

    RemoveEmptyItemsInBag = Symbol(
        [0xF370],
        [0x200F370],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    RemoveItemNoHole = Symbol(
        [0xF390],
        [0x200F390],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: index\nreturn: ?",
    )

    RemoveItem = Symbol(
        [0xF404],
        [0x200F404],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: index",
    )

    RemoveHeldItemNoHole = Symbol(
        [0xF454],
        [0x200F454],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: held_index",
    )

    RemoveItemByIdAndStackNoHole = Symbol(
        [0xF4D4],
        [0x200F4D4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_ptr\nreturn: ?",
    )

    RemoveEquivItem = Symbol(
        [0xF558],
        [0x200F558],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_ptr\nreturn: ?",
    )

    RemoveEquivItemNoHole = Symbol(
        [0xF600],
        [0x200F600],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_ptr\nreturn: ?",
    )

    DecrementStackItem = Symbol(
        [0xF694],
        [0x200F694],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_ptr\nreturn: ?",
    )

    RemoveItemNoHoleCheck = Symbol(
        [0xF718],
        [0x200F718],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: index\nreturn: ?",
    )

    RemoveFirstUnequippedItemOfType = Symbol(
        [0xF798],
        [0x200F798],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: ?",
    )

    RemoveAllItems = Symbol(
        [0xF7A8],
        [0x200F7A8],
        None,
        (
            "WARNING! Does not remove from party items\n\nNote: unverified, ported from"
            " Irdkwia's notes"
        ),
    )

    RemoveAllItemsStartingAt = Symbol(
        [0xF7DC],
        [0x200F7DC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: index",
    )

    SpecialProcAddItemToBag = Symbol(
        [0xF84C],
        [0x200F84C],
        None,
        (
            "Implements SPECIAL_PROC_ADD_ITEM_TO_BAG (see"
            " ScriptSpecialProcessCall).\n\nr0: pointer to an owned_item\nreturn: bool"
        ),
    )

    AddItemToBagNoHeld = Symbol(
        [0xF874],
        [0x200F874],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_str\nreturn: ?",
    )

    AddItemToBag = Symbol(
        [0xF884],
        [0x200F884],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item_str\nr1:"
            " held_by\nreturn: ?"
        ),
    )

    ScriptSpecialProcess0x39 = Symbol(
        [0xFD54],
        [0x200FD54],
        None,
        "Implements SPECIAL_PROC_0x39 (see ScriptSpecialProcessCall).\n\nreturn: bool",
    )

    CountItemTypeInStorage = Symbol(
        [0xFEE4],
        [0x200FEE4],
        None,
        (
            "Implements SPECIAL_PROC_COUNT_ITEM_TYPE_IN_STORAGE (see"
            " ScriptSpecialProcessCall).\n\nr0: pointer to an owned_item\nreturn:"
            " number of items of the specified ID in storage"
        ),
    )

    RemoveItemsTypeInStorage = Symbol(
        [0x101E4],
        [0x20101E4],
        None,
        (
            "Probably? Implements SPECIAL_PROC_0x2A (see"
            " ScriptSpecialProcessCall).\n\nr0: pointer to an owned_item\nreturn: bool"
        ),
    )

    AddItemToStorage = Symbol(
        [0x1031C],
        [0x201031C],
        None,
        (
            "Implements SPECIAL_PROC_ADD_ITEM_TO_STORAGE (see"
            " ScriptSpecialProcessCall).\n\nr0: pointer to an owned_item\nreturn: bool"
        ),
    )

    SetMoneyStored = Symbol(
        [0x10724],
        [0x2010724],
        None,
        (
            "Sets the amount of money the player has stored in the Duskull Bank,"
            " clamping the value to the range [0, MAX_MONEY_STORED].\n\nr0: new value"
        ),
    )

    GetKecleonItems1 = Symbol(
        [0x10A4C], [0x2010A4C], None, "Note: unverified, ported from Irdkwia's notes"
    )

    GetKecleonItems2 = Symbol(
        [0x10D58], [0x2010D58], None, "Note: unverified, ported from Irdkwia's notes"
    )

    GetExclusiveItemOffset = Symbol(
        [0x10E40],
        [0x2010E40],
        None,
        (
            "Gets the exclusive item offset, which is the item ID relative to that of"
            " the first exclusive item, the Prism Ruff.\n\nr0: item ID\nreturn: offset"
        ),
    )

    ApplyExclusiveItemStatBoosts = Symbol(
        [0x10E64],
        [0x2010E64],
        None,
        (
            "Applies stat boosts from an exclusive item.\n\nr0: item ID\nr1: pointer to"
            " attack stat to modify\nr2: pointer to special attack stat to modify\nr3:"
            " pointer to defense stat to modify\nstack[0]: pointer to special defense"
            " stat to modify"
        ),
    )

    SetExclusiveItemEffect = Symbol(
        [0x10F80],
        [0x2010F80],
        None,
        (
            "Sets the bit for an exclusive item effect.\n\nr0: pointer to the effects"
            " bitvector to modify\nr1: exclusive item effect ID"
        ),
    )

    ExclusiveItemEffectFlagTest = Symbol(
        [0x10FA4],
        [0x2010FA4],
        None,
        (
            "Tests the exclusive item bitvector for a specific exclusive item"
            " effect.\n\nr0: the effects bitvector to test\nr1: exclusive item effect"
            " ID\nreturn: bool"
        ),
    )

    IsExclusiveItemIdForMonster = Symbol(
        [0x10FC4],
        [0x2010FC4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nr1: monster"
            " ID\nr2: type ID 1\nr3: type ID 2\nreturn: bool"
        ),
    )

    IsExclusiveItemForMonster = Symbol(
        [0x11094],
        [0x2011094],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item\nr1: monster"
            " ID\nr2: type ID 1\nr3: type ID 2\nreturn: bool"
        ),
    )

    BagHasExclusiveItemTypeForMonster = Symbol(
        [0x110D8],
        [0x20110D8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: excl_type\nr1:"
            " monster ID\nr2: type ID 1\nr3: type ID 2\nreturn: item ID"
        ),
    )

    ProcessGinsengOverworld = Symbol(
        [0x115F8],
        [0x20115F8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: target\nr1: [output]"
            " move ID\nr2: [output] move boost\nreturn: boost"
        ),
    )

    ApplyGummiBoostsGroundMode = Symbol(
        [0x1189C],
        [0x201189C],
        None,
        (
            "Applies the IQ boosts from eating a Gummi to the target monster.\n\nr0:"
            " Pointer to something\nr1: Pointer to something\nr2: Pointer to"
            " something\nr3: Pointer to something\nstack[0]: ?\nstack[1]: ?\nstack[2]:"
            " Pointer to a buffer to store some result into"
        ),
    )

    LoadSynthBin = Symbol(
        [0x12AE0], [0x2012AE0], None, "Note: unverified, ported from Irdkwia's notes"
    )

    CloseSynthBin = Symbol(
        [0x12B34], [0x2012B34], None, "Note: unverified, ported from Irdkwia's notes"
    )

    GetSynthItem = Symbol(
        [0x13250], [0x2013250], None, "Note: unverified, ported from Irdkwia's notes"
    )

    LoadWazaP = Symbol(
        [0x133C4], [0x20133C4], None, "Note: unverified, ported from Irdkwia's notes"
    )

    LoadWazaP2 = Symbol(
        [0x133EC], [0x20133EC], None, "Note: unverified, ported from Irdkwia's notes"
    )

    UnloadCurrentWazaP = Symbol(
        [0x13414], [0x2013414], None, "Note: unverified, ported from Irdkwia's notes"
    )

    GetMoveName = Symbol(
        [0x13454],
        [0x2013454],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: move"
            " name"
        ),
    )

    FormatMoveString = Symbol(
        [0x13478],
        [0x2013478],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: string_buffer\nr1:"
            " move\nr2: type_print"
        ),
    )

    FormatMoveStringMore = Symbol(
        [0x13780],
        [0x2013780],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ???\nr1: ???\nr2:"
            " move\nr3: type_print"
        ),
    )

    InitMove = Symbol(
        [0x137B8],
        [0x20137B8],
        None,
        (
            "Initializes a move info struct.\n\nThis sets f_exists and f_enabled_for_ai"
            " on the flags, the ID to the given ID, the PP to the max PP for the move"
            " ID, and the ginseng boost to 0.\n\nr0: pointer to move to initialize\nr1:"
            " move ID"
        ),
    )

    GetInfoMoveCheckId = Symbol(
        [0x137E8],
        [0x20137E8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nr1: move ID",
    )

    GetInfoMoveGround = Symbol(
        [0x13828],
        [0x2013828],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: ground move\nr1: move ID",
    )

    GetMoveTargetAndRange = Symbol(
        [0x13840],
        [0x2013840],
        None,
        (
            "Gets the move target-and-range field. See struct move_target_and_range in"
            " the C headers.\n\nr0: move pointer\nr1: AI flag (every move has two"
            " target-and-range fields, one for players and one for AI)\nreturn: move"
            " target and range"
        ),
    )

    GetMoveType = Symbol(
        [0x13864],
        [0x2013864],
        None,
        "Gets the type of a move\n\nr0: Pointer to move data\nreturn: Type of the move",
    )

    GetMovesetLevelUpPtr = Symbol(
        [0x13884],
        [0x2013884],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn: ?",
    )

    IsInvalidMoveset = Symbol(
        [0x138CC],
        [0x20138CC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_id\nreturn: bool",
    )

    GetMovesetHmTmPtr = Symbol(
        [0x138F4],
        [0x20138F4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn: ?",
    )

    GetMovesetEggPtr = Symbol(
        [0x13940],
        [0x2013940],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn: ?",
    )

    GetMoveAiWeight = Symbol(
        [0x1398C],
        [0x201398C],
        None,
        (
            "Gets the AI weight of a move\n\nr0: Pointer to move data\nreturn: AI"
            " weight of the move"
        ),
    )

    GetMoveNbStrikes = Symbol(
        [0x139AC],
        [0x20139AC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nreturn: # strikes",
    )

    GetMoveBasePower = Symbol(
        [0x139CC],
        [0x20139CC],
        None,
        (
            "Gets the base power of a move from the move data table.\n\nr0: move"
            " pointer\nreturn: base power"
        ),
    )

    GetMoveBasePowerGround = Symbol(
        [0x139EC],
        [0x20139EC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ground_move\nreturn:"
            " base power"
        ),
    )

    GetMoveAccuracyOrAiChance = Symbol(
        [0x13A0C],
        [0x2013A0C],
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
        [0x13A30],
        [0x2013A30],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nreturn: base PP",
    )

    GetMaxPp = Symbol(
        [0x13A50],
        [0x2013A50],
        None,
        (
            "Gets the maximum PP for a given move.\n\nIrkdwia's notes:"
            " GetMovePPWithBonus\n\nr0: move pointer\nreturn: max PP for the given"
            " move, capped at 99"
        ),
    )

    GetMoveMaxGinsengBoost = Symbol(
        [0x13AD0],
        [0x2013AD0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nreturn: max"
            " ginseng boost"
        ),
    )

    GetMoveMaxGinsengBoostGround = Symbol(
        [0x13AF0],
        [0x2013AF0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ground_move\nreturn:"
            " max ginseng boost"
        ),
    )

    GetMoveCritChance = Symbol(
        [0x13B10],
        [0x2013B10],
        None,
        (
            "Gets the critical hit chance of a move.\n\nr0: move pointer\nreturn:"
            " critical hit chance"
        ),
    )

    IsThawingMove = Symbol(
        [0x13B30],
        [0x2013B30],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nreturn: bool",
    )

    IsAffectedByTaunt = Symbol(
        [0x13B50],
        [0x2013B50],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nBased on struct"
            " move_data, maybe this should be IsUsableWhileTaunted?\n\nr0:"
            " move\nreturn: bool"
        ),
    )

    GetMoveRangeId = Symbol(
        [0x13B70],
        [0x2013B70],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nreturn: range ID",
    )

    GetMoveActualAccuracy = Symbol(
        [0x13B90],
        [0x2013B90],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn:"
            " accuracy"
        ),
    )

    GetMoveBasePowerFromId = Symbol(
        [0x13BE8],
        [0x2013BE8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: base"
            " power"
        ),
    )

    IsMoveRangeString19 = Symbol(
        [0x13C04],
        [0x2013C04],
        None,
        (
            "Returns whether a move's range string is 19 ('User').\n\nr0: Move"
            " pointer\nreturn: True if the move's range string field has a value of 19."
        ),
    )

    GetMoveMessageFromId = Symbol(
        [0x13C30],
        [0x2013C30],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID?\nreturn: string",
    )

    GetNbMoves = Symbol(
        [0x13C64],
        [0x2013C64],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_str\nreturn:"
            " # moves"
        ),
    )

    GetMovesetIdx = Symbol(
        [0x13CAC, 0x14804],
        [0x2013CAC, 0x2014804],
        None,
        (
            "Returns the move position in the moveset if it is found, -1"
            " otherwise\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " moveset_str\nr1: move ID\nreturn: ?"
        ),
    )

    IsReflectedByMagicCoat = Symbol(
        [0x13D08],
        [0x2013D08],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    CanBeSnatched = Symbol(
        [0x13D24],
        [0x2013D24],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    FailsWhileMuzzled = Symbol(
        [0x13D40],
        [0x2013D40],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nCalled IsMouthMove in"
            " Irdkwia's notes, which presumably is relevant to the Muzzled"
            " status.\n\nr0: move ID\nreturn: bool"
        ),
    )

    IsSoundMove = Symbol(
        [0x13D5C],
        [0x2013D5C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nreturn: bool",
    )

    IsRecoilMove = Symbol(
        [0x13E14],
        [0x2013E14],
        None,
        (
            "Checks if the given move is a recoil move (affected by Reckless).\n\nr0:"
            " move ID\nreturn: bool"
        ),
    )

    AllManip1 = Symbol(
        [0x141E0], [0x20141E0], None, "Note: unverified, ported from Irdkwia's notes"
    )

    AllManip2 = Symbol(
        [0x14208], [0x2014208], None, "Note: unverified, ported from Irdkwia's notes"
    )

    ManipMoves1v1 = Symbol(
        [0x1429C], [0x201429C], None, "Note: unverified, ported from Irdkwia's notes"
    )

    ManipMoves1v2 = Symbol(
        [0x1433C], [0x201433C], None, "Note: unverified, ported from Irdkwia's notes"
    )

    ManipMoves2v1 = Symbol(
        [0x144A4], [0x20144A4], None, "Note: unverified, ported from Irdkwia's notes"
    )

    ManipMoves2v2 = Symbol(
        [0x14544], [0x2014544], None, "Note: unverified, ported from Irdkwia's notes"
    )

    DungeonMoveToGroundMove = Symbol(
        [0x146AC],
        [0x20146AC],
        None,
        (
            "Converts a struct move to a struct ground_move.\n\nr0: [output]"
            " ground_move\nr1: move"
        ),
    )

    GroundToDungeonMoveset = Symbol(
        [0x146E4],
        [0x20146E4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output]"
            " moveset_dun_str\nr1: moveset_str"
        ),
    )

    DungeonToGroundMoveset = Symbol(
        [0x14778],
        [0x2014778],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output]"
            " moveset_str\nr1: moveset_dun_str"
        ),
    )

    GetInfoGroundMoveset = Symbol(
        [0x147B8],
        [0x20147B8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_str\nr1:"
            " moves_id"
        ),
    )

    FindFirstFreeMovesetIdx = Symbol(
        [0x14860],
        [0x2014860],
        None,
        (
            "Returns the first position of an empty move in the moveset if it is found,"
            " -1 otherwise\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " moveset_str\nreturn: index"
        ),
    )

    LearnMoves = Symbol(
        [0x148AC],
        [0x20148AC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_str\nr1:"
            " moves_id"
        ),
    )

    CopyMoveTo = Symbol(
        [0x14A4C],
        [0x2014A4C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: write_info\nr1:"
            " buffer_write"
        ),
    )

    CopyMoveFrom = Symbol(
        [0x14A84],
        [0x2014A84],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info\nr1:"
            " buffer_read"
        ),
    )

    CopyMovesetTo = Symbol(
        [0x14ABC],
        [0x2014ABC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: write_info\nr1:"
            " buffer_write"
        ),
    )

    CopyMovesetFrom = Symbol(
        [0x14AEC],
        [0x2014AEC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info\nr1:"
            " buffer_read"
        ),
    )

    Is2TurnsMove = Symbol(
        [0x14C64],
        [0x2014C64],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    IsRegularAttackOrProjectile = Symbol(
        [0x14CEC],
        [0x2014CEC],
        None,
        (
            "Checks if a move ID is MOVE_REGULAR_ATTACK or MOVE_PROJECTILE.\n\nr0: move"
            " ID\nreturn: bool"
        ),
    )

    IsPunchMove = Symbol(
        [0x14D18],
        [0x2014D18],
        None,
        (
            "Checks if the given move is a punch move (affected by Iron Fist).\n\nr0:"
            " move ID\nreturn: bool"
        ),
    )

    IsHealingWishOrLunarDance = Symbol(
        [0x14D58],
        [0x2014D58],
        None,
        (
            "Checks if a move ID is MOVE_HEALING_WISH or MOVE_LUNAR_DANCE.\n\nr0: move"
            " ID\nreturn: bool"
        ),
    )

    IsCopyingMove = Symbol(
        [0x14D84],
        [0x2014D84],
        None,
        (
            "Checks if a move ID is MOVE_MIMIC, MOVE_SKETCH, or MOVE_COPYCAT.\n\nr0:"
            " move ID\nreturn: bool"
        ),
    )

    IsTrappingMove = Symbol(
        [0x14DBC],
        [0x2014DBC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    IsOneHitKoMove = Symbol(
        [0x14E00],
        [0x2014E00],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    IsNot2TurnsMoveOrSketch = Symbol(
        [0x14E38],
        [0x2014E38],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    IsRealMove = Symbol(
        [0x14E64],
        [0x2014E64],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    IsMovesetValid = Symbol(
        [0x14EF8],
        [0x2014EF8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_str\nreturn:"
            " bool"
        ),
    )

    IsRealMoveInTimeDarkness = Symbol(
        [0x14F64],
        [0x2014F64],
        None,
        (
            "Seed Flare isn't a real move in Time/Darkness\n\nNote: unverified, ported"
            " from Irdkwia's notes\n\nr0: move ID\nreturn: bool"
        ),
    )

    IsMovesetValidInTimeDarkness = Symbol(
        [0x15004],
        [0x2015004],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_str\nreturn:"
            " bool"
        ),
    )

    GetFirstNotRealMoveInTimeDarkness = Symbol(
        [0x15024],
        [0x2015024],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_str\nreturn:"
            " index"
        ),
    )

    IsSameMove = Symbol(
        [0x1514C],
        [0x201514C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_dun_str\nr1:"
            " move_data_dun_str\nreturn: bool"
        ),
    )

    GetMoveCategory = Symbol(
        [0x151C8],
        [0x20151C8],
        None,
        (
            "Gets a move's category (physical, special, status).\n\nr0: move"
            " ID\nreturn: move category enum"
        ),
    )

    GetPpIncrease = Symbol(
        [0x151E4],
        [0x20151E4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nr1: IQ"
            " skills bitvector\nreturn: PP increase"
        ),
    )

    OpenWaza = Symbol(
        [0x15294],
        [0x2015294],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: waza_id",
    )

    SelectWaza = Symbol(
        [0x152FC],
        [0x20152FC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: waza_id",
    )

    ManipBgmPlayback = Symbol(
        [0x18EA4],
        [0x2018EA4],
        None,
        (
            "Uncertain. More like bgm1&2 end\n\nNote: unverified, ported from Irdkwia's"
            " notes"
        ),
    )

    SoundDriverReset = Symbol(
        [0x190C8],
        [0x20190C8],
        None,
        "Uncertain.\n\nNote: unverified, ported from Irdkwia's notes",
    )

    LoadDseFile = Symbol(
        [0x1938C],
        [0x201938C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output] iovec\nr1:"
            " filename\nreturn: bytes read"
        ),
    )

    PlaySeLoad = Symbol(
        [0x19574], [0x2019574], None, "Note: unverified, ported from Irdkwia's notes"
    )

    PlayBgm = Symbol(
        [0x198B8], [0x20198B8], None, "Note: unverified, ported from Irdkwia's notes"
    )

    StopBgm = Symbol(
        [0x19B28], [0x2019B28], None, "Note: unverified, ported from Irdkwia's notes"
    )

    ChangeBgm = Symbol(
        [0x19C50], [0x2019C50], None, "Note: unverified, ported from Irdkwia's notes"
    )

    PlayBgm2 = Symbol(
        [0x19D84], [0x2019D84], None, "Note: unverified, ported from Irdkwia's notes"
    )

    StopBgm2 = Symbol(
        [0x19FE8], [0x2019FE8], None, "Note: unverified, ported from Irdkwia's notes"
    )

    ChangeBgm2 = Symbol(
        [0x1A0E8], [0x201A0E8], None, "Note: unverified, ported from Irdkwia's notes"
    )

    PlayME = Symbol(
        [0x1A1C8], [0x201A1C8], None, "Note: unverified, ported from Irdkwia's notes"
    )

    StopME = Symbol(
        [0x1A40C],
        [0x201A40C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: fade_out",
    )

    PlaySe = Symbol(
        [0x1A4FC], [0x201A4FC], None, "Note: unverified, ported from Irdkwia's notes"
    )

    PlaySeFullSpec = Symbol(
        [0x1A66C], [0x201A66C], None, "Note: unverified, ported from Irdkwia's notes"
    )

    SeChangeVolume = Symbol(
        [0x1A828], [0x201A828], None, "Note: unverified, ported from Irdkwia's notes"
    )

    SeChangePan = Symbol(
        [0x1A900], [0x201A900], None, "Note: unverified, ported from Irdkwia's notes"
    )

    StopSe = Symbol(
        [0x1A9E4], [0x201A9E4], None, "Note: unverified, ported from Irdkwia's notes"
    )

    DeleteWanTableEntry = Symbol(
        [0x1D1DC],
        [0x201D1DC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: wan_table_ptr\nr1:"
            " wan_id"
        ),
    )

    FindWanTableEntry = Symbol(
        [0x1D2D4],
        [0x201D2D4],
        None,
        (
            "Appears to search in the given table (in practice always seems to be"
            " LOADED_WAN_TABLE_PTR) for an entry with the given file name.\n\nr0: table"
            " pointer\nr1: file name\nreturn: index of the found file, if found, or -1"
            " if not found"
        ),
    )

    GetLoadedWanTableEntry = Symbol(
        [0x1D334],
        [0x201D334],
        None,
        (
            "wan_id = -1 if it is not loaded\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: wan_table_ptr\nr1: bin_file_id\nr2: file_id\nreturn: wan_id"
        ),
    )

    LoadWanTableEntry = Symbol(
        [0x1D3DC],
        [0x201D3DC],
        None,
        (
            "Appears to load data from the given file (in practice always seems to be"
            " animation data), using previously loaded data in the given table (see"
            " FindWanTableEntry) if possible.\n\nr0: table pointer\nr1: file name\nr2:"
            " flags\nreturn: table index of the loaded data"
        ),
    )

    ReplaceWanFromBinFile = Symbol(
        [0x1D684],
        [0x201D684],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: wan_table_ptr\nr1:"
            " wan_id\nr2: bin_file_id\nr3: file_id\nstack[0]: compressed"
        ),
    )

    DeleteWanTableEntryVeneer = Symbol(
        [0x1D72C],
        [0x201D72C],
        None,
        (
            "Likely a linker-generated veneer for DeleteWanTableEntry.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " wan_table_ptr\nr1: wan_id"
        ),
    )

    LoadWteFromRom = Symbol(
        [0x1DE4C],
        [0x201DE4C],
        None,
        (
            "Loads a SIR0-wrapped WTE file from ROM, and returns a handle to it\n\nr0:"
            " [output] pointer to wte handle\nr1: file path string\nr2: load file flags"
        ),
    )

    LoadWteFromFileDirectory = Symbol(
        [0x1DEC4],
        [0x201DEC4],
        None,
        (
            "Loads a SIR0-wrapped WTE file from a file directory, and returns a handle"
            " to it\n\nr0: [output] pointer to wte handle\nr1: file directory id\nr2:"
            " file index\nr3: malloc flags"
        ),
    )

    UnloadWte = Symbol(
        [0x1DF18],
        [0x201DF18],
        None,
        (
            "Frees the buffer used to store the WTE data in the handle, and sets both"
            " pointers to null\n\nr0: pointer to wte handle"
        ),
    )

    LoadWtuFromBin = Symbol(
        [0x1DFB4],
        [0x201DFB4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: bin_file_id\nr1:"
            " file_id\nr2: load_type\nreturn: ?"
        ),
    )

    ProcessWte = Symbol(
        [0x1E0B0],
        [0x201E0B0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: header_ptr\nr1:"
            " unk_pal\nr2: unk_tex\nr3: unk_tex_param"
        ),
    )

    HandleSir0Translation = Symbol(
        [0x1F4B4],
        [0x201F4B4],
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
        [0x1F534],
        [0x201F534],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: sir0_ptr",
    )

    HandleSir0TranslationVeneer = Symbol(
        [0x1F58C],
        [0x201F58C],
        None,
        (
            "Likely a linker-generated veneer for HandleSir0Translation.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " [output] double pointer to beginning of data\nr1: pointer to source file"
            " buffer\nreturn: return code"
        ),
    )

    DecompressAtNormalVeneer = Symbol(
        [0x1F5C0],
        [0x201F5C0],
        None,
        (
            "Likely a linker-generated veneer for DecompressAtNormal.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " addr_decomp\nr1: expected_size\nr2: AT pointer\nreturn: ?"
        ),
    )

    DecompressAtNormal = Symbol(
        [0x1F5CC],
        [0x201F5CC],
        None,
        (
            "Overwrites r3 probably passed to match DecompressAtHalf's"
            " definition.\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " addr_decomp\nr1: expected_size\nr2: AT pointer\nreturn: ?"
        ),
    )

    DecompressAtHalf = Symbol(
        [0x1FA10],
        [0x201FA10],
        None,
        (
            "Same as DecompressAtNormal, except it stores each nibble as a byte\nand"
            " adds the high nibble (r3).\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: addr_decomp\nr1: expected_size\nr2: AT pointer\nr3:"
            " high_nibble\nreturn: ?"
        ),
    )

    DecompressAtFromMemoryPointerVeneer = Symbol(
        [0x1FF4C],
        [0x201FF4C],
        None,
        (
            "Likely a linker-generated veneer for DecompressAtFromMemoryPointer.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " addr_decomp\nr1: expected_size\nr2: AT pointer\nreturn: ?"
        ),
    )

    DecompressAtFromMemoryPointer = Symbol(
        [0x1FF58],
        [0x201FF58],
        None,
        (
            "Overwrites r3 probably passed to match DecompressAtHalf's"
            " definition.\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " addr_decomp\nr1: expected_size\nr2: AT pointer\nreturn: ?"
        ),
    )

    WriteByteFromMemoryPointer = Symbol(
        [0x20470],
        [0x2020470],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: byte",
    )

    GetAtSize = Symbol(
        [0x204EC],
        [0x20204EC],
        None,
        (
            "Doesn't work for AT3PX and AT4PN\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: AT pointer\nr1: ?\nreturn: ?"
        ),
    )

    GetLanguageType = Symbol(
        [0x205A0],
        [0x20205A0],
        None,
        (
            "Gets the language type.\n\nThis is the value backing the special"
            " LANGUAGE_TYPE script variable.\n\nreturn: language type"
        ),
    )

    GetLanguage = Symbol(
        [0x205B0],
        [0x20205B0],
        None,
        (
            "Gets the single-byte language ID of the current program.\n\nThe language"
            " ID appears to be used to index some global tables.\n\nreturn: language ID"
        ),
    )

    StrcmpTag = Symbol(
        [0x208C8],
        [0x20208C8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: s1\nr1: s2\nreturn: bool",
    )

    StoiTag = Symbol(
        [0x2090C],
        [0x202090C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: s\nreturn: int",
    )

    AnalyzeText = Symbol(
        [0x20DC8],
        [0x2020DC8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nreturn: ?",
    )

    PreprocessString = Symbol(
        [0x223F0],
        [0x20223F0],
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
        [0x235B8],
        [0x20235B8],
        None,
        (
            "Calls PreprocessString after resolving the given message ID to a"
            " string.\n\nr0: [output] formatted string\nr1: maximum capacity of the"
            " output buffer\nr2: message ID\nr3: preprocessor flags\nstack[0]: pointer"
            " to preprocessor args"
        ),
    )

    InitPreprocessorArgs = Symbol(
        [0x23690],
        [0x2023690],
        None,
        "Initializes a struct preprocess_args.\n\nr0: preprocessor args pointer",
    )

    SetStringAccuracy = Symbol(
        [0x24360], [0x2024360], None, "Note: unverified, ported from Irdkwia's notes"
    )

    SetStringPower = Symbol(
        [0x24428], [0x2024428], None, "Note: unverified, ported from Irdkwia's notes"
    )

    SetQuestionMarks = Symbol(
        [0x250E4],
        [0x20250E4],
        None,
        (
            "Fills the buffer with the string '???'\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: buffer"
        ),
    )

    StrcpySimple = Symbol(
        [0x25100],
        [0x2025100],
        None,
        (
            "A simple implementation of the strcpy(3) C library function.\n\nThis"
            " function was probably manually implemented by the developers. See Strcpy"
            " for what's probably the real libc function.\n\nr0: dest\nr1: src"
        ),
    )

    StrncpySimple = Symbol(
        [0x2511C],
        [0x202511C],
        None,
        (
            "A simple implementation of the strncpy(3) C library function.\n\nThis"
            " function was probably manually implemented by the developers. See Strncpy"
            " for what's probably the real libc function.\n\nr0: dest\nr1: src\nr2: n"
        ),
    )

    StrncpySimpleNoPad = Symbol(
        [0x25170],
        [0x2025170],
        None,
        (
            "Similar to StrncpySimple, but does not zero-pad the end of dest beyond the"
            " null-terminator.\n\nr0: dest\nr1: src\nr2: n"
        ),
    )

    StrncmpSimple = Symbol(
        [0x251AC],
        [0x20251AC],
        None,
        (
            "A simple implementation of the strncmp(3) C library function.\n\nThis"
            " function was probably manually implemented by the developers. See Strncmp"
            " for what's probably the real libc function.\n\nr0: s1\nr1: s2\nr2:"
            " n\nreturn: comparison value"
        ),
    )

    StrncpySimpleNoPadSafe = Symbol(
        [0x251F4],
        [0x20251F4],
        None,
        (
            "Like StrncpySimpleNoPad, except there's a useless check on that each"
            " character is less than 0x100 (which is impossible for the result of a"
            " ldrb instruction).\n\nr0: dest\nr1: src\nr2: n"
        ),
    )

    SpecialStrcpy = Symbol(
        [0x25230],
        [0x2025230],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dst\nr1: src",
    )

    GetStringFromFile = Symbol(
        [0x25788],
        [0x2025788],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: Buffer\nr1: String ID",
    )

    LoadStringFile = Symbol(
        [0x25818],
        [0x2025818],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GetStringFromFileVeneer = Symbol(
        [0x258B8],
        [0x20258B8],
        None,
        (
            "Likely a linker-generated veneer for GetStringFromFile.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " Buffer\nr1: String ID"
        ),
    )

    StringFromMessageId = Symbol(
        [0x258C4],
        [0x20258C4],
        None,
        (
            "Gets the string corresponding to a given message ID.\n\nr0: message"
            " ID\nreturn: string from the string files with the given message ID"
        ),
    )

    CopyStringFromMessageId = Symbol(
        [0x2590C],
        [0x202590C],
        None,
        (
            "Gets the string corresponding to a given message ID and copies it to the"
            " buffer specified in r0.\n\nThis function won't write more than <buffer"
            " length> bytes.\n\nr0: Buffer\nr1: String ID\nr2: Buffer length"
        ),
    )

    LoadTblTalk = Symbol(
        [0x2593C],
        [0x202593C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GetTalkLine = Symbol(
        [0x2598C],
        [0x202598C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0:"
            " personality_index\nr1: group_id\nr2: restrictions\nreturn: ?"
        ),
    )

    SetScreenWindowsColor = Symbol(
        [0x27A68],
        [0x2027A68],
        None,
        (
            "Sets the palette of the frames of windows in the specified screen\n\nr0:"
            " palette index\nr1: is upper screen"
        ),
    )

    SetBothScreensWindowsColor = Symbol(
        [0x27A80],
        [0x2027A80],
        None,
        (
            "Sets the palette of the frames of windows in both screens\n\nr0: palette"
            " index"
        ),
    )

    GetDialogBoxField0xC = Symbol(
        [0x2833C],
        [0x202833C],
        None,
        (
            "Gets field_0xc from the dialog box of the given ID.\n\nr0:"
            " dbox_id\nreturn: field_0xc"
        ),
    )

    Arm9LoadUnkFieldNa0x2029EC8 = Symbol(
        [0x29EC8],
        [0x2029EC8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id",
    )

    Arm9StoreUnkFieldNa0x2029ED8 = Symbol(
        [0x29ED8],
        [0x2029ED8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nr1: value",
    )

    CreateNormalMenu = Symbol(
        [0x2B0EC],
        [0x202B0EC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0:"
            " layout_struct_ptr\nr1: menu_flags\nr2: additional_info_ptr\nr3:"
            " menu_struct_ptr\nstack[0]: option_id\nreturn: menu_id"
        ),
    )

    FreeNormalMenu = Symbol(
        [0x2B4C4],
        [0x202B4C4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id",
    )

    IsNormalMenuActive = Symbol(
        [0x2B4F0],
        [0x202B4F0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id\nreturn: bool",
    )

    GetNormalMenuResult = Symbol(
        [0x2B57C],
        [0x202B57C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id\nreturn: ?",
    )

    CreateAdvancedMenu = Symbol(
        [0x2BA20],
        [0x202BA20],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0:"
            " layout_struct_ptr\nr1: menu_flags\nr2: additional_info_ptr\nr3:"
            " entry_function\nstack[0]: nb_options\nstack[1]: nb_opt_pp\nreturn:"
            " menu_id"
        ),
    )

    FreeAdvancedMenu = Symbol(
        [0x2BC44],
        [0x202BC44],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id",
    )

    IsAdvancedMenuActive = Symbol(
        [0x2BCDC],
        [0x202BCDC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id\nreturn: bool",
    )

    GetAdvancedMenuCurrentOption = Symbol(
        [0x2BCFC],
        [0x202BCFC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id\nreturn: ?",
    )

    GetAdvancedMenuResult = Symbol(
        [0x2BD10],
        [0x202BD10],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id\nreturn: ?",
    )

    CreateDBox = Symbol(
        [0x2F0B0],
        [0x202F0B0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0:"
            " layout_struct_ptr\nreturn: dbox_id"
        ),
    )

    FreeDBox = Symbol(
        [0x2F148],
        [0x202F148],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id",
    )

    IsDBoxActive = Symbol(
        [0x2F180],
        [0x202F180],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id\nreturn: bool",
    )

    ShowMessageInDBox = Symbol(
        [0x2F1B4],
        [0x202F1B4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id\nr1:"
            " preprocessor flags (see PreprocessString)\nr2: string_id\nr3: pointer to"
            " preprocessor args (see PreprocessString)"
        ),
    )

    ShowDBox = Symbol(
        [0x2F3A4],
        [0x202F3A4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id",
    )

    CreatePortraitBox = Symbol(
        [0x2F5AC],
        [0x202F5AC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ???\nr1: ???\nr2:"
            " ???\nreturn: dbox_id"
        ),
    )

    FreePortraitBox = Symbol(
        [0x2F650],
        [0x202F650],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id",
    )

    ShowPortraitBox = Symbol(
        [0x2F690],
        [0x202F690],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id\nr1:"
            " portrait_ptr"
        ),
    )

    HidePortraitBox = Symbol(
        [0x2F6DC],
        [0x202F6DC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id",
    )

    IsMenuOptionActive = Symbol(
        [0x32474],
        [0x2032474],
        None,
        (
            "Called whenever a menu option is selected. Returns whether the option is"
            " active or not.\n\nr0: ?\nReturn: True if the menu option is enabled,"
            " false otherwise."
        ),
    )

    ShowKeyboard = Symbol(
        [0x367F0],
        [0x20367F0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: MessageID\nr1:"
            " buffer1\nr2: ???\nr3: buffer2\nreturn: ?"
        ),
    )

    GetKeyboardStatus = Symbol(
        [0x36CD4],
        [0x2036CD4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    GetKeyboardStringResult = Symbol(
        [0x3755C],
        [0x203755C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    PrintMoveOptionMenu = Symbol(
        [0x402C0],
        [0x20402C0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    PrintIqSkillsMenu = Symbol(
        [0x41A40],
        [0x2041A40],
        None,
        (
            "Draws the IQ skills menu for a certain monster.\n\nr0: Monster"
            " species\nr1: Pointer to bitarray where the enabled skills will be written"
            " when enabling or disabling them in the menu\nr2: Monster IQ\nr3: True if"
            " the monster is blinded"
        ),
    )

    GetNotifyNote = Symbol(
        [0x484A0],
        [0x20484A0],
        None,
        "Returns the current value of NOTIFY_NOTE.\n\nreturn: bool",
    )

    SetNotifyNote = Symbol(
        [0x484B0], [0x20484B0], None, "Sets NOTIFY_NOTE to the given value.\n\nr0: bool"
    )

    InitMainTeamAfterQuiz = Symbol(
        [0x487C4],
        [0x20487C4],
        None,
        (
            "Implements SPECIAL_PROC_INIT_MAIN_TEAM_AFTER_QUIZ (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    ScriptSpecialProcess0x3 = Symbol(
        [0x48A0C],
        [0x2048A0C],
        None,
        "Implements SPECIAL_PROC_0x3 (see ScriptSpecialProcessCall).\n\nNo params.",
    )

    ScriptSpecialProcess0x4 = Symbol(
        [0x48A84],
        [0x2048A84],
        None,
        "Implements SPECIAL_PROC_0x4 (see ScriptSpecialProcessCall).\n\nNo params.",
    )

    ReadStringSave = Symbol(
        [0x48BB4],
        [0x2048BB4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer",
    )

    CheckStringSave = Symbol(
        [0x48BD0],
        [0x2048BD0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nreturn: bool",
    )

    WriteSaveFile = Symbol(
        [0x48E74],
        [0x2048E74],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: save_info\nr1:"
            " buffer\nr2: size\nreturn: status code"
        ),
    )

    ReadSaveFile = Symbol(
        [0x48ED0],
        [0x2048ED0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: save_info\nr1:"
            " buffer\nr2: size\nreturn: status code"
        ),
    )

    CalcChecksum = Symbol(
        [0x48F24],
        [0x2048F24],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nr1: size",
    )

    CheckChecksum = Symbol(
        [0x48F4C],
        [0x2048F4C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nr1:"
            " size\nreturn: check_ok"
        ),
    )

    NoteSaveBase = Symbol(
        [0x48F84],
        [0x2048F84],
        None,
        (
            "Probably related to saving or quicksaving?\n\nThis function prints the"
            " debug message 'NoteSave Base %d %d' with some values. It's also the only"
            " place where GetRngSeed is called.\n\nr0: Irdkwia's notes: state"
            " ID\nothers: ?\nreturn: status code"
        ),
    )

    WriteQuickSaveInfo = Symbol(
        [0x49248],
        [0x2049248],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nr1: size",
    )

    ReadSaveHeader = Symbol(
        [0x4926C], [0x204926C], None, "Note: unverified, ported from Irdkwia's notes"
    )

    NoteLoadBase = Symbol(
        [0x49370],
        [0x2049370],
        None,
        (
            "Probably related to loading a save file or quicksave?\n\nThis function"
            " prints the debug message 'NoteLoad Base %d' with some value. It's also"
            " the only place where SetRngSeed is called.\n\nreturn: status code"
        ),
    )

    ReadQuickSaveInfo = Symbol(
        [0x49628],
        [0x2049628],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nr1:"
            " size\nreturn: status code"
        ),
    )

    GetGameMode = Symbol(
        [0x4AFC0],
        [0x204AFC0],
        None,
        "Gets the value of GAME_MODE.\n\nreturn: game mode",
    )

    InitScriptVariableValues = Symbol(
        [0x4B04C],
        [0x204B04C],
        None,
        (
            "Initialize the script variable values table (SCRIPT_VARS_VALUES).\n\nThe"
            " whole table is first zero-initialized. Then, all script variable values"
            " are first initialized to their defaults, after which some of them are"
            " overwritten with other hard-coded values.\n\nNo params."
        ),
    )

    InitEventFlagScriptVars = Symbol(
        [0x4B304],
        [0x204B304],
        None,
        (
            "Initializes an assortment of event flag script variables (see the code for"
            " an exhaustive list).\n\nNo params."
        ),
    )

    ZinitScriptVariable = Symbol(
        [0x4B434],
        [0x204B434],
        None,
        (
            "Zero-initialize the values of the given script variable.\n\nr0: pointer to"
            " the local variable table (only needed if id >= VAR_LOCAL0)\nr1: script"
            " variable ID"
        ),
    )

    LoadScriptVariableRaw = Symbol(
        [0x4B49C],
        [0x204B49C],
        None,
        (
            "Loads a script variable descriptor for a given ID.\n\nr0: [output] script"
            " variable descriptor pointer\nr1: pointer to the local variable table"
            " (doesn't need to be valid; just controls the output value pointer)\nr2:"
            " script variable ID"
        ),
    )

    LoadScriptVariableValue = Symbol(
        [0x4B4EC],
        [0x204B4EC],
        None,
        (
            "Loads the value of a script variable.\n\nr0: pointer to the local variable"
            " table (only needed if id >= VAR_LOCAL0)\nr1: script variable ID\nreturn:"
            " value"
        ),
    )

    LoadScriptVariableValueAtIndex = Symbol(
        [0x4B678],
        [0x204B678],
        None,
        (
            "Loads the value of a script variable at some index (for script variables"
            " that are arrays).\n\nr0: pointer to the local variable table (only needed"
            " if id >= VAR_LOCAL0)\nr1: script variable ID\nr2: value index for the"
            " given script var\nreturn: value"
        ),
    )

    SaveScriptVariableValue = Symbol(
        [0x4B820],
        [0x204B820],
        None,
        (
            "Saves the given value to a script variable.\n\nr0: pointer to local"
            " variable table (only needed if id >= VAR_LOCAL0)\nr1: script variable"
            " ID\nr2: value to save"
        ),
    )

    SaveScriptVariableValueAtIndex = Symbol(
        [0x4B988],
        [0x204B988],
        None,
        (
            "Saves the given value to a script variable at some index (for script"
            " variables that are arrays).\n\nr0: pointer to local variable table (only"
            " needed if id >= VAR_LOCAL0)\nr1: script variable ID\nr2: value index for"
            " the given script var\nr3: value to save"
        ),
    )

    LoadScriptVariableValueSum = Symbol(
        [0x4BB00],
        [0x204BB00],
        None,
        (
            "Loads the sum of all values of a given script variable (for script"
            " variables that are arrays).\n\nr0: pointer to the local variable table"
            " (only needed if id >= VAR_LOCAL0)\nr1: script variable ID\nreturn: sum of"
            " values"
        ),
    )

    LoadScriptVariableValueBytes = Symbol(
        [0x4BB64],
        [0x204BB64],
        None,
        (
            "Loads some number of bytes from the value of a given script"
            " variable.\n\nr0: script variable ID\nr1: [output] script variable value"
            " bytes\nr2: number of bytes to load"
        ),
    )

    SaveScriptVariableValueBytes = Symbol(
        [0x4BBCC],
        [0x204BBCC],
        None,
        (
            "Saves some number of bytes to the given script variable.\n\nr0: script"
            " variable ID\nr1: bytes to save\nr2: number of bytes"
        ),
    )

    ScriptVariablesEqual = Symbol(
        [0x4BC18],
        [0x204BC18],
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
        [0x4C1E4],
        [0x204C1E4],
        None,
        (
            "Saves event flag script variables (see the code for an exhaustive list) to"
            " their respective BACKUP script variables, but only in certain game"
            " modes.\n\nThis function prints the debug string 'EventFlag BackupGameMode"
            " %d' with the game mode.\n\nNo params."
        ),
    )

    DumpScriptVariableValues = Symbol(
        [0x4C408],
        [0x204C408],
        None,
        (
            "Runs EventFlagBackup, then copies the script variable values table"
            " (SCRIPT_VARS_VALUES) to the given pointer.\n\nr0: destination pointer for"
            " the data dump\nreturn: always 1"
        ),
    )

    RestoreScriptVariableValues = Symbol(
        [0x4C430],
        [0x204C430],
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
        [0x4C488],
        [0x204C488],
        None,
        (
            "Initializes most of the SCENARIO_* script variables (except"
            " SCENARIO_TALK_BIT_FLAG for some reason). Also initializes the"
            " PLAY_OLD_GAME variable.\n\nNo params."
        ),
    )

    SetScenarioScriptVar = Symbol(
        [0x4C618],
        [0x204C618],
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
        [0x4C8EC],
        [0x204C8EC],
        None,
        (
            "Gets the special episode type from the SPECIAL_EPISODE_TYPE script"
            " variable.\n\nreturn: special episode type"
        ),
    )

    HasPlayedOldGame = Symbol(
        [0x4CA70],
        [0x204CA70],
        None,
        "Returns the value of the VAR_PLAY_OLD_GAME script variable.\n\nreturn: bool",
    )

    GetPerformanceFlagWithChecks = Symbol(
        [0x4CA94],
        [0x204CA94],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: flag_id\nreturn: ?",
    )

    GetScenarioBalance = Symbol(
        [0x4CB94],
        [0x204CB94],
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
        [0x4CCB8],
        [0x204CCB8],
        None,
        (
            "Saves scenario flag script variables (SCENARIO_SELECT,"
            " SCENARIO_MAIN_BIT_FLAG) to their respective BACKUP script variables, but"
            " only in certain game modes.\n\nThis function prints the debug string"
            " 'ScenarioFlag BackupGameMode %d' with the game mode.\n\nNo params."
        ),
    )

    InitWorldMapScriptVars = Symbol(
        [0x4CD88],
        [0x204CD88],
        None,
        (
            "Initializes the WORLD_MAP_* script variable values (IDs 0x55-0x57).\n\nNo"
            " params."
        ),
    )

    InitDungeonListScriptVars = Symbol(
        [0x4CE90],
        [0x204CE90],
        None,
        (
            "Initializes the DUNGEON_*_LIST script variable values (IDs"
            " 0x4f-0x54).\n\nNo params."
        ),
    )

    SetDungeonConquest = Symbol(
        [0x4CF38],
        [0x204CF38],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nr1:"
            " bit_value"
        ),
    )

    CheckDungeonOpen = Symbol(
        [0x4CF9C],
        [0x204CF9C],
        None,
        (
            "Related to dungeon open list\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: dungeon ID\nreturn: status code?"
        ),
    )

    GlobalProgressAlloc = Symbol(
        [0x4D108],
        [0x204D108],
        None,
        (
            "Allocates a new global progress struct.\n\nThis updates the global pointer"
            " and returns a copy of that pointer.\n\nreturn: pointer to a newly"
            " allocated global progress struct"
        ),
    )

    ResetGlobalProgress = Symbol(
        [0x4D130],
        [0x204D130],
        None,
        "Zero-initializes the global progress struct.\n\nNo params.",
    )

    SetMonsterFlag1 = Symbol(
        [0x4D14C],
        [0x204D14C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID",
    )

    GetMonsterFlag1 = Symbol(
        [0x4D188],
        [0x204D188],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn: ?",
    )

    SetMonsterFlag2 = Symbol(
        [0x4D1C4],
        [0x204D1C4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID",
    )

    HasMonsterBeenAttackedInDungeons = Symbol(
        [0x4D208],
        [0x204D208],
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
        [0x4D250],
        [0x204D250],
        None,
        "Marks a dungeon tip as already shown to the player\n\nr0: Dungeon tip ID",
    )

    GetDungeonTipShown = Symbol(
        [0x4D290],
        [0x204D290],
        None,
        (
            "Checks if a dungeon tip has already been shown before or not.\n\nr0:"
            " Dungeon tip ID\nreturn: True if the tip has been shown before, false"
            " otherwise."
        ),
    )

    SetMaxReachedFloor = Symbol(
        [0x4D2DC],
        [0x204D2DC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nr1: max"
            " floor"
        ),
    )

    GetMaxReachedFloor = Symbol(
        [0x4D2F8],
        [0x204D2F8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn:"
            " max floor"
        ),
    )

    IncrementNbAdventures = Symbol(
        [0x4D318],
        [0x204D318],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GetNbAdventures = Symbol(
        [0x4D34C],
        [0x204D34C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: # adventures",
    )

    CanMonsterSpawn = Symbol(
        [0x4D360],
        [0x204D360],
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
        [0x4D368],
        [0x204D368],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID",
    )

    CopyProgressInfoTo = Symbol(
        [0x4D3C0],
        [0x204D3C0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: write_info\nothers: ?",
    )

    CopyProgressInfoFromScratchTo = Symbol(
        [0x4D548],
        [0x204D548],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: start_address\nr1:"
            " total_length\nreturn: ?"
        ),
    )

    CopyProgressInfoFrom = Symbol(
        [0x4D580],
        [0x204D580],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info",
    )

    CopyProgressInfoFromScratchFrom = Symbol(
        [0x4D748],
        [0x204D748],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: start_address\nr1:"
            " total_length"
        ),
    )

    SetPortraitMonsterId = Symbol(
        [0x4D7D4],
        [0x204D7D4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: portrait_ptr\nr1:"
            " monster ID"
        ),
    )

    SetPortraitExpressionId = Symbol(
        [0x4D7F4],
        [0x204D7F4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: portrait_ptr\nr1:"
            " expression_id"
        ),
    )

    SetPortraitUnknownAttr = Symbol(
        [0x4D804],
        [0x204D804],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: portrait_ptr\nr1: attr",
    )

    SetPortraitAttrStruct = Symbol(
        [0x4D848],
        [0x204D848],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: portrait_ptr\nr1:"
            " attr_ptr"
        ),
    )

    LoadPortrait = Symbol(
        [0x4D8BC],
        [0x204D8BC],
        None,
        (
            "If buffer_portrait is null, it only checks if it exists\n\nNote:"
            " unverified, ported from Irdkwia's notes\n\nr0: portrait_ptr\nr1:"
            " buffer_portrait\nreturn: exists"
        ),
    )

    GetNbFloors = Symbol(
        [0x4F57C],
        [0x204F57C],
        None,
        (
            "Returns the number of floors of the given dungeon.\n\nThe result is"
            " hardcoded for certain dungeons, such as dojo mazes.\n\nr0: Dungeon"
            " ID\nreturn: Number of floors"
        ),
    )

    GetNbFloorsPlusOne = Symbol(
        [0x4F5B4],
        [0x204F5B4],
        None,
        (
            "Returns the number of floors of the given dungeon + 1.\n\nr0: Dungeon"
            " ID\nreturn: Number of floors + 1"
        ),
    )

    GetDungeonGroup = Symbol(
        [0x4F5C8],
        [0x204F5C8],
        None,
        (
            "Returns the dungeon group associated to the given dungeon.\n\nFor IDs"
            " greater or equal to dungeon_id::DUNGEON_NORMAL_FLY_MAZE, returns"
            " dungeon_group_id::DGROUP_MAROWAK_DOJO.\n\nr0: Dungeon ID\nreturn:"
            " Group ID"
        ),
    )

    GetNbPrecedingFloors = Symbol(
        [0x4F5E0],
        [0x204F5E0],
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
        [0x4F5F8],
        [0x204F5F8],
        None,
        (
            "Returns the total amount of floors among all the dungeons in the dungeon"
            " group of the specified dungeon.\n\nr0: Dungeon ID\nreturn: Total number"
            " of floors in the group of the specified dungeon"
        ),
    )

    DungeonFloorToGroupFloor = Symbol(
        [0x4F64C],
        [0x204F64C],
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
        [0x4F958], [0x204F958], None, "Note: unverified, ported from Irdkwia's notes"
    )

    SetAdventureLogStructLocation = Symbol(
        [0x4FA24],
        [0x204FA24],
        None,
        (
            "Sets the location of the adventure log struct in memory.\n\nSets it in a"
            " static memory location (At 0x22AB69C [US], 0x22ABFDC [EU], 0x22ACE58"
            " [JP])\n\nNo params."
        ),
    )

    SetAdventureLogDungeonFloor = Symbol(
        [0x4FA3C],
        [0x204FA3C],
        None,
        "Sets the current dungeon floor pair.\n\nr0: struct dungeon_floor_pair",
    )

    GetAdventureLogDungeonFloor = Symbol(
        [0x4FA5C],
        [0x204FA5C],
        None,
        "Gets the current dungeon floor pair.\n\nreturn: struct dungeon_floor_pair",
    )

    ClearAdventureLogStruct = Symbol(
        [0x4FA70],
        [0x204FA70],
        None,
        "Clears the adventure log structure.\n\nNo params.",
    )

    SetAdventureLogCompleted = Symbol(
        [0x4FB9C],
        [0x204FB9C],
        None,
        "Marks one of the adventure log entry as completed.\n\nr0: entry ID",
    )

    IsAdventureLogNotEmpty = Symbol(
        [0x4FBC4],
        [0x204FBC4],
        None,
        (
            "Checks if at least one of the adventure log entries is"
            " completed.\n\nreturn: bool"
        ),
    )

    GetAdventureLogCompleted = Symbol(
        [0x4FBFC],
        [0x204FBFC],
        None,
        "Checks if one adventure log entry is completed.\n\nr0: entry ID\nreturn: bool",
    )

    IncrementNbDungeonsCleared = Symbol(
        [0x4FC28],
        [0x204FC28],
        None,
        (
            "Increments by 1 the number of dungeons cleared.\n\nImplements"
            " SPECIAL_PROC_0x3A (see ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    GetNbDungeonsCleared = Symbol(
        [0x4FC6C],
        [0x204FC6C],
        None,
        (
            "Gets the number of dungeons cleared.\n\nreturn: the number of dungeons"
            " cleared"
        ),
    )

    IncrementNbFriendRescues = Symbol(
        [0x4FC80],
        [0x204FC80],
        None,
        "Increments by 1 the number of successful friend rescues.\n\nNo params.",
    )

    GetNbFriendRescues = Symbol(
        [0x4FCC8],
        [0x204FCC8],
        None,
        (
            "Gets the number of successful friend rescues.\n\nreturn: the number of"
            " successful friend rescues"
        ),
    )

    IncrementNbEvolutions = Symbol(
        [0x4FCDC],
        [0x204FCDC],
        None,
        "Increments by 1 the number of evolutions.\n\nNo params.",
    )

    GetNbEvolutions = Symbol(
        [0x4FD24],
        [0x204FD24],
        None,
        "Gets the number of evolutions.\n\nreturn: the number of evolutions",
    )

    IncrementNbSteals = Symbol(
        [0x4FD38],
        [0x204FD38],
        None,
        (
            "Leftover from Time & Darkness. Does not do anything.\n\nCalls to this"
            " matches the ones for incrementing the number of successful steals in Time"
            " & Darkness.\n\nNo params."
        ),
    )

    IncrementNbEggsHatched = Symbol(
        [0x4FD3C],
        [0x204FD3C],
        None,
        "Increments by 1 the number of eggs hatched.\n\nNo params.",
    )

    GetNbEggsHatched = Symbol(
        [0x4FD78],
        [0x204FD78],
        None,
        "Gets the number of eggs hatched.\n\nreturn: the number of eggs hatched",
    )

    GetNbPokemonJoined = Symbol(
        [0x4FD8C],
        [0x204FD8C],
        None,
        (
            "Gets the number of different pokémon that joined.\n\nreturn: the number of"
            " different pokémon that joined"
        ),
    )

    GetNbMovesLearned = Symbol(
        [0x4FDA0],
        [0x204FDA0],
        None,
        (
            "Gets the number of different moves learned.\n\nreturn: the number of"
            " different moves learned"
        ),
    )

    SetVictoriesOnOneFloor = Symbol(
        [0x4FDB4],
        [0x204FDB4],
        None,
        "Sets the record of victories on one floor.\n\nr0: the new record of victories",
    )

    GetVictoriesOnOneFloor = Symbol(
        [0x4FDE8],
        [0x204FDE8],
        None,
        "Gets the record of victories on one floor.\n\nreturn: the record of victories",
    )

    SetPokemonJoined = Symbol(
        [0x4FDFC], [0x204FDFC], None, "Marks one pokémon as joined.\n\nr0: monster ID"
    )

    SetPokemonBattled = Symbol(
        [0x4FE58], [0x204FE58], None, "Marks one pokémon as battled.\n\nr0: monster ID"
    )

    GetNbPokemonBattled = Symbol(
        [0x4FEB4],
        [0x204FEB4],
        None,
        (
            "Gets the number of different pokémon that battled against you.\n\nreturn:"
            " the number of different pokémon that battled against you"
        ),
    )

    IncrementNbBigTreasureWins = Symbol(
        [0x4FEC8],
        [0x204FEC8],
        None,
        (
            "Increments by 1 the number of big treasure wins.\n\nImplements"
            " SPECIAL_PROC_0x3B (see ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    SetNbBigTreasureWins = Symbol(
        [0x4FEE8],
        [0x204FEE8],
        None,
        (
            "Sets the number of big treasure wins.\n\nr0: the new number of big"
            " treasure wins"
        ),
    )

    GetNbBigTreasureWins = Symbol(
        [0x4FF20],
        [0x204FF20],
        None,
        (
            "Gets the number of big treasure wins.\n\nreturn: the number of big"
            " treasure wins"
        ),
    )

    SetNbRecycled = Symbol(
        [0x4FF34],
        [0x204FF34],
        None,
        "Sets the number of items recycled.\n\nr0: the new number of items recycled",
    )

    GetNbRecycled = Symbol(
        [0x4FF6C],
        [0x204FF6C],
        None,
        "Gets the number of items recycled.\n\nreturn: the number of items recycled",
    )

    IncrementNbSkyGiftsSent = Symbol(
        [0x4FF80],
        [0x204FF80],
        None,
        (
            "Increments by 1 the number of sky gifts sent.\n\nImplements"
            " SPECIAL_PROC_SEND_SKY_GIFT_TO_GUILDMASTER (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    SetNbSkyGiftsSent = Symbol(
        [0x4FFA0],
        [0x204FFA0],
        None,
        "Sets the number of Sky Gifts sent.\n\nreturn: the number of Sky Gifts sent",
    )

    GetNbSkyGiftsSent = Symbol(
        [0x4FFD8],
        [0x204FFD8],
        None,
        "Gets the number of Sky Gifts sent.\n\nreturn: the number of Sky Gifts sent",
    )

    ComputeSpecialCounters = Symbol(
        [0x4FFEC],
        [0x204FFEC],
        None,
        (
            "Computes the counters from the bit fields in the adventure log, as they"
            " are not updated automatically when bit fields are altered.\n\nAffects"
            " GetNbPokemonJoined, GetNbMovesLearned, GetNbPokemonBattled and"
            " GetNbItemAcquired.\n\nNo params."
        ),
    )

    RecruitSpecialPokemonLog = Symbol(
        [0x50244],
        [0x2050244],
        None,
        (
            "Marks a specified special pokémon as recruited in the adventure"
            " log.\n\nIrdkwia's notes: Useless in Sky\n\nr0: monster ID"
        ),
    )

    IncrementNbFainted = Symbol(
        [0x502B0],
        [0x20502B0],
        None,
        "Increments by 1 the number of times you fainted.\n\nNo params.",
    )

    GetNbFainted = Symbol(
        [0x502EC],
        [0x20502EC],
        None,
        (
            "Gets the number of times you fainted.\n\nreturn: the number of times you"
            " fainted"
        ),
    )

    SetItemAcquired = Symbol(
        [0x50300], [0x2050300], None, "Marks one specific item as acquired.\n\nr0: item"
    )

    GetNbItemAcquired = Symbol(
        [0x503CC],
        [0x20503CC],
        None,
        "Gets the number of items acquired.\n\nreturn: the number of items acquired",
    )

    SetChallengeLetterCleared = Symbol(
        [0x50420],
        [0x2050420],
        None,
        "Sets a challenge letter as cleared.\n\nr0: challenge ID",
    )

    GetSentryDutyGamePoints = Symbol(
        [0x504A4],
        [0x20504A4],
        None,
        (
            "Gets the points for the associated rank in the footprints minigame.\n\nr0:"
            " the rank (range 0-4, 1st to 5th)\nreturn: points"
        ),
    )

    SetSentryDutyGamePoints = Symbol(
        [0x504BC],
        [0x20504BC],
        None,
        (
            "Sets a new record in the footprints minigame.\n\nr0: points\nreturn: the"
            " rank (range 0-4, 1st to 5th; -1 if out of ranking)"
        ),
    )

    CopyLogTo = Symbol(
        [0x5054C],
        [0x205054C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: write_info",
    )

    CopyLogFrom = Symbol(
        [0x50738],
        [0x2050738],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info",
    )

    GetAbilityString = Symbol(
        [0x5091C],
        [0x205091C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nr1: ability ID",
    )

    GetAbilityDescStringId = Symbol(
        [0x5093C],
        [0x205093C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ability ID\nreturn:"
            " string ID"
        ),
    )

    GetTypeStringId = Symbol(
        [0x50950],
        [0x2050950],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: type ID\nreturn:"
            " string ID"
        ),
    )

    CopyBitsTo = Symbol(
        [0x509C0],
        [0x20509C0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: write_info\nr1:"
            " buffer_write\nr2: nb_bits"
        ),
    )

    CopyBitsFrom = Symbol(
        [0x50A40],
        [0x2050A40],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info\nr1:"
            " buffer_read\nr2: nb_bits"
        ),
    )

    StoreDefaultTeamName = Symbol(
        [0x50ACC],
        [0x2050ACC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GetTeamNameCheck = Symbol(
        [0x50B10],
        [0x2050B10],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer",
    )

    GetTeamName = Symbol(
        [0x50B7C],
        [0x2050B7C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer",
    )

    SetTeamName = Symbol(
        [0x50B94],
        [0x2050B94],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer",
    )

    SubFixedPoint = Symbol(
        [0x50F10],
        [0x2050F10],
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
        [0x51020],
        [0x2051020],
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
        [0x51064],
        [0x2051064],
        None,
        (
            "Compute the ceiling of a decimal fixed-point number (16 fraction"
            " bits).\n\nNumbers are in the format {16-bit integer part, 16-bit"
            " thousandths}, where the integer part is the lower word. Probably used"
            " primarily for belly.\n\nr0: number\nreturn: ceil(number)"
        ),
    )

    DungeonGoesUp = Symbol(
        [0x51288],
        [0x2051288],
        None,
        (
            "Returns whether the specified dungeon is considered as going upward or"
            " not\n\nr0: dungeon id\nreturn: bool"
        ),
    )

    GetTurnLimit = Symbol(
        [0x512B0],
        [0x20512B0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn:"
            " turn limit"
        ),
    )

    DoesNotSaveWhenEntering = Symbol(
        [0x512C8],
        [0x20512C8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    TreasureBoxDropsEnabled = Symbol(
        [0x512F0],
        [0x20512F0],
        None,
        (
            "Checks if enemy Treasure Box drops are enabled in the dungeon.\n\nr0:"
            " dungeon ID\nreturn: bool"
        ),
    )

    IsLevelResetDungeon = Symbol(
        [0x51318],
        [0x2051318],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    GetMaxItemsAllowed = Symbol(
        [0x51340],
        [0x2051340],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn:"
            " max items allowed"
        ),
    )

    IsMoneyAllowed = Symbol(
        [0x51358],
        [0x2051358],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    GetMaxRescueAttempts = Symbol(
        [0x51380],
        [0x2051380],
        None,
        (
            "Returns the maximum rescue attempts allowed in the specified"
            " dungeon.\n\nr0: dungeon id\nreturn: Max rescue attempts, or -1 if rescues"
            " are disabled."
        ),
    )

    IsRecruitingAllowed = Symbol(
        [0x51398],
        [0x2051398],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    GetLeaderChangeFlag = Symbol(
        [0x513C0],
        [0x20513C0],
        None,
        (
            "Returns true if the flag that allows changing leaders is set in the"
            " restrictions of the specified dungeon\n\nr0: dungeon id\nreturn: True if"
            " the restrictions of the current dungeon allow changing leaders, false"
            " otherwise."
        ),
    )

    GetUnknownDungeonOption = Symbol(
        [0x513E8],
        [0x20513E8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: ?",
    )

    CanEnemyEvolve = Symbol(
        [0x51400],
        [0x2051400],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    GetMaxMembersAllowed = Symbol(
        [0x51428],
        [0x2051428],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn:"
            " max members allowed"
        ),
    )

    IsIqEnabled = Symbol(
        [0x51440],
        [0x2051440],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    IsTrapInvisibleWhenAttacking = Symbol(
        [0x51468],
        [0x2051468],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    JoinedAtRangeCheck = Symbol(
        [0x51490],
        [0x2051490],
        None,
        (
            "Returns whether a certain joined_at field value is between"
            " dungeon_id::DUNGEON_JOINED_AT_BIDOOF and"
            " dungeon_id::DUNGEON_DUMMY_0xE3.\n\nIrdkwia's notes:"
            " IsSupportPokemon\n\nr0: joined_at id\nreturn: bool"
        ),
    )

    IsDojoDungeon = Symbol(
        [0x514B0],
        [0x20514B0],
        None,
        (
            "Checks if the given dungeon is a Marowak Dojo dungeon.\n\nr0: dungeon"
            " ID\nreturn: bool"
        ),
    )

    IsFutureDungeon = Symbol(
        [0x514CC],
        [0x20514CC],
        None,
        (
            "Checks if the given dungeon is a dungeon in the future arc of the main"
            " story.\n\nr0: dungeon ID\nreturn: bool"
        ),
    )

    IsSpecialEpisodeDungeon = Symbol(
        [0x514E8],
        [0x20514E8],
        None,
        (
            "Checks if the given dungeon is a special episode dungeon.\n\nr0: dungeon"
            " ID\nreturn: bool"
        ),
    )

    RetrieveFromItemList1 = Symbol(
        [0x51504],
        [0x2051504],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon_info\nr1:"
            " ?\nreturn: ?"
        ),
    )

    IsForbiddenFloor = Symbol(
        [0x51568],
        [0x2051568],
        None,
        (
            "Related to missions floors forbidden\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: dungeon_info\nothers: ?\nreturn: bool"
        ),
    )

    Copy16BitsFrom = Symbol(
        [0x515EC],
        [0x20515EC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info\nr1:"
            " buffer_read"
        ),
    )

    RetrieveFromItemList2 = Symbol(
        [0x5167C],
        [0x205167C],
        None,
        (
            "Same as RetrieveFromItemList1, except there is one more"
            " comparison\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " dungeon_info"
        ),
    )

    IsInvalidForMission = Symbol(
        [0x516DC],
        [0x20516DC],
        None,
        (
            "It's a guess\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " dungeon_id\nreturn: bool"
        ),
    )

    IsExpEnabledInDungeon = Symbol(
        [0x5171C],
        [0x205171C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon_id\nreturn: bool",
    )

    IsSkyExclusiveDungeon = Symbol(
        [0x51744],
        [0x2051744],
        None,
        (
            "Also the dungeons where Giratina has its Origin Form\n\nNote: unverified,"
            " ported from Irdkwia's notes\n\nr0: dungeon_id\nreturn: bool"
        ),
    )

    JoinedAtRangeCheck2 = Symbol(
        [0x51760],
        [0x2051760],
        None,
        (
            "Returns whether a certain joined_at field value is equal to"
            " dungeon_id::DUNGEON_BEACH or is between dungeon_id::DUNGEON_DUMMY_0xEC"
            " and dungeon_id::DUNGEON_DUMMY_0xF0.\n\nIrdkwia's notes:"
            " IsSEPokemon\n\nr0: joined_at id\nreturn: bool"
        ),
    )

    GetBagCapacity = Symbol(
        [0x517D4],
        [0x20517D4],
        None,
        (
            "Returns the player's bag capacity for a given point in the game.\n\nr0:"
            " scenario_balance\nreturn: bag capacity"
        ),
    )

    GetBagCapacitySpecialEpisode = Symbol(
        [0x517E4],
        [0x20517E4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: se_type\nreturn: bag"
            " capacity"
        ),
    )

    GetRankUpEntry = Symbol(
        [0x517F4],
        [0x20517F4],
        None,
        (
            "Gets the rank up data for the specified rank.\n\nr0: rank index\nreturn:"
            " struct rankup_table_entry*"
        ),
    )

    GetBgRegionArea = Symbol(
        [0x51E8C],
        [0x2051E8C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: offset\nr1:"
            " subregion_id\nr2: region_id\nreturn: ?"
        ),
    )

    LoadMonsterMd = Symbol(
        [0x52358],
        [0x2052358],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GetNameRaw = Symbol(
        [0x52394],
        [0x2052394],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dst_ptr\nr1: id",
    )

    GetName = Symbol(
        [0x523D0],
        [0x20523D0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dst_ptr\nr1: id\nr2:"
            " color_id"
        ),
    )

    GetNameWithGender = Symbol(
        [0x52440],
        [0x2052440],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dst_ptr\nr1: id\nr2:"
            " color_id"
        ),
    )

    GetSpeciesString = Symbol(
        [0x52500],
        [0x2052500],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dst_ptr\nr1: id",
    )

    GetNameString = Symbol(
        [0x526C8],
        [0x20526C8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: name",
    )

    GetSpriteIndex = Symbol(
        [0x526EC, 0x52708, 0x52724],
        [0x20526EC, 0x2052708, 0x2052724],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: sprite index",
    )

    GetDexNumber = Symbol(
        [0x52740],
        [0x2052740],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: dex number",
    )

    GetCategoryString = Symbol(
        [0x5275C],
        [0x205275C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: category",
    )

    GetMonsterGender = Symbol(
        [0x527A8],
        [0x20527A8],
        None,
        (
            "Returns the gender field of a monster given its ID.\n\nr0: monster"
            " id\nreturn: monster gender"
        ),
    )

    GetBodySize = Symbol(
        [0x527C4],
        [0x20527C4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: body size",
    )

    GetSpriteSize = Symbol(
        [0x527E0],
        [0x20527E0],
        None,
        (
            "Returns the sprite size of the specified monster. If the size is between 1"
            " and 6, 6 will be returned.\n\nr0: monster id\nreturn: sprite size"
        ),
    )

    GetSpriteFileSize = Symbol(
        [0x5281C],
        [0x205281C],
        None,
        (
            "Returns the sprite file size of the specified monster.\n\nr0: monster"
            " id\nreturn: sprite file size"
        ),
    )

    GetShadowSize = Symbol(
        [0x5283C],
        [0x205283C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: shadow size",
    )

    GetSpeedStatus = Symbol(
        [0x52858],
        [0x2052858],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: speed status",
    )

    GetMovementType = Symbol(
        [0x52874],
        [0x2052874],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: movement"
            " type"
        ),
    )

    GetRegenSpeed = Symbol(
        [0x52890],
        [0x2052890],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: regen speed",
    )

    GetCanMoveFlag = Symbol(
        [0x528B4],
        [0x20528B4],
        None,
        (
            "Returns the flag that determines if a monster can move in dungeons.\n\nr0:"
            " Monster ID\nreturn: 'Can move' flag"
        ),
    )

    GetChanceAsleep = Symbol(
        [0x528E0],
        [0x20528E0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: chance"
            " asleep"
        ),
    )

    GetLowKickMultiplier = Symbol(
        [0x528FC],
        [0x20528FC],
        None,
        (
            "Gets the Low Kick (and Grass Knot) damage multiplier (i.e., weight) for"
            " the given species.\n\nr0: monster ID\nreturn: multiplier as a binary"
            " fixed-point number with 8 fraction bits."
        ),
    )

    GetSize = Symbol(
        [0x52918],
        [0x2052918],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: size",
    )

    GetBaseHp = Symbol(
        [0x52934],
        [0x2052934],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: base HP",
    )

    CanThrowItems = Symbol(
        [0x52950],
        [0x2052950],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: bool",
    )

    CanEvolve = Symbol(
        [0x5297C],
        [0x205297C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: bool",
    )

    GetMonsterPreEvolution = Symbol(
        [0x529A8],
        [0x20529A8],
        None,
        (
            "Returns the pre-evolution id of a monster given its ID.\n\nr0: monster"
            " id\nreturn: ID of the monster that evolves into the one specified in r0"
        ),
    )

    GetBaseOffensiveStat = Symbol(
        [0x529C4],
        [0x20529C4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nr1: stat"
            " index\nreturn: base attack/special attack stat"
        ),
    )

    GetBaseDefensiveStat = Symbol(
        [0x529E4],
        [0x20529E4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nr1: stat"
            " index\nreturn: base defense/special defense stat"
        ),
    )

    GetType = Symbol(
        [0x52A04],
        [0x2052A04],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nr1: type index (0"
            " for primary type or 1 for secondary type)\nreturn: type"
        ),
    )

    GetAbility = Symbol(
        [0x52A24],
        [0x2052A24],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nr1: ability index"
            " (0 for primary ability or 1 for secondary ability)\nreturn: ability"
        ),
    )

    GetRecruitRate2 = Symbol(
        [0x52A44],
        [0x2052A44],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: recruit"
            " rate 2"
        ),
    )

    GetRecruitRate1 = Symbol(
        [0x52A60],
        [0x2052A60],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: recruit"
            " rate 1"
        ),
    )

    GetExp = Symbol(
        [0x52A7C],
        [0x2052A7C],
        None,
        (
            "Base Formula = ((Level-1)*ExpYield)//10+ExpYield\nNote: Defeating an enemy"
            " without using a move will divide this amount by 2\n\nNote: unverified,"
            " ported from Irdkwia's notes\n\nr0: id\nr1: level\nreturn: exp"
        ),
    )

    GetEvoParameters = Symbol(
        [0x52AB0],
        [0x2052AB0],
        None,
        (
            "Bx\nHas something to do with evolution\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: [output] struct_evo_param\nr1: id"
        ),
    )

    GetTreasureBoxChances = Symbol(
        [0x52AE0],
        [0x2052AE0],
        None,
        (
            "Has something to do with bytes 3C-3E\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: id\nr1: [output] struct_chances"
        ),
    )

    GetIqGroup = Symbol(
        [0x52B28],
        [0x2052B28],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: IQ group",
    )

    GetSpawnThreshold = Symbol(
        [0x52B44],
        [0x2052B44],
        None,
        (
            "Returns the spawn threshold of the given monster ID\n\nThe spawn threshold"
            " determines the minimum SCENARIO_BALANCE_FLAG value required by a monster"
            " to spawn in dungeons.\n\nr0: monster id\nreturn: Spawn threshold"
        ),
    )

    NeedsItemToSpawn = Symbol(
        [0x52B60],
        [0x2052B60],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: bool",
    )

    GetExclusiveItem = Symbol(
        [0x52B8C],
        [0x2052B8C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nr1: determines"
            " which exclusive item\nreturn: exclusive item"
        ),
    )

    GetFamilyIndex = Symbol(
        [0x52BB8],
        [0x2052BB8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: family index",
    )

    LoadM2nAndN2m = Symbol(
        [0x52BD4],
        [0x2052BD4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    IsNotNickname = Symbol(
        [0x52FB0],
        [0x2052FB0],
        None,
        (
            "Checks if the string_buffer matches the name of the species\n\nNote:"
            " unverified, ported from Irdkwia's notes\n\nr0: string_buffer\nr1: monster"
            " ID\nreturn: bool"
        ),
    )

    GetLvlStats = Symbol(
        [0x5379C],
        [0x205379C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output] level"
            " stats\nr1: monster ID\nr2: level"
        ),
    )

    GetEvoFamily = Symbol(
        [0x53DD0],
        [0x2053DD0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: monster_str\nr1:"
            " evo_family_str\nreturn: nb_family"
        ),
    )

    GetEvolutions = Symbol(
        [0x53E88],
        [0x2053E88],
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
        [0x53FC8],
        [0x2053FC8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dmons_addr",
    )

    GetBaseForm = Symbol(
        [0x54024],
        [0x2054024],
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
        [0x54250],
        [0x2054250],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: base form",
    )

    GetBaseFormCastformCherrimDeoxys = Symbol(
        [0x54398],
        [0x2054398],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: base form",
    )

    GetAllBaseForms = Symbol(
        [0x54464],
        [0x2054464],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: base form",
    )

    GetDexNumberVeneer = Symbol(
        [0x54474],
        [0x2054474],
        None,
        (
            "Likely a linker-generated veneer for GetDexNumber.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " id\nreturn: dex number"
        ),
    )

    GetMonsterIdFromSpawnEntry = Symbol(
        [0x54480],
        [0x2054480],
        None,
        (
            "Returns the monster ID of the specified monster spawn entry\n\nr0: Pointer"
            " to the monster spawn entry\nreturn: monster_spawn_entry::id"
        ),
    )

    SetMonsterId = Symbol(
        [0x544A0],
        [0x20544A0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: mons_spawn_str\nr1:"
            " monster ID"
        ),
    )

    SetMonsterLevelAndId = Symbol(
        [0x544A8],
        [0x20544A8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: mons_spawn_str\nr1:"
            " level\nr2: monster ID"
        ),
    )

    GetMonsterLevelFromSpawnEntry = Symbol(
        [0x544B8],
        [0x20544B8],
        None,
        (
            "Returns the level of the specified monster spawn entry.\n\nr0: pointer to"
            " the monster spawn entry\nreturn: uint8_t"
        ),
    )

    GetMonsterGenderVeneer = Symbol(
        [0x54760],
        [0x2054760],
        None,
        (
            "Likely a linker-generated veneer for GetMonsterGender.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " monster id\nreturn: monster gender"
        ),
    )

    IsMonsterValid = Symbol(
        [0x5476C],
        [0x205476C],
        None,
        "Checks if an monster ID is valid.\n\nr0: monster ID\nreturn: bool",
    )

    IsUnown = Symbol(
        [0x54A88],
        [0x2054A88],
        None,
        "Checks if a monster ID is an Unown.\n\nr0: monster ID\nreturn: bool",
    )

    IsShaymin = Symbol(
        [0x54AA4],
        [0x2054AA4],
        None,
        "Checks if a monster ID is a Shaymin form.\n\nr0: monster ID\nreturn: bool",
    )

    IsCastform = Symbol(
        [0x54AD4],
        [0x2054AD4],
        None,
        "Checks if a monster ID is a Castform form.\n\nr0: monster ID\nreturn: bool",
    )

    IsCherrim = Symbol(
        [0x54B2C],
        [0x2054B2C],
        None,
        "Checks if a monster ID is a Cherrim form.\n\nr0: monster ID\nreturn: bool",
    )

    IsDeoxys = Symbol(
        [0x54B74],
        [0x2054B74],
        None,
        "Checks if a monster ID is a Deoxys form.\n\nr0: monster ID\nreturn: bool",
    )

    GetSecondFormIfValid = Symbol(
        [0x54BA4],
        [0x2054BA4],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn:"
            " second form"
        ),
    )

    FemaleToMaleForm = Symbol(
        [0x54BE0],
        [0x2054BE0],
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
        [0x54C24],
        [0x2054C24],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: base form",
    )

    BaseFormsEqual = Symbol(
        [0x54CD8],
        [0x2054CD8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id1\nr1: id2\nreturn:"
            " if the base forms are the same"
        ),
    )

    DexNumbersEqual = Symbol(
        [0x54DC4],
        [0x2054DC4],
        None,
        (
            "Each Unown is considered as different\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: id1\nr1: id2\nreturn: bool"
        ),
    )

    GendersEqual = Symbol(
        [0x54E4C],
        [0x2054E4C],
        None,
        (
            "Checks if the genders for two monster IDs are equal.\n\nr0: id1\nr1:"
            " id2\nreturn: bool"
        ),
    )

    GendersEqualNotGenderless = Symbol(
        [0x54E78],
        [0x2054E78],
        None,
        (
            "Checks if the genders for two monster IDs are equal. Always returns false"
            " if either gender is GENDER_GENDERLESS.\n\nr0: id1\nr1: id2\nreturn: bool"
        ),
    )

    IsMonsterOnTeam = Symbol(
        [0x55148],
        [0x2055148],
        None,
        (
            "Checks if a given monster is on the exploration team (not necessarily the"
            " active party)?\n\nIrdkwia's notes:\n  recruit_strategy=0: strict"
            " equality\n  recruit_strategy=1: relative equality\n\nr0: monster ID\nr1:"
            " recruit_strategy\nreturn: bool"
        ),
    )

    GetNbRecruited = Symbol(
        [0x55274],
        [0x2055274],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: recruit_str",
    )

    GetMember = Symbol(
        [0x555A8],
        [0x20555A8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: member_idx\nreturn: ?",
    )

    GetHeroStrIdIfExists = Symbol(
        [0x55650],
        [0x2055650],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    GetPartnerStrIdIfExists = Symbol(
        [0x5567C],
        [0x205567C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    GetFirstTeamMemberStrIdIfExists = Symbol(
        [0x556A8],
        [0x20556A8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    GetSecondTeamMemberStrIdIfExists = Symbol(
        [0x556EC],
        [0x20556EC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    GetThirdTeamMemberStrIdIfExists = Symbol(
        [0x55730],
        [0x2055730],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    GetHeroData = Symbol(
        [0x55770],
        [0x2055770],
        None,
        (
            "Returns the ground monster data of the hero (first slot in Chimecho"
            " Assembly)\n\nreturn: Monster data"
        ),
    )

    GetPartnerData = Symbol(
        [0x55798],
        [0x2055798],
        None,
        (
            "Returns the ground monster data of the partner (second slot in Chimecho"
            " Assembly)\n\nreturn: Monster data"
        ),
    )

    GetFirstTeamMemberData = Symbol(
        [0x557C4],
        [0x20557C4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: Monster data",
    )

    GetSecondTeamMemberData = Symbol(
        [0x5580C],
        [0x205580C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: Monster data",
    )

    GetThirdTeamMemberData = Symbol(
        [0x55854],
        [0x2055854],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: Monster data",
    )

    GetFirstEmptyRecruitSlot = Symbol(
        [0x55964],
        [0x2055964],
        None,
        (
            "Returns -1 if there is none\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: ?\nreturn: ?"
        ),
    )

    CheckTeamMemberField8 = Symbol(
        [0x56228],
        [0x2056228],
        None,
        (
            "Checks if a value obtained from team_member::field_0x8 is equal to certain"
            " values.\n\nThis is known to return true for some or all of the guest"
            " monsters.\n\nr0: Value read from team_member::field_0x8\nreturn: True if"
            " the value is equal to 0x55AA or 0x5AA5"
        ),
    )

    IsMonsterIdInNormalRange = Symbol(
        [0x56294],
        [0x2056294],
        None,
        (
            "Checks if a monster ID is in the range [0, 554], meaning it's before the"
            " special story monster IDs and secondary gender IDs.\n\nr0: monster"
            " ID\nreturn: bool"
        ),
    )

    GetTeamMemberData = Symbol(
        [0x5638C],
        [0x205638C],
        None,
        (
            "Returns a struct containing information about a team member.\n\nIrdkwia's"
            " notes (note the discrepancy): GetEquivalentTeamID\n  r0: str_id\n "
            " return: team_id, -1 if not in team\n\nr0: Index\nreturn: Pointer to"
            " struct containing team member information"
        ),
    )

    GetTeamMember = Symbol(
        [0x563BC],
        [0x20563BC],
        None,
        (
            "Null pointer if -1\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " team_id\nreturn: team member"
        ),
    )

    SetTeamSetupHeroAndPartnerOnly = Symbol(
        [0x569CC],
        [0x20569CC],
        None,
        (
            "Implements SPECIAL_PROC_SET_TEAM_SETUP_HERO_AND_PARTNER_ONLY (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    SetTeamSetupHeroOnly = Symbol(
        [0x56AB0],
        [0x2056AB0],
        None,
        (
            "Implements SPECIAL_PROC_SET_TEAM_SETUP_HERO_ONLY (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    GetPartyMembers = Symbol(
        [0x56C20],
        [0x2056C20],
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
        [0x57D58],
        [0x2057D58],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    ClearItem = Symbol(
        [0x581F0],
        [0x20581F0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: team_id\nr1: check",
    )

    ChangeGiratinaFormIfSkyDungeon = Symbol(
        [0x585D8],
        [0x20585D8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID",
    )

    CanLearnIqSkill = Symbol(
        [0x58CD8],
        [0x2058CD8],
        None,
        (
            "Returns whether an IQ skill can be learned with a given IQ amount or"
            " not.\n\nIf the specified amount is 0, it always returns false.\n\nr0: IQ"
            " amount\nr1: IQ skill\nreturn: True if the specified skill can be learned"
            " with the specified IQ amount."
        ),
    )

    GetLearnableIqSkills = Symbol(
        [0x58D04],
        [0x2058D04],
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
        [0x58DA4],
        [0x2058DA4],
        None,
        (
            "Disables an IQ skill.\n\nr0: Pointer to the bitarray containing the list"
            " of enabled IQ skills\nr1: ID of the skill to disable"
        ),
    )

    EnableIqSkill = Symbol(
        [0x58DF4],
        [0x2058DF4],
        None,
        (
            "Enables an IQ skill and disables any other skills that are incompatible"
            " with it.\n\nr0: Pointer to the bitarray containing the list of enabled IQ"
            " skills\nr1: ID of the skill to enable"
        ),
    )

    GetSpeciesIqSkill = Symbol(
        [0x58E68],
        [0x2058E68],
        None,
        (
            "Gets the <index>th skill on the list of IQ skills that a given monster"
            " species can learn.\n\nr0: Species ID\nr1: Index (starting at 0)\nreturn:"
            " IQ skill ID"
        ),
    )

    IqSkillFlagTest = Symbol(
        [0x58F04],
        [0x2058F04],
        None,
        (
            "Tests whether an IQ skill with a given ID is active.\n\nr0: IQ skill"
            " bitvector to test\nr1: IQ skill ID\nreturn: bool"
        ),
    )

    GetNextIqSkill = Symbol(
        [0x58F24],
        [0x2058F24],
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
        [0x590F8],
        [0x20590F8],
        None,
        (
            "Returns the data of a monster sent into the Explorer Dojo using the"
            " 'exchange teams' option.\n\nr0: Entry number (0-3)\nreturn: Ground"
            " monster data of the specified entry"
        ),
    )

    WriteMonsterInfoToSave = Symbol(
        [0x59118],
        [0x2059118],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: start_address\nr1:"
            " total_length\nreturn: ?"
        ),
    )

    ReadMonsterInfoFromSave = Symbol(
        [0x59224],
        [0x2059224],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: start_address\nr1:"
            " total_length"
        ),
    )

    WriteMonsterToSave = Symbol(
        [0x59334],
        [0x2059334],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: write_info\nr1:"
            " ground_monster"
        ),
    )

    ReadMonsterFromSave = Symbol(
        [0x59444],
        [0x2059444],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info\nr1:"
            " ground_monster"
        ),
    )

    GetEvolutionPossibilities = Symbol(
        [0x59B18],
        [0x2059B18],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ground_monster\nr1:"
            " evo_struct_addr"
        ),
    )

    GetMonsterEvoStatus = Symbol(
        [0x5A210],
        [0x205A210],
        None,
        (
            "evo_status = 0: Not possible now\nevo_status = 1: Possible now\nevo_status"
            " = 2: No further\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " ground_monster\nreturn: evo_status"
        ),
    )

    GetSosMailCount = Symbol(
        [0x5B97C],
        [0x205B97C],
        None,
        (
            "Implements SPECIAL_PROC_GET_SOS_MAIL_COUNT (see"
            " ScriptSpecialProcessCall).\n\nr0: ?\nr1: some flag?\nreturn: SOS mail"
            " count"
        ),
    )

    IsMissionValid = Symbol(
        [0x5CA40],
        [0x205CA40],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: mission\nreturn: bool",
    )

    GenerateMission = Symbol(
        [0x5D224],
        [0x205D224],
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
        [0x5E5D0],
        [0x205E5D0],
        None,
        (
            "Generates the missions displayed on the Job Bulletin Board and the Outlaw"
            " Notice Board.\n\nNo params."
        ),
    )

    DungeonRequestsDone = Symbol(
        [0x5EDA4],
        [0x205EDA4],
        None,
        (
            "Seems to return the number of missions completed.\n\nPart of the"
            " implementation for SPECIAL_PROC_DUNGEON_HAD_REQUEST_DONE (see"
            " ScriptSpecialProcessCall).\n\nr0: ?\nr1: some flag?\nreturn: number of"
            " missions completed"
        ),
    )

    DungeonRequestsDoneWrapper = Symbol(
        [0x5EE10],
        [0x205EE10],
        None,
        (
            "Calls DungeonRequestsDone with the second argument set to false.\n\nr0:"
            " ?\nreturn: number of mission completed"
        ),
    )

    AnyDungeonRequestsDone = Symbol(
        [0x5EE20],
        [0x205EE20],
        None,
        (
            "Calls DungeonRequestsDone with the second argument set to true, and"
            " converts the integer output to a boolean.\n\nr0: ?\nreturn: bool: whether"
            " the number of missions completed is greater than 0"
        ),
    )

    GetAcceptedMission = Symbol(
        [0x5F0D8],
        [0x205F0D8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: mission_id\nreturn:"
            " mission"
        ),
    )

    GetMissionByTypeAndDungeon = Symbol(
        [0x5F3AC],
        [0x205F3AC],
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
        [0x5F4A4],
        [0x205F4A4],
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
        [0x5F758],
        [0x205F758],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    DeleteAllPossibleMonstersList = Symbol(
        [0x5F7C4],
        [0x205F7C4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GenerateAllPossibleDungeonsList = Symbol(
        [0x5F7F4],
        [0x205F7F4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    DeleteAllPossibleDungeonsList = Symbol(
        [0x5F8A0],
        [0x205F8A0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GenerateAllPossibleDeliverList = Symbol(
        [0x5F8D0],
        [0x205F8D0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?",
    )

    DeleteAllPossibleDeliverList = Symbol(
        [0x5F90C],
        [0x205F90C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    ClearMissionData = Symbol(
        [0x5F9B8],
        [0x205F9B8],
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
        [0x62A14],
        [0x2062A14],
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
        [0x62A58],
        [0x2062A58],
        None,
        (
            "Calls CanMonsterBeUsedForMission with r1 = 1.\n\nr0: Monster ID\nreturn:"
            " Result of CanMonsterBeUsedForMission"
        ),
    )

    CanMonsterBeUsedForMission = Symbol(
        [0x62A68],
        [0x2062A68],
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
        [0x62AE4],
        [0x2062AE4],
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
        [0x62DDC],
        [0x2062DDC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nr1:"
            " to_sky\nreturn: bool"
        ),
    )

    IsAvailableItem = Symbol(
        [0x6345C],
        [0x206345C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: bool",
    )

    GetAvailableItemDeliveryList = Symbol(
        [0x634A8],
        [0x20634A8],
        None,
        (
            "Uncertain.\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " item_buffer\nreturn: nb_items"
        ),
    )

    GetActorMatchingStorageId = Symbol(
        [0x65998],
        [0x2065998],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: actor_id\nreturn:"
            " storage ID"
        ),
    )

    ScriptSpecialProcess0x3D = Symbol(
        [0x65B50],
        [0x2065B50],
        None,
        "Implements SPECIAL_PROC_0x3D (see ScriptSpecialProcessCall).\n\nNo params.",
    )

    ScriptSpecialProcess0x3E = Symbol(
        [0x65B60],
        [0x2065B60],
        None,
        "Implements SPECIAL_PROC_0x3E (see ScriptSpecialProcessCall).\n\nNo params.",
    )

    ScriptSpecialProcess0x17 = Symbol(
        [0x65C48],
        [0x2065C48],
        None,
        "Implements SPECIAL_PROC_0x17 (see ScriptSpecialProcessCall).\n\nNo params.",
    )

    ItemAtTableIdx = Symbol(
        [0x65CF8],
        [0x2065CF8],
        None,
        (
            "Gets info about the item at a given item table (not sure what this table"
            " is...) index.\n\nUsed by SPECIAL_PROC_COUNT_TABLE_ITEM_TYPE_IN_BAG and"
            " friends (see ScriptSpecialProcessCall).\n\nr0: table index\nr1: [output]"
            " pointer to an owned_item"
        ),
    )

    DungeonSwapIdToIdx = Symbol(
        [0x6A714],
        [0x206A714],
        None,
        (
            "Converts a dungeon ID to its corresponding index in DUNGEON_SWAP_ID_TABLE,"
            " or -1 if not found.\n\nr0: dungeon ID\nreturn: index"
        ),
    )

    DungeonSwapIdxToId = Symbol(
        [0x6A750],
        [0x206A750],
        None,
        (
            "Converts an index in DUNGEON_SWAP_ID_TABLE to the corresponding dungeon"
            " ID, or DUNGEON_DUMMY_0xFF if the index is -1.\n\nr0: index\nreturn:"
            " dungeon ID"
        ),
    )

    ResumeBgm = Symbol(
        [0x6D9BC],
        [0x206D9BC],
        None,
        "Uncertain.\n\nNote: unverified, ported from Irdkwia's notes",
    )

    FlushChannels = Symbol(
        [0x70674], [0x2070674], None, "Note: unverified, ported from Irdkwia's notes"
    )

    UpdateChannels = Symbol(
        [0x7448C],
        [0x207448C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    WaitForInterrupt = Symbol(
        [0x7BC30],
        [0x207BC30],
        None,
        (
            "Presumably blocks until the program receives an interrupt.\n\nThis just"
            " calls (in Ghidra terminology) coproc_moveto_Wait_for_interrupt(0). See"
            " https://en.wikipedia.org/wiki/ARM_architecture_family#Coprocessors.\n\nNo"
            " params."
        ),
    )

    FileInit = Symbol(
        [0x7F3E4],
        [0x207F3E4],
        None,
        (
            "Initializes a file_stream structure for file I/O.\n\nThis function must"
            " always be called before opening a file.\n\nr0: file_stream pointer"
        ),
    )

    Abs = Symbol(
        [0x8655C],
        [0x208655C],
        None,
        "Takes the absolute value of an integer.\n\nr0: x\nreturn: abs(x)",
    )

    Mbtowc = Symbol(
        [0x871BC],
        [0x20871BC],
        None,
        (
            "The mbtowc(3) C library function.\n\nr0: pwc\nr1: s\nr2: n\nreturn: number"
            " of consumed bytes, or -1 on failure"
        ),
    )

    TryAssignByte = Symbol(
        [0x871F4],
        [0x20871F4],
        None,
        (
            "Assign a byte to the target of a pointer if the pointer is"
            " non-null.\n\nr0: pointer\nr1: value\nreturn: true on success, false on"
            " failure"
        ),
    )

    TryAssignByteWrapper = Symbol(
        [0x87208],
        [0x2087208],
        None,
        (
            "Wrapper around TryAssignByte.\n\nAccesses the TryAssignByte function with"
            " a weird chain of pointer dereferences.\n\nr0: pointer\nr1: value\nreturn:"
            " true on success, false on failure"
        ),
    )

    Wcstombs = Symbol(
        [0x87224],
        [0x2087224],
        None,
        (
            "The wcstombs(3) C library function.\n\nr0: dest\nr1: src\nr2: n\nreturn:"
            " characters converted"
        ),
    )

    Memcpy = Symbol(
        [0x8729C],
        [0x208729C],
        None,
        "The memcpy(3) C library function.\n\nr0: dest\nr1: src\nr2: n",
    )

    Memmove = Symbol(
        [0x872BC],
        [0x20872BC],
        None,
        (
            "The memmove(3) C library function.\n\nThe implementation is nearly the"
            " same as Memcpy, but it copies bytes from back to front if src <"
            " dst.\n\nr0: dest\nr1: src\nr2: n"
        ),
    )

    Memset = Symbol(
        [0x87308],
        [0x2087308],
        None,
        (
            "The memset(3) C library function.\n\nThis is just a wrapper around"
            " MemsetInternal that returns the pointer at the end.\n\nr0: s\nr1: c (int,"
            " but must be a single-byte value)\nr2: n\nreturn: s"
        ),
    )

    Memchr = Symbol(
        [0x8731C],
        [0x208731C],
        None,
        (
            "The memchr(3) C library function.\n\nr0: s\nr1: c\nr2: n\nreturn: pointer"
            " to first occurrence of c in s, or a null pointer if no match"
        ),
    )

    Memcmp = Symbol(
        [0x87348],
        [0x2087348],
        None,
        (
            "The memcmp(3) C library function.\n\nr0: s1\nr1: s2\nr2: n\nreturn:"
            " comparison value"
        ),
    )

    MemsetInternal = Symbol(
        [0x87388],
        [0x2087388],
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
        [0x88C74],
        [0x2088C74],
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
        [0x89498],
        [0x2089498],
        None,
        (
            "Best-effort append the given data to a slice. If the slice's capacity is"
            " reached, any remaining data will be truncated.\n\nr0: slice pointer\nr1:"
            " buffer of data to append\nr2: number of bytes in the data buffer\nreturn:"
            " true"
        ),
    )

    VsprintfInternal = Symbol(
        [0x894DC],
        [0x20894DC],
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
        [0x89544],
        [0x2089544],
        None,
        (
            "The vsprintf(3) C library function.\n\nr0: str\nr1: format\nr2:"
            " ap\nreturn: number of characters printed, excluding the null-terminator"
        ),
    )

    Snprintf = Symbol(
        [0x8955C],
        [0x208955C],
        None,
        (
            "The snprintf(3) C library function.\n\nThis calls VsprintfInternal"
            " directly, so it's presumably the real snprintf.\n\nr0: str\nr1: n\nr2:"
            " format\n...: variadic\nreturn: number of characters printed, excluding"
            " the null-terminator"
        ),
    )

    Sprintf = Symbol(
        [0x89584],
        [0x2089584],
        None,
        (
            "The sprintf(3) C library function.\n\nThis calls VsprintfInternal"
            " directly, so it's presumably the real sprintf.\n\nr0: str\nr1:"
            " format\n...: variadic\nreturn: number of characters printed, excluding"
            " the null-terminator"
        ),
    )

    Strlen = Symbol(
        [0x89678],
        [0x2089678],
        None,
        "The strlen(3) C library function.\n\nr0: s\nreturn: length of s",
    )

    Strcpy = Symbol(
        [0x89694],
        [0x2089694],
        None,
        (
            "The strcpy(3) C library function.\n\nThis function is optimized to copy"
            " characters in aligned 4-byte chunks if possible, correctly handling any"
            " unaligned bytes at the front/back.\n\nr0: dest\nr1: src"
        ),
    )

    Strncpy = Symbol(
        [0x8975C],
        [0x208975C],
        None,
        "The strncpy(3) C library function.\n\nr0: dest\nr1: src\nr2: n",
    )

    Strcat = Symbol(
        [0x897AC],
        [0x20897AC],
        None,
        "The strcat(3) C library function.\n\nr0: dest\nr1: src",
    )

    Strncat = Symbol(
        [0x897DC],
        [0x20897DC],
        None,
        "The strncat(3) C library function.\n\nr0: dest\nr1: src\nr2: n",
    )

    Strcmp = Symbol(
        [0x8982C],
        [0x208982C],
        None,
        (
            "The strcmp(3) C library function.\n\nSimilarly to Strcpy, this function is"
            " optimized to compare characters in aligned 4-byte chunks if"
            " possible.\n\nr0: s1\nr1: s2\nreturn: comparison value"
        ),
    )

    Strncmp = Symbol(
        [0x89940],
        [0x2089940],
        None,
        (
            "The strncmp(3) C library function.\n\nr0: s1\nr1: s2\nr2: n\nreturn:"
            " comparison value"
        ),
    )

    Strchr = Symbol(
        [0x89974],
        [0x2089974],
        None,
        (
            "The strchr(3) C library function.\n\nr0: string\nr1: c\nreturn: pointer to"
            " the located byte c, or null pointer if no match"
        ),
    )

    Strcspn = Symbol(
        [0x899B0],
        [0x20899B0],
        None,
        (
            "The strcspn(3) C library function.\n\nr0: string\nr1: stopset\nreturn:"
            " offset of the first character in string within stopset"
        ),
    )

    Strstr = Symbol(
        [0x89A70],
        [0x2089A70],
        None,
        (
            "The strstr(3) C library function.\n\nr0: haystack\nr1: needle\nreturn:"
            " pointer into haystack where needle starts, or null pointer if no match"
        ),
    )

    Wcslen = Symbol(
        [0x8B3E8],
        [0x208B3E8],
        None,
        "The wcslen(3) C library function.\n\nr0: ws\nreturn: length of ws",
    )

    AddFloat = Symbol(
        [0x8ECB8],
        [0x208ECB8],
        None,
        (
            "This appears to be the libgcc implementation of __addsf3 (not sure which"
            " gcc version), which implements the addition operator for IEEE 754"
            " floating-point numbers.\n\nr0: a\nr1: b\nreturn: a + b"
        ),
    )

    DivideFloat = Symbol(
        [0x8F234],
        [0x208F234],
        None,
        (
            "This appears to be the libgcc implementation of __divsf3 (not sure which"
            " gcc version), which implements the division operator for IEEE 754"
            " floating-point numbers.\n\nr0: dividend\nr1: divisor\nreturn: dividend /"
            " divisor"
        ),
    )

    FloatToDouble = Symbol(
        [0x8F5EC],
        [0x208F5EC],
        None,
        (
            "This appears to be the libgcc implementation of __extendsfdf2 (not sure"
            " which gcc version), which implements the float to double cast operation"
            " for IEEE 754 floating-point numbers.\n\nr0: float\nreturn: (double)float"
        ),
    )

    FloatToInt = Symbol(
        [0x8F670],
        [0x208F670],
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
        [0x8F6A4],
        [0x208F6A4],
        None,
        (
            "This appears to be the libgcc implementation of __floatsisf (not sure"
            " which gcc version), which implements the int to float cast operation for"
            " IEEE 754 floating-point numbers.\n\nr0: int\nreturn: (float)int"
        ),
    )

    UIntToFloat = Symbol(
        [0x8F6EC],
        [0x208F6EC],
        None,
        (
            "This appears to be the libgcc implementation of __floatunsisf (not sure"
            " which gcc version), which implements the unsigned int to float cast"
            " operation for IEEE 754 floating-point numbers.\n\nr0: uint\nreturn:"
            " (float)uint"
        ),
    )

    MultiplyFloat = Symbol(
        [0x8F734],
        [0x208F734],
        None,
        (
            "This appears to be the libgcc implementation of __mulsf3 (not sure which"
            " gcc version), which implements the multiplication operator for IEEE 754"
            " floating-point numbers."
        ),
    )

    Sqrtf = Symbol(
        [0x8F914],
        [0x208F914],
        None,
        "The sqrtf(3) C library function.\n\nr0: x\nreturn: sqrt(x)",
    )

    SubtractFloat = Symbol(
        [0x8FA04],
        [0x208FA04],
        None,
        (
            "This appears to be the libgcc implementation of __subsf3 (not sure which"
            " gcc version), which implements the subtraction operator for IEEE 754"
            " floating-point numbers.\n\nr0: a\nr1: b\nreturn: a - b"
        ),
    )

    DivideInt = Symbol(
        [0x8FEA4],
        [0x208FEA4],
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
        [0x900B0],
        [0x20900B0],
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
        [0x900B8],
        [0x20900B8],
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


class NaArm9Data:
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
        [0xCA84],
        [0x200CA84],
        None,
        "The damage source value for any item in CATEGORY_ORBS, 0x262.",
    )

    DAMAGE_SOURCE_CODE_NON_ORB_ITEM = Symbol(
        [0xCA88],
        [0x200CA88],
        None,
        "The damage source value for any item not in CATEGORY_ORBS, 0x263.",
    )

    AURA_BOW_ID_LAST = Symbol(
        [0xCC34], [0x200CC34], 0x4, "Highest item ID of the aura bows."
    )

    NUMBER_OF_ITEMS = Symbol(
        [0xE7BC, 0xE860], [0x200E7BC, 0x200E860], 0x4, "Number of items in the game."
    )

    MAX_MONEY_CARRIED = Symbol(
        [0xED50],
        [0x200ED50],
        0x4,
        "Maximum amount of money the player can carry, 99999.",
    )

    MAX_MONEY_STORED = Symbol(
        [0x10750],
        [0x2010750],
        0x4,
        "Maximum amount of money the player can store in the Duskull Bank, 9999999.",
    )

    DIALOG_BOX_LIST_PTR = Symbol(
        [0x28350], [0x2028350], 0x4, "Hard-coded pointer to DIALOG_BOX_LIST."
    )

    SCRIPT_VARS_VALUES_PTR = Symbol(
        [0x4B2F8, 0x4B4E4, 0x4C42C, 0x4C484],
        [0x204B2F8, 0x204B4E4, 0x204C42C, 0x204C484],
        0x4,
        "Hard-coded pointer to SCRIPT_VARS_VALUES.",
    )

    MONSTER_ID_LIMIT = Symbol(
        [0x5449C],
        [0x205449C],
        0x4,
        "One more than the maximum valid monster ID (0x483).",
    )

    MAX_RECRUITABLE_TEAM_MEMBERS = Symbol(
        [0x55238, 0x5564C],
        [0x2055238, 0x205564C],
        0x4,
        (
            "555, appears to be the maximum number of members recruited to an"
            " exploration team, at least for the purposes of some checks that need to"
            " iterate over all team members."
        ),
    )

    CART_REMOVED_IMG_DATA = Symbol([0x92AE8], [0x2092AE8], 0x4000, "")

    AVAILABLE_ITEMS_IN_GROUP_TABLE = Symbol(
        [0x94D34],
        [0x2094D34],
        0x3200,
        (
            "100*0x80\nLinked to the dungeon group id\n\nNote: unverified, ported from"
            " Irdkwia's notes"
        ),
    )

    ARM9_UNKNOWN_TABLE__NA_2097FF8 = Symbol(
        [0x97FF8],
        [0x2097FF8],
        0x40,
        "16*0x4 (0x2+0x2)\n\nNote: unverified, ported from Irdkwia's notes",
    )

    KECLEON_SHOP_ITEM_TABLE_LISTS_1 = Symbol(
        [0x980C0],
        [0x20980C0],
        0x10,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: enum item_id[4]",
    )

    KECLEON_SHOP_ITEM_TABLE_LISTS_2 = Symbol(
        [0x980D0],
        [0x20980D0],
        0x10,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: enum item_id[4]",
    )

    EXCLUSIVE_ITEM_STAT_BOOST_DATA = Symbol(
        [0x980E8],
        [0x20980E8],
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
        [0x980E8], [0x20980E8], 0x39, "EXCLUSIVE_ITEM_STAT_BOOST_DATA, offset by 0"
    )

    EXCLUSIVE_ITEM_SPECIAL_ATTACK_BOOSTS = Symbol(
        [0x980E9], [0x20980E9], 0x39, "EXCLUSIVE_ITEM_STAT_BOOST_DATA, offset by 1"
    )

    EXCLUSIVE_ITEM_DEFENSE_BOOSTS = Symbol(
        [0x980EA], [0x20980EA], 0x39, "EXCLUSIVE_ITEM_STAT_BOOST_DATA, offset by 2"
    )

    EXCLUSIVE_ITEM_SPECIAL_DEFENSE_BOOSTS = Symbol(
        [0x980EB], [0x20980EB], 0x39, "EXCLUSIVE_ITEM_STAT_BOOST_DATA, offset by 3"
    )

    EXCLUSIVE_ITEM_EFFECT_DATA = Symbol(
        [0x98124],
        [0x2098124],
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
        [0x98125], [0x2098125], 0x777, "EXCLUSIVE_ITEM_EFFECT_DATA, offset by 1"
    )

    RECYCLE_SHOP_ITEM_LIST = Symbol(
        [0x988CC], [0x20988CC], 0x360, "Note: unverified, ported from Irdkwia's notes"
    )

    TYPE_SPECIFIC_EXCLUSIVE_ITEMS = Symbol(
        [0x98C2C],
        [0x2098C2C],
        0x88,
        (
            "Lists of type-specific exclusive items (silk, dust, gem, globe) for each"
            " type.\n\ntype: struct item_id_16[17][4]"
        ),
    )

    RECOIL_MOVE_LIST = Symbol(
        [0x98D74],
        [0x2098D74],
        0x16,
        (
            "Null-terminated list of all the recoil moves, as 2-byte move IDs.\n\ntype:"
            " struct move_id_16[11]"
        ),
    )

    PUNCH_MOVE_LIST = Symbol(
        [0x98D8A],
        [0x2098D8A],
        0x20,
        (
            "Null-terminated list of all the punch moves, as 2-byte move IDs.\n\ntype:"
            " struct move_id_16[16]"
        ),
    )

    MOVE_POWER_STARS_TABLE = Symbol(
        [0x99CD4],
        [0x2099CD4],
        0x18,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int[6]",
    )

    MOVE_ACCURACY_STARS_TABLE = Symbol(
        [0x99CEC],
        [0x2099CEC],
        0x20,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int[8]",
    )

    PARTNER_TALK_KIND_TABLE = Symbol(
        [0x9CCE4],
        [0x209CCE4],
        0x58,
        (
            "Table of values for the PARTNER_TALK_KIND script variable.\n\ntype: struct"
            " partner_talk_kind_table_entry[11]"
        ),
    )

    SCRIPT_VARS_LOCALS = Symbol(
        [0x9CECC],
        [0x209CECC],
        0x40,
        (
            "List of special 'local' variables available to the script engine. There"
            " are 4 16-byte entries.\n\nEach entry has the same structure as an entry"
            " in SCRIPT_VARS.\n\ntype: struct script_local_var_table"
        ),
    )

    SCRIPT_VARS = Symbol(
        [0x9D870],
        [0x209D870],
        0x730,
        (
            "List of predefined global variables that track game state, which are"
            " available to the script engine. There are 115 16-byte entries.\n\nThese"
            " variables underpin the various ExplorerScript global variables you can"
            " use in the SkyTemple SSB debugger.\n\ntype: struct script_var_table"
        ),
    )

    HARDCODED_PORTRAIT_DATA_TABLE = Symbol(
        [0x9E014],
        [0x209E014],
        0xC0,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " portrait_data_entry[32]"
        ),
    )

    WONDER_MAIL_BITS_MAP = Symbol(
        [0x9E0E8],
        [0x209E0E8],
        0x20,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: uint8_t[32]",
    )

    WONDER_MAIL_BITS_SWAP = Symbol(
        [0x9E108],
        [0x209E108],
        0x24,
        (
            "Last 2 bytes are unused\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\ntype: uint8_t[36]"
        ),
    )

    ARM9_UNKNOWN_TABLE__NA_209E12C = Symbol(
        [0x9E12C],
        [0x209E12C],
        0x38,
        "52*0x2 + 2 bytes unused\n\nNote: unverified, ported from Irdkwia's notes",
    )

    ARM9_UNKNOWN_TABLE__NA_209E164 = Symbol(
        [0x9E164],
        [0x209E164],
        0x100,
        "256*0x1\n\nNote: unverified, ported from Irdkwia's notes",
    )

    ARM9_UNKNOWN_TABLE__NA_209E280 = Symbol(
        [0x9E280],
        [0x209E280],
        0x20,
        "32*0x1\n\nNote: unverified, ported from Irdkwia's notes",
    )

    WONDER_MAIL_ENCRYPTION_TABLE = Symbol(
        [0x9E2A0],
        [0x209E2A0],
        0x100,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: uint8_t[256]",
    )

    DUNGEON_DATA_LIST = Symbol(
        [0x9E3A0],
        [0x209E3A0],
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
        [0x9E670],
        [0x209E670],
        0x4C,
        (
            "List of monster IDs with a corresponding milestone in the Adventure"
            " Log.\n\ntype: struct monster_id_16[38]"
        ),
    )

    ARM9_UNKNOWN_DATA__NA_209E6BC = Symbol(
        [0x9E6BC], [0x209E6BC], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    TACTIC_NAME_STRING_IDS = Symbol(
        [0x9E6C0],
        [0x209E6C0],
        0x18,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[12]",
    )

    STATUS_NAME_STRING_IDS = Symbol(
        [0x9E6D8],
        [0x209E6D8],
        0xCC,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[102]",
    )

    DUNGEON_RETURN_STATUS_TABLE = Symbol(
        [0x9E7A4],
        [0x209E7A4],
        0x16C,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " dungeon_return_status[91]"
        ),
    )

    STATUSES_FULL_DESCRIPTION_STRING_IDS = Symbol(
        [0x9E910],
        [0x209E910],
        0x19C,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " status_description[103]"
        ),
    )

    ARM9_UNKNOWN_DATA__NA_209EAAC = Symbol(
        [0x9EAAC], [0x209EAAC], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_FLOOR_RANKS_AND_ITEM_LISTS_1 = Symbol(
        [0x9EAB0], [0x209EAB0], 0xC64, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_FLOORS_FORBIDDEN = Symbol(
        [0x9F714],
        [0x209F714],
        0xC8,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " mission_floors_forbidden[100]"
        ),
    )

    MISSION_FLOOR_RANKS_AND_ITEM_LISTS_2 = Symbol(
        [0x9F7DC], [0x209F7DC], 0x12F8, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_FLOOR_RANKS_PTRS = Symbol(
        [0xA0AD4],
        [0x20A0AD4],
        0x190,
        (
            "Uses MISSION_FLOOR_RANKS_AND_ITEM_LISTS\n\nNote: unverified, ported from"
            " Irdkwia's notes"
        ),
    )

    DUNGEON_RESTRICTIONS = Symbol(
        [0xA0C64],
        [0x20A0C64],
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
        [0xA186C], [0x20A186C], 0x2, "Stat boost value for the Special Band."
    )

    MUNCH_BELT_STAT_BOOST = Symbol(
        [0xA187C], [0x20A187C], 0x2, "Stat boost value for the Munch Belt."
    )

    GUMMI_STAT_BOOST = Symbol(
        [0xA1888],
        [0x20A1888],
        0x2,
        "Stat boost value if a stat boost occurs when eating normal Gummis.",
    )

    MIN_IQ_EXCLUSIVE_MOVE_USER = Symbol([0xA188C], [0x20A188C], 0x4, "")

    WONDER_GUMMI_IQ_GAIN = Symbol(
        [0xA1890], [0x20A1890], 0x2, "IQ gain when ingesting wonder gummis."
    )

    AURA_BOW_STAT_BOOST = Symbol(
        [0xA1898], [0x20A1898], 0x2, "Stat boost value for the aura bows."
    )

    MIN_IQ_ITEM_MASTER = Symbol([0xA18A4], [0x20A18A4], 0x4, "")

    DEF_SCARF_STAT_BOOST = Symbol(
        [0xA18A8], [0x20A18A8], 0x2, "Stat boost value for the Defense Scarf."
    )

    POWER_BAND_STAT_BOOST = Symbol(
        [0xA18AC], [0x20A18AC], 0x2, "Stat boost value for the Power Band."
    )

    WONDER_GUMMI_STAT_BOOST = Symbol(
        [0xA18B0],
        [0x20A18B0],
        0x2,
        "Stat boost value if a stat boost occurs when eating Wonder Gummis.",
    )

    ZINC_BAND_STAT_BOOST = Symbol(
        [0xA18B4], [0x20A18B4], 0x2, "Stat boost value for the Zinc Band."
    )

    EGG_HP_BONUS = Symbol(
        [0xA18B8], [0x20A18B8], 0x2, "Note: unverified, ported from Irdkwia's notes"
    )

    EVOLUTION_HP_BONUS = Symbol(
        [0xA18C4], [0x20A18C4], 0x2, "Note: unverified, ported from Irdkwia's notes"
    )

    EVOLUTION_PHYSICAL_STAT_BONUSES = Symbol(
        [0xA18D0],
        [0x20A18D0],
        0x4,
        "0x2: Atk + 0x2: Def\n\nNote: unverified, ported from Irdkwia's notes",
    )

    EGG_STAT_BONUSES = Symbol(
        [0xA18DC],
        [0x20A18DC],
        0x8,
        (
            "0x2: Atk + 0x2: SpAtk + 0x2: Def + 0x2: SpDef\n\nNote: unverified, ported"
            " from Irdkwia's notes"
        ),
    )

    EVOLUTION_SPECIAL_STAT_BONUSES = Symbol(
        [0xA18E4],
        [0x20A18E4],
        0x4,
        "0x2: SpAtk + 0x2: SpDef\n\nNote: unverified, ported from Irdkwia's notes",
    )

    FORBIDDEN_FORGOT_MOVE_LIST = Symbol(
        [0xA1918],
        [0x20A1918],
        0x12,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " forbidden_forgot_move_entry[3]"
        ),
    )

    TACTICS_UNLOCK_LEVEL_TABLE = Symbol(
        [0xA1940], [0x20A1940], 0x18, "type: int16_t[12]"
    )

    CLIENT_LEVEL_TABLE = Symbol(
        [0xA1978],
        [0x20A1978],
        0x20,
        (
            "Still a guess\n\nNote: unverified, ported from Irdkwia's notes\n\ntype:"
            " int16_t[16]"
        ),
    )

    OUTLAW_LEVEL_TABLE = Symbol(
        [0xA1998],
        [0x20A1998],
        0x20,
        (
            "Table of 2-byte outlaw levels for outlaw missions, indexed by mission"
            " rank.\n\ntype: int16_t[16]"
        ),
    )

    OUTLAW_MINION_LEVEL_TABLE = Symbol(
        [0xA19B8],
        [0x20A19B8],
        0x20,
        (
            "Table of 2-byte outlaw minion levels for outlaw hideout missions, indexed"
            " by mission rank.\n\ntype: int16_t[16]"
        ),
    )

    HIDDEN_POWER_BASE_POWER_TABLE = Symbol(
        [0xA19D8],
        [0x20A19D8],
        0x28,
        (
            "Still a guess\n\nNote: unverified, ported from Irdkwia's notes\n\ntype:"
            " int[10]"
        ),
    )

    VERSION_EXCLUSIVE_MONSTERS = Symbol(
        [0xA1A00],
        [0x20A1A00],
        0x5C,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " version_exclusive_monster[23]"
        ),
    )

    IQ_SKILL_RESTRICTIONS = Symbol(
        [0xA1A5C],
        [0x20A1A5C],
        0x8A,
        (
            "Table of 2-byte values for each IQ skill that represent a group. IQ skills"
            " in the same group can not be enabled at the same time.\n\ntype:"
            " int16_t[69]"
        ),
    )

    SECONDARY_TERRAIN_TYPES = Symbol(
        [0xA1AE8],
        [0x20A1AE8],
        0xC8,
        (
            "The type of secondary terrain for each dungeon in the game.\n\nThis is an"
            " array of 200 bytes. Each byte is an enum corresponding to one"
            " dungeon.\n\ntype: struct secondary_terrain_type_8[200]"
        ),
    )

    SENTRY_DUTY_MONSTER_IDS = Symbol(
        [0xA1BB0],
        [0x20A1BB0],
        0xCC,
        (
            "Table of monster IDs usable in the sentry duty minigame.\n\ntype: struct"
            " monster_id_16[102]"
        ),
    )

    IQ_SKILLS = Symbol(
        [0xA1C7C],
        [0x20A1C7C],
        0x114,
        (
            "Table of 4-byte values for each IQ skill that represent the required IQ"
            " value to unlock a skill.\n\ntype: int[69]"
        ),
    )

    IQ_GROUP_SKILLS = Symbol(
        [0xA1D90], [0x20A1D90], 0x190, "Irdkwia's notes: 25*16*0x1"
    )

    MONEY_QUANTITY_TABLE = Symbol(
        [0xA1F20],
        [0x20A1F20],
        0x190,
        (
            "Table that maps money quantity codes (as recorded in, e.g., struct item)"
            " to actual amounts.\n\ntype: int[100]"
        ),
    )

    ARM9_UNKNOWN_TABLE__NA_20A20B0 = Symbol(
        [0xA20B0],
        [0x20A20B0],
        0x200,
        "256*0x2\n\nNote: unverified, ported from Irdkwia's notes",
    )

    IQ_GUMMI_GAIN_TABLE = Symbol([0xA22B0], [0x20A22B0], 0x288, "type: int16_t[18][18]")

    GUMMI_BELLY_RESTORE_TABLE = Symbol(
        [0xA2538], [0x20A2538], 0x288, "type: int16_t[18][18]"
    )

    BAG_CAPACITY_TABLE_SPECIAL_EPISODES = Symbol(
        [0xA27C0],
        [0x20A27C0],
        0x14,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: uint32_t[5]",
    )

    BAG_CAPACITY_TABLE = Symbol(
        [0xA27D4],
        [0x20A27D4],
        0x20,
        (
            "Array of 4-byte integers containing the bag capacity for each bag"
            " level.\n\ntype: uint32_t[8]"
        ),
    )

    SPECIAL_EPISODE_MAIN_CHARACTERS = Symbol(
        [0xA27F4], [0x20A27F4], 0xC8, "type: struct monster_id_16[100]"
    )

    GUEST_MONSTER_DATA = Symbol(
        [0xA28BC],
        [0x20A28BC],
        0x288,
        (
            "Data for guest monsters that join you during certain story"
            " dungeons.\n\nArray of 18 36-byte entries.\n\nSee the struct definitions"
            " and End45's dungeon data document for more info.\n\ntype: struct"
            " guest_monster[18]"
        ),
    )

    RANK_UP_TABLE = Symbol([0xA2B44], [0x20A2B44], 0xD0, "")

    DS_DOWNLOAD_TEAMS = Symbol(
        [0xA2C14],
        [0x20A2C14],
        0x70,
        (
            "Seems like this is just a collection of null-terminated lists concatenated"
            " together.\n\nNote: unverified, ported from Irdkwia's notes\n\nstruct"
            " monster_id_16[56]"
        ),
    )

    ARM9_UNKNOWN_PTR__NA_20A2C84 = Symbol(
        [0xA2C84], [0x20A2C84], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    UNOWN_SPECIES_ADDITIONAL_CHARS = Symbol(
        [0xA2C88],
        [0x20A2C88],
        0x80,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: enum monster_id[28]",
    )

    MONSTER_SPRITE_DATA = Symbol([0xA2D08], [0x20A2D08], 0x4B0, "")

    REMOTE_STRINGS = Symbol(
        [0xA3B40], [0x20A3B40], 0x2C, "Note: unverified, ported from Irdkwia's notes"
    )

    RANK_STRINGS_1 = Symbol(
        [0xA3B6C], [0x20A3B6C], 0x30, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_MENU_STRING_IDS_1 = Symbol(
        [0xA3B9C],
        [0x20A3B9C],
        0x10,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[8]",
    )

    RANK_STRINGS_2 = Symbol(
        [0xA3BAC], [0x20A3BAC], 0x30, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_MENU_STRING_IDS_2 = Symbol(
        [0xA3BDC],
        [0x20A3BDC],
        0x10,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[8]",
    )

    RANK_STRINGS_3 = Symbol(
        [0xA3BEC], [0x20A3BEC], 0xB4, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_DUNGEON_UNLOCK_TABLE = Symbol(
        [0xA3CAC],
        [0x20A3CAC],
        0x6,
        (
            "Irdkwia's notes: SpecialDungeonMissions\n\ntype: struct"
            " dungeon_unlock_entry[3]"
        ),
    )

    NO_SEND_ITEM_TABLE = Symbol(
        [0xA3CB2],
        [0x20A3CB2],
        0x6,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: struct item_id_16[3]",
    )

    ARM9_UNKNOWN_TABLE__NA_20A3CC8 = Symbol(
        [0xA3CC8],
        [0x20A3CC8],
        0x1C,
        (
            "14*0x2\nLinked to ARM9_UNKNOWN_TABLE__NA_20A3CE4\n\nNote: unverified,"
            " ported from Irdkwia's notes"
        ),
    )

    ARM9_UNKNOWN_TABLE__NA_20A3CE4 = Symbol(
        [0xA3CE4],
        [0x20A3CE4],
        0x10,
        "8*0x2\n\nNote: unverified, ported from Irdkwia's notes",
    )

    ARM9_UNKNOWN_FUNCTION_TABLE__NA_20A3CF4 = Symbol(
        [0xA3CF4],
        [0x20A3CF4],
        0x20,
        "Could be related to missions\n\nNote: unverified, ported from Irdkwia's notes",
    )

    MISSION_BANNED_STORY_MONSTERS = Symbol(
        [0xA3D14],
        [0x20A3D14],
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
        [0xA3D3E],
        [0x20A3D3E],
        0x2E,
        (
            "Maybe it is the Item table used for Item Deliveries\n\nNote: unverified,"
            " ported from Irdkwia's notes\n\ntype: struct item_id_16[23]"
        ),
    )

    MISSION_RANK_POINTS = Symbol(
        [0xA3D6C],
        [0x20A3D6C],
        0x40,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int[16]",
    )

    MISSION_BANNED_MONSTERS = Symbol(
        [0xA3DAC],
        [0x20A3DAC],
        0xF8,
        (
            "Null-terminated list of monster IDs that can't be used (probably as"
            " clients or targets) when generating missions.\n\ntype: struct"
            " monster_id_16[124]"
        ),
    )

    MISSION_STRING_IDS = Symbol(
        [0xA3EA4],
        [0x20A3EA4],
        0x788,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[964]",
    )

    LEVEL_LIST = Symbol(
        [0xA46EC], [0x20A46EC], 0x21D0, "Note: unverified, ported from Irdkwia's notes"
    )

    EVENTS = Symbol(
        [0xA5488],
        [0x20A5488],
        0x1434,
        (
            "Table of levels for the script engine, in which scenes can take place."
            " There are a version-dependent number of 12-byte entries.\n\ntype: struct"
            " script_level[length / 12]"
        ),
    )

    ARM9_UNKNOWN_TABLE__NA_20A68BC = Symbol(
        [0xA68BC],
        [0x20A68BC],
        0xC,
        "6*0x2\n\nNote: unverified, ported from Irdkwia's notes",
    )

    DEMO_TEAMS = Symbol(
        [0xA68C8],
        [0x20A68C8],
        0x48,
        (
            "18*0x4 (Hero ID 0x2, Partner ID 0x2)\n\nNote: unverified, ported from"
            " Irdkwia's notes"
        ),
    )

    ACTOR_LIST = Symbol(
        [0xA6910], [0x20A6910], 0x28F8, "Note: unverified, ported from Irdkwia's notes"
    )

    ENTITIES = Symbol(
        [0xA7FF0],
        [0x20A7FF0],
        0x1218,
        (
            "Table of entities for the script engine, which can move around and do"
            " things within a scene. There are 386 12-byte entries.\n\ntype: struct"
            " script_entity[386]"
        ),
    )

    JOB_D_BOX_LAYOUT_1 = Symbol(
        [0xA9218], [0x20A9218], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_1 = Symbol(
        [0xA9228], [0x20A9228], 0x20, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_2 = Symbol(
        [0xA9248], [0x20A9248], 0x20, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_3 = Symbol(
        [0xA92B8], [0x20A92B8], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_4 = Symbol(
        [0xA92D0], [0x20A92D0], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_5 = Symbol(
        [0xA92E8], [0x20A92E8], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_6 = Symbol(
        [0xA9300], [0x20A9300], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_7 = Symbol(
        [0xA9318], [0x20A9318], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_8 = Symbol(
        [0xA9330], [0x20A9330], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_9 = Symbol(
        [0xA9348], [0x20A9348], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_10 = Symbol(
        [0xA9360], [0x20A9360], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_11 = Symbol(
        [0xA9378], [0x20A9378], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_12 = Symbol(
        [0xA9390], [0x20A9390], 0x20, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_13 = Symbol(
        [0xA93B0], [0x20A93B0], 0x20, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_D_BOX_LAYOUT_2 = Symbol(
        [0xA93D0], [0x20A93D0], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_SWAP_ID_TABLE = Symbol(
        [0xA93E0],
        [0x20A93E0],
        0xD4,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " dungeon_id_8[212]"
        ),
    )

    MAP_MARKER_PLACEMENTS = Symbol(
        [0xA94D0],
        [0x20A94D0],
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
        [0xA9FB0],
        [0x20A9FB0],
        0x4974,
        "4701*0x4\n\nNote: unverified, ported from Irdkwia's notes",
    )

    ARM9_UNKNOWN_TABLE__NA_20AE924 = Symbol(
        [0xAE924],
        [0x20AE924],
        0x2D4,
        "724*0x1\n\nNote: unverified, ported from Irdkwia's notes",
    )

    MEMORY_ALLOCATION_ARENA_GETTERS = Symbol(
        [0xAEF00],
        [0x20AEF00],
        0x8,
        (
            "Functions to get the desired memory arena for allocating and freeing heap"
            " memory.\n\ntype: struct mem_arena_getters"
        ),
    )

    PRNG_SEQUENCE_NUM = Symbol(
        [0xAEF2C],
        [0x20AEF2C],
        0x2,
        (
            "[Runtime] The current PRNG sequence number for the general-purpose PRNG."
            " See Rand16Bit for more information on how the general-purpose PRNG works."
        ),
    )

    LOADED_OVERLAY_GROUP_0 = Symbol(
        [0xAF230],
        [0x20AF230],
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
        [0xAF234],
        [0x20AF234],
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
        [0xAF238],
        [0x20AF238],
        0x4,
        (
            "[Runtime] The overlay group ID of the overlay currently loaded in slot 2."
            " A group ID of 0 denotes no overlay.\n\nOverlay group IDs that can be"
            " loaded in slot 2:\n- 0x1 (overlay 0)\n- 0x2 (overlay 10)\n- 0x3 (overlay"
            " 35)\n\ntype: enum overlay_group_id"
        ),
    )

    PACK_FILE_OPENED = Symbol(
        None,
        None,
        None,
        (
            "[Runtime] A pointer to the 6 opened Pack files (listed at"
            " PACK_FILE_PATHS_TABLE)\n\ntype: struct pack_file_opened*"
        ),
    )

    PACK_FILE_PATHS_TABLE = Symbol(
        [0xAF6A0],
        [0x20AF6A0],
        0x18,
        (
            "List of pointers to path strings to all known pack files.\nThe game uses"
            " this table to load its resources when launching dungeon mode.\n\ntype:"
            " char*[6]"
        ),
    )

    GAME_STATE_VALUES = Symbol([0xAF6B8], [0x20AF6B8], None, "[Runtime]")

    BAG_ITEMS_PTR_MIRROR = Symbol(
        [0xAF6B8],
        [0x20AF6B8],
        0x4,
        (
            "[Runtime] Probably a mirror of ram.yml::BAG_ITEMS_PTR?\n\nNote:"
            " unverified, ported from Irdkwia's notes"
        ),
    )

    ITEM_DATA_TABLE_PTRS = Symbol(
        [0xAF6C0],
        [0x20AF6C0],
        0xC,
        (
            "[Runtime] List of pointers to various item data tables.\n\nThe first two"
            " pointers are definitely item-related (although the order appears to be"
            " flipped between EU/NA?). Not sure about the third pointer."
        ),
    )

    DUNGEON_MOVE_TABLES = Symbol(
        [0xAF6DC],
        [0x20AF6DC],
        None,
        (
            "[Runtime] Seems to be some sort of region (a table of tables?) that holds"
            " pointers to various important tables related to moves."
        ),
    )

    MOVE_DATA_TABLE_PTR = Symbol(
        [0xAF6E4],
        [0x20AF6E4],
        0x4,
        (
            "[Runtime] Points to the contents of the move data table loaded from"
            " waza_p.bin\n\ntype: struct move_data_table*"
        ),
    )

    LOADED_WAN_TABLE_PTR = Symbol(
        [0xAFC68],
        [0x20AFC68],
        0x4,
        "pointer to a wan table\n\nNote: unverified, ported from Irdkwia's notes",
    )

    LANGUAGE_INFO_DATA = Symbol([0xAFCE8], [0x20AFCE8], None, "[Runtime]")

    TBL_TALK_GROUP_STRING_ID_START = Symbol(
        [0xAFCF8],
        [0x20AFCF8],
        0xC,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[6]",
    )

    KEYBOARD_STRING_IDS = Symbol(
        [0xAFDFC],
        [0x20AFDFC],
        0x3C,
        "30*0x2\n\nNote: unverified, ported from Irdkwia's notes\n\ntype: int16_t[30]",
    )

    NOTIFY_NOTE = Symbol(
        [0xAFEF8],
        [0x20AFEF8],
        0x1,
        "[Runtime] Flag related to saving and loading state?\n\ntype: bool",
    )

    DEFAULT_HERO_ID = Symbol(
        [0xAFEFC],
        [0x20AFEFC],
        0x2,
        (
            "The default monster ID for the hero (0x4: Charmander)\n\ntype: struct"
            " monster_id_16"
        ),
    )

    DEFAULT_PARTNER_ID = Symbol(
        [0xAFEFE],
        [0x20AFEFE],
        0x2,
        (
            "The default monster ID for the partner (0x1: Bulbasaur)\n\ntype: struct"
            " monster_id_16"
        ),
    )

    GAME_MODE = Symbol([0xAFF70], [0x20AFF70], 0x1, "[Runtime]\n\ntype: uint8_t")

    GLOBAL_PROGRESS_PTR = Symbol(
        [0xAFF74], [0x20AFF74], 0x4, "[Runtime]\n\ntype: struct global_progress*"
    )

    ADVENTURE_LOG_PTR = Symbol(
        [0xAFF78], [0x20AFF78], 0x4, "[Runtime]\n\ntype: struct adventure_log*"
    )

    ITEM_TABLES_PTRS_1 = Symbol(
        [0xB0948],
        [0x20B0948],
        0x68,
        "Irdkwia's notes: 26*0x4, uses MISSION_FLOOR_RANKS_AND_ITEM_LISTS",
    )

    UNOWN_SPECIES_ADDITIONAL_CHAR_PTR_TABLE = Symbol(
        [0xB09D8],
        [0x20B09D8],
        0x70,
        (
            "Uses UNOWN_SPECIES_ADDITIONAL_CHARS\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\ntype: enum monster_id*[28]"
        ),
    )

    PARTY_MONSTERS_PTR = Symbol(
        [0xB0A48], [0x20B0A48], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_LIST_PTR = Symbol(
        [0xB0A78], [0x20B0A78], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    REMOTE_STRING_PTR_TABLE = Symbol(
        [0xB0A7C],
        [0x20B0A7C],
        0x1C,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: const char*[7]",
    )

    RANK_STRING_PTR_TABLE = Symbol(
        [0xB0A98],
        [0x20B0A98],
        0x40,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: const char*[16]",
    )

    SMD_EVENTS_FUN_TABLE = Symbol(
        [0xB0B90],
        [0x20B0B90],
        0x1FC,
        (
            "Irdkwia's notes: named DSEEventFunctionPtrTable with length 0x3C0 (note"
            " the disagreement), 240*0x4."
        ),
    )

    MUSIC_DURATION_LOOKUP_TABLE_1 = Symbol(
        [0xB0F50],
        [0x20B0F50],
        0x100,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[128]",
    )

    MUSIC_DURATION_LOOKUP_TABLE_2 = Symbol(
        [0xB1050],
        [0x20B1050],
        0x200,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int32_t[128]",
    )

    JUICE_BAR_NECTAR_IQ_GAIN = Symbol(
        [0x11810], [0x2011810], 0x1, "IQ gain when ingesting nectar at the Juice Bar."
    )

    TEXT_SPEED = Symbol([0x20C98], [0x2020C98], None, "Controls text speed.")

    HERO_START_LEVEL = Symbol(
        [0x48880], [0x2048880], None, "Starting level of the hero."
    )

    PARTNER_START_LEVEL = Symbol(
        [0x488F0], [0x20488F0], None, "Starting level of the partner."
    )


class NaArm9Section:
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
    length = 0xB73F8
    functions = NaArm9Functions
    data = NaArm9Data


class NaItcmFunctions:
    GetKeyN2MSwitch = Symbol(
        [0x1434],
        [0x20B47B4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: key\nr1: switch",
    )

    GetKeyN2M = Symbol(
        [0x1468],
        [0x20B47E8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: key\nreturn: monster ID",
    )

    GetKeyN2MBaseForm = Symbol(
        [0x14D4],
        [0x20B4854],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: key\nreturn: monster ID",
    )

    GetKeyM2NSwitch = Symbol(
        [0x150C],
        [0x20B488C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nr1: switch",
    )

    GetKeyM2N = Symbol(
        [0x1540],
        [0x20B48C0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn: key",
    )

    GetKeyM2NBaseForm = Symbol(
        [0x15AC],
        [0x20B492C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn: key",
    )

    ShouldMonsterRunAwayVariationOutlawCheck = Symbol(
        [0x2390],
        [0x20B5710],
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
        [0x20B5744],
        None,
        (
            "Used by the AI to determine the direction in which a monster should"
            " move\n\nr0: Entity pointer\nr1: ?"
        ),
    )

    CalculateAiTargetPos = Symbol(
        [0x32C8],
        [0x20B6648],
        None,
        (
            "Calculates the target position of an AI-controlled monster and stores it"
            " in the monster's ai_target_pos field\n\nr0: Entity pointer"
        ),
    )

    ChooseAiMove = Symbol(
        [0x3658],
        [0x20B69D8],
        None,
        (
            "Determines if an AI-controlled monster will use a move and which one it"
            " will use\n\nr0: Entity pointer"
        ),
    )


class NaItcmData:
    MEMORY_ALLOCATION_TABLE = Symbol(
        [0x0],
        [0x20B3380],
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
        [0x20B3384],
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
        [0x20B33C0],
        0x1800,
        (
            "[Runtime] The block array for DEFAULT_MEMORY_ARENA.\n\nNote: This symbol"
            " isn't actually part of the ITCM, it gets created at runtime on the spot"
            " in RAM that used to contain the code that was moved to the ITCM.\n\ntype:"
            " struct mem_block[256]"
        ),
    )


class NaItcmSection:
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
    loadaddress = 0x20B3380
    length = 0x4000
    functions = NaItcmFunctions
    data = NaItcmData


class NaMove_effectsFunctions:
    DoMoveDamage = Symbol(
        [0x0, 0x4740, 0x5AF0, 0x7FC8],
        [0x2325DC0, 0x232A500, 0x232B8B0, 0x232DD88],
        None,
        (
            "Move effect: Deal damage.\nRelevant moves: Many!\n\nThis just wraps"
            " DealDamage with a multiplier of 1 (i.e., the fixed-point number"
            " 0x100).\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3: item"
            " ID\nreturn: whether or not damage was dealt"
        ),
    )

    DoMoveIronTail = Symbol(
        [0x24],
        [0x2325DE4],
        None,
        (
            "Move effect: Iron Tail\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageMultihitUntilMiss = Symbol(
        [0xA4],
        [0x2325E64],
        None,
        (
            "Move effect: Deal multihit damage until a strike misses\nRelevant moves:"
            " Ice Ball, Rollout\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveYawn = Symbol(
        [0x104],
        [0x2325EC4],
        None,
        (
            "Move effect: Yawn\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSleep = Symbol(
        [0x140],
        [0x2325F00],
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
        [0x2325F3C],
        None,
        (
            "Move effect: Nightmare\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMorningSun = Symbol(
        [0x1B4],
        [0x2325F74],
        None,
        (
            "Move effect: Morning Sun\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveVitalThrow = Symbol(
        [0x1F4],
        [0x2325FB4],
        None,
        (
            "Move effect: Vital Throw\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDig = Symbol(
        [0x204],
        [0x2325FC4],
        None,
        (
            "Move effect: Dig\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSweetScent = Symbol(
        [0x2C8],
        [0x2326088],
        None,
        (
            "Move effect: Sweet Scent\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveCharm = Symbol(
        [0x2E8],
        [0x23260A8],
        None,
        (
            "Move effect: Charm\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRainDance = Symbol(
        [0x310],
        [0x23260D0],
        None,
        (
            "Move effect: Rain Dance\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHail = Symbol(
        [0x36C],
        [0x232612C],
        None,
        (
            "Move effect: Hail\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHealStatus = Symbol(
        [0x3C8],
        [0x2326188],
        None,
        (
            "Move effect: Heal the team's status conditions\nRelevant moves:"
            " Aromatherapy, Heal Bell, Refresh\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveBubble = Symbol(
        [0x3E0],
        [0x23261A0],
        None,
        (
            "Move effect: Bubble\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveEncore = Symbol(
        [0x44C],
        [0x232620C],
        None,
        (
            "Move effect: Encore\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRage = Symbol(
        [0x460],
        [0x2326220],
        None,
        (
            "Move effect: Rage\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSuperFang = Symbol(
        [0x4A4],
        [0x2326264],
        None,
        (
            "Move effect: Super Fang\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePainSplit = Symbol(
        [0x55C],
        [0x232631C],
        None,
        (
            "Move effect: Pain Split\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveTorment = Symbol(
        [0x648],
        [0x2326408],
        None,
        (
            "Move effect: Torment\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveStringShot = Symbol(
        [0x790],
        [0x2326550],
        None,
        (
            "Move effect: String Shot\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSwagger = Symbol(
        [0x7A8],
        [0x2326568],
        None,
        (
            "Move effect: Swagger\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSnore = Symbol(
        [0x7E4],
        [0x23265A4],
        None,
        (
            "Move effect: Snore\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveScreech = Symbol(
        [0x888],
        [0x2326648],
        None,
        (
            "Move effect: Screech\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageCringe30 = Symbol(
        [0x8B0],
        [0x2326670],
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
        [0x23266DC],
        None,
        (
            "Move effect: Weather Ball\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveWhirlpool = Symbol(
        [0x990],
        [0x2326750],
        None,
        (
            "Move effect: Whirlpool\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFakeTears = Symbol(
        [0xA18],
        [0x23267D8],
        None,
        (
            "Move effect: Fake Tears\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSpite = Symbol(
        [0xA4C],
        [0x232680C],
        None,
        (
            "Move effect: Spite\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFocusEnergy = Symbol(
        [0xAFC],
        [0x23268BC],
        None,
        (
            "Move effect: Focus Energy\nRelevant moves: Focus Energy,"
            " MOVE_TAG_0x1AC\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSmokescreen = Symbol(
        [0xB0C],
        [0x23268CC],
        None,
        (
            "Move effect: Smokescreen\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMirrorMove = Symbol(
        [0xB48],
        [0x2326908],
        None,
        (
            "Move effect: Mirror Move\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveOverheat = Symbol(
        [0xB6C],
        [0x232692C],
        None,
        (
            "Move effect: Overheat\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveAuroraBeam = Symbol(
        [0xBD0],
        [0x2326990],
        None,
        (
            "Move effect: Aurora Beam\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMemento = Symbol(
        [0xC4C],
        [0x2326A0C],
        None,
        (
            "Move effect: Memento\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveOctazooka = Symbol(
        [0xCB4],
        [0x2326A74],
        None,
        (
            "Move effect: Octazooka\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFlatter = Symbol(
        [0xD28],
        [0x2326AE8],
        None,
        (
            "Move effect: Flatter\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveWillOWisp = Symbol(
        [0xD64],
        [0x2326B24],
        None,
        (
            "Move effect: Will-O-Wisp\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveReturn = Symbol(
        [0xE00],
        [0x2326BC0],
        None,
        (
            "Move effect: Return\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveGrudge = Symbol(
        [0xEE4],
        [0x2326CA4],
        None,
        (
            "Move effect: Grudge\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveCounter = Symbol(
        [0xEF4],
        [0x2326CB4],
        None,
        (
            "Move effect: Give the user the Counter status\nRelevant moves: Pursuit,"
            " Counter, Payback\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageBurn10FlameWheel = Symbol(
        [0xF08],
        [0x2326CC8],
        None,
        (
            "Move effect: Deal damage with a 10% chance (FLAME_WHEEL_BURN_CHANCE) of"
            " burning the defender.\nRelevant moves: Flame Wheel, Lava Plume\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveDamageBurn10 = Symbol(
        [0xF90],
        [0x2326D50],
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
        [0x2326DD8],
        None,
        (
            "Move effect: Expose all Ghost-type enemies, and reset evasion"
            " boosts\nRelevant moves: Odor Sleuth, Foresight\n\nr0: attacker"
            " pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn: whether the"
            " move was successfully used"
        ),
    )

    DoMoveDoubleTeam = Symbol(
        [0x1044],
        [0x2326E04],
        None,
        (
            "Move effect: Double Team\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveGust = Symbol(
        [0x1060],
        [0x2326E20],
        None,
        (
            "Move effect: Gust\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBoostDefense1 = Symbol(
        [0x10A0],
        [0x2326E60],
        None,
        (
            "Move effect: Boost the user's defense by one stage\nRelevant moves:"
            " Harden, Withdraw\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveParalyze = Symbol(
        [0x10C0, 0x2470, 0x5674],
        [0x2326E80, 0x2328230, 0x232B434],
        None,
        (
            "Move effect: Paralyze the defender if possible\nRelevant moves: Disable,"
            " Stun Spore, Glare\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBoostAttack1 = Symbol(
        [0x10D8],
        [0x2326E98],
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
        [0x2326EB8],
        None,
        (
            "Move effect: Razor Wind\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBide = Symbol(
        [0x1188],
        [0x2326F48],
        None,
        (
            "Move effect: Give the user the Bide status\nRelevant moves: Bide, Revenge,"
            " Avalanche\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBideUnleash = Symbol(
        [0x11CC],
        [0x2326F8C],
        None,
        (
            "Move effect: Unleashes the Bide status\nRelevant moves: Bide (unleashing),"
            " Revenge (unleashing), Avalanche (unleashing)\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveCrunch = Symbol(
        [0x1274],
        [0x2327034],
        None,
        (
            "Move effect: Deal damage with a 20% chance (CRUNCH_LOWER_DEFENSE_CHANCE)"
            " of lowering the defender's defense.\nRelevant moves: Crunch, Shadow Ball"
            " via Nature Power\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether or not damage was dealt"
        ),
    )

    DoMoveDamageCringe20 = Symbol(
        [0x12F4],
        [0x23270B4],
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
        [0x1360],
        [0x2327120],
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
        [0x232718C],
        None,
        (
            "Move effect: Endeavor\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFacade = Symbol(
        [0x148C],
        [0x232724C],
        None,
        (
            "Move effect: Facade\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageLowerSpeed20 = Symbol(
        [0x14CC],
        [0x232728C],
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
        [0x23272F8],
        None,
        (
            "Move effect: Brick Break\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDamageLowerSpeed100 = Symbol(
        [0x15A8],
        [0x2327368],
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
        [0x23273CC],
        None,
        (
            "Move effect: Focus Punch\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDamageDrain = Symbol(
        [0x1698],
        [0x2327458],
        None,
        (
            "Move effect: Deal draining damage, healing the attacker by a proportion of"
            " the damage dealt.\nRelevant moves: Giga Drain, Leech Life, Mega Drain,"
            " Drain Punch\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether or not damage was dealt"
        ),
    )

    DoMoveReversal = Symbol(
        [0x17D8],
        [0x2327598],
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
        [0x232764C],
        None,
        (
            "Move effect: SmellingSalt\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMetalSound = Symbol(
        [0x18F4],
        [0x23276B4],
        None,
        (
            "Move effect: Metal Sound\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTickle = Symbol(
        [0x1928],
        [0x23276E8],
        None,
        (
            "Move effect: Tickle\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveShadowHold = Symbol(
        [0x1984],
        [0x2327744],
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
        [0x2327758],
        None,
        (
            "Move effect: Haze\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageMultihitFatigue = Symbol(
        [0x19AC],
        [0x232776C],
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
        [0x23277B8],
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
        [0x2327804],
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
        [0x1B28],
        [0x23278E8],
        None,
        (
            "Move effect: Synthesis\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBoostSpeed1 = Symbol(
        [0x1B68],
        [0x2327928],
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
        [0x2327940],
        None,
        (
            "Move effect: Rapid Spin\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSureShot = Symbol(
        [0x1BEC],
        [0x23279AC],
        None,
        (
            "Move effect: Give the user the Sure-Shot status\nRelevant moves: Mind"
            " Reader, Lock-On\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveCosmicPower = Symbol(
        [0x1C24],
        [0x23279E4],
        None,
        (
            "Move effect: Cosmic Power\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSkyAttack = Symbol(
        [0x1C68],
        [0x2327A28],
        None,
        (
            "Move effect: Sky Attack\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageFreeze15 = Symbol(
        [0x1D34],
        [0x2327AF4],
        None,
        (
            "Move effect: Deal damage with a 15% chance (POWDER_SNOW_FREEZE_CHANCE) of"
            " freezing the defender.\nRelevant moves: Powder Snow, Blizzard, Ice Punch,"
            " Ice Beam\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether or not damage was dealt"
        ),
    )

    DoMoveMeteorMash = Symbol(
        [0x1D9C],
        [0x2327B5C],
        None,
        (
            "Move effect: Meteor Mash\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveEndure = Symbol(
        [0x1E20],
        [0x2327BE0],
        None,
        (
            "Move effect: Endure\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveLowerSpeed1 = Symbol(
        [0x1E30],
        [0x2327BF0],
        None,
        (
            "Move effect: Lower the defender's defense by one stage\nRelevant moves:"
            " Scary Face, Cotton Spore\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDamageConfuse10 = Symbol(
        [0x1E48],
        [0x2327C08],
        None,
        (
            "Move effect: Deal damage with a 10% chance (PSYBEAM_CONFUSE_CHANCE) of"
            " confusing the defender.\nRelevant moves: Psybeam, Signal Beam, Confusion,"
            " Chatter, Rock Climb\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePsywave = Symbol(
        [0x1EB4],
        [0x2327C74],
        None,
        (
            "Move effect: Psywave\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageLowerDefensiveStatVariable = Symbol(
        [0x1F18],
        [0x2327CD8],
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
        [0x1FA0],
        [0x2327D60],
        None,
        (
            "Move effect: Psycho Boost\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveUproar = Symbol(
        [0x2010],
        [0x2327DD0],
        None,
        (
            "Move effect: Uproar\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveWaterSpout = Symbol(
        [0x2020],
        [0x2327DE0],
        None,
        (
            "Move effect: Water Spout\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMovePsychUp = Symbol(
        [0x20D4],
        [0x2327E94],
        None,
        (
            "Move effect: Psych Up\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageWithRecoil = Symbol(
        [0x2174],
        [0x2327F34],
        None,
        (
            "Move effect: Deals damage, inflicting recoil damage on the"
            " attacker.\nRelevant moves: Submission, Take Down, Volt Tackle, Wood"
            " Hammer, Brave Bird\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: bool, whether or not damage was dealt"
        ),
    )

    EntityIsValidMoveEffects = Symbol(
        [0x224C, 0x4618, 0x6740, 0x8490],
        [0x232800C, 0x232A3D8, 0x232C500, 0x232E250],
        None,
        "See overlay29.yml::EntityIsValid",
    )

    DoMoveRecoverHp = Symbol(
        [0x2270],
        [0x2328030],
        None,
        (
            "Move effect: Recover 50% of the user's max HP\nRelevant moves: Recover,"
            " Slack Off\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveEarthquake = Symbol(
        [0x22B4],
        [0x2328074],
        None,
        (
            "Move effect: Earthquake\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    GetNaturePowerVariant = Symbol(
        [0x2314],
        [0x23280D4],
        None,
        (
            "Gets the nature power variant for the current dungeon, based on the"
            " tileset ID.\n\nreturn: nature power variant"
        ),
    )

    DoMoveNaturePower = Symbol(
        [0x2350],
        [0x2328110],
        None,
        (
            "Move effect: Nature Power\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move (unused)\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveDamageParalyze10 = Symbol(
        [0x23AC],
        [0x232816C],
        None,
        (
            "Move effect: Deal damage with a 10% chance (LICK_PARALZYE_CHANCE) of"
            " paralyzing the defender.\nRelevant moves: Lick, Spark, Body Slam,"
            " DragonBreath\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSelfdestruct = Symbol(
        [0x2418],
        [0x23281D8],
        None,
        (
            "Move effect: Selfdestruct\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveShadowBall = Symbol(
        [0x2488],
        [0x2328248],
        None,
        (
            "Move effect: Shadow Ball\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveCharge = Symbol(
        [0x2508],
        [0x23282C8],
        None,
        (
            "Move effect: Charge\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveThunderbolt = Symbol(
        [0x2568],
        [0x2328328],
        None,
        (
            "Move effect: Thunderbolt\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMist = Symbol(
        [0x25D4],
        [0x2328394],
        None,
        (
            "Move effect: Mist\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFissure = Symbol(
        [0x25E4],
        [0x23283A4],
        None,
        (
            "Move effect: Fissure\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageCringe10 = Symbol(
        [0x26FC],
        [0x23284BC],
        None,
        (
            "Move effect: Deal damage with a 10% chance (EXTRASENSORY_CRINGE_CHANCE) to"
            " inflict the cringe status on the defender.\nRelevant moves: Extrasensory,"
            " Hyper Fang, Bone Club\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSafeguard = Symbol(
        [0x2768],
        [0x2328528],
        None,
        (
            "Move effect: Safeguard\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveAbsorb = Symbol(
        [0x2778],
        [0x2328538],
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
        [0x2874, 0x4154, 0x6010, 0x8060],
        [0x2328634, 0x2329F14, 0x232BDD0, 0x232DE20],
        None,
        "See overlay29.yml::DefenderAbilityIsActive",
    )

    DoMoveSkillSwap = Symbol(
        [0x28D8],
        [0x2328698],
        None,
        (
            "Move effect: Skill Swap\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSketch = Symbol(
        [0x29D4],
        [0x2328794],
        None,
        (
            "Move effect: Sketch\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHeadbutt = Symbol(
        [0x2B04],
        [0x23288C4],
        None,
        (
            "Move effect: Headbutt\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDoubleEdge = Symbol(
        [0x2B70],
        [0x2328930],
        None,
        (
            "Move effect: Double-Edge\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSandstorm = Symbol(
        [0x2C38],
        [0x23289F8],
        None,
        (
            "Move effect: Sandstorm\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveLowerAccuracy1 = Symbol(
        [0x2C94],
        [0x2328A54],
        None,
        (
            "Move effect: Lower the defender's accuracy by one stage\nRelevant moves:"
            " Sand-Attack, Kinesis, Flash\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDamagePoison40 = Symbol(
        [0x2CB4],
        [0x2328A74],
        None,
        (
            "Move effect: Deal damage with a 40% chance (SMOG_POISON_CHANCE) of"
            " poisoning the defender.\nRelevant moves: Smog, Cross Poison, Gunk Shot,"
            " Poison Jab\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether or not damage was dealt"
        ),
    )

    DoMoveGrowth = Symbol(
        [0x2D20],
        [0x2328AE0],
        None,
        (
            "Move effect: Growth\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSacredFire = Symbol(
        [0x2D40],
        [0x2328B00],
        None,
        (
            "Move effect: Sacred Fire\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveOhko = Symbol(
        [0x2DC8],
        [0x2328B88],
        None,
        (
            "Move effect: Possibly one-hit KO the defender\nRelevant moves: Sheer Cold,"
            " Guillotine\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSolarBeam = Symbol(
        [0x2EB4],
        [0x2328C74],
        None,
        (
            "Move effect: SolarBeam\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSonicBoom = Symbol(
        [0x2F84],
        [0x2328D44],
        None,
        (
            "Move effect: SonicBoom\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFly = Symbol(
        [0x3024],
        [0x2328DE4],
        None,
        (
            "Move effect: Fly\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveExplosion = Symbol(
        [0x30B4],
        [0x2328E74],
        None,
        (
            "Move effect: Explosion\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDive = Symbol(
        [0x310C],
        [0x2328ECC],
        None,
        (
            "Move effect: Dive\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveWaterfall = Symbol(
        [0x31D4],
        [0x2328F94],
        None,
        (
            "Move effect: Waterfall\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageLowerAccuracy40 = Symbol(
        [0x3240],
        [0x2329000],
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
        [0x32B4],
        [0x2329074],
        None,
        (
            "Move effect: Stockpile\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveTwister = Symbol(
        [0x330C],
        [0x23290CC],
        None,
        (
            "Move effect: Twister\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveTwineedle = Symbol(
        [0x339C],
        [0x232915C],
        None,
        (
            "Move effect: Twineedle\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRecoverHpTeam = Symbol(
        [0x3434],
        [0x23291F4],
        None,
        (
            "Move effect: Recover 25% HP for all team members\nRelevant moves:"
            " Softboiled, Milk Drink\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMinimize = Symbol(
        [0x347C],
        [0x232923C],
        None,
        (
            "Move effect: Minimize\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSeismicToss = Symbol(
        [0x3498],
        [0x2329258],
        None,
        (
            "Move effect: Seismic Toss\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveConfuse = Symbol(
        [0x360C],
        [0x23293CC],
        None,
        (
            "Move effect: Confuse target enemies if possible.\nRelevant moves: Confuse"
            " Ray, Supersonic, Sweet Kiss, Teeter Dance, Totter (item effect)\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveTaunt = Symbol(
        [0x3624],
        [0x23293E4],
        None,
        (
            "Move effect: Taunt\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMoonlight = Symbol(
        [0x3638],
        [0x23293F8],
        None,
        (
            "Move effect: Moonlight\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHornDrill = Symbol(
        [0x3678],
        [0x2329438],
        None,
        (
            "Move effect: Horn Drill\n\nThis is exactly the same as DoMoveOhko, except"
            " there's a call to SubstitutePlaceholderStringTags at the end.\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveSwordsDance = Symbol(
        [0x3774],
        [0x2329534],
        None,
        (
            "Move effect: Swords Dance\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveConversion = Symbol(
        [0x3794],
        [0x2329554],
        None,
        (
            "Move effect: Conversion\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveConversion2 = Symbol(
        [0x38A4],
        [0x2329664],
        None,
        (
            "Move effect: Conversion 2\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveHelpingHand = Symbol(
        [0x38B4],
        [0x2329674],
        None,
        (
            "Move effect: Helping Hand\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveBoostDefense2 = Symbol(
        [0x3918],
        [0x23296D8],
        None,
        (
            "Move effect: Boost the defender's defense stat by two stages\nRelevant"
            " moves: Iron Defense, Acid Armor, Barrier\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveWarp = Symbol(
        [0x3938],
        [0x23296F8],
        None,
        (
            "Move effect: Warp the target to another tile on the floor\nRelevant moves:"
            " Teleport, Warp (item effect), MOVE_TAG_0x1A8\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveThundershock = Symbol(
        [0x3950],
        [0x2329710],
        None,
        (
            "Move effect: Thundershock\n\nThis is identical to DoMoveDamageParalyze10,"
            " except it uses a different data symbol for the paralysis chance (but it's"
            " still 10%).\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveThunderWave = Symbol(
        [0x39BC],
        [0x232977C],
        None,
        (
            "Move effect: Thunder Wave\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveZapCannon = Symbol(
        [0x3A30],
        [0x23297F0],
        None,
        (
            "Move effect: Zap Cannon\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBlock = Symbol(
        [0x3A94],
        [0x2329854],
        None,
        (
            "Move effect: Block\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePoison = Symbol(
        [0x3AA8],
        [0x2329868],
        None,
        (
            "Move effect: Poison the defender if possible\nRelevant moves: Poison Gas,"
            " PoisonPowder\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveToxic = Symbol(
        [0x3AC0],
        [0x2329880],
        None,
        (
            "Move effect: Toxic\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePoisonFang = Symbol(
        [0x3AD8],
        [0x2329898],
        None,
        (
            "Move effect: Poison Fang\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDamagePoison18 = Symbol(
        [0x3B44],
        [0x2329904],
        None,
        (
            "Move effect: Deal damage with an 18% chance (POISON_STING_POISON_CHANCE)"
            " to poison the defender.\nRelevant moves: Poison Sting, Sludge, Sludge"
            " Bomb\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3: item"
            " ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveJumpKick = Symbol(
        [0x3BB0],
        [0x2329970],
        None,
        (
            "Move effect: Jump Kick\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBounce = Symbol(
        [0x3CDC],
        [0x2329A9C],
        None,
        (
            "Move effect: Bounce\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHiJumpKick = Symbol(
        [0x3DA8],
        [0x2329B68],
        None,
        (
            "Move effect: Hi Jump Kick\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTriAttack = Symbol(
        [0x3ED4],
        [0x2329C94],
        None,
        (
            "Move effect: Tri Attack\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSwapItems = Symbol(
        [0x3F90],
        [0x2329D50],
        None,
        (
            "Move effect: Swaps the held items of the attacker and defender.\nRelevant"
            " moves: Trick, Switcheroo\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTripleKick = Symbol(
        [0x41B8],
        [0x2329F78],
        None,
        (
            "Move effect: Triple Kick\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSport = Symbol(
        [0x41F4],
        [0x2329FB4],
        None,
        (
            "Move effect: Activate the relevant sport condition (Mud Sport, Water"
            " Sport) on the floor\nRelevant moves: Mud Sport, Water Sport\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveMudSlap = Symbol(
        [0x4220],
        [0x2329FE0],
        None,
        (
            "Move effect: Mud-Slap\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageStealItem = Symbol(
        [0x428C],
        [0x232A04C],
        None,
        (
            "Move effect: Deal damage and steal the defender's item if"
            " possible.\nRelevant moves: Thief, Covet\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveAmnesia = Symbol(
        [0x4298],
        [0x232A058],
        None,
        (
            "Move effect: Amnesia\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveNightShade = Symbol(
        [0x42B8],
        [0x232A078],
        None,
        (
            "Move effect: Night Shade\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveGrowl = Symbol(
        [0x4358],
        [0x232A118],
        None,
        (
            "Move effect: Growl\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSurf = Symbol(
        [0x4388],
        [0x232A148],
        None,
        (
            "Move effect: Surf\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRolePlay = Symbol(
        [0x43C8],
        [0x232A188],
        None,
        (
            "Move effect: Role Play\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSunnyDay = Symbol(
        [0x4460],
        [0x232A220],
        None,
        (
            "Move effect: Sunny Day\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveLowerDefense1 = Symbol(
        [0x44BC],
        [0x232A27C],
        None,
        (
            "Move effect: Lower the defender's defense by one stage\nRelevant moves:"
            " Tail Whip, Leer\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveWish = Symbol(
        [0x44EC],
        [0x232A2AC],
        None,
        (
            "Move effect: Wish\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFakeOut = Symbol(
        [0x44FC],
        [0x232A2BC],
        None,
        (
            "Move effect: Fake Out\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSleepTalk = Symbol(
        [0x4568],
        [0x232A328],
        None,
        (
            "Move effect: Sleep Talk\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePayDay = Symbol(
        [0x4580],
        [0x232A340],
        None,
        (
            "Move effect: Pay Day\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveAssist = Symbol(
        [0x463C],
        [0x232A3FC],
        None,
        (
            "Move effect: Assist\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRest = Symbol(
        [0x4654],
        [0x232A414],
        None,
        (
            "Move effect: Rest\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveIngrain = Symbol(
        [0x46C0],
        [0x232A480],
        None,
        (
            "Move effect: Ingrain\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSwallow = Symbol(
        [0x46D0],
        [0x232A490],
        None,
        (
            "Move effect: Swallow\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveCurse = Symbol(
        [0x4728],
        [0x232A4E8],
        None,
        (
            "Move effect: Curse\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSuperpower = Symbol(
        [0x4764],
        [0x232A524],
        None,
        (
            "Move effect: Superpower\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSteelWing = Symbol(
        [0x47EC],
        [0x232A5AC],
        None,
        (
            "Move effect: Steel Wing\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSpitUp = Symbol(
        [0x4880],
        [0x232A640],
        None,
        (
            "Move effect: Spit Up\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDynamicPunch = Symbol(
        [0x48C8],
        [0x232A688],
        None,
        (
            "Move effect: DynamicPunch\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveKnockOff = Symbol(
        [0x492C],
        [0x232A6EC],
        None,
        (
            "Move effect: Knock Off\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSplash = Symbol(
        [0x4B2C],
        [0x232A8EC],
        None,
        (
            "Move effect: Splash\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSetDamage = Symbol(
        [0x4E84],
        [0x232AC44],
        None,
        (
            "Move effect: Give the user the Set Damage status\nRelevant moves: Doom"
            " Desire, Future Sight\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBellyDrum = Symbol(
        [0x4E94],
        [0x232AC54],
        None,
        (
            "Move effect: Belly Drum\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveLightScreen = Symbol(
        [0x4F48],
        [0x232AD08],
        None,
        (
            "Move effect: Light Screen\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSecretPower = Symbol(
        [0x4F58],
        [0x232AD18],
        None,
        (
            "Move effect: Secret Power\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDamageConfuse30 = Symbol(
        [0x5130],
        [0x232AEF0],
        None,
        (
            "Move effect: Deal damage with a 30% chance (DIZZY_PUNCH_CONFUSE_CHANCE) to"
            " confuse the defender.\nRelevant moves: Dizzy Punch, Water Pulse\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveBulkUp = Symbol(
        [0x519C],
        [0x232AF5C],
        None,
        (
            "Move effect: Bulk Up\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePause = Symbol(
        [0x51E0],
        [0x232AFA0],
        None,
        (
            "Move effect: Inflicts the Paused status on the defender\nRelevant moves:"
            " Imprison, Observer (item effect), MOVE_TAG_0x1AD\n\nr0: attacker"
            " pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn: whether the"
            " move was successfully used"
        ),
    )

    DoMoveFeatherDance = Symbol(
        [0x5230],
        [0x232AFF0],
        None,
        (
            "Move effect: FeatherDance\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveBeatUp = Symbol(
        [0x5264],
        [0x232B024],
        None,
        (
            "Move effect: Beat Up\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBlastBurn = Symbol(
        [0x5358],
        [0x232B118],
        None,
        (
            "Move effect: Blast Burn\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveCrushClaw = Symbol(
        [0x53A4],
        [0x232B164],
        None,
        (
            "Move effect: Crush Claw\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBlazeKick = Symbol(
        [0x5424],
        [0x232B1E4],
        None,
        (
            "Move effect: Blaze Kick\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePresent = Symbol(
        [0x54AC],
        [0x232B26C],
        None,
        (
            "Move effect: Present\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveEruption = Symbol(
        [0x55A8],
        [0x232B368],
        None,
        (
            "Move effect: Eruption\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveTransform = Symbol(
        [0x568C],
        [0x232B44C],
        None,
        (
            "Move effect: Transform\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePoisonTail = Symbol(
        [0x56D4],
        [0x232B494],
        None,
        (
            "Move effect: Poison Tail\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveBlowback = Symbol(
        [0x5740],
        [0x232B500],
        None,
        (
            "Move effect: Blows the defender back\nRelevant moves: Whirlwind, Roar,"
            " Blowback (item effect)\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveCamouflage = Symbol(
        [0x5758],
        [0x232B518],
        None,
        (
            "Move effect: Camouflage\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveTailGlow = Symbol(
        [0x5808],
        [0x232B5C8],
        None,
        (
            "Move effect: Tail Glow\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageConstrict10 = Symbol(
        [0x5828],
        [0x232B5E8],
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
        [0x58E4],
        [0x232B6A4],
        None,
        (
            "Move effect: Perish Song\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveWrap = Symbol(
        [0x58F8],
        [0x232B6B8],
        None,
        (
            "Move effect: Wrap\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSpikes = Symbol(
        [0x5908],
        [0x232B6C8],
        None,
        (
            "Move effect: Spikes\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMagnitude = Symbol(
        [0x5978],
        [0x232B738],
        None,
        (
            "Move effect: Magnitude\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMagicCoat = Symbol(
        [0x5A00],
        [0x232B7C0],
        None,
        (
            "Move effect: Magic Coat\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveProtect = Symbol(
        [0x5A10],
        [0x232B7D0],
        None,
        (
            "Move effect: Try to give the user the Protect status\nRelevant moves:"
            " Protect, Detect\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDefenseCurl = Symbol(
        [0x5A20],
        [0x232B7E0],
        None,
        (
            "Move effect: Defense Curl\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDecoy = Symbol(
        [0x5A40],
        [0x232B800],
        None,
        (
            "Move effect: Inflict the Decoy status on the target\nRelevant moves:"
            " Follow Me, Substitute, Decoy Maker (item effect)\n\nr0: attacker"
            " pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn: whether the"
            " move was successfully used"
        ),
    )

    DoMoveMistBall = Symbol(
        [0x5A60],
        [0x232B820],
        None,
        (
            "Move effect: Mist Ball\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDestinyBond = Symbol(
        [0x5AE0],
        [0x232B8A0],
        None,
        (
            "Move effect: Destiny Bond\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMirrorCoat = Symbol(
        [0x5B14],
        [0x232B8D4],
        None,
        (
            "Move effect: Mirror Coat\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveCalmMind = Symbol(
        [0x5B24],
        [0x232B8E4],
        None,
        (
            "Move effect: Calm Mind\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHiddenPower = Symbol(
        [0x5B68],
        [0x232B928],
        None,
        (
            "Move effect: Hidden Power\n\nThis is exactly the same as DoMoveDamage"
            " (both are wrappers around DealDamage), except this function always"
            " returns true.\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMetalClaw = Symbol(
        [0x5B80],
        [0x232B940],
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
        [0x5C10],
        [0x232B9D0],
        None,
        (
            "Move effect: Attract\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveCopycat = Symbol(
        [0x5C84],
        [0x232BA44],
        None,
        (
            "Move effect: The attacker uses the move last used by enemy it's"
            " facing.\nRelevant moves: Mimic, Copycat\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveFrustration = Symbol(
        [0x5D8C],
        [0x232BB4C],
        None,
        (
            "Move effect: Frustration\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveLeechSeed = Symbol(
        [0x5E74],
        [0x232BC34],
        None,
        (
            "Move effect: Leech Seed\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMetronome = Symbol(
        [0x5EA4],
        [0x232BC64],
        None,
        (
            "Move effect: Metronome\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDreamEater = Symbol(
        [0x5F04],
        [0x232BCC4],
        None,
        (
            "Move effect: Dream Eater\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSnatch = Symbol(
        [0x6074],
        [0x232BE34],
        None,
        (
            "Move effect: Snatch\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRecycle = Symbol(
        [0x6084],
        [0x232BE44],
        None,
        (
            "Move effect: Recycle\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveReflect = Symbol(
        [0x61B8],
        [0x232BF78],
        None,
        (
            "Move effect: Reflect\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDragonRage = Symbol(
        [0x61C8],
        [0x232BF88],
        None,
        (
            "Move effect: Dragon Rage\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDragonDance = Symbol(
        [0x6268],
        [0x232C028],
        None,
        (
            "Move effect: Dragon Dance\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSkullBash = Symbol(
        [0x62A4],
        [0x232C064],
        None,
        (
            "Move effect: Skull Bash\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageLowerSpecialDefense50 = Symbol(
        [0x6334],
        [0x232C0F4],
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
        [0x63E4],
        [0x232C1A4],
        None,
        (
            "Move effect: Struggle\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRockSmash = Symbol(
        [0x64BC],
        [0x232C27C],
        None,
        (
            "Move effect: Rock Smash\nRelevant moves: Rock Smash,"
            " MOVE_UNNAMED_0x169\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSeeTrap = Symbol(
        [0x6540],
        [0x232C300],
        None,
        (
            "Move effect: See-Trap (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTakeaway = Symbol(
        [0x6550],
        [0x232C310],
        None,
        (
            "Move effect: Takeaway (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveRebound = Symbol(
        [0x6764],
        [0x232C524],
        None,
        (
            "Move effect: Rebound (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSwitchPositions = Symbol(
        [0x6778],
        [0x232C538],
        None,
        (
            "Move effect: Switches the user's position with positions of other monsters"
            " in the room.\nRelevant moves: Baton Pass, Switcher (item effect)\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveStayAway = Symbol(
        [0x67A0],
        [0x232C560],
        None,
        (
            "Move effect: Stay Away (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveCleanse = Symbol(
        [0x67B8],
        [0x232C578],
        None,
        (
            "Move effect: Cleanse (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSiesta = Symbol(
        [0x68F4],
        [0x232C6B4],
        None,
        (
            "Move effect: Siesta (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTwoEdge = Symbol(
        [0x6930],
        [0x232C6F0],
        None,
        (
            "Move effect: Two-Edge (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveNoMove = Symbol(
        [0x6A58],
        [0x232C818],
        None,
        (
            "Move effect: No-Move (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveScan = Symbol(
        [0x6A6C],
        [0x232C82C],
        None,
        (
            "Move effect: Scan (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMovePowerEars = Symbol(
        [0x6A7C],
        [0x232C83C],
        None,
        (
            "Move effect: Power-Ears (item effect)\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveTransfer = Symbol(
        [0x6A8C],
        [0x232C84C],
        None,
        (
            "Move effect: Transfer (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSlowDown = Symbol(
        [0x6C54],
        [0x232CA14],
        None,
        (
            "Move effect: Slow Down (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSearchlight = Symbol(
        [0x6C6C],
        [0x232CA2C],
        None,
        (
            "Move effect: Searchlight (item effect)\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMovePetrify = Symbol(
        [0x6C7C],
        [0x232CA3C],
        None,
        (
            "Move effect: Petrifies the target\nRelevant moves: Petrify (item effect),"
            " MOVE_TAG_0x1A9\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePounce = Symbol(
        [0x6C8C],
        [0x232CA4C],
        None,
        (
            "Move effect: Pounce (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTrawl = Symbol(
        [0x6CA0],
        [0x232CA60],
        None,
        (
            "Move effect: Trawl (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveEscape = Symbol(
        [0x6CB0],
        [0x232CA70],
        None,
        (
            "Move effect: Escape (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDrought = Symbol(
        [0x6D48],
        [0x232CB08],
        None,
        (
            "Move effect: Drought (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTrapBuster = Symbol(
        [0x6D58],
        [0x232CB18],
        None,
        (
            "Move effect: Trap Buster (item effect)\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveWildCall = Symbol(
        [0x6F04],
        [0x232CCC4],
        None,
        (
            "Move effect: Wild Call (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveInvisify = Symbol(
        [0x6FD0],
        [0x232CD90],
        None,
        (
            "Move effect: Invisify (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveOneShot = Symbol(
        [0x6FE4],
        [0x232CDA4],
        None,
        (
            "Move effect: One-Shot (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveHpGauge = Symbol(
        [0x7080],
        [0x232CE40],
        None,
        (
            "Move effect: HP Gauge (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveVacuumCut = Symbol(
        [0x7090],
        [0x232CE50],
        None,
        (
            "Move effect: Vacuum Cut\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveReviver = Symbol(
        [0x70BC],
        [0x232CE7C],
        None,
        (
            "Move effect: Reviver (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveShocker = Symbol(
        [0x70D4],
        [0x232CE94],
        None,
        (
            "Move effect: Shocker (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveEcho = Symbol(
        [0x70EC],
        [0x232CEAC],
        None,
        (
            "Move effect: Echo (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveFamish = Symbol(
        [0x7194],
        [0x232CF54],
        None,
        (
            "Move effect: Famish (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveOneRoom = Symbol(
        [0x71B4],
        [0x232CF74],
        None,
        (
            "Move effect: One-Room (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveFillIn = Symbol(
        [0x71C4],
        [0x232CF84],
        None,
        (
            "Move effect: Fill-In (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTrapper = Symbol(
        [0x7330],
        [0x232D0F0],
        None,
        (
            "Move effect: Trapper (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveItemize = Symbol(
        [0x7388],
        [0x232D148],
        None,
        (
            "Move effect: Itemize (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveHurl = Symbol(
        [0x741C],
        [0x232D1DC],
        None,
        (
            "Move effect: Hurls the target\nRelevant moves: Strength, Hurl (item"
            " effect), Fling\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMobile = Symbol(
        [0x742C],
        [0x232D1EC],
        None,
        (
            "Move effect: Mobile (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSeeStairs = Symbol(
        [0x743C],
        [0x232D1FC],
        None,
        (
            "Move effect: See Stairs (item effect)\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveLongToss = Symbol(
        [0x744C],
        [0x232D20C],
        None,
        (
            "Move effect: Long Toss (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMovePierce = Symbol(
        [0x745C],
        [0x232D21C],
        None,
        (
            "Move effect: Pierce (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoHammerArm = Symbol(
        [0x746C],
        [0x232D22C],
        None,
        (
            "Move effect: Hammer Arm\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveAquaRing = Symbol(
        [0x74B0],
        [0x232D270],
        None,
        (
            "Move effect: Aqua Ring\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveGastroAcid = Symbol(
        [0x74C0],
        [0x232D280],
        None,
        (
            "Move effect: Gastro Acid\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveHealingWish = Symbol(
        [0x74D8],
        [0x232D298],
        None,
        (
            "Move effect: Healing Wish\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveCloseCombat = Symbol(
        [0x7528],
        [0x232D2E8],
        None,
        (
            "Move effect: Close Combat\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveLuckyChant = Symbol(
        [0x75A8],
        [0x232D368],
        None,
        (
            "Move effect: Lucky Chant\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveGuardSwap = Symbol(
        [0x75B8],
        [0x232D378],
        None,
        (
            "Move effect: Guard Swap\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHealOrder = Symbol(
        [0x7618],
        [0x232D3D8],
        None,
        (
            "Move effect: Heal Order\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHealBlock = Symbol(
        [0x7640],
        [0x232D400],
        None,
        (
            "Move effect: Heal Block\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveThunderFang = Symbol(
        [0x7658],
        [0x232D418],
        None,
        (
            "Move effect: Thunder Fang\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDefog = Symbol(
        [0x76EC],
        [0x232D4AC],
        None,
        (
            "Move effect: Defog\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveTrumpCard = Symbol(
        [0x77A0],
        [0x232D560],
        None,
        (
            "Move effect: Trump Card\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveIceFang = Symbol(
        [0x7860],
        [0x232D620],
        None,
        (
            "Move effect: Ice Fang\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePsychoShift = Symbol(
        [0x78F0],
        [0x232D6B0],
        None,
        (
            "Move effect: Psycho Shift\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveEmbargo = Symbol(
        [0x7910],
        [0x232D6D0],
        None,
        (
            "Move effect: Embargo\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBrine = Symbol(
        [0x7928],
        [0x232D6E8],
        None,
        (
            "Move effect: Deal damage, with a 2x multiplier if the defender is at or"
            " below half HP.\nRelevant moves: Brine, Assurance\n\nr0: attacker"
            " pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn: whether the"
            " move was successfully used"
        ),
    )

    DoMoveNaturalGift = Symbol(
        [0x7978],
        [0x232D738],
        None,
        (
            "Move effect: Natural Gift\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveGyroBall = Symbol(
        [0x7A38],
        [0x232D7F8],
        None,
        (
            "Move effect: Gyro Ball\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveShadowForce = Symbol(
        [0x7AA0],
        [0x232D860],
        None,
        (
            "Move effect: Shadow Force\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveGravity = Symbol(
        [0x7B3C],
        [0x232D8FC],
        None,
        (
            "Move effect: Gravity\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveStealthRock = Symbol(
        [0x7B4C],
        [0x232D90C],
        None,
        (
            "Move effect: Stealth Rock\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveChargeBeam = Symbol(
        [0x7BBC],
        [0x232D97C],
        None,
        (
            "Move effect: Charge Beam\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDamageEatItem = Symbol(
        [0x7C24],
        [0x232D9E4],
        None,
        (
            "Move effect: Deals damage, and eats any beneficial items the defender is"
            " holding.\nRelevant moves: Pluck, Bug Bite\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveAcupressure = Symbol(
        [0x7D10],
        [0x232DAD0],
        None,
        (
            "Move effect: Acupressure\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMagnetRise = Symbol(
        [0x7E94],
        [0x232DC54],
        None,
        (
            "Move effect: Magnet Rise\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveToxicSpikes = Symbol(
        [0x7EA4],
        [0x232DC64],
        None,
        (
            "Move effect: Toxic Spikes\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveLastResort = Symbol(
        [0x7F14],
        [0x232DCD4],
        None,
        (
            "Move effect: Last Resort\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTrickRoom = Symbol(
        [0x7FB8],
        [0x232DD78],
        None,
        (
            "Move effect: Trick Room\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveWorrySeed = Symbol(
        [0x7FEC],
        [0x232DDAC],
        None,
        (
            "Move effect: Worry Seed\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageHpDependent = Symbol(
        [0x80C4],
        [0x232DE84],
        None,
        (
            "Move effect: Deal damage, with a multiplier dependent on the defender's"
            " current HP.\nRelevant moves: Wring Out, Crush Grip\n\nr0: attacker"
            " pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn: whether the"
            " move was successfully used"
        ),
    )

    DoMoveHeartSwap = Symbol(
        [0x8178],
        [0x232DF38],
        None,
        (
            "Move effect: Heart Swap\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRoost = Symbol(
        [0x8208],
        [0x232DFC8],
        None,
        (
            "Move effect: Roost\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePowerSwap = Symbol(
        [0x82C4],
        [0x232E084],
        None,
        (
            "Move effect: Power Swap\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePowerTrick = Symbol(
        [0x8324],
        [0x232E0E4],
        None,
        (
            "Move effect: Power Trick\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveFeint = Symbol(
        [0x8338],
        [0x232E0F8],
        None,
        (
            "Move effect: Feint\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFlareBlitz = Symbol(
        [0x8370],
        [0x232E130],
        None,
        (
            "Move effect: Flare Blitz\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDefendOrder = Symbol(
        [0x84B4],
        [0x232E274],
        None,
        (
            "Move effect: Defend Order\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveFireFang = Symbol(
        [0x84F8],
        [0x232E2B8],
        None,
        (
            "Move effect: Fire Fang\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveLunarDance = Symbol(
        [0x85A8],
        [0x232E368],
        None,
        (
            "Move effect: Lunar Dance\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMiracleEye = Symbol(
        [0x8610],
        [0x232E3D0],
        None,
        (
            "Move effect: Miracle Eye\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveWakeUpSlap = Symbol(
        [0x8640],
        [0x232E400],
        None,
        (
            "Move effect: Wake-Up Slap\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMetalBurst = Symbol(
        [0x86CC],
        [0x232E48C],
        None,
        (
            "Move effect: Metal Burst\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveHeadSmash = Symbol(
        [0x86E0],
        [0x232E4A0],
        None,
        (
            "Move effect: Head Smash\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveCaptivate = Symbol(
        [0x87A0],
        [0x232E560],
        None,
        (
            "Move effect: Captivate\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveLeafStorm = Symbol(
        [0x8864],
        [0x232E624],
        None,
        (
            "Move effect: Leaf Storm\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDracoMeteor = Symbol(
        [0x88BC],
        [0x232E67C],
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
        [0x8920],
        [0x232E6E0],
        None,
        (
            "Move effect: Rock Polish\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveNastyPlot = Symbol(
        [0x8954],
        [0x232E714],
        None,
        (
            "Move effect: Nasty Plot\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveTag0x1AB = Symbol(
        [0x8974],
        [0x232E734],
        None,
        (
            "Move effect: MOVE_TAG_0x1AB\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTag0x1A6 = Symbol(
        [0x8990],
        [0x232E750],
        None,
        (
            "Move effect: MOVE_TAG_0x1A6\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTag0x1A7 = Symbol(
        [0x89D4],
        [0x232E794],
        None,
        (
            "Move effect: MOVE_TAG_0x1A7\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )


class NaMove_effectsData:
    LUNAR_DANCE_PP_RESTORATION = Symbol(
        [0x860C], [0x232E3CC], 0x4, "The amount of PP restored by Lunar Dance (999)."
    )


class NaMove_effectsSection:
    name = "move_effects"
    description = (
        "Move effect handlers for individual moves, called by ExecuteMoveEffect (and"
        " also the Metronome and Nature Power tables).\n\nThis subregion contains only"
        " the move effect handlers themselves, and not necessarily all the utility"
        " functions used by the move effect handlers (such as the damage calculation"
        " functions). These supporting utilities are in the main overlay29 block."
    )
    loadaddress = 0x2325DC0
    length = 0x8A4C
    functions = NaMove_effectsFunctions
    data = NaMove_effectsData


class NaOverlay0Functions:
    pass


class NaOverlay0Data:
    TOP_MENU_MUSIC_ID = Symbol(
        [0x1720], [0x22BE1A0], None, "Music ID to play in the top menu."
    )


class NaOverlay0Section:
    name = "overlay0"
    description = (
        "Likely contains supporting data and code related to the top menu.\n\nThis is"
        " loaded together with overlay 1 while in the top menu. Since it's in overlay"
        " group 2 (together with overlay 10, which is another 'data' overlay), this"
        " overlay probably plays a similar role. It mentions several files from the"
        " BACK folder that are known backgrounds for the top menu."
    )
    loadaddress = 0x22BCA80
    length = 0x609A0
    functions = NaOverlay0Functions
    data = NaOverlay0Data


class NaOverlay1Functions:
    CreateMainMenus = Symbol(
        [0x7BC4],
        [0x23310E4],
        None,
        (
            "Prepares the top menu and sub menu, adding the different options that"
            " compose them.\n\nContains multiple calls to AddMainMenuOption and"
            " AddSubMenuOption. Some of them are conditionally executed depending on"
            " which options should be unlocked.\n\nNo params."
        ),
    )

    AddMainMenuOption = Symbol(
        [0x8038],
        [0x2331558],
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
        [0x8110],
        [0x2331630],
        None,
        (
            "Adds an option to the 'Other' submenu on the top menu.\n\nThis function is"
            " called for each one of the options in the submenu. It loops the SUBMENU"
            " data field, if the specified action ID does not exist there, the option"
            " won't be added.\n\nr0: Action ID\nr1: True if the option should be"
            " enabled, false otherwise"
        ),
    )


class NaOverlay1Data:
    PRINTS_STRINGS = Symbol(
        [0x11C0C], [0x233B12C], 0x1E8, "Note: unverified, ported from Irdkwia's notes"
    )

    PRINTS_STRUCT = Symbol(
        [0x11DF4],
        [0x233B314],
        0x1F0,
        "62*0x8\n\nNote: unverified, ported from Irdkwia's notes",
    )

    OVERLAY1_D_BOX_LAYOUT_1 = Symbol(
        [0x11FF8], [0x233B518], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY1_D_BOX_LAYOUT_2 = Symbol(
        [0x12008], [0x233B528], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY1_D_BOX_LAYOUT_3 = Symbol(
        [0x12018], [0x233B538], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY1_D_BOX_LAYOUT_4 = Symbol(
        [0x12028], [0x233B548], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    CONTINUE_CHOICE = Symbol([0x12048], [0x233B568], 0x20, "")

    SUBMENU = Symbol([0x12068], [0x233B588], 0x48, "")

    MAIN_MENU = Symbol([0x120B0], [0x233B5D0], 0xA0, "")

    OVERLAY1_D_BOX_LAYOUT_5 = Symbol(
        [0x121FC], [0x233B71C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY1_D_BOX_LAYOUT_6 = Symbol(
        [0x1220C], [0x233B72C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY1_D_BOX_LAYOUT_7 = Symbol(
        [0x1221C], [0x233B73C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    MAIN_MENU_CONFIRM = Symbol([0x1222C], [0x233B74C], 0x18, "")

    OVERLAY1_D_BOX_LAYOUT_8 = Symbol(
        [0x122B0], [0x233B7D0], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY1_D_BOX_LAYOUT_9 = Symbol(
        [0x122D0], [0x233B7F0], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    MAIN_DEBUG_MENU_1 = Symbol([0x122F0], [0x233B810], 0x60, "")

    OVERLAY1_D_BOX_LAYOUT_10 = Symbol(
        [0x12350], [0x233B870], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    MAIN_DEBUG_MENU_2 = Symbol([0x12370], [0x233B890], 0x38, "")


class NaOverlay1Section:
    name = "overlay1"
    description = (
        "Likely controls the top menu.\n\nThis is loaded together with overlay 0 while"
        " in the top menu. Since it's in overlay group 1 (together with other 'main'"
        " overlays like overlay 11 and overlay 29), this is probably the"
        " controller.\n\nSeems to contain code related to Wi-Fi rescue. It mentions"
        " several files from the GROUND and BACK folders."
    )
    loadaddress = 0x2329520
    length = 0x12D20
    functions = NaOverlay1Functions
    data = NaOverlay1Data


class NaOverlay10Functions:
    SprintfStatic = Symbol(
        [0x9CC, 0x4DBC],
        [0x22BD44C, 0x22C183C],
        None,
        (
            "Statically defined copy of sprintf(3) in overlay 10. See arm9.yml for more"
            " information.\n\nr0: str\nr1: format\n...: variadic\nreturn: number of"
            " characters printed, excluding the null-terminator"
        ),
    )

    GetEffectAnimation = Symbol(
        [0x3420],
        [0x22BFEA0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: anim_id\nreturn:"
            " effect animation pointer"
        ),
    )

    GetMoveAnimation = Symbol(
        [0x3434],
        [0x22BFEB4],
        None,
        (
            "Get the move animation corresponding to the given move ID.\n\nr0:"
            " move_id\nreturn: move animation pointer"
        ),
    )

    GetSpecialMonsterMoveAnimation = Symbol(
        [0x3448],
        [0x22BFEC8],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ent_id\nreturn:"
            " special monster move animation pointer"
        ),
    )

    GetTrapAnimation = Symbol(
        [0x345C],
        [0x22BFEDC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: trap_id\nreturn: trap"
            " animation"
        ),
    )

    GetItemAnimation1 = Symbol(
        [0x3470],
        [0x22BFEF0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item_id\nreturn:"
            " first field of the item animation info"
        ),
    )

    GetItemAnimation2 = Symbol(
        [0x3484],
        [0x22BFF04],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item_id\nreturn:"
            " second field of the item animation info"
        ),
    )

    GetMoveAnimationSpeed = Symbol(
        [0x3498],
        [0x22BFF18],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: move_id\nreturn:"
            " anim_ent_ptr (This might be a mistake? It seems to be an integer, not a"
            " pointer)"
        ),
    )

    CheckEndDungeon = Symbol(
        [0x5E0C],
        [0x22C288C],
        None,
        (
            "Do the stuff when you lose in a dungeon.\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: End condition code? Seems to control what tasks"
            " get run and what transition happens when the dungeon ends\nreturn: return"
            " code?"
        ),
    )


class NaOverlay10Data:
    FIRST_DUNGEON_WITH_MONSTER_HOUSE_TRAPS = Symbol(
        [0x798C],
        [0x22C440C],
        0x1,
        (
            "The first dungeon that can have extra traps spawn in Monster Houses, Dark"
            " Hill\n\ntype: struct dungeon_id_8"
        ),
    )

    BAD_POISON_DAMAGE_COOLDOWN = Symbol(
        [0x7994],
        [0x22C4414],
        0x2,
        "The number of turns between passive bad poison (toxic) damage.",
    )

    PROTEIN_STAT_BOOST = Symbol(
        [0x79A0],
        [0x22C4420],
        0x2,
        "The permanent attack boost from ingesting a Protein.",
    )

    WATERFALL_CRINGE_CHANCE = Symbol(
        [0x79A4],
        [0x22C4424],
        0x2,
        "The chance of Waterfall inflicting the cringe status, as a percentage (30%).",
    )

    AURORA_BEAM_LOWER_ATTACK_CHANCE = Symbol(
        [0x79A8],
        [0x22C4428],
        0x2,
        "The chance of Aurora Beam halving attack, as a percentage (60%).",
    )

    SPAWN_CAP_NO_MONSTER_HOUSE = Symbol(
        [0x79B0],
        [0x22C4430],
        0x2,
        (
            "The maximum number of enemies that can spawn on a floor without a monster"
            " house (15)."
        ),
    )

    OREN_BERRY_DAMAGE = Symbol(
        [0x79B8], [0x22C4438], 0x2, "Damage dealt by eating an Oren Berry."
    )

    IRON_TAIL_LOWER_DEFENSE_CHANCE = Symbol(
        [0x79C0],
        [0x22C4440],
        0x2,
        "The chance of Iron Tail lowering defense, as a percentage (30%).",
    )

    TWINEEDLE_POISON_CHANCE = Symbol(
        [0x79C4],
        [0x22C4444],
        0x2,
        "The chance of Twineedle poisoning, as a percentage (20%).",
    )

    EXTRASENSORY_CRINGE_CHANCE = Symbol(
        [0x79C8],
        [0x22C4448],
        0x2,
        (
            "The chance of Extrasensory (and others, see DoMoveDamageCringe10)"
            " inflicting the cringe status, as a percentage (10%)."
        ),
    )

    ROCK_SLIDE_CRINGE_CHANCE = Symbol(
        [0x79CC],
        [0x22C444C],
        0x2,
        (
            "The chance of Rock Slide (and others, see DoMoveDamageCringe30) inflicting"
            " the cringe status, as a percentage (30%)"
        ),
    )

    CRUNCH_LOWER_DEFENSE_CHANCE = Symbol(
        [0x79D0],
        [0x22C4450],
        0x2,
        (
            "The chance of Crunch (and others, see DoMoveDamageLowerDef20) lowering"
            " defense, as a percentage (20%)."
        ),
    )

    UNOWN_STONE_DROP_CHANCE = Symbol(
        [0x79F4],
        [0x22C4474],
        0x2,
        "The chance of an Unown dropping an Unown stone, as a percentage (21%).",
    )

    SITRUS_BERRY_HP_RESTORATION = Symbol(
        [0x79F8],
        [0x22C4478],
        0x2,
        "The amount of HP restored by eating a Sitrus Berry.",
    )

    MUDDY_WATER_LOWER_ACCURACY_CHANCE = Symbol(
        [0x7A04],
        [0x22C4484],
        0x2,
        (
            "The chance of Muddy Water (and others, see DoMoveDamageLowerAccuracy40)"
            " lowering accuracy, as a percentage (40%)."
        ),
    )

    SILVER_WIND_BOOST_CHANCE = Symbol(
        [0x7A08],
        [0x22C4488],
        0x2,
        (
            "The chance of Silver Wind (and others, see DoMoveDamageBoostAllStats)"
            " boosting all stats, as a percentage (20%)."
        ),
    )

    POISON_TAIL_POISON_CHANCE = Symbol(
        [0x7A0C],
        [0x22C448C],
        0x2,
        "The chance of Poison Tail poisoning, as a percentage (10%).",
    )

    THUNDERSHOCK_PARALYZE_CHANCE = Symbol(
        [0x7A10],
        [0x22C4490],
        0x2,
        "The chance of Thundershock paralyzing, as a percentage (10%).",
    )

    BOUNCE_PARALYZE_CHANCE = Symbol(
        [0x7A14],
        [0x22C4494],
        0x2,
        "The chance of Bounce paralyzing, as a percentage (30%)",
    )

    HEADBUTT_CRINGE_CHANCE = Symbol(
        [0x7A18],
        [0x22C4498],
        0x2,
        "The chance of Headbutt inflicting the cringe status, as a percentage (25%).",
    )

    FIRE_FANG_CRINGE_CHANCE = Symbol(
        [0x7A1C],
        [0x22C449C],
        0x2,
        "The chance of Fire Fang inflicting the cringe status, as a percentage (25%).",
    )

    SACRED_FIRE_BURN_CHANCE = Symbol(
        [0x7A20],
        [0x22C44A0],
        0x2,
        "The chance of Sacred Fire burning, as a percentage (50%).",
    )

    WHIRLPOOL_CONSTRICTION_CHANCE = Symbol(
        [0x7A24],
        [0x22C44A4],
        0x2,
        (
            "The chance of Whirlpool inflicting the constriction status, as a"
            " percentage (10%)."
        ),
    )

    EXP_ELITE_EXP_BOOST = Symbol(
        [0x7A28],
        [0x22C44A8],
        0x2,
        "The percentage increase in experience from the Exp. Elite IQ skill",
    )

    MONSTER_HOUSE_MAX_NON_MONSTER_SPAWNS = Symbol(
        [0x7A2C],
        [0x22C44AC],
        0x2,
        (
            "The maximum number of extra non-monster spawns (items/traps) in a Monster"
            " House, 7"
        ),
    )

    HEAL_ORDER_HP_RESTORATION = Symbol(
        [0x7A38], [0x22C44B8], 0x2, "The amount of HP restored by Heal Order (40)."
    )

    STEEL_WING_BOOST_DEFENSE_CHANCE = Symbol(
        [0x7A44],
        [0x22C44C4],
        0x2,
        "The chance of Steel Wing boosting defense, as a percentage (20%).",
    )

    GOLD_THORN_POWER = Symbol(
        [0x7A50], [0x22C44D0], 0x2, "Attack power for Golden Thorns."
    )

    SPAWN_COOLDOWN = Symbol(
        [0x7A5C],
        [0x22C44DC],
        0x2,
        "The number of turns between enemy spawns under normal conditions.",
    )

    MIST_BALL_LOWER_SPECIAL_ATTACK_CHANCE = Symbol(
        [0x7A60],
        [0x22C44E0],
        0x2,
        "The chance of Mist Ball lowering special attack, as a percentage (50%).",
    )

    CHARGE_BEAM_BOOST_SPECIAL_ATTACK_CHANCE = Symbol(
        [0x7A70],
        [0x22C44F0],
        0x2,
        "The chance of Charge Beam boosting special attack, as a percentage (40%).",
    )

    ORAN_BERRY_FULL_HP_BOOST = Symbol(
        [0x7A74],
        [0x22C44F4],
        0x2,
        "The permanent HP boost from eating an Oran Berry at full HP (0).",
    )

    LIFE_SEED_HP_BOOST = Symbol(
        [0x7A78], [0x22C44F8], 0x2, "The permanent HP boost from eating a Life Seed."
    )

    OCTAZOOKA_LOWER_ACCURACY_CHANCE = Symbol(
        [0x7A80],
        [0x22C4500],
        0x2,
        "The chance of Octazooka lowering accuracy, as a percentage (60%).",
    )

    LUSTER_PURGE_LOWER_SPECIAL_DEFENSE_CHANCE = Symbol(
        [0x7A8C],
        [0x22C450C],
        0x2,
        (
            "The chance of Luster Purge (and others, see"
            " DoMoveDamageLowerSpecialDefense50) lowering special defense, as a"
            " percentage (50%)."
        ),
    )

    CONSTRICT_LOWER_SPEED_CHANCE = Symbol(
        [0x7A94],
        [0x22C4514],
        0x2,
        (
            "The chance of Constrict (and others, see DoMoveDamageLowerSpeed20)"
            " lowering speed, as a percentage (20%)."
        ),
    )

    ICE_FANG_FREEZE_CHANCE = Symbol(
        [0x7A98],
        [0x22C4518],
        0x2,
        "The chance of Ice Fang freezing, as a percentage (15%).",
    )

    SMOG_POISON_CHANCE = Symbol(
        [0x7A9C],
        [0x22C451C],
        0x2,
        (
            "The chance of Smog (and others, see DoMoveDamagePoison40) poisoning, as a"
            " percentage (40%)."
        ),
    )

    LICK_PARALYZE_CHANCE = Symbol(
        [0x7AA8],
        [0x22C4528],
        0x2,
        (
            "The chance of Lick (and others, see DoMoveDamageParalyze10) paralyzing, as"
            " a percentage (10%)."
        ),
    )

    THUNDER_FANG_PARALYZE_CHANCE = Symbol(
        [0x7AAC],
        [0x22C452C],
        0x2,
        "The chance of Thunder Fang paralyzing, as a percentage (10%).",
    )

    BITE_CRINGE_CHANCE = Symbol(
        [0x7AB4],
        [0x22C4534],
        0x2,
        (
            "The chance of Bite (and others, see DoMoveDamageCringe20) inflicting the"
            " cringe status, as a percentage (20%)"
        ),
    )

    SKY_ATTACK_CRINGE_CHANCE = Symbol(
        [0x7AB8],
        [0x22C4538],
        0x2,
        "The chance of Sky Attack inflicting the cringe status, as a percentage (25%).",
    )

    ICE_FANG_CRINGE_CHANCE = Symbol(
        [0x7ABC],
        [0x22C453C],
        0x2,
        "The chance of Ice Fang inflicting the cringe status, as a percentage (25%).",
    )

    BLAZE_KICK_BURN_CHANCE = Symbol(
        [0x7AC0],
        [0x22C4540],
        0x2,
        "The chance of Blaze Kick burning, as a percentage (10%).",
    )

    FLAMETHROWER_BURN_CHANCE = Symbol(
        [0x7AC4],
        [0x22C4544],
        0x2,
        (
            "The chance of Flamethrower (and others, see DoMoveDamageBurn10) burning,"
            " as a percentage (10%)."
        ),
    )

    DIZZY_PUNCH_CONFUSE_CHANCE = Symbol(
        [0x7AC8],
        [0x22C4548],
        0x2,
        (
            "The chance of Dizzy Punch (and others, see DoMoveDamageConfuse30)"
            " confusing, as a percentage (30%)."
        ),
    )

    SECRET_POWER_EFFECT_CHANCE = Symbol(
        [0x7ACC],
        [0x22C454C],
        0x2,
        "The chance of Secret Power inflicting an effect, as a percentage (30%).",
    )

    METAL_CLAW_BOOST_ATTACK_CHANCE = Symbol(
        [0x7AD4],
        [0x22C4554],
        0x2,
        "The chance of Metal Claw boosting attack, as a percentage (20%).",
    )

    SONICBOOM_FIXED_DAMAGE = Symbol(
        [0x7AE8],
        [0x22C4568],
        0x2,
        "The amount of fixed damage dealt by SonicBoom (20).",
    )

    EXCLUSIVE_ITEM_EXP_BOOST = Symbol(
        [0x7B0C],
        [0x22C458C],
        0x2,
        "The percentage increase in experience from exp-boosting exclusive items.",
    )

    AFTERMATH_CHANCE = Symbol(
        [0x7B14],
        [0x22C4594],
        0x2,
        "The chance of the Aftermath ability activating, as a percentage (50%).",
    )

    INTIMIDATOR_ACTIVATION_CHANCE = Symbol(
        [0x7B38],
        [0x22C45B8],
        0x2,
        "The percentage chance that Intimidator will activate.",
    )

    ORAN_BERRY_HP_RESTORATION = Symbol(
        [0x7B6C], [0x22C45EC], 0x2, "The amount of HP restored by eating a Oran Berry."
    )

    SITRUS_BERRY_FULL_HP_BOOST = Symbol(
        [0x7B74],
        [0x22C45F4],
        0x2,
        "The permanent HP boost from eating a Sitrus Berry at full HP.",
    )

    SNORE_CRINGE_CHANCE = Symbol(
        [0x7B80],
        [0x22C4600],
        0x2,
        "The chance of Snore inflicting the cringe status, as a percentage (30%).",
    )

    METEOR_MASH_BOOST_ATTACK_CHANCE = Symbol(
        [0x7B84],
        [0x22C4604],
        0x2,
        "The chance of Meteor Mash boosting attack, as a percentage (20%).",
    )

    CRUSH_CLAW_LOWER_DEFENSE_CHANCE = Symbol(
        [0x7B88],
        [0x22C4608],
        0x2,
        "The chance of Crush Claw lowering defense, as a percentage (50%).",
    )

    BURN_DAMAGE_COOLDOWN = Symbol(
        [0x7B90], [0x22C4610], 0x2, "The number of turns between passive burn damage."
    )

    SHADOW_BALL_LOWER_SPECIAL_DEFENSE_CHANCE = Symbol(
        [0x7B9C],
        [0x22C461C],
        0x2,
        "The chance of Shadow Ball lowering special defense, as a percentage (20%).",
    )

    STICK_POWER = Symbol([0x7BA4], [0x22C4624], 0x2, "Attack power for Sticks.")

    BUBBLE_LOWER_SPEED_CHANCE = Symbol(
        [0x7BAC],
        [0x22C462C],
        0x2,
        "The chance of Bubble lowering speed, as a percentage (10%).",
    )

    POWDER_SNOW_FREEZE_CHANCE = Symbol(
        [0x7BB4],
        [0x22C4634],
        0x2,
        (
            "The chance of Powder Snow (and others, see DoMoveDamageFreeze15) freezing,"
            " as a percentage (15%)."
        ),
    )

    POISON_STING_POISON_CHANCE = Symbol(
        [0x7BBC],
        [0x22C463C],
        0x2,
        (
            "The chance of Poison Sting (and others, see DoMoveDamagePoison18)"
            " poisoning, as a percentage (18%)."
        ),
    )

    SPAWN_COOLDOWN_THIEF_ALERT = Symbol(
        [0x7BC0],
        [0x22C4640],
        0x2,
        (
            "The number of turns between enemy spawns when the Thief Alert condition is"
            " active."
        ),
    )

    POISON_FANG_POISON_CHANCE = Symbol(
        [0x7BC4],
        [0x22C4644],
        0x2,
        "The chance of Poison Fang poisoning, as a percentage (30%).",
    )

    THUNDER_PARALYZE_CHANCE = Symbol(
        [0x7BD8],
        [0x22C4658],
        0x2,
        (
            "The chance of Thunder (and others, see DoMoveDamageParalyze20) paralyzing,"
            " as a percentage (20%)"
        ),
    )

    THUNDERBOLT_PARALYZE_CHANCE = Symbol(
        [0x7BDC],
        [0x22C465C],
        0x2,
        "The chance of Thunderbolt paralyzing, as a percentage (15%).",
    )

    MONSTER_HOUSE_MAX_MONSTER_SPAWNS = Symbol(
        [0x7BE0],
        [0x22C4660],
        0x2,
        (
            "The maximum number of monster spawns in a Monster House, 30, but"
            " multiplied by 2/3 for some reason (so the actual maximum is 45)"
        ),
    )

    TWISTER_CRINGE_CHANCE = Symbol(
        [0x7BE8],
        [0x22C4668],
        0x2,
        "The chance of Twister inflicting the cringe status, as a percentage (10%).",
    )

    SPEED_BOOST_TURNS = Symbol(
        [0x7BEC],
        [0x22C466C],
        0x2,
        (
            "Number of turns (250) after which Speed Boost will trigger and increase"
            " speed by one stage."
        ),
    )

    FAKE_OUT_CRINGE_CHANCE = Symbol(
        [0x7BF0],
        [0x22C4670],
        0x2,
        "The chance of Fake Out inflicting the cringe status, as a percentage (35%).",
    )

    THUNDER_FANG_CRINGE_CHANCE = Symbol(
        [0x7BF8],
        [0x22C4678],
        0x2,
        (
            "The chance of Thunder Fang inflicting the cringe status, as a percentage"
            " (25%)."
        ),
    )

    FLARE_BLITZ_BURN_CHANCE = Symbol(
        [0x7C04],
        [0x22C4684],
        0x2,
        (
            "The chance of Flare Blitz burning, as a percentage (25%). This value is"
            " also used for the Fire Fang burn chance."
        ),
    )

    FLAME_WHEEL_BURN_CHANCE = Symbol(
        [0x7C08],
        [0x22C4688],
        0x2,
        (
            "The chance of Flame Wheel (and others, see DoMoveDamageBurn10FlameWheel)"
            " burning, as a percentage (10%)."
        ),
    )

    PSYBEAM_CONFUSE_CHANCE = Symbol(
        [0x7C10],
        [0x22C4690],
        0x2,
        (
            "The chance of Psybeam (and others, see DoMoveDamageConfuse10) confusing,"
            " as a percentage (10%)."
        ),
    )

    TRI_ATTACK_STATUS_CHANCE = Symbol(
        [0x7C14],
        [0x22C4694],
        0x2,
        (
            "The chance of Tri Attack inflicting any status condition, as a percentage"
            " (20%)."
        ),
    )

    MIRACLE_CHEST_EXP_BOOST = Symbol(
        [0x7C18],
        [0x22C4698],
        0x2,
        "The percentage increase in experience from the Miracle Chest item",
    )

    WONDER_CHEST_EXP_BOOST = Symbol(
        [0x7C1C],
        [0x22C469C],
        0x2,
        "The percentage increase in experience from the Wonder Chest item",
    )

    SPAWN_CAP_WITH_MONSTER_HOUSE = Symbol(
        [0x7C24],
        [0x22C46A4],
        0x2,
        (
            "The maximum number of enemies that can spawn on a floor with a monster"
            " house, not counting those in the monster house (4)."
        ),
    )

    POISON_DAMAGE_COOLDOWN = Symbol(
        [0x7C28], [0x22C46A8], 0x2, "The number of turns between passive poison damage."
    )

    GEO_PEBBLE_DAMAGE = Symbol(
        [0x7C34], [0x22C46B4], 0x2, "Damage dealt by Geo Pebbles."
    )

    GRAVELEROCK_DAMAGE = Symbol(
        [0x7C38], [0x22C46B8], 0x2, "Damage dealt by Gravelerocks."
    )

    RARE_FOSSIL_DAMAGE = Symbol(
        [0x7C3C], [0x22C46BC], 0x2, "Damage dealt by Rare Fossils."
    )

    GINSENG_CHANCE_3 = Symbol(
        [0x7C40],
        [0x22C46C0],
        0x2,
        (
            "The percentage chance for...something to be set to 3 in a calculation"
            " related to the Ginseng boost."
        ),
    )

    ZINC_STAT_BOOST = Symbol(
        [0x7C44],
        [0x22C46C4],
        0x2,
        "The permanent special defense boost from ingesting a Zinc.",
    )

    IRON_STAT_BOOST = Symbol(
        [0x7C48],
        [0x22C46C8],
        0x2,
        "The permanent defense boost from ingesting an Iron.",
    )

    CALCIUM_STAT_BOOST = Symbol(
        [0x7C4C],
        [0x22C46CC],
        0x2,
        "The permanent special attack boost from ingesting a Calcium.",
    )

    DRAGON_RAGE_FIXED_DAMAGE = Symbol(
        [0x7C54],
        [0x22C46D4],
        0x2,
        "The amount of fixed damage dealt by Dragon Rage (30).",
    )

    CORSOLA_TWIG_POWER = Symbol(
        [0x7C58], [0x22C46D8], 0x2, "Attack power for Corsola Twigs."
    )

    CACNEA_SPIKE_POWER = Symbol(
        [0x7C5C], [0x22C46DC], 0x2, "Attack power for Cacnea Spikes."
    )

    GOLD_FANG_POWER = Symbol([0x7C60], [0x22C46E0], 0x2, "Attack power for Gold Fangs.")

    SILVER_SPIKE_POWER = Symbol(
        [0x7C64], [0x22C46E4], 0x2, "Attack power for Silver Spikes."
    )

    IRON_THORN_POWER = Symbol(
        [0x7C68], [0x22C46E8], 0x2, "Attack power for Iron Thorns."
    )

    HEALING_WISH_HP_RESTORATION = Symbol(
        [0x7C74],
        [0x22C46F4],
        0x2,
        (
            "The amount of HP restored by Healing Wish (999). This also applies to"
            " Lunar Dance."
        ),
    )

    FACADE_DAMAGE_MULTIPLIER = Symbol(
        [0x7C98],
        [0x22C4718],
        0x4,
        (
            "The Facade damage multiplier for users with a status condition, as a"
            " binary fixed-point number with 8 fraction bits (0x200 -> 2x)."
        ),
    )

    IMPRISON_TURN_RANGE = Symbol(
        [0x7C9C],
        [0x22C471C],
        0x4,
        (
            "The turn range for the Paused status inflicted by Imprison, [3,"
            " 6).\n\ntype: int16_t[2]"
        ),
    )

    SLEEP_TURN_RANGE = Symbol(
        [0x7CA0],
        [0x22C4720],
        0x4,
        (
            "Appears to control the range of turns for which the sleep condition can"
            " last.\n\nThe first two bytes are the low value of the range, and the"
            " later two bytes are the high value."
        ),
    )

    NIGHTMARE_TURN_RANGE = Symbol(
        [0x7CA4],
        [0x22C4724],
        0x4,
        (
            "The turn range for the Nightmare status inflicted by Nightmare, [4,"
            " 8).\n\ntype: int16_t[2]"
        ),
    )

    REST_TURN_RANGE = Symbol(
        [0x7CC8],
        [0x22C4748],
        0x4,
        (
            "The turn range for the Napping status inflicted by Rest, [1, 4).\n\ntype:"
            " int16_t[2]"
        ),
    )

    SPORT_CONDITION_TURN_RANGE = Symbol(
        [0x7D0C],
        [0x22C478C],
        0x4,
        (
            "The turn range for the sport conditions activated by Mud Sport and Water"
            " Sport, [10, 12).\n\ntype: int16_t[2]"
        ),
    )

    SURE_SHOT_TURN_RANGE = Symbol(
        [0x7D18],
        [0x22C4798],
        0x4,
        (
            "The turn range for the Sure Shot status inflicted by Mind Reader and"
            " Lock-On, [10, 12).\n\ntype: int16_t[2]"
        ),
    )

    SMOKESCREEN_TURN_RANGE = Symbol(
        [0x7D44],
        [0x22C47C4],
        0x4,
        (
            "The turn range for the Whiffer status inflicted by Smokescreen, [1,"
            " 4).\n\ntype: int16_t[2]"
        ),
    )

    POWER_PITCHER_DAMAGE_MULTIPLIER = Symbol(
        [0x7D78],
        [0x22C47F8],
        0x4,
        (
            "The multiplier for projectile damage from Power Pitcher (1.5), as a binary"
            " fixed-point number (8 fraction bits)"
        ),
    )

    AIR_BLADE_DAMAGE_MULTIPLIER = Symbol(
        [0x7DC4],
        [0x22C4844],
        0x4,
        (
            "The multiplier for damage from the Air Blade (1.5), as a binary"
            " fixed-point number (8 fraction bits)"
        ),
    )

    HIDDEN_STAIRS_SPAWN_CHANCE_MULTIPLIER = Symbol(
        [0x7DD0],
        [0x22C4850],
        0x4,
        (
            "The hidden stairs spawn chance multiplier (~1.2) as a binary fixed-point"
            " number (8 fraction bits), if applicable. See"
            " ShouldBoostHiddenStairsSpawnChance in overlay 29."
        ),
    )

    YAWN_TURN_RANGE = Symbol(
        [0x7DE0],
        [0x22C4860],
        0x4,
        (
            "The turn range for the Yawning status inflicted by Yawn, [2, 2].\n\ntype:"
            " int16_t[2]"
        ),
    )

    SPEED_BOOST_TURN_RANGE = Symbol(
        [0x7E08],
        [0x22C4888],
        0x4,
        (
            "Appears to control the range of turns for which a speed boost can"
            " last.\n\nThe first two bytes are the low value of the range, and the"
            " later two bytes are the high value."
        ),
    )

    SYNTHESIS_HP_RESTORATION_TABLE = Symbol(
        [0x7ED4],
        [0x22C4954],
        0x10,
        (
            "Maps each weather type (by index, see enum weather_id) to the"
            " corresponding HP restoration value for Synthesis.\n\ntype: int16_t[8]"
        ),
    )

    ROOST_HP_RESTORATION_TABLE = Symbol(
        [0x7EE4],
        [0x22C4964],
        0x10,
        (
            "Maps each weather type (by index, see enum weather_id) to the"
            " corresponding HP restoration value for Roost.\n\nEvery entry in this"
            " table is 40.\n\ntype: int16_t[8]"
        ),
    )

    MOONLIGHT_HP_RESTORATION_TABLE = Symbol(
        [0x7EF4],
        [0x22C4974],
        0x10,
        (
            "Maps each weather type (by index, see enum weather_id) to the"
            " corresponding HP restoration value for Moonlight.\n\ntype: int16_t[8]"
        ),
    )

    MORNING_SUN_HP_RESTORATION_TABLE = Symbol(
        [0x7F04],
        [0x22C4984],
        0x10,
        (
            "Maps each weather type (by index, see enum weather_id) to the"
            " corresponding HP restoration value for Morning Sun.\n\ntype: int16_t[8]"
        ),
    )

    WEATHER_ATTRIBUTE_TABLE = Symbol(
        [0x81EC],
        [0x22C4C6C],
        0x30,
        (
            "Maps each weather type (by index, see enum weather_id) to the"
            " corresponding Weather Ball type and Castform form.\n\ntype: struct"
            " weather_attributes[8]"
        ),
    )

    OFFENSIVE_STAT_STAGE_MULTIPLIERS = Symbol(
        [0x8318],
        [0x22C4D98],
        0x54,
        (
            "Table of multipliers for offensive stats (attack/special attack) for each"
            " stage 0-20, as binary fixed-point numbers (8 fraction bits)"
        ),
    )

    DEFENSIVE_STAT_STAGE_MULTIPLIERS = Symbol(
        [0x836C],
        [0x22C4DEC],
        0x54,
        (
            "Table of multipliers for defensive stats (defense/special defense) for"
            " each stage 0-20, as binary fixed-point numbers (8 fraction bits)"
        ),
    )

    NATURE_POWER_TABLE = Symbol(
        [0x83C0],
        [0x22C4E40],
        0x78,
        (
            "Maps enum nature_power_variant to the associated move ID and effect"
            " handler.\n\ntype: struct wildcard_move_desc[15]"
        ),
    )

    APPLES_AND_BERRIES_ITEM_IDS = Symbol(
        [0x8438],
        [0x22C4EB8],
        0x84,
        (
            "Table of item IDs for Apples and Berries, which trigger the exclusive item"
            " effect EXCLUSIVE_EFF_RECOVER_HP_FROM_APPLES_AND_BERRIES.\n\ntype: struct"
            " item_id_16[66]"
        ),
    )

    RECRUITMENT_LEVEL_BOOST_TABLE = Symbol(
        [0x85E4],
        [0x22C5064],
        0xCC,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[102]",
    )

    NATURAL_GIFT_ITEM_TABLE = Symbol(
        [0x86B0],
        [0x22C5130],
        0xCC,
        (
            "Maps items to their type and base power if used with Natural Gift.\n\nAny"
            " item not listed in this table explicitly will be Normal type with a base"
            " power of 1 when used with Natural Gift.\n\ntype: struct"
            " natural_gift_item_info[34]"
        ),
    )

    RANDOM_MUSIC_ID_TABLE = Symbol(
        [0x877C],
        [0x22C51FC],
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
        [0x886C],
        [0x22C52EC],
        0x120,
        "8 * 6 * 3 * 0x2\n\nNote: unverified, ported from Irdkwia's notes",
    )

    MALE_ACCURACY_STAGE_MULTIPLIERS = Symbol(
        [0x898C],
        [0x22C540C],
        0x54,
        (
            "Table of multipliers for the accuracy stat for males for each stage 0-20,"
            " as binary fixed-point numbers (8 fraction bits)"
        ),
    )

    MALE_EVASION_STAGE_MULTIPLIERS = Symbol(
        [0x89E0],
        [0x22C5460],
        0x54,
        (
            "Table of multipliers for the evasion stat for males for each stage 0-20,"
            " as binary fixed-point numbers (8 fraction bits)"
        ),
    )

    FEMALE_ACCURACY_STAGE_MULTIPLIERS = Symbol(
        [0x8A34],
        [0x22C54B4],
        0x54,
        (
            "Table of multipliers for the accuracy stat for females for each stage"
            " 0-20, as binary fixed-point numbers (8 fraction bits)"
        ),
    )

    FEMALE_EVASION_STAGE_MULTIPLIERS = Symbol(
        [0x8A88],
        [0x22C5508],
        0x54,
        (
            "Table of multipliers for the evasion stat for females for each stage 0-20,"
            " as binary fixed-point numbers (8 fraction bits)"
        ),
    )

    MUSIC_ID_TABLE = Symbol(
        [0x8ADC],
        [0x22C555C],
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
        [0x8C30],
        [0x22C56B0],
        0x288,
        (
            "Table of type matchups.\n\nEach row corresponds to the type matchups of a"
            " specific attack type, with each entry within the row specifying the"
            " type's effectiveness against a target type.\n\ntype: struct"
            " type_matchup_table"
        ),
    )

    FIXED_ROOM_MONSTER_SPAWN_STATS_TABLE = Symbol(
        [0x8EB8],
        [0x22C5938],
        0x4A4,
        (
            "Table of stats for monsters that can spawn in fixed rooms, pointed into by"
            " the FIXED_ROOM_MONSTER_SPAWN_TABLE.\n\nThis is an array of 99 12-byte"
            " entries containing stat spreads for one monster entry each.\n\ntype:"
            " struct fixed_room_monster_spawn_stats_entry[99]"
        ),
    )

    METRONOME_TABLE = Symbol(
        [0x935C],
        [0x22C5DDC],
        0x540,
        (
            "Something to do with the moves that Metronome can turn into.\n\ntype:"
            " struct wildcard_move_desc[168]"
        ),
    )

    TILESET_PROPERTIES = Symbol(
        [0x989C], [0x22C631C], 0x954, "type: struct tileset_property[199]"
    )

    FIXED_ROOM_PROPERTIES_TABLE = Symbol(
        [0xA1F0],
        [0x22C6C70],
        0xC00,
        (
            "Table of properties for fixed rooms.\n\nThis is an array of 256 12-byte"
            " entries containing properties for a given fixed room ID.\n\nSee the"
            " struct definitions and End45's dungeon data document for more"
            " info.\n\ntype: struct fixed_room_properties_entry[256]"
        ),
    )

    TRAP_ANIMATION_INFO = Symbol(
        [0xAFD0],
        [0x22C7A50],
        0x34,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " trap_animation[26]"
        ),
    )

    ITEM_ANIMATION_INFO = Symbol(
        [0xB004],
        [0x22C7A84],
        0x15E0,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " item_animation[1400]"
        ),
    )

    MOVE_ANIMATION_INFO = Symbol(
        [0xC5E4], [0x22C9064], 0x34C8, "type: struct move_animation[563]"
    )

    EFFECT_ANIMATION_INFO = Symbol(
        [0xFAAC],
        [0x22CC52C],
        0x4C90,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " effect_animation[700]"
        ),
    )

    SPECIAL_MONSTER_MOVE_ANIMATION_INFO = Symbol(
        [0x1473C],
        [0x22D11BC],
        0xADF4,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " special_monster_move_animation[7422]"
        ),
    )


class NaOverlay10Section:
    name = "overlay10"
    description = (
        "Appears to be used both during ground mode and dungeon mode. With dungeon"
        " mode, whereas overlay 29 contains the main dungeon engine, this overlay seems"
        " to contain routines and data for dungeon mechanics."
    )
    loadaddress = 0x22BCA80
    length = 0x1F7A0
    functions = NaOverlay10Functions
    data = NaOverlay10Data


class NaOverlay11Functions:
    FuncThatCallsCommandParsing = Symbol([0xF24], [0x22DD164], None, "")

    ScriptCommandParsing = Symbol([0x1B24], [0x22DDD64], None, "")

    SsbLoad2 = Symbol([0x84BC], [0x22E46FC], None, "")

    StationLoadHanger = Symbol([0x8994], [0x22E4BD4], None, "")

    ScriptStationLoadTalk = Symbol([0x91A4], [0x22E53E4], None, "")

    SsbLoad1 = Symbol([0x9B10], [0x22E5D50], None, "")

    ScriptSpecialProcessCall = Symbol(
        [0xAED8],
        [0x22E7118],
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
        [0x22E803C],
        None,
        (
            "Returns an entry from RECRUITMENT_TABLE_SPECIES.\n\nNote: This indexes"
            " without doing bounds checking.\n\nr0: index into"
            " RECRUITMENT_TABLE_SPECIES\nreturn: enum monster_id"
        ),
    )

    PrepareMenuAcceptTeamMember = Symbol(
        [0xBE40],
        [0x22E8080],
        None,
        (
            "Implements SPECIAL_PROC_PREPARE_MENU_ACCEPT_TEAM_MEMBER (see"
            " ScriptSpecialProcessCall).\n\nr0: index into RECRUITMENT_TABLE_SPECIES"
        ),
    )

    InitRandomNpcJobs = Symbol(
        [0xBEE4],
        [0x22E8124],
        None,
        (
            "Implements SPECIAL_PROC_INIT_RANDOM_NPC_JOBS (see"
            " ScriptSpecialProcessCall).\n\nr0: job type? 0 is a random NPC job, 1 is a"
            " bottle mission\nr1: ?"
        ),
    )

    GetRandomNpcJobType = Symbol(
        [0xBF7C],
        [0x22E81BC],
        None,
        (
            "Implements SPECIAL_PROC_GET_RANDOM_NPC_JOB_TYPE (see"
            " ScriptSpecialProcessCall).\n\nreturn: job type?"
        ),
    )

    GetRandomNpcJobSubtype = Symbol(
        [0xBF94],
        [0x22E81D4],
        None,
        (
            "Implements SPECIAL_PROC_GET_RANDOM_NPC_JOB_SUBTYPE (see"
            " ScriptSpecialProcessCall).\n\nreturn: job subtype?"
        ),
    )

    GetRandomNpcJobStillAvailable = Symbol(
        [0xBFB0],
        [0x22E81F0],
        None,
        (
            "Implements SPECIAL_PROC_GET_RANDOM_NPC_JOB_STILL_AVAILABLE (see"
            " ScriptSpecialProcessCall).\n\nreturn: bool"
        ),
    )

    AcceptRandomNpcJob = Symbol(
        [0xC018],
        [0x22E8258],
        None,
        (
            "Implements SPECIAL_PROC_ACCEPT_RANDOM_NPC_JOB (see"
            " ScriptSpecialProcessCall).\n\nreturn: bool"
        ),
    )

    GroundMainLoop = Symbol(
        [0xC534],
        [0x22E8774],
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
        [0x22E935C],
        None,
        (
            "The GetAllocArena function used for ground mode. See SetMemAllocatorParams"
            " for more information.\n\nr0: initial memory arena pointer, or null\nr1:"
            " flags (see MemAlloc)\nreturn: memory arena pointer, or null"
        ),
    )

    GetFreeArenaGround = Symbol(
        [0xD180],
        [0x22E93C0],
        None,
        (
            "The GetFreeArena function used for ground mode. See SetMemAllocatorParams"
            " for more information.\n\nr0: initial memory arena pointer, or null\nr1:"
            " pointer to free\nreturn: memory arena pointer, or null"
        ),
    )

    GroundMainReturnDungeon = Symbol(
        [0xD1D4],
        [0x22E9414],
        None,
        (
            "Implements SPECIAL_PROC_RETURN_DUNGEON (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    GroundMainNextDay = Symbol(
        [0xD1F8],
        [0x22E9438],
        None,
        (
            "Implements SPECIAL_PROC_NEXT_DAY (see ScriptSpecialProcessCall).\n\nNo"
            " params."
        ),
    )

    JumpToTitleScreen = Symbol(
        [0xD39C],
        [0x22E95DC],
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
        [0x22E9694],
        None,
        (
            "Implements SPECIAL_PROC_RETURN_TO_TITLE_SCREEN (see"
            " ScriptSpecialProcessCall).\n\nr0: fade duration\nreturn: bool (but note"
            " that the special process ignores this and always returns 0)"
        ),
    )

    ScriptSpecialProcess0x16 = Symbol(
        [0xD4B4],
        [0x22E96F4],
        None,
        "Implements SPECIAL_PROC_0x16 (see ScriptSpecialProcessCall).\n\nr0: bool",
    )

    LoadBackgroundAttributes = Symbol(
        [0xF900],
        [0x22EBB40],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output]"
            " bg_attr_str\nr1: bg_id"
        ),
    )

    LoadMapType10 = Symbol(
        [0x10AE4],
        [0x22ECD24],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output]"
            " buffer_ptr\nr1: map_id\nr2: dungeon_info_str\nr3: additional_info"
        ),
    )

    LoadMapType11 = Symbol(
        [0x11004],
        [0x22ED244],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output]"
            " buffer_ptr\nr1: map_id\nr2: dungeon_info_str\nr3: additional_info"
        ),
    )

    GetSpecialLayoutBackground = Symbol(
        [0x1531C],
        [0x22F155C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: bg_id\nr1:"
            " dungeon_info_str\nr2: additional_info\nr3: copy_fixed_room_layout"
        ),
    )

    SetAnimDataFields = Symbol(
        [0x185DC],
        [0x22F481C],
        None,
        "Sets some fields on the animation struct?\n\nr0: animation pointer\nr1: ?",
    )

    SetAnimDataFieldsWrapper = Symbol(
        [0x1871C],
        [0x22F495C],
        None,
        "Calls SetAnimDataFields with the second argument right-shifted by 16.",
    )

    InitAnimDataFromOtherAnimData = Symbol(
        [0x18A24],
        [0x22F4C64],
        None,
        (
            "Appears to partially copy some animation data into another animation"
            " struct, plus doing extra initialization on the destination struct.\n\nr0:"
            " dst\nr1: src"
        ),
    )

    SetAnimDataFields2 = Symbol(
        [0x190A8],
        [0x22F52E8],
        None,
        (
            "Sets some fields on the animation struct, based on the params?\n\nr0:"
            " animation pointer\nr1: flags\nr2: ?"
        ),
    )

    LoadObjectAnimData = Symbol(
        [0x1AC20],
        [0x22F6E60],
        None,
        (
            "Loads the animation (WAN) data for a given object index?\n\nr0: animation"
            " pointer\nr1: object index\nr2: flags"
        ),
    )

    InitAnimDataFromOtherAnimDataVeneer = Symbol(
        [0x1ACCC],
        [0x22F6F0C],
        None,
        (
            "Likely a linker-generated veneer for InitAnimDataFromOtherAnimData.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " dst\nr1: src"
        ),
    )

    AnimRelatedFunction = Symbol(
        [0x1ACD4, 0x1AE24],
        [0x22F6F14, 0x22F7064],
        None,
        (
            "Does more stuff related to animations...probably?\n\nr0: animation"
            " pointer?\nothers: ?"
        ),
    )

    SprintfStatic = Symbol(
        [0x2CC8C],
        [0x2308ECC],
        None,
        (
            "Statically defined copy of sprintf(3) in overlay 11. See arm9.yml for more"
            " information.\n\nr0: str\nr1: format\n...: variadic\nreturn: number of"
            " characters printed, excluding the null-terminator"
        ),
    )

    StatusUpdate = Symbol(
        [0x37858],
        [0x2313A98],
        None,
        (
            "Implements SPECIAL_PROC_STATUS_UPDATE (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )


class NaOverlay11Data:
    OVERLAY11_UNKNOWN_TABLE__NA_2316A38 = Symbol(
        [0x3A7F8],
        [0x2316A38],
        0xA0,
        (
            "Multiple entries are pointers to the string 'script.c'\n\nNote:"
            " unverified, ported from Irdkwia's notes\n\ntype: undefined4[40]"
        ),
    )

    SCRIPT_COMMAND_PARSING_DATA = Symbol(
        [0x3A898], [0x2316AD8], 0x20, "Used by ScriptCommandParsing somehow"
    )

    SCRIPT_OP_CODE_NAMES = Symbol(
        [0x3A8B8],
        [0x2316AF8],
        0x1B18,
        (
            "Opcode name strings pointed to by entries in SCRIPT_OP_CODES"
            " (script_opcode::name)"
        ),
    )

    SCRIPT_OP_CODES = Symbol(
        [0x3C3D0],
        [0x2318610],
        0xBF8,
        (
            "Table of opcodes for the script engine. There are 383 8-byte"
            " entries.\n\nThese opcodes underpin the various ExplorerScript functions"
            " you can call in the SkyTemple SSB debugger.\n\ntype: struct"
            " script_opcode_table"
        ),
    )

    OVERLAY11_DEBUG_STRINGS = Symbol(
        [0x3CFC8],
        [0x2319208],
        0x8E4,
        "Strings used with various debug printing functions throughout the overlay",
    )

    C_ROUTINE_NAMES = Symbol(
        [0x3D8AC],
        [0x2319AEC],
        0x2D3C,
        (
            "Common routine name strings pointed to by entries in C_ROUTINES"
            " (common_routine::name)"
        ),
    )

    C_ROUTINES = Symbol(
        [0x405E8],
        [0x231C828],
        0x15E8,
        (
            "Common routines used within the unionall.ssb script (the master script)."
            " There are 701 8-byte entries.\n\nThese routines underpin the"
            " ExplorerScript coroutines you can call in the SkyTemple SSB"
            " debugger.\n\ntype: struct common_routine_table"
        ),
    )

    GROUND_WEATHER_TABLE = Symbol(
        [0x41BD0],
        [0x231DE10],
        0x30,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " ground_weather_entry[12]"
        ),
    )

    GROUND_WAN_FILES_TABLE = Symbol(
        [0x41C00],
        [0x231DE40],
        0x1014,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: char[343][12]",
    )

    OBJECTS = Symbol(
        [0x42C14],
        [0x231EE54],
        0x1A04,
        (
            "Table of objects for the script engine, which can be placed in scenes."
            " There are a version-dependent number of 12-byte entries.\n\ntype: struct"
            " script_object[length / 12]"
        ),
    )

    RECRUITMENT_TABLE_LOCATIONS = Symbol(
        [0x44654],
        [0x2320894],
        0x16,
        (
            "Table of dungeon IDs corresponding to entries in"
            " RECRUITMENT_TABLE_SPECIES.\n\ntype: struct dungeon_id_16[22]"
        ),
    )

    RECRUITMENT_TABLE_LEVELS = Symbol(
        [0x4466C],
        [0x23208AC],
        0x2C,
        (
            "Table of levels for recruited Pokémon, corresponding to entries in"
            " RECRUITMENT_TABLE_SPECIES.\n\ntype: int16_t[22]"
        ),
    )

    RECRUITMENT_TABLE_SPECIES = Symbol(
        [0x44698],
        [0x23208D8],
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
        [0x44AEC],
        [0x2320D2C],
        0x288,
        (
            "Irdkwia's notes: FIXED_FLOOR_GROUND_ASSOCIATION\n\ntype: struct"
            " level_tilemap_list_entry[81]"
        ),
    )

    OVERLAY11_OVERLAY_LOAD_TABLE = Symbol(
        [0x46E2C],
        [0x232306C],
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

    UNIONALL_RAM_ADDRESS = Symbol([0x48A64], [0x2324CA4], None, "[Runtime]")

    GROUND_STATE_MAP = Symbol([0x48A80], [0x2324CC0], None, "[Runtime]")

    GROUND_STATE_PTRS = Symbol(
        [0x48AB4],
        [0x2324CF4],
        0x18,
        (
            "Host pointers to multiple structure used for performing an overworld"
            " scene\n\ntype: struct main_ground_data"
        ),
    )


class NaOverlay11Section:
    name = "overlay11"
    description = (
        "The script engine.\n\nThis is the 'main' overlay of ground mode. The script"
        " engine is what runs the ground mode scripts contained in the SCRIPT folder,"
        " which are written in a custom scripting language. These scripts encode things"
        " like cutscenes, screen transitions, ground mode events, and tons of other"
        " things related to ground mode."
    )
    loadaddress = 0x22DC240
    length = 0x48C40
    functions = NaOverlay11Functions
    data = NaOverlay11Data


class NaOverlay12Functions:
    pass


class NaOverlay12Data:
    pass


class NaOverlay12Section:
    name = "overlay12"
    description = "Unused; all zeroes."
    loadaddress = 0x238A140
    length = 0x20
    functions = NaOverlay12Functions
    data = NaOverlay12Data


class NaOverlay13Functions:
    EntryOverlay13 = Symbol(
        [0x0],
        [0x238A140],
        None,
        (
            "Main function of this overlay.\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nNo params."
        ),
    )

    ExitOverlay13 = Symbol(
        [0x50],
        [0x238A190],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    Overlay13SwitchFunctionNa238A1C8 = Symbol(
        [0x88],
        [0x238A1C8],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: int?",
    )

    Overlay13SwitchFunctionNa238A574 = Symbol(
        [0x434],
        [0x238A574],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GetPersonality = Symbol(
        [0x1C68],
        [0x238BDA8],
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
        [0x238BDF0],
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
        [0x238BE4C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: switch_case",
    )


class NaOverlay13Data:
    QUIZ_BORDER_COLOR_TABLE = Symbol(
        [0x1ED0], [0x238C010], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    PORTRAIT_ATTRIBUTES = Symbol(
        [0x1ED4], [0x238C014], 0x8, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_MALE_FEMALE_BOOST_TABLE = Symbol(
        [0x1EDC], [0x238C01C], 0x8, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY13_UNKNOWN_STRUCT__NA_238C024 = Symbol(
        [0x1EE4], [0x238C024], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_D_BOX_LAYOUT_1 = Symbol(
        [0x1EF4], [0x238C034], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_D_BOX_LAYOUT_2 = Symbol(
        [0x1F04], [0x238C044], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_D_BOX_LAYOUT_3 = Symbol(
        [0x1F14], [0x238C054], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_D_BOX_LAYOUT_4 = Symbol(
        [0x1F24], [0x238C064], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_MENU_1 = Symbol(
        [0x1F34], [0x238C074], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    STARTERS_PARTNER_IDS = Symbol(
        [0x1F4C], [0x238C08C], 0x2A, "type: struct monster_id_16[21]"
    )

    STARTERS_HERO_IDS = Symbol(
        [0x1F78], [0x238C0B8], 0x40, "type: struct monster_id_16[32]"
    )

    STARTERS_TYPE_INCOMPATIBILITY_TABLE = Symbol(
        [0x1FB8], [0x238C0F8], 0x54, "Note: unverified, ported from Irdkwia's notes"
    )

    STARTERS_STRINGS = Symbol(
        [0x200C], [0x238C14C], 0x60, "Irdkwia's notes: InsightsStringIDs"
    )

    QUIZ_QUESTION_STRINGS = Symbol([0x206C], [0x238C1AC], 0x84, "0x2 * (66 questions)")

    QUIZ_ANSWER_STRINGS = Symbol(
        [0x20F0], [0x238C230], 0x160, "0x2 * (175 answers + null-terminator)"
    )

    QUIZ_ANSWER_POINTS = Symbol(
        [0x2250],
        [0x238C390],
        0xAE0,
        "0x10 * (174 answers?)\n\nNote: unverified, ported from Irdkwia's notes",
    )

    OVERLAY13_RESERVED_SPACE = Symbol(
        [0x2D50], [0x238CE90], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY13_UNKNOWN_POINTER__NA_238CEA0 = Symbol(
        [0x2D60], [0x238CEA0], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY13_UNKNOWN_POINTER__NA_238CEA4 = Symbol(
        [0x2D64], [0x238CEA4], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY13_UNKNOWN_POINTER__NA_238CEA8 = Symbol(
        [0x2D68], [0x238CEA8], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_D_BOX_LAYOUT_5 = Symbol(
        [0x2D6C], [0x238CEAC], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_D_BOX_LAYOUT_6 = Symbol(
        [0x2D7C], [0x238CEBC], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_DEBUG_MENU = Symbol(
        [0x2D8C], [0x238CECC], 0x48, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY13_UNKNOWN_STRUCT__NA_238CF14 = Symbol(
        [0x2DD4], [0x238CF14], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_QUESTION_ANSWER_ASSOCIATIONS = Symbol(
        [0x2DE4],
        [0x238CF24],
        0x84,
        "0x2 * (66 questions)\n\nNote: unverified, ported from Irdkwia's notes",
    )


class NaOverlay13Section:
    name = "overlay13"
    description = (
        "Controls the personality test, including the available partners and playable"
        " Pokémon. The actual personality test questions are stored in the MESSAGE"
        " folder."
    )
    loadaddress = 0x238A140
    length = 0x2E80
    functions = NaOverlay13Functions
    data = NaOverlay13Data


class NaOverlay14Functions:
    SentrySetupState = Symbol(
        [0x0],
        [0x238A140],
        None,
        (
            "Allocates and initializes the sentry duty struct.\n\nPossibly the"
            " entrypoint of this overlay?\n\nr0: controls initial game state? If 2, the"
            " minigame starts in state 4 rather than state 6.\nreturn: always 1"
        ),
    )

    SentryUpdateDisplay = Symbol(
        [0xCBC],
        [0x238ADFC],
        None,
        (
            "Seems to update various parts of the display, such as the round"
            " number.\n\nNo params."
        ),
    )

    SentrySetExitingState = Symbol(
        [0x1598],
        [0x238B6D8],
        None,
        (
            "Sets the completion state to exiting, triggering the minigame to run its"
            " exit sequence.\n\nNo params."
        ),
    )

    SentryRunState = Symbol(
        [0x16BC],
        [0x238B7FC],
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
        [0x238C1C8],
        None,
        (
            "Queues up a new intermediate game state to transition to, where the"
            " transition handler will be called immediately by SentryRunState after the"
            " current state handler has returned.\n\nr0: new state"
        ),
    )

    SentryState0 = Symbol([0x20A8], [0x238C1E8], None, "No params.")

    SentryState1 = Symbol([0x20CC], [0x238C20C], None, "No params.")

    SentryState2 = Symbol([0x2124], [0x238C264], None, "No params.")

    SentryState3 = Symbol([0x2148], [0x238C288], None, "No params.")

    SentryState4 = Symbol([0x2270], [0x238C3B0], None, "No params.")

    SentryStateExit = Symbol(
        [0x2294],
        [0x238C3D4],
        None,
        "State 0x5: Exit (wraps SentrySetExitingState).\n\nNo params.",
    )

    SentryState6 = Symbol([0x22A0], [0x238C3E0], None, "No params.")

    SentryState7 = Symbol(
        [0x22C4],
        [0x238C404],
        None,
        (
            "This state corresponds to when Loudred tells you the instructions for the"
            " minigame (STRING_ID_SENTRY_INSTRUCTIONS).\n\nNo params."
        ),
    )

    SentryState8 = Symbol([0x22DC], [0x238C41C], None, "No params.")

    SentryState9 = Symbol([0x2300], [0x238C440], None, "No params.")

    SentryStateA = Symbol(
        [0x2324],
        [0x238C464],
        None,
        (
            "This state corresponds to when Loudred alerts you that someone is coming"
            " (STRING_ID_SENTRY_HERE_COMES).\n\nNo params."
        ),
    )

    SentryStateB = Symbol([0x233C], [0x238C47C], None, "No params.")

    SentryStateGenerateChoices = Symbol(
        [0x2354],
        [0x238C494],
        None,
        "State 0xC: Generate the four choices for a round.\n\nNo params.",
    )

    SentryStateGetUserChoice = Symbol(
        [0x2954],
        [0x238CA94],
        None,
        "State 0xD: Wait for the player to select an answer.\n\nNo params.",
    )

    SentryStateFinalizeRound = Symbol(
        [0x2E84],
        [0x238CFC4],
        None,
        (
            "State 0xE: Deal with the bookkeeping after the player has made a final"
            " choice for the round.\n\nThis includes things like incrementing the round"
            " counter. It also appears to check the final point count on the last round"
            " to determine the player's overall performance.\n\nNo params."
        ),
    )

    SentryStateF = Symbol([0x31C8], [0x238D308], None, "No params.")

    SentryState10 = Symbol([0x31E0], [0x238D320], None, "No params.")

    SentryState11 = Symbol(
        [0x3258],
        [0x238D398],
        None,
        (
            "This state corresponds to when the partner tells you to try again after"
            " the player makes a wrong selection for the first time"
            " (STRING_ID_SENTRY_TRY_AGAIN).\n\nNo params."
        ),
    )

    SentryState12 = Symbol([0x3270], [0x238D3B0], None, "No params.")

    SentryState13 = Symbol(
        [0x32A8],
        [0x238D3E8],
        None,
        (
            "This state corresponds to when Loudred tells you that you're out of time"
            " (STRING_ID_SENTRY_OUT_OF_TIME).\n\nNo params."
        ),
    )

    SentryState14 = Symbol(
        [0x32D0],
        [0x238D410],
        None,
        (
            "This state corresponds to when the player is shouting their guess"
            " (STRING_ID_SENTRY_FOOTPRINT_IS_6EE), and when Loudred tells the visitor"
            " to come in (STRING_ID_SENTRY_COME_IN_6EF).\n\nNo params."
        ),
    )

    SentryState15 = Symbol([0x32E8], [0x238D428], None, "No params.")

    SentryState16 = Symbol([0x3328], [0x238D468], None, "No params.")

    SentryState17 = Symbol(
        [0x3380],
        [0x238D4C0],
        None,
        (
            "This state corresponds to when Loudred tells the player that they chose"
            " the wrong answer (STRING_ID_SENTRY_WRONG,"
            " STRING_ID_SENTRY_BUCK_UP).\n\nNo params."
        ),
    )

    SentryState18 = Symbol([0x33F8], [0x238D538], None, "No params.")

    SentryState19 = Symbol(
        [0x3430],
        [0x238D570],
        None,
        (
            "This state seems to be similar to state 0x14, when the player is shouting"
            " their guess (STRING_ID_SENTRY_FOOTPRINT_IS_6EC), and when Loudred tells"
            " the visitor to come in (STRING_ID_SENTRY_COME_IN_6ED), but used in a"
            " different context (different state transitions to and from this"
            " state).\n\nNo params."
        ),
    )

    SentryState1A = Symbol([0x3448], [0x238D588], None, "No params.")

    SentryStateFinalizePoints = Symbol(
        [0x3488],
        [0x238D5C8],
        None,
        (
            "State 0x1B: Apply any modifiers to the player's point total, such as"
            " granting 2000 bonus points for 100% correctness.\n\nNo params."
        ),
    )

    SentryState1C = Symbol(
        [0x3518],
        [0x238D658],
        None,
        (
            "This state corresponds to when Loudred tells the player that they chose"
            " the correct answer ('Yep! Looks like you're right!').\n\nNo params."
        ),
    )

    SentryState1D = Symbol([0x355C], [0x238D69C], None, "No params.")

    SentryState1E = Symbol(
        [0x35C0],
        [0x238D700],
        None,
        (
            "This state corresponds to one of the possible dialogue options when you've"
            " finished all the rounds (STRING_ID_SENTRY_KEEP_YOU_WAITING,"
            " STRING_ID_SENTRY_THATLL_DO_IT).\n\nNo params."
        ),
    )

    SentryState1F = Symbol([0x35D8], [0x238D718], None, "No params.")

    SentryState20 = Symbol(
        [0x3654],
        [0x238D794],
        None,
        (
            "This state corresponds to one of the possible dialogue options when you've"
            " finished all the rounds (STRING_ID_SENTRY_NO_MORE_VISITORS,"
            " STRING_ID_SENTRY_THATS_ALL).\n\nNo params."
        ),
    )

    SentryState21 = Symbol([0x366C], [0x238D7AC], None, "No params.")


class NaOverlay14Data:
    SENTRY_DUTY_STRUCT_SIZE = Symbol(
        [0x3C4], [0x238A504], 0x4, "Number of bytes in the sentry duty struct (14548)."
    )

    SENTRY_LOUDRED_MONSTER_ID = Symbol(
        [0x200C],
        [0x238C14C],
        0x4,
        "Monster ID for Loudred, used as the speaker ID for dialog.",
    )

    STRING_ID_SENTRY_TOP_SESSIONS = Symbol(
        [0x2010],
        [0x238C150],
        0x4,
        "String ID 0x6D9:\n Here are the rankings for the\ntop sentry sessions.",
    )

    STRING_ID_SENTRY_INSTRUCTIONS = Symbol(
        [0x2014],
        [0x238C154],
        0x4,
        (
            "String ID 0x6D8:\n Look at the footprint on the top\nscreen, OK? Then"
            " identify the Pokémon![C]\n You can get only [CS:V]two wrong[CR],"
            " OK?\n[partner] will keep an eye on things!"
        ),
    )

    STRING_ID_SENTRY_HERE_COMES = Symbol(
        [0x2018],
        [0x238C158],
        0x4,
        (
            "String ID 0x6DA:\n Here comes a Pokémon! Check\nits footprint and tell me"
            " what it is!"
        ),
    )

    STRING_ID_SENTRY_WHOSE_FOOTPRINT = Symbol(
        [0x201C], [0x238C15C], 0x4, "String ID 0x6DB:\n Whose footprint is this?[W:60]"
    )

    STRING_ID_SENTRY_TRY_AGAIN = Symbol(
        [0x2024],
        [0x238C164],
        0x4,
        "String ID 0x6EB:\n Huh? I don't think so. Try again!",
    )

    STRING_ID_SENTRY_OUT_OF_TIME = Symbol(
        [0x2028],
        [0x238C168],
        0x4,
        "String ID 0x6DC:\n [se_play:0][W:30]Out of time! Pick up the pace![W:75]",
    )

    STRING_ID_SENTRY_FOOTPRINT_IS_6EE = Symbol(
        [0x202C],
        [0x238C16C],
        0x4,
        (
            "String ID 0x6EE:\n The footprint is [kind:]'s!\nThe footprint is"
            " [kind:]'s![W:60]"
        ),
    )

    STRING_ID_SENTRY_COME_IN_6EF = Symbol(
        [0x2030],
        [0x238C170],
        0x4,
        "String ID 0x6EF:\n Heard ya! Come in, visitor![W:30]",
    )

    STRING_ID_SENTRY_WRONG = Symbol(
        [0x2038],
        [0x238C178],
        0x4,
        "String ID 0x6F1:\n ......[se_play:0][W:30]Huh?! Looks wrong to me![W:50]",
    )

    STRING_ID_SENTRY_BUCK_UP = Symbol(
        [0x203C],
        [0x238C17C],
        0x4,
        (
            "String ID 0x6F2 (and also used as Loudred's speaker ID after subtracting"
            " 0x5B0):\n The correct answer is\n[kind:]! Buck up! And snap to"
            " it![se_play:0][W:120]"
        ),
    )

    STRING_ID_SENTRY_FOOTPRINT_IS_6EC = Symbol(
        [0x2044],
        [0x238C184],
        0x4,
        (
            "String ID 0x6EC:\n The footprint is [kind:]'s!\nThe footprint is"
            " [kind:]'s![W:60]"
        ),
    )

    STRING_ID_SENTRY_COME_IN_6ED = Symbol(
        [0x2048],
        [0x238C188],
        0x4,
        "String ID 0x6ED:\n Heard ya! Come in, visitor![W:30]",
    )

    STRING_ID_SENTRY_KEEP_YOU_WAITING = Symbol(
        [0x2050],
        [0x238C190],
        0x4,
        "String ID 0x6F3:\n [se_play:0]Sorry to keep you waiting.",
    )

    STRING_ID_SENTRY_THATLL_DO_IT = Symbol(
        [0x2054],
        [0x238C194],
        0x4,
        (
            "String ID 0x6F4:\n [partner] and [hero]![C]\n That'll do it! Now get back"
            " here!"
        ),
    )

    SENTRY_CHATOT_MONSTER_ID = Symbol(
        [0x2058],
        [0x238C198],
        0x4,
        "Monster ID for Chatot, used as the speaker ID for dialog.",
    )

    STRING_ID_SENTRY_NO_MORE_VISITORS = Symbol(
        [0x205C],
        [0x238C19C],
        0x4,
        "String ID 0x6F5:\n [se_play:0]No more visitors! No more\nvisitors! ♪",
    )

    STRING_ID_SENTRY_THATS_ALL = Symbol(
        [0x2060],
        [0x238C1A0],
        0x4,
        (
            "String ID 0x6F6:\n OK, got that![C]\n Hey, [partner] and\n[hero]![C]\n"
            " That's all for today! Now get\nback here!"
        ),
    )

    SENTRY_GROVYLE_MONSTER_ID = Symbol(
        [0x2924],
        [0x238CA64],
        0x4,
        (
            "Monster ID for Grovyle, which appears to be explicitly excluded when"
            " generating species choices."
        ),
    )

    FOOTPRINT_DEBUG_MENU = Symbol([0x3960], [0x238DAA0], 0x48, "")

    SENTRY_DUTY_PTR = Symbol(
        [0x3A40], [0x238DB80], 0x4, "Pointer to the SENTRY_DUTY_STRUCT."
    )

    SENTRY_DUTY_STATE_HANDLER_TABLE = Symbol(
        [0x3A54],
        [0x238DB94],
        0x8C,
        (
            "Null-terminated table of handler functions for the different states in the"
            " state machine. See SentryRunState.\n\ntype: state_handler_fn_t[35]"
        ),
    )


class NaOverlay14Section:
    name = "overlay14"
    description = "Runs the sentry duty minigame."
    loadaddress = 0x238A140
    length = 0x3AE0
    functions = NaOverlay14Functions
    data = NaOverlay14Data


class NaOverlay15Functions:
    pass


class NaOverlay15Data:
    BANK_MAIN_MENU = Symbol([0xF14], [0x238B054], 0x28, "")

    BANK_D_BOX_LAYOUT_1 = Symbol(
        [0xF3C], [0x238B07C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    BANK_D_BOX_LAYOUT_2 = Symbol(
        [0xF4C], [0x238B08C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    BANK_D_BOX_LAYOUT_3 = Symbol(
        [0xF5C], [0x238B09C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    BANK_D_BOX_LAYOUT_4 = Symbol(
        [0xF6C], [0x238B0AC], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    BANK_D_BOX_LAYOUT_5 = Symbol(
        [0xF7C], [0x238B0BC], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY15_RESERVED_SPACE = Symbol(
        [0x1024], [0x238B164], 0x1C, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY15_UNKNOWN_POINTER__NA_238B180 = Symbol(
        [0x1040], [0x238B180], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )


class NaOverlay15Section:
    name = "overlay15"
    description = "Controls the Duskull Bank."
    loadaddress = 0x238A140
    length = 0x1060
    functions = NaOverlay15Functions
    data = NaOverlay15Data


class NaOverlay16Functions:
    pass


class NaOverlay16Data:
    EVO_MENU_CONFIRM = Symbol([0x2BC8], [0x238CD08], 0x18, "Irdkwia's notes: 3*0x8")

    EVO_SUBMENU = Symbol([0x2BE0], [0x238CD20], 0x20, "Irdkwia's notes: 4*0x8")

    EVO_MAIN_MENU = Symbol([0x2C00], [0x238CD40], 0x20, "Irdkwia's notes: 4*0x8")

    EVO_MENU_STRING_IDS = Symbol(
        [0x2C20],
        [0x238CD60],
        0x34,
        "26*0x2\n\nNote: unverified, ported from Irdkwia's notes",
    )

    EVO_D_BOX_LAYOUT_1 = Symbol(
        [0x2C54], [0x238CD94], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    EVO_D_BOX_LAYOUT_2 = Symbol(
        [0x2C64], [0x238CDA4], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    EVO_D_BOX_LAYOUT_3 = Symbol(
        [0x2C74], [0x238CDB4], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    EVO_D_BOX_LAYOUT_4 = Symbol(
        [0x2C84], [0x238CDC4], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    EVO_D_BOX_LAYOUT_5 = Symbol(
        [0x2C94], [0x238CDD4], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    EVO_D_BOX_LAYOUT_6 = Symbol(
        [0x2CA4], [0x238CDE4], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    EVO_D_BOX_LAYOUT_7 = Symbol(
        [0x2CB4], [0x238CDF4], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY16_RESERVED_SPACE = Symbol(
        [0x2CF4], [0x238CE34], 0xC, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY16_UNKNOWN_POINTER__NA_238CE40 = Symbol(
        [0x2D00], [0x238CE40], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY16_UNKNOWN_POINTER__NA_238CE58 = Symbol(
        [0x2D18], [0x238CE58], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )


class NaOverlay16Section:
    name = "overlay16"
    description = "Controls Luminous Spring."
    loadaddress = 0x238A140
    length = 0x2D20
    functions = NaOverlay16Functions
    data = NaOverlay16Data


class NaOverlay17Functions:
    pass


class NaOverlay17Data:
    ASSEMBLY_D_BOX_LAYOUT_1 = Symbol(
        [0x19F4], [0x238BB34], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    ASSEMBLY_D_BOX_LAYOUT_2 = Symbol(
        [0x1A04], [0x238BB44], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    ASSEMBLY_D_BOX_LAYOUT_3 = Symbol(
        [0x1A14], [0x238BB54], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    ASSEMBLY_D_BOX_LAYOUT_4 = Symbol(
        [0x1A24], [0x238BB64], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    ASSEMBLY_D_BOX_LAYOUT_5 = Symbol(
        [0x1A34], [0x238BB74], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    ASSEMBLY_MENU_CONFIRM = Symbol([0x1A44], [0x238BB84], 0x18, "")

    ASSEMBLY_MAIN_MENU_1 = Symbol([0x1A5C], [0x238BB9C], 0x18, "")

    ASSEMBLY_MAIN_MENU_2 = Symbol([0x1A74], [0x238BBB4], 0x20, "")

    ASSEMBLY_SUBMENU_1 = Symbol([0x1A94], [0x238BBD4], 0x28, "")

    ASSEMBLY_SUBMENU_2 = Symbol([0x1ABC], [0x238BBFC], 0x30, "")

    ASSEMBLY_SUBMENU_3 = Symbol([0x1AEC], [0x238BC2C], 0x30, "")

    ASSEMBLY_SUBMENU_4 = Symbol([0x1B1C], [0x238BC5C], 0x38, "")

    ASSEMBLY_SUBMENU_5 = Symbol([0x1B54], [0x238BC94], 0x38, "")

    ASSEMBLY_SUBMENU_6 = Symbol([0x1B8C], [0x238BCCC], 0x38, "")

    ASSEMBLY_SUBMENU_7 = Symbol([0x1BC4], [0x238BD04], 0x40, "")

    OVERLAY17_FUNCTION_POINTER_TABLE = Symbol(
        [0x1C04], [0x238BD44], 0xA8, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY17_RESERVED_SPACE = Symbol(
        [0x1CAC], [0x238BDEC], 0x14, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY17_UNKNOWN_POINTER__NA_238BE00 = Symbol(
        [0x1CC0], [0x238BE00], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY17_UNKNOWN_POINTER__NA_238BE04 = Symbol(
        [0x1CC4], [0x238BE04], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY17_UNKNOWN_POINTER__NA_238BE08 = Symbol(
        [0x1CC8], [0x238BE08], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )


class NaOverlay17Section:
    name = "overlay17"
    description = "Controls the Chimecho Assembly."
    loadaddress = 0x238A140
    length = 0x1CE0
    functions = NaOverlay17Functions
    data = NaOverlay17Data


class NaOverlay18Functions:
    pass


class NaOverlay18Data:
    OVERLAY18_D_BOX_LAYOUT_1 = Symbol(
        [0x3130], [0x238D270], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_2 = Symbol(
        [0x3140], [0x238D280], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_3 = Symbol(
        [0x3150], [0x238D290], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_4 = Symbol(
        [0x3160], [0x238D2A0], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_5 = Symbol(
        [0x3170], [0x238D2B0], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_6 = Symbol(
        [0x3180], [0x238D2C0], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_7 = Symbol(
        [0x3190], [0x238D2D0], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_8 = Symbol(
        [0x31A0], [0x238D2E0], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_9 = Symbol(
        [0x31B0], [0x238D2F0], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_10 = Symbol(
        [0x31C0], [0x238D300], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_D_BOX_LAYOUT_11 = Symbol(
        [0x31D0], [0x238D310], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    MOVES_MENU_CONFIRM = Symbol([0x31E0], [0x238D320], 0x18, "")

    MOVES_SUBMENU_1 = Symbol([0x31F8], [0x238D338], 0x20, "")

    MOVES_SUBMENU_2 = Symbol([0x3218], [0x238D358], 0x20, "")

    MOVES_MAIN_MENU = Symbol([0x3238], [0x238D378], 0x20, "")

    MOVES_SUBMENU_3 = Symbol([0x3258], [0x238D398], 0x28, "")

    MOVES_SUBMENU_4 = Symbol([0x3280], [0x238D3C0], 0x30, "")

    MOVES_SUBMENU_5 = Symbol([0x32B0], [0x238D3F0], 0x48, "")

    MOVES_SUBMENU_6 = Symbol([0x32F8], [0x238D438], 0x48, "")

    MOVES_SUBMENU_7 = Symbol([0x3340], [0x238D480], 0x48, "")

    OVERLAY18_FUNCTION_POINTER_TABLE = Symbol(
        [0x3388], [0x238D4C8], 0x130, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_RESERVED_SPACE = Symbol(
        [0x34DC], [0x238D61C], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_UNKNOWN_POINTER__NA_238D620 = Symbol(
        [0x34E0], [0x238D620], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_UNKNOWN_POINTER__NA_238D624 = Symbol(
        [0x34E4], [0x238D624], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY18_UNKNOWN_POINTER__NA_238D628 = Symbol(
        [0x34E8], [0x238D628], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )


class NaOverlay18Section:
    name = "overlay18"
    description = "Controls the Electivire Link Shop."
    loadaddress = 0x238A140
    length = 0x3500
    functions = NaOverlay18Functions
    data = NaOverlay18Data


class NaOverlay19Functions:
    GetBarItem = Symbol(
        [0x0],
        [0x238A140],
        None,
        (
            "Gets the struct bar_item from BAR_AVAILABLE_ITEMS with the specified item"
            " ID.\n\nr0: item ID\nreturn: struct bar_item*"
        ),
    )

    GetRecruitableMonsterAll = Symbol(
        [0x84],
        [0x238A1C4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: int?",
    )

    GetRecruitableMonsterList = Symbol(
        [0x134],
        [0x238A274],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: int?",
    )

    GetRecruitableMonsterListRestricted = Symbol(
        [0x1DC],
        [0x238A31C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: int?",
    )


class NaOverlay19Data:
    OVERLAY19_UNKNOWN_TABLE__NA_238DAE0 = Symbol(
        [0x39A0],
        [0x238DAE0],
        0x8,
        "4*0x2\n\nNote: unverified, ported from Irdkwia's notes",
    )

    BAR_UNLOCKABLE_DUNGEONS_TABLE = Symbol(
        [0x39A8],
        [0x238DAE8],
        0xC,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " dungeon_id_16[6]"
        ),
    )

    BAR_RECRUITABLE_MONSTER_TABLE = Symbol(
        [0x39B4],
        [0x238DAF4],
        0xD8,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " monster_id_16[108]"
        ),
    )

    BAR_AVAILABLE_ITEMS = Symbol(
        [0x3A8C],
        [0x238DBCC],
        0x5AC,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: struct bar_item[66]",
    )

    OVERLAY19_UNKNOWN_STRING_IDS__NA_238E178 = Symbol(
        [0x4038], [0x238E178], 0x2C, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY19_UNKNOWN_STRUCT__NA_238E1A4 = Symbol(
        [0x4064],
        [0x238E1A4],
        0x28,
        "5*0x8\n\nNote: unverified, ported from Irdkwia's notes",
    )

    OVERLAY19_UNKNOWN_STRING_IDS__NA_238E1CC = Symbol(
        [0x408C], [0x238E1CC], 0xC, "Note: unverified, ported from Irdkwia's notes"
    )

    BAR_D_BOX_LAYOUT_1 = Symbol(
        [0x4098], [0x238E1D8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    BAR_D_BOX_LAYOUT_2 = Symbol(
        [0x40A8], [0x238E1E8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    BAR_D_BOX_LAYOUT_3 = Symbol(
        [0x40B8], [0x238E1F8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    BAR_MENU_CONFIRM_1 = Symbol([0x40C8], [0x238E208], 0x18, "")

    BAR_MENU_CONFIRM_2 = Symbol([0x40E0], [0x238E220], 0x18, "")

    OVERLAY19_UNKNOWN_STRING_IDS__NA_238E238 = Symbol(
        [0x40F8], [0x238E238], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    BAR_MAIN_MENU = Symbol([0x4110], [0x238E250], 0x20, "")

    BAR_SUBMENU_1 = Symbol([0x4130], [0x238E270], 0x20, "")

    BAR_SUBMENU_2 = Symbol([0x4150], [0x238E290], 0x30, "")

    OVERLAY19_RESERVED_SPACE = Symbol(
        [0x4204], [0x238E344], 0x1C, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY19_UNKNOWN_POINTER__NA_238E360 = Symbol(
        [0x4220], [0x238E360], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY19_UNKNOWN_POINTER__NA_238E364 = Symbol(
        [0x4224], [0x238E364], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )


class NaOverlay19Section:
    name = "overlay19"
    description = "Controls Spinda's Juice Bar."
    loadaddress = 0x238A140
    length = 0x4240
    functions = NaOverlay19Functions
    data = NaOverlay19Data


class NaOverlay2Functions:
    pass


class NaOverlay2Data:
    pass


class NaOverlay2Section:
    name = "overlay2"
    description = (
        "Controls the Nintendo WFC Settings interface, accessed from the top menu"
        " (Other > Nintendo WFC > Nintendo WFC Settings). Presumably contains code for"
        " Nintendo Wi-Fi setup."
    )
    loadaddress = 0x2329520
    length = 0x2AFA0
    functions = NaOverlay2Functions
    data = NaOverlay2Data


class NaOverlay20Functions:
    pass


class NaOverlay20Data:
    OVERLAY20_UNKNOWN_POINTER__NA_238CF7C = Symbol(
        [0x2E3C], [0x238CF7C], 0x8, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_MENU_CONFIRM_1 = Symbol([0x2E44], [0x238CF84], 0x18, "")

    RECYCLE_MENU_CONFIRM_2 = Symbol([0x2E5C], [0x238CF9C], 0x18, "")

    RECYCLE_SUBMENU_1 = Symbol([0x2E74], [0x238CFB4], 0x18, "")

    RECYCLE_SUBMENU_2 = Symbol([0x2E8C], [0x238CFCC], 0x20, "")

    RECYCLE_MAIN_MENU_1 = Symbol([0x2EAC], [0x238CFEC], 0x28, "")

    OVERLAY20_UNKNOWN_TABLE__NA_238D014 = Symbol(
        [0x2ED4], [0x238D014], 0x14, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT_1 = Symbol(
        [0x2EE8], [0x238D028], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT_2 = Symbol(
        [0x2EF8], [0x238D038], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT_3 = Symbol(
        [0x2F08], [0x238D048], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT_4 = Symbol(
        [0x2F18], [0x238D058], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT_5 = Symbol(
        [0x2F28], [0x238D068], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT_6 = Symbol(
        [0x2F38], [0x238D078], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_MAIN_MENU_2 = Symbol([0x2F48], [0x238D088], 0x20, "")

    RECYCLE_D_BOX_LAYOUT_7 = Symbol(
        [0x2F68], [0x238D0A8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT_8 = Symbol(
        [0x2F78], [0x238D0B8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT_9 = Symbol(
        [0x2F88], [0x238D0C8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT1_0 = Symbol(
        [0x2F98], [0x238D0D8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_D_BOX_LAYOUT1_1 = Symbol(
        [0x2FA8], [0x238D0E8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_MAIN_MENU_3 = Symbol([0x2FB8], [0x238D0F8], 0x18, "")

    OVERLAY20_RESERVED_SPACE = Symbol(
        [0x2FD0], [0x238D110], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY20_UNKNOWN_POINTER__NA_238D120 = Symbol(
        [0x2FE0], [0x238D120], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY20_UNKNOWN_POINTER__NA_238D124 = Symbol(
        [0x2FE4], [0x238D124], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY20_UNKNOWN_POINTER__NA_238D128 = Symbol(
        [0x2FE8], [0x238D128], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY20_UNKNOWN_POINTER__NA_238D12C = Symbol(
        [0x2FEC], [0x238D12C], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )


class NaOverlay20Section:
    name = "overlay20"
    description = "Controls the Recycle Shop."
    loadaddress = 0x238A140
    length = 0x3000
    functions = NaOverlay20Functions
    data = NaOverlay20Data


class NaOverlay21Functions:
    pass


class NaOverlay21Data:
    SWAP_SHOP_D_BOX_LAYOUT_1 = Symbol(
        [0x28E8], [0x238CA28], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    SWAP_SHOP_MENU_CONFIRM = Symbol([0x28F8], [0x238CA38], 0x18, "")

    SWAP_SHOP_SUBMENU_1 = Symbol([0x2910], [0x238CA50], 0x18, "")

    SWAP_SHOP_SUBMENU_2 = Symbol([0x2928], [0x238CA68], 0x20, "")

    SWAP_SHOP_MAIN_MENU_1 = Symbol([0x2948], [0x238CA88], 0x20, "")

    SWAP_SHOP_MAIN_MENU_2 = Symbol([0x2968], [0x238CAA8], 0x28, "")

    SWAP_SHOP_SUBMENU_3 = Symbol([0x2990], [0x238CAD0], 0x30, "")

    OVERLAY21_UNKNOWN_STRING_IDS = Symbol(
        [0x29C0], [0x238CB00], 0x38, "Note: unverified, ported from Irdkwia's notes"
    )

    SWAP_SHOP_D_BOX_LAYOUT_2 = Symbol(
        [0x29F8], [0x238CB38], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    SWAP_SHOP_D_BOX_LAYOUT_3 = Symbol(
        [0x2A08], [0x238CB48], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    SWAP_SHOP_D_BOX_LAYOUT_4 = Symbol(
        [0x2A18], [0x238CB58], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    SWAP_SHOP_D_BOX_LAYOUT_5 = Symbol(
        [0x2A28], [0x238CB68], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    SWAP_SHOP_D_BOX_LAYOUT_6 = Symbol(
        [0x2A38], [0x238CB78], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    SWAP_SHOP_D_BOX_LAYOUT_7 = Symbol(
        [0x2A48], [0x238CB88], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    SWAP_SHOP_D_BOX_LAYOUT_8 = Symbol(
        [0x2A58], [0x238CB98], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    SWAP_SHOP_D_BOX_LAYOUT_9 = Symbol(
        [0x2A68], [0x238CBA8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY21_JP_STRING = Symbol([0x2DDC], [0x238CF1C], 0x8, "合成：")

    OVERLAY21_RESERVED_SPACE = Symbol(
        [0x2DF8], [0x238CF38], 0x8, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY21_UNKNOWN_POINTER__NA_238CF40 = Symbol(
        [0x2E00], [0x238CF40], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY21_UNKNOWN_POINTER__NA_238CF44 = Symbol(
        [0x2E04], [0x238CF44], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )


class NaOverlay21Section:
    name = "overlay21"
    description = "Controls the Croagunk Swap Shop."
    loadaddress = 0x238A140
    length = 0x2E20
    functions = NaOverlay21Functions
    data = NaOverlay21Data


class NaOverlay22Functions:
    pass


class NaOverlay22Data:
    SHOP_D_BOX_LAYOUT_1 = Symbol(
        [0x46DC], [0x238E81C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_D_BOX_LAYOUT_2 = Symbol(
        [0x46FC], [0x238E83C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY22_UNKNOWN_STRUCT__NA_238E85C = Symbol(
        [0x471C], [0x238E85C], 0xC, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_MENU_CONFIRM = Symbol([0x4728], [0x238E868], 0x18, "")

    SHOP_MAIN_MENU_1 = Symbol([0x4740], [0x238E880], 0x20, "")

    SHOP_MAIN_MENU_2 = Symbol([0x4760], [0x238E8A0], 0x20, "")

    SHOP_MAIN_MENU_3 = Symbol([0x4780], [0x238E8C0], 0x30, "")

    OVERLAY22_UNKNOWN_STRING_IDS = Symbol(
        [0x47B0], [0x238E8F0], 0x60, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_D_BOX_LAYOUT_3 = Symbol(
        [0x4810], [0x238E950], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_D_BOX_LAYOUT_4 = Symbol(
        [0x4820], [0x238E960], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_D_BOX_LAYOUT_5 = Symbol(
        [0x4830], [0x238E970], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_D_BOX_LAYOUT_6 = Symbol(
        [0x4840], [0x238E980], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_D_BOX_LAYOUT_7 = Symbol(
        [0x4850], [0x238E990], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_D_BOX_LAYOUT_8 = Symbol(
        [0x4860], [0x238E9A0], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_D_BOX_LAYOUT_9 = Symbol(
        [0x4870], [0x238E9B0], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_D_BOX_LAYOUT_10 = Symbol(
        [0x4880], [0x238E9C0], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY22_RESERVED_SPACE = Symbol(
        [0x4B18], [0x238EC58], 0x8, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY22_UNKNOWN_POINTER__NA_238EC60 = Symbol(
        [0x4B20], [0x238EC60], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY22_UNKNOWN_POINTER__NA_238EC64 = Symbol(
        [0x4B24], [0x238EC64], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY22_UNKNOWN_POINTER__NA_238EC68 = Symbol(
        [0x4B28], [0x238EC68], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY22_UNKNOWN_POINTER__NA_238EC6C = Symbol(
        [0x4B2C], [0x238EC6C], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY22_UNKNOWN_POINTER__NA_238EC70 = Symbol(
        [0x4B30], [0x238EC70], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )


class NaOverlay22Section:
    name = "overlay22"
    description = "Controls the Kecleon Shop in Treasure Town."
    loadaddress = 0x238A140
    length = 0x4B40
    functions = NaOverlay22Functions
    data = NaOverlay22Data


class NaOverlay23Functions:
    pass


class NaOverlay23Data:
    OVERLAY23_UNKNOWN_VALUE__NA_238D2E8 = Symbol(
        [0x31A8], [0x238D2E8], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY23_UNKNOWN_VALUE__NA_238D2EC = Symbol(
        [0x31AC], [0x238D2EC], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY23_UNKNOWN_STRUCT__NA_238D2F0 = Symbol(
        [0x31B0], [0x238D2F0], 0xC, "Note: unverified, ported from Irdkwia's notes"
    )

    STORAGE_MENU_CONFIRM = Symbol([0x31BC], [0x238D2FC], 0x18, "")

    STORAGE_MAIN_MENU_1 = Symbol([0x31D4], [0x238D314], 0x20, "")

    STORAGE_MAIN_MENU_2 = Symbol([0x31F4], [0x238D334], 0x20, "")

    STORAGE_MAIN_MENU_3 = Symbol([0x3214], [0x238D354], 0x20, "")

    STORAGE_MAIN_MENU_4 = Symbol([0x3234], [0x238D374], 0x28, "")

    OVERLAY23_UNKNOWN_STRING_IDS = Symbol(
        [0x325C], [0x238D39C], 0x2C, "Note: unverified, ported from Irdkwia's notes"
    )

    STORAGE_D_BOX_LAYOUT_1 = Symbol(
        [0x3288], [0x238D3C8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    STORAGE_D_BOX_LAYOUT_2 = Symbol(
        [0x3298], [0x238D3D8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    STORAGE_D_BOX_LAYOUT_3 = Symbol(
        [0x32A8], [0x238D3E8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    STORAGE_D_BOX_LAYOUT_4 = Symbol(
        [0x32B8], [0x238D3F8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    STORAGE_D_BOX_LAYOUT_5 = Symbol(
        [0x32C8], [0x238D408], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    STORAGE_D_BOX_LAYOUT_6 = Symbol(
        [0x32D8], [0x238D418], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    STORAGE_D_BOX_LAYOUT_7 = Symbol(
        [0x32E8], [0x238D428], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    STORAGE_D_BOX_LAYOUT_8 = Symbol(
        [0x32F8], [0x238D438], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY23_RESERVED_SPACE = Symbol(
        [0x3748], [0x238D888], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY23_UNKNOWN_POINTER__NA_238D8A0 = Symbol(
        [0x3760], [0x238D8A0], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )


class NaOverlay23Section:
    name = "overlay23"
    description = (
        "Controls Kangaskhan Storage (both in Treasure Town and via Kangaskhan Rocks)."
    )
    loadaddress = 0x238A140
    length = 0x3780
    functions = NaOverlay23Functions
    data = NaOverlay23Data


class NaOverlay24Functions:
    pass


class NaOverlay24Data:
    OVERLAY24_UNKNOWN_STRUCT__NA_238C508 = Symbol(
        [0x23C8], [0x238C508], 0xC, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY24_UNKNOWN_STRUCT__NA_238C514 = Symbol(
        [0x23D4], [0x238C514], 0xC, "Note: unverified, ported from Irdkwia's notes"
    )

    DAYCARE_MENU_CONFIRM = Symbol([0x23E0], [0x238C520], 0x18, "")

    DAYCARE_MAIN_MENU = Symbol([0x23F8], [0x238C538], 0x20, "")

    OVERLAY24_UNKNOWN_STRING_IDS = Symbol(
        [0x2418], [0x238C558], 0x38, "Note: unverified, ported from Irdkwia's notes"
    )

    DAYCARE_D_BOX_LAYOUT_1 = Symbol(
        [0x2450], [0x238C590], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DAYCARE_D_BOX_LAYOUT_2 = Symbol(
        [0x2460], [0x238C5A0], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DAYCARE_D_BOX_LAYOUT_3 = Symbol(
        [0x2470], [0x238C5B0], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DAYCARE_D_BOX_LAYOUT_4 = Symbol(
        [0x2480], [0x238C5C0], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DAYCARE_D_BOX_LAYOUT_5 = Symbol(
        [0x2490], [0x238C5D0], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY24_RESERVED_SPACE = Symbol(
        [0x24A0], [0x238C5E0], 0x20, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY24_UNKNOWN_POINTER__NA_238C600 = Symbol(
        [0x24C0], [0x238C600], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )


class NaOverlay24Section:
    name = "overlay24"
    description = "Controls the Chansey Day Care."
    loadaddress = 0x238A140
    length = 0x24E0
    functions = NaOverlay24Functions
    data = NaOverlay24Data


class NaOverlay25Functions:
    pass


class NaOverlay25Data:
    OVERLAY25_UNKNOWN_STRUCT__NA_238B498 = Symbol(
        [0x1358], [0x238B498], 0xC, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_D_BOX_LAYOUT_1 = Symbol(
        [0x1364], [0x238B4A4], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_MENU_CONFIRM = Symbol([0x1374], [0x238B4B4], 0x18, "")

    APPRAISAL_MAIN_MENU = Symbol([0x138C], [0x238B4CC], 0x20, "")

    APPRAISAL_SUBMENU = Symbol([0x13AC], [0x238B4EC], 0x20, "")

    OVERLAY25_UNKNOWN_STRING_IDS = Symbol(
        [0x13CC], [0x238B50C], 0x28, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_D_BOX_LAYOUT_2 = Symbol(
        [0x13F4], [0x238B534], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_D_BOX_LAYOUT_3 = Symbol(
        [0x1404], [0x238B544], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_D_BOX_LAYOUT_4 = Symbol(
        [0x1414], [0x238B554], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_D_BOX_LAYOUT_5 = Symbol(
        [0x1424], [0x238B564], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_D_BOX_LAYOUT_6 = Symbol(
        [0x1434], [0x238B574], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_D_BOX_LAYOUT_7 = Symbol(
        [0x1444], [0x238B584], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_D_BOX_LAYOUT_8 = Symbol(
        [0x1454], [0x238B594], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY25_RESERVED_SPACE = Symbol(
        [0x1484], [0x238B5C4], 0x1C, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY25_UNKNOWN_POINTER__NA_238B5E0 = Symbol(
        [0x14A0], [0x238B5E0], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )


class NaOverlay25Section:
    name = "overlay25"
    description = "Controls Xatu Appraisal."
    loadaddress = 0x238A140
    length = 0x14C0
    functions = NaOverlay25Functions
    data = NaOverlay25Data


class NaOverlay26Functions:
    pass


class NaOverlay26Data:
    OVERLAY26_UNKNOWN_TABLE__NA_238AE20 = Symbol(
        [0xCE0],
        [0x238AE20],
        0x8C,
        "0x6 + 11*0xC + 0x2\n\nNote: unverified, ported from Irdkwia's notes",
    )

    OVERLAY26_RESERVED_SPACE = Symbol(
        [0xE08], [0x238AF48], 0x18, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY26_UNKNOWN_POINTER__NA_238AF60 = Symbol(
        [0xE20], [0x238AF60], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY26_UNKNOWN_POINTER__NA_238AF64 = Symbol(
        [0xE24], [0x238AF64], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY26_UNKNOWN_POINTER__NA_238AF68 = Symbol(
        [0xE28], [0x238AF68], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY26_UNKNOWN_POINTER__NA_238AF6C = Symbol(
        [0xE2C], [0x238AF6C], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY26_UNKNOWN_POINTER5__NA_238AF70 = Symbol(
        [0xE30], [0x238AF70], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )


class NaOverlay26Section:
    name = "overlay26"
    description = (
        "Related to mission completion. It's loaded when the dungeon completion summary"
        " is shown upon exiting a dungeon, and during the cutscenes where you collect"
        " mission rewards from clients."
    )
    loadaddress = 0x238A140
    length = 0xE40
    functions = NaOverlay26Functions
    data = NaOverlay26Data


class NaOverlay27Functions:
    pass


class NaOverlay27Data:
    OVERLAY27_UNKNOWN_VALUE__NA_238C948 = Symbol(
        [0x2808], [0x238C948], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY27_UNKNOWN_VALUE__NA_238C94C = Symbol(
        [0x280C], [0x238C94C], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY27_UNKNOWN_STRUCT__NA_238C950 = Symbol(
        [0x2810], [0x238C950], 0xC, "Note: unverified, ported from Irdkwia's notes"
    )

    DISCARD_ITEMS_MENU_CONFIRM = Symbol([0x281C], [0x238C95C], 0x18, "")

    DISCARD_ITEMS_SUBMENU_1 = Symbol([0x2834], [0x238C974], 0x20, "")

    DISCARD_ITEMS_SUBMENU_2 = Symbol([0x2854], [0x238C994], 0x20, "")

    DISCARD_ITEMS_MAIN_MENU = Symbol([0x2874], [0x238C9B4], 0x28, "")

    OVERLAY27_UNKNOWN_STRING_IDS = Symbol(
        [0x289C], [0x238C9DC], 0x30, "Note: unverified, ported from Irdkwia's notes"
    )

    DISCARD_D_BOX_LAYOUT_1 = Symbol(
        [0x28CC], [0x238CA0C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DISCARD_D_BOX_LAYOUT_2 = Symbol(
        [0x28DC], [0x238CA1C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DISCARD_D_BOX_LAYOUT_3 = Symbol(
        [0x28EC], [0x238CA2C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DISCARD_D_BOX_LAYOUT_4 = Symbol(
        [0x28FC], [0x238CA3C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DISCARD_D_BOX_LAYOUT_5 = Symbol(
        [0x290C], [0x238CA4C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DISCARD_D_BOX_LAYOUT_6 = Symbol(
        [0x291C], [0x238CA5C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DISCARD_D_BOX_LAYOUT_7 = Symbol(
        [0x292C], [0x238CA6C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DISCARD_D_BOX_LAYOUT_8 = Symbol(
        [0x293C], [0x238CA7C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY27_RESERVED_SPACE = Symbol(
        [0x2D30], [0x238CE70], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY27_UNKNOWN_POINTER__NA_238CE80 = Symbol(
        [0x2D40], [0x238CE80], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY27_UNKNOWN_POINTER__NA_238CE84 = Symbol(
        [0x2D44], [0x238CE84], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )


class NaOverlay27Section:
    name = "overlay27"
    description = "Controls the special episode item discard menu."
    loadaddress = 0x238A140
    length = 0x2D60
    functions = NaOverlay27Functions
    data = NaOverlay27Data


class NaOverlay28Functions:
    pass


class NaOverlay28Data:
    pass


class NaOverlay28Section:
    name = "overlay28"
    description = "Controls the staff credits sequence."
    loadaddress = 0x238A140
    length = 0xC60
    functions = NaOverlay28Functions
    data = NaOverlay28Data


class NaOverlay29Functions:
    DungeonAlloc = Symbol(
        [0x281C],
        [0x22DEA5C],
        None,
        (
            "Allocates a new dungeon struct.\n\nThis updates the master dungeon pointer"
            " and returns a copy of that pointer.\n\nreturn: pointer to a newly"
            " allocated dungeon struct"
        ),
    )

    GetDungeonPtrMaster = Symbol(
        [0x2840],
        [0x22DEA80],
        None,
        (
            "Returns the master dungeon pointer (a global, see"
            " DUNGEON_PTR_MASTER).\n\nreturn: pointer to a newly allocated dungeon"
            " struct"
        ),
    )

    DungeonZInit = Symbol(
        [0x2850],
        [0x22DEA90],
        None,
        (
            "Zero-initializes the dungeon struct pointed to by the master dungeon"
            " pointer.\n\nNo params."
        ),
    )

    DungeonFree = Symbol(
        [0x2870],
        [0x22DEAB0],
        None,
        (
            "Frees the dungeons struct pointer to by the master dungeon pointer, and"
            " nullifies the pointer.\n\nNo params."
        ),
    )

    RunDungeon = Symbol(
        [0x2CF8],
        [0x22DEF38],
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
            0x70A8,
            0x7578,
            0xD3B4,
            0x103C8,
            0x10B80,
            0x12108,
            0x13560,
            0x14350,
            0x1904C,
            0x1A068,
            0x1B124,
            0x2075C,
            0x22B58,
            0x23EA4,
            0x267F8,
            0x28578,
            0x2934C,
            0x299C4,
            0x2BCB8,
            0x2C03C,
            0x2CD7C,
            0x326B0,
            0x32DC8,
            0x34DD0,
            0x35674,
            0x38ED8,
            0x3CAF4,
            0x3CC0C,
            0x3DD4C,
            0x3EF54,
            0x40988,
            0x42B98,
            0x43330,
            0x439BC,
            0x43F3C,
            0x44524,
            0x451F8,
            0x493E0,
            0x52600,
            0x57D6C,
            0x58E98,
            0x5BA68,
            0x688B8,
            0x69458,
            0x6B964,
            0x6D63C,
            0x71B90,
            0x729D4,
        ],
        [
            0x22E0354,
            0x22E1A1C,
            0x22E32E8,
            0x22E37B8,
            0x22E95F4,
            0x22EC608,
            0x22ECDC0,
            0x22EE348,
            0x22EF7A0,
            0x22F0590,
            0x22F528C,
            0x22F62A8,
            0x22F7364,
            0x22FC99C,
            0x22FED98,
            0x23000E4,
            0x2302A38,
            0x23047B8,
            0x230558C,
            0x2305C04,
            0x2307EF8,
            0x230827C,
            0x2308FBC,
            0x230E8F0,
            0x230F008,
            0x2311010,
            0x23118B4,
            0x2315118,
            0x2318D34,
            0x2318E4C,
            0x2319F8C,
            0x231B194,
            0x231CBC8,
            0x231EDD8,
            0x231F570,
            0x231FBFC,
            0x232017C,
            0x2320764,
            0x2321438,
            0x2325620,
            0x232E840,
            0x2333FAC,
            0x23350D8,
            0x2337CA8,
            0x2344AF8,
            0x2345698,
            0x2347BA4,
            0x234987C,
            0x234DDD0,
            0x234EC14,
        ],
        None,
        (
            "Checks if an entity pointer points to a valid entity (not entity type 0,"
            " which represents no entity).\n\nr0: entity pointer\nreturn: bool"
        ),
    )

    GetFloorType = Symbol(
        [0x4170],
        [0x22E03B0],
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
        [0x22E0620],
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
        [0x22E0864],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0:"
            " fixed_room_id\nreturn: bool"
        ),
    )

    IsCurrentFixedRoomBossFight = Symbol(
        [0x4640],
        [0x22E0880],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: bool",
    )

    IsMarowakTrainingMaze = Symbol(
        [0x4660],
        [0x22E08A0],
        None,
        (
            "Check if the current dungeon is one of the training mazes in Marowak Dojo"
            " (this excludes Final Maze).\n\nreturn: bool"
        ),
    )

    FixedRoomIsSubstituteRoom = Symbol(
        [0x468C],
        [0x22E08CC],
        None,
        (
            "Checks if the current fixed room is the 'substitute room' (ID"
            " 0x6E).\n\nreturn: bool"
        ),
    )

    StoryRestrictionsEnabled = Symbol(
        [0x46E8],
        [0x22E0928],
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
        [0x22E095C],
        None,
        (
            "Likely a linker-generated veneer for GetScenarioBalance.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-"
        ),
    )

    FadeToBlack = Symbol(
        [0x4728],
        [0x22E0968],
        None,
        "Fades the screen to black across several frames.\n\nNo params.",
    )

    GetTileAtEntity = Symbol(
        [0x53E8],
        [0x22E1628],
        None,
        (
            "Returns a pointer to the tile where an entity is located.\n\nr0: pointer"
            " to entity\nreturns: pointer to tile"
        ),
    )

    SpawnTrap = Symbol(
        [0x6020],
        [0x22E2260],
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
        [0x22E2314],
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
        [0x22E274C],
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
        [0x22E2810],
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
        [0x22E2954],
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
        [0x22E2A38],
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
        [0x22E2AD8],
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
        [0x6B98],
        [0x22E2DD8],
        None,
        (
            "Sets the Map Surveyor flag in the dungeon struct to true if a team member"
            " has Map Surveyor, sets it to false otherwise.\n\nThis function has two"
            " variants: in the EU ROM, it will return true if the flag was changed. The"
            " NA version will return the new value of the flag instead.\n\nreturn: bool"
        ),
    )

    PointCameraToMonster = Symbol(
        [0x6C14],
        [0x22E2E54],
        None,
        "Points the camera to the specified monster.\n\nr0: Entity pointer\nr1: ?",
    )

    UpdateCamera = Symbol(
        [0x6C84],
        [0x22E2EC4],
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
            0x70CC,
            0x120D8,
            0x19754,
            0x23658,
            0x2648C,
            0x2BCDC,
            0x2E79C,
            0x32338,
            0x335D0,
            0x34DF4,
            0x359B8,
            0x38EFC,
            0x6B910,
        ],
        [
            0x22E330C,
            0x22EE318,
            0x22F5994,
            0x22FF898,
            0x23026CC,
            0x2307F1C,
            0x230A9DC,
            0x230E578,
            0x230F810,
            0x2311034,
            0x2311BF8,
            0x231513C,
            0x2347B50,
        ],
        None,
        (
            "Checks if a monster is holding a certain item that isn't disabled by"
            " Klutz.\n\nr0: entity pointer\nr1: item ID\nreturn: bool"
        ),
    )

    GetVisibilityRange = Symbol(
        [0x70FC],
        [0x22E333C],
        None,
        (
            "Returns dungeon::display_data::visibility_range. If the visibility range"
            " is 0, returns 2 instead.\n\nreturn: Visibility range of the current"
            " floor, or 2 if the visibility is 0."
        ),
    )

    UpdateStatusIconFlags = Symbol(
        [0x7874],
        [0x22E3AB4],
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
        [0x8724],
        [0x22E4964],
        None,
        (
            "Displays the graphical effect on a monster that just recovered PP.\n\nr0:"
            " entity pointer"
        ),
    )

    LoadMappaFileAttributes = Symbol(
        [0xAD7C],
        [0x22E6FBC],
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
        [0xBB0C],
        [0x22E7D4C],
        None,
        (
            "Returns true if the specified monster is included in the floor's monster"
            " spawn list (the modified list after a maximum of 14 different species"
            " were chosen, not the raw list read from the mappa file).\n\nr0: Monster"
            " ID\nreturn: bool"
        ),
    )

    GetMonsterIdToSpawn = Symbol(
        [0xBB60],
        [0x22E7DA0],
        None,
        (
            "Get the id of the monster to be randomly spawned.\n\nr0: the spawn weight"
            " to use (0 for normal, 1 for monster house)\nreturn: monster ID"
        ),
    )

    GetMonsterLevelToSpawn = Symbol(
        [0xBC18],
        [0x22E7E58],
        None,
        (
            "Get the level of the monster to be spawned, given its id.\n\nr0: monster"
            " ID\nreturn: Level of the monster to be spawned, or 1 if the specified ID"
            " can't be found on the floor's spawn table."
        ),
    )

    GetDirectionTowardsPosition = Symbol(
        [0xCDE0],
        [0x22E9020],
        None,
        (
            "Gets the direction in which a monster should move to go from the origin"
            " position to the target position\n\nr0: Origin position\nr1: Target"
            " position\nreturn: Direction in which to move to reach the target position"
            " from the origin position"
        ),
    )

    GetChebyshevDistance = Symbol(
        [0xCE4C],
        [0x22E908C],
        None,
        (
            "Returns the Chebyshev distance between two positions. Calculated as"
            " max(abs(x0-x1), abs(y0-y1)).\n\nr0: Position A\nr1: Position B\nreturn:"
            " Chebyshev Distance between position A and position B"
        ),
    )

    IsPositionActuallyInSight = Symbol(
        [0xCE8C],
        [0x22E90CC],
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
        [0xCF64],
        [0x22E91A4],
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
        [0xD340],
        [0x22E9580],
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
        [0xD3D8],
        [0x22E9618],
        None,
        "Returns a pointer to the monster data of the current leader.\n\nNo params.",
    )

    TickStatusTurnCounter = Symbol(
        [0xD804],
        [0x22E9A44],
        None,
        (
            "Ticks down a turn counter for a status condition. If the counter equals"
            " 0x7F, it will not be decreased.\n\nr0: pointer to the status turn"
            " counter\nreturn: new counter value"
        ),
    )

    AdvanceFrame = Symbol(
        [0xDDA0],
        [0x22E9FE0],
        None,
        (
            "Advances one frame. Does not return until the next frame starts.\n\nr0: ?"
            " - Unused by the function"
        ),
    )

    GenerateDungeonRngSeed = Symbol(
        [0xE740],
        [0x22EA980],
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
        [0xE78C],
        [0x22EA9CC],
        None,
        (
            "Gets the current preseed stored in the global dungeon PRNG state. See"
            " GenerateDungeonRngSeed for more information.\n\nreturn: current dungeon"
            " RNG preseed"
        ),
    )

    SetDungeonRngPreseed = Symbol(
        [0xE79C],
        [0x22EA9DC],
        None,
        (
            "Sets the preseed in the global dungeon PRNG state. See"
            " GenerateDungeonRngSeed for more information.\n\nr0: preseed"
        ),
    )

    InitDungeonRng = Symbol(
        [0xE7AC],
        [0x22EA9EC],
        None,
        (
            "Initialize (or reinitialize) the dungeon PRNG with a given seed. The"
            " primary LCG and the five secondary LCGs are initialized jointly, and with"
            " the same seed.\n\nr0: seed"
        ),
    )

    DungeonRand16Bit = Symbol(
        [0xE7E0],
        [0x22EAA20],
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
        [0xE858],
        [0x22EAA98],
        None,
        (
            "Compute a pseudorandom integer under a given maximum value using the"
            " dungeon PRNG.\n\nr0: high\nreturn: pseudorandom integer on the interval"
            " [0, high - 1]"
        ),
    )

    DungeonRandRange = Symbol(
        [0xE880],
        [0x22EAAC0],
        None,
        (
            "Compute a pseudorandom value between two integers using the dungeon"
            " PRNG.\n\nr0: x\nr1: y\nreturn: pseudorandom integer on the interval"
            " [min(x, y), max(x, y) - 1]"
        ),
    )

    DungeonRandOutcome = Symbol(
        [0xE8E0, 0xE910],
        [0x22EAB20, 0x22EAB50],
        None,
        (
            "Returns the result of a possibly biased coin flip (a Bernoulli random"
            " variable) with some success probability p, using the dungeon PRNG.\n\nr0:"
            " success percentage (100*p)\nreturn: true with probability p, false with"
            " probability (1-p)"
        ),
    )

    CalcStatusDuration = Symbol(
        [0xE940],
        [0x22EAB80],
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
        [0xE9F4],
        [0x22EAC34],
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
        [0xEA0C],
        [0x22EAC4C],
        None,
        (
            "Sets the dungeon PRNG to use one of the 5 secondary LCGs for subsequent"
            " random number generation.\n\nr0: secondary LCG index"
        ),
    )

    DungeonRngSetPrimary = Symbol(
        [0xEA24],
        [0x22EAC64],
        None,
        (
            "Sets the dungeon PRNG to use the primary LCG for subsequent random number"
            " generation.\n\nNo params."
        ),
    )

    ChangeDungeonMusic = Symbol(
        [0xEBD4],
        [0x22EAE14],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: music ID",
    )

    TrySwitchPlace = Symbol(
        [0xEF38],
        [0x22EB178],
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
        [0xF1B4],
        [0x22EB3F4],
        None,
        (
            "Clears the fields related to AI in the monster's data struct, setting them"
            " all to 0.\nSpecifically, monster::action::action_id,"
            " monster::action::action_use_idx and monster::action::field_0xA are"
            " cleared.\n\nr0: Pointer to the monster's action field"
        ),
    )

    SetMonsterActionFields = Symbol(
        [0xF1C8],
        [0x22EB408],
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
        [0xF1DC],
        [0x22EB41C],
        None,
        (
            "Sets a monster's action to action::ACTION_PASS_TURN or"
            " action::ACTION_WALK, depending on the result of GetCanMoveFlag for the"
            " monster's ID.\n\nr0: Pointer to the monster's action field\nr1:"
            " Monster ID"
        ),
    )

    GetItemAction = Symbol(
        [0xF398],
        [0x22EB5D8],
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
        [0xF5DC],
        [0x22EB81C],
        None,
        (
            "Adds an option to the list of actions that can be taken on a pokémon, item"
            " or move to the currently active sub-menu on dungeon mode (team, moves,"
            " items, etc.).\n\nr0: Action ID\nr1: True if the option should be enabled,"
            " false otherwise"
        ),
    )

    DisableDungeonSubMenuOption = Symbol(
        [0xF6B4],
        [0x22EB8F4],
        None,
        (
            "Disables an option that was addeed to a dungeon sub-menu.\n\nr0: Action ID"
            " of the option that should be disabled"
        ),
    )

    SetActionRegularAttack = Symbol(
        [0xFA10],
        [0x22EBC50],
        None,
        (
            "Sets a monster's action to action::ACTION_REGULAR_ATTACK, with a specified"
            " direction.\n\nr0: Pointer to the monster's action field\nr1: Direction in"
            " which to use the move. Gets stored in monster::action::direction."
        ),
    )

    SetActionUseMoveAi = Symbol(
        [0xFA7C],
        [0x22EBCBC],
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
        [0xFAC8],
        [0x22EBD08],
        None,
        (
            "The main function which executes the actions that take place in a"
            " fractional turn. Called in a loop by RunDungeon while IsFloorOver returns"
            " false.\n\nr0: first loop flag (true when the function is first called"
            " during a floor)"
        ),
    )

    RunLeaderTurn = Symbol(
        [0x100C8],
        [0x22EC308],
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
        [0x1049C],
        [0x22EC6DC],
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
        [0x105A8],
        [0x22EC7E8],
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
        [0x10908],
        [0x22ECB48],
        None,
        (
            "Decrements dungeon::wind_turns and displays a wind warning message if"
            " required.\n\nNo params."
        ),
    )

    SetForcedLossReason = Symbol(
        [0x10DC8],
        [0x22ED008],
        None,
        (
            "Sets dungeon::forced_loss_reason to the specified value\n\nr0: Forced loss"
            " reason"
        ),
    )

    GetForcedLossReason = Symbol(
        [0x10DDC],
        [0x22ED01C],
        None,
        "Returns dungeon::forced_loss_reason\n\nreturn: forced_loss_reason",
    )

    BindTrapToTile = Symbol(
        [0x11618],
        [0x22ED858],
        None,
        (
            "Sets the given tile's associated object to be the given trap, and sets the"
            " visibility of the trap.\n\nr0: tile pointer\nr1: entity pointer\nr2:"
            " visibility flag"
        ),
    )

    SpawnEnemyTrapAtPos = Symbol(
        [0x11730],
        [0x22ED970],
        None,
        (
            "A convenience wrapper around SpawnTrap and BindTrapToTile. Always passes 0"
            " for the team parameter (making it an enemy trap).\n\nr0: trap ID\nr1: x"
            " position\nr2: y position\nr3: flags\nstack[0]: visibility flag"
        ),
    )

    DebugRecruitingEnabled = Symbol(
        [0x1382C],
        [0x22EFA6C],
        None,
        (
            "Always returns true. Called by SpecificRecruitCheck.\n\nSeems to be a"
            " function used during development to disable recruiting. If it returns"
            " false, SpecificRecruitCheck will also return false.\n\nreturn: true"
        ),
    )

    GetLeaderAction = Symbol(
        [0x1494C],
        [0x22F0B8C],
        None,
        (
            "Returns a pointer to the action data of the current leader (field 0x4A on"
            " its monster struct).\n\nNo params."
        ),
    )

    SetLeaderAction = Symbol(
        [0x14C9C],
        [0x22F0EDC],
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
        [0x176F4],
        [0x22F3934],
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
        [0x1ABD8],
        [0x22F6E18],
        None,
        (
            "Zeroes the damage data struct, which is output by the damage calculation"
            " function.\n\nr0: damage data pointer"
        ),
    )

    DungeonGetTotalSpriteFileSize = Symbol(
        [0x1AE28],
        [0x22F7068],
        None,
        (
            "Checks Castform and Cherrim\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: monster ID\nreturn: sprite file size"
        ),
    )

    DungeonGetSpriteIndex = Symbol(
        [0x1B148],
        [0x22F7388],
        None,
        (
            "Gets the sprite index of the specified monster on this floor\n\nr0:"
            " Monster ID\nreturn: Sprite index of the specified monster ID"
        ),
    )

    JoinedAtRangeCheck2Veneer = Symbol(
        [0x1B168],
        [0x22F73A8],
        None,
        (
            "Likely a linker-generated veneer for arm9::JoinedAtRangeCheck2.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nNo"
            " params."
        ),
    )

    FloorNumberIsEven = Symbol(
        [0x1B174],
        [0x22F73B4],
        None,
        (
            "Checks if the current dungeon floor number is even (probably to determine"
            " whether an enemy spawn should be female).\n\nHas a special check to"
            " return false for Labyrinth Cave B10F (the Gabite boss fight).\n\nreturn:"
            " bool"
        ),
    )

    GetKecleonIdToSpawnByFloor = Symbol(
        [0x1B1AC],
        [0x22F73EC],
        None,
        (
            "If the current floor number is even, returns female Kecleon's id (0x3D7),"
            " otherwise returns male Kecleon's id (0x17F).\n\nreturn: monster ID"
        ),
    )

    StoreSpriteFileIndexBothGenders = Symbol(
        [0x1B1CC],
        [0x22F740C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nr1: file ID",
    )

    LoadMonsterSpriteInner = Symbol(
        [0x1B294],
        [0x22F74D4],
        None,
        "This is called by LoadMonsterSprite a bunch of times.\n\nr0: monster ID",
    )

    SwapMonsterWanFileIndex = Symbol(
        [0x1B394],
        [0x22F75D4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: src_id\nr1: dst_id",
    )

    LoadMonsterSprite = Symbol(
        [0x1B414],
        [0x22F7654],
        None,
        (
            "Loads the sprite of the specified monster to use it in a"
            " dungeon.\n\nIrdkwia's notes: Handles Castform/Cherrim/Deoxys\n\nr0:"
            " monster ID\nr1: ?"
        ),
    )

    DeleteMonsterSpriteFile = Symbol(
        [0x1B528],
        [0x22F7768],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID",
    )

    DeleteAllMonsterSpriteFiles = Symbol(
        [0x1B5C4],
        [0x22F7804],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    EuFaintCheck = Symbol(
        None,
        None,
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
        [0x1BCF0],
        [0x22F7F30],
        None,
        (
            "Handles a fainted pokémon (reviving does not count as fainting).\n\nr0:"
            " Fainted entity\nr1: Damage source (move ID or greater than the max move"
            " id for other causes)\nr2: Entity responsible of the fainting"
        ),
    )

    UpdateAiTargetPos = Symbol(
        [0x1CF04],
        [0x22F9144],
        None,
        (
            "Given a monster, updates its target_pos field based on its current"
            " position and the direction in which it plans to attack.\n\nr0: Entity"
            " pointer"
        ),
    )

    SetMonsterTypeAndAbility = Symbol(
        [0x1CF54],
        [0x22F9194],
        None,
        (
            "Checks Forecast ability\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: target entity pointer"
        ),
    )

    TryActivateSlowStart = Symbol(
        [0x1CFFC],
        [0x22F923C],
        None,
        (
            "Runs a check over all monsters on the field for the ability Slow Start,"
            " and lowers the speed of those who have it.\n\nNo params"
        ),
    )

    TryActivateArtificialWeatherAbilities = Symbol(
        [0x1D098],
        [0x22F92D8],
        None,
        (
            "Runs a check over all monsters on the field for abilities that affect the"
            " weather and changes the floor's weather accordingly.\n\nNo params"
        ),
    )

    GetMonsterApparentId = Symbol(
        [0x1D1C8],
        [0x22F9408],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: target entity"
            " pointer\nr1: current_id\nreturn: ?"
        ),
    )

    DefenderAbilityIsActive = Symbol(
        [0x1D48C, 0x257CC, 0x2E700, 0x35954, 0x46B24, 0x567CC],
        [0x22F96CC, 0x2301A0C, 0x230A940, 0x2311B94, 0x2322D64, 0x2332A0C],
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
            0x1D4E0,
            0x25820,
            0x2E754,
            0x33740,
            0x3C870,
            0x3E794,
            0x3F0D8,
            0x46B78,
            0x71220,
        ],
        [
            0x22F9720,
            0x2301A60,
            0x230A994,
            0x230F980,
            0x2318AB0,
            0x231A9D4,
            0x231B318,
            0x2322DB8,
            0x234D460,
        ],
        None,
        (
            "Checks if an entity is a monster (entity type 1).\n\nr0: entity"
            " pointer\nreturn: bool"
        ),
    )

    TryActivateTruant = Symbol(
        [0x1D5B0],
        [0x22F97F0],
        None,
        (
            "Checks if an entity has the ability Truant, and if so tries to apply the"
            " pause status to it.\n\nr0: pointer to entity"
        ),
    )

    TryPointCameraToMonster = Symbol(
        [0x1D674],
        [0x22F98B4],
        None,
        (
            "Attempts to place the camera on top of the specified monster.\n\nIf the"
            " camera is already on top of the specified entity, the function does"
            " nothing.\n\nr0: Entity pointer. Must be a monster, otherwise the function"
            " does nothing.\nr1: ?\nr2: ?"
        ),
    )

    RestorePpAllMovesSetFlags = Symbol(
        [0x1D834],
        [0x22F9A74],
        None,
        (
            "Restores PP for all moves, clears flags move::f_consume_2_pp,"
            " move::flags2_unk5 and move::flags2_unk7, and sets flag"
            " move::f_consume_pp.\nCalled when a monster is revived.\n\nr0: pointer to"
            " entity whose moves will be restored"
        ),
    )

    ShouldMonsterHeadToStairs = Symbol(
        [0x1E1F0],
        [0x22FA430],
        None,
        (
            "Checks if a given monster should try to reach the stairs when controlled"
            " by the AI\n\nr0: Entity pointer\nreturn: True if the monster should try"
            " to reach the stairs, false otherwise"
        ),
    )

    MewSpawnCheck = Symbol(
        [0x1E3B0],
        [0x22FA5F0],
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
            0x1EA58,
            0x23CE8,
            0x2E778,
            0x3366C,
            0x34E24,
            0x385AC,
            0x3D568,
            0x3E63C,
            0x476D8,
            0x567A8,
            0x6B940,
            0x6C070,
        ],
        [
            0x22FAC98,
            0x22FFF28,
            0x230A9B8,
            0x230F8AC,
            0x2311064,
            0x23147EC,
            0x23197A8,
            0x231A87C,
            0x2323918,
            0x23329E8,
            0x2347B80,
            0x23482B0,
        ],
        None,
        (
            "Checks if a monster is a team member under the effects of a certain"
            " exclusive item effect.\n\nr0: entity pointer\nr1: exclusive item effect"
            " ID\nreturn: bool"
        ),
    )

    GetTeamMemberWithIqSkill = Symbol(
        [0x1EDB8],
        [0x22FAFF8],
        None,
        (
            "Returns an entity pointer to the first team member which has the specified"
            " iq skill.\n\nr0: iq skill id\nreturn: pointer to entity"
        ),
    )

    TeamMemberHasEnabledIqSkill = Symbol(
        [0x1EE24],
        [0x22FB064],
        None,
        (
            "Returns true if any team member has the specified iq skill.\n\nr0: iq"
            " skill id\nreturn: bool"
        ),
    )

    TeamLeaderIqSkillIsEnabled = Symbol(
        [0x1EE40],
        [0x22FB080],
        None,
        (
            "Returns true the leader has the specified iq skill.\n\nr0: iq skill"
            " id\nreturn: bool"
        ),
    )

    HasSuperEffectiveMoveAgainstUser = Symbol(
        [0x1EECC],
        [0x22FB10C],
        None,
        (
            "Checks if the target has at least one super effective move against the"
            " user.\n\nr0: User\nr1: Target\nr2: If true, moves with a max Ginseng"
            " boost != 99 will be ignored\nreturn: True if the target has at least one"
            " super effective move against the user, false otherwise."
        ),
    )

    CheckSpawnThreshold = Symbol(
        [0x1F3AC],
        [0x22FB5EC],
        None,
        (
            "Checks if a given monster ID can spawn in dungeons.\n\nThe function"
            " returns true if the monster's spawn threshold value is <="
            " SCENARIO_BALANCE_FLAG\n\nr0: monster ID\nreturn: True if the monster can"
            " spawn, false otherwise"
        ),
    )

    HasLowHealth = Symbol(
        [0x1F3D0],
        [0x22FB610],
        None,
        (
            "Checks if the entity passed is a valid monster, and if it's at low health"
            " (below 25% rounded down)\n\nr0: entity pointer\nreturn: bool"
        ),
    )

    AreEntitiesAdjacent = Symbol(
        [0x1F438],
        [0x22FB678],
        None,
        (
            "Checks whether two entities are adjacent or not.\n\nThe function checks"
            " all 8 possible directions.\n\nr0: First entity\nr1: Second"
            " entity\nreturn: True if both entities are adjacent, false otherwise."
        ),
    )

    IsSpecialStoryAlly = Symbol(
        [0x1F890],
        [0x22FBAD0],
        None,
        (
            "Checks if a monster is a special story ally.\n\nThis is a hard-coded check"
            " that looks at the monster's 'Joined At' field. If the value is in the"
            " range [DUNGEON_JOINED_AT_BIDOOF, DUNGEON_DUMMY_0xE3], this check will"
            " return true.\n\nr0: monster pointer\nreturn: bool"
        ),
    )

    IsExperienceLocked = Symbol(
        [0x1F8B0],
        [0x22FBAF0],
        None,
        (
            "Checks if a monster does not gain experience.\n\nThis basically just"
            " inverts IsSpecialStoryAlly, with the exception of also checking for the"
            " 'Joined At' field being DUNGEON_CLIENT (is this set for mission"
            " clients?).\n\nr0: monster pointer\nreturn: bool"
        ),
    )

    InitTeam = Symbol(
        [0x202CC],
        [0x22FC50C],
        None,
        "Seems to initialize the team when entering a dungeon.\n\nr0: ?",
    )

    SpawnMonster = Symbol(
        [0x20E44],
        [0x22FD084],
        None,
        (
            "Spawns the given monster on a tile.\n\nr0: pointer to struct"
            " spawned_monster_data\nr1: if true, the monster cannot spawn asleep,"
            " otherwise it will randomly be asleep\nreturn: pointer to entity"
        ),
    )

    InitTeamMember = Symbol(
        [0x21174],
        [0x22FD3B4],
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
        [0x21B80],
        [0x22FDDC0],
        None,
        (
            "Initializes a monster struct.\n\nr0: pointer to monster to initialize\nr1:"
            " some flag"
        ),
    )

    ExecuteMonsterAction = Symbol(
        [0x2227C],
        [0x22FE4BC],
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
        [0x22F88],
        [0x22FF1C8],
        None,
        (
            "Returns true if the monster has any status problem that prevents it from"
            " acting\n\nr0: Entity pointer\nreturn: True if the specified monster can't"
            " act because of a status problem, false otherwise."
        ),
    )

    CalcSpeedStage = Symbol(
        [0x23BB4],
        [0x22FFDF4],
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
        [0x23D0C],
        [0x22FFF4C],
        None,
        (
            "Calls CalcSpeedStage with a speed counter weight of 1.\n\nr0: pointer to"
            " entity\nreturn: speed stage"
        ),
    )

    GetNumberOfAttacks = Symbol(
        [0x23D1C],
        [0x22FFF5C],
        None,
        (
            "Returns the number of attacks that a monster can do in one turn (1 or"
            " 2).\n\nChecks for the abilities Swift Swim, Chlorophyll, Unburden, and"
            " for exclusive items.\n\nr0: pointer to entity\nreturns: int"
        ),
    )

    GetMonsterName = Symbol(
        [0x23F24],
        [0x2300164],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nr1: TargetInfo",
    )

    SprintfStatic = Symbol(
        [0x24088],
        [0x23002C8],
        None,
        (
            "Statically defined copy of sprintf(3) in overlay 29. See arm9.yml for more"
            " information.\n\nr0: str\nr1: format\n...: variadic\nreturn: number of"
            " characters printed, excluding the null-terminator"
        ),
    )

    IsMonsterCornered = Symbol(
        [0x24ED8],
        [0x2301118],
        None,
        (
            "True if the given monster is cornered (it can't move in any"
            " direction)\n\nr0: Entity pointer\nreturn: True if the monster can't move"
            " in any direction, false otherwise."
        ),
    )

    CanAttackInDirection = Symbol(
        [0x24FF4],
        [0x2301234],
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
        [0x250B8],
        [0x23012F8],
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
        [0x25378],
        [0x23015B8],
        None,
        (
            "Checks if a monster should run away from other monsters\n\nr0: Entity"
            " pointer\nreturn: True if the monster should run away, false otherwise"
        ),
    )

    ShouldMonsterRunAwayVariation = Symbol(
        [0x25468],
        [0x23016A8],
        None,
        (
            "Calls ShouldMonsterRunAway and returns its result. It also calls another"
            " function if the result was true.\n\nr0: Entity pointer\nr1: ?\nreturn:"
            " Result of the call to ShouldMonsterRunAway"
        ),
    )

    NoGastroAcidStatus = Symbol(
        [0x25A9C],
        [0x2301CDC],
        None,
        (
            "Checks if a monster does not have the Gastro Acid status.\n\nr0: entity"
            " pointer\nreturn: bool"
        ),
    )

    AbilityIsActive = Symbol(
        [0x25AD0],
        [0x2301D10],
        None,
        (
            "Checks if a monster has a certain ability that isn't disabled by Gastro"
            " Acid.\n\nr0: entity pointer\nr1: ability ID\nreturn: bool"
        ),
    )

    AbilityIsActiveVeneer = Symbol(
        [0x25B38],
        [0x2301D78],
        None,
        (
            "Likely a linker-generated veneer for AbilityIsActive.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " entity pointer\nr1: ability ID\nreturn: bool"
        ),
    )

    AbilityIsActiveAnyEntity = Symbol(
        [0x25B44],
        [0x2301D84],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: user entity"
            " pointer\nr1: ability ID\nreturn: bool"
        ),
    )

    LevitateIsActive = Symbol(
        [0x25BD8],
        [0x2301E18],
        None,
        (
            "Checks if a monster is levitating (has the effect of Levitate and Gravity"
            " is not active).\n\nr0: pointer to entity\nreturn: bool"
        ),
    )

    MonsterIsType = Symbol(
        [0x25C10],
        [0x2301E50],
        None,
        (
            "Checks if a monster is a given type.\n\nr0: entity pointer\nr1: type"
            " ID\nreturn: bool"
        ),
    )

    IsTypeAffectedByGravity = Symbol(
        [0x25C48],
        [0x2301E88],
        None,
        (
            "Checks if Gravity is active and that the given type is affected (i.e.,"
            " Flying type).\n\nr0: target entity pointer (unused)\nr1: type ID\nreturn:"
            " bool"
        ),
    )

    HasTypeAffectedByGravity = Symbol(
        [0x25C6C],
        [0x2301EAC],
        None,
        (
            "Checks if Gravity is active and that the given monster is of an affected"
            " type (i.e., Flying type).\n\nr0: target entity pointer\nr1: type"
            " ID\nreturn: bool"
        ),
    )

    CanSeeInvisibleMonsters = Symbol(
        [0x25CAC],
        [0x2301EEC],
        None,
        (
            "Returns whether a certain monster can see other invisible monsters.\nTo be"
            " precise, this function returns true if the monster is holding Goggle"
            " Specs or if it has the status status::STATUS_EYEDROPS.\n\nr0: Entity"
            " pointer\nreturn: True if the monster can see invisible monsters."
        ),
    )

    HasDropeyeStatus = Symbol(
        [0x25D10],
        [0x2301F50],
        None,
        (
            "Returns whether a certain monster is under the effect of"
            " status::STATUS_DROPEYE.\n\nr0: Entity pointer\nreturn: True if the"
            " monster has dropeye status."
        ),
    )

    IqSkillIsEnabled = Symbol(
        [0x25D40],
        [0x2301F80],
        None,
        (
            "Checks if a monster has a certain IQ skill enabled.\n\nr0: entity"
            " pointer\nr1: IQ skill ID\nreturn: bool"
        ),
    )

    UpdateIqSkills = Symbol(
        [0x25D7C],
        [0x2301FBC],
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
        [0x2603C],
        [0x230227C],
        None,
        (
            "Check the type of a move when used by a certain monster. Accounts for"
            " special cases such as Hidden Power, Weather Ball, the regular"
            " attack...\n\nr0: Entity pointer\nr1: Pointer to move data\nreturn: Type"
            " of the move"
        ),
    )

    GetMovePower = Symbol(
        [0x260DC],
        [0x230231C],
        None,
        (
            "Gets the power of a move, factoring in Ginseng/Space Globe boosts.\n\nr0:"
            " user pointer\nr1: move pointer\nreturn: move power"
        ),
    )

    AddExpSpecial = Symbol(
        [0x262FC],
        [0x230253C],
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
        [0x264BC],
        [0x23026FC],
        None,
        (
            "Checks if the specified enemy should evolve because it just defeated an"
            " ally, and if so, attempts to evolve it.\n\nr0: Pointer to the enemy to"
            " check"
        ),
    )

    TryDecreaseLevel = Symbol(
        [0x26D48],
        [0x2302F88],
        None,
        (
            "Decrease the target monster's level if possible.\n\nr0: user entity"
            " pointer\nr1: target entity pointer\nr2: number of levels to"
            " decrease\nreturn: success flag"
        ),
    )

    LevelUp = Symbol(
        [0x26DFC],
        [0x230303C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: user entity"
            " pointer\nr1: target entity pointer\nr2: message flag?\nr3: ?\nreturn:"
            " success flag?"
        ),
    )

    EvolveMonster = Symbol(
        [0x27A3C],
        [0x2303C7C],
        None,
        (
            "Makes the specified monster evolve into the specified species.\n\nr0:"
            " Pointer to the entity to evolve\nr1: ?\nr2: Species to evolve into"
        ),
    )

    GetSleepAnimationId = Symbol(
        [0x28874],
        [0x2304AB4],
        None,
        (
            "Returns the animation id to be applied to a monster that has the sleep,"
            " napping, nightmare or bide status.\n\nReturns a different animation for"
            " sudowoodo and for monsters with infinite sleep turns (0x7F).\n\nr0:"
            " pointer to entity\nreturn: animation ID"
        ),
    )

    DisplayActions = Symbol(
        [0x28DA0],
        [0x2304FE0],
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
        [0x2A018],
        [0x2306258],
        None,
        (
            "Cures the target's freeze, shadow hold, ingrain, petrified, constriction"
            " or wrap (both as user and as target) status due to the action of the"
            " user.\n\nr0: pointer to user\nr1: pointer to target\nr2: if true, the"
            " event will be printed to the log"
        ),
    )

    EndCringeClassStatus = Symbol(
        [0x2A194],
        [0x23063D4],
        None,
        (
            "Cures the target's cringe, confusion, cowering, pause, taunt, encore or"
            " infatuated status due to the action of the user, and prints the event to"
            " the log.\n\nr0: pointer to user\nr1: pointer to target"
        ),
    )

    RunMonsterAi = Symbol(
        [0x2C100],
        [0x2308340],
        None,
        (
            "Runs the AI for a single monster to determine whether the monster can act"
            " and which action it should perform if so\n\nr0: Pointer to monster\nr1: ?"
        ),
    )

    ApplyDamage = Symbol(
        [0x2CDA0],
        [0x2308FE0],
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
        [0x2E7CC],
        [0x230AA0C],
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
        [0x2E84C],
        [0x230AA8C],
        None,
        (
            "Gets the type matchup for a given combat interaction, accounting for both"
            " of the user's types.\n\nCalls GetTypeMatchup twice and combines the"
            " result.\n\nr0: attacker pointer\nr1: defender pointer\nr2: attack"
            " type\nreturn: enum type_matchup"
        ),
    )

    GetTypeMatchup = Symbol(
        [0x2EA18],
        [0x230AC58],
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
        [0x2F96C],
        [0x230BBAC],
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
        [0x30F4C],
        [0x230D18C],
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
        [0x31000],
        [0x230D240],
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
        [0x31168],
        [0x230D3A8],
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
        [0x311B4],
        [0x230D3F4],
        None,
        (
            "A wrapper around CalcDamageFixed.\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: fixed damage\nstack[0]: [output] struct containing info"
            " about the damage calculation\nstack[1]: attack type\nstack[2]: move"
            " category\nstack[3]: damage source\nstack[4]: damage message\nothers: ?"
        ),
    )

    ResetDamageCalcScratchSpace = Symbol(
        [0x312E8],
        [0x230D528],
        None,
        (
            "CalcDamage seems to use scratch space of some kind, which this function"
            " zeroes.\n\nNo params."
        ),
    )

    SpecificRecruitCheck = Symbol(
        [0x318D4],
        [0x230DB14],
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
        [0x31990],
        [0x230DBD0],
        None,
        (
            "Determines if a defeated enemy will attempt to join the team\n\nr0: user"
            " entity pointer\nr1: target entity pointer\nreturn: True if the target"
            " will attempt to join the team"
        ),
    )

    TryRecruit = Symbol(
        [0x31E24],
        [0x230E064],
        None,
        (
            "Asks the player if they would like to recruit the enemy that was just"
            " defeated and handles the recruitment if they accept.\n\nr0: user entity"
            " pointer\nr1: monster to recruit entity pointer\nreturn: True if the"
            " monster was recruited, false if it wasn't"
        ),
    )

    TrySpawnMonsterAndTickSpawnCounter = Symbol(
        [0x3247C],
        [0x230E6BC],
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
        [0x33488],
        [0x230F6C8],
        None,
        (
            "Checks if a monster is holding an aura bow that isn't disabled by"
            " Klutz.\n\nr0: entity pointer\nreturn: bool"
        ),
    )

    ExclusiveItemOffenseBoost = Symbol(
        [0x33538],
        [0x230F778],
        None,
        (
            "Gets the exclusive item boost for attack/special attack for a"
            " monster\n\nr0: entity pointer\nr1: move category index (0 for physical, 1"
            " for special)\nreturn: boost"
        ),
    )

    ExclusiveItemDefenseBoost = Symbol(
        [0x33548],
        [0x230F788],
        None,
        (
            "Gets the exclusive item boost for defense/special defense for a"
            " monster\n\nr0: entity pointer\nr1: move category index (0 for physical, 1"
            " for special)\nreturn: boost"
        ),
    )

    TeamMemberHasExclusiveItemEffectActive = Symbol(
        [0x33600],
        [0x230F840],
        None,
        (
            "Checks if any team member is under the effects of a certain exclusive item"
            " effect.\n\nr0: exclusive item effect ID\nreturn: bool"
        ),
    )

    TrySpawnEnemyItemDrop = Symbol(
        [0x33798],
        [0x230F9D8],
        None,
        (
            "Determine what item a defeated enemy should drop, if any, then (probably?)"
            " spawn that item underneath them.\n\nThis function is called at the time"
            " when an enemy is defeated from ApplyDamage.\n\nr0: attacker entity (who"
            " defeated the enemy)\nr1: defender entity (who was defeated)"
        ),
    )

    TickNoSlipCap = Symbol(
        [0x33950],
        [0x230FB90],
        None,
        (
            "Checks if the entity is a team member and holds the No-Slip Cap, and if so"
            " attempts to make one item in the bag sticky.\n\nr0: pointer to entity"
        ),
    )

    TickStatusAndHealthRegen = Symbol(
        [0x34E48],
        [0x2311088],
        None,
        (
            "Applies the natural HP regen effect by taking modifiers into account"
            " (Poison Heal, Heal Ribbon, weather-related regen). Then it ticks down"
            " counters for volatile status effects, and heals them if the counter"
            " reached zero.\n\nr0: pointer to entity"
        ),
    )

    InflictSleepStatusSingle = Symbol(
        [0x355E4],
        [0x2311824],
        None,
        (
            "This is called by TryInflictSleepStatus.\n\nr0: entity pointer\nr1: number"
            " of turns"
        ),
    )

    TryInflictSleepStatus = Symbol(
        [0x35698],
        [0x23118D8],
        None,
        (
            "Inflicts the Sleep status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2:"
            " number of turns\nr3: flag to log a message on failure"
        ),
    )

    TryInflictNightmareStatus = Symbol(
        [0x35A0C],
        [0x2311C4C],
        None,
        (
            "Inflicts the Nightmare status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2:"
            " number of turns"
        ),
    )

    TryInflictNappingStatus = Symbol(
        [0x35B20],
        [0x2311D60],
        None,
        (
            "Inflicts the Napping status condition (from Rest) on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2:"
            " number of turns"
        ),
    )

    TryInflictYawningStatus = Symbol(
        [0x35C30],
        [0x2311E70],
        None,
        (
            "Inflicts the Yawning status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2:"
            " number of turns"
        ),
    )

    TryInflictSleeplessStatus = Symbol(
        [0x35D40],
        [0x2311F80],
        None,
        (
            "Inflicts the Sleepless status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer"
        ),
    )

    TryInflictPausedStatus = Symbol(
        [0x35E2C],
        [0x231206C],
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
        [0x35F6C],
        [0x23121AC],
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
        [0x360F8],
        [0x2312338],
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
        [0x363D8],
        [0x2312618],
        None,
        (
            "Inflicts the Burn status condition on all team members if possible.\n\nNo"
            " params."
        ),
    )

    TryInflictPoisonedStatus = Symbol(
        [0x36424],
        [0x2312664],
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
        [0x366FC],
        [0x231293C],
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
        [0x369B8],
        [0x2312BF8],
        None,
        (
            "Inflicts the Frozen status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: flag"
            " to log a message on failure"
        ),
    )

    TryInflictConstrictionStatus = Symbol(
        [0x36BE0],
        [0x2312E20],
        None,
        (
            "Inflicts the Constriction status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2:"
            " animation ID\nr3: flag to log a message on failure"
        ),
    )

    TryInflictShadowHoldStatus = Symbol(
        [0x36D38],
        [0x2312F78],
        None,
        (
            "Inflicts the Shadow Hold (AKA Immobilized) status condition on a target"
            " monster if possible.\n\nr0: user entity pointer\nr1: target entity"
            " pointer\nr2: flag to log a message on failure"
        ),
    )

    TryInflictIngrainStatus = Symbol(
        [0x36EF0],
        [0x2313130],
        None,
        (
            "Inflicts the Ingrain status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer"
        ),
    )

    TryInflictWrappedStatus = Symbol(
        [0x36FB4],
        [0x23131F4],
        None,
        (
            "Inflicts the Wrapped status condition on a target monster if"
            " possible.\n\nThis also gives the user the Wrap status (Wrapped around"
            " foe).\n\nr0: user entity pointer\nr1: target entity pointer"
        ),
    )

    FreeOtherWrappedMonsters = Symbol(
        [0x371B0],
        [0x23133F0],
        None,
        (
            "Frees from the wrap status all monsters which are wrapped by/around the"
            " monster passed as parameter.\n\nr0: pointer to entity"
        ),
    )

    TryInflictPetrifiedStatus = Symbol(
        [0x3722C],
        [0x231346C],
        None,
        (
            "Inflicts the Petrified status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer"
        ),
    )

    LowerOffensiveStat = Symbol(
        [0x373BC],
        [0x23135FC],
        None,
        (
            "Lowers the specified offensive stat on the target monster.\n\nr0: user"
            " entity pointer\nr1: target entity pointer\nr2: stat index\nr3: number of"
            " stages\nstack[0]: ?\nstack[1]: ?"
        ),
    )

    LowerDefensiveStat = Symbol(
        [0x375D4],
        [0x2313814],
        None,
        (
            "Lowers the specified defensive stat on the target monster.\n\nr0: user"
            " entity pointer\nr1: target entity pointer\nr2: stat index\nr3: number of"
            " stages\nstack[0]: ?\nstack[1]: ?"
        ),
    )

    BoostOffensiveStat = Symbol(
        [0x3775C],
        [0x231399C],
        None,
        (
            "Boosts the specified offensive stat on the target monster.\n\nr0: user"
            " entity pointer\nr1: target entity pointer\nr2: stat index\nr3: number of"
            " stages"
        ),
    )

    BoostDefensiveStat = Symbol(
        [0x378C8],
        [0x2313B08],
        None,
        (
            "Boosts the specified defensive stat on the target monster.\n\nr0: user"
            " entity pointer\nr1: target entity pointer\nr2: stat index\nr3: number of"
            " stages"
        ),
    )

    ApplyOffensiveStatMultiplier = Symbol(
        [0x37B00],
        [0x2313D40],
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
        [0x37D24],
        [0x2313F64],
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
        [0x37EA4],
        [0x23140E4],
        None,
        (
            "Boosts the specified hit chance stat (accuracy or evasion) on the target"
            " monster.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: stat"
            " index"
        ),
    )

    LowerHitChanceStat = Symbol(
        [0x37FEC],
        [0x231422C],
        None,
        (
            "Lowers the specified hit chance stat (accuracy or evasion) on the target"
            " monster.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: stat"
            " index\nr3: ? (Irdkwia's notes say this is the number of stages, but I'm"
            " pretty sure that's incorrect)"
        ),
    )

    TryInflictCringeStatus = Symbol(
        [0x381A8],
        [0x23143E8],
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
        [0x38304],
        [0x2314544],
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
        [0x385D0],
        [0x2314810],
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
        [0x386FC],
        [0x231493C],
        None,
        (
            "A wrapper around BoostSpeed with the number of stages set to 1.\n\nr0:"
            " user entity pointer\nr1: target entity pointer\nr2: number of turns\nr3:"
            " flag to log a message on failure"
        ),
    )

    LowerSpeed = Symbol(
        [0x38714],
        [0x2314954],
        None,
        (
            "Lowers the speed of the target monster.\n\nr0: user entity pointer\nr1:"
            " target entity pointer\nr2: number of stages\nr3: flag to log a message on"
            " failure"
        ),
    )

    TrySealMove = Symbol(
        [0x3887C],
        [0x2314ABC],
        None,
        (
            "Seals one of the target monster's moves. The move to be sealed is randomly"
            " selected.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: flag"
            " to log a message on failure\nreturn: Whether or not a move was sealed"
        ),
    )

    BoostOrLowerSpeed = Symbol(
        [0x389EC],
        [0x2314C2C],
        None,
        (
            "Randomly boosts or lowers the speed of the target monster by one stage"
            " with equal probability.\n\nr0: user entity pointer\nr1: target entity"
            " pointer"
        ),
    )

    ResetHitChanceStat = Symbol(
        [0x38A4C],
        [0x2314C8C],
        None,
        (
            "Resets the specified hit chance stat (accuracy or evasion) back to normal"
            " on the target monster.\n\nr0: user entity pointer\nr1: target entity"
            " pointer\nr2: stat index\nr3: ?"
        ),
    )

    TryActivateQuickFeet = Symbol(
        [0x38BDC],
        [0x2314E1C],
        None,
        (
            "Activate the Quick Feet ability on the defender, if the monster has it and"
            " it's active.\n\nr0: attacker pointer\nr1: defender pointer\nreturn: bool,"
            " whether or not the ability was activated"
        ),
    )

    TryInflictConfusedStatus = Symbol(
        [0x38CF8],
        [0x2314F38],
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
        [0x38F2C],
        [0x231516C],
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
        [0x3902C],
        [0x231526C],
        None,
        (
            "Restore HP of the target monster if possible.\n\nr0: user entity"
            " pointer\nr1: target entity pointer\nr2: HP to restore\nreturn: success"
            " flag"
        ),
    )

    TryIncreaseHp = Symbol(
        [0x390A4],
        [0x23152E4],
        None,
        (
            "Restore HP and possibly boost max HP of the target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: HP"
            " to restore\nr3: max HP boost\nstack[0]: flag to log a message on"
            " failure\nreturn: Success flag"
        ),
    )

    RevealItems = Symbol(
        [0x393D0],
        [0x2315610],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: user entity"
            " pointer\nr1: target entity pointer"
        ),
    )

    RevealStairs = Symbol(
        [0x39460],
        [0x23156A0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: user entity"
            " pointer\nr1: target entity pointer"
        ),
    )

    RevealEnemies = Symbol(
        [0x3951C],
        [0x231575C],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: user entity"
            " pointer\nr1: target entity pointer"
        ),
    )

    TryInflictLeechSeedStatus = Symbol(
        [0x395AC],
        [0x23157EC],
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
        [0x39810],
        [0x2315A50],
        None,
        (
            "Inflicts the Destiny Bond status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer"
        ),
    )

    IsBlinded = Symbol(
        [0x3B5A4],
        [0x23177E4],
        None,
        (
            "Returns true if the monster has the blinded status (see"
            " statuses::blinded), or if it is not the leader and is holding Y-Ray"
            " Specs.\n\nr0: pointer to entity\nr1: flag for whether to check for the"
            " held item\nreturn: bool"
        ),
    )

    RestoreMovePP = Symbol(
        [0x3B9E0],
        [0x2317C20],
        None,
        (
            "Restores the PP of all the target's moves by the specified amount.\n\nr0:"
            " user entity pointer\nr1: target entity pointer\nr2: PP to restore\nr3:"
            " flag to suppress message logging"
        ),
    )

    SetReflectDamageCountdownTo4 = Symbol(
        [0x3C180],
        [0x23183C0],
        None,
        (
            "Sets the monster's reflect damage countdown to a global value"
            " (0x4).\n\nr0: pointer to entity"
        ),
    )

    HasConditionalGroundImmunity = Symbol(
        [0x3C80C],
        [0x2318A4C],
        None,
        (
            "Checks if a monster is currently immune to Ground-type moves for reasons"
            " other than typing and ability.\n\nThis includes checks for Gravity and"
            " Magnet Rise.\n\nr0: entity pointer\nreturn: bool"
        ),
    )

    Conversion2IsActive = Symbol(
        [0x3D5D4],
        [0x2319814],
        None,
        (
            "Checks if the monster is under the effect of Conversion 2 (its type was"
            " changed).\n\nReturns 1 if the effects is a status, 2 if it comes from an"
            " exclusive item, 0 otherwise.\n\nr0: pointer to entity\nreturn: int"
        ),
    )

    AiConsiderMove = Symbol(
        [0x3D640],
        [0x2319880],
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
        [0x3DD70],
        [0x2319FB0],
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
        [0x3DE64],
        [0x231A0A4],
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
        [0x3E454],
        [0x231A694],
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
        [0x3E560],
        [0x231A7A0],
        None,
        (
            "Checks if a monster should use PP when using a move. It also displays the"
            " corresponding animation if PP Saver triggers and prints the required"
            " messages to the message log.\n\nr0: entity pointer\nreturn: True if the"
            " monster should not use PP, false if it should."
        ),
    )

    GetEntityMoveTargetAndRange = Symbol(
        [0x3EA6C],
        [0x231ACAC],
        None,
        (
            "Gets the move target-and-range field when used by a given entity. See"
            " struct move_target_and_range in the C headers.\n\nr0: entity pointer\nr1:"
            " move pointer\nr2: AI flag (same as GetMoveTargetAndRange)\nreturn: move"
            " target and range"
        ),
    )

    IsInSpawnList = Symbol(
        [0x3F1BC],
        [0x231B3FC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: spawn_list_ptr\nr1:"
            " monster ID\nreturn: bool"
        ),
    )

    ChangeShayminForme = Symbol(
        [0x3F2AC],
        [0x231B4EC],
        None,
        (
            "forme:\n  1: change from Land to Sky\n  2: change from Sky to"
            " Land\nresult:\n  0: not Shaymin\n  1: not correct Forme\n  2: frozen\n "
            " 3: ok\n\nNote: unverified, ported from Irdkwia's notes\n\nr0: Target\nr1:"
            " forme\nreturn: result"
        ),
    )

    ApplyItemEffect = Symbol(
        [0x3F44C],
        [0x231B68C],
        None,
        (
            "Seems to apply an item's effect via a giant switch statement?\n\nr3:"
            " attacker pointer\nstack[0]: defender pointer\nstack[1]: thrown item"
            " pointer\nothers: ?"
        ),
    )

    ViolentSeedBoost = Symbol(
        [0x40BDC],
        [0x231CE1C],
        None,
        (
            "Applies the Violent Seed boost to an entity.\n\nr0: attacker pointer\nr1:"
            " defender pointer"
        ),
    )

    ApplyGummiBoostsDungeonMode = Symbol(
        [0x40E80],
        [0x231D0C0],
        None,
        (
            "Applies the IQ and possible stat boosts from eating a Gummi to the target"
            " monster.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: Gummi"
            " type ID\nr3: Stat boost amount, if a random stat boost occurs"
        ),
    )

    GetMaxPpWrapper = Symbol(
        [0x427B0],
        [0x231E9F0],
        None,
        (
            "Gets the maximum PP for a given move. A wrapper around the function in the"
            " ARM 9 binary.\n\nr0: move pointer\nreturn: max PP for the given move,"
            " capped at 99"
        ),
    )

    MoveIsNotPhysical = Symbol(
        [0x427D8],
        [0x231EA18],
        None,
        "Checks if a move isn't a physical move.\n\nr0: move ID\nreturn: bool",
    )

    TryPounce = Symbol(
        [0x439E0],
        [0x231FC20],
        None,
        (
            "Makes the target monster execute the Pounce action in a given direction if"
            " possible.\n\nIf the direction ID is 8, the target will pounce in the"
            " direction it's currently facing.\n\nr0: user entity pointer\nr1: target"
            " entity pointer\nr2: direction ID"
        ),
    )

    TryBlowAway = Symbol(
        [0x43BA0],
        [0x231FDE0],
        None,
        (
            "Blows away the target monster in a given direction if possible.\n\nr0:"
            " user entity pointer\nr1: target entity pointer\nr2: direction ID"
        ),
    )

    TryExplosion = Symbol(
        [0x44548],
        [0x2320788],
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
        [0x44AC8],
        [0x2320D08],
        None,
        (
            "Makes the target monster warp if possible.\n\nr0: user entity pointer\nr1:"
            " target entity pointer\nr2: warp type\nr3: position (if warp type is"
            " position-based)"
        ),
    )

    MoveHitCheck = Symbol(
        [0x47A08],
        [0x2323C48],
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
        [0x482F4],
        [0x2324534],
        None,
        (
            "Checks if a move is a Hyper Beam variant that requires a a turn to"
            " recharge.\n\nInclude moves: Frenzy Plant, Hydro Cannon, Hyper Beam, Blast"
            " Burn, Rock Wrecker, Giga Impact, Roar of Time\n\nr0: move\nreturn: bool"
        ),
    )

    HasMaxGinsengBoost99 = Symbol(
        [0x48558],
        [0x2324798],
        None,
        (
            "Checks if a move has a max Ginseng boost value of 99\n\nr0: Move\nreturn:"
            " True if the move's max Ginseng boost is 99, false otherwise."
        ),
    )

    DungeonRandOutcomeUserTargetInteraction = Symbol(
        [0x486F4],
        [0x2324934],
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
        [0x487E0],
        [0x2324A20],
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
        [0x48834],
        [0x2324A74],
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
        [0x488E4],
        [0x2324B24],
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
        [0x48B4C],
        [0x2324D8C],
        None,
        (
            "Updates the PP of any moves that were used by a monster, if PP should be"
            " consumed.\n\nr0: entity pointer\nr1: flag for whether or not PP should be"
            " consumed"
        ),
    )

    GetDamageSourceWrapper = Symbol(
        [0x48C04],
        [0x2324E44],
        None,
        (
            "Wraps GetDamageSource (in arm9) for a move info struct rather than a move"
            " ID.\n\nr0: move info pointer\nr1: item ID\nreturn: damage source"
        ),
    )

    LowerSshort = Symbol(
        [0x48C24],
        [0x2324E64],
        None,
        (
            "Gets the lower 2 bytes of a 4-byte number and interprets it as a signed"
            " short.\n\nr0: 4-byte number x\nreturn: (short) x"
        ),
    )

    GetMoveAnimationId = Symbol(
        [0x498D0],
        [0x2325B10],
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
        [0x49A38],
        [0x2325C78],
        None,
        (
            "Checks whether a moved used by a monster should play its alternative"
            " animation. Includes checks for Curse, Snore, Sleep Talk, Solar Beam and"
            " 2-turn moves.\n\nr0: Pointer to the entity that used the move\nr1: Move"
            " pointer\nreturn: True if the move should play its alternative animation"
        ),
    )

    ExecuteMoveEffect = Symbol(
        [0x52624],
        [0x232E864],
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
        [0x56830],
        [0x2332A70],
        None,
        (
            "Exactly the same as DoMoveDamage, except it appears DealDamage was"
            " inlined.\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether or not damage was dealt"
        ),
    )

    DealDamage = Symbol(
        [0x568E0],
        [0x2332B20],
        None,
        (
            "Deals damage from a move or item used by an attacking monster on a"
            " defending monster.\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: damage multiplier (as a binary fixed-point number with 8"
            " fraction bits)\nstack[0]: item ID\nreturn: amount of damage dealt"
        ),
    )

    CalcDamageProjectile = Symbol(
        [0x56A0C],
        [0x2332C4C],
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
        [0x56B2C],
        [0x2332D6C],
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
        [0x56E34],
        [0x2333074],
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
        [0x58AC8],
        [0x2334D08],
        None,
        (
            "Get the weather, as experienced by a specific entity.\n\nr0: entity"
            " pointer\nreturn: weather ID"
        ),
    )

    TryWeatherFormChange = Symbol(
        [0x58F30],
        [0x2335170],
        None,
        (
            "Tries to change a monster into one of its weather-related alternative"
            " forms. Applies to Castform and Cherrim, and checks for their unique"
            " abilities.\n\nr0: pointer to entity"
        ),
    )

    ActivateSportCondition = Symbol(
        [0x5920C],
        [0x233544C],
        None,
        (
            "Activates the Mud Sport or Water Sport condition on the dungeon floor for"
            " some number of turns.\n\nr0: water sport flag (false for Mud Sport, true"
            " for Water Sport)"
        ),
    )

    DigitCount = Symbol(
        [0x59430],
        [0x2335670],
        None,
        (
            "Counts the number of digits in a nonnegative integer.\n\nIf the number is"
            " negative, it is cast to a uint16_t before counting digits.\n\nr0:"
            " int\nreturn: number of digits in int"
        ),
    )

    LoadTextureUi = Symbol(
        [0x59480],
        [0x23356C0],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    DisplayNumberTextureUi = Symbol(
        [0x59640],
        [0x2335880],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: x position\nr1: y"
            " position\nr2: number\nr3: ally_mode\nreturn: xsize"
        ),
    )

    DisplayCharTextureUi = Symbol(
        [0x59748],
        [0x2335988],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: call_back_str\nr1: x"
            " position\nr2: y position\nr3: char_id\nstack[0]: ?\nreturn: ?"
        ),
    )

    DisplayUi = Symbol(
        [0x597D0],
        [0x2335A10],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    GetTile = Symbol(
        [0x59EBC],
        [0x23360FC],
        None,
        (
            "Get the tile at some position. If the coordinates are out of bounds,"
            " returns a default tile.\n\nr0: x position\nr1: y position\nreturn: tile"
            " pointer"
        ),
    )

    GetTileSafe = Symbol(
        [0x59F24],
        [0x2336164],
        None,
        (
            "Get the tile at some position. If the coordinates are out of bounds,"
            " returns a pointer to a copy of the default tile.\n\nr0: x position\nr1: y"
            " position\nreturn: tile pointer"
        ),
    )

    IsFullFloorFixedRoom = Symbol(
        [0x59F94],
        [0x23361D4],
        None,
        (
            "Checks if the current fixed room on the dungeon generation info"
            " corresponds to a fixed, full-floor layout.\n\nThe first non-full-floor"
            " fixed room is 0xA5, which is for Sealed Chambers.\n\nreturn: bool"
        ),
    )

    GetStairsRoom = Symbol(
        [0x5A1E8],
        [0x2336428],
        None,
        "Returns the index of the room that contains the stairs\n\nreturn: Room index",
    )

    GetRandomSpawnMonsterID = Symbol(
        [0x5BD58],
        [0x2337F98],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: monster ID?",
    )

    GravityIsActive = Symbol(
        [0x5C150],
        [0x2338390],
        None,
        "Checks if gravity is active on the floor.\n\nreturn: bool",
    )

    ShouldBoostKecleonShopSpawnChance = Symbol(
        [0x5C280],
        [0x23384C0],
        None,
        (
            "Gets the boost_kecleon_shop_spawn_chance field on the dungeon"
            " struct.\n\nreturn: bool"
        ),
    )

    SetShouldBoostKecleonShopSpawnChance = Symbol(
        [0x5C298],
        [0x23384D8],
        None,
        (
            "Sets the boost_kecleon_shop_spawn_chance field on the dungeon struct to"
            " the given value.\n\nr0: bool to set the flag to"
        ),
    )

    UpdateShouldBoostKecleonShopSpawnChance = Symbol(
        [0x5C2B0],
        [0x23384F0],
        None,
        (
            "Sets the boost_kecleon_shop_spawn_chance field on the dungeon struct"
            " depending on if a team member has the exclusive item effect for more"
            " kecleon shops.\n\nNo params."
        ),
    )

    IsSecretBazaar = Symbol(
        [0x5C384],
        [0x23385C4],
        None,
        "Checks if the current floor is the Secret Bazaar.\n\nreturn: bool",
    )

    ShouldBoostHiddenStairsSpawnChance = Symbol(
        [0x5C3AC],
        [0x23385EC],
        None,
        (
            "Gets the boost_hidden_stairs_spawn_chance field on the dungeon"
            " struct.\n\nreturn: bool"
        ),
    )

    SetShouldBoostHiddenStairsSpawnChance = Symbol(
        [0x5C3C4],
        [0x2338604],
        None,
        (
            "Sets the boost_hidden_stairs_spawn_chance field on the dungeon struct to"
            " the given value.\n\nr0: bool to set the flag to"
        ),
    )

    UpdateShouldBoostHiddenStairsSpawnChance = Symbol(
        [0x5C3DC],
        [0x233861C],
        None,
        (
            "Sets the boost_hidden_stairs_spawn_chance field on the dungeon struct"
            " depending on if a team member has the exclusive item effect for more"
            " hidden stairs.\n\nNo params."
        ),
    )

    IsSecretRoom = Symbol(
        [0x5C41C],
        [0x233865C],
        None,
        (
            "Checks if the current floor is the Secret Room fixed floor (from hidden"
            " stairs).\n\nreturn: bool"
        ),
    )

    IsSecretFloor = Symbol(
        [0x5C444],
        [0x2338684],
        None,
        (
            "Checks if the current floor is a secret bazaar or a secret"
            " room.\n\nreturn: bool"
        ),
    )

    GetDungeonGenInfoUnk0C = Symbol(
        [0x5C640], [0x2338880], None, "return: dungeon_generation_info::field_0xc"
    )

    GetMinimapData = Symbol(
        [0x5CED8],
        [0x2339118],
        None,
        (
            "Returns a pointer to the minimap_display_data struct in the dungeon"
            " struct.\n\nreturn: minimap_display_data*"
        ),
    )

    SetMinimapDataE447 = Symbol(
        [0x5DFD8],
        [0x233A218],
        None,
        (
            "Sets minimap_display_data::field_0xE447 to the specified value\n\nr0:"
            " Value to set the field to"
        ),
    )

    GetMinimapDataE447 = Symbol(
        None,
        None,
        None,
        (
            "Exclusive to the EU ROM. Returns"
            " minimap_display_data::field_0xE447.\n\nreturn:"
            " minimap_display_data::field_0xE447"
        ),
    )

    SetMinimapDataE448 = Symbol(
        [0x5DFF0],
        [0x233A230],
        None,
        (
            "Sets minimap_display_data::field_0xE448 to the specified value\n\nr0:"
            " Value to set the field to"
        ),
    )

    LoadFixedRoomDataVeneer = Symbol(
        [0x5E3E4],
        [0x233A624],
        None,
        (
            "Likely a linker-generated veneer for LoadFixedRoomData.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nNo"
            " params."
        ),
    )

    IsNormalFloor = Symbol(
        [0x5E414],
        [0x233A654],
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
        [0x5E498],
        [0x233A6D8],
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
        [0x5EC38],
        [0x233AE78],
        None,
        "Gets the terrain type of a tile.\n\nr0: tile pointer\nreturn: terrain ID",
    )

    DungeonRand100 = Symbol(
        [0x5EC44],
        [0x233AE84],
        None,
        (
            "Compute a pseudorandom integer on the interval [0, 100) using the dungeon"
            " PRNG.\n\nreturn: pseudorandom integer"
        ),
    )

    ClearHiddenStairs = Symbol(
        [0x5EC54],
        [0x233AE94],
        None,
        (
            "Clears the tile (terrain and spawns) on which Hidden Stairs are spawned,"
            " if applicable.\n\nNo params."
        ),
    )

    FlagHallwayJunctions = Symbol(
        [0x5ECCC],
        [0x233AF0C],
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
        [0x5EDE8],
        [0x233B028],
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
        [0x5EF50],
        [0x233B190],
        None,
        (
            "Generates a floor layout with a 4x2 grid of rooms, surrounded by an outer"
            " ring of hallways.\n\nr0: floor properties"
        ),
    )

    GenerateCrossroadsFloor = Symbol(
        [0x5F3DC],
        [0x233B61C],
        None,
        (
            "Generates a floor layout with a mesh of hallways on the interior 3x2 grid,"
            " surrounded by a boundary of rooms protruding from the interior like"
            " spikes, excluding the corner cells.\n\nr0: floor properties"
        ),
    )

    GenerateLineFloor = Symbol(
        [0x5F83C],
        [0x233BA7C],
        None,
        (
            "Generates a floor layout with 5 grid cells in a horizontal line.\n\nr0:"
            " floor properties"
        ),
    )

    GenerateCrossFloor = Symbol(
        [0x5F99C],
        [0x233BBDC],
        None,
        (
            "Generates a floor layout with 5 rooms arranged in a cross ('plus sign')"
            " formation.\n\nr0: floor properties"
        ),
    )

    GenerateBeetleFloor = Symbol(
        [0x5FB34],
        [0x233BD74],
        None,
        (
            "Generates a floor layout in a 'beetle' formation, which is created by"
            " taking a 3x3 grid of rooms, connecting the rooms within each row, and"
            " merging the central column into one big room.\n\nr0: floor properties"
        ),
    )

    MergeRoomsVertically = Symbol(
        [0x5FCF0],
        [0x233BF30],
        None,
        (
            "Merges two vertically stacked rooms into one larger room.\n\nr0: x grid"
            " coordinate of the rooms to merge\nr1: y grid coordinate of the upper"
            " room\nr2: dy, where the lower room has a y grid coordinate of y+dy\nr3:"
            " grid to update"
        ),
    )

    GenerateOuterRoomsFloor = Symbol(
        [0x5FE3C],
        [0x233C07C],
        None,
        (
            "Generates a floor layout with a ring of rooms on the grid boundary and"
            " nothing in the interior.\n\nNote that this function is bugged, and won't"
            " properly connect all the rooms together for grid_size_x < 4.\n\nr0: grid"
            " size x\nr1: grid size y\nr2: floor properties"
        ),
    )

    IsNotFullFloorFixedRoom = Symbol(
        [0x600D0],
        [0x233C310],
        None,
        (
            "Checks if a fixed room ID does not correspond to a fixed, full-floor"
            " layout.\n\nThe first non-full-floor fixed room is 0xA5, which is for"
            " Sealed Chambers.\n\nr0: fixed room ID\nreturn: bool"
        ),
    )

    GenerateFixedRoom = Symbol(
        [0x600EC],
        [0x233C32C],
        None,
        (
            "Handles fixed room generation if the floor contains a fixed room.\n\nr0:"
            " fixed room ID\nr1: floor properties\nreturn: bool"
        ),
    )

    GenerateOneRoomMonsterHouseFloor = Symbol(
        [0x60534],
        [0x233C774],
        None,
        (
            "Generates a floor layout with just a large, one-room Monster"
            " House.\n\nThis is the default layout if dungeon generation fails.\n\nNo"
            " params."
        ),
    )

    GenerateTwoRoomsWithMonsterHouseFloor = Symbol(
        [0x60604],
        [0x233C844],
        None,
        (
            "Generate a floor layout with two rooms (left and right), one of which is a"
            " Monster House.\n\nNo params."
        ),
    )

    GenerateExtraHallways = Symbol(
        [0x607A8],
        [0x233C9E8],
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
        [0x60D44],
        [0x233CF84],
        None,
        (
            "Get the grid cell positions for a given set of floor grid"
            " dimensions.\n\nr0: [output] pointer to array of the starting x"
            " coordinates of each grid column\nr1: [output] pointer to array of the"
            " starting y coordinates of each grid row\nr2: grid size x\nr3: grid size y"
        ),
    )

    InitDungeonGrid = Symbol(
        [0x60DC4],
        [0x233D004],
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
        [0x60EC4],
        [0x233D104],
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
        [0x610D8],
        [0x233D318],
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
        [0x61434],
        [0x233D674],
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
        [0x61E1C],
        [0x233E05C],
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
        [0x621FC],
        [0x233E43C],
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
        [0x62AF4],
        [0x233ED34],
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
        [0x62EE0],
        [0x233F120],
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
        [0x631E4],
        [0x233F424],
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
        [0x636C0],
        [0x233F900],
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
        [0x636FC],
        [0x233F93C],
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
        [0x639A8],
        [0x233FBE8],
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
        [0x63D5C],
        [0x233FF9C],
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
        [0x63FE4],
        [0x2340224],
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
        [0x64218],
        [0x2340458],
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
        [0x64494],
        [0x23406D4],
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
        [0x6463C],
        [0x234087C],
        None,
        "Set spawn flag 5 (0b100000 or 0x20) on all tiles in a room.\n\nr0: grid cell",
    )

    IsNextToHallway = Symbol(
        [0x64690],
        [0x23408D0],
        None,
        (
            "Checks if a tile position is either in a hallway or next to one.\n\nr0:"
            " x\nr1: y\nreturn: bool"
        ),
    )

    ResolveInvalidSpawns = Symbol(
        [0x64734],
        [0x2340974],
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
        [0x647CC],
        [0x2340A0C],
        None,
        "Converts all secondary terrain tiles (water/lava) to chasms.\n\nNo params.",
    )

    EnsureImpassableTilesAreWalls = Symbol(
        [0x64838],
        [0x2340A78],
        None,
        "Ensures all tiles with the impassable flag are walls.\n\nNo params.",
    )

    InitializeTile = Symbol(
        [0x64894], [0x2340AD4], None, "Initialize a tile struct.\n\nr0: tile pointer"
    )

    ResetFloor = Symbol(
        [0x648CC],
        [0x2340B0C],
        None,
        (
            "Resets the floor in preparation for a floor generation attempt.\n\nResets"
            " all tiles, resets the border to be impassable, and clears entity"
            " spawns.\n\nNo params."
        ),
    )

    PosIsOutOfBounds = Symbol(
        [0x64A6C],
        [0x2340CAC],
        None,
        (
            "Checks if a position (x, y) is out of bounds on the map: !((0 <= x <= 55)"
            " && (0 <= y <= 31)).\n\nr0: x\nr1: y\nreturn: bool"
        ),
    )

    ShuffleSpawnPositions = Symbol(
        [0x64AA4],
        [0x2340CE4],
        None,
        (
            "Randomly shuffle an array of spawn positions.\n\nr0: spawn position array"
            " containing bytes {x1, y1, x2, y2, ...}\nr1: number of (x, y) pairs in the"
            " spawn position array"
        ),
    )

    SpawnNonEnemies = Symbol(
        [0x64B0C],
        [0x2340D4C],
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
        [0x65230],
        [0x2341470],
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
        [0x6552C],
        [0x234176C],
        None,
        (
            "Set a specific tile to have secondary terrain (water/lava), but only if"
            " it's a passable wall.\n\nr0: tile pointer"
        ),
    )

    GenerateSecondaryTerrainFormations = Symbol(
        [0x6556C],
        [0x23417AC],
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
        [0x65C2C],
        [0x2341E6C],
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
        [0x66308], [0x2342548], None, "Converts all wall tiles to chasms.\n\nNo params."
    )

    ResetInnerBoundaryTileRows = Symbol(
        [0x6693C],
        [0x2342B7C],
        None,
        (
            "Reset the inner boundary tile rows (y == 1 and y == 30) to their initial"
            " state of all wall tiles, with impassable walls at the edges (x == 0 and x"
            " == 55).\n\nNo params."
        ),
    )

    ResetImportantSpawnPositions = Symbol(
        [0x66A28],
        [0x2342C68],
        None,
        (
            "Resets important spawn positions (the player, stairs, and hidden stairs)"
            " back to their default values.\n\nr0: dungeon generation info pointer (a"
            " field on the dungeon struct)"
        ),
    )

    SpawnStairs = Symbol(
        [0x66A4C],
        [0x2342C8C],
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
        [0x66B5C],
        [0x2342D9C],
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
        [0x66CC8],
        [0x2342F08],
        None,
        (
            "Resets hidden stairs spawn information for the floor. This includes the"
            " position on the floor generation status as well as the flag indicating"
            " whether the spawn was blocked.\n\nNo params."
        ),
    )

    LoadFixedRoomData = Symbol(
        [0x67B50],
        [0x2343D90],
        None,
        (
            "Loads fixed room data from BALANCE/fixed.bin into the buffer pointed to by"
            " FIXED_ROOM_DATA_PTR.\n\nNo params."
        ),
    )

    LoadFixedRoom = Symbol(
        [0x67BE0], [0x2343E20], None, "Note: unverified, ported from Irdkwia's notes"
    )

    OpenFixedBin = Symbol(
        [0x67E14],
        [0x2344054],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    CloseFixedBin = Symbol(
        [0x67E48],
        [0x2344088],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    AreOrbsAllowed = Symbol(
        [0x67E6C],
        [0x23440AC],
        None,
        (
            "Checks if orbs are usable in the given fixed room.\n\nAlways true if not a"
            " full-floor fixed room.\n\nr0: fixed room ID\nreturn: bool"
        ),
    )

    AreTileJumpsAllowed = Symbol(
        [0x67E9C],
        [0x23440DC],
        None,
        (
            "Checks if tile jumps (warping, being blown away, and leaping) are allowed"
            " in the given fixed room.\n\nAlways true if not a full-floor fixed"
            " room.\n\nr0: fixed room ID\nreturn: bool"
        ),
    )

    AreTrawlOrbsAllowed = Symbol(
        [0x67ECC],
        [0x234410C],
        None,
        (
            "Checks if Trawl Orbs work in the given fixed room.\n\nAlways true if not a"
            " full-floor fixed room.\n\nr0: fixed room ID\nreturn: bool"
        ),
    )

    AreOrbsAllowedVeneer = Symbol(
        [0x67EFC],
        [0x234413C],
        None,
        (
            "Likely a linker-generated veneer for InitMemAllocTable.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " fixed room ID\nreturn: bool"
        ),
    )

    AreLateGameTrapsEnabled = Symbol(
        [0x67F08],
        [0x2344148],
        None,
        (
            "Check if late-game traps (Summon, Pitfall, and Pokémon traps) work in the"
            " given fixed room.\n\nOr disabled? This function, which Irdkwia's notes"
            " label as a disable check, check the struct field labeled in End's notes"
            " as an enable flag.\n\nr0: fixed room ID\nreturn: bool"
        ),
    )

    AreMovesEnabled = Symbol(
        [0x67F20],
        [0x2344160],
        None,
        (
            "Checks if moves (excluding the regular attack) are usable in the given"
            " fixed room.\n\nr0: fixed room ID\nreturn: bool"
        ),
    )

    IsRoomIlluminated = Symbol(
        [0x67F38],
        [0x2344178],
        None,
        (
            "Checks if the given fixed room is fully illuminated.\n\nr0: fixed room"
            " ID\nreturn: bool"
        ),
    )

    GetMatchingMonsterId = Symbol(
        [0x67F50],
        [0x2344190],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nr1:"
            " ?\nr2: ?\nreturn: monster ID"
        ),
    )

    GenerateItemExplicit = Symbol(
        [0x68174],
        [0x23443B4],
        None,
        (
            "Initializes an item struct with the given information.\n\nThis calls"
            " InitStandardItem, then explicitly sets the quantity and stickiness. If"
            " quantity == 0 for Poké, GenerateCleanItem is used instead.\n\nr0: pointer"
            " to item to initialize\nr1: item ID\nr2: quantity\nr3: sticky flag"
        ),
    )

    GenerateAndSpawnItem = Symbol(
        [0x681F0],
        [0x2344430],
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
        [0x682CC],
        [0x234450C],
        None,
        (
            "Checks if the current floor is either the Secret Bazaar or a Secret"
            " Room.\n\nreturn: bool"
        ),
    )

    GenerateStandardItem = Symbol(
        [0x68990],
        [0x2344BD0],
        None,
        (
            "Wrapper around GenerateItem with quantity set to 0\n\nr0: pointer to item"
            " to initialize\nr1: item ID\nr2: stickiness type"
        ),
    )

    GenerateCleanItem = Symbol(
        [0x689A4],
        [0x2344BE4],
        None,
        (
            "Wrapper around GenerateItem with quantity set to 0 and stickiness type set"
            " to SPAWN_STICKY_NEVER.\n\nr0: pointer to item to initialize\nr1: item ID"
        ),
    )

    SpawnItem = Symbol(
        [0x692F8],
        [0x2345538],
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
        [0x697FC],
        [0x2345A3C],
        None,
        (
            "Wraps SpawnEnemyItemDrop in a more convenient interface.\n\nr0:"
            " entity\nr1: position\nr2: item\nr3: ?"
        ),
    )

    SpawnEnemyItemDrop = Symbol(
        [0x69898],
        [0x2345AD8],
        None,
        (
            "Appears to spawn an enemy item drop at a specified location, with a log"
            " message.\n\nr0: entity\nr1: item entity\nr2: item info\nr3: ?\nstack[0]:"
            " pointer to int16_t[2] for x/y direction (corresponding to"
            " DIRECTIONS_XY)\nstack[1]: ?"
        ),
    )

    TryGenerateUnownStoneDrop = Symbol(
        [0x69E20],
        [0x2346060],
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
        [0x6A5A4],
        [0x23467E4],
        None,
        (
            "Checks if a monster has a certain held item.\n\nr0: entity pointer\nr1:"
            " item ID\nreturn: bool"
        ),
    )

    GenerateMoneyQuantity = Symbol(
        [0x6A5F4],
        [0x2346834],
        None,
        (
            "Set the quantity code on an item (assuming it's Poké), given some maximum"
            " acceptable money amount.\n\nr0: item pointer\nr1: max money amount"
            " (inclusive)"
        ),
    )

    CheckTeamItemsFlags = Symbol(
        [0x6A998],
        [0x2346BD8],
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
        [0x6B084],
        [0x23472C4],
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
        [0x6CF0C],
        [0x234914C],
        None,
        (
            "Checks if there's an active challenge request on the current"
            " dungeon.\n\nreturn: True if there's an active challenge request on the"
            " current dungeon in the list of missions."
        ),
    )

    IsOutlawOrChallengeRequestFloor = Symbol(
        [0x6CF84],
        [0x23491C4],
        None,
        (
            "Checks if the current floor is an active mission destination of type"
            " MISSION_TAKE_ITEM_FROM_OUTLAW, MISSION_ARREST_OUTLAW or"
            " MISSION_CHALLENGE_REQUEST.\n\nreturn: bool"
        ),
    )

    IsDestinationFloor = Symbol(
        [0x6CFC8],
        [0x2349208],
        None,
        "Checks if the current floor is a mission destination floor.\n\nreturn: bool",
    )

    IsCurrentMissionType = Symbol(
        [0x6CFDC],
        [0x234921C],
        None,
        (
            "Checks if the current floor is an active mission destination of a given"
            " type (and any subtype).\n\nr0: mission type\nreturn: bool"
        ),
    )

    IsCurrentMissionTypeExact = Symbol(
        [0x6D010],
        [0x2349250],
        None,
        (
            "Checks if the current floor is an active mission destination of a given"
            " type and subtype.\n\nr0: mission type\nr1: mission subtype\nreturn: bool"
        ),
    )

    IsOutlawMonsterHouseFloor = Symbol(
        [0x6D04C],
        [0x234928C],
        None,
        (
            "Checks if the current floor is a mission destination for a Monster House"
            " outlaw mission.\n\nreturn: bool"
        ),
    )

    IsGoldenChamber = Symbol(
        [0x6D070],
        [0x23492B0],
        None,
        "Checks if the current floor is a Golden Chamber floor.\n\nreturn: bool",
    )

    IsLegendaryChallengeFloor = Symbol(
        [0x6D094],
        [0x23492D4],
        None,
        (
            "Checks if the current floor is a boss floor for a Legendary Challenge"
            " Letter mission.\n\nreturn: bool"
        ),
    )

    IsJirachiChallengeFloor = Symbol(
        [0x6D0D4],
        [0x2349314],
        None,
        (
            "Checks if the current floor is the boss floor in Star Cave Pit for"
            " Jirachi's Challenge Letter mission.\n\nreturn: bool"
        ),
    )

    IsDestinationFloorWithMonster = Symbol(
        [0x6D10C],
        [0x234934C],
        None,
        (
            "Checks if the current floor is a mission destination floor with a special"
            " monster.\n\nSee FloorHasMissionMonster for details.\n\nreturn: bool"
        ),
    )

    LoadMissionMonsterSprites = Symbol(
        [0x6D1B8],
        [0x23493F8],
        None,
        (
            "Loads the sprites of monsters that appear on the current floor because of"
            " a mission, if applicable.\n\nThis includes monsters to be rescued,"
            " outlaws and its minions.\n\nNo params."
        ),
    )

    MissionTargetEnemyIsDefeated = Symbol(
        [0x6D230],
        [0x2349470],
        None,
        (
            "Checks if the target enemy of the mission on the current floor has been"
            " defeated.\n\nreturn: bool"
        ),
    )

    SetMissionTargetEnemyDefeated = Symbol(
        [0x6D250],
        [0x2349490],
        None,
        (
            "Set the flag for whether or not the target enemy of the current mission"
            " has been defeated.\n\nr0: new flag value"
        ),
    )

    IsDestinationFloorWithFixedRoom = Symbol(
        [0x6D264],
        [0x23494A4],
        None,
        (
            "Checks if the current floor is a mission destination floor with a fixed"
            " room.\n\nThe entire floor can be a fixed room layout, or it can just"
            " contain a Sealed Chamber.\n\nreturn: bool"
        ),
    )

    GetItemToRetrieve = Symbol(
        [0x6D28C],
        [0x23494CC],
        None,
        (
            "Get the ID of the item that needs to be retrieve on the current floor for"
            " a mission, if one exists.\n\nreturn: item ID"
        ),
    )

    GetItemToDeliver = Symbol(
        [0x6D2B0],
        [0x23494F0],
        None,
        (
            "Get the ID of the item that needs to be delivered to a mission client on"
            " the current floor, if one exists.\n\nreturn: item ID"
        ),
    )

    GetSpecialTargetItem = Symbol(
        [0x6D2DC],
        [0x234951C],
        None,
        (
            "Get the ID of the special target item for a Sealed Chamber or Treasure"
            " Memo mission on the current floor.\n\nreturn: item ID"
        ),
    )

    IsDestinationFloorWithItem = Symbol(
        [0x6D324],
        [0x2349564],
        None,
        (
            "Checks if the current floor is a mission destination floor with a special"
            " item.\n\nThis excludes missions involving taking an item from an"
            " outlaw.\n\nreturn: bool"
        ),
    )

    IsDestinationFloorWithHiddenOutlaw = Symbol(
        [0x6D384],
        [0x23495C4],
        None,
        (
            "Checks if the current floor is a mission destination floor with a 'hidden"
            " outlaw' that behaves like a normal enemy.\n\nreturn: bool"
        ),
    )

    IsDestinationFloorWithFleeingOutlaw = Symbol(
        [0x6D3A8],
        [0x23495E8],
        None,
        (
            "Checks if the current floor is a mission destination floor with a 'fleeing"
            " outlaw' that runs away.\n\nreturn: bool"
        ),
    )

    GetMissionTargetEnemy = Symbol(
        [0x6D3E0],
        [0x2349620],
        None,
        (
            "Get the monster ID of the target enemy to be defeated on the current floor"
            " for a mission, if one exists.\n\nreturn: monster ID"
        ),
    )

    GetMissionEnemyMinionGroup = Symbol(
        [0x6D3F8],
        [0x2349638],
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
        [0x6D484],
        [0x23496C4],
        None,
        (
            "Sets dungeon::target_monster_not_found_flag to the specified value.\n\nr0:"
            " Value to set the flag to"
        ),
    )

    GetTargetMonsterNotFoundFlag = Symbol(
        [0x6D498],
        [0x23496D8],
        None,
        (
            "Gets the value of dungeon::target_monster_not_found_flag.\n\nreturn:"
            " dungeon::target_monster_not_found_flag"
        ),
    )

    FloorHasMissionMonster = Symbol(
        [0x6D508],
        [0x2349748],
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
        [0x6D660],
        [0x23498A0],
        None,
        (
            "Generates the monster ID in the egg from the given mission. Uses the base"
            " form of the monster.\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: mission struct"
        ),
    )

    LogMessageByIdWithPopupCheckUser = Symbol(
        [0x6F064],
        [0x234B2A4],
        None,
        (
            "Logs a message in the message log alongside a message popup, if the user"
            " hasn't fainted.\n\nr0: user entity pointer\nr1: message ID"
        ),
    )

    LogMessageWithPopupCheckUser = Symbol(
        [0x6F0A4],
        [0x234B2E4],
        None,
        (
            "Logs a message in the message log alongside a message popup, if the user"
            " hasn't fainted.\n\nr0: user entity pointer\nr1: message string"
        ),
    )

    LogMessageByIdQuiet = Symbol(
        [0x6F0DC],
        [0x234B31C],
        None,
        (
            "Logs a message in the message log (but without a message popup).\n\nr0:"
            " user entity pointer\nr1: message ID"
        ),
    )

    LogMessageQuiet = Symbol(
        [0x6F100],
        [0x234B340],
        None,
        (
            "Logs a message in the message log (but without a message popup).\n\nr0:"
            " user entity pointer\nr1: message string"
        ),
    )

    LogMessageByIdWithPopupCheckUserTarget = Symbol(
        [0x6F110],
        [0x234B350],
        None,
        (
            "Logs a message in the message log alongside a message popup, if some user"
            " check passes and the target hasn't fainted.\n\nr0: user entity"
            " pointer\nr1: target entity pointer\nr2: message ID"
        ),
    )

    LogMessageWithPopupCheckUserTarget = Symbol(
        [0x6F164],
        [0x234B3A4],
        None,
        (
            "Logs a message in the message log alongside a message popup, if some user"
            " check passes and the target hasn't fainted.\n\nr0: user entity"
            " pointer\nr1: target entity pointer\nr2: message string"
        ),
    )

    LogMessageByIdQuietCheckUserTarget = Symbol(
        [0x6F1B0],
        [0x234B3F0],
        None,
        (
            "Logs a message in the message log (but without a message popup), if some"
            " user check passes and the target hasn't fainted.\n\nr0: user entity"
            " pointer\nr1: target entity pointer\nr2: message ID"
        ),
    )

    LogMessageByIdWithPopupCheckUserUnknown = Symbol(
        [0x6F204],
        [0x234B444],
        None,
        (
            "Logs a message in the message log alongside a message popup, if the user"
            " hasn't fainted and some other unknown check.\n\nr0: user entity"
            " pointer\nr1: ?\nr2: message ID"
        ),
    )

    LogMessageByIdWithPopup = Symbol(
        [0x6F258],
        [0x234B498],
        None,
        (
            "Logs a message in the message log alongside a message popup.\n\nr0: user"
            " entity pointer\nr1: message ID"
        ),
    )

    LogMessageWithPopup = Symbol(
        [0x6F27C],
        [0x234B4BC],
        None,
        (
            "Logs a message in the message log alongside a message popup.\n\nr0: user"
            " entity pointer\nr1: message string"
        ),
    )

    LogMessage = Symbol(
        [0x6F2C8],
        [0x234B508],
        None,
        (
            "Logs a message in the message log.\n\nr0: user entity pointer\nr1: message"
            " string\nr2: bool, whether or not to present a message popup"
        ),
    )

    LogMessageById = Symbol(
        [0x6F4D4],
        [0x234B714],
        None,
        (
            "Logs a message in the message log.\n\nr0: user entity pointer\nr1: message"
            " ID\nr2: bool, whether or not to present a message popup"
        ),
    )

    OpenMessageLog = Symbol(
        [0x6F91C], [0x234BB5C], None, "Opens the message log window.\n\nr0: ?\nr1: ?"
    )

    RunDungeonMode = Symbol(
        [0x6FCE8],
        [0x234BF28],
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
        [0x70CB0],
        [0x234CEF0],
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
        [0x70D20],
        [0x234CF60],
        None,
        (
            "This changes the palettes of windows in both screens to an appropiate"
            " value depending on the playthrough\nIf you're in a special episode, they"
            " turn green , otherwise, they turn blue or pink depending on your"
            " character's sex\n\nNo params"
        ),
    )

    GetPersonalityIndex = Symbol(
        [0x70DAC],
        [0x234CFEC],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: monster"
            " pointer\nreturn: ?"
        ),
    )

    DisplayMessage = Symbol(
        [0x71018],
        [0x234D258],
        None,
        (
            "Displays a message in a dialogue box that optionally waits for player"
            " input before closing.\n\nr0: ?\nr1: ID of the string to display\nr2: True"
            " to wait for player input before closing the dialogue box, false to close"
            " it automatically once all the characters get printed."
        ),
    )

    DisplayMessage2 = Symbol(
        [0x7106C], [0x234D2AC], None, "Very similar to DisplayMessage"
    )

    YesNoMenu = Symbol(
        [0x712D8],
        [0x234D518],
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
        [0x71350],
        [0x234D590],
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
        [0x71BB4], [0x234DDF4], None, "Note: unverified, ported from Irdkwia's notes"
    )

    OthersMenuLoop = Symbol(
        [0x73580],
        [0x234F7C0],
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
        [0x737E4],
        [0x234FA24],
        None,
        (
            "Called when the in-dungeon 'others' menu is open. Does not return until"
            " the menu is closed.\n\nreturn: Always 0"
        ),
    )


class NaOverlay29Data:
    DUNGEON_STRUCT_SIZE = Symbol(
        [0x2838, 0x286C],
        [0x22DEA78, 0x22DEAAC],
        0x4,
        "Size of the dungeon struct (0x2CB14)",
    )

    MAX_HP_CAP = Symbol(
        [0x7B90, 0x355D4, 0x3C214],
        [0x22E3DD0, 0x2311814, 0x2318454],
        0x4,
        "The maximum amount of HP a monster can have (999).",
    )

    OFFSET_OF_DUNGEON_FLOOR_PROPERTIES = Symbol(
        [0xB7B8, 0x5EC28],
        [0x22E79F8, 0x233AE68],
        0x4,
        "Offset of the floor properties field in the dungeon struct (0x286B2)",
    )

    SPAWN_RAND_MAX = Symbol(
        [0xBC10],
        [0x22E7E50],
        0x4,
        (
            "Equal to 10,000 (0x2710). Used as parameter for DungeonRandInt to generate"
            " the random number which determines the entity to spawn."
        ),
    )

    DUNGEON_PRNG_LCG_MULTIPLIER = Symbol(
        [0xE788, 0xE84C],
        [0x22EA9C8, 0x22EAA8C],
        0x4,
        (
            "The multiplier shared by all of the dungeon PRNG's LCGs, 1566083941"
            " (0x5D588B65)."
        ),
    )

    DUNGEON_PRNG_LCG_INCREMENT_SECONDARY = Symbol(
        [0xE854],
        [0x22EAA94],
        0x4,
        (
            "The increment for the dungeon PRNG's secondary LCGs, 2531011 (0x269EC3)."
            " This happens to be the same increment that the Microsoft Visual C++"
            " runtime library uses in its implementation of the rand() function."
        ),
    )

    KECLEON_FEMALE_ID = Symbol(
        [0x1B1C4],
        [0x22F7404],
        0x4,
        "0x3D7 (983). Used when spawning Kecleon on an even numbered floor.",
    )

    KECLEON_MALE_ID = Symbol(
        [0x1B1C8],
        [0x22F7408],
        0x4,
        "0x17F (383). Used when spawning Kecleon on an odd numbered floor.",
    )

    MSG_ID_SLOW_START = Symbol(
        [0x1D090],
        [0x22F92D0],
        0x4,
        (
            "ID of the message printed when a monster has the ability Slow Start at the"
            " beginning of the floor."
        ),
    )

    EXPERIENCE_POINT_GAIN_CAP = Symbol(
        [0x26488],
        [0x23026C8],
        0x4,
        (
            "A cap on the experience that can be given to a monster in one call to"
            " AddExpSpecial"
        ),
    )

    JUDGMENT_MOVE_ID = Symbol(
        [0x30218],
        [0x230C458],
        0x4,
        "Move ID for Judgment (0x1D3)\n\ntype: enum move_id",
    )

    REGULAR_ATTACK_MOVE_ID = Symbol(
        [0x3021C],
        [0x230C45C],
        0x4,
        "Move ID for the regular attack (0x163)\n\ntype: enum move_id",
    )

    DEOXYS_ATTACK_ID = Symbol(
        [0x30220],
        [0x230C460],
        0x4,
        "Monster ID for Deoxys in Attack Forme (0x1A3)\n\ntype: enum monster_id",
    )

    DEOXYS_SPEED_ID = Symbol(
        [0x30224],
        [0x230C464],
        0x4,
        "Monster ID for Deoxys in Speed Forme (0x1A5)\n\ntype: enum monster_id",
    )

    GIRATINA_ALTERED_ID = Symbol(
        [0x30228],
        [0x230C468],
        0x4,
        "Monster ID for Giratina in Altered Forme (0x211)\n\ntype: enum monster_id",
    )

    PUNISHMENT_MOVE_ID = Symbol(
        [0x3022C],
        [0x230C46C],
        0x4,
        "Move ID for Punishment (0x1BD)\n\ntype: enum move_id",
    )

    OFFENSE_STAT_MAX = Symbol(
        [0x3025C],
        [0x230C49C],
        0x4,
        (
            "Cap on an attacker's modified offense (attack or special attack) stat"
            " after boosts. Used during damage calculation."
        ),
    )

    PROJECTILE_MOVE_ID = Symbol(
        [0x30E3C, 0x404C0],
        [0x230D07C, 0x231C700],
        0x4,
        "The move ID of the special 'projectile' move (0x195)\n\ntype: enum move_id",
    )

    BELLY_LOST_PER_TURN = Symbol(
        [0x34830],
        [0x2310A70],
        0x4,
        (
            "The base value by which belly is decreased every turn.\n\nIts raw value is"
            " 0x199A, which encodes a binary fixed-point number (16 fraction bits) with"
            " value (0x199A * 2^-16), and is the closest approximation to 0.1"
            " representable in this number format."
        ),
    )

    MONSTER_HEAL_HP_MAX = Symbol(
        [0x390A0],
        [0x23152E0],
        0x4,
        "The maximum amount of HP a monster can have (999).",
    )

    MOVE_TARGET_AND_RANGE_SPECIAL_USER_HEALING = Symbol(
        [0x3EAF4],
        [0x231AD34],
        0x4,
        (
            "The move target and range code for special healing moves that target just"
            " the user (0x273).\n\ntype: struct move_target_and_range (+ padding)"
        ),
    )

    PLAIN_SEED_VALUE = Symbol(
        [0x40508], [0x231C748], 0x4, "Some value related to the Plain Seed (0xBE9)."
    )

    MAX_ELIXIR_PP_RESTORATION = Symbol(
        [0x4050C],
        [0x231C74C],
        0x4,
        "The amount of PP restored per move by ingesting a Max Elixir (0x3E7).",
    )

    SLIP_SEED_VALUE = Symbol(
        [0x4096C], [0x231CBAC], 0x4, "Some value related to the Slip Seed (0xC75)."
    )

    ROCK_WRECKER_MOVE_ID = Symbol(
        [0x48360], [0x23245A0], 0x4, "The move ID for Rock Wrecker (453)."
    )

    CASTFORM_NORMAL_FORM_MALE_ID = Symbol(
        [0x591F8], [0x2335438], 0x4, "Castform's male normal form ID (0x17B)"
    )

    CASTFORM_NORMAL_FORM_FEMALE_ID = Symbol(
        [0x591FC], [0x233543C], 0x4, "Castform's female normal form ID (0x3D3)"
    )

    CHERRIM_SUNSHINE_FORM_MALE_ID = Symbol(
        [0x59200], [0x2335440], 0x4, "Cherrim's male sunshine form ID (0x1CD)"
    )

    CHERRIM_OVERCAST_FORM_FEMALE_ID = Symbol(
        [0x59204], [0x2335444], 0x4, "Cherrim's female overcast form ID (0x424)"
    )

    CHERRIM_SUNSHINE_FORM_FEMALE_ID = Symbol(
        [0x59208], [0x2335448], 0x4, "Cherrim's female sunshine form ID (0x425)"
    )

    FLOOR_GENERATION_STATUS_PTR = Symbol(
        [
            0x5EC2C,
            0x5ECC8,
            0x5EF4C,
            0x5F3D8,
            0x5F838,
            0x5F998,
            0x5FB30,
            0x5FCEC,
            0x600CC,
            0x6052C,
            0x60D40,
            0x60EC0,
            0x610D0,
            0x61430,
            0x61E18,
            0x63D50,
            0x63FDC,
            0x64490,
            0x6521C,
            0x65524,
            0x65F38,
            0x662D0,
            0x665A0,
            0x66934,
            0x66A24,
            0x66B58,
            0x66CE8,
        ],
        [
            0x233AE6C,
            0x233AF08,
            0x233B18C,
            0x233B618,
            0x233BA78,
            0x233BBD8,
            0x233BD70,
            0x233BF2C,
            0x233C30C,
            0x233C76C,
            0x233CF80,
            0x233D100,
            0x233D310,
            0x233D670,
            0x233E058,
            0x233FF90,
            0x234021C,
            0x23406D0,
            0x234145C,
            0x2341764,
            0x2342178,
            0x2342510,
            0x23427E0,
            0x2342B74,
            0x2342C64,
            0x2342D98,
            0x2342F28,
        ],
        0x4,
        (
            "Pointer to the global FLOOR_GENERATION_STATUS\n\ntype: struct"
            " floor_generation_status*"
        ),
    )

    OFFSET_OF_DUNGEON_N_NORMAL_ITEM_SPAWNS = Symbol(
        [0x5EC34, 0x65224],
        [0x233AE74, 0x2341464],
        0x4,
        (
            "Offset of the (number of base items + 1) field on the dungeon struct"
            " (0x12AFA)"
        ),
    )

    DUNGEON_GRID_COLUMN_BYTES = Symbol(
        [
            0x5F3D4,
            0x5F834,
            0x5FB2C,
            0x5FCE8,
            0x600C8,
            0x60530,
            0x607A4,
            0x60D38,
            0x60EBC,
            0x610D4,
            0x6142C,
            0x61E14,
            0x621F8,
            0x62AF0,
            0x62ED4,
            0x636BC,
            0x63D54,
            0x63FE0,
            0x64214,
            0x6628C,
        ],
        [
            0x233B614,
            0x233BA74,
            0x233BD6C,
            0x233BF28,
            0x233C308,
            0x233C770,
            0x233C9E4,
            0x233CF78,
            0x233D0FC,
            0x233D314,
            0x233D66C,
            0x233E054,
            0x233E438,
            0x233ED30,
            0x233F114,
            0x233F8FC,
            0x233FF94,
            0x2340220,
            0x2340454,
            0x23424CC,
        ],
        0x4,
        (
            "The number of bytes in one column of the dungeon grid cell array, 450,"
            " which corresponds to a column of 15 grid cells."
        ),
    )

    DEFAULT_MAX_POSITION = Symbol(
        [0x63D58],
        [0x233FF98],
        0x4,
        (
            "A large number (9999) to use as a default position for keeping track of"
            " min/max position values"
        ),
    )

    OFFSET_OF_DUNGEON_GUARANTEED_ITEM_ID = Symbol(
        [0x65220, 0x68C40],
        [0x2341460, 0x2344E80],
        0x4,
        "Offset of the guaranteed item ID field in the dungeon struct (0x2C9E8)",
    )

    FIXED_ROOM_TILE_SPAWN_TABLE = Symbol(
        [0x73B90],
        [0x234FDD0],
        0x2C,
        (
            "Table of tiles that can spawn in fixed rooms, pointed into by the"
            " FIXED_ROOM_TILE_SPAWN_TABLE.\n\nThis is an array of 11 4-byte entries"
            " containing info about one tile each. Info includes the trap ID if a trap,"
            " room ID, and flags.\n\ntype: struct fixed_room_tile_spawn_entry[11]"
        ),
    )

    TREASURE_BOX_1_ITEM_IDS = Symbol(
        [0x73BBC],
        [0x234FDFC],
        0x18,
        (
            "Item IDs for variant 1 of each of the treasure box items"
            " (ITEM_*_BOX_1).\n\ntype: struct item_id_16[12]"
        ),
    )

    FIXED_ROOM_REVISIT_OVERRIDES = Symbol(
        [0x73BD4],
        [0x234FE14],
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
        [0x73CD4],
        [0x234FF14],
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
        [0x73EB4],
        [0x23500F4],
        0x1F8,
        (
            "Table of items that can spawn in fixed rooms, pointed into by the"
            " FIXED_ROOM_ENTITY_SPAWN_TABLE.\n\nThis is an array of 63 8-byte entries"
            " containing one item ID each.\n\ntype: struct"
            " fixed_room_item_spawn_entry[63]"
        ),
    )

    FIXED_ROOM_ENTITY_SPAWN_TABLE = Symbol(
        [0x740AC],
        [0x23502EC],
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
        [0x74F7C],
        [0x23511BC],
        0x10,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::muzzled * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_MAGNET_RISE = Symbol(
        [0x74F8C],
        [0x23511CC],
        0x10,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::magnet_rise * 8. See UpdateStatusIconFlags for"
            " details."
        ),
    )

    STATUS_ICON_ARRAY_MIRACLE_EYE = Symbol(
        [0x74FAC],
        [0x23511EC],
        0x18,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::miracle_eye * 8. See UpdateStatusIconFlags for"
            " details."
        ),
    )

    STATUS_ICON_ARRAY_LEECH_SEED = Symbol(
        [0x74FBC],
        [0x23511FC],
        0x18,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::leech_seed * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_LONG_TOSS = Symbol(
        [0x74FD4],
        [0x2351214],
        0x18,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::long_toss * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_BLINDED = Symbol(
        [0x7502C],
        [0x235126C],
        0x28,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::blinded * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_BURN = Symbol(
        [0x75054],
        [0x2351294],
        0x28,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::burn * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_SURE_SHOT = Symbol(
        [0x7507C],
        [0x23512BC],
        0x28,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::sure_shot * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_INVISIBLE = Symbol(
        [0x750A4],
        [0x23512E4],
        0x28,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::invisible * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_SLEEP = Symbol(
        [0x750CC],
        [0x235130C],
        0x40,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::sleep * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_CURSE = Symbol(
        [0x750FC],
        [0x235133C],
        0x38,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::curse * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_FREEZE = Symbol(
        [0x75034],
        [0x2351274],
        0x40,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::freeze * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_CRINGE = Symbol(
        [0x75174],
        [0x23513B4],
        0x40,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::cringe * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_BIDE = Symbol(
        [0x751B4],
        [0x23513F4],
        0x70,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::bide * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_REFLECT = Symbol(
        [0x752B4],
        [0x23514F4],
        0x90,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::reflect * 8. See UpdateStatusIconFlags for details."
        ),
    )

    DIRECTIONS_XY = Symbol(
        [0x754DC],
        [0x235171C],
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
        [0x75DD0],
        [0x2352010],
        0x20,
        (
            "Action ID associated with each item category. Used by"
            " GetItemAction.\n\nEach entry is 2 bytes long."
        ),
    )

    FRACTIONAL_TURN_SEQUENCE = Symbol(
        [0x76044],
        [0x2352284],
        0xFA,
        (
            "Read by certain functions that are called by RunFractionalTurn to see if"
            " they should be executed.\n\nArray is accessed via a pointer added to some"
            " multiple of fractional_turn, so that if the resulting memory location is"
            " zero, the function returns."
        ),
    )

    BELLY_DRAIN_IN_WALLS_INT = Symbol(
        [0x76528],
        [0x2352768],
        0x2,
        (
            "The additional amount by which belly is decreased every turn when inside"
            " walls (integer part)"
        ),
    )

    BELLY_DRAIN_IN_WALLS_THOUSANDTHS = Symbol(
        [0x7652A],
        [0x235276A],
        0x2,
        (
            "The additional amount by which belly is decreased every turn when inside"
            " walls (fractional thousandths)"
        ),
    )

    SPATK_STAT_IDX = Symbol(
        [0x768A8],
        [0x2352AE8],
        0x4,
        (
            "The index (1) of the special attack entry in internal stat structs, such"
            " as the stat modifier array for a monster."
        ),
    )

    ATK_STAT_IDX = Symbol(
        [0x768AC],
        [0x2352AEC],
        0x4,
        (
            "The index (0) of the attack entry in internal stat structs, such as the"
            " stat modifier array for a monster."
        ),
    )

    MAP_COLOR_TABLE = Symbol(
        [0x76D90],
        [0x2352FD0],
        0x24,
        (
            "In order: white, black, red, green, blue, magenta, dark pink, chartreuse,"
            " light orange\n\nNote: unverified, ported from Irdkwia's notes\n\ntype:"
            " struct rgb[9]"
        ),
    )

    CORNER_CARDINAL_NEIGHBOR_IS_OPEN = Symbol(
        [0x76DD0],
        [0x2353010],
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
        [0x772F8],
        [0x2353538],
        0x4,
        (
            "[Runtime] Pointer to the dungeon struct in dungeon mode.\n\nThis is a"
            " 'working copy' of DUNGEON_PTR_MASTER. The main dungeon engine uses this"
            " pointer (or rather pointers to this pointer) when actually running"
            " dungeon mode.\n\ntype: struct dungeon*"
        ),
    )

    DUNGEON_PTR_MASTER = Symbol(
        [0x772FC],
        [0x235353C],
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
        [0x7731C],
        [0x235355C],
        0x4,
        "[Runtime] Pointer to the current leader of the team.\n\ntype: struct entity*",
    )

    DUNGEON_PRNG_STATE = Symbol(
        [0x77330],
        [0x2353570],
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
        [0x77344],
        [0x2353584],
        0x14,
        (
            "[Runtime] An array of 5 integers corresponding to the last value generated"
            " for each secondary LCG sequence.\n\nBased on the assembly, this appears"
            " to be its own global array, separate from DUNGEON_PRNG_STATE."
        ),
    )

    EXCL_ITEM_EFFECTS_WEATHER_ATK_SPEED_BOOST = Symbol(
        [0x77370],
        [0x23535B0],
        0x8,
        (
            "Array of IDs for exclusive item effects that increase attack speed with"
            " certain weather conditions."
        ),
    )

    EXCL_ITEM_EFFECTS_WEATHER_MOVE_SPEED_BOOST = Symbol(
        [0x77378],
        [0x23535B8],
        0x8,
        (
            "Array of IDs for exclusive item effects that increase movement speed with"
            " certain weather conditions."
        ),
    )

    EXCL_ITEM_EFFECTS_WEATHER_NO_STATUS = Symbol(
        [0x77380],
        [0x23535C0],
        0x8,
        (
            "Array of IDs for exclusive item effects that grant status immunity with"
            " certain weather conditions."
        ),
    )

    EXCL_ITEM_EFFECTS_EVASION_BOOST = Symbol(
        [0x774D0],
        [0x2353710],
        0x8,
        (
            "Array of IDs for exclusive item effects that grant an evasion boost with"
            " certain weather conditions."
        ),
    )

    DEFAULT_TILE = Symbol(
        [0x774E4],
        [0x2353724],
        0x14,
        (
            "The default tile struct.\n\nThis is just a struct full of zeroes, but is"
            " used as a fallback in various places where a 'default' tile is needed,"
            " such as when a grid index is out of range.\n\ntype: struct tile"
        ),
    )

    HIDDEN_STAIRS_SPAWN_BLOCKED = Symbol(
        [0x7754C],
        [0x235378C],
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
        [0x77554],
        [0x2353794],
        0x4,
        (
            "[Runtime] Pointer to decoded fixed room data loaded from the"
            " BALANCE/fixed.bin file."
        ),
    )

    NECTAR_IQ_BOOST = Symbol(
        [0x40144], [0x231C384], None, "IQ boost from ingesting Nectar."
    )


class NaOverlay29Section:
    name = "overlay29"
    description = (
        "The dungeon engine.\n\nThis is the 'main' overlay of dungeon mode. It controls"
        " most things that happen in a Mystery Dungeon, such as dungeon layout"
        " generation, dungeon menus, enemy AI, and generally just running each turn"
        " while within a dungeon."
    )
    loadaddress = 0x22DC240
    length = 0x77620
    functions = NaOverlay29Functions
    data = NaOverlay29Data


class NaOverlay3Functions:
    pass


class NaOverlay3Data:
    pass


class NaOverlay3Section:
    name = "overlay3"
    description = "Controls the Friend Rescue submenu within the top menu."
    loadaddress = 0x233CA80
    length = 0xA160
    functions = NaOverlay3Functions
    data = NaOverlay3Data


class NaOverlay30Functions:
    pass


class NaOverlay30Data:
    OVERLAY30_JP_STRING_1 = Symbol([0x3860], [0x2386080], 0xC, "みさき様")

    OVERLAY30_JP_STRING_2 = Symbol([0x386C], [0x238608C], 0xC, "やよい様")


class NaOverlay30Section:
    name = "overlay30"
    description = "Controls quicksaving in dungeons."
    loadaddress = 0x2382820
    length = 0x38A0
    functions = NaOverlay30Functions
    data = NaOverlay30Data


class NaOverlay31Functions:
    EntryOverlay31 = Symbol(
        [0x0],
        [0x2382820],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nNo params.",
    )

    DungeonMenuSwitch = Symbol(
        [0x2A0],
        [0x2382AC0],
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: appears to be an"
            " index of some sort, probably the menu index based on the function name?"
        ),
    )

    MovesMenu = Symbol(
        [0x29A0],
        [0x23851C0],
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
        [0x2385404],
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
        [0x482C],
        [0x238704C],
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
        [0x5F6C],
        [0x238878C],
        None,
        (
            "Called when the in-dungeon 'rest' menu is open. Does not return until the"
            " menu is closed.\n\nNo params."
        ),
    )

    RecruitmentSearchMenuLoop = Symbol(
        [0x63E4],
        [0x2388C04],
        None,
        (
            "Called on each frame while the in-dungeon 'recruitment search' menu is"
            " open.\n\nreturn: int (Actually, this is probably some sort of enum shared"
            " by all the MenuLoop functions)"
        ),
    )

    HelpMenuLoop = Symbol(
        [0x69DC],
        [0x23891FC],
        None,
        (
            "Called on each frame while the in-dungeon 'help' menu is open.\n\nThe menu"
            " is still considered open while one of the help pages is being viewed, so"
            " this function keeps being called even after choosing an"
            " option.\n\nreturn: int (Actually, this is probably some sort of enum"
            " shared by all the MenuLoop functions)"
        ),
    )


class NaOverlay31Data:
    DUNGEON_D_BOX_LAYOUT_1 = Symbol(
        [0x7574], [0x2389D94], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_2 = Symbol(
        [0x7584], [0x2389DA4], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_3 = Symbol(
        [0x7594], [0x2389DB4], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_4 = Symbol(
        [0x75A4], [0x2389DC4], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_MAIN_MENU = Symbol([0x75B4], [0x2389DD4], 0x40, "")

    OVERLAY31_UNKNOWN_STRING_IDS = Symbol(
        [0x7600], [0x2389E20], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_STRUCT__NA_2389E30 = Symbol(
        [0x7610], [0x2389E30], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_5 = Symbol(
        [0x7620], [0x2389E40], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_6 = Symbol(
        [0x7630], [0x2389E50], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_7 = Symbol(
        [0x7640], [0x2389E60], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_SUBMENU_1 = Symbol([0x7650], [0x2389E70], 0x20, "")

    DUNGEON_SUBMENU_2 = Symbol([0x7670], [0x2389E90], 0x20, "")

    DUNGEON_SUBMENU_3 = Symbol([0x7690], [0x2389EB0], 0x20, "")

    DUNGEON_SUBMENU_4 = Symbol([0x76B0], [0x2389ED0], 0x20, "")

    OVERLAY31_UNKNOWN_STRUCT__NA_2389EF0 = Symbol(
        [0x76D0], [0x2389EF0], 0xC, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_8 = Symbol(
        [0x76DC], [0x2389EFC], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_9 = Symbol(
        [0x76EC], [0x2389F0C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_10 = Symbol(
        [0x76FC], [0x2389F1C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_11 = Symbol(
        [0x770C], [0x2389F2C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_12 = Symbol(
        [0x771C], [0x2389F3C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_13 = Symbol(
        [0x772C], [0x2389F4C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_JP_STRING = Symbol(
        [0x7744], [0x2389F64], 0x24, "\n\n----　 初期ポジション=%d　----- \n"
    )

    DUNGEON_D_BOX_LAYOUT_14 = Symbol(
        [0x7768], [0x2389F88], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_15 = Symbol(
        [0x7778], [0x2389F98], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_16 = Symbol(
        [0x7788], [0x2389FA8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_17 = Symbol(
        [0x7798], [0x2389FB8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_18 = Symbol(
        [0x77A8], [0x2389FC8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_19 = Symbol(
        [0x77B8], [0x2389FD8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_STRUCT__NA_2389FE8 = Symbol(
        [0x77C8], [0x2389FE8], 0xC, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_20 = Symbol(
        [0x77D4], [0x2389FF4], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_21 = Symbol(
        [0x77E4], [0x238A004], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_22 = Symbol(
        [0x77F4], [0x238A014], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_23 = Symbol(
        [0x7804], [0x238A024], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_24 = Symbol(
        [0x7814], [0x238A034], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_25 = Symbol(
        [0x78EC], [0x238A10C], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_SUBMENU_5 = Symbol([0x78FC], [0x238A11C], 0x18, "")

    DUNGEON_D_BOX_LAYOUT_26 = Symbol(
        [0x7914], [0x238A134], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_STRUCT__NA_238A144 = Symbol(
        [0x7924], [0x238A144], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_27 = Symbol(
        [0x7950], [0x238A170], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_28 = Symbol(
        [0x7960], [0x238A180], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_STRUCT__NA_238A190 = Symbol(
        [0x7970], [0x238A190], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_SUBMENU_6 = Symbol([0x7980], [0x238A1A0], 0x48, "")

    DUNGEON_D_BOX_LAYOUT_29 = Symbol(
        [0x79C8], [0x238A1E8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_30 = Symbol(
        [0x79D8], [0x238A1F8], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_31 = Symbol(
        [0x79E8], [0x238A208], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_D_BOX_LAYOUT_32 = Symbol(
        [0x79F8], [0x238A218], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_RESERVED_SPACE = Symbol(
        [0x7A30], [0x238A250], 0x10, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A260 = Symbol(
        [0x7A40], [0x238A260], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_VALUE__NA_238A264 = Symbol(
        [0x7A44], [0x238A264], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A268 = Symbol(
        [0x7A48], [0x238A268], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A26C = Symbol(
        [0x7A4C], [0x238A26C], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A270 = Symbol(
        [0x7A50], [0x238A270], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A274 = Symbol(
        [0x7A54], [0x238A274], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A278 = Symbol(
        [0x7A58], [0x238A278], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A27C = Symbol(
        [0x7A5C], [0x238A27C], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A280 = Symbol(
        [0x7A60], [0x238A280], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A284 = Symbol(
        [0x7A64], [0x238A284], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A288 = Symbol(
        [0x7A68], [0x238A288], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY31_UNKNOWN_POINTER__NA_238A28C = Symbol(
        [0x7A6C], [0x238A28C], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )


class NaOverlay31Section:
    name = "overlay31"
    description = "Controls the dungeon menu (during dungeon mode)."
    loadaddress = 0x2382820
    length = 0x7A80
    functions = NaOverlay31Functions
    data = NaOverlay31Data


class NaOverlay32Functions:
    pass


class NaOverlay32Data:
    pass


class NaOverlay32Section:
    name = "overlay32"
    description = "Unused; all zeroes."
    loadaddress = 0x2382820
    length = 0x20
    functions = NaOverlay32Functions
    data = NaOverlay32Data


class NaOverlay33Functions:
    pass


class NaOverlay33Data:
    pass


class NaOverlay33Section:
    name = "overlay33"
    description = "Unused; all zeroes."
    loadaddress = 0x2382820
    length = 0x20
    functions = NaOverlay33Functions
    data = NaOverlay33Data


class NaOverlay34Functions:
    ExplorersOfSkyMain = Symbol(
        [0x0],
        [0x22DC240],
        None,
        (
            "The main function for Explorers of Sky.\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: probably a game mode ID?\nreturn: probably a"
            " return code?"
        ),
    )


class NaOverlay34Data:
    OVERLAY34_UNKNOWN_STRUCT__NA_22DD014 = Symbol(
        [0xDD4],
        [0x22DD014],
        0x10,
        "1*0x4 + 3*0x4\n\nNote: unverified, ported from Irdkwia's notes",
    )

    START_MENU_CONFIRM = Symbol([0xDE4], [0x22DD024], 0x18, "Irdkwia's notes: 3*0x8")

    OVERLAY34_UNKNOWN_STRUCT__NA_22DD03C = Symbol(
        [0xDFC],
        [0x22DD03C],
        0x10,
        "1*0x4 + 3*0x4\n\nNote: unverified, ported from Irdkwia's notes",
    )

    DUNGEON_DEBUG_MENU = Symbol([0xE0C], [0x22DD04C], 0x28, "Irdkwia's notes: 5*0x8")

    OVERLAY34_RESERVED_SPACE = Symbol(
        [0xE34], [0x22DD074], 0xC, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY34_UNKNOWN_POINTER__NA_22DD080 = Symbol(
        [0xE40], [0x22DD080], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY34_UNKNOWN_POINTER__NA_22DD084 = Symbol(
        [0xE44], [0x22DD084], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY34_UNKNOWN_POINTER__NA_22DD088 = Symbol(
        [0xE48], [0x22DD088], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY34_UNKNOWN_POINTER__NA_22DD08C = Symbol(
        [0xE4C], [0x22DD08C], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY34_UNKNOWN_POINTER__NA_22DD090 = Symbol(
        [0xE50], [0x22DD090], 0x4, "Note: unverified, ported from Irdkwia's notes"
    )


class NaOverlay34Section:
    name = "overlay34"
    description = (
        "Related to launching the game.\n\nThere are mention in the strings of logos"
        " like the ESRB logo. This only seems to be loaded during the ESRB rating"
        " splash screen, so this is likely the sole purpose of this overlay."
    )
    loadaddress = 0x22DC240
    length = 0xE60
    functions = NaOverlay34Functions
    data = NaOverlay34Data


class NaOverlay35Functions:
    pass


class NaOverlay35Data:
    pass


class NaOverlay35Section:
    name = "overlay35"
    description = "Unused; all zeroes."
    loadaddress = 0x22BCA80
    length = 0x20
    functions = NaOverlay35Functions
    data = NaOverlay35Data


class NaOverlay4Functions:
    pass


class NaOverlay4Data:
    pass


class NaOverlay4Section:
    name = "overlay4"
    description = "Controls the Trade Items submenu within the top menu."
    loadaddress = 0x233CA80
    length = 0x2BE0
    functions = NaOverlay4Functions
    data = NaOverlay4Data


class NaOverlay5Functions:
    pass


class NaOverlay5Data:
    pass


class NaOverlay5Section:
    name = "overlay5"
    description = "Controls the Trade Team submenu within the top menu."
    loadaddress = 0x233CA80
    length = 0x3240
    functions = NaOverlay5Functions
    data = NaOverlay5Data


class NaOverlay6Functions:
    pass


class NaOverlay6Data:
    pass


class NaOverlay6Section:
    name = "overlay6"
    description = "Controls the Wonder Mail S submenu within the top menu."
    loadaddress = 0x233CA80
    length = 0x2460
    functions = NaOverlay6Functions
    data = NaOverlay6Data


class NaOverlay7Functions:
    pass


class NaOverlay7Data:
    pass


class NaOverlay7Section:
    name = "overlay7"
    description = (
        "Controls the Nintendo WFC submenu within the top menu (under 'Other')."
    )
    loadaddress = 0x233CA80
    length = 0x5100
    functions = NaOverlay7Functions
    data = NaOverlay7Data


class NaOverlay8Functions:
    pass


class NaOverlay8Data:
    pass


class NaOverlay8Section:
    name = "overlay8"
    description = (
        "Controls the Send Demo Dungeon submenu within the top menu (under 'Other')."
    )
    loadaddress = 0x233CA80
    length = 0x2200
    functions = NaOverlay8Functions
    data = NaOverlay8Data


class NaOverlay9Functions:
    pass


class NaOverlay9Data:
    TOP_MENU_RETURN_MUSIC_ID = Symbol(
        [0xE80],
        [0x233D900],
        None,
        "Song playing in the main menu when returning from the Sky Jukebox.",
    )


class NaOverlay9Section:
    name = "overlay9"
    description = "Controls the Sky Jukebox."
    loadaddress = 0x233CA80
    length = 0x2D80
    functions = NaOverlay9Functions
    data = NaOverlay9Data


class NaRamFunctions:
    pass


class NaRamData:
    DUNGEON_COLORMAP_PTR = Symbol(
        [0x1B9CF4],
        [0x21B9CF4],
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
        [0x1B9D34],
        [0x21B9D34],
        0x2CB14,
        (
            "The dungeon context struct used for tons of stuff in dungeon mode. See"
            " struct dungeon in the C headers.\n\nThis struct never seems to be"
            " referenced directly, and is instead usually accessed via DUNGEON_PTR in"
            " overlay 29.\n\ntype: struct dungeon"
        ),
    )

    MOVE_DATA_TABLE = Symbol(
        [0x2113CC],
        [0x22113CC],
        0x38C6,
        (
            "The move data table loaded directly from /BALANCE/waza_p.bin. See struct"
            " move_data_table in the C headers.\n\nPointed to by MOVE_DATA_TABLE_PTR in"
            " the ARM 9 binary.\n\ntype: struct move_data_table"
        ),
    )

    FRAMES_SINCE_LAUNCH = Symbol(
        [0x2A354C, 0x2A359C],
        [0x22A354C, 0x22A359C],
        0x4,
        (
            "Starts at 0 when the game is first launched, and continuously ticks up"
            " once per frame while the game is running."
        ),
    )

    BAG_ITEMS = Symbol(
        [0x2A3824],
        [0x22A3824],
        0x12C,
        (
            "Array of item structs within the player's bag.\n\nWhile the game only"
            " allows a maximum of 48 items during normal play, it seems to read up to"
            " 50 item slots if filled.\n\ntype: struct item[50]"
        ),
    )

    BAG_ITEMS_PTR = Symbol([0x2A3BA8], [0x22A3BA8], 0x4, "Pointer to BAG_ITEMS.")

    STORAGE_ITEMS = Symbol(
        [0x2A3BAE],
        [0x22A3BAE],
        0x7D0,
        (
            "Array of item IDs in the player's item storage.\n\nFor stackable items,"
            " the quantities are stored elsewhere, in STORAGE_ITEM_QUANTITIES.\n\ntype:"
            " struct item_id_16[1000]"
        ),
    )

    STORAGE_ITEM_QUANTITIES = Symbol(
        [0x2A437E],
        [0x22A437E],
        0x7D0,
        (
            "Array of 1000 2-byte (unsigned) quantities corresponding to the item IDs"
            " in STORAGE_ITEMS.\n\nIf the corresponding item ID is not a stackable"
            " item, the entry in this array is unused, and will be 0."
        ),
    )

    KECLEON_SHOP_ITEMS_PTR = Symbol(
        [0x2A4B50], [0x22A4B50], 0x4, "Pointer to KECLEON_SHOP_ITEMS."
    )

    KECLEON_SHOP_ITEMS = Symbol(
        [0x2A4B54],
        [0x22A4B54],
        0x20,
        (
            "Array of up to 8 items in the Kecleon Shop.\n\nIf there are fewer than 8"
            " items, the array is expected to be null-terminated.\n\ntype: struct"
            " bulk_item[8]"
        ),
    )

    UNUSED_KECLEON_SHOP_ITEMS = Symbol(
        [0x2A4B74],
        [0x22A4B74],
        0x20,
        (
            "Seems to be another array like KECLEON_SHOP_ITEMS, but don't actually"
            " appear to be used by the Kecleon Shop."
        ),
    )

    KECLEON_WARES_ITEMS_PTR = Symbol(
        [0x2A4B94], [0x22A4B94], 0x4, "Pointer to KECLEON_WARES_ITEMS."
    )

    KECLEON_WARES_ITEMS = Symbol(
        [0x2A4B98],
        [0x22A4B98],
        0x10,
        (
            "Array of up to 4 items in Kecleon Wares.\n\nIf there are fewer than 4"
            " items, the array is expected to be null-terminated.\n\ntype: struct"
            " bulk_item[4]"
        ),
    )

    UNUSED_KECLEON_WARES_ITEMS = Symbol(
        [0x2A4BA8],
        [0x22A4BA8],
        0x10,
        (
            "Seems to be another array like KECLEON_WARES_ITEMS, but don't actually"
            " appear to be used by Kecleon Wares."
        ),
    )

    MONEY_CARRIED = Symbol(
        [0x2A4BB8],
        [0x22A4BB8],
        0x4,
        "The amount of money the player is currently carrying.",
    )

    MONEY_STORED = Symbol(
        [0x2A4BC4],
        [0x22A4BC4],
        0x4,
        "The amount of money the player currently has stored in the Duskull Bank.",
    )

    DIALOG_BOX_LIST = Symbol(
        [0x2A88DC], [0x22A88DC], None, "Array of allocated dialog box structs."
    )

    LAST_NEW_MOVE = Symbol(
        [0x2AAE4C],
        [0x22AAE4C],
        0x8,
        (
            "Move struct of the last new move introduced when learning a new move."
            " Persists even after the move selection is made in the menu.\n\ntype:"
            " struct move"
        ),
    )

    SCRIPT_VARS_VALUES = Symbol(
        [0x2AB0AC],
        [0x22AB0AC],
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
        [0x2AB15C],
        [0x22AB15C],
        0x1,
        (
            "The player's bag level, which determines the bag capacity. This indexes"
            " directly into the BAG_CAPACITY_TABLE in the ARM9 binary."
        ),
    )

    DEBUG_SPECIAL_EPISODE_NUMBER = Symbol(
        [0x2AB4AC],
        [0x22AB4AC],
        0x1,
        (
            "The number of the special episode currently being played.\n\nThis backs"
            " the EXECUTE_SPECIAL_EPISODE_TYPE script variable.\n\ntype: struct"
            " special_episode_type_8"
        ),
    )

    PENDING_DUNGEON_ID = Symbol(
        [0x2AB4FC],
        [0x22AB4FC],
        0x1,
        (
            "The ID of the selected dungeon when setting off from the"
            " overworld.\n\nControls the text and map location during the 'map"
            " cutscene' just before entering a dungeon, as well as the actual dungeon"
            " loaded afterwards.\n\ntype: struct dungeon_id_8"
        ),
    )

    PENDING_STARTING_FLOOR = Symbol(
        [0x2AB4FD],
        [0x22AB4FD],
        0x1,
        (
            "The floor number to start from in the dungeon specified by"
            " PENDING_DUNGEON_ID."
        ),
    )

    PLAY_TIME_SECONDS = Symbol(
        [0x2AB694], [0x22AB694], 0x4, "The player's total play time in seconds."
    )

    PLAY_TIME_FRAME_COUNTER = Symbol(
        [0x2AB698],
        [0x22AB698],
        0x1,
        (
            "Counts from 0-59 in a loop, with the play time being incremented by 1"
            " second with each rollover."
        ),
    )

    TEAM_NAME = Symbol(
        [0x2AB918],
        [0x22AB918],
        0xC,
        (
            "The team name.\n\nA null-terminated string, with a maximum length of 10."
            " Presumably encoded with the ANSI/Shift JIS encoding the game typically"
            " uses.\n\nThis is presumably part of a larger struct, together with other"
            " nearby data."
        ),
    )

    TEAM_MEMBER_LIST = Symbol(
        [0x2ABDE0],
        [0x22ABDE0],
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
        [0x2B514C],
        [0x22B514C],
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
        [0x2B99C4],
        [0x22B99C4],
        0x4,
        (
            "Starts at 0 when the game is first launched, and ticks up by 3 per frame"
            " while the game is running."
        ),
    )

    SENTRY_DUTY_STRUCT = Symbol([0x37A5D0], [0x237A5D0], 0x38D4, "")

    TURNING_ON_THE_SPOT_FLAG = Symbol(
        [0x37C9A6],
        [0x237C9A6],
        0x1,
        "[Runtime] Flag for whether the player is turning on the spot (pressing Y).",
    )

    METRONOME_NEXT_INDEX = Symbol(
        [0x37CA88],
        [0x237CA88],
        0x4,
        "[Runtime] The index into METRONOME_TABLE for the next usage of Metronome.",
    )

    FLOOR_GENERATION_STATUS = Symbol(
        [0x37CFBC],
        [0x237CFBC],
        0x40,
        (
            "[Runtime] Status data related to generation of the current floor in a"
            " dungeon.\n\nThis data is populated as the dungeon floor is"
            " generated.\n\ntype: struct floor_generation_status"
        ),
    )


class NaRamSection:
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
    functions = NaRamFunctions
    data = NaRamData


class NaSections:
    arm7 = NaArm7Section

    arm9 = NaArm9Section

    itcm = NaItcmSection

    move_effects = NaMove_effectsSection

    overlay0 = NaOverlay0Section

    overlay1 = NaOverlay1Section

    overlay10 = NaOverlay10Section

    overlay11 = NaOverlay11Section

    overlay12 = NaOverlay12Section

    overlay13 = NaOverlay13Section

    overlay14 = NaOverlay14Section

    overlay15 = NaOverlay15Section

    overlay16 = NaOverlay16Section

    overlay17 = NaOverlay17Section

    overlay18 = NaOverlay18Section

    overlay19 = NaOverlay19Section

    overlay2 = NaOverlay2Section

    overlay20 = NaOverlay20Section

    overlay21 = NaOverlay21Section

    overlay22 = NaOverlay22Section

    overlay23 = NaOverlay23Section

    overlay24 = NaOverlay24Section

    overlay25 = NaOverlay25Section

    overlay26 = NaOverlay26Section

    overlay27 = NaOverlay27Section

    overlay28 = NaOverlay28Section

    overlay29 = NaOverlay29Section

    overlay3 = NaOverlay3Section

    overlay30 = NaOverlay30Section

    overlay31 = NaOverlay31Section

    overlay32 = NaOverlay32Section

    overlay33 = NaOverlay33Section

    overlay34 = NaOverlay34Section

    overlay35 = NaOverlay35Section

    overlay4 = NaOverlay4Section

    overlay5 = NaOverlay5Section

    overlay6 = NaOverlay6Section

    overlay7 = NaOverlay7Section

    overlay8 = NaOverlay8Section

    overlay9 = NaOverlay9Section

    ram = NaRamSection
