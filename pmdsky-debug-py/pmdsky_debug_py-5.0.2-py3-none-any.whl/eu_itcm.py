from .protocol import Symbol


class EuItcmArm7Functions:
    EntryArm7 = Symbol(
        None,
        None,
        None,
        (
            "The entrypoint for the ARM7 CPU. This is like the 'main' function for the"
            " ARM7 subsystem.\n\nNo params."
        ),
    )


class EuItcmArm7Data:
    pass


class EuItcmArm7Section:
    name = "arm7"
    description = (
        "The ARM7 binary.\n\nThis is the secondary binary that gets loaded when the"
        " game is launched.\n\nSpeaking generally, this is the program run by the"
        " Nintendo DS's secondary ARM7TDMI CPU, which handles the audio engine, the"
        " touch screen, Wi-Fi functions, cryptography, and more."
    )
    loadaddress = None
    length = None
    functions = EuItcmArm7Functions
    data = EuItcmArm7Data


class EuItcmArm9Functions:
    EntryArm9 = Symbol(
        None,
        None,
        None,
        (
            "The entrypoint for the ARM9 CPU. This is like the 'main' function for the"
            " ARM9 subsystem.\n\nNo params."
        ),
    )

    InitMemAllocTable = Symbol(
        None,
        None,
        None,
        (
            "Initializes MEMORY_ALLOCATION_TABLE.\n\nSets up the default memory arena,"
            " sets the default memory allocator parameters (calls"
            " SetMemAllocatorParams(0, 0)), and does some other stuff.\n\nNo params."
        ),
    )

    SetMemAllocatorParams = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "The default function for retrieving the arena for memory allocations. This"
            " function always just returns the initial arena pointer.\n\nr0: initial"
            " memory arena pointer, or null\nr1: flags (see MemAlloc)\nreturn: memory"
            " arena pointer, or null"
        ),
    )

    GetFreeArenaDefault = Symbol(
        None,
        None,
        None,
        (
            "The default function for retrieving the arena for memory freeing. This"
            " function always just returns the initial arena pointer.\n\nr0: initial"
            " memory arena pointer, or null\nr1: pointer to free\nreturn: memory arena"
            " pointer, or null"
        ),
    )

    InitMemArena = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Converts the internal alloc flags bitfield (struct mem_block field 0x4) to"
            " the block type bitfield (struct mem_block field 0x0).\n\nr0: internal"
            " alloc flags\nreturn: block type flags"
        ),
    )

    FindAvailableMemBlock = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Frees heap-allocated memory.\n\nThis function is just a wrapper around"
            " MemLocateUnset.\n\nr0: pointer"
        ),
    )

    MemArenaAlloc = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Divide a number by 256 and round up to the nearest integer.\n\nr0:"
            " number\nreturn: number // 256"
        ),
    )

    MultiplyByFixedPoint = Symbol(
        None,
        None,
        None,
        (
            "Multiply a signed integer x by a signed binary fixed-point multiplier (8"
            " fraction bits).\n\nr0: x\nr1: multiplier\nreturn: x * multiplier"
        ),
    )

    UMultiplyByFixedPoint = Symbol(
        None,
        None,
        None,
        (
            "Multiplies an unsigned integer x by an unsigned binary fixed-point"
            " multiplier (8 fraction bits).\n\nr0: x\nr1: multiplier\nreturn: x *"
            " multiplier"
        ),
    )

    GetRngSeed = Symbol(None, None, None, "Get the current value of PRNG_SEQUENCE_NUM.")

    SetRngSeed = Symbol(
        None, None, None, "Seed PRNG_SEQUENCE_NUM to a given value.\n\nr0: seed"
    )

    Rand16Bit = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Computes a random 32-bit integer using the general-purpose PRNG. The upper"
            " and lower 16 bits are each generated with a separate call to Rand16Bit"
            " (so this function advances the PRNG twice).\n\nreturn: pseudorandom int"
            " on the interval [0, 4294967295]"
        ),
    )

    RandIntSafe = Symbol(
        None,
        None,
        None,
        (
            "Same as RandInt, except explicitly masking out the upper 16 bits of the"
            " output from Rand16Bit (which should be zero anyway).\n\nr0: high\nreturn:"
            " pseudorandom integer on the interval [0, high - 1]"
        ),
    )

    RandRangeSafe = Symbol(
        None,
        None,
        None,
        (
            "Like RandRange, except reordering the inputs as needed, and explicitly"
            " masking out the upper 16 bits of the output from Rand16Bit (which should"
            " be zero anyway).\n\nr0: x\nr1: y\nreturn: pseudorandom integer on the"
            " interval [min(x, y), max(x, y) - 1]"
        ),
    )

    WaitForever = Symbol(
        None,
        None,
        None,
        (
            "Sets some program state and calls WaitForInterrupt in an infinite"
            " loop.\n\nThis is called on fatal errors to hang the program"
            " indefinitely.\n\nNo params."
        ),
    )

    InterruptMasterDisable = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: previous state",
    )

    InterruptMasterEnable = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: previous state",
    )

    InitMemAllocTableVeneer = Symbol(
        None,
        None,
        None,
        (
            "Likely a linker-generated veneer for InitMemAllocTable.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nNo"
            " params."
        ),
    )

    ZInit8 = Symbol(None, None, None, "Zeroes an 8-byte buffer.\n\nr0: ptr")

    PointsToZero = Symbol(
        None,
        None,
        None,
        "Checks whether a pointer points to zero.\n\nr0: ptr\nreturn: bool",
    )

    MemZero = Symbol(None, None, None, "Zeroes a buffer.\n\nr0: ptr\nr1: len")

    MemZero16 = Symbol(
        None,
        None,
        None,
        "Zeros a buffer of 16-bit values.\n\nr0: ptr\nr1: len (# bytes)",
    )

    MemZero32 = Symbol(
        None,
        None,
        None,
        "Zeros a buffer of 32-bit values.\n\nr0: ptr\nr1: len (# bytes)",
    )

    MemsetSimple = Symbol(
        None,
        None,
        None,
        (
            "A simple implementation of the memset(3) C library function.\n\nThis"
            " function was probably manually implemented by the developers. See Memset"
            " for what's probably the real libc function.\n\nr0: ptr\nr1: value\nr2:"
            " len (# bytes)"
        ),
    )

    Memset32 = Symbol(
        None,
        None,
        None,
        (
            "Fills a buffer of 32-bit values with a given value.\n\nr0: ptr\nr1:"
            " value\nr2: len (# bytes)"
        ),
    )

    MemcpySimple = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Copies 16-bit values from one buffer to another.\n\nr0: dest\nr1: src\nr2:"
            " n (# bytes)"
        ),
    )

    Memcpy32 = Symbol(
        None,
        None,
        None,
        (
            "Copies 32-bit values from one buffer to another.\n\nr0: dest\nr1: src\nr2:"
            " n (# bytes)"
        ),
    )

    TaskProcBoot = Symbol(
        None,
        None,
        None,
        (
            "Probably related to booting the game?\n\nThis function prints the debug"
            " message 'task proc boot'.\n\nNo params."
        ),
    )

    EnableAllInterrupts = Symbol(
        None,
        None,
        None,
        (
            "Sets the Interrupt Master Enable (IME) register to 1, which enables all"
            " CPU interrupts (if enabled in the Interrupt Enable (IE) register).\n\nSee"
            " https://problemkaputt.de/gbatek.htm#dsiomaps.\n\nreturn: old value in the"
            " IME register"
        ),
    )

    GetTime = Symbol(
        None,
        None,
        None,
        (
            "Seems to get the current (system?) time as an IEEE 754 floating-point"
            " number.\n\nreturn: current time (maybe in seconds?)"
        ),
    )

    DisableAllInterrupts = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Probably resumes the sound player if paused?\n\nThis function prints the"
            " debug string 'sound resume'."
        ),
    )

    CardPullOutWithStatus = Symbol(
        None,
        None,
        None,
        (
            "Probably aborts the program with some status code? It seems to serve a"
            " similar purpose to the exit(3) function.\n\nThis function prints the"
            " debug string 'card pull out %d' with the status code.\n\nr0: status code"
        ),
    )

    CardPullOut = Symbol(
        None,
        None,
        None,
        (
            "Sets some global flag that probably triggers system exit?\n\nThis function"
            " prints the debug string 'card pull out'.\n\nNo params."
        ),
    )

    CardBackupError = Symbol(
        None,
        None,
        None,
        (
            "Sets some global flag that maybe indicates a save error?\n\nThis function"
            " prints the debug string 'card backup error'.\n\nNo params."
        ),
    )

    HaltProcessDisp = Symbol(
        None,
        None,
        None,
        (
            "Maybe halts the process display?\n\nThis function prints the debug string"
            " 'halt process disp %d' with the status code.\n\nr0: status code"
        ),
    )

    OverlayIsLoaded = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Loads an overlay from ROM by its group ID.\n\nSee the"
            " LOADED_OVERLAY_GROUP_* data symbols or enum overlay_group_id in the C"
            " headers for a mapping between group ID and overlay number.\n\nr0: group"
            " ID of the overlay to load"
        ),
    )

    UnloadOverlay = Symbol(
        None,
        None,
        None,
        (
            "Unloads an overlay from ROM by its group ID.\n\nSee the"
            " LOADED_OVERLAY_GROUP_* data symbols or enum overlay_group_id in the C"
            " headers for a mapping between group ID and overlay number.\n\nr0: group"
            " ID of the overlay to unload\nothers: ?"
        ),
    )

    EuclideanNorm = Symbol(
        None,
        None,
        None,
        (
            "Computes the Euclidean norm of a two-component integer array, sort of like"
            " hypotf(3).\n\nr0: integer array [x, y]\nreturn: sqrt(x*x + y*y)"
        ),
    )

    ClampComponentAbs = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: controller\nr1:"
            " btn_ptr\nreturn: any_activated"
        ),
    )

    GetPressedButtons = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: controller\nr1:"
            " btn_ptr\nreturn: any_activated"
        ),
    )

    GetReleasedStylus = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: stylus_ptr\nreturn:"
            " any_activated"
        ),
    )

    KeyWaitInit = Symbol(
        None,
        None,
        None,
        (
            "Implements (most of?) SPECIAL_PROC_KEY_WAIT_INIT (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    DataTransferInit = Symbol(
        None,
        None,
        None,
        (
            "Initializes data transfer mode to get data from the ROM cartridge.\n\nNo"
            " params."
        ),
    )

    DataTransferStop = Symbol(
        None,
        None,
        None,
        (
            "Finalizes data transfer from the ROM cartridge.\n\nThis function must"
            " always be called if DataTransferInit was called, or the game will"
            " crash.\n\nNo params."
        ),
    )

    FileInitVeneer = Symbol(
        None,
        None,
        None,
        (
            "Likely a linker-generated veneer for FileInit.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " file_stream pointer"
        ),
    )

    FileOpen = Symbol(
        None,
        None,
        None,
        (
            "Opens a file from the ROM file system at the given path, sort of like C's"
            " fopen(3) library function.\n\nr0: file_stream pointer\nr1: file path"
            " string"
        ),
    )

    FileGetSize = Symbol(
        None,
        None,
        None,
        "Gets the size of an open file.\n\nr0: file_stream pointer\nreturn: file size",
    )

    FileRead = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Sets a file stream's position indicator.\n\nThis function has the a"
            " similar API to the fseek(3) library function from C, including using the"
            " same codes for the `whence` parameter:\n- SEEK_SET=0\n- SEEK_CUR=1\n-"
            " SEEK_END=2\n\nr0: file_stream pointer\nr1: offset\nr2: whence"
        ),
    )

    FileClose = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: addr_ptr",
    )

    LoadFileFromRom = Symbol(
        None,
        None,
        None,
        (
            "Loads a file from ROM by filepath into a heap-allocated buffer.\n\nr0:"
            " [output] pointer to an IO struct {ptr, len}\nr1: file path string"
            " pointer\nr2: flags"
        ),
    )

    GetDebugFlag1 = Symbol(
        None,
        None,
        None,
        "Just returns 0 in the final binary.\n\nr0: flag ID\nreturn: flag value",
    )

    SetDebugFlag1 = Symbol(
        None, None, None, "A no-op in the final binary.\n\nr0: flag ID\nr1: flag value"
    )

    AppendProgPos = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Would log a printf format string in the debug binary.\n\nThis still"
            " constructs the string with Vsprintf, but doesn't actually do anything"
            " with it in the final binary.\n\nr0: format\n...: variadic"
        ),
    )

    GetDebugFlag2 = Symbol(
        None,
        None,
        None,
        "Just returns 0 in the final binary.\n\nr0: flag ID\nreturn: flag value",
    )

    SetDebugFlag2 = Symbol(
        None, None, None, "A no-op in the final binary.\n\nr0: flag ID\nr1: flag value"
    )

    DebugPrint = Symbol(
        None,
        None,
        None,
        (
            "Would log a printf format string in the debug binary. A no-op in the final"
            " binary.\n\nr0: log level\nr1: format\n...: variadic"
        ),
    )

    FatalError = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Open the 6 files at PACK_FILE_PATHS_TABLE into PACK_FILE_OPENED. Called"
            " during game initialisation.\n\nNo params."
        ),
    )

    GetFileLengthInPackWithPackNb = Symbol(
        None,
        None,
        None,
        (
            "Call GetFileLengthInPack after looking up the global Pack archive by its"
            " number\n\nr0: pack file number\nr1: file number\nreturn: size of the file"
            " in bytes from the Pack Table of Content"
        ),
    )

    LoadFileInPackWithPackId = Symbol(
        None,
        None,
        None,
        (
            "Call LoadFileInPack after looking up the global Pack archive by its"
            " identifier\n\nr0: pack file identifier\nr1: [output] target buffer\nr2:"
            " file index\nreturn: number of read bytes (identical to the length of the"
            " pack from the Table of Content)"
        ),
    )

    AllocAndLoadFileInPack = Symbol(
        None,
        None,
        None,
        (
            "Allocate a file and load a file from the pack archive inside.\nThe data"
            " pointed by the pointer in the output need to be freed once is not needed"
            " anymore.\n\nr0: pack file identifier\nr1: file index\nr2: [output] result"
            " struct (will contain length and pointer)\nr3: allocation flags"
        ),
    )

    OpenPackFile = Symbol(
        None,
        None,
        None,
        (
            "Open a Pack file, to be read later. Initialise the output"
            " structure.\n\nr0: [output] pack file struct\nr1: file name"
        ),
    )

    GetFileLengthInPack = Symbol(
        None,
        None,
        None,
        (
            "Get the length of a file entry from a Pack archive\n\nr0: pack file"
            " struct\nr1: file index\nreturn: size of the file in bytes from the Pack"
            " Table of Content"
        ),
    )

    LoadFileInPack = Symbol(
        None,
        None,
        None,
        (
            "Load the indexed file from the Pack archive, itself loaded from the"
            " ROM.\n\nr0: pack file struct\nr1: [output] target buffer\nr2: file"
            " index\nreturn: number of read bytes (identical to the length of the pack"
            " from the Table of Content)"
        ),
    )

    GetDamageSource = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Likely a linker-generated veneer for GetItemCategory.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " Item ID\nreturn: Category ID"
        ),
    )

    GetItemMoveId16 = Symbol(
        None,
        None,
        None,
        (
            "Wraps GetItemMoveId, ensuring that the return value is 16-bit.\n\nr0: item"
            " ID\nreturn: move ID"
        ),
    )

    IsThrownItem = Symbol(
        None,
        None,
        None,
        (
            "Checks if a given item ID is a thrown item (CATEGORY_THROWN_LINE or"
            " CATEGORY_THROWN_ARC).\n\nr0: item ID\nreturn: bool"
        ),
    )

    IsNotMoney = Symbol(
        None,
        None,
        None,
        "Checks if an item ID is not ITEM_POKE.\n\nr0: item ID\nreturn: bool",
    )

    IsEdible = Symbol(
        None,
        None,
        None,
        (
            "Checks if an item has an item category of CATEGORY_BERRIES_SEEDS_VITAMINS"
            " or CATEGORY_FOOD_GUMMIES.\n\nr0: item ID\nreturn: bool"
        ),
    )

    IsHM = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: bool",
    )

    IsGummi = Symbol(
        None, None, None, "Checks if an item is a Gummi.\n\nr0: item ID\nreturn: bool"
    )

    IsAuraBow = Symbol(
        None,
        None,
        None,
        (
            "Checks if an item is one of the aura bows received at the start of the"
            " game.\n\nr0: item ID\nreturn: bool"
        ),
    )

    InitItem = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Wrapper around InitItem with quantity set to 0.\n\nr0: pointer to item to"
            " initialize\nr1: item ID\nr2: sticky flag"
        ),
    )

    GetDisplayedBuyPrice = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item\nreturn: buy price",
    )

    GetDisplayedSellPrice = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item\nreturn: sell price",
    )

    GetActualBuyPrice = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item\nreturn: buy price",
    )

    GetActualSellPrice = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item\nreturn: sell price",
    )

    FindItemInInventory = Symbol(
        None,
        None,
        None,
        (
            "Returns x if item_id is at position x in the bag\nReturns 0x8000+x if"
            " item_id is at position x in storage\nReturns -1 if item is not"
            " found\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " item_id\nreturn: inventory index"
        ),
    )

    SprintfStatic = Symbol(
        None,
        None,
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

    ItemZInit = Symbol(None, None, None, "Zero-initializes an item struct.\n\nr0: item")

    WriteItemsToSave = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: start_address\nr1:"
            " total_length\nreturn: ?"
        ),
    )

    ReadItemsFromSave = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: start_address\nr1:"
            " total_length\nreturn: ?"
        ),
    )

    IsItemAvailableInDungeonGroup = Symbol(
        None,
        None,
        None,
        (
            "Checks one specific bit from table [NA]2094D34\n\nNote: unverified, ported"
            " from Irdkwia's notes\n\nr0: dungeon ID\nr1: item ID\nreturn: bool"
        ),
    )

    GetItemIdFromList = Symbol(
        None,
        None,
        None,
        (
            "category_num and item_num are numbers in range 0-10000\n\nNote:"
            " unverified, ported from Irdkwia's notes\n\nr0: list_id\nr1:"
            " category_num\nr2: item_num\nreturn: item ID"
        ),
    )

    NormalizeTreasureBox = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn:"
            " normalized item ID"
        ),
    )

    RemoveEmptyItems = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: list_pointer\nr1: size",
    )

    LoadItemPspi2n = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    GetExclusiveItemType = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: ?",
    )

    GetExclusiveItemOffsetEnsureValid = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        "Checks if an item ID is valid(?).\n\nr0: item ID\nreturn: bool",
    )

    GetExclusiveItemParameter = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: ?",
    )

    GetItemCategory = Symbol(
        None,
        None,
        None,
        (
            "Returns the category of the specified item\n\nr0: Item ID\nreturn: Item"
            " category"
        ),
    )

    EnsureValidItem = Symbol(
        None,
        None,
        None,
        (
            "Checks if the given item ID is valid (using IsItemValid). If so, return"
            " the given item ID. Otherwise, return ITEM_PLAIN_SEED.\n\nr0: item"
            " ID\nreturn: valid item ID"
        ),
    )

    GetItemName = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: item"
            " name"
        ),
    )

    GetItemNameFormatted = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output] name\nr1:"
            " item_id\nr2: flag\nr3: flag2"
        ),
    )

    GetItemBuyPrice = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: buy"
            " price"
        ),
    )

    GetItemSellPrice = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: sell"
            " price"
        ),
    )

    GetItemSpriteId = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn:"
            " sprite ID"
        ),
    )

    GetItemPaletteId = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn:"
            " palette ID"
        ),
    )

    GetItemActionName = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn:"
            " action name ID"
        ),
    )

    GetThrownItemQuantityLimit = Symbol(
        None,
        None,
        None,
        (
            "Get the minimum or maximum quantity for a given thrown item ID.\n\nr0:"
            " item ID\nr1: 0 for minimum, 1 for maximum\nreturn: minimum/maximum"
            " quantity for the given item ID"
        ),
    )

    GetItemMoveId = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: move ID",
    )

    TestItemFlag0xE = Symbol(
        None,
        None,
        None,
        (
            "Tests bit 7 if r1 is 0, bit 6 if r1 is 1, bit 5 otherwise\n\nNote:"
            " unverified, ported from Irdkwia's notes\n\nr0: item ID\nr1:"
            " bit_id\nreturn: bool"
        ),
    )

    IsItemInTimeDarkness = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: bool",
    )

    IsItemValidVeneer = Symbol(
        None,
        None,
        None,
        (
            "Likely a linker-generated veneer for IsItemValid.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " item ID\nreturn: bool"
        ),
    )

    SetGold = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: new value",
    )

    GetGold = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: value",
    )

    SetMoneyCarried = Symbol(
        None,
        None,
        None,
        (
            "Sets the amount of money the player is carrying, clamping the value to the"
            " range [0, MAX_MONEY_CARRIED].\n\nr0: new value"
        ),
    )

    GetCurrentBagCapacity = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: bag capacity",
    )

    IsBagFull = Symbol(
        None,
        None,
        None,
        (
            "Implements SPECIAL_PROC_IS_BAG_FULL (see"
            " ScriptSpecialProcessCall).\n\nreturn: bool"
        ),
    )

    GetNbItemsInBag = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: # items",
    )

    CountNbItemsOfTypeInBag = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: count",
    )

    CountItemTypeInBag = Symbol(
        None,
        None,
        None,
        (
            "Implements SPECIAL_PROC_COUNT_ITEM_TYPE_IN_BAG (see"
            " ScriptSpecialProcessCall).\n\nIrdkwia's notes: Count also"
            " stackable\n\nr0: item ID\nreturn: number of items of the specified ID in"
            " the bag"
        ),
    )

    IsItemInBag = Symbol(
        None,
        None,
        None,
        "Checks if an item is in the player's bag.\n\nr0: item ID\nreturn: bool",
    )

    IsItemWithFlagsInBag = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nr1:"
            " flags\nreturn: bool"
        ),
    )

    IsItemInTreasureBoxes = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: bool",
    )

    IsHeldItemInBag = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item\nreturn: bool",
    )

    IsItemForSpecialSpawnInBag = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: bool",
    )

    HasStorableItems = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: bool",
    )

    GetItemIndex = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_ptr\nreturn: index",
    )

    GetEquivItemIndex = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_ptr\nreturn: index",
    )

    GetEquippedThrowableItem = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: index",
    )

    GetFirstUnequippedItemOfType = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: index",
    )

    CopyItemAtIdx = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: index\nr1: [output]"
            " item_ptr\nreturn: exists"
        ),
    )

    GetItemAtIdx = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: index\nreturn: item"
            " pointer"
        ),
    )

    RemoveEmptyItemsInBag = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    RemoveItemNoHole = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: index\nreturn: ?",
    )

    RemoveItem = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nr0: index"
    )

    RemoveHeldItemNoHole = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: held_index",
    )

    RemoveItemByIdAndStackNoHole = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_ptr\nreturn: ?",
    )

    RemoveEquivItem = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_ptr\nreturn: ?",
    )

    RemoveEquivItemNoHole = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_ptr\nreturn: ?",
    )

    DecrementStackItem = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_ptr\nreturn: ?",
    )

    RemoveItemNoHoleCheck = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: index\nreturn: ?",
    )

    RemoveFirstUnequippedItemOfType = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: ?",
    )

    RemoveAllItems = Symbol(
        None,
        None,
        None,
        (
            "WARNING! Does not remove from party items\n\nNote: unverified, ported from"
            " Irdkwia's notes"
        ),
    )

    RemoveAllItemsStartingAt = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nr0: index"
    )

    SpecialProcAddItemToBag = Symbol(
        None,
        None,
        None,
        (
            "Implements SPECIAL_PROC_ADD_ITEM_TO_BAG (see"
            " ScriptSpecialProcessCall).\n\nr0: pointer to an owned_item\nreturn: bool"
        ),
    )

    AddItemToBagNoHeld = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item_str\nreturn: ?",
    )

    AddItemToBag = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item_str\nr1:"
            " held_by\nreturn: ?"
        ),
    )

    ScriptSpecialProcess0x39 = Symbol(
        None,
        None,
        None,
        "Implements SPECIAL_PROC_0x39 (see ScriptSpecialProcessCall).\n\nreturn: bool",
    )

    CountItemTypeInStorage = Symbol(
        None,
        None,
        None,
        (
            "Implements SPECIAL_PROC_COUNT_ITEM_TYPE_IN_STORAGE (see"
            " ScriptSpecialProcessCall).\n\nr0: pointer to an owned_item\nreturn:"
            " number of items of the specified ID in storage"
        ),
    )

    RemoveItemsTypeInStorage = Symbol(
        None,
        None,
        None,
        (
            "Probably? Implements SPECIAL_PROC_0x2A (see"
            " ScriptSpecialProcessCall).\n\nr0: pointer to an owned_item\nreturn: bool"
        ),
    )

    AddItemToStorage = Symbol(
        None,
        None,
        None,
        (
            "Implements SPECIAL_PROC_ADD_ITEM_TO_STORAGE (see"
            " ScriptSpecialProcessCall).\n\nr0: pointer to an owned_item\nreturn: bool"
        ),
    )

    SetMoneyStored = Symbol(
        None,
        None,
        None,
        (
            "Sets the amount of money the player has stored in the Duskull Bank,"
            " clamping the value to the range [0, MAX_MONEY_STORED].\n\nr0: new value"
        ),
    )

    GetKecleonItems1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    GetKecleonItems2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    GetExclusiveItemOffset = Symbol(
        None,
        None,
        None,
        (
            "Gets the exclusive item offset, which is the item ID relative to that of"
            " the first exclusive item, the Prism Ruff.\n\nr0: item ID\nreturn: offset"
        ),
    )

    ApplyExclusiveItemStatBoosts = Symbol(
        None,
        None,
        None,
        (
            "Applies stat boosts from an exclusive item.\n\nr0: item ID\nr1: pointer to"
            " attack stat to modify\nr2: pointer to special attack stat to modify\nr3:"
            " pointer to defense stat to modify\nstack[0]: pointer to special defense"
            " stat to modify"
        ),
    )

    SetExclusiveItemEffect = Symbol(
        None,
        None,
        None,
        (
            "Sets the bit for an exclusive item effect.\n\nr0: pointer to the effects"
            " bitvector to modify\nr1: exclusive item effect ID"
        ),
    )

    ExclusiveItemEffectFlagTest = Symbol(
        None,
        None,
        None,
        (
            "Tests the exclusive item bitvector for a specific exclusive item"
            " effect.\n\nr0: the effects bitvector to test\nr1: exclusive item effect"
            " ID\nreturn: bool"
        ),
    )

    IsExclusiveItemIdForMonster = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nr1: monster"
            " ID\nr2: type ID 1\nr3: type ID 2\nreturn: bool"
        ),
    )

    IsExclusiveItemForMonster = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item\nr1: monster"
            " ID\nr2: type ID 1\nr3: type ID 2\nreturn: bool"
        ),
    )

    BagHasExclusiveItemTypeForMonster = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: excl_type\nr1:"
            " monster ID\nr2: type ID 1\nr3: type ID 2\nreturn: item ID"
        ),
    )

    ProcessGinsengOverworld = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: target\nr1: [output]"
            " move ID\nr2: [output] move boost\nreturn: boost"
        ),
    )

    ApplyGummiBoostsGroundMode = Symbol(
        None,
        None,
        None,
        (
            "Applies the IQ boosts from eating a Gummi to the target monster.\n\nr0:"
            " Pointer to something\nr1: Pointer to something\nr2: Pointer to"
            " something\nr3: Pointer to something\nstack[0]: ?\nstack[1]: ?\nstack[2]:"
            " Pointer to a buffer to store some result into"
        ),
    )

    LoadSynthBin = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    CloseSynthBin = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    GetSynthItem = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    LoadWazaP = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    LoadWazaP2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    UnloadCurrentWazaP = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    GetMoveName = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: move"
            " name"
        ),
    )

    FormatMoveString = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: string_buffer\nr1:"
            " move\nr2: type_print"
        ),
    )

    FormatMoveStringMore = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ???\nr1: ???\nr2:"
            " move\nr3: type_print"
        ),
    )

    InitMove = Symbol(
        None,
        None,
        None,
        (
            "Initializes a move info struct.\n\nThis sets f_exists and f_enabled_for_ai"
            " on the flags, the ID to the given ID, the PP to the max PP for the move"
            " ID, and the ginseng boost to 0.\n\nr0: pointer to move to initialize\nr1:"
            " move ID"
        ),
    )

    GetInfoMoveCheckId = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nr1: move ID",
    )

    GetInfoMoveGround = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: ground move\nr1: move ID",
    )

    GetMoveTargetAndRange = Symbol(
        None,
        None,
        None,
        (
            "Gets the move target-and-range field. See struct move_target_and_range in"
            " the C headers.\n\nr0: move pointer\nr1: AI flag (every move has two"
            " target-and-range fields, one for players and one for AI)\nreturn: move"
            " target and range"
        ),
    )

    GetMoveType = Symbol(
        None,
        None,
        None,
        "Gets the type of a move\n\nr0: Pointer to move data\nreturn: Type of the move",
    )

    GetMovesetLevelUpPtr = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn: ?",
    )

    IsInvalidMoveset = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_id\nreturn: bool",
    )

    GetMovesetHmTmPtr = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn: ?",
    )

    GetMovesetEggPtr = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn: ?",
    )

    GetMoveAiWeight = Symbol(
        None,
        None,
        None,
        (
            "Gets the AI weight of a move\n\nr0: Pointer to move data\nreturn: AI"
            " weight of the move"
        ),
    )

    GetMoveNbStrikes = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nreturn: # strikes",
    )

    GetMoveBasePower = Symbol(
        None,
        None,
        None,
        (
            "Gets the base power of a move from the move data table.\n\nr0: move"
            " pointer\nreturn: base power"
        ),
    )

    GetMoveBasePowerGround = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ground_move\nreturn:"
            " base power"
        ),
    )

    GetMoveAccuracyOrAiChance = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nreturn: base PP",
    )

    GetMaxPp = Symbol(
        None,
        None,
        None,
        (
            "Gets the maximum PP for a given move.\n\nIrkdwia's notes:"
            " GetMovePPWithBonus\n\nr0: move pointer\nreturn: max PP for the given"
            " move, capped at 99"
        ),
    )

    GetMoveMaxGinsengBoost = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nreturn: max"
            " ginseng boost"
        ),
    )

    GetMoveMaxGinsengBoostGround = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ground_move\nreturn:"
            " max ginseng boost"
        ),
    )

    GetMoveCritChance = Symbol(
        None,
        None,
        None,
        (
            "Gets the critical hit chance of a move.\n\nr0: move pointer\nreturn:"
            " critical hit chance"
        ),
    )

    IsThawingMove = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nreturn: bool",
    )

    IsAffectedByTaunt = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nBased on struct"
            " move_data, maybe this should be IsUsableWhileTaunted?\n\nr0:"
            " move\nreturn: bool"
        ),
    )

    GetMoveRangeId = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nreturn: range ID",
    )

    GetMoveActualAccuracy = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn:"
            " accuracy"
        ),
    )

    GetMoveBasePowerFromId = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: base"
            " power"
        ),
    )

    IsMoveRangeString19 = Symbol(
        None,
        None,
        None,
        (
            "Returns whether a move's range string is 19 ('User').\n\nr0: Move"
            " pointer\nreturn: True if the move's range string field has a value of 19."
        ),
    )

    GetMoveMessageFromId = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID?\nreturn: string",
    )

    GetNbMoves = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_str\nreturn:"
            " # moves"
        ),
    )

    GetMovesetIdx = Symbol(
        None,
        None,
        None,
        (
            "Returns the move position in the moveset if it is found, -1"
            " otherwise\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " moveset_str\nr1: move ID\nreturn: ?"
        ),
    )

    IsReflectedByMagicCoat = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    CanBeSnatched = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    FailsWhileMuzzled = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nCalled IsMouthMove in"
            " Irdkwia's notes, which presumably is relevant to the Muzzled"
            " status.\n\nr0: move ID\nreturn: bool"
        ),
    )

    IsSoundMove = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move\nreturn: bool",
    )

    IsRecoilMove = Symbol(
        None,
        None,
        None,
        (
            "Checks if the given move is a recoil move (affected by Reckless).\n\nr0:"
            " move ID\nreturn: bool"
        ),
    )

    AllManip1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    AllManip2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    ManipMoves1v1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    ManipMoves1v2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    ManipMoves2v1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    ManipMoves2v2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DungeonMoveToGroundMove = Symbol(
        None,
        None,
        None,
        (
            "Converts a struct move to a struct ground_move.\n\nr0: [output]"
            " ground_move\nr1: move"
        ),
    )

    GroundToDungeonMoveset = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output]"
            " moveset_dun_str\nr1: moveset_str"
        ),
    )

    DungeonToGroundMoveset = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output]"
            " moveset_str\nr1: moveset_dun_str"
        ),
    )

    GetInfoGroundMoveset = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_str\nr1:"
            " moves_id"
        ),
    )

    FindFirstFreeMovesetIdx = Symbol(
        None,
        None,
        None,
        (
            "Returns the first position of an empty move in the moveset if it is found,"
            " -1 otherwise\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " moveset_str\nreturn: index"
        ),
    )

    LearnMoves = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_str\nr1:"
            " moves_id"
        ),
    )

    CopyMoveTo = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: write_info\nr1:"
            " buffer_write"
        ),
    )

    CopyMoveFrom = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info\nr1:"
            " buffer_read"
        ),
    )

    CopyMovesetTo = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: write_info\nr1:"
            " buffer_write"
        ),
    )

    CopyMovesetFrom = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info\nr1:"
            " buffer_read"
        ),
    )

    Is2TurnsMove = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    IsRegularAttackOrProjectile = Symbol(
        None,
        None,
        None,
        (
            "Checks if a move ID is MOVE_REGULAR_ATTACK or MOVE_PROJECTILE.\n\nr0: move"
            " ID\nreturn: bool"
        ),
    )

    IsPunchMove = Symbol(
        None,
        None,
        None,
        (
            "Checks if the given move is a punch move (affected by Iron Fist).\n\nr0:"
            " move ID\nreturn: bool"
        ),
    )

    IsHealingWishOrLunarDance = Symbol(
        None,
        None,
        None,
        (
            "Checks if a move ID is MOVE_HEALING_WISH or MOVE_LUNAR_DANCE.\n\nr0: move"
            " ID\nreturn: bool"
        ),
    )

    IsCopyingMove = Symbol(
        None,
        None,
        None,
        (
            "Checks if a move ID is MOVE_MIMIC, MOVE_SKETCH, or MOVE_COPYCAT.\n\nr0:"
            " move ID\nreturn: bool"
        ),
    )

    IsTrappingMove = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    IsOneHitKoMove = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    IsNot2TurnsMoveOrSketch = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    IsRealMove = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: move ID\nreturn: bool",
    )

    IsMovesetValid = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_str\nreturn:"
            " bool"
        ),
    )

    IsRealMoveInTimeDarkness = Symbol(
        None,
        None,
        None,
        (
            "Seed Flare isn't a real move in Time/Darkness\n\nNote: unverified, ported"
            " from Irdkwia's notes\n\nr0: move ID\nreturn: bool"
        ),
    )

    IsMovesetValidInTimeDarkness = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_str\nreturn:"
            " bool"
        ),
    )

    GetFirstNotRealMoveInTimeDarkness = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_str\nreturn:"
            " index"
        ),
    )

    IsSameMove = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: moveset_dun_str\nr1:"
            " move_data_dun_str\nreturn: bool"
        ),
    )

    GetMoveCategory = Symbol(
        None,
        None,
        None,
        (
            "Gets a move's category (physical, special, status).\n\nr0: move"
            " ID\nreturn: move category enum"
        ),
    )

    GetPpIncrease = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nr1: IQ"
            " skills bitvector\nreturn: PP increase"
        ),
    )

    OpenWaza = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nr0: waza_id"
    )

    SelectWaza = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nr0: waza_id"
    )

    ManipBgmPlayback = Symbol(
        None,
        None,
        None,
        (
            "Uncertain. More like bgm1&2 end\n\nNote: unverified, ported from Irdkwia's"
            " notes"
        ),
    )

    SoundDriverReset = Symbol(
        None, None, None, "Uncertain.\n\nNote: unverified, ported from Irdkwia's notes"
    )

    LoadDseFile = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output] iovec\nr1:"
            " filename\nreturn: bytes read"
        ),
    )

    PlaySeLoad = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    PlayBgm = Symbol(None, None, None, "Note: unverified, ported from Irdkwia's notes")

    StopBgm = Symbol(None, None, None, "Note: unverified, ported from Irdkwia's notes")

    ChangeBgm = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    PlayBgm2 = Symbol(None, None, None, "Note: unverified, ported from Irdkwia's notes")

    StopBgm2 = Symbol(None, None, None, "Note: unverified, ported from Irdkwia's notes")

    ChangeBgm2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    PlayME = Symbol(None, None, None, "Note: unverified, ported from Irdkwia's notes")

    StopME = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: fade_out",
    )

    PlaySe = Symbol(None, None, None, "Note: unverified, ported from Irdkwia's notes")

    PlaySeFullSpec = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SeChangeVolume = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SeChangePan = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    StopSe = Symbol(None, None, None, "Note: unverified, ported from Irdkwia's notes")

    DeleteWanTableEntry = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: wan_table_ptr\nr1:"
            " wan_id"
        ),
    )

    FindWanTableEntry = Symbol(
        None,
        None,
        None,
        (
            "Appears to search in the given table (in practice always seems to be"
            " LOADED_WAN_TABLE_PTR) for an entry with the given file name.\n\nr0: table"
            " pointer\nr1: file name\nreturn: index of the found file, if found, or -1"
            " if not found"
        ),
    )

    GetLoadedWanTableEntry = Symbol(
        None,
        None,
        None,
        (
            "wan_id = -1 if it is not loaded\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: wan_table_ptr\nr1: bin_file_id\nr2: file_id\nreturn: wan_id"
        ),
    )

    LoadWanTableEntry = Symbol(
        None,
        None,
        None,
        (
            "Appears to load data from the given file (in practice always seems to be"
            " animation data), using previously loaded data in the given table (see"
            " FindWanTableEntry) if possible.\n\nr0: table pointer\nr1: file name\nr2:"
            " flags\nreturn: table index of the loaded data"
        ),
    )

    ReplaceWanFromBinFile = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: wan_table_ptr\nr1:"
            " wan_id\nr2: bin_file_id\nr3: file_id\nstack[0]: compressed"
        ),
    )

    DeleteWanTableEntryVeneer = Symbol(
        None,
        None,
        None,
        (
            "Likely a linker-generated veneer for DeleteWanTableEntry.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " wan_table_ptr\nr1: wan_id"
        ),
    )

    LoadWteFromRom = Symbol(
        None,
        None,
        None,
        (
            "Loads a SIR0-wrapped WTE file from ROM, and returns a handle to it\n\nr0:"
            " [output] pointer to wte handle\nr1: file path string\nr2: load file flags"
        ),
    )

    LoadWteFromFileDirectory = Symbol(
        None,
        None,
        None,
        (
            "Loads a SIR0-wrapped WTE file from a file directory, and returns a handle"
            " to it\n\nr0: [output] pointer to wte handle\nr1: file directory id\nr2:"
            " file index\nr3: malloc flags"
        ),
    )

    UnloadWte = Symbol(
        None,
        None,
        None,
        (
            "Frees the buffer used to store the WTE data in the handle, and sets both"
            " pointers to null\n\nr0: pointer to wte handle"
        ),
    )

    LoadWtuFromBin = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: bin_file_id\nr1:"
            " file_id\nr2: load_type\nreturn: ?"
        ),
    )

    ProcessWte = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: header_ptr\nr1:"
            " unk_pal\nr2: unk_tex\nr3: unk_tex_param"
        ),
    )

    HandleSir0Translation = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: sir0_ptr",
    )

    HandleSir0TranslationVeneer = Symbol(
        None,
        None,
        None,
        (
            "Likely a linker-generated veneer for HandleSir0Translation.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " [output] double pointer to beginning of data\nr1: pointer to source file"
            " buffer\nreturn: return code"
        ),
    )

    DecompressAtNormalVeneer = Symbol(
        None,
        None,
        None,
        (
            "Likely a linker-generated veneer for DecompressAtNormal.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " addr_decomp\nr1: expected_size\nr2: AT pointer\nreturn: ?"
        ),
    )

    DecompressAtNormal = Symbol(
        None,
        None,
        None,
        (
            "Overwrites r3 probably passed to match DecompressAtHalf's"
            " definition.\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " addr_decomp\nr1: expected_size\nr2: AT pointer\nreturn: ?"
        ),
    )

    DecompressAtHalf = Symbol(
        None,
        None,
        None,
        (
            "Same as DecompressAtNormal, except it stores each nibble as a byte\nand"
            " adds the high nibble (r3).\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: addr_decomp\nr1: expected_size\nr2: AT pointer\nr3:"
            " high_nibble\nreturn: ?"
        ),
    )

    DecompressAtFromMemoryPointerVeneer = Symbol(
        None,
        None,
        None,
        (
            "Likely a linker-generated veneer for DecompressAtFromMemoryPointer.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " addr_decomp\nr1: expected_size\nr2: AT pointer\nreturn: ?"
        ),
    )

    DecompressAtFromMemoryPointer = Symbol(
        None,
        None,
        None,
        (
            "Overwrites r3 probably passed to match DecompressAtHalf's"
            " definition.\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " addr_decomp\nr1: expected_size\nr2: AT pointer\nreturn: ?"
        ),
    )

    WriteByteFromMemoryPointer = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nr0: byte"
    )

    GetAtSize = Symbol(
        None,
        None,
        None,
        (
            "Doesn't work for AT3PX and AT4PN\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: AT pointer\nr1: ?\nreturn: ?"
        ),
    )

    GetLanguageType = Symbol(
        None,
        None,
        None,
        (
            "Gets the language type.\n\nThis is the value backing the special"
            " LANGUAGE_TYPE script variable.\n\nreturn: language type"
        ),
    )

    GetLanguage = Symbol(
        None,
        None,
        None,
        (
            "Gets the single-byte language ID of the current program.\n\nThe language"
            " ID appears to be used to index some global tables.\n\nreturn: language ID"
        ),
    )

    StrcmpTag = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: s1\nr1: s2\nreturn: bool",
    )

    StoiTag = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: s\nreturn: int",
    )

    AnalyzeText = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nreturn: ?",
    )

    PreprocessString = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Calls PreprocessString after resolving the given message ID to a"
            " string.\n\nr0: [output] formatted string\nr1: maximum capacity of the"
            " output buffer\nr2: message ID\nr3: preprocessor flags\nstack[0]: pointer"
            " to preprocessor args"
        ),
    )

    InitPreprocessorArgs = Symbol(
        None,
        None,
        None,
        "Initializes a struct preprocess_args.\n\nr0: preprocessor args pointer",
    )

    SetStringAccuracy = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SetStringPower = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SetQuestionMarks = Symbol(
        None,
        None,
        None,
        (
            "Fills the buffer with the string '???'\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: buffer"
        ),
    )

    StrcpySimple = Symbol(
        None,
        None,
        None,
        (
            "A simple implementation of the strcpy(3) C library function.\n\nThis"
            " function was probably manually implemented by the developers. See Strcpy"
            " for what's probably the real libc function.\n\nr0: dest\nr1: src"
        ),
    )

    StrncpySimple = Symbol(
        None,
        None,
        None,
        (
            "A simple implementation of the strncpy(3) C library function.\n\nThis"
            " function was probably manually implemented by the developers. See Strncpy"
            " for what's probably the real libc function.\n\nr0: dest\nr1: src\nr2: n"
        ),
    )

    StrncpySimpleNoPad = Symbol(
        None,
        None,
        None,
        (
            "Similar to StrncpySimple, but does not zero-pad the end of dest beyond the"
            " null-terminator.\n\nr0: dest\nr1: src\nr2: n"
        ),
    )

    StrncmpSimple = Symbol(
        None,
        None,
        None,
        (
            "A simple implementation of the strncmp(3) C library function.\n\nThis"
            " function was probably manually implemented by the developers. See Strncmp"
            " for what's probably the real libc function.\n\nr0: s1\nr1: s2\nr2:"
            " n\nreturn: comparison value"
        ),
    )

    StrncpySimpleNoPadSafe = Symbol(
        None,
        None,
        None,
        (
            "Like StrncpySimpleNoPad, except there's a useless check on that each"
            " character is less than 0x100 (which is impossible for the result of a"
            " ldrb instruction).\n\nr0: dest\nr1: src\nr2: n"
        ),
    )

    SpecialStrcpy = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dst\nr1: src",
    )

    GetStringFromFile = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: Buffer\nr1: String ID",
    )

    LoadStringFile = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    GetStringFromFileVeneer = Symbol(
        None,
        None,
        None,
        (
            "Likely a linker-generated veneer for GetStringFromFile.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " Buffer\nr1: String ID"
        ),
    )

    StringFromMessageId = Symbol(
        None,
        None,
        None,
        (
            "Gets the string corresponding to a given message ID.\n\nr0: message"
            " ID\nreturn: string from the string files with the given message ID"
        ),
    )

    CopyStringFromMessageId = Symbol(
        None,
        None,
        None,
        (
            "Gets the string corresponding to a given message ID and copies it to the"
            " buffer specified in r0.\n\nThis function won't write more than <buffer"
            " length> bytes.\n\nr0: Buffer\nr1: String ID\nr2: Buffer length"
        ),
    )

    LoadTblTalk = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    GetTalkLine = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0:"
            " personality_index\nr1: group_id\nr2: restrictions\nreturn: ?"
        ),
    )

    SetScreenWindowsColor = Symbol(
        None,
        None,
        None,
        (
            "Sets the palette of the frames of windows in the specified screen\n\nr0:"
            " palette index\nr1: is upper screen"
        ),
    )

    SetBothScreensWindowsColor = Symbol(
        None,
        None,
        None,
        (
            "Sets the palette of the frames of windows in both screens\n\nr0: palette"
            " index"
        ),
    )

    GetDialogBoxField0xC = Symbol(
        None,
        None,
        None,
        (
            "Gets field_0xc from the dialog box of the given ID.\n\nr0:"
            " dbox_id\nreturn: field_0xc"
        ),
    )

    Arm9LoadUnkFieldNa0x2029EC8 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nr0: id"
    )

    Arm9StoreUnkFieldNa0x2029ED8 = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nr1: value",
    )

    CreateNormalMenu = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0:"
            " layout_struct_ptr\nr1: menu_flags\nr2: additional_info_ptr\nr3:"
            " menu_struct_ptr\nstack[0]: option_id\nreturn: menu_id"
        ),
    )

    FreeNormalMenu = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id"
    )

    IsNormalMenuActive = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id\nreturn: bool",
    )

    GetNormalMenuResult = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id\nreturn: ?",
    )

    CreateAdvancedMenu = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0:"
            " layout_struct_ptr\nr1: menu_flags\nr2: additional_info_ptr\nr3:"
            " entry_function\nstack[0]: nb_options\nstack[1]: nb_opt_pp\nreturn:"
            " menu_id"
        ),
    )

    FreeAdvancedMenu = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id"
    )

    IsAdvancedMenuActive = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id\nreturn: bool",
    )

    GetAdvancedMenuCurrentOption = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id\nreturn: ?",
    )

    GetAdvancedMenuResult = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: menu_id\nreturn: ?",
    )

    CreateDBox = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0:"
            " layout_struct_ptr\nreturn: dbox_id"
        ),
    )

    FreeDBox = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id"
    )

    IsDBoxActive = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id\nreturn: bool",
    )

    ShowMessageInDBox = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id\nr1:"
            " preprocessor flags (see PreprocessString)\nr2: string_id\nr3: pointer to"
            " preprocessor args (see PreprocessString)"
        ),
    )

    ShowDBox = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id"
    )

    CreatePortraitBox = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ???\nr1: ???\nr2:"
            " ???\nreturn: dbox_id"
        ),
    )

    FreePortraitBox = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id"
    )

    ShowPortraitBox = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id\nr1:"
            " portrait_ptr"
        ),
    )

    HidePortraitBox = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nr0: dbox_id"
    )

    IsMenuOptionActive = Symbol(
        None,
        None,
        None,
        (
            "Called whenever a menu option is selected. Returns whether the option is"
            " active or not.\n\nr0: ?\nReturn: True if the menu option is enabled,"
            " false otherwise."
        ),
    )

    ShowKeyboard = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: MessageID\nr1:"
            " buffer1\nr2: ???\nr3: buffer2\nreturn: ?"
        ),
    )

    GetKeyboardStatus = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?"
    )

    GetKeyboardStringResult = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?"
    )

    PrintMoveOptionMenu = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    PrintIqSkillsMenu = Symbol(
        None,
        None,
        None,
        (
            "Draws the IQ skills menu for a certain monster.\n\nr0: Monster"
            " species\nr1: Pointer to bitarray where the enabled skills will be written"
            " when enabling or disabling them in the menu\nr2: Monster IQ\nr3: True if"
            " the monster is blinded"
        ),
    )

    GetNotifyNote = Symbol(
        None, None, None, "Returns the current value of NOTIFY_NOTE.\n\nreturn: bool"
    )

    SetNotifyNote = Symbol(
        None, None, None, "Sets NOTIFY_NOTE to the given value.\n\nr0: bool"
    )

    InitMainTeamAfterQuiz = Symbol(
        None,
        None,
        None,
        (
            "Implements SPECIAL_PROC_INIT_MAIN_TEAM_AFTER_QUIZ (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    ScriptSpecialProcess0x3 = Symbol(
        None,
        None,
        None,
        "Implements SPECIAL_PROC_0x3 (see ScriptSpecialProcessCall).\n\nNo params.",
    )

    ScriptSpecialProcess0x4 = Symbol(
        None,
        None,
        None,
        "Implements SPECIAL_PROC_0x4 (see ScriptSpecialProcessCall).\n\nNo params.",
    )

    ReadStringSave = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer"
    )

    CheckStringSave = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nreturn: bool",
    )

    WriteSaveFile = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: save_info\nr1:"
            " buffer\nr2: size\nreturn: status code"
        ),
    )

    ReadSaveFile = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: save_info\nr1:"
            " buffer\nr2: size\nreturn: status code"
        ),
    )

    CalcChecksum = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nr1: size",
    )

    CheckChecksum = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nr1:"
            " size\nreturn: check_ok"
        ),
    )

    NoteSaveBase = Symbol(
        None,
        None,
        None,
        (
            "Probably related to saving or quicksaving?\n\nThis function prints the"
            " debug message 'NoteSave Base %d %d' with some values. It's also the only"
            " place where GetRngSeed is called.\n\nr0: Irdkwia's notes: state"
            " ID\nothers: ?\nreturn: status code"
        ),
    )

    WriteQuickSaveInfo = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nr1: size",
    )

    ReadSaveHeader = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    NoteLoadBase = Symbol(
        None,
        None,
        None,
        (
            "Probably related to loading a save file or quicksave?\n\nThis function"
            " prints the debug message 'NoteLoad Base %d' with some value. It's also"
            " the only place where SetRngSeed is called.\n\nreturn: status code"
        ),
    )

    ReadQuickSaveInfo = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nr1:"
            " size\nreturn: status code"
        ),
    )

    GetGameMode = Symbol(
        None, None, None, "Gets the value of GAME_MODE.\n\nreturn: game mode"
    )

    InitScriptVariableValues = Symbol(
        None,
        None,
        None,
        (
            "Initialize the script variable values table (SCRIPT_VARS_VALUES).\n\nThe"
            " whole table is first zero-initialized. Then, all script variable values"
            " are first initialized to their defaults, after which some of them are"
            " overwritten with other hard-coded values.\n\nNo params."
        ),
    )

    InitEventFlagScriptVars = Symbol(
        None,
        None,
        None,
        (
            "Initializes an assortment of event flag script variables (see the code for"
            " an exhaustive list).\n\nNo params."
        ),
    )

    ZinitScriptVariable = Symbol(
        None,
        None,
        None,
        (
            "Zero-initialize the values of the given script variable.\n\nr0: pointer to"
            " the local variable table (only needed if id >= VAR_LOCAL0)\nr1: script"
            " variable ID"
        ),
    )

    LoadScriptVariableRaw = Symbol(
        None,
        None,
        None,
        (
            "Loads a script variable descriptor for a given ID.\n\nr0: [output] script"
            " variable descriptor pointer\nr1: pointer to the local variable table"
            " (doesn't need to be valid; just controls the output value pointer)\nr2:"
            " script variable ID"
        ),
    )

    LoadScriptVariableValue = Symbol(
        None,
        None,
        None,
        (
            "Loads the value of a script variable.\n\nr0: pointer to the local variable"
            " table (only needed if id >= VAR_LOCAL0)\nr1: script variable ID\nreturn:"
            " value"
        ),
    )

    LoadScriptVariableValueAtIndex = Symbol(
        None,
        None,
        None,
        (
            "Loads the value of a script variable at some index (for script variables"
            " that are arrays).\n\nr0: pointer to the local variable table (only needed"
            " if id >= VAR_LOCAL0)\nr1: script variable ID\nr2: value index for the"
            " given script var\nreturn: value"
        ),
    )

    SaveScriptVariableValue = Symbol(
        None,
        None,
        None,
        (
            "Saves the given value to a script variable.\n\nr0: pointer to local"
            " variable table (only needed if id >= VAR_LOCAL0)\nr1: script variable"
            " ID\nr2: value to save"
        ),
    )

    SaveScriptVariableValueAtIndex = Symbol(
        None,
        None,
        None,
        (
            "Saves the given value to a script variable at some index (for script"
            " variables that are arrays).\n\nr0: pointer to local variable table (only"
            " needed if id >= VAR_LOCAL0)\nr1: script variable ID\nr2: value index for"
            " the given script var\nr3: value to save"
        ),
    )

    LoadScriptVariableValueSum = Symbol(
        None,
        None,
        None,
        (
            "Loads the sum of all values of a given script variable (for script"
            " variables that are arrays).\n\nr0: pointer to the local variable table"
            " (only needed if id >= VAR_LOCAL0)\nr1: script variable ID\nreturn: sum of"
            " values"
        ),
    )

    LoadScriptVariableValueBytes = Symbol(
        None,
        None,
        None,
        (
            "Loads some number of bytes from the value of a given script"
            " variable.\n\nr0: script variable ID\nr1: [output] script variable value"
            " bytes\nr2: number of bytes to load"
        ),
    )

    SaveScriptVariableValueBytes = Symbol(
        None,
        None,
        None,
        (
            "Saves some number of bytes to the given script variable.\n\nr0: script"
            " variable ID\nr1: bytes to save\nr2: number of bytes"
        ),
    )

    ScriptVariablesEqual = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Saves event flag script variables (see the code for an exhaustive list) to"
            " their respective BACKUP script variables, but only in certain game"
            " modes.\n\nThis function prints the debug string 'EventFlag BackupGameMode"
            " %d' with the game mode.\n\nNo params."
        ),
    )

    DumpScriptVariableValues = Symbol(
        None,
        None,
        None,
        (
            "Runs EventFlagBackup, then copies the script variable values table"
            " (SCRIPT_VARS_VALUES) to the given pointer.\n\nr0: destination pointer for"
            " the data dump\nreturn: always 1"
        ),
    )

    RestoreScriptVariableValues = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Initializes most of the SCENARIO_* script variables (except"
            " SCENARIO_TALK_BIT_FLAG for some reason). Also initializes the"
            " PLAY_OLD_GAME variable.\n\nNo params."
        ),
    )

    SetScenarioScriptVar = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Gets the special episode type from the SPECIAL_EPISODE_TYPE script"
            " variable.\n\nreturn: special episode type"
        ),
    )

    HasPlayedOldGame = Symbol(
        None,
        None,
        None,
        "Returns the value of the VAR_PLAY_OLD_GAME script variable.\n\nreturn: bool",
    )

    GetPerformanceFlagWithChecks = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: flag_id\nreturn: ?",
    )

    GetScenarioBalance = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Saves scenario flag script variables (SCENARIO_SELECT,"
            " SCENARIO_MAIN_BIT_FLAG) to their respective BACKUP script variables, but"
            " only in certain game modes.\n\nThis function prints the debug string"
            " 'ScenarioFlag BackupGameMode %d' with the game mode.\n\nNo params."
        ),
    )

    InitWorldMapScriptVars = Symbol(
        None,
        None,
        None,
        (
            "Initializes the WORLD_MAP_* script variable values (IDs 0x55-0x57).\n\nNo"
            " params."
        ),
    )

    InitDungeonListScriptVars = Symbol(
        None,
        None,
        None,
        (
            "Initializes the DUNGEON_*_LIST script variable values (IDs"
            " 0x4f-0x54).\n\nNo params."
        ),
    )

    SetDungeonConquest = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nr1:"
            " bit_value"
        ),
    )

    CheckDungeonOpen = Symbol(
        None,
        None,
        None,
        (
            "Related to dungeon open list\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: dungeon ID\nreturn: status code?"
        ),
    )

    GlobalProgressAlloc = Symbol(
        None,
        None,
        None,
        (
            "Allocates a new global progress struct.\n\nThis updates the global pointer"
            " and returns a copy of that pointer.\n\nreturn: pointer to a newly"
            " allocated global progress struct"
        ),
    )

    ResetGlobalProgress = Symbol(
        None, None, None, "Zero-initializes the global progress struct.\n\nNo params."
    )

    SetMonsterFlag1 = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID",
    )

    GetMonsterFlag1 = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn: ?",
    )

    SetMonsterFlag2 = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID",
    )

    HasMonsterBeenAttackedInDungeons = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        "Marks a dungeon tip as already shown to the player\n\nr0: Dungeon tip ID",
    )

    GetDungeonTipShown = Symbol(
        None,
        None,
        None,
        (
            "Checks if a dungeon tip has already been shown before or not.\n\nr0:"
            " Dungeon tip ID\nreturn: True if the tip has been shown before, false"
            " otherwise."
        ),
    )

    SetMaxReachedFloor = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nr1: max"
            " floor"
        ),
    )

    GetMaxReachedFloor = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn:"
            " max floor"
        ),
    )

    IncrementNbAdventures = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    GetNbAdventures = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: # adventures",
    )

    CanMonsterSpawn = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID",
    )

    CopyProgressInfoTo = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: write_info\nothers: ?",
    )

    CopyProgressInfoFromScratchTo = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: start_address\nr1:"
            " total_length\nreturn: ?"
        ),
    )

    CopyProgressInfoFrom = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info",
    )

    CopyProgressInfoFromScratchFrom = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: start_address\nr1:"
            " total_length"
        ),
    )

    SetPortraitMonsterId = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: portrait_ptr\nr1:"
            " monster ID"
        ),
    )

    SetPortraitExpressionId = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: portrait_ptr\nr1:"
            " expression_id"
        ),
    )

    SetPortraitUnknownAttr = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: portrait_ptr\nr1: attr",
    )

    SetPortraitAttrStruct = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: portrait_ptr\nr1:"
            " attr_ptr"
        ),
    )

    LoadPortrait = Symbol(
        None,
        None,
        None,
        (
            "If buffer_portrait is null, it only checks if it exists\n\nNote:"
            " unverified, ported from Irdkwia's notes\n\nr0: portrait_ptr\nr1:"
            " buffer_portrait\nreturn: exists"
        ),
    )

    GetNbFloors = Symbol(
        None,
        None,
        None,
        (
            "Returns the number of floors of the given dungeon.\n\nThe result is"
            " hardcoded for certain dungeons, such as dojo mazes.\n\nr0: Dungeon"
            " ID\nreturn: Number of floors"
        ),
    )

    GetNbFloorsPlusOne = Symbol(
        None,
        None,
        None,
        (
            "Returns the number of floors of the given dungeon + 1.\n\nr0: Dungeon"
            " ID\nreturn: Number of floors + 1"
        ),
    )

    GetDungeonGroup = Symbol(
        None,
        None,
        None,
        (
            "Returns the dungeon group associated to the given dungeon.\n\nFor IDs"
            " greater or equal to dungeon_id::DUNGEON_NORMAL_FLY_MAZE, returns"
            " dungeon_group_id::DGROUP_MAROWAK_DOJO.\n\nr0: Dungeon ID\nreturn:"
            " Group ID"
        ),
    )

    GetNbPrecedingFloors = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Returns the total amount of floors among all the dungeons in the dungeon"
            " group of the specified dungeon.\n\nr0: Dungeon ID\nreturn: Total number"
            " of floors in the group of the specified dungeon"
        ),
    )

    DungeonFloorToGroupFloor = Symbol(
        None,
        None,
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
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SetAdventureLogStructLocation = Symbol(
        None,
        None,
        None,
        (
            "Sets the location of the adventure log struct in memory.\n\nSets it in a"
            " static memory location (At 0x22AB69C [US], 0x22ABFDC [EU], 0x22ACE58"
            " [JP])\n\nNo params."
        ),
    )

    SetAdventureLogDungeonFloor = Symbol(
        None,
        None,
        None,
        "Sets the current dungeon floor pair.\n\nr0: struct dungeon_floor_pair",
    )

    GetAdventureLogDungeonFloor = Symbol(
        None,
        None,
        None,
        "Gets the current dungeon floor pair.\n\nreturn: struct dungeon_floor_pair",
    )

    ClearAdventureLogStruct = Symbol(
        None, None, None, "Clears the adventure log structure.\n\nNo params."
    )

    SetAdventureLogCompleted = Symbol(
        None,
        None,
        None,
        "Marks one of the adventure log entry as completed.\n\nr0: entry ID",
    )

    IsAdventureLogNotEmpty = Symbol(
        None,
        None,
        None,
        (
            "Checks if at least one of the adventure log entries is"
            " completed.\n\nreturn: bool"
        ),
    )

    GetAdventureLogCompleted = Symbol(
        None,
        None,
        None,
        "Checks if one adventure log entry is completed.\n\nr0: entry ID\nreturn: bool",
    )

    IncrementNbDungeonsCleared = Symbol(
        None,
        None,
        None,
        (
            "Increments by 1 the number of dungeons cleared.\n\nImplements"
            " SPECIAL_PROC_0x3A (see ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    GetNbDungeonsCleared = Symbol(
        None,
        None,
        None,
        (
            "Gets the number of dungeons cleared.\n\nreturn: the number of dungeons"
            " cleared"
        ),
    )

    IncrementNbFriendRescues = Symbol(
        None,
        None,
        None,
        "Increments by 1 the number of successful friend rescues.\n\nNo params.",
    )

    GetNbFriendRescues = Symbol(
        None,
        None,
        None,
        (
            "Gets the number of successful friend rescues.\n\nreturn: the number of"
            " successful friend rescues"
        ),
    )

    IncrementNbEvolutions = Symbol(
        None, None, None, "Increments by 1 the number of evolutions.\n\nNo params."
    )

    GetNbEvolutions = Symbol(
        None,
        None,
        None,
        "Gets the number of evolutions.\n\nreturn: the number of evolutions",
    )

    IncrementNbSteals = Symbol(
        None,
        None,
        None,
        (
            "Leftover from Time & Darkness. Does not do anything.\n\nCalls to this"
            " matches the ones for incrementing the number of successful steals in Time"
            " & Darkness.\n\nNo params."
        ),
    )

    IncrementNbEggsHatched = Symbol(
        None, None, None, "Increments by 1 the number of eggs hatched.\n\nNo params."
    )

    GetNbEggsHatched = Symbol(
        None,
        None,
        None,
        "Gets the number of eggs hatched.\n\nreturn: the number of eggs hatched",
    )

    GetNbPokemonJoined = Symbol(
        None,
        None,
        None,
        (
            "Gets the number of different pokémon that joined.\n\nreturn: the number of"
            " different pokémon that joined"
        ),
    )

    GetNbMovesLearned = Symbol(
        None,
        None,
        None,
        (
            "Gets the number of different moves learned.\n\nreturn: the number of"
            " different moves learned"
        ),
    )

    SetVictoriesOnOneFloor = Symbol(
        None,
        None,
        None,
        "Sets the record of victories on one floor.\n\nr0: the new record of victories",
    )

    GetVictoriesOnOneFloor = Symbol(
        None,
        None,
        None,
        "Gets the record of victories on one floor.\n\nreturn: the record of victories",
    )

    SetPokemonJoined = Symbol(
        None, None, None, "Marks one pokémon as joined.\n\nr0: monster ID"
    )

    SetPokemonBattled = Symbol(
        None, None, None, "Marks one pokémon as battled.\n\nr0: monster ID"
    )

    GetNbPokemonBattled = Symbol(
        None,
        None,
        None,
        (
            "Gets the number of different pokémon that battled against you.\n\nreturn:"
            " the number of different pokémon that battled against you"
        ),
    )

    IncrementNbBigTreasureWins = Symbol(
        None,
        None,
        None,
        (
            "Increments by 1 the number of big treasure wins.\n\nImplements"
            " SPECIAL_PROC_0x3B (see ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    SetNbBigTreasureWins = Symbol(
        None,
        None,
        None,
        (
            "Sets the number of big treasure wins.\n\nr0: the new number of big"
            " treasure wins"
        ),
    )

    GetNbBigTreasureWins = Symbol(
        None,
        None,
        None,
        (
            "Gets the number of big treasure wins.\n\nreturn: the number of big"
            " treasure wins"
        ),
    )

    SetNbRecycled = Symbol(
        None,
        None,
        None,
        "Sets the number of items recycled.\n\nr0: the new number of items recycled",
    )

    GetNbRecycled = Symbol(
        None,
        None,
        None,
        "Gets the number of items recycled.\n\nreturn: the number of items recycled",
    )

    IncrementNbSkyGiftsSent = Symbol(
        None,
        None,
        None,
        (
            "Increments by 1 the number of sky gifts sent.\n\nImplements"
            " SPECIAL_PROC_SEND_SKY_GIFT_TO_GUILDMASTER (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    SetNbSkyGiftsSent = Symbol(
        None,
        None,
        None,
        "Sets the number of Sky Gifts sent.\n\nreturn: the number of Sky Gifts sent",
    )

    GetNbSkyGiftsSent = Symbol(
        None,
        None,
        None,
        "Gets the number of Sky Gifts sent.\n\nreturn: the number of Sky Gifts sent",
    )

    ComputeSpecialCounters = Symbol(
        None,
        None,
        None,
        (
            "Computes the counters from the bit fields in the adventure log, as they"
            " are not updated automatically when bit fields are altered.\n\nAffects"
            " GetNbPokemonJoined, GetNbMovesLearned, GetNbPokemonBattled and"
            " GetNbItemAcquired.\n\nNo params."
        ),
    )

    RecruitSpecialPokemonLog = Symbol(
        None,
        None,
        None,
        (
            "Marks a specified special pokémon as recruited in the adventure"
            " log.\n\nIrdkwia's notes: Useless in Sky\n\nr0: monster ID"
        ),
    )

    IncrementNbFainted = Symbol(
        None,
        None,
        None,
        "Increments by 1 the number of times you fainted.\n\nNo params.",
    )

    GetNbFainted = Symbol(
        None,
        None,
        None,
        (
            "Gets the number of times you fainted.\n\nreturn: the number of times you"
            " fainted"
        ),
    )

    SetItemAcquired = Symbol(
        None, None, None, "Marks one specific item as acquired.\n\nr0: item"
    )

    GetNbItemAcquired = Symbol(
        None,
        None,
        None,
        "Gets the number of items acquired.\n\nreturn: the number of items acquired",
    )

    SetChallengeLetterCleared = Symbol(
        None, None, None, "Sets a challenge letter as cleared.\n\nr0: challenge ID"
    )

    GetSentryDutyGamePoints = Symbol(
        None,
        None,
        None,
        (
            "Gets the points for the associated rank in the footprints minigame.\n\nr0:"
            " the rank (range 0-4, 1st to 5th)\nreturn: points"
        ),
    )

    SetSentryDutyGamePoints = Symbol(
        None,
        None,
        None,
        (
            "Sets a new record in the footprints minigame.\n\nr0: points\nreturn: the"
            " rank (range 0-4, 1st to 5th; -1 if out of ranking)"
        ),
    )

    CopyLogTo = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: write_info",
    )

    CopyLogFrom = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info",
    )

    GetAbilityString = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nr1: ability ID",
    )

    GetAbilityDescStringId = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ability ID\nreturn:"
            " string ID"
        ),
    )

    GetTypeStringId = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: type ID\nreturn:"
            " string ID"
        ),
    )

    CopyBitsTo = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: write_info\nr1:"
            " buffer_write\nr2: nb_bits"
        ),
    )

    CopyBitsFrom = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info\nr1:"
            " buffer_read\nr2: nb_bits"
        ),
    )

    StoreDefaultTeamName = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    GetTeamNameCheck = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer"
    )

    GetTeamName = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer"
    )

    SetTeamName = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer"
    )

    SubFixedPoint = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Compute the ceiling of a decimal fixed-point number (16 fraction"
            " bits).\n\nNumbers are in the format {16-bit integer part, 16-bit"
            " thousandths}, where the integer part is the lower word. Probably used"
            " primarily for belly.\n\nr0: number\nreturn: ceil(number)"
        ),
    )

    DungeonGoesUp = Symbol(
        None,
        None,
        None,
        (
            "Returns whether the specified dungeon is considered as going upward or"
            " not\n\nr0: dungeon id\nreturn: bool"
        ),
    )

    GetTurnLimit = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn:"
            " turn limit"
        ),
    )

    DoesNotSaveWhenEntering = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    TreasureBoxDropsEnabled = Symbol(
        None,
        None,
        None,
        (
            "Checks if enemy Treasure Box drops are enabled in the dungeon.\n\nr0:"
            " dungeon ID\nreturn: bool"
        ),
    )

    IsLevelResetDungeon = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    GetMaxItemsAllowed = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn:"
            " max items allowed"
        ),
    )

    IsMoneyAllowed = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    GetMaxRescueAttempts = Symbol(
        None,
        None,
        None,
        (
            "Returns the maximum rescue attempts allowed in the specified"
            " dungeon.\n\nr0: dungeon id\nreturn: Max rescue attempts, or -1 if rescues"
            " are disabled."
        ),
    )

    IsRecruitingAllowed = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    GetLeaderChangeFlag = Symbol(
        None,
        None,
        None,
        (
            "Returns true if the flag that allows changing leaders is set in the"
            " restrictions of the specified dungeon\n\nr0: dungeon id\nreturn: True if"
            " the restrictions of the current dungeon allow changing leaders, false"
            " otherwise."
        ),
    )

    GetUnknownDungeonOption = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: ?",
    )

    CanEnemyEvolve = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    GetMaxMembersAllowed = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn:"
            " max members allowed"
        ),
    )

    IsIqEnabled = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    IsTrapInvisibleWhenAttacking = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID\nreturn: bool",
    )

    JoinedAtRangeCheck = Symbol(
        None,
        None,
        None,
        (
            "Returns whether a certain joined_at field value is between"
            " dungeon_id::DUNGEON_JOINED_AT_BIDOOF and"
            " dungeon_id::DUNGEON_DUMMY_0xE3.\n\nIrdkwia's notes:"
            " IsSupportPokemon\n\nr0: joined_at id\nreturn: bool"
        ),
    )

    IsDojoDungeon = Symbol(
        None,
        None,
        None,
        (
            "Checks if the given dungeon is a Marowak Dojo dungeon.\n\nr0: dungeon"
            " ID\nreturn: bool"
        ),
    )

    IsFutureDungeon = Symbol(
        None,
        None,
        None,
        (
            "Checks if the given dungeon is a dungeon in the future arc of the main"
            " story.\n\nr0: dungeon ID\nreturn: bool"
        ),
    )

    IsSpecialEpisodeDungeon = Symbol(
        None,
        None,
        None,
        (
            "Checks if the given dungeon is a special episode dungeon.\n\nr0: dungeon"
            " ID\nreturn: bool"
        ),
    )

    RetrieveFromItemList1 = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon_info\nr1:"
            " ?\nreturn: ?"
        ),
    )

    IsForbiddenFloor = Symbol(
        None,
        None,
        None,
        (
            "Related to missions floors forbidden\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: dungeon_info\nothers: ?\nreturn: bool"
        ),
    )

    Copy16BitsFrom = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info\nr1:"
            " buffer_read"
        ),
    )

    RetrieveFromItemList2 = Symbol(
        None,
        None,
        None,
        (
            "Same as RetrieveFromItemList1, except there is one more"
            " comparison\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " dungeon_info"
        ),
    )

    IsInvalidForMission = Symbol(
        None,
        None,
        None,
        (
            "It's a guess\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " dungeon_id\nreturn: bool"
        ),
    )

    IsExpEnabledInDungeon = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon_id\nreturn: bool",
    )

    IsSkyExclusiveDungeon = Symbol(
        None,
        None,
        None,
        (
            "Also the dungeons where Giratina has its Origin Form\n\nNote: unverified,"
            " ported from Irdkwia's notes\n\nr0: dungeon_id\nreturn: bool"
        ),
    )

    JoinedAtRangeCheck2 = Symbol(
        None,
        None,
        None,
        (
            "Returns whether a certain joined_at field value is equal to"
            " dungeon_id::DUNGEON_BEACH or is between dungeon_id::DUNGEON_DUMMY_0xEC"
            " and dungeon_id::DUNGEON_DUMMY_0xF0.\n\nIrdkwia's notes:"
            " IsSEPokemon\n\nr0: joined_at id\nreturn: bool"
        ),
    )

    GetBagCapacity = Symbol(
        None,
        None,
        None,
        (
            "Returns the player's bag capacity for a given point in the game.\n\nr0:"
            " scenario_balance\nreturn: bag capacity"
        ),
    )

    GetBagCapacitySpecialEpisode = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: se_type\nreturn: bag"
            " capacity"
        ),
    )

    GetRankUpEntry = Symbol(
        None,
        None,
        None,
        (
            "Gets the rank up data for the specified rank.\n\nr0: rank index\nreturn:"
            " struct rankup_table_entry*"
        ),
    )

    GetBgRegionArea = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: offset\nr1:"
            " subregion_id\nr2: region_id\nreturn: ?"
        ),
    )

    LoadMonsterMd = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    GetNameRaw = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dst_ptr\nr1: id",
    )

    GetName = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dst_ptr\nr1: id\nr2:"
            " color_id"
        ),
    )

    GetNameWithGender = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: dst_ptr\nr1: id\nr2:"
            " color_id"
        ),
    )

    GetSpeciesString = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dst_ptr\nr1: id",
    )

    GetNameString = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: name",
    )

    GetSpriteIndex = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: sprite index",
    )

    GetDexNumber = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: dex number",
    )

    GetCategoryString = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: category",
    )

    GetMonsterGender = Symbol(
        None,
        None,
        None,
        (
            "Returns the gender field of a monster given its ID.\n\nr0: monster"
            " id\nreturn: monster gender"
        ),
    )

    GetBodySize = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: body size",
    )

    GetSpriteSize = Symbol(
        None,
        None,
        None,
        (
            "Returns the sprite size of the specified monster. If the size is between 1"
            " and 6, 6 will be returned.\n\nr0: monster id\nreturn: sprite size"
        ),
    )

    GetSpriteFileSize = Symbol(
        None,
        None,
        None,
        (
            "Returns the sprite file size of the specified monster.\n\nr0: monster"
            " id\nreturn: sprite file size"
        ),
    )

    GetShadowSize = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: shadow size",
    )

    GetSpeedStatus = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: speed status",
    )

    GetMovementType = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: movement"
            " type"
        ),
    )

    GetRegenSpeed = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: regen speed",
    )

    GetCanMoveFlag = Symbol(
        None,
        None,
        None,
        (
            "Returns the flag that determines if a monster can move in dungeons.\n\nr0:"
            " Monster ID\nreturn: 'Can move' flag"
        ),
    )

    GetChanceAsleep = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: chance"
            " asleep"
        ),
    )

    GetLowKickMultiplier = Symbol(
        None,
        None,
        None,
        (
            "Gets the Low Kick (and Grass Knot) damage multiplier (i.e., weight) for"
            " the given species.\n\nr0: monster ID\nreturn: multiplier as a binary"
            " fixed-point number with 8 fraction bits."
        ),
    )

    GetSize = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: size",
    )

    GetBaseHp = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: base HP",
    )

    CanThrowItems = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: bool",
    )

    CanEvolve = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: bool",
    )

    GetMonsterPreEvolution = Symbol(
        None,
        None,
        None,
        (
            "Returns the pre-evolution id of a monster given its ID.\n\nr0: monster"
            " id\nreturn: ID of the monster that evolves into the one specified in r0"
        ),
    )

    GetBaseOffensiveStat = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nr1: stat"
            " index\nreturn: base attack/special attack stat"
        ),
    )

    GetBaseDefensiveStat = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nr1: stat"
            " index\nreturn: base defense/special defense stat"
        ),
    )

    GetType = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nr1: type index (0"
            " for primary type or 1 for secondary type)\nreturn: type"
        ),
    )

    GetAbility = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nr1: ability index"
            " (0 for primary ability or 1 for secondary ability)\nreturn: ability"
        ),
    )

    GetRecruitRate2 = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: recruit"
            " rate 2"
        ),
    )

    GetRecruitRate1 = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: recruit"
            " rate 1"
        ),
    )

    GetExp = Symbol(
        None,
        None,
        None,
        (
            "Base Formula = ((Level-1)*ExpYield)//10+ExpYield\nNote: Defeating an enemy"
            " without using a move will divide this amount by 2\n\nNote: unverified,"
            " ported from Irdkwia's notes\n\nr0: id\nr1: level\nreturn: exp"
        ),
    )

    GetEvoParameters = Symbol(
        None,
        None,
        None,
        (
            "Bx\nHas something to do with evolution\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: [output] struct_evo_param\nr1: id"
        ),
    )

    GetTreasureBoxChances = Symbol(
        None,
        None,
        None,
        (
            "Has something to do with bytes 3C-3E\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: id\nr1: [output] struct_chances"
        ),
    )

    GetIqGroup = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: IQ group",
    )

    GetSpawnThreshold = Symbol(
        None,
        None,
        None,
        (
            "Returns the spawn threshold of the given monster ID\n\nThe spawn threshold"
            " determines the minimum SCENARIO_BALANCE_FLAG value required by a monster"
            " to spawn in dungeons.\n\nr0: monster id\nreturn: Spawn threshold"
        ),
    )

    NeedsItemToSpawn = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: bool",
    )

    GetExclusiveItem = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nr1: determines"
            " which exclusive item\nreturn: exclusive item"
        ),
    )

    GetFamilyIndex = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: family index",
    )

    LoadM2nAndN2m = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    IsNotNickname = Symbol(
        None,
        None,
        None,
        (
            "Checks if the string_buffer matches the name of the species\n\nNote:"
            " unverified, ported from Irdkwia's notes\n\nr0: string_buffer\nr1: monster"
            " ID\nreturn: bool"
        ),
    )

    GetLvlStats = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output] level"
            " stats\nr1: monster ID\nr2: level"
        ),
    )

    GetEvoFamily = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: monster_str\nr1:"
            " evo_family_str\nreturn: nb_family"
        ),
    )

    GetEvolutions = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dmons_addr",
    )

    GetBaseForm = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: base form",
    )

    GetBaseFormCastformCherrimDeoxys = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: base form",
    )

    GetAllBaseForms = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: base form",
    )

    GetDexNumberVeneer = Symbol(
        None,
        None,
        None,
        (
            "Likely a linker-generated veneer for GetDexNumber.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " id\nreturn: dex number"
        ),
    )

    GetMonsterIdFromSpawnEntry = Symbol(
        None,
        None,
        None,
        (
            "Returns the monster ID of the specified monster spawn entry\n\nr0: Pointer"
            " to the monster spawn entry\nreturn: monster_spawn_entry::id"
        ),
    )

    SetMonsterId = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: mons_spawn_str\nr1:"
            " monster ID"
        ),
    )

    SetMonsterLevelAndId = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: mons_spawn_str\nr1:"
            " level\nr2: monster ID"
        ),
    )

    GetMonsterLevelFromSpawnEntry = Symbol(
        None,
        None,
        None,
        (
            "Returns the level of the specified monster spawn entry.\n\nr0: pointer to"
            " the monster spawn entry\nreturn: uint8_t"
        ),
    )

    GetMonsterGenderVeneer = Symbol(
        None,
        None,
        None,
        (
            "Likely a linker-generated veneer for GetMonsterGender.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " monster id\nreturn: monster gender"
        ),
    )

    IsMonsterValid = Symbol(
        None,
        None,
        None,
        "Checks if an monster ID is valid.\n\nr0: monster ID\nreturn: bool",
    )

    IsUnown = Symbol(
        None,
        None,
        None,
        "Checks if a monster ID is an Unown.\n\nr0: monster ID\nreturn: bool",
    )

    IsShaymin = Symbol(
        None,
        None,
        None,
        "Checks if a monster ID is a Shaymin form.\n\nr0: monster ID\nreturn: bool",
    )

    IsCastform = Symbol(
        None,
        None,
        None,
        "Checks if a monster ID is a Castform form.\n\nr0: monster ID\nreturn: bool",
    )

    IsCherrim = Symbol(
        None,
        None,
        None,
        "Checks if a monster ID is a Cherrim form.\n\nr0: monster ID\nreturn: bool",
    )

    IsDeoxys = Symbol(
        None,
        None,
        None,
        "Checks if a monster ID is a Deoxys form.\n\nr0: monster ID\nreturn: bool",
    )

    GetSecondFormIfValid = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn:"
            " second form"
        ),
    )

    FemaleToMaleForm = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: id\nreturn: base form",
    )

    BaseFormsEqual = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: id1\nr1: id2\nreturn:"
            " if the base forms are the same"
        ),
    )

    DexNumbersEqual = Symbol(
        None,
        None,
        None,
        (
            "Each Unown is considered as different\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: id1\nr1: id2\nreturn: bool"
        ),
    )

    GendersEqual = Symbol(
        None,
        None,
        None,
        (
            "Checks if the genders for two monster IDs are equal.\n\nr0: id1\nr1:"
            " id2\nreturn: bool"
        ),
    )

    GendersEqualNotGenderless = Symbol(
        None,
        None,
        None,
        (
            "Checks if the genders for two monster IDs are equal. Always returns false"
            " if either gender is GENDER_GENDERLESS.\n\nr0: id1\nr1: id2\nreturn: bool"
        ),
    )

    IsMonsterOnTeam = Symbol(
        None,
        None,
        None,
        (
            "Checks if a given monster is on the exploration team (not necessarily the"
            " active party)?\n\nIrdkwia's notes:\n  recruit_strategy=0: strict"
            " equality\n  recruit_strategy=1: relative equality\n\nr0: monster ID\nr1:"
            " recruit_strategy\nreturn: bool"
        ),
    )

    GetNbRecruited = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: recruit_str",
    )

    GetMember = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: member_idx\nreturn: ?",
    )

    GetHeroStrIdIfExists = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?"
    )

    GetPartnerStrIdIfExists = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?"
    )

    GetFirstTeamMemberStrIdIfExists = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?"
    )

    GetSecondTeamMemberStrIdIfExists = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?"
    )

    GetThirdTeamMemberStrIdIfExists = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?"
    )

    GetHeroData = Symbol(
        None,
        None,
        None,
        (
            "Returns the ground monster data of the hero (first slot in Chimecho"
            " Assembly)\n\nreturn: Monster data"
        ),
    )

    GetPartnerData = Symbol(
        None,
        None,
        None,
        (
            "Returns the ground monster data of the partner (second slot in Chimecho"
            " Assembly)\n\nreturn: Monster data"
        ),
    )

    GetFirstTeamMemberData = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: Monster data",
    )

    GetSecondTeamMemberData = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: Monster data",
    )

    GetThirdTeamMemberData = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: Monster data",
    )

    GetFirstEmptyRecruitSlot = Symbol(
        None,
        None,
        None,
        (
            "Returns -1 if there is none\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: ?\nreturn: ?"
        ),
    )

    CheckTeamMemberField8 = Symbol(
        None,
        None,
        None,
        (
            "Checks if a value obtained from team_member::field_0x8 is equal to certain"
            " values.\n\nThis is known to return true for some or all of the guest"
            " monsters.\n\nr0: Value read from team_member::field_0x8\nreturn: True if"
            " the value is equal to 0x55AA or 0x5AA5"
        ),
    )

    IsMonsterIdInNormalRange = Symbol(
        None,
        None,
        None,
        (
            "Checks if a monster ID is in the range [0, 554], meaning it's before the"
            " special story monster IDs and secondary gender IDs.\n\nr0: monster"
            " ID\nreturn: bool"
        ),
    )

    GetTeamMemberData = Symbol(
        None,
        None,
        None,
        (
            "Returns a struct containing information about a team member.\n\nIrdkwia's"
            " notes (note the discrepancy): GetEquivalentTeamID\n  r0: str_id\n "
            " return: team_id, -1 if not in team\n\nr0: Index\nreturn: Pointer to"
            " struct containing team member information"
        ),
    )

    GetTeamMember = Symbol(
        None,
        None,
        None,
        (
            "Null pointer if -1\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " team_id\nreturn: team member"
        ),
    )

    SetTeamSetupHeroAndPartnerOnly = Symbol(
        None,
        None,
        None,
        (
            "Implements SPECIAL_PROC_SET_TEAM_SETUP_HERO_AND_PARTNER_ONLY (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    SetTeamSetupHeroOnly = Symbol(
        None,
        None,
        None,
        (
            "Implements SPECIAL_PROC_SET_TEAM_SETUP_HERO_ONLY (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    GetPartyMembers = Symbol(
        None,
        None,
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
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    ClearItem = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: team_id\nr1: check",
    )

    ChangeGiratinaFormIfSkyDungeon = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: dungeon ID",
    )

    CanLearnIqSkill = Symbol(
        None,
        None,
        None,
        (
            "Returns whether an IQ skill can be learned with a given IQ amount or"
            " not.\n\nIf the specified amount is 0, it always returns false.\n\nr0: IQ"
            " amount\nr1: IQ skill\nreturn: True if the specified skill can be learned"
            " with the specified IQ amount."
        ),
    )

    GetLearnableIqSkills = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Disables an IQ skill.\n\nr0: Pointer to the bitarray containing the list"
            " of enabled IQ skills\nr1: ID of the skill to disable"
        ),
    )

    EnableIqSkill = Symbol(
        None,
        None,
        None,
        (
            "Enables an IQ skill and disables any other skills that are incompatible"
            " with it.\n\nr0: Pointer to the bitarray containing the list of enabled IQ"
            " skills\nr1: ID of the skill to enable"
        ),
    )

    GetSpeciesIqSkill = Symbol(
        None,
        None,
        None,
        (
            "Gets the <index>th skill on the list of IQ skills that a given monster"
            " species can learn.\n\nr0: Species ID\nr1: Index (starting at 0)\nreturn:"
            " IQ skill ID"
        ),
    )

    IqSkillFlagTest = Symbol(
        None,
        None,
        None,
        (
            "Tests whether an IQ skill with a given ID is active.\n\nr0: IQ skill"
            " bitvector to test\nr1: IQ skill ID\nreturn: bool"
        ),
    )

    GetNextIqSkill = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Returns the data of a monster sent into the Explorer Dojo using the"
            " 'exchange teams' option.\n\nr0: Entry number (0-3)\nreturn: Ground"
            " monster data of the specified entry"
        ),
    )

    WriteMonsterInfoToSave = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: start_address\nr1:"
            " total_length\nreturn: ?"
        ),
    )

    ReadMonsterInfoFromSave = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: start_address\nr1:"
            " total_length"
        ),
    )

    WriteMonsterToSave = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: write_info\nr1:"
            " ground_monster"
        ),
    )

    ReadMonsterFromSave = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: read_info\nr1:"
            " ground_monster"
        ),
    )

    GetEvolutionPossibilities = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ground_monster\nr1:"
            " evo_struct_addr"
        ),
    )

    GetMonsterEvoStatus = Symbol(
        None,
        None,
        None,
        (
            "evo_status = 0: Not possible now\nevo_status = 1: Possible now\nevo_status"
            " = 2: No further\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " ground_monster\nreturn: evo_status"
        ),
    )

    GetSosMailCount = Symbol(
        None,
        None,
        None,
        (
            "Implements SPECIAL_PROC_GET_SOS_MAIL_COUNT (see"
            " ScriptSpecialProcessCall).\n\nr0: ?\nr1: some flag?\nreturn: SOS mail"
            " count"
        ),
    )

    IsMissionValid = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: mission\nreturn: bool",
    )

    GenerateMission = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Generates the missions displayed on the Job Bulletin Board and the Outlaw"
            " Notice Board.\n\nNo params."
        ),
    )

    DungeonRequestsDone = Symbol(
        None,
        None,
        None,
        (
            "Seems to return the number of missions completed.\n\nPart of the"
            " implementation for SPECIAL_PROC_DUNGEON_HAD_REQUEST_DONE (see"
            " ScriptSpecialProcessCall).\n\nr0: ?\nr1: some flag?\nreturn: number of"
            " missions completed"
        ),
    )

    DungeonRequestsDoneWrapper = Symbol(
        None,
        None,
        None,
        (
            "Calls DungeonRequestsDone with the second argument set to false.\n\nr0:"
            " ?\nreturn: number of mission completed"
        ),
    )

    AnyDungeonRequestsDone = Symbol(
        None,
        None,
        None,
        (
            "Calls DungeonRequestsDone with the second argument set to true, and"
            " converts the integer output to a boolean.\n\nr0: ?\nreturn: bool: whether"
            " the number of missions completed is greater than 0"
        ),
    )

    GetAcceptedMission = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: mission_id\nreturn:"
            " mission"
        ),
    )

    GetMissionByTypeAndDungeon = Symbol(
        None,
        None,
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
        None,
        None,
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
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?"
    )

    DeleteAllPossibleMonstersList = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    GenerateAllPossibleDungeonsList = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?"
    )

    DeleteAllPossibleDungeonsList = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    GenerateAllPossibleDeliverList = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nreturn: ?"
    )

    DeleteAllPossibleDeliverList = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    ClearMissionData = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Calls CanMonsterBeUsedForMission with r1 = 1.\n\nr0: Monster ID\nreturn:"
            " Result of CanMonsterBeUsedForMission"
        ),
    )

    CanMonsterBeUsedForMission = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nr1:"
            " to_sky\nreturn: bool"
        ),
    )

    IsAvailableItem = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: item ID\nreturn: bool",
    )

    GetAvailableItemDeliveryList = Symbol(
        None,
        None,
        None,
        (
            "Uncertain.\n\nNote: unverified, ported from Irdkwia's notes\n\nr0:"
            " item_buffer\nreturn: nb_items"
        ),
    )

    GetActorMatchingStorageId = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: actor_id\nreturn:"
            " storage ID"
        ),
    )

    ScriptSpecialProcess0x3D = Symbol(
        None,
        None,
        None,
        "Implements SPECIAL_PROC_0x3D (see ScriptSpecialProcessCall).\n\nNo params.",
    )

    ScriptSpecialProcess0x3E = Symbol(
        None,
        None,
        None,
        "Implements SPECIAL_PROC_0x3E (see ScriptSpecialProcessCall).\n\nNo params.",
    )

    ScriptSpecialProcess0x17 = Symbol(
        None,
        None,
        None,
        "Implements SPECIAL_PROC_0x17 (see ScriptSpecialProcessCall).\n\nNo params.",
    )

    ItemAtTableIdx = Symbol(
        None,
        None,
        None,
        (
            "Gets info about the item at a given item table (not sure what this table"
            " is...) index.\n\nUsed by SPECIAL_PROC_COUNT_TABLE_ITEM_TYPE_IN_BAG and"
            " friends (see ScriptSpecialProcessCall).\n\nr0: table index\nr1: [output]"
            " pointer to an owned_item"
        ),
    )

    DungeonSwapIdToIdx = Symbol(
        None,
        None,
        None,
        (
            "Converts a dungeon ID to its corresponding index in DUNGEON_SWAP_ID_TABLE,"
            " or -1 if not found.\n\nr0: dungeon ID\nreturn: index"
        ),
    )

    DungeonSwapIdxToId = Symbol(
        None,
        None,
        None,
        (
            "Converts an index in DUNGEON_SWAP_ID_TABLE to the corresponding dungeon"
            " ID, or DUNGEON_DUMMY_0xFF if the index is -1.\n\nr0: index\nreturn:"
            " dungeon ID"
        ),
    )

    ResumeBgm = Symbol(
        None, None, None, "Uncertain.\n\nNote: unverified, ported from Irdkwia's notes"
    )

    FlushChannels = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    UpdateChannels = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    WaitForInterrupt = Symbol(
        None,
        None,
        None,
        (
            "Presumably blocks until the program receives an interrupt.\n\nThis just"
            " calls (in Ghidra terminology) coproc_moveto_Wait_for_interrupt(0). See"
            " https://en.wikipedia.org/wiki/ARM_architecture_family#Coprocessors.\n\nNo"
            " params."
        ),
    )

    FileInit = Symbol(
        None,
        None,
        None,
        (
            "Initializes a file_stream structure for file I/O.\n\nThis function must"
            " always be called before opening a file.\n\nr0: file_stream pointer"
        ),
    )

    Abs = Symbol(
        None,
        None,
        None,
        "Takes the absolute value of an integer.\n\nr0: x\nreturn: abs(x)",
    )

    Mbtowc = Symbol(
        None,
        None,
        None,
        (
            "The mbtowc(3) C library function.\n\nr0: pwc\nr1: s\nr2: n\nreturn: number"
            " of consumed bytes, or -1 on failure"
        ),
    )

    TryAssignByte = Symbol(
        None,
        None,
        None,
        (
            "Assign a byte to the target of a pointer if the pointer is"
            " non-null.\n\nr0: pointer\nr1: value\nreturn: true on success, false on"
            " failure"
        ),
    )

    TryAssignByteWrapper = Symbol(
        None,
        None,
        None,
        (
            "Wrapper around TryAssignByte.\n\nAccesses the TryAssignByte function with"
            " a weird chain of pointer dereferences.\n\nr0: pointer\nr1: value\nreturn:"
            " true on success, false on failure"
        ),
    )

    Wcstombs = Symbol(
        None,
        None,
        None,
        (
            "The wcstombs(3) C library function.\n\nr0: dest\nr1: src\nr2: n\nreturn:"
            " characters converted"
        ),
    )

    Memcpy = Symbol(
        None,
        None,
        None,
        "The memcpy(3) C library function.\n\nr0: dest\nr1: src\nr2: n",
    )

    Memmove = Symbol(
        None,
        None,
        None,
        (
            "The memmove(3) C library function.\n\nThe implementation is nearly the"
            " same as Memcpy, but it copies bytes from back to front if src <"
            " dst.\n\nr0: dest\nr1: src\nr2: n"
        ),
    )

    Memset = Symbol(
        None,
        None,
        None,
        (
            "The memset(3) C library function.\n\nThis is just a wrapper around"
            " MemsetInternal that returns the pointer at the end.\n\nr0: s\nr1: c (int,"
            " but must be a single-byte value)\nr2: n\nreturn: s"
        ),
    )

    Memchr = Symbol(
        None,
        None,
        None,
        (
            "The memchr(3) C library function.\n\nr0: s\nr1: c\nr2: n\nreturn: pointer"
            " to first occurrence of c in s, or a null pointer if no match"
        ),
    )

    Memcmp = Symbol(
        None,
        None,
        None,
        (
            "The memcmp(3) C library function.\n\nr0: s1\nr1: s2\nr2: n\nreturn:"
            " comparison value"
        ),
    )

    MemsetInternal = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Best-effort append the given data to a slice. If the slice's capacity is"
            " reached, any remaining data will be truncated.\n\nr0: slice pointer\nr1:"
            " buffer of data to append\nr2: number of bytes in the data buffer\nreturn:"
            " true"
        ),
    )

    VsprintfInternal = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "The vsprintf(3) C library function.\n\nr0: str\nr1: format\nr2:"
            " ap\nreturn: number of characters printed, excluding the null-terminator"
        ),
    )

    Snprintf = Symbol(
        None,
        None,
        None,
        (
            "The snprintf(3) C library function.\n\nThis calls VsprintfInternal"
            " directly, so it's presumably the real snprintf.\n\nr0: str\nr1: n\nr2:"
            " format\n...: variadic\nreturn: number of characters printed, excluding"
            " the null-terminator"
        ),
    )

    Sprintf = Symbol(
        None,
        None,
        None,
        (
            "The sprintf(3) C library function.\n\nThis calls VsprintfInternal"
            " directly, so it's presumably the real sprintf.\n\nr0: str\nr1:"
            " format\n...: variadic\nreturn: number of characters printed, excluding"
            " the null-terminator"
        ),
    )

    Strlen = Symbol(
        None,
        None,
        None,
        "The strlen(3) C library function.\n\nr0: s\nreturn: length of s",
    )

    Strcpy = Symbol(
        None,
        None,
        None,
        (
            "The strcpy(3) C library function.\n\nThis function is optimized to copy"
            " characters in aligned 4-byte chunks if possible, correctly handling any"
            " unaligned bytes at the front/back.\n\nr0: dest\nr1: src"
        ),
    )

    Strncpy = Symbol(
        None,
        None,
        None,
        "The strncpy(3) C library function.\n\nr0: dest\nr1: src\nr2: n",
    )

    Strcat = Symbol(
        None, None, None, "The strcat(3) C library function.\n\nr0: dest\nr1: src"
    )

    Strncat = Symbol(
        None,
        None,
        None,
        "The strncat(3) C library function.\n\nr0: dest\nr1: src\nr2: n",
    )

    Strcmp = Symbol(
        None,
        None,
        None,
        (
            "The strcmp(3) C library function.\n\nSimilarly to Strcpy, this function is"
            " optimized to compare characters in aligned 4-byte chunks if"
            " possible.\n\nr0: s1\nr1: s2\nreturn: comparison value"
        ),
    )

    Strncmp = Symbol(
        None,
        None,
        None,
        (
            "The strncmp(3) C library function.\n\nr0: s1\nr1: s2\nr2: n\nreturn:"
            " comparison value"
        ),
    )

    Strchr = Symbol(
        None,
        None,
        None,
        (
            "The strchr(3) C library function.\n\nr0: string\nr1: c\nreturn: pointer to"
            " the located byte c, or null pointer if no match"
        ),
    )

    Strcspn = Symbol(
        None,
        None,
        None,
        (
            "The strcspn(3) C library function.\n\nr0: string\nr1: stopset\nreturn:"
            " offset of the first character in string within stopset"
        ),
    )

    Strstr = Symbol(
        None,
        None,
        None,
        (
            "The strstr(3) C library function.\n\nr0: haystack\nr1: needle\nreturn:"
            " pointer into haystack where needle starts, or null pointer if no match"
        ),
    )

    Wcslen = Symbol(
        None,
        None,
        None,
        "The wcslen(3) C library function.\n\nr0: ws\nreturn: length of ws",
    )

    AddFloat = Symbol(
        None,
        None,
        None,
        (
            "This appears to be the libgcc implementation of __addsf3 (not sure which"
            " gcc version), which implements the addition operator for IEEE 754"
            " floating-point numbers.\n\nr0: a\nr1: b\nreturn: a + b"
        ),
    )

    DivideFloat = Symbol(
        None,
        None,
        None,
        (
            "This appears to be the libgcc implementation of __divsf3 (not sure which"
            " gcc version), which implements the division operator for IEEE 754"
            " floating-point numbers.\n\nr0: dividend\nr1: divisor\nreturn: dividend /"
            " divisor"
        ),
    )

    FloatToDouble = Symbol(
        None,
        None,
        None,
        (
            "This appears to be the libgcc implementation of __extendsfdf2 (not sure"
            " which gcc version), which implements the float to double cast operation"
            " for IEEE 754 floating-point numbers.\n\nr0: float\nreturn: (double)float"
        ),
    )

    FloatToInt = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "This appears to be the libgcc implementation of __floatsisf (not sure"
            " which gcc version), which implements the int to float cast operation for"
            " IEEE 754 floating-point numbers.\n\nr0: int\nreturn: (float)int"
        ),
    )

    UIntToFloat = Symbol(
        None,
        None,
        None,
        (
            "This appears to be the libgcc implementation of __floatunsisf (not sure"
            " which gcc version), which implements the unsigned int to float cast"
            " operation for IEEE 754 floating-point numbers.\n\nr0: uint\nreturn:"
            " (float)uint"
        ),
    )

    MultiplyFloat = Symbol(
        None,
        None,
        None,
        (
            "This appears to be the libgcc implementation of __mulsf3 (not sure which"
            " gcc version), which implements the multiplication operator for IEEE 754"
            " floating-point numbers."
        ),
    )

    Sqrtf = Symbol(
        None, None, None, "The sqrtf(3) C library function.\n\nr0: x\nreturn: sqrt(x)"
    )

    SubtractFloat = Symbol(
        None,
        None,
        None,
        (
            "This appears to be the libgcc implementation of __subsf3 (not sure which"
            " gcc version), which implements the subtraction operator for IEEE 754"
            " floating-point numbers.\n\nr0: a\nr1: b\nreturn: a - b"
        ),
    )

    DivideInt = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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


class EuItcmArm9Data:
    ARM9_HEADER = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SDK_STRINGS = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DEFAULT_MEMORY_ARENA_SIZE = Symbol(
        None,
        None,
        None,
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

    AURA_BOW_ID_LAST = Symbol(None, None, None, "Highest item ID of the aura bows.")

    NUMBER_OF_ITEMS = Symbol(None, None, None, "Number of items in the game.")

    MAX_MONEY_CARRIED = Symbol(
        None, None, None, "Maximum amount of money the player can carry, 99999."
    )

    MAX_MONEY_STORED = Symbol(
        None,
        None,
        None,
        "Maximum amount of money the player can store in the Duskull Bank, 9999999.",
    )

    DIALOG_BOX_LIST_PTR = Symbol(
        None, None, None, "Hard-coded pointer to DIALOG_BOX_LIST."
    )

    SCRIPT_VARS_VALUES_PTR = Symbol(
        None, None, None, "Hard-coded pointer to SCRIPT_VARS_VALUES."
    )

    MONSTER_ID_LIMIT = Symbol(
        None, None, None, "One more than the maximum valid monster ID (0x483)."
    )

    MAX_RECRUITABLE_TEAM_MEMBERS = Symbol(
        None,
        None,
        None,
        (
            "555, appears to be the maximum number of members recruited to an"
            " exploration team, at least for the purposes of some checks that need to"
            " iterate over all team members."
        ),
    )

    CART_REMOVED_IMG_DATA = Symbol(None, None, None, "")

    AVAILABLE_ITEMS_IN_GROUP_TABLE = Symbol(
        None,
        None,
        None,
        (
            "100*0x80\nLinked to the dungeon group id\n\nNote: unverified, ported from"
            " Irdkwia's notes"
        ),
    )

    ARM9_UNKNOWN_TABLE__NA_2097FF8 = Symbol(
        None,
        None,
        None,
        "16*0x4 (0x2+0x2)\n\nNote: unverified, ported from Irdkwia's notes",
    )

    KECLEON_SHOP_ITEM_TABLE_LISTS_1 = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: enum item_id[4]",
    )

    KECLEON_SHOP_ITEM_TABLE_LISTS_2 = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: enum item_id[4]",
    )

    EXCLUSIVE_ITEM_STAT_BOOST_DATA = Symbol(
        None,
        None,
        None,
        (
            "Contains stat boost effects for different exclusive item classes.\n\nEach"
            " 4-byte entry contains the boost data for (attack, special attack,"
            " defense, special defense), 1 byte each, for a specific exclusive item"
            " class, indexed according to the stat boost data index list.\n\ntype:"
            " struct exclusive_item_stat_boost_entry[15]"
        ),
    )

    EXCLUSIVE_ITEM_ATTACK_BOOSTS = Symbol(
        None, None, None, "EXCLUSIVE_ITEM_STAT_BOOST_DATA, offset by 0"
    )

    EXCLUSIVE_ITEM_SPECIAL_ATTACK_BOOSTS = Symbol(
        None, None, None, "EXCLUSIVE_ITEM_STAT_BOOST_DATA, offset by 1"
    )

    EXCLUSIVE_ITEM_DEFENSE_BOOSTS = Symbol(
        None, None, None, "EXCLUSIVE_ITEM_STAT_BOOST_DATA, offset by 2"
    )

    EXCLUSIVE_ITEM_SPECIAL_DEFENSE_BOOSTS = Symbol(
        None, None, None, "EXCLUSIVE_ITEM_STAT_BOOST_DATA, offset by 3"
    )

    EXCLUSIVE_ITEM_EFFECT_DATA = Symbol(
        None,
        None,
        None,
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
        None, None, None, "EXCLUSIVE_ITEM_EFFECT_DATA, offset by 1"
    )

    RECYCLE_SHOP_ITEM_LIST = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    TYPE_SPECIFIC_EXCLUSIVE_ITEMS = Symbol(
        None,
        None,
        None,
        (
            "Lists of type-specific exclusive items (silk, dust, gem, globe) for each"
            " type.\n\ntype: struct item_id_16[17][4]"
        ),
    )

    RECOIL_MOVE_LIST = Symbol(
        None,
        None,
        None,
        (
            "Null-terminated list of all the recoil moves, as 2-byte move IDs.\n\ntype:"
            " struct move_id_16[11]"
        ),
    )

    PUNCH_MOVE_LIST = Symbol(
        None,
        None,
        None,
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
        None,
        None,
        None,
        (
            "Table of values for the PARTNER_TALK_KIND script variable.\n\ntype: struct"
            " partner_talk_kind_table_entry[11]"
        ),
    )

    SCRIPT_VARS_LOCALS = Symbol(
        None,
        None,
        None,
        (
            "List of special 'local' variables available to the script engine. There"
            " are 4 16-byte entries.\n\nEach entry has the same structure as an entry"
            " in SCRIPT_VARS.\n\ntype: struct script_local_var_table"
        ),
    )

    SCRIPT_VARS = Symbol(
        None,
        None,
        None,
        (
            "List of predefined global variables that track game state, which are"
            " available to the script engine. There are 115 16-byte entries.\n\nThese"
            " variables underpin the various ExplorerScript global variables you can"
            " use in the SkyTemple SSB debugger.\n\ntype: struct script_var_table"
        ),
    )

    HARDCODED_PORTRAIT_DATA_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " portrait_data_entry[32]"
        ),
    )

    WONDER_MAIL_BITS_MAP = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: uint8_t[32]",
    )

    WONDER_MAIL_BITS_SWAP = Symbol(
        None,
        None,
        None,
        (
            "Last 2 bytes are unused\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\ntype: uint8_t[36]"
        ),
    )

    ARM9_UNKNOWN_TABLE__NA_209E12C = Symbol(
        None,
        None,
        None,
        "52*0x2 + 2 bytes unused\n\nNote: unverified, ported from Irdkwia's notes",
    )

    ARM9_UNKNOWN_TABLE__NA_209E164 = Symbol(
        None, None, None, "256*0x1\n\nNote: unverified, ported from Irdkwia's notes"
    )

    ARM9_UNKNOWN_TABLE__NA_209E280 = Symbol(
        None, None, None, "32*0x1\n\nNote: unverified, ported from Irdkwia's notes"
    )

    WONDER_MAIL_ENCRYPTION_TABLE = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: uint8_t[256]",
    )

    DUNGEON_DATA_LIST = Symbol(
        None,
        None,
        None,
        (
            "Data about every dungeon in the game.\n\nThis is an array of 180 dungeon"
            " data list entry structs. Each entry is 4 bytes, and contains floor count"
            " information along with an index into the bulk of the dungeon's data in"
            " mappa_s.bin.\n\nSee the struct definitions and End45's dungeon data"
            " document for more info.\n\ntype: struct dungeon_data_list_entry[180]"
        ),
    )

    ADVENTURE_LOG_ENCOUNTERS_MONSTER_IDS = Symbol(
        None,
        None,
        None,
        (
            "List of monster IDs with a corresponding milestone in the Adventure"
            " Log.\n\ntype: struct monster_id_16[38]"
        ),
    )

    ARM9_UNKNOWN_DATA__NA_209E6BC = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    TACTIC_NAME_STRING_IDS = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[12]",
    )

    STATUS_NAME_STRING_IDS = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[102]",
    )

    DUNGEON_RETURN_STATUS_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " dungeon_return_status[91]"
        ),
    )

    STATUSES_FULL_DESCRIPTION_STRING_IDS = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " status_description[103]"
        ),
    )

    ARM9_UNKNOWN_DATA__NA_209EAAC = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_FLOOR_RANKS_AND_ITEM_LISTS_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_FLOORS_FORBIDDEN = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " mission_floors_forbidden[100]"
        ),
    )

    MISSION_FLOOR_RANKS_AND_ITEM_LISTS_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_FLOOR_RANKS_PTRS = Symbol(
        None,
        None,
        None,
        (
            "Uses MISSION_FLOOR_RANKS_AND_ITEM_LISTS\n\nNote: unverified, ported from"
            " Irdkwia's notes"
        ),
    )

    DUNGEON_RESTRICTIONS = Symbol(
        None,
        None,
        None,
        (
            "Data related to dungeon restrictions for every dungeon in the"
            " game.\n\nThis is an array of 256 dungeon restriction structs. Each entry"
            " is 12 bytes, and contains information about restrictions within the given"
            " dungeon.\n\nSee the struct definitions and End45's dungeon data document"
            " for more info.\n\ntype: struct dungeon_restriction[256]"
        ),
    )

    SPECIAL_BAND_STAT_BOOST = Symbol(
        None, None, None, "Stat boost value for the Special Band."
    )

    MUNCH_BELT_STAT_BOOST = Symbol(
        None, None, None, "Stat boost value for the Munch Belt."
    )

    GUMMI_STAT_BOOST = Symbol(
        None,
        None,
        None,
        "Stat boost value if a stat boost occurs when eating normal Gummis.",
    )

    MIN_IQ_EXCLUSIVE_MOVE_USER = Symbol(None, None, None, "")

    WONDER_GUMMI_IQ_GAIN = Symbol(
        None, None, None, "IQ gain when ingesting wonder gummis."
    )

    AURA_BOW_STAT_BOOST = Symbol(
        None, None, None, "Stat boost value for the aura bows."
    )

    MIN_IQ_ITEM_MASTER = Symbol(None, None, None, "")

    DEF_SCARF_STAT_BOOST = Symbol(
        None, None, None, "Stat boost value for the Defense Scarf."
    )

    POWER_BAND_STAT_BOOST = Symbol(
        None, None, None, "Stat boost value for the Power Band."
    )

    WONDER_GUMMI_STAT_BOOST = Symbol(
        None,
        None,
        None,
        "Stat boost value if a stat boost occurs when eating Wonder Gummis.",
    )

    ZINC_BAND_STAT_BOOST = Symbol(
        None, None, None, "Stat boost value for the Zinc Band."
    )

    EGG_HP_BONUS = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    EVOLUTION_HP_BONUS = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    EVOLUTION_PHYSICAL_STAT_BONUSES = Symbol(
        None,
        None,
        None,
        "0x2: Atk + 0x2: Def\n\nNote: unverified, ported from Irdkwia's notes",
    )

    EGG_STAT_BONUSES = Symbol(
        None,
        None,
        None,
        (
            "0x2: Atk + 0x2: SpAtk + 0x2: Def + 0x2: SpDef\n\nNote: unverified, ported"
            " from Irdkwia's notes"
        ),
    )

    EVOLUTION_SPECIAL_STAT_BONUSES = Symbol(
        None,
        None,
        None,
        "0x2: SpAtk + 0x2: SpDef\n\nNote: unverified, ported from Irdkwia's notes",
    )

    FORBIDDEN_FORGOT_MOVE_LIST = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " forbidden_forgot_move_entry[3]"
        ),
    )

    TACTICS_UNLOCK_LEVEL_TABLE = Symbol(None, None, None, "type: int16_t[12]")

    CLIENT_LEVEL_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Still a guess\n\nNote: unverified, ported from Irdkwia's notes\n\ntype:"
            " int16_t[16]"
        ),
    )

    OUTLAW_LEVEL_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Table of 2-byte outlaw levels for outlaw missions, indexed by mission"
            " rank.\n\ntype: int16_t[16]"
        ),
    )

    OUTLAW_MINION_LEVEL_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Table of 2-byte outlaw minion levels for outlaw hideout missions, indexed"
            " by mission rank.\n\ntype: int16_t[16]"
        ),
    )

    HIDDEN_POWER_BASE_POWER_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Still a guess\n\nNote: unverified, ported from Irdkwia's notes\n\ntype:"
            " int[10]"
        ),
    )

    VERSION_EXCLUSIVE_MONSTERS = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " version_exclusive_monster[23]"
        ),
    )

    IQ_SKILL_RESTRICTIONS = Symbol(
        None,
        None,
        None,
        (
            "Table of 2-byte values for each IQ skill that represent a group. IQ skills"
            " in the same group can not be enabled at the same time.\n\ntype:"
            " int16_t[69]"
        ),
    )

    SECONDARY_TERRAIN_TYPES = Symbol(
        None,
        None,
        None,
        (
            "The type of secondary terrain for each dungeon in the game.\n\nThis is an"
            " array of 200 bytes. Each byte is an enum corresponding to one"
            " dungeon.\n\ntype: struct secondary_terrain_type_8[200]"
        ),
    )

    SENTRY_DUTY_MONSTER_IDS = Symbol(
        None,
        None,
        None,
        (
            "Table of monster IDs usable in the sentry duty minigame.\n\ntype: struct"
            " monster_id_16[102]"
        ),
    )

    IQ_SKILLS = Symbol(
        None,
        None,
        None,
        (
            "Table of 4-byte values for each IQ skill that represent the required IQ"
            " value to unlock a skill.\n\ntype: int[69]"
        ),
    )

    IQ_GROUP_SKILLS = Symbol(None, None, None, "Irdkwia's notes: 25*16*0x1")

    MONEY_QUANTITY_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Table that maps money quantity codes (as recorded in, e.g., struct item)"
            " to actual amounts.\n\ntype: int[100]"
        ),
    )

    ARM9_UNKNOWN_TABLE__NA_20A20B0 = Symbol(
        None, None, None, "256*0x2\n\nNote: unverified, ported from Irdkwia's notes"
    )

    IQ_GUMMI_GAIN_TABLE = Symbol(None, None, None, "type: int16_t[18][18]")

    GUMMI_BELLY_RESTORE_TABLE = Symbol(None, None, None, "type: int16_t[18][18]")

    BAG_CAPACITY_TABLE_SPECIAL_EPISODES = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: uint32_t[5]",
    )

    BAG_CAPACITY_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Array of 4-byte integers containing the bag capacity for each bag"
            " level.\n\ntype: uint32_t[8]"
        ),
    )

    SPECIAL_EPISODE_MAIN_CHARACTERS = Symbol(
        None, None, None, "type: struct monster_id_16[100]"
    )

    GUEST_MONSTER_DATA = Symbol(
        None,
        None,
        None,
        (
            "Data for guest monsters that join you during certain story"
            " dungeons.\n\nArray of 18 36-byte entries.\n\nSee the struct definitions"
            " and End45's dungeon data document for more info.\n\ntype: struct"
            " guest_monster[18]"
        ),
    )

    RANK_UP_TABLE = Symbol(None, None, None, "")

    DS_DOWNLOAD_TEAMS = Symbol(
        None,
        None,
        None,
        (
            "Seems like this is just a collection of null-terminated lists concatenated"
            " together.\n\nNote: unverified, ported from Irdkwia's notes\n\nstruct"
            " monster_id_16[56]"
        ),
    )

    ARM9_UNKNOWN_PTR__NA_20A2C84 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    UNOWN_SPECIES_ADDITIONAL_CHARS = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: enum monster_id[28]",
    )

    MONSTER_SPRITE_DATA = Symbol(None, None, None, "")

    REMOTE_STRINGS = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    RANK_STRINGS_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_MENU_STRING_IDS_1 = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[8]",
    )

    RANK_STRINGS_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_MENU_STRING_IDS_2 = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[8]",
    )

    RANK_STRINGS_3 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_DUNGEON_UNLOCK_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Irdkwia's notes: SpecialDungeonMissions\n\ntype: struct"
            " dungeon_unlock_entry[3]"
        ),
    )

    NO_SEND_ITEM_TABLE = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: struct item_id_16[3]",
    )

    ARM9_UNKNOWN_TABLE__NA_20A3CC8 = Symbol(
        None,
        None,
        None,
        (
            "14*0x2\nLinked to ARM9_UNKNOWN_TABLE__NA_20A3CE4\n\nNote: unverified,"
            " ported from Irdkwia's notes"
        ),
    )

    ARM9_UNKNOWN_TABLE__NA_20A3CE4 = Symbol(
        None, None, None, "8*0x2\n\nNote: unverified, ported from Irdkwia's notes"
    )

    ARM9_UNKNOWN_FUNCTION_TABLE__NA_20A3CF4 = Symbol(
        None,
        None,
        None,
        "Could be related to missions\n\nNote: unverified, ported from Irdkwia's notes",
    )

    MISSION_BANNED_STORY_MONSTERS = Symbol(
        None,
        None,
        None,
        (
            "Null-terminated list of monster IDs that can't be used (probably as"
            " clients or targets) when generating missions before a certain point in"
            " the story.\n\nTo be precise, PERFOMANCE_PROGRESS_FLAG[9] must be enabled"
            " so these monsters can appear as mission clients.\n\ntype: struct"
            " monster_id_16[length / 2]"
        ),
    )

    ITEM_DELIVERY_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Maybe it is the Item table used for Item Deliveries\n\nNote: unverified,"
            " ported from Irdkwia's notes\n\ntype: struct item_id_16[23]"
        ),
    )

    MISSION_RANK_POINTS = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int[16]",
    )

    MISSION_BANNED_MONSTERS = Symbol(
        None,
        None,
        None,
        (
            "Null-terminated list of monster IDs that can't be used (probably as"
            " clients or targets) when generating missions.\n\ntype: struct"
            " monster_id_16[124]"
        ),
    )

    MISSION_STRING_IDS = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[964]",
    )

    LEVEL_LIST = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    EVENTS = Symbol(
        None,
        None,
        None,
        (
            "Table of levels for the script engine, in which scenes can take place."
            " There are a version-dependent number of 12-byte entries.\n\ntype: struct"
            " script_level[length / 12]"
        ),
    )

    ARM9_UNKNOWN_TABLE__NA_20A68BC = Symbol(
        None, None, None, "6*0x2\n\nNote: unverified, ported from Irdkwia's notes"
    )

    DEMO_TEAMS = Symbol(
        None,
        None,
        None,
        (
            "18*0x4 (Hero ID 0x2, Partner ID 0x2)\n\nNote: unverified, ported from"
            " Irdkwia's notes"
        ),
    )

    ACTOR_LIST = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    ENTITIES = Symbol(
        None,
        None,
        None,
        (
            "Table of entities for the script engine, which can move around and do"
            " things within a scene. There are 386 12-byte entries.\n\ntype: struct"
            " script_entity[386]"
        ),
    )

    JOB_D_BOX_LAYOUT_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_3 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_4 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_5 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_6 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_7 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_8 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_9 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_10 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_11 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_12 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_MENU_13 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    JOB_D_BOX_LAYOUT_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DUNGEON_SWAP_ID_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " dungeon_id_8[212]"
        ),
    )

    MAP_MARKER_PLACEMENTS = Symbol(
        None,
        None,
        None,
        (
            "The map marker position of each dungeon on the Wonder Map.\n\nThis is an"
            " array of 310 map marker structs. Each entry is 8 bytes, and contains"
            " positional information about a dungeon on the map.\n\nSee the struct"
            " definitions and End45's dungeon data document for more info.\n\ntype:"
            " struct map_marker[310]"
        ),
    )

    ARM9_UNKNOWN_TABLE__NA_20A9FB0 = Symbol(
        None, None, None, "4701*0x4\n\nNote: unverified, ported from Irdkwia's notes"
    )

    ARM9_UNKNOWN_TABLE__NA_20AE924 = Symbol(
        None, None, None, "724*0x1\n\nNote: unverified, ported from Irdkwia's notes"
    )

    MEMORY_ALLOCATION_ARENA_GETTERS = Symbol(
        None,
        None,
        None,
        (
            "Functions to get the desired memory arena for allocating and freeing heap"
            " memory.\n\ntype: struct mem_arena_getters"
        ),
    )

    PRNG_SEQUENCE_NUM = Symbol(
        None,
        None,
        None,
        (
            "[Runtime] The current PRNG sequence number for the general-purpose PRNG."
            " See Rand16Bit for more information on how the general-purpose PRNG works."
        ),
    )

    LOADED_OVERLAY_GROUP_0 = Symbol(
        None,
        None,
        None,
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
        None,
        None,
        None,
        (
            "[Runtime] The overlay group ID of the overlay currently loaded in slot 1."
            " A group ID of 0 denotes no overlay.\n\nOverlay group IDs that can be"
            " loaded in slot 1:\n- 0x4 (overlay 1)\n- 0x5 (overlay 2)\n- 0xD (overlay"
            " 11)\n- 0xE (overlay 29)\n- 0xF (overlay 34)\n\ntype: enum"
            " overlay_group_id"
        ),
    )

    LOADED_OVERLAY_GROUP_2 = Symbol(
        None,
        None,
        None,
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
        None,
        None,
        None,
        (
            "List of pointers to path strings to all known pack files.\nThe game uses"
            " this table to load its resources when launching dungeon mode.\n\ntype:"
            " char*[6]"
        ),
    )

    GAME_STATE_VALUES = Symbol(None, None, None, "[Runtime]")

    BAG_ITEMS_PTR_MIRROR = Symbol(
        None,
        None,
        None,
        (
            "[Runtime] Probably a mirror of ram.yml::BAG_ITEMS_PTR?\n\nNote:"
            " unverified, ported from Irdkwia's notes"
        ),
    )

    ITEM_DATA_TABLE_PTRS = Symbol(
        None,
        None,
        None,
        (
            "[Runtime] List of pointers to various item data tables.\n\nThe first two"
            " pointers are definitely item-related (although the order appears to be"
            " flipped between EU/NA?). Not sure about the third pointer."
        ),
    )

    DUNGEON_MOVE_TABLES = Symbol(
        None,
        None,
        None,
        (
            "[Runtime] Seems to be some sort of region (a table of tables?) that holds"
            " pointers to various important tables related to moves."
        ),
    )

    MOVE_DATA_TABLE_PTR = Symbol(
        None,
        None,
        None,
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

    LANGUAGE_INFO_DATA = Symbol(None, None, None, "[Runtime]")

    TBL_TALK_GROUP_STRING_ID_START = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[6]",
    )

    KEYBOARD_STRING_IDS = Symbol(
        None,
        None,
        None,
        "30*0x2\n\nNote: unverified, ported from Irdkwia's notes\n\ntype: int16_t[30]",
    )

    NOTIFY_NOTE = Symbol(
        None,
        None,
        None,
        "[Runtime] Flag related to saving and loading state?\n\ntype: bool",
    )

    DEFAULT_HERO_ID = Symbol(
        None,
        None,
        None,
        (
            "The default monster ID for the hero (0x4: Charmander)\n\ntype: struct"
            " monster_id_16"
        ),
    )

    DEFAULT_PARTNER_ID = Symbol(
        None,
        None,
        None,
        (
            "The default monster ID for the partner (0x1: Bulbasaur)\n\ntype: struct"
            " monster_id_16"
        ),
    )

    GAME_MODE = Symbol(None, None, None, "[Runtime]\n\ntype: uint8_t")

    GLOBAL_PROGRESS_PTR = Symbol(
        None, None, None, "[Runtime]\n\ntype: struct global_progress*"
    )

    ADVENTURE_LOG_PTR = Symbol(
        None, None, None, "[Runtime]\n\ntype: struct adventure_log*"
    )

    ITEM_TABLES_PTRS_1 = Symbol(
        None,
        None,
        None,
        "Irdkwia's notes: 26*0x4, uses MISSION_FLOOR_RANKS_AND_ITEM_LISTS",
    )

    UNOWN_SPECIES_ADDITIONAL_CHAR_PTR_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Uses UNOWN_SPECIES_ADDITIONAL_CHARS\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\ntype: enum monster_id*[28]"
        ),
    )

    PARTY_MONSTERS_PTR = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    MISSION_LIST_PTR = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    REMOTE_STRING_PTR_TABLE = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: const char*[7]",
    )

    RANK_STRING_PTR_TABLE = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: const char*[16]",
    )

    SMD_EVENTS_FUN_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Irdkwia's notes: named DSEEventFunctionPtrTable with length 0x3C0 (note"
            " the disagreement), 240*0x4."
        ),
    )

    MUSIC_DURATION_LOOKUP_TABLE_1 = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[128]",
    )

    MUSIC_DURATION_LOOKUP_TABLE_2 = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int32_t[128]",
    )

    JUICE_BAR_NECTAR_IQ_GAIN = Symbol(
        None, None, None, "IQ gain when ingesting nectar at the Juice Bar."
    )

    TEXT_SPEED = Symbol(None, None, None, "Controls text speed.")

    HERO_START_LEVEL = Symbol(None, None, None, "Starting level of the hero.")

    PARTNER_START_LEVEL = Symbol(None, None, None, "Starting level of the partner.")


class EuItcmArm9Section:
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
    loadaddress = 0x1FF8000
    length = 0x4000
    functions = EuItcmArm9Functions
    data = EuItcmArm9Data


class EuItcmItcmFunctions:
    GetKeyN2MSwitch = Symbol(
        [0x1434],
        [0x1FF9434],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: key\nr1: switch",
    )

    GetKeyN2M = Symbol(
        [0x1468],
        [0x1FF9468],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: key\nreturn: monster ID",
    )

    GetKeyN2MBaseForm = Symbol(
        [0x14D4],
        [0x1FF94D4],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: key\nreturn: monster ID",
    )

    GetKeyM2NSwitch = Symbol(
        [0x150C],
        [0x1FF950C],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nr1: switch",
    )

    GetKeyM2N = Symbol(
        [0x1540],
        [0x1FF9540],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn: key",
    )

    GetKeyM2NBaseForm = Symbol(
        [0x15AC],
        [0x1FF95AC],
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nreturn: key",
    )

    ShouldMonsterRunAwayVariationOutlawCheck = Symbol(
        [0x2390],
        [0x1FFA390],
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
        [0x1FFA3C4],
        None,
        (
            "Used by the AI to determine the direction in which a monster should"
            " move\n\nr0: Entity pointer\nr1: ?"
        ),
    )

    CalculateAiTargetPos = Symbol(
        [0x32C8],
        [0x1FFB2C8],
        None,
        (
            "Calculates the target position of an AI-controlled monster and stores it"
            " in the monster's ai_target_pos field\n\nr0: Entity pointer"
        ),
    )

    ChooseAiMove = Symbol(
        [0x3658],
        [0x1FFB658],
        None,
        (
            "Determines if an AI-controlled monster will use a move and which one it"
            " will use\n\nr0: Entity pointer"
        ),
    )


class EuItcmItcmData:
    MEMORY_ALLOCATION_TABLE = Symbol(
        None,
        None,
        None,
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
        None,
        None,
        None,
        (
            "[Runtime] The default memory allocation arena. This is part of"
            " MEMORY_ALLOCATION_TABLE, but is also referenced on its own by various"
            " functions.\n\nNote: This symbol isn't actually part of the ITCM, it gets"
            " created at runtime on the spot in RAM that used to contain the code that"
            " was moved to the ITCM.\n\ntype: struct mem_arena"
        ),
    )

    DEFAULT_MEMORY_ARENA_BLOCKS = Symbol(
        None,
        None,
        None,
        (
            "[Runtime] The block array for DEFAULT_MEMORY_ARENA.\n\nNote: This symbol"
            " isn't actually part of the ITCM, it gets created at runtime on the spot"
            " in RAM that used to contain the code that was moved to the ITCM.\n\ntype:"
            " struct mem_block[256]"
        ),
    )


class EuItcmItcmSection:
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
    loadaddress = 0x1FF8000
    length = 0x4000
    functions = EuItcmItcmFunctions
    data = EuItcmItcmData


class EuItcmMove_effectsFunctions:
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
        None,
        None,
        None,
        (
            "Move effect: Deal multihit damage until a strike misses\nRelevant moves:"
            " Ice Ball, Rollout\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveYawn = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Vital Throw\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDig = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Charm\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRainDance = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Rain Dance\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHail = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Hail\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHealStatus = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Encore\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRage = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Rage\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSuperFang = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Super Fang\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePainSplit = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Pain Split\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveTorment = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Torment\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveStringShot = Symbol(
        None,
        None,
        None,
        (
            "Move effect: String Shot\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSwagger = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Swagger\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSnore = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Snore\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveScreech = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Weather Ball\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveWhirlpool = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Spite\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFocusEnergy = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Focus Energy\nRelevant moves: Focus Energy,"
            " MOVE_TAG_0x1AC\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSmokescreen = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Smokescreen\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMirrorMove = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Mirror Move\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveOverheat = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Overheat\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveAuroraBeam = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Aurora Beam\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMemento = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Flatter\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveWillOWisp = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Will-O-Wisp\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveReturn = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Razor Wind\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBide = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Give the user the Bide status\nRelevant moves: Bide, Revenge,"
            " Avalanche\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBideUnleash = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Endeavor\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFacade = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Brick Break\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDamageLowerSpeed100 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage and lower the defender's speed.\nRelevant moves:"
            " Rock Tomb, Icy Wind, Mud Shot\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveFocusPunch = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Focus Punch\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDamageDrain = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: SmellingSalt\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMetalSound = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Metal Sound\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTickle = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Tickle\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveShadowHold = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Inflict the Shadow Hold status on the defender\nRelevant"
            " moves: Spider Web, Mean Look\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveHaze = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Haze\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageMultihitFatigue = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal multihit damage, then confuse the attacker\nRelevant"
            " moves: Outrage, Petal Dance\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDamageWeightDependent = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage, multiplied by a weight-dependent"
            " factor.\nRelevant moves: Low Kick, Grass Knot\n\nr0: attacker"
            " pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn: whether or"
            " not damage was dealt"
        ),
    )

    DoMoveDamageBoostAllStats = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Boost the team's movement speed by one stage\nRelevant moves:"
            " Agility, Speed Boost (item effect), MOVE_TAG_0x1AA, Tailwind\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveRapidSpin = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Rapid Spin\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSureShot = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Sky Attack\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageFreeze15 = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Endure\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveLowerSpeed1 = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Psywave\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageLowerDefensiveStatVariable = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Psycho Boost\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveUproar = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Psych Up\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageWithRecoil = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deals damage, inflicting recoil damage on the"
            " attacker.\nRelevant moves: Submission, Take Down, Volt Tackle, Wood"
            " Hammer, Brave Bird\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: bool, whether or not damage was dealt"
        ),
    )

    EntityIsValidMoveEffects = Symbol(
        None, None, None, "See overlay29.yml::EntityIsValid"
    )

    DoMoveRecoverHp = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Recover 50% of the user's max HP\nRelevant moves: Recover,"
            " Slack Off\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveEarthquake = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Earthquake\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    GetNaturePowerVariant = Symbol(
        None,
        None,
        None,
        (
            "Gets the nature power variant for the current dungeon, based on the"
            " tileset ID.\n\nreturn: nature power variant"
        ),
    )

    DoMoveNaturePower = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Mist\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFissure = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Safeguard\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveAbsorb = Symbol(
        None,
        None,
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
        None, None, None, "See overlay29.yml::DefenderAbilityIsActive"
    )

    DoMoveSkillSwap = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Skill Swap\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSketch = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Double-Edge\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSandstorm = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Possibly one-hit KO the defender\nRelevant moves: Sheer Cold,"
            " Guillotine\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSolarBeam = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Fly\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveExplosion = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Explosion\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDive = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Stockpile\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveTwister = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Twister\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveTwineedle = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Twineedle\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRecoverHpTeam = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Seismic Toss\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveConfuse = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Confuse target enemies if possible.\nRelevant moves: Confuse"
            " Ray, Supersonic, Sweet Kiss, Teeter Dance, Totter (item effect)\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveTaunt = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Conversion\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveConversion2 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Conversion 2\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveHelpingHand = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Thunder Wave\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveZapCannon = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Zap Cannon\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBlock = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Block\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePoison = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Poison the defender if possible\nRelevant moves: Poison Gas,"
            " PoisonPowder\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveToxic = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Jump Kick\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBounce = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Bounce\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHiJumpKick = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Hi Jump Kick\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTriAttack = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Tri Attack\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSwapItems = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Swaps the held items of the attacker and defender.\nRelevant"
            " moves: Trick, Switcheroo\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTripleKick = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Triple Kick\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSport = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Activate the relevant sport condition (Mud Sport, Water"
            " Sport) on the floor\nRelevant moves: Mud Sport, Water Sport\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveMudSlap = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Surf\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRolePlay = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Role Play\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSunnyDay = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Sleep Talk\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePayDay = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Pay Day\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveAssist = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Assist\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRest = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Rest\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveIngrain = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Ingrain\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSwallow = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Swallow\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveCurse = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Curse\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSuperpower = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Spit Up\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDynamicPunch = Symbol(
        None,
        None,
        None,
        (
            "Move effect: DynamicPunch\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveKnockOff = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Knock Off\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSplash = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Splash\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSetDamage = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Give the user the Set Damage status\nRelevant moves: Doom"
            " Desire, Future Sight\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBellyDrum = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Belly Drum\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveLightScreen = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Light Screen\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSecretPower = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Beat Up\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBlastBurn = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Present\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveEruption = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Eruption\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveTransform = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Blows the defender back\nRelevant moves: Whirlwind, Roar,"
            " Blowback (item effect)\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveCamouflage = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Perish Song\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveWrap = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Wrap\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSpikes = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Spikes\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMagnitude = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Magnitude\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMagicCoat = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Magic Coat\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveProtect = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Destiny Bond\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMirrorCoat = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Attract\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveCopycat = Symbol(
        None,
        None,
        None,
        (
            "Move effect: The attacker uses the move last used by enemy it's"
            " facing.\nRelevant moves: Mimic, Copycat\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveFrustration = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Frustration\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveLeechSeed = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Leech Seed\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMetronome = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Metronome\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDreamEater = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Dream Eater\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSnatch = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Snatch\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRecycle = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Recycle\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveReflect = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Dragon Dance\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSkullBash = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Skull Bash\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageLowerSpecialDefense50 = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Struggle\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRockSmash = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Rock Smash\nRelevant moves: Rock Smash,"
            " MOVE_UNNAMED_0x169\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveSeeTrap = Symbol(
        None,
        None,
        None,
        (
            "Move effect: See-Trap (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTakeaway = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Takeaway (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveRebound = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Rebound (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSwitchPositions = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Switches the user's position with positions of other monsters"
            " in the room.\nRelevant moves: Baton Pass, Switcher (item effect)\n\nr0:"
            " attacker pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn:"
            " whether the move was successfully used"
        ),
    )

    DoMoveStayAway = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Stay Away (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveCleanse = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Two-Edge (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveNoMove = Symbol(
        None,
        None,
        None,
        (
            "Move effect: No-Move (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveScan = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Scan (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMovePowerEars = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Power-Ears (item effect)\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveTransfer = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Transfer (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSlowDown = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Slow Down (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSearchlight = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Searchlight (item effect)\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMovePetrify = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Petrifies the target\nRelevant moves: Petrify (item effect),"
            " MOVE_TAG_0x1A9\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePounce = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Pounce (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTrawl = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Trawl (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveEscape = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Escape (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDrought = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Drought (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTrapBuster = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Trap Buster (item effect)\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveWildCall = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Wild Call (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveInvisify = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Invisify (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveOneShot = Symbol(
        None,
        None,
        None,
        (
            "Move effect: One-Shot (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveHpGauge = Symbol(
        None,
        None,
        None,
        (
            "Move effect: HP Gauge (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveVacuumCut = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Vacuum Cut\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveReviver = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Reviver (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveShocker = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Shocker (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveEcho = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Echo (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveFamish = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Famish (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveOneRoom = Symbol(
        None,
        None,
        None,
        (
            "Move effect: One-Room (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveFillIn = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Fill-In (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTrapper = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Trapper (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveItemize = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Itemize (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveHurl = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Hurls the target\nRelevant moves: Strength, Hurl (item"
            " effect), Fling\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveMobile = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Mobile (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveSeeStairs = Symbol(
        None,
        None,
        None,
        (
            "Move effect: See Stairs (item effect)\n\nr0: attacker pointer\nr1:"
            " defender pointer\nr2: move\nr3: item ID\nreturn: whether the move was"
            " successfully used"
        ),
    )

    DoMoveLongToss = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Long Toss (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMovePierce = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Pierce (item effect)\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoHammerArm = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Hammer Arm\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveAquaRing = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Aqua Ring\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveGastroAcid = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Gastro Acid\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveHealingWish = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Healing Wish\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveCloseCombat = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Close Combat\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveLuckyChant = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Lucky Chant\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveGuardSwap = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Guard Swap\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHealOrder = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Heal Order\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveHealBlock = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Heal Block\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveThunderFang = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Thunder Fang\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveDefog = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Defog\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveTrumpCard = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Trump Card\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveIceFang = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Ice Fang\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePsychoShift = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Psycho Shift\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveEmbargo = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Embargo\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveBrine = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage, with a 2x multiplier if the defender is at or"
            " below half HP.\nRelevant moves: Brine, Assurance\n\nr0: attacker"
            " pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn: whether the"
            " move was successfully used"
        ),
    )

    DoMoveNaturalGift = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Natural Gift\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveGyroBall = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Gyro Ball\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveShadowForce = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Shadow Force\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveGravity = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Gravity\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveStealthRock = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Stealth Rock\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveChargeBeam = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Acupressure\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMagnetRise = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Magnet Rise\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveToxicSpikes = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Toxic Spikes\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveLastResort = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Last Resort\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTrickRoom = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Trick Room\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveWorrySeed = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Worry Seed\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDamageHpDependent = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Deal damage, with a multiplier dependent on the defender's"
            " current HP.\nRelevant moves: Wring Out, Crush Grip\n\nr0: attacker"
            " pointer\nr1: defender pointer\nr2: move\nr3: item ID\nreturn: whether the"
            " move was successfully used"
        ),
    )

    DoMoveHeartSwap = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Heart Swap\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveRoost = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Roost\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePowerSwap = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Power Swap\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMovePowerTrick = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Power Trick\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveFeint = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Feint\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveFlareBlitz = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: Fire Fang\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveLunarDance = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Lunar Dance\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMiracleEye = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Miracle Eye\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveWakeUpSlap = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Wake-Up Slap\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveMetalBurst = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Metal Burst\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveHeadSmash = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Head Smash\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveCaptivate = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Captivate\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveLeafStorm = Symbol(
        None,
        None,
        None,
        (
            "Move effect: Leaf Storm\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: item ID\nreturn: whether the move was successfully used"
        ),
    )

    DoMoveDracoMeteor = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Move effect: MOVE_TAG_0x1A6\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )

    DoMoveTag0x1A7 = Symbol(
        None,
        None,
        None,
        (
            "Move effect: MOVE_TAG_0x1A7\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: move\nr3: item ID\nreturn: whether the move was successfully"
            " used"
        ),
    )


class EuItcmMove_effectsData:
    LUNAR_DANCE_PP_RESTORATION = Symbol(
        None, None, None, "The amount of PP restored by Lunar Dance (999)."
    )


class EuItcmMove_effectsSection:
    name = "move_effects"
    description = (
        "Move effect handlers for individual moves, called by ExecuteMoveEffect (and"
        " also the Metronome and Nature Power tables).\n\nThis subregion contains only"
        " the move effect handlers themselves, and not necessarily all the utility"
        " functions used by the move effect handlers (such as the damage calculation"
        " functions). These supporting utilities are in the main overlay29 block."
    )
    loadaddress = None
    length = None
    functions = EuItcmMove_effectsFunctions
    data = EuItcmMove_effectsData


class EuItcmOverlay0Functions:
    pass


class EuItcmOverlay0Data:
    TOP_MENU_MUSIC_ID = Symbol(None, None, None, "Music ID to play in the top menu.")


class EuItcmOverlay0Section:
    name = "overlay0"
    description = (
        "Likely contains supporting data and code related to the top menu.\n\nThis is"
        " loaded together with overlay 1 while in the top menu. Since it's in overlay"
        " group 2 (together with overlay 10, which is another 'data' overlay), this"
        " overlay probably plays a similar role. It mentions several files from the"
        " BACK folder that are known backgrounds for the top menu."
    )
    loadaddress = None
    length = None
    functions = EuItcmOverlay0Functions
    data = EuItcmOverlay0Data


class EuItcmOverlay1Functions:
    CreateMainMenus = Symbol(
        None,
        None,
        None,
        (
            "Prepares the top menu and sub menu, adding the different options that"
            " compose them.\n\nContains multiple calls to AddMainMenuOption and"
            " AddSubMenuOption. Some of them are conditionally executed depending on"
            " which options should be unlocked.\n\nNo params."
        ),
    )

    AddMainMenuOption = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Adds an option to the 'Other' submenu on the top menu.\n\nThis function is"
            " called for each one of the options in the submenu. It loops the SUBMENU"
            " data field, if the specified action ID does not exist there, the option"
            " won't be added.\n\nr0: Action ID\nr1: True if the option should be"
            " enabled, false otherwise"
        ),
    )


class EuItcmOverlay1Data:
    PRINTS_STRINGS = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    PRINTS_STRUCT = Symbol(
        None, None, None, "62*0x8\n\nNote: unverified, ported from Irdkwia's notes"
    )

    OVERLAY1_D_BOX_LAYOUT_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY1_D_BOX_LAYOUT_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY1_D_BOX_LAYOUT_3 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY1_D_BOX_LAYOUT_4 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    CONTINUE_CHOICE = Symbol(None, None, None, "")

    SUBMENU = Symbol(None, None, None, "")

    MAIN_MENU = Symbol(None, None, None, "")

    OVERLAY1_D_BOX_LAYOUT_5 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY1_D_BOX_LAYOUT_6 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY1_D_BOX_LAYOUT_7 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    MAIN_MENU_CONFIRM = Symbol(None, None, None, "")

    OVERLAY1_D_BOX_LAYOUT_8 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY1_D_BOX_LAYOUT_9 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    MAIN_DEBUG_MENU_1 = Symbol(None, None, None, "")

    OVERLAY1_D_BOX_LAYOUT_10 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    MAIN_DEBUG_MENU_2 = Symbol(None, None, None, "")


class EuItcmOverlay1Section:
    name = "overlay1"
    description = (
        "Likely controls the top menu.\n\nThis is loaded together with overlay 0 while"
        " in the top menu. Since it's in overlay group 1 (together with other 'main'"
        " overlays like overlay 11 and overlay 29), this is probably the"
        " controller.\n\nSeems to contain code related to Wi-Fi rescue. It mentions"
        " several files from the GROUND and BACK folders."
    )
    loadaddress = None
    length = None
    functions = EuItcmOverlay1Functions
    data = EuItcmOverlay1Data


class EuItcmOverlay10Functions:
    SprintfStatic = Symbol(
        None,
        None,
        None,
        (
            "Statically defined copy of sprintf(3) in overlay 10. See arm9.yml for more"
            " information.\n\nr0: str\nr1: format\n...: variadic\nreturn: number of"
            " characters printed, excluding the null-terminator"
        ),
    )

    GetEffectAnimation = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: anim_id\nreturn:"
            " effect animation pointer"
        ),
    )

    GetMoveAnimation = Symbol(
        None,
        None,
        None,
        (
            "Get the move animation corresponding to the given move ID.\n\nr0:"
            " move_id\nreturn: move animation pointer"
        ),
    )

    GetSpecialMonsterMoveAnimation = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: ent_id\nreturn:"
            " special monster move animation pointer"
        ),
    )

    GetTrapAnimation = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: trap_id\nreturn: trap"
            " animation"
        ),
    )

    GetItemAnimation1 = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item_id\nreturn:"
            " first field of the item animation info"
        ),
    )

    GetItemAnimation2 = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: item_id\nreturn:"
            " second field of the item animation info"
        ),
    )

    GetMoveAnimationSpeed = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: move_id\nreturn:"
            " anim_ent_ptr (This might be a mistake? It seems to be an integer, not a"
            " pointer)"
        ),
    )

    CheckEndDungeon = Symbol(
        None,
        None,
        None,
        (
            "Do the stuff when you lose in a dungeon.\n\nNote: unverified, ported from"
            " Irdkwia's notes\n\nr0: End condition code? Seems to control what tasks"
            " get run and what transition happens when the dungeon ends\nreturn: return"
            " code?"
        ),
    )


class EuItcmOverlay10Data:
    FIRST_DUNGEON_WITH_MONSTER_HOUSE_TRAPS = Symbol(
        None,
        None,
        None,
        (
            "The first dungeon that can have extra traps spawn in Monster Houses, Dark"
            " Hill\n\ntype: struct dungeon_id_8"
        ),
    )

    BAD_POISON_DAMAGE_COOLDOWN = Symbol(
        None,
        None,
        None,
        "The number of turns between passive bad poison (toxic) damage.",
    )

    PROTEIN_STAT_BOOST = Symbol(
        None, None, None, "The permanent attack boost from ingesting a Protein."
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
        None,
        None,
        None,
        (
            "The maximum number of enemies that can spawn on a floor without a monster"
            " house (15)."
        ),
    )

    OREN_BERRY_DAMAGE = Symbol(
        None, None, None, "Damage dealt by eating an Oren Berry."
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
        None,
        None,
        None,
        "The chance of an Unown dropping an Unown stone, as a percentage (21%).",
    )

    SITRUS_BERRY_HP_RESTORATION = Symbol(
        None, None, None, "The amount of HP restored by eating a Sitrus Berry."
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
        None,
        None,
        None,
        "The percentage increase in experience from the Exp. Elite IQ skill",
    )

    MONSTER_HOUSE_MAX_NON_MONSTER_SPAWNS = Symbol(
        None,
        None,
        None,
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

    GOLD_THORN_POWER = Symbol(None, None, None, "Attack power for Golden Thorns.")

    SPAWN_COOLDOWN = Symbol(
        None,
        None,
        None,
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
        None,
        None,
        None,
        "The permanent HP boost from eating an Oran Berry at full HP (0).",
    )

    LIFE_SEED_HP_BOOST = Symbol(
        None, None, None, "The permanent HP boost from eating a Life Seed."
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
        None,
        None,
        None,
        "The percentage increase in experience from exp-boosting exclusive items.",
    )

    AFTERMATH_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of the Aftermath ability activating, as a percentage (50%).",
    )

    INTIMIDATOR_ACTIVATION_CHANCE = Symbol(
        None, None, None, "The percentage chance that Intimidator will activate."
    )

    ORAN_BERRY_HP_RESTORATION = Symbol(
        None, None, None, "The amount of HP restored by eating a Oran Berry."
    )

    SITRUS_BERRY_FULL_HP_BOOST = Symbol(
        None,
        None,
        None,
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
        None, None, None, "The number of turns between passive burn damage."
    )

    SHADOW_BALL_LOWER_SPECIAL_DEFENSE_CHANCE = Symbol(
        None,
        None,
        None,
        "The chance of Shadow Ball lowering special defense, as a percentage (20%).",
    )

    STICK_POWER = Symbol(None, None, None, "Attack power for Sticks.")

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
        None,
        None,
        None,
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
        None,
        None,
        None,
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
        None,
        None,
        None,
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
        None,
        None,
        None,
        "The percentage increase in experience from the Miracle Chest item",
    )

    WONDER_CHEST_EXP_BOOST = Symbol(
        None,
        None,
        None,
        "The percentage increase in experience from the Wonder Chest item",
    )

    SPAWN_CAP_WITH_MONSTER_HOUSE = Symbol(
        None,
        None,
        None,
        (
            "The maximum number of enemies that can spawn on a floor with a monster"
            " house, not counting those in the monster house (4)."
        ),
    )

    POISON_DAMAGE_COOLDOWN = Symbol(
        None, None, None, "The number of turns between passive poison damage."
    )

    GEO_PEBBLE_DAMAGE = Symbol(None, None, None, "Damage dealt by Geo Pebbles.")

    GRAVELEROCK_DAMAGE = Symbol(None, None, None, "Damage dealt by Gravelerocks.")

    RARE_FOSSIL_DAMAGE = Symbol(None, None, None, "Damage dealt by Rare Fossils.")

    GINSENG_CHANCE_3 = Symbol(
        None,
        None,
        None,
        (
            "The percentage chance for...something to be set to 3 in a calculation"
            " related to the Ginseng boost."
        ),
    )

    ZINC_STAT_BOOST = Symbol(
        None, None, None, "The permanent special defense boost from ingesting a Zinc."
    )

    IRON_STAT_BOOST = Symbol(
        None, None, None, "The permanent defense boost from ingesting an Iron."
    )

    CALCIUM_STAT_BOOST = Symbol(
        None, None, None, "The permanent special attack boost from ingesting a Calcium."
    )

    DRAGON_RAGE_FIXED_DAMAGE = Symbol(
        None, None, None, "The amount of fixed damage dealt by Dragon Rage (30)."
    )

    CORSOLA_TWIG_POWER = Symbol(None, None, None, "Attack power for Corsola Twigs.")

    CACNEA_SPIKE_POWER = Symbol(None, None, None, "Attack power for Cacnea Spikes.")

    GOLD_FANG_POWER = Symbol(None, None, None, "Attack power for Gold Fangs.")

    SILVER_SPIKE_POWER = Symbol(None, None, None, "Attack power for Silver Spikes.")

    IRON_THORN_POWER = Symbol(None, None, None, "Attack power for Iron Thorns.")

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
        None,
        None,
        None,
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
        None,
        None,
        None,
        (
            "The multiplier for projectile damage from Power Pitcher (1.5), as a binary"
            " fixed-point number (8 fraction bits)"
        ),
    )

    AIR_BLADE_DAMAGE_MULTIPLIER = Symbol(
        None,
        None,
        None,
        (
            "The multiplier for damage from the Air Blade (1.5), as a binary"
            " fixed-point number (8 fraction bits)"
        ),
    )

    HIDDEN_STAIRS_SPAWN_CHANCE_MULTIPLIER = Symbol(
        None,
        None,
        None,
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
        None,
        None,
        None,
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
        None,
        None,
        None,
        (
            "Maps each weather type (by index, see enum weather_id) to the"
            " corresponding Weather Ball type and Castform form.\n\ntype: struct"
            " weather_attributes[8]"
        ),
    )

    OFFENSIVE_STAT_STAGE_MULTIPLIERS = Symbol(
        None,
        None,
        None,
        (
            "Table of multipliers for offensive stats (attack/special attack) for each"
            " stage 0-20, as binary fixed-point numbers (8 fraction bits)"
        ),
    )

    DEFENSIVE_STAT_STAGE_MULTIPLIERS = Symbol(
        None,
        None,
        None,
        (
            "Table of multipliers for defensive stats (defense/special defense) for"
            " each stage 0-20, as binary fixed-point numbers (8 fraction bits)"
        ),
    )

    NATURE_POWER_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Maps enum nature_power_variant to the associated move ID and effect"
            " handler.\n\ntype: struct wildcard_move_desc[15]"
        ),
    )

    APPLES_AND_BERRIES_ITEM_IDS = Symbol(
        None,
        None,
        None,
        (
            "Table of item IDs for Apples and Berries, which trigger the exclusive item"
            " effect EXCLUSIVE_EFF_RECOVER_HP_FROM_APPLES_AND_BERRIES.\n\ntype: struct"
            " item_id_16[66]"
        ),
    )

    RECRUITMENT_LEVEL_BOOST_TABLE = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: int16_t[102]",
    )

    NATURAL_GIFT_ITEM_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Maps items to their type and base power if used with Natural Gift.\n\nAny"
            " item not listed in this table explicitly will be Normal type with a base"
            " power of 1 when used with Natural Gift.\n\ntype: struct"
            " natural_gift_item_info[34]"
        ),
    )

    RANDOM_MUSIC_ID_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Table of music IDs for dungeons with a random assortment of music"
            " tracks.\n\nThis is a table with 30 rows, each with 4 2-byte music IDs."
            " Each row contains the possible music IDs for a given group, from which"
            " the music track will be selected randomly.\n\ntype: struct"
            " music_id_16[30][4]"
        ),
    )

    SHOP_ITEM_CHANCES = Symbol(
        None,
        None,
        None,
        "8 * 6 * 3 * 0x2\n\nNote: unverified, ported from Irdkwia's notes",
    )

    MALE_ACCURACY_STAGE_MULTIPLIERS = Symbol(
        None,
        None,
        None,
        (
            "Table of multipliers for the accuracy stat for males for each stage 0-20,"
            " as binary fixed-point numbers (8 fraction bits)"
        ),
    )

    MALE_EVASION_STAGE_MULTIPLIERS = Symbol(
        None,
        None,
        None,
        (
            "Table of multipliers for the evasion stat for males for each stage 0-20,"
            " as binary fixed-point numbers (8 fraction bits)"
        ),
    )

    FEMALE_ACCURACY_STAGE_MULTIPLIERS = Symbol(
        None,
        None,
        None,
        (
            "Table of multipliers for the accuracy stat for females for each stage"
            " 0-20, as binary fixed-point numbers (8 fraction bits)"
        ),
    )

    FEMALE_EVASION_STAGE_MULTIPLIERS = Symbol(
        None,
        None,
        None,
        (
            "Table of multipliers for the evasion stat for females for each stage 0-20,"
            " as binary fixed-point numbers (8 fraction bits)"
        ),
    )

    MUSIC_ID_TABLE = Symbol(
        None,
        None,
        None,
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
        None,
        None,
        None,
        (
            "Table of type matchups.\n\nEach row corresponds to the type matchups of a"
            " specific attack type, with each entry within the row specifying the"
            " type's effectiveness against a target type.\n\ntype: struct"
            " type_matchup_table"
        ),
    )

    FIXED_ROOM_MONSTER_SPAWN_STATS_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Table of stats for monsters that can spawn in fixed rooms, pointed into by"
            " the FIXED_ROOM_MONSTER_SPAWN_TABLE.\n\nThis is an array of 99 12-byte"
            " entries containing stat spreads for one monster entry each.\n\ntype:"
            " struct fixed_room_monster_spawn_stats_entry[99]"
        ),
    )

    METRONOME_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Something to do with the moves that Metronome can turn into.\n\ntype:"
            " struct wildcard_move_desc[168]"
        ),
    )

    TILESET_PROPERTIES = Symbol(None, None, None, "type: struct tileset_property[199]")

    FIXED_ROOM_PROPERTIES_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Table of properties for fixed rooms.\n\nThis is an array of 256 12-byte"
            " entries containing properties for a given fixed room ID.\n\nSee the"
            " struct definitions and End45's dungeon data document for more"
            " info.\n\ntype: struct fixed_room_properties_entry[256]"
        ),
    )

    TRAP_ANIMATION_INFO = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " trap_animation[26]"
        ),
    )

    ITEM_ANIMATION_INFO = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " item_animation[1400]"
        ),
    )

    MOVE_ANIMATION_INFO = Symbol(None, None, None, "type: struct move_animation[563]")

    EFFECT_ANIMATION_INFO = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " effect_animation[700]"
        ),
    )

    SPECIAL_MONSTER_MOVE_ANIMATION_INFO = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\ntype: struct"
            " special_monster_move_animation[7422]"
        ),
    )


class EuItcmOverlay10Section:
    name = "overlay10"
    description = (
        "Appears to be used both during ground mode and dungeon mode. With dungeon"
        " mode, whereas overlay 29 contains the main dungeon engine, this overlay seems"
        " to contain routines and data for dungeon mechanics."
    )
    loadaddress = None
    length = None
    functions = EuItcmOverlay10Functions
    data = EuItcmOverlay10Data


class EuItcmOverlay11Functions:
    FuncThatCallsCommandParsing = Symbol(None, None, None, "")

    ScriptCommandParsing = Symbol(None, None, None, "")

    SsbLoad2 = Symbol(None, None, None, "")

    StationLoadHanger = Symbol(None, None, None, "")

    ScriptStationLoadTalk = Symbol(None, None, None, "")

    SsbLoad1 = Symbol(None, None, None, "")

    ScriptSpecialProcessCall = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Returns an entry from RECRUITMENT_TABLE_SPECIES.\n\nNote: This indexes"
            " without doing bounds checking.\n\nr0: index into"
            " RECRUITMENT_TABLE_SPECIES\nreturn: enum monster_id"
        ),
    )

    PrepareMenuAcceptTeamMember = Symbol(
        None,
        None,
        None,
        (
            "Implements SPECIAL_PROC_PREPARE_MENU_ACCEPT_TEAM_MEMBER (see"
            " ScriptSpecialProcessCall).\n\nr0: index into RECRUITMENT_TABLE_SPECIES"
        ),
    )

    InitRandomNpcJobs = Symbol(
        None,
        None,
        None,
        (
            "Implements SPECIAL_PROC_INIT_RANDOM_NPC_JOBS (see"
            " ScriptSpecialProcessCall).\n\nr0: job type? 0 is a random NPC job, 1 is a"
            " bottle mission\nr1: ?"
        ),
    )

    GetRandomNpcJobType = Symbol(
        None,
        None,
        None,
        (
            "Implements SPECIAL_PROC_GET_RANDOM_NPC_JOB_TYPE (see"
            " ScriptSpecialProcessCall).\n\nreturn: job type?"
        ),
    )

    GetRandomNpcJobSubtype = Symbol(
        None,
        None,
        None,
        (
            "Implements SPECIAL_PROC_GET_RANDOM_NPC_JOB_SUBTYPE (see"
            " ScriptSpecialProcessCall).\n\nreturn: job subtype?"
        ),
    )

    GetRandomNpcJobStillAvailable = Symbol(
        None,
        None,
        None,
        (
            "Implements SPECIAL_PROC_GET_RANDOM_NPC_JOB_STILL_AVAILABLE (see"
            " ScriptSpecialProcessCall).\n\nreturn: bool"
        ),
    )

    AcceptRandomNpcJob = Symbol(
        None,
        None,
        None,
        (
            "Implements SPECIAL_PROC_ACCEPT_RANDOM_NPC_JOB (see"
            " ScriptSpecialProcessCall).\n\nreturn: bool"
        ),
    )

    GroundMainLoop = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "The GetAllocArena function used for ground mode. See SetMemAllocatorParams"
            " for more information.\n\nr0: initial memory arena pointer, or null\nr1:"
            " flags (see MemAlloc)\nreturn: memory arena pointer, or null"
        ),
    )

    GetFreeArenaGround = Symbol(
        None,
        None,
        None,
        (
            "The GetFreeArena function used for ground mode. See SetMemAllocatorParams"
            " for more information.\n\nr0: initial memory arena pointer, or null\nr1:"
            " pointer to free\nreturn: memory arena pointer, or null"
        ),
    )

    GroundMainReturnDungeon = Symbol(
        None,
        None,
        None,
        (
            "Implements SPECIAL_PROC_RETURN_DUNGEON (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )

    GroundMainNextDay = Symbol(
        None,
        None,
        None,
        (
            "Implements SPECIAL_PROC_NEXT_DAY (see ScriptSpecialProcessCall).\n\nNo"
            " params."
        ),
    )

    JumpToTitleScreen = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Implements SPECIAL_PROC_RETURN_TO_TITLE_SCREEN (see"
            " ScriptSpecialProcessCall).\n\nr0: fade duration\nreturn: bool (but note"
            " that the special process ignores this and always returns 0)"
        ),
    )

    ScriptSpecialProcess0x16 = Symbol(
        None,
        None,
        None,
        "Implements SPECIAL_PROC_0x16 (see ScriptSpecialProcessCall).\n\nr0: bool",
    )

    LoadBackgroundAttributes = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output]"
            " bg_attr_str\nr1: bg_id"
        ),
    )

    LoadMapType10 = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output]"
            " buffer_ptr\nr1: map_id\nr2: dungeon_info_str\nr3: additional_info"
        ),
    )

    LoadMapType11 = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: [output]"
            " buffer_ptr\nr1: map_id\nr2: dungeon_info_str\nr3: additional_info"
        ),
    )

    GetSpecialLayoutBackground = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: bg_id\nr1:"
            " dungeon_info_str\nr2: additional_info\nr3: copy_fixed_room_layout"
        ),
    )

    SetAnimDataFields = Symbol(
        None,
        None,
        None,
        "Sets some fields on the animation struct?\n\nr0: animation pointer\nr1: ?",
    )

    SetAnimDataFieldsWrapper = Symbol(
        None,
        None,
        None,
        "Calls SetAnimDataFields with the second argument right-shifted by 16.",
    )

    InitAnimDataFromOtherAnimData = Symbol(
        None,
        None,
        None,
        (
            "Appears to partially copy some animation data into another animation"
            " struct, plus doing extra initialization on the destination struct.\n\nr0:"
            " dst\nr1: src"
        ),
    )

    SetAnimDataFields2 = Symbol(
        None,
        None,
        None,
        (
            "Sets some fields on the animation struct, based on the params?\n\nr0:"
            " animation pointer\nr1: flags\nr2: ?"
        ),
    )

    LoadObjectAnimData = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Statically defined copy of sprintf(3) in overlay 11. See arm9.yml for more"
            " information.\n\nr0: str\nr1: format\n...: variadic\nreturn: number of"
            " characters printed, excluding the null-terminator"
        ),
    )

    StatusUpdate = Symbol(
        None,
        None,
        None,
        (
            "Implements SPECIAL_PROC_STATUS_UPDATE (see"
            " ScriptSpecialProcessCall).\n\nNo params."
        ),
    )


class EuItcmOverlay11Data:
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
        None,
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\ntype: char[343][12]",
    )

    OBJECTS = Symbol(
        None,
        None,
        None,
        (
            "Table of objects for the script engine, which can be placed in scenes."
            " There are a version-dependent number of 12-byte entries.\n\ntype: struct"
            " script_object[length / 12]"
        ),
    )

    RECRUITMENT_TABLE_LOCATIONS = Symbol(
        None,
        None,
        None,
        (
            "Table of dungeon IDs corresponding to entries in"
            " RECRUITMENT_TABLE_SPECIES.\n\ntype: struct dungeon_id_16[22]"
        ),
    )

    RECRUITMENT_TABLE_LEVELS = Symbol(
        None,
        None,
        None,
        (
            "Table of levels for recruited Pokémon, corresponding to entries in"
            " RECRUITMENT_TABLE_SPECIES.\n\ntype: int16_t[22]"
        ),
    )

    RECRUITMENT_TABLE_SPECIES = Symbol(
        None,
        None,
        None,
        (
            "Table of Pokémon recruited at special locations, such as at the ends of"
            " certain dungeons (e.g., Dialga or the Seven Treasures legendaries) or"
            " during a cutscene (e.g., Cresselia and Manaphy).\n\nInterestingly, this"
            " includes both Heatran genders. It also includes Darkrai for some"
            " reason?\n\ntype: struct monster_id_16[22]"
        ),
    )

    LEVEL_TILEMAP_LIST = Symbol(
        None,
        None,
        None,
        (
            "Irdkwia's notes: FIXED_FLOOR_GROUND_ASSOCIATION\n\ntype: struct"
            " level_tilemap_list_entry[81]"
        ),
    )

    OVERLAY11_OVERLAY_LOAD_TABLE = Symbol(
        None,
        None,
        None,
        (
            "The overlays that can be loaded while this one is loaded.\n\nEach entry is"
            " 16 bytes, consisting of:\n- overlay group ID (see arm9.yml or enum"
            " overlay_group_id in the C headers for a mapping between group ID and"
            " overlay number)\n- function pointer to entry point\n- function pointer to"
            " destructor\n- possibly function pointer to frame-update"
            " function?\n\ntype: struct overlay_load_entry[21]"
        ),
    )

    UNIONALL_RAM_ADDRESS = Symbol(None, None, None, "[Runtime]")

    GROUND_STATE_MAP = Symbol(None, None, None, "[Runtime]")

    GROUND_STATE_PTRS = Symbol(
        None,
        None,
        None,
        (
            "Host pointers to multiple structure used for performing an overworld"
            " scene\n\ntype: struct main_ground_data"
        ),
    )


class EuItcmOverlay11Section:
    name = "overlay11"
    description = (
        "The script engine.\n\nThis is the 'main' overlay of ground mode. The script"
        " engine is what runs the ground mode scripts contained in the SCRIPT folder,"
        " which are written in a custom scripting language. These scripts encode things"
        " like cutscenes, screen transitions, ground mode events, and tons of other"
        " things related to ground mode."
    )
    loadaddress = None
    length = None
    functions = EuItcmOverlay11Functions
    data = EuItcmOverlay11Data


class EuItcmOverlay12Functions:
    pass


class EuItcmOverlay12Data:
    pass


class EuItcmOverlay12Section:
    name = "overlay12"
    description = "Unused; all zeroes."
    loadaddress = None
    length = None
    functions = EuItcmOverlay12Functions
    data = EuItcmOverlay12Data


class EuItcmOverlay13Functions:
    EntryOverlay13 = Symbol(
        None,
        None,
        None,
        (
            "Main function of this overlay.\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nNo params."
        ),
    )

    ExitOverlay13 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    Overlay13SwitchFunctionNa238A1C8 = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: int?",
    )

    Overlay13SwitchFunctionNa238A574 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    GetPersonality = Symbol(
        None,
        None,
        None,
        (
            "Returns the personality obtained after answering all the questions.\n\nThe"
            " value to return is determined by checking the points obtained for each"
            " the personalities and returning the one with the highest amount of"
            " points.\n\nreturn: Personality (0-15)"
        ),
    )

    GetOptionStringFromID = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: switch_case",
    )


class EuItcmOverlay13Data:
    QUIZ_BORDER_COLOR_TABLE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    PORTRAIT_ATTRIBUTES = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_MALE_FEMALE_BOOST_TABLE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY13_UNKNOWN_STRUCT__NA_238C024 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_D_BOX_LAYOUT_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_D_BOX_LAYOUT_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_D_BOX_LAYOUT_3 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_D_BOX_LAYOUT_4 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_MENU_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    STARTERS_PARTNER_IDS = Symbol(None, None, None, "type: struct monster_id_16[21]")

    STARTERS_HERO_IDS = Symbol(None, None, None, "type: struct monster_id_16[32]")

    STARTERS_TYPE_INCOMPATIBILITY_TABLE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    STARTERS_STRINGS = Symbol(None, None, None, "Irdkwia's notes: InsightsStringIDs")

    QUIZ_QUESTION_STRINGS = Symbol(None, None, None, "0x2 * (66 questions)")

    QUIZ_ANSWER_STRINGS = Symbol(
        None, None, None, "0x2 * (175 answers + null-terminator)"
    )

    QUIZ_ANSWER_POINTS = Symbol(
        None,
        None,
        None,
        "0x10 * (174 answers?)\n\nNote: unverified, ported from Irdkwia's notes",
    )

    OVERLAY13_RESERVED_SPACE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY13_UNKNOWN_POINTER__NA_238CEA0 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY13_UNKNOWN_POINTER__NA_238CEA4 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY13_UNKNOWN_POINTER__NA_238CEA8 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_D_BOX_LAYOUT_5 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_D_BOX_LAYOUT_6 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_DEBUG_MENU = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY13_UNKNOWN_STRUCT__NA_238CF14 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    QUIZ_QUESTION_ANSWER_ASSOCIATIONS = Symbol(
        None,
        None,
        None,
        "0x2 * (66 questions)\n\nNote: unverified, ported from Irdkwia's notes",
    )


class EuItcmOverlay13Section:
    name = "overlay13"
    description = (
        "Controls the personality test, including the available partners and playable"
        " Pokémon. The actual personality test questions are stored in the MESSAGE"
        " folder."
    )
    loadaddress = None
    length = None
    functions = EuItcmOverlay13Functions
    data = EuItcmOverlay13Data


class EuItcmOverlay14Functions:
    SentrySetupState = Symbol(
        None,
        None,
        None,
        (
            "Allocates and initializes the sentry duty struct.\n\nPossibly the"
            " entrypoint of this overlay?\n\nr0: controls initial game state? If 2, the"
            " minigame starts in state 4 rather than state 6.\nreturn: always 1"
        ),
    )

    SentryUpdateDisplay = Symbol(
        None,
        None,
        None,
        (
            "Seems to update various parts of the display, such as the round"
            " number.\n\nNo params."
        ),
    )

    SentrySetExitingState = Symbol(
        None,
        None,
        None,
        (
            "Sets the completion state to exiting, triggering the minigame to run its"
            " exit sequence.\n\nNo params."
        ),
    )

    SentryRunState = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Queues up a new intermediate game state to transition to, where the"
            " transition handler will be called immediately by SentryRunState after the"
            " current state handler has returned.\n\nr0: new state"
        ),
    )

    SentryState0 = Symbol(None, None, None, "No params.")

    SentryState1 = Symbol(None, None, None, "No params.")

    SentryState2 = Symbol(None, None, None, "No params.")

    SentryState3 = Symbol(None, None, None, "No params.")

    SentryState4 = Symbol(None, None, None, "No params.")

    SentryStateExit = Symbol(
        None, None, None, "State 0x5: Exit (wraps SentrySetExitingState).\n\nNo params."
    )

    SentryState6 = Symbol(None, None, None, "No params.")

    SentryState7 = Symbol(
        None,
        None,
        None,
        (
            "This state corresponds to when Loudred tells you the instructions for the"
            " minigame (STRING_ID_SENTRY_INSTRUCTIONS).\n\nNo params."
        ),
    )

    SentryState8 = Symbol(None, None, None, "No params.")

    SentryState9 = Symbol(None, None, None, "No params.")

    SentryStateA = Symbol(
        None,
        None,
        None,
        (
            "This state corresponds to when Loudred alerts you that someone is coming"
            " (STRING_ID_SENTRY_HERE_COMES).\n\nNo params."
        ),
    )

    SentryStateB = Symbol(None, None, None, "No params.")

    SentryStateGenerateChoices = Symbol(
        None,
        None,
        None,
        "State 0xC: Generate the four choices for a round.\n\nNo params.",
    )

    SentryStateGetUserChoice = Symbol(
        None,
        None,
        None,
        "State 0xD: Wait for the player to select an answer.\n\nNo params.",
    )

    SentryStateFinalizeRound = Symbol(
        None,
        None,
        None,
        (
            "State 0xE: Deal with the bookkeeping after the player has made a final"
            " choice for the round.\n\nThis includes things like incrementing the round"
            " counter. It also appears to check the final point count on the last round"
            " to determine the player's overall performance.\n\nNo params."
        ),
    )

    SentryStateF = Symbol(None, None, None, "No params.")

    SentryState10 = Symbol(None, None, None, "No params.")

    SentryState11 = Symbol(
        None,
        None,
        None,
        (
            "This state corresponds to when the partner tells you to try again after"
            " the player makes a wrong selection for the first time"
            " (STRING_ID_SENTRY_TRY_AGAIN).\n\nNo params."
        ),
    )

    SentryState12 = Symbol(None, None, None, "No params.")

    SentryState13 = Symbol(
        None,
        None,
        None,
        (
            "This state corresponds to when Loudred tells you that you're out of time"
            " (STRING_ID_SENTRY_OUT_OF_TIME).\n\nNo params."
        ),
    )

    SentryState14 = Symbol(
        None,
        None,
        None,
        (
            "This state corresponds to when the player is shouting their guess"
            " (STRING_ID_SENTRY_FOOTPRINT_IS_6EE), and when Loudred tells the visitor"
            " to come in (STRING_ID_SENTRY_COME_IN_6EF).\n\nNo params."
        ),
    )

    SentryState15 = Symbol(None, None, None, "No params.")

    SentryState16 = Symbol(None, None, None, "No params.")

    SentryState17 = Symbol(
        None,
        None,
        None,
        (
            "This state corresponds to when Loudred tells the player that they chose"
            " the wrong answer (STRING_ID_SENTRY_WRONG,"
            " STRING_ID_SENTRY_BUCK_UP).\n\nNo params."
        ),
    )

    SentryState18 = Symbol(None, None, None, "No params.")

    SentryState19 = Symbol(
        None,
        None,
        None,
        (
            "This state seems to be similar to state 0x14, when the player is shouting"
            " their guess (STRING_ID_SENTRY_FOOTPRINT_IS_6EC), and when Loudred tells"
            " the visitor to come in (STRING_ID_SENTRY_COME_IN_6ED), but used in a"
            " different context (different state transitions to and from this"
            " state).\n\nNo params."
        ),
    )

    SentryState1A = Symbol(None, None, None, "No params.")

    SentryStateFinalizePoints = Symbol(
        None,
        None,
        None,
        (
            "State 0x1B: Apply any modifiers to the player's point total, such as"
            " granting 2000 bonus points for 100% correctness.\n\nNo params."
        ),
    )

    SentryState1C = Symbol(
        None,
        None,
        None,
        (
            "This state corresponds to when Loudred tells the player that they chose"
            " the correct answer ('Yep! Looks like you're right!').\n\nNo params."
        ),
    )

    SentryState1D = Symbol(None, None, None, "No params.")

    SentryState1E = Symbol(
        None,
        None,
        None,
        (
            "This state corresponds to one of the possible dialogue options when you've"
            " finished all the rounds (STRING_ID_SENTRY_KEEP_YOU_WAITING,"
            " STRING_ID_SENTRY_THATLL_DO_IT).\n\nNo params."
        ),
    )

    SentryState1F = Symbol(None, None, None, "No params.")

    SentryState20 = Symbol(
        None,
        None,
        None,
        (
            "This state corresponds to one of the possible dialogue options when you've"
            " finished all the rounds (STRING_ID_SENTRY_NO_MORE_VISITORS,"
            " STRING_ID_SENTRY_THATS_ALL).\n\nNo params."
        ),
    )

    SentryState21 = Symbol(None, None, None, "No params.")


class EuItcmOverlay14Data:
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

    FOOTPRINT_DEBUG_MENU = Symbol(None, None, None, "")

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


class EuItcmOverlay14Section:
    name = "overlay14"
    description = "Runs the sentry duty minigame."
    loadaddress = None
    length = None
    functions = EuItcmOverlay14Functions
    data = EuItcmOverlay14Data


class EuItcmOverlay15Functions:
    pass


class EuItcmOverlay15Data:
    BANK_MAIN_MENU = Symbol(None, None, None, "")

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


class EuItcmOverlay15Section:
    name = "overlay15"
    description = "Controls the Duskull Bank."
    loadaddress = None
    length = None
    functions = EuItcmOverlay15Functions
    data = EuItcmOverlay15Data


class EuItcmOverlay16Functions:
    pass


class EuItcmOverlay16Data:
    EVO_MENU_CONFIRM = Symbol(None, None, None, "Irdkwia's notes: 3*0x8")

    EVO_SUBMENU = Symbol(None, None, None, "Irdkwia's notes: 4*0x8")

    EVO_MAIN_MENU = Symbol(None, None, None, "Irdkwia's notes: 4*0x8")

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


class EuItcmOverlay16Section:
    name = "overlay16"
    description = "Controls Luminous Spring."
    loadaddress = None
    length = None
    functions = EuItcmOverlay16Functions
    data = EuItcmOverlay16Data


class EuItcmOverlay17Functions:
    pass


class EuItcmOverlay17Data:
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

    ASSEMBLY_MENU_CONFIRM = Symbol(None, None, None, "")

    ASSEMBLY_MAIN_MENU_1 = Symbol(None, None, None, "")

    ASSEMBLY_MAIN_MENU_2 = Symbol(None, None, None, "")

    ASSEMBLY_SUBMENU_1 = Symbol(None, None, None, "")

    ASSEMBLY_SUBMENU_2 = Symbol(None, None, None, "")

    ASSEMBLY_SUBMENU_3 = Symbol(None, None, None, "")

    ASSEMBLY_SUBMENU_4 = Symbol(None, None, None, "")

    ASSEMBLY_SUBMENU_5 = Symbol(None, None, None, "")

    ASSEMBLY_SUBMENU_6 = Symbol(None, None, None, "")

    ASSEMBLY_SUBMENU_7 = Symbol(None, None, None, "")

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


class EuItcmOverlay17Section:
    name = "overlay17"
    description = "Controls the Chimecho Assembly."
    loadaddress = None
    length = None
    functions = EuItcmOverlay17Functions
    data = EuItcmOverlay17Data


class EuItcmOverlay18Functions:
    pass


class EuItcmOverlay18Data:
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

    MOVES_MENU_CONFIRM = Symbol(None, None, None, "")

    MOVES_SUBMENU_1 = Symbol(None, None, None, "")

    MOVES_SUBMENU_2 = Symbol(None, None, None, "")

    MOVES_MAIN_MENU = Symbol(None, None, None, "")

    MOVES_SUBMENU_3 = Symbol(None, None, None, "")

    MOVES_SUBMENU_4 = Symbol(None, None, None, "")

    MOVES_SUBMENU_5 = Symbol(None, None, None, "")

    MOVES_SUBMENU_6 = Symbol(None, None, None, "")

    MOVES_SUBMENU_7 = Symbol(None, None, None, "")

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


class EuItcmOverlay18Section:
    name = "overlay18"
    description = "Controls the Electivire Link Shop."
    loadaddress = None
    length = None
    functions = EuItcmOverlay18Functions
    data = EuItcmOverlay18Data


class EuItcmOverlay19Functions:
    GetBarItem = Symbol(
        None,
        None,
        None,
        (
            "Gets the struct bar_item from BAR_AVAILABLE_ITEMS with the specified item"
            " ID.\n\nr0: item ID\nreturn: struct bar_item*"
        ),
    )

    GetRecruitableMonsterAll = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: int?",
    )

    GetRecruitableMonsterList = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: int?",
    )

    GetRecruitableMonsterListRestricted = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: int?",
    )


class EuItcmOverlay19Data:
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

    BAR_MENU_CONFIRM_1 = Symbol(None, None, None, "")

    BAR_MENU_CONFIRM_2 = Symbol(None, None, None, "")

    OVERLAY19_UNKNOWN_STRING_IDS__NA_238E238 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    BAR_MAIN_MENU = Symbol(None, None, None, "")

    BAR_SUBMENU_1 = Symbol(None, None, None, "")

    BAR_SUBMENU_2 = Symbol(None, None, None, "")

    OVERLAY19_RESERVED_SPACE = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY19_UNKNOWN_POINTER__NA_238E360 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY19_UNKNOWN_POINTER__NA_238E364 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )


class EuItcmOverlay19Section:
    name = "overlay19"
    description = "Controls Spinda's Juice Bar."
    loadaddress = None
    length = None
    functions = EuItcmOverlay19Functions
    data = EuItcmOverlay19Data


class EuItcmOverlay2Functions:
    pass


class EuItcmOverlay2Data:
    pass


class EuItcmOverlay2Section:
    name = "overlay2"
    description = (
        "Controls the Nintendo WFC Settings interface, accessed from the top menu"
        " (Other > Nintendo WFC > Nintendo WFC Settings). Presumably contains code for"
        " Nintendo Wi-Fi setup."
    )
    loadaddress = None
    length = None
    functions = EuItcmOverlay2Functions
    data = EuItcmOverlay2Data


class EuItcmOverlay20Functions:
    pass


class EuItcmOverlay20Data:
    OVERLAY20_UNKNOWN_POINTER__NA_238CF7C = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    RECYCLE_MENU_CONFIRM_1 = Symbol(None, None, None, "")

    RECYCLE_MENU_CONFIRM_2 = Symbol(None, None, None, "")

    RECYCLE_SUBMENU_1 = Symbol(None, None, None, "")

    RECYCLE_SUBMENU_2 = Symbol(None, None, None, "")

    RECYCLE_MAIN_MENU_1 = Symbol(None, None, None, "")

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

    RECYCLE_MAIN_MENU_2 = Symbol(None, None, None, "")

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

    RECYCLE_MAIN_MENU_3 = Symbol(None, None, None, "")

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


class EuItcmOverlay20Section:
    name = "overlay20"
    description = "Controls the Recycle Shop."
    loadaddress = None
    length = None
    functions = EuItcmOverlay20Functions
    data = EuItcmOverlay20Data


class EuItcmOverlay21Functions:
    pass


class EuItcmOverlay21Data:
    SWAP_SHOP_D_BOX_LAYOUT_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SWAP_SHOP_MENU_CONFIRM = Symbol(None, None, None, "")

    SWAP_SHOP_SUBMENU_1 = Symbol(None, None, None, "")

    SWAP_SHOP_SUBMENU_2 = Symbol(None, None, None, "")

    SWAP_SHOP_MAIN_MENU_1 = Symbol(None, None, None, "")

    SWAP_SHOP_MAIN_MENU_2 = Symbol(None, None, None, "")

    SWAP_SHOP_SUBMENU_3 = Symbol(None, None, None, "")

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


class EuItcmOverlay21Section:
    name = "overlay21"
    description = "Controls the Croagunk Swap Shop."
    loadaddress = None
    length = None
    functions = EuItcmOverlay21Functions
    data = EuItcmOverlay21Data


class EuItcmOverlay22Functions:
    pass


class EuItcmOverlay22Data:
    SHOP_D_BOX_LAYOUT_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_D_BOX_LAYOUT_2 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY22_UNKNOWN_STRUCT__NA_238E85C = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    SHOP_MENU_CONFIRM = Symbol(None, None, None, "")

    SHOP_MAIN_MENU_1 = Symbol(None, None, None, "")

    SHOP_MAIN_MENU_2 = Symbol(None, None, None, "")

    SHOP_MAIN_MENU_3 = Symbol(None, None, None, "")

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


class EuItcmOverlay22Section:
    name = "overlay22"
    description = "Controls the Kecleon Shop in Treasure Town."
    loadaddress = None
    length = None
    functions = EuItcmOverlay22Functions
    data = EuItcmOverlay22Data


class EuItcmOverlay23Functions:
    pass


class EuItcmOverlay23Data:
    OVERLAY23_UNKNOWN_VALUE__NA_238D2E8 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY23_UNKNOWN_VALUE__NA_238D2EC = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY23_UNKNOWN_STRUCT__NA_238D2F0 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    STORAGE_MENU_CONFIRM = Symbol(None, None, None, "")

    STORAGE_MAIN_MENU_1 = Symbol(None, None, None, "")

    STORAGE_MAIN_MENU_2 = Symbol(None, None, None, "")

    STORAGE_MAIN_MENU_3 = Symbol(None, None, None, "")

    STORAGE_MAIN_MENU_4 = Symbol(None, None, None, "")

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


class EuItcmOverlay23Section:
    name = "overlay23"
    description = (
        "Controls Kangaskhan Storage (both in Treasure Town and via Kangaskhan Rocks)."
    )
    loadaddress = None
    length = None
    functions = EuItcmOverlay23Functions
    data = EuItcmOverlay23Data


class EuItcmOverlay24Functions:
    pass


class EuItcmOverlay24Data:
    OVERLAY24_UNKNOWN_STRUCT__NA_238C508 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY24_UNKNOWN_STRUCT__NA_238C514 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DAYCARE_MENU_CONFIRM = Symbol(None, None, None, "")

    DAYCARE_MAIN_MENU = Symbol(None, None, None, "")

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


class EuItcmOverlay24Section:
    name = "overlay24"
    description = "Controls the Chansey Day Care."
    loadaddress = None
    length = None
    functions = EuItcmOverlay24Functions
    data = EuItcmOverlay24Data


class EuItcmOverlay25Functions:
    pass


class EuItcmOverlay25Data:
    OVERLAY25_UNKNOWN_STRUCT__NA_238B498 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_D_BOX_LAYOUT_1 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    APPRAISAL_MENU_CONFIRM = Symbol(None, None, None, "")

    APPRAISAL_MAIN_MENU = Symbol(None, None, None, "")

    APPRAISAL_SUBMENU = Symbol(None, None, None, "")

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


class EuItcmOverlay25Section:
    name = "overlay25"
    description = "Controls Xatu Appraisal."
    loadaddress = None
    length = None
    functions = EuItcmOverlay25Functions
    data = EuItcmOverlay25Data


class EuItcmOverlay26Functions:
    pass


class EuItcmOverlay26Data:
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


class EuItcmOverlay26Section:
    name = "overlay26"
    description = (
        "Related to mission completion. It's loaded when the dungeon completion summary"
        " is shown upon exiting a dungeon, and during the cutscenes where you collect"
        " mission rewards from clients."
    )
    loadaddress = None
    length = None
    functions = EuItcmOverlay26Functions
    data = EuItcmOverlay26Data


class EuItcmOverlay27Functions:
    pass


class EuItcmOverlay27Data:
    OVERLAY27_UNKNOWN_VALUE__NA_238C948 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY27_UNKNOWN_VALUE__NA_238C94C = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OVERLAY27_UNKNOWN_STRUCT__NA_238C950 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    DISCARD_ITEMS_MENU_CONFIRM = Symbol(None, None, None, "")

    DISCARD_ITEMS_SUBMENU_1 = Symbol(None, None, None, "")

    DISCARD_ITEMS_SUBMENU_2 = Symbol(None, None, None, "")

    DISCARD_ITEMS_MAIN_MENU = Symbol(None, None, None, "")

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


class EuItcmOverlay27Section:
    name = "overlay27"
    description = "Controls the special episode item discard menu."
    loadaddress = None
    length = None
    functions = EuItcmOverlay27Functions
    data = EuItcmOverlay27Data


class EuItcmOverlay28Functions:
    pass


class EuItcmOverlay28Data:
    pass


class EuItcmOverlay28Section:
    name = "overlay28"
    description = "Controls the staff credits sequence."
    loadaddress = None
    length = None
    functions = EuItcmOverlay28Functions
    data = EuItcmOverlay28Data


class EuItcmOverlay29Functions:
    DungeonAlloc = Symbol(
        None,
        None,
        None,
        (
            "Allocates a new dungeon struct.\n\nThis updates the master dungeon pointer"
            " and returns a copy of that pointer.\n\nreturn: pointer to a newly"
            " allocated dungeon struct"
        ),
    )

    GetDungeonPtrMaster = Symbol(
        None,
        None,
        None,
        (
            "Returns the master dungeon pointer (a global, see"
            " DUNGEON_PTR_MASTER).\n\nreturn: pointer to a newly allocated dungeon"
            " struct"
        ),
    )

    DungeonZInit = Symbol(
        None,
        None,
        None,
        (
            "Zero-initializes the dungeon struct pointed to by the master dungeon"
            " pointer.\n\nNo params."
        ),
    )

    DungeonFree = Symbol(
        None,
        None,
        None,
        (
            "Frees the dungeons struct pointer to by the master dungeon pointer, and"
            " nullifies the pointer.\n\nNo params."
        ),
    )

    RunDungeon = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Checks if an entity pointer points to a valid entity (not entity type 0,"
            " which represents no entity).\n\nr0: entity pointer\nreturn: bool"
        ),
    )

    GetFloorType = Symbol(
        None,
        None,
        None,
        (
            "Get the current floor type.\n\nFloor types:\n  0 appears to mean the"
            " current floor is 'normal'\n  1 appears to mean the current floor is a"
            " fixed floor\n  2 means the current floor has a rescue point\n\nreturn:"
            " floor type"
        ),
    )

    TryForcedLoss = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0:"
            " fixed_room_id\nreturn: bool"
        ),
    )

    IsCurrentFixedRoomBossFight = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: bool",
    )

    IsMarowakTrainingMaze = Symbol(
        None,
        None,
        None,
        (
            "Check if the current dungeon is one of the training mazes in Marowak Dojo"
            " (this excludes Final Maze).\n\nreturn: bool"
        ),
    )

    FixedRoomIsSubstituteRoom = Symbol(
        None,
        None,
        None,
        (
            "Checks if the current fixed room is the 'substitute room' (ID"
            " 0x6E).\n\nreturn: bool"
        ),
    )

    StoryRestrictionsEnabled = Symbol(
        None,
        None,
        None,
        (
            "Returns true if certain special restrictions are enabled.\n\nIf true, you"
            " will get kicked out of the dungeon if a team member that passes the"
            " arm9::JoinedAtRangeCheck2 check faints.\n\nreturn:"
            " !dungeon::nonstory_flag || dungeon::hidden_land_flag"
        ),
    )

    GetScenarioBalanceVeneer = Symbol(
        None,
        None,
        None,
        (
            "Likely a linker-generated veneer for GetScenarioBalance.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-"
        ),
    )

    FadeToBlack = Symbol(
        None,
        None,
        None,
        "Fades the screen to black across several frames.\n\nNo params.",
    )

    GetTileAtEntity = Symbol(
        None,
        None,
        None,
        (
            "Returns a pointer to the tile where an entity is located.\n\nr0: pointer"
            " to entity\nreturns: pointer to tile"
        ),
    )

    SpawnTrap = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Checks if a monster can target a position. This function just calls"
            " IsPositionInSight using the position of the user as the origin.\n\nr0:"
            " Entity pointer\nr1: Target position\nreturn: True if the specified"
            " monster can target the target position, false otherwise."
        ),
    )

    GetTeamMemberIndex = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Sets the Map Surveyor flag in the dungeon struct to true if a team member"
            " has Map Surveyor, sets it to false otherwise.\n\nThis function has two"
            " variants: in the EU ROM, it will return true if the flag was changed. The"
            " NA version will return the new value of the flag instead.\n\nreturn: bool"
        ),
    )

    PointCameraToMonster = Symbol(
        None,
        None,
        None,
        "Points the camera to the specified monster.\n\nr0: Entity pointer\nr1: ?",
    )

    UpdateCamera = Symbol(
        None,
        None,
        None,
        (
            "Called every frame. Sets the camera to the right coordinates depending on"
            " the monster it points to.\n\nIt also takes care of updating the minimap,"
            " checking which elements should be shown on it, as well as whether the"
            " screen should be black due to the blinker status.\n\nr0: ?"
        ),
    )

    ItemIsActive = Symbol(
        None,
        None,
        None,
        (
            "Checks if a monster is holding a certain item that isn't disabled by"
            " Klutz.\n\nr0: entity pointer\nr1: item ID\nreturn: bool"
        ),
    )

    GetVisibilityRange = Symbol(
        None,
        None,
        None,
        (
            "Returns dungeon::display_data::visibility_range. If the visibility range"
            " is 0, returns 2 instead.\n\nreturn: Visibility range of the current"
            " floor, or 2 if the visibility is 0."
        ),
    )

    UpdateStatusIconFlags = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Displays the graphical effect on a monster that just recovered PP.\n\nr0:"
            " entity pointer"
        ),
    )

    LoadMappaFileAttributes = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Returns true if the specified monster is included in the floor's monster"
            " spawn list (the modified list after a maximum of 14 different species"
            " were chosen, not the raw list read from the mappa file).\n\nr0: Monster"
            " ID\nreturn: bool"
        ),
    )

    GetMonsterIdToSpawn = Symbol(
        None,
        None,
        None,
        (
            "Get the id of the monster to be randomly spawned.\n\nr0: the spawn weight"
            " to use (0 for normal, 1 for monster house)\nreturn: monster ID"
        ),
    )

    GetMonsterLevelToSpawn = Symbol(
        None,
        None,
        None,
        (
            "Get the level of the monster to be spawned, given its id.\n\nr0: monster"
            " ID\nreturn: Level of the monster to be spawned, or 1 if the specified ID"
            " can't be found on the floor's spawn table."
        ),
    )

    GetDirectionTowardsPosition = Symbol(
        None,
        None,
        None,
        (
            "Gets the direction in which a monster should move to go from the origin"
            " position to the target position\n\nr0: Origin position\nr1: Target"
            " position\nreturn: Direction in which to move to reach the target position"
            " from the origin position"
        ),
    )

    GetChebyshevDistance = Symbol(
        None,
        None,
        None,
        (
            "Returns the Chebyshev distance between two positions. Calculated as"
            " max(abs(x0-x1), abs(y0-y1)).\n\nr0: Position A\nr1: Position B\nreturn:"
            " Chebyshev Distance between position A and position B"
        ),
    )

    IsPositionActuallyInSight = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        "Returns a pointer to the monster data of the current leader.\n\nNo params.",
    )

    TickStatusTurnCounter = Symbol(
        None,
        None,
        None,
        (
            "Ticks down a turn counter for a status condition. If the counter equals"
            " 0x7F, it will not be decreased.\n\nr0: pointer to the status turn"
            " counter\nreturn: new counter value"
        ),
    )

    AdvanceFrame = Symbol(
        None,
        None,
        None,
        (
            "Advances one frame. Does not return until the next frame starts.\n\nr0: ?"
            " - Unused by the function"
        ),
    )

    GenerateDungeonRngSeed = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Gets the current preseed stored in the global dungeon PRNG state. See"
            " GenerateDungeonRngSeed for more information.\n\nreturn: current dungeon"
            " RNG preseed"
        ),
    )

    SetDungeonRngPreseed = Symbol(
        None,
        None,
        None,
        (
            "Sets the preseed in the global dungeon PRNG state. See"
            " GenerateDungeonRngSeed for more information.\n\nr0: preseed"
        ),
    )

    InitDungeonRng = Symbol(
        None,
        None,
        None,
        (
            "Initialize (or reinitialize) the dungeon PRNG with a given seed. The"
            " primary LCG and the five secondary LCGs are initialized jointly, and with"
            " the same seed.\n\nr0: seed"
        ),
    )

    DungeonRand16Bit = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Compute a pseudorandom integer under a given maximum value using the"
            " dungeon PRNG.\n\nr0: high\nreturn: pseudorandom integer on the interval"
            " [0, high - 1]"
        ),
    )

    DungeonRandRange = Symbol(
        None,
        None,
        None,
        (
            "Compute a pseudorandom value between two integers using the dungeon"
            " PRNG.\n\nr0: x\nr1: y\nreturn: pseudorandom integer on the interval"
            " [min(x, y), max(x, y) - 1]"
        ),
    )

    DungeonRandOutcome = Symbol(
        None,
        None,
        None,
        (
            "Returns the result of a possibly biased coin flip (a Bernoulli random"
            " variable) with some success probability p, using the dungeon PRNG.\n\nr0:"
            " success percentage (100*p)\nreturn: true with probability p, false with"
            " probability (1-p)"
        ),
    )

    CalcStatusDuration = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Sets the dungeon PRNG to use one of the 5 secondary LCGs for subsequent"
            " random number generation.\n\nr0: secondary LCG index"
        ),
    )

    DungeonRngSetPrimary = Symbol(
        None,
        None,
        None,
        (
            "Sets the dungeon PRNG to use the primary LCG for subsequent random number"
            " generation.\n\nNo params."
        ),
    )

    ChangeDungeonMusic = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: music ID",
    )

    TrySwitchPlace = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Clears the fields related to AI in the monster's data struct, setting them"
            " all to 0.\nSpecifically, monster::action::action_id,"
            " monster::action::action_use_idx and monster::action::field_0xA are"
            " cleared.\n\nr0: Pointer to the monster's action field"
        ),
    )

    SetMonsterActionFields = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Sets a monster's action to action::ACTION_PASS_TURN or"
            " action::ACTION_WALK, depending on the result of GetCanMoveFlag for the"
            " monster's ID.\n\nr0: Pointer to the monster's action field\nr1:"
            " Monster ID"
        ),
    )

    GetItemAction = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Adds an option to the list of actions that can be taken on a pokémon, item"
            " or move to the currently active sub-menu on dungeon mode (team, moves,"
            " items, etc.).\n\nr0: Action ID\nr1: True if the option should be enabled,"
            " false otherwise"
        ),
    )

    DisableDungeonSubMenuOption = Symbol(
        None,
        None,
        None,
        (
            "Disables an option that was addeed to a dungeon sub-menu.\n\nr0: Action ID"
            " of the option that should be disabled"
        ),
    )

    SetActionRegularAttack = Symbol(
        None,
        None,
        None,
        (
            "Sets a monster's action to action::ACTION_REGULAR_ATTACK, with a specified"
            " direction.\n\nr0: Pointer to the monster's action field\nr1: Direction in"
            " which to use the move. Gets stored in monster::action::direction."
        ),
    )

    SetActionUseMoveAi = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "The main function which executes the actions that take place in a"
            " fractional turn. Called in a loop by RunDungeon while IsFloorOver returns"
            " false.\n\nr0: first loop flag (true when the function is first called"
            " during a floor)"
        ),
    )

    RunLeaderTurn = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Decrements dungeon::wind_turns and displays a wind warning message if"
            " required.\n\nNo params."
        ),
    )

    SetForcedLossReason = Symbol(
        None,
        None,
        None,
        (
            "Sets dungeon::forced_loss_reason to the specified value\n\nr0: Forced loss"
            " reason"
        ),
    )

    GetForcedLossReason = Symbol(
        None,
        None,
        None,
        "Returns dungeon::forced_loss_reason\n\nreturn: forced_loss_reason",
    )

    BindTrapToTile = Symbol(
        None,
        None,
        None,
        (
            "Sets the given tile's associated object to be the given trap, and sets the"
            " visibility of the trap.\n\nr0: tile pointer\nr1: entity pointer\nr2:"
            " visibility flag"
        ),
    )

    SpawnEnemyTrapAtPos = Symbol(
        None,
        None,
        None,
        (
            "A convenience wrapper around SpawnTrap and BindTrapToTile. Always passes 0"
            " for the team parameter (making it an enemy trap).\n\nr0: trap ID\nr1: x"
            " position\nr2: y position\nr3: flags\nstack[0]: visibility flag"
        ),
    )

    DebugRecruitingEnabled = Symbol(
        None,
        None,
        None,
        (
            "Always returns true. Called by SpecificRecruitCheck.\n\nSeems to be a"
            " function used during development to disable recruiting. If it returns"
            " false, SpecificRecruitCheck will also return false.\n\nreturn: true"
        ),
    )

    GetLeaderAction = Symbol(
        None,
        None,
        None,
        (
            "Returns a pointer to the action data of the current leader (field 0x4A on"
            " its monster struct).\n\nNo params."
        ),
    )

    SetLeaderAction = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Zeroes the damage data struct, which is output by the damage calculation"
            " function.\n\nr0: damage data pointer"
        ),
    )

    DungeonGetTotalSpriteFileSize = Symbol(
        None,
        None,
        None,
        (
            "Checks Castform and Cherrim\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: monster ID\nreturn: sprite file size"
        ),
    )

    DungeonGetSpriteIndex = Symbol(
        None,
        None,
        None,
        (
            "Gets the sprite index of the specified monster on this floor\n\nr0:"
            " Monster ID\nreturn: Sprite index of the specified monster ID"
        ),
    )

    JoinedAtRangeCheck2Veneer = Symbol(
        None,
        None,
        None,
        (
            "Likely a linker-generated veneer for arm9::JoinedAtRangeCheck2.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nNo"
            " params."
        ),
    )

    FloorNumberIsEven = Symbol(
        None,
        None,
        None,
        (
            "Checks if the current dungeon floor number is even (probably to determine"
            " whether an enemy spawn should be female).\n\nHas a special check to"
            " return false for Labyrinth Cave B10F (the Gabite boss fight).\n\nreturn:"
            " bool"
        ),
    )

    GetKecleonIdToSpawnByFloor = Symbol(
        None,
        None,
        None,
        (
            "If the current floor number is even, returns female Kecleon's id (0x3D7),"
            " otherwise returns male Kecleon's id (0x17F).\n\nreturn: monster ID"
        ),
    )

    StoreSpriteFileIndexBothGenders = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nr1: file ID",
    )

    LoadMonsterSpriteInner = Symbol(
        None,
        None,
        None,
        "This is called by LoadMonsterSprite a bunch of times.\n\nr0: monster ID",
    )

    SwapMonsterWanFileIndex = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: src_id\nr1: dst_id",
    )

    LoadMonsterSprite = Symbol(
        None,
        None,
        None,
        (
            "Loads the sprite of the specified monster to use it in a"
            " dungeon.\n\nIrdkwia's notes: Handles Castform/Cherrim/Deoxys\n\nr0:"
            " monster ID\nr1: ?"
        ),
    )

    DeleteMonsterSpriteFile = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID",
    )

    DeleteAllMonsterSpriteFiles = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
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
        None,
        None,
        None,
        (
            "Handles a fainted pokémon (reviving does not count as fainting).\n\nr0:"
            " Fainted entity\nr1: Damage source (move ID or greater than the max move"
            " id for other causes)\nr2: Entity responsible of the fainting"
        ),
    )

    UpdateAiTargetPos = Symbol(
        None,
        None,
        None,
        (
            "Given a monster, updates its target_pos field based on its current"
            " position and the direction in which it plans to attack.\n\nr0: Entity"
            " pointer"
        ),
    )

    SetMonsterTypeAndAbility = Symbol(
        None,
        None,
        None,
        (
            "Checks Forecast ability\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: target entity pointer"
        ),
    )

    TryActivateSlowStart = Symbol(
        None,
        None,
        None,
        (
            "Runs a check over all monsters on the field for the ability Slow Start,"
            " and lowers the speed of those who have it.\n\nNo params"
        ),
    )

    TryActivateArtificialWeatherAbilities = Symbol(
        None,
        None,
        None,
        (
            "Runs a check over all monsters on the field for abilities that affect the"
            " weather and changes the floor's weather accordingly.\n\nNo params"
        ),
    )

    GetMonsterApparentId = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: target entity"
            " pointer\nr1: current_id\nreturn: ?"
        ),
    )

    DefenderAbilityIsActive = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Checks if an entity is a monster (entity type 1).\n\nr0: entity"
            " pointer\nreturn: bool"
        ),
    )

    TryActivateTruant = Symbol(
        None,
        None,
        None,
        (
            "Checks if an entity has the ability Truant, and if so tries to apply the"
            " pause status to it.\n\nr0: pointer to entity"
        ),
    )

    TryPointCameraToMonster = Symbol(
        None,
        None,
        None,
        (
            "Attempts to place the camera on top of the specified monster.\n\nIf the"
            " camera is already on top of the specified entity, the function does"
            " nothing.\n\nr0: Entity pointer. Must be a monster, otherwise the function"
            " does nothing.\nr1: ?\nr2: ?"
        ),
    )

    RestorePpAllMovesSetFlags = Symbol(
        None,
        None,
        None,
        (
            "Restores PP for all moves, clears flags move::f_consume_2_pp,"
            " move::flags2_unk5 and move::flags2_unk7, and sets flag"
            " move::f_consume_pp.\nCalled when a monster is revived.\n\nr0: pointer to"
            " entity whose moves will be restored"
        ),
    )

    ShouldMonsterHeadToStairs = Symbol(
        None,
        None,
        None,
        (
            "Checks if a given monster should try to reach the stairs when controlled"
            " by the AI\n\nr0: Entity pointer\nreturn: True if the monster should try"
            " to reach the stairs, false otherwise"
        ),
    )

    MewSpawnCheck = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Checks if a monster is a team member under the effects of a certain"
            " exclusive item effect.\n\nr0: entity pointer\nr1: exclusive item effect"
            " ID\nreturn: bool"
        ),
    )

    GetTeamMemberWithIqSkill = Symbol(
        None,
        None,
        None,
        (
            "Returns an entity pointer to the first team member which has the specified"
            " iq skill.\n\nr0: iq skill id\nreturn: pointer to entity"
        ),
    )

    TeamMemberHasEnabledIqSkill = Symbol(
        None,
        None,
        None,
        (
            "Returns true if any team member has the specified iq skill.\n\nr0: iq"
            " skill id\nreturn: bool"
        ),
    )

    TeamLeaderIqSkillIsEnabled = Symbol(
        None,
        None,
        None,
        (
            "Returns true the leader has the specified iq skill.\n\nr0: iq skill"
            " id\nreturn: bool"
        ),
    )

    HasSuperEffectiveMoveAgainstUser = Symbol(
        None,
        None,
        None,
        (
            "Checks if the target has at least one super effective move against the"
            " user.\n\nr0: User\nr1: Target\nr2: If true, moves with a max Ginseng"
            " boost != 99 will be ignored\nreturn: True if the target has at least one"
            " super effective move against the user, false otherwise."
        ),
    )

    CheckSpawnThreshold = Symbol(
        None,
        None,
        None,
        (
            "Checks if a given monster ID can spawn in dungeons.\n\nThe function"
            " returns true if the monster's spawn threshold value is <="
            " SCENARIO_BALANCE_FLAG\n\nr0: monster ID\nreturn: True if the monster can"
            " spawn, false otherwise"
        ),
    )

    HasLowHealth = Symbol(
        None,
        None,
        None,
        (
            "Checks if the entity passed is a valid monster, and if it's at low health"
            " (below 25% rounded down)\n\nr0: entity pointer\nreturn: bool"
        ),
    )

    AreEntitiesAdjacent = Symbol(
        None,
        None,
        None,
        (
            "Checks whether two entities are adjacent or not.\n\nThe function checks"
            " all 8 possible directions.\n\nr0: First entity\nr1: Second"
            " entity\nreturn: True if both entities are adjacent, false otherwise."
        ),
    )

    IsSpecialStoryAlly = Symbol(
        None,
        None,
        None,
        (
            "Checks if a monster is a special story ally.\n\nThis is a hard-coded check"
            " that looks at the monster's 'Joined At' field. If the value is in the"
            " range [DUNGEON_JOINED_AT_BIDOOF, DUNGEON_DUMMY_0xE3], this check will"
            " return true.\n\nr0: monster pointer\nreturn: bool"
        ),
    )

    IsExperienceLocked = Symbol(
        None,
        None,
        None,
        (
            "Checks if a monster does not gain experience.\n\nThis basically just"
            " inverts IsSpecialStoryAlly, with the exception of also checking for the"
            " 'Joined At' field being DUNGEON_CLIENT (is this set for mission"
            " clients?).\n\nr0: monster pointer\nreturn: bool"
        ),
    )

    InitTeam = Symbol(
        None,
        None,
        None,
        "Seems to initialize the team when entering a dungeon.\n\nr0: ?",
    )

    SpawnMonster = Symbol(
        None,
        None,
        None,
        (
            "Spawns the given monster on a tile.\n\nr0: pointer to struct"
            " spawned_monster_data\nr1: if true, the monster cannot spawn asleep,"
            " otherwise it will randomly be asleep\nreturn: pointer to entity"
        ),
    )

    InitTeamMember = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Initializes a monster struct.\n\nr0: pointer to monster to initialize\nr1:"
            " some flag"
        ),
    )

    ExecuteMonsterAction = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Returns true if the monster has any status problem that prevents it from"
            " acting\n\nr0: Entity pointer\nreturn: True if the specified monster can't"
            " act because of a status problem, false otherwise."
        ),
    )

    CalcSpeedStage = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Calls CalcSpeedStage with a speed counter weight of 1.\n\nr0: pointer to"
            " entity\nreturn: speed stage"
        ),
    )

    GetNumberOfAttacks = Symbol(
        None,
        None,
        None,
        (
            "Returns the number of attacks that a monster can do in one turn (1 or"
            " 2).\n\nChecks for the abilities Swift Swim, Chlorophyll, Unburden, and"
            " for exclusive items.\n\nr0: pointer to entity\nreturns: int"
        ),
    )

    GetMonsterName = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nr0: buffer\nr1: TargetInfo",
    )

    SprintfStatic = Symbol(
        None,
        None,
        None,
        (
            "Statically defined copy of sprintf(3) in overlay 29. See arm9.yml for more"
            " information.\n\nr0: str\nr1: format\n...: variadic\nreturn: number of"
            " characters printed, excluding the null-terminator"
        ),
    )

    IsMonsterCornered = Symbol(
        None,
        None,
        None,
        (
            "True if the given monster is cornered (it can't move in any"
            " direction)\n\nr0: Entity pointer\nreturn: True if the monster can't move"
            " in any direction, false otherwise."
        ),
    )

    CanAttackInDirection = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Checks if a monster should run away from other monsters\n\nr0: Entity"
            " pointer\nreturn: True if the monster should run away, false otherwise"
        ),
    )

    ShouldMonsterRunAwayVariation = Symbol(
        None,
        None,
        None,
        (
            "Calls ShouldMonsterRunAway and returns its result. It also calls another"
            " function if the result was true.\n\nr0: Entity pointer\nr1: ?\nreturn:"
            " Result of the call to ShouldMonsterRunAway"
        ),
    )

    NoGastroAcidStatus = Symbol(
        None,
        None,
        None,
        (
            "Checks if a monster does not have the Gastro Acid status.\n\nr0: entity"
            " pointer\nreturn: bool"
        ),
    )

    AbilityIsActive = Symbol(
        None,
        None,
        None,
        (
            "Checks if a monster has a certain ability that isn't disabled by Gastro"
            " Acid.\n\nr0: entity pointer\nr1: ability ID\nreturn: bool"
        ),
    )

    AbilityIsActiveVeneer = Symbol(
        None,
        None,
        None,
        (
            "Likely a linker-generated veneer for AbilityIsActive.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " entity pointer\nr1: ability ID\nreturn: bool"
        ),
    )

    AbilityIsActiveAnyEntity = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: user entity"
            " pointer\nr1: ability ID\nreturn: bool"
        ),
    )

    LevitateIsActive = Symbol(
        None,
        None,
        None,
        (
            "Checks if a monster is levitating (has the effect of Levitate and Gravity"
            " is not active).\n\nr0: pointer to entity\nreturn: bool"
        ),
    )

    MonsterIsType = Symbol(
        None,
        None,
        None,
        (
            "Checks if a monster is a given type.\n\nr0: entity pointer\nr1: type"
            " ID\nreturn: bool"
        ),
    )

    IsTypeAffectedByGravity = Symbol(
        None,
        None,
        None,
        (
            "Checks if Gravity is active and that the given type is affected (i.e.,"
            " Flying type).\n\nr0: target entity pointer (unused)\nr1: type ID\nreturn:"
            " bool"
        ),
    )

    HasTypeAffectedByGravity = Symbol(
        None,
        None,
        None,
        (
            "Checks if Gravity is active and that the given monster is of an affected"
            " type (i.e., Flying type).\n\nr0: target entity pointer\nr1: type"
            " ID\nreturn: bool"
        ),
    )

    CanSeeInvisibleMonsters = Symbol(
        None,
        None,
        None,
        (
            "Returns whether a certain monster can see other invisible monsters.\nTo be"
            " precise, this function returns true if the monster is holding Goggle"
            " Specs or if it has the status status::STATUS_EYEDROPS.\n\nr0: Entity"
            " pointer\nreturn: True if the monster can see invisible monsters."
        ),
    )

    HasDropeyeStatus = Symbol(
        None,
        None,
        None,
        (
            "Returns whether a certain monster is under the effect of"
            " status::STATUS_DROPEYE.\n\nr0: Entity pointer\nreturn: True if the"
            " monster has dropeye status."
        ),
    )

    IqSkillIsEnabled = Symbol(
        None,
        None,
        None,
        (
            "Checks if a monster has a certain IQ skill enabled.\n\nr0: entity"
            " pointer\nr1: IQ skill ID\nreturn: bool"
        ),
    )

    UpdateIqSkills = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Check the type of a move when used by a certain monster. Accounts for"
            " special cases such as Hidden Power, Weather Ball, the regular"
            " attack...\n\nr0: Entity pointer\nr1: Pointer to move data\nreturn: Type"
            " of the move"
        ),
    )

    GetMovePower = Symbol(
        None,
        None,
        None,
        (
            "Gets the power of a move, factoring in Ginseng/Space Globe boosts.\n\nr0:"
            " user pointer\nr1: move pointer\nreturn: move power"
        ),
    )

    AddExpSpecial = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Checks if the specified enemy should evolve because it just defeated an"
            " ally, and if so, attempts to evolve it.\n\nr0: Pointer to the enemy to"
            " check"
        ),
    )

    TryDecreaseLevel = Symbol(
        None,
        None,
        None,
        (
            "Decrease the target monster's level if possible.\n\nr0: user entity"
            " pointer\nr1: target entity pointer\nr2: number of levels to"
            " decrease\nreturn: success flag"
        ),
    )

    LevelUp = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: user entity"
            " pointer\nr1: target entity pointer\nr2: message flag?\nr3: ?\nreturn:"
            " success flag?"
        ),
    )

    EvolveMonster = Symbol(
        None,
        None,
        None,
        (
            "Makes the specified monster evolve into the specified species.\n\nr0:"
            " Pointer to the entity to evolve\nr1: ?\nr2: Species to evolve into"
        ),
    )

    GetSleepAnimationId = Symbol(
        None,
        None,
        None,
        (
            "Returns the animation id to be applied to a monster that has the sleep,"
            " napping, nightmare or bide status.\n\nReturns a different animation for"
            " sudowoodo and for monsters with infinite sleep turns (0x7F).\n\nr0:"
            " pointer to entity\nreturn: animation ID"
        ),
    )

    DisplayActions = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Cures the target's freeze, shadow hold, ingrain, petrified, constriction"
            " or wrap (both as user and as target) status due to the action of the"
            " user.\n\nr0: pointer to user\nr1: pointer to target\nr2: if true, the"
            " event will be printed to the log"
        ),
    )

    EndCringeClassStatus = Symbol(
        None,
        None,
        None,
        (
            "Cures the target's cringe, confusion, cowering, pause, taunt, encore or"
            " infatuated status due to the action of the user, and prints the event to"
            " the log.\n\nr0: pointer to user\nr1: pointer to target"
        ),
    )

    RunMonsterAi = Symbol(
        None,
        None,
        None,
        (
            "Runs the AI for a single monster to determine whether the monster can act"
            " and which action it should perform if so\n\nr0: Pointer to monster\nr1: ?"
        ),
    )

    ApplyDamage = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Gets the type matchup for a given combat interaction, accounting for both"
            " of the user's types.\n\nCalls GetTypeMatchup twice and combines the"
            " result.\n\nr0: attacker pointer\nr1: defender pointer\nr2: attack"
            " type\nreturn: enum type_matchup"
        ),
    )

    GetTypeMatchup = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "A wrapper around CalcDamageFixed.\n\nr0: attacker pointer\nr1: defender"
            " pointer\nr2: fixed damage\nstack[0]: [output] struct containing info"
            " about the damage calculation\nstack[1]: attack type\nstack[2]: move"
            " category\nstack[3]: damage source\nstack[4]: damage message\nothers: ?"
        ),
    )

    ResetDamageCalcScratchSpace = Symbol(
        None,
        None,
        None,
        (
            "CalcDamage seems to use scratch space of some kind, which this function"
            " zeroes.\n\nNo params."
        ),
    )

    SpecificRecruitCheck = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Determines if a defeated enemy will attempt to join the team\n\nr0: user"
            " entity pointer\nr1: target entity pointer\nreturn: True if the target"
            " will attempt to join the team"
        ),
    )

    TryRecruit = Symbol(
        None,
        None,
        None,
        (
            "Asks the player if they would like to recruit the enemy that was just"
            " defeated and handles the recruitment if they accept.\n\nr0: user entity"
            " pointer\nr1: monster to recruit entity pointer\nreturn: True if the"
            " monster was recruited, false if it wasn't"
        ),
    )

    TrySpawnMonsterAndTickSpawnCounter = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Checks if a monster is holding an aura bow that isn't disabled by"
            " Klutz.\n\nr0: entity pointer\nreturn: bool"
        ),
    )

    ExclusiveItemOffenseBoost = Symbol(
        None,
        None,
        None,
        (
            "Gets the exclusive item boost for attack/special attack for a"
            " monster\n\nr0: entity pointer\nr1: move category index (0 for physical, 1"
            " for special)\nreturn: boost"
        ),
    )

    ExclusiveItemDefenseBoost = Symbol(
        None,
        None,
        None,
        (
            "Gets the exclusive item boost for defense/special defense for a"
            " monster\n\nr0: entity pointer\nr1: move category index (0 for physical, 1"
            " for special)\nreturn: boost"
        ),
    )

    TeamMemberHasExclusiveItemEffectActive = Symbol(
        None,
        None,
        None,
        (
            "Checks if any team member is under the effects of a certain exclusive item"
            " effect.\n\nr0: exclusive item effect ID\nreturn: bool"
        ),
    )

    TrySpawnEnemyItemDrop = Symbol(
        None,
        None,
        None,
        (
            "Determine what item a defeated enemy should drop, if any, then (probably?)"
            " spawn that item underneath them.\n\nThis function is called at the time"
            " when an enemy is defeated from ApplyDamage.\n\nr0: attacker entity (who"
            " defeated the enemy)\nr1: defender entity (who was defeated)"
        ),
    )

    TickNoSlipCap = Symbol(
        None,
        None,
        None,
        (
            "Checks if the entity is a team member and holds the No-Slip Cap, and if so"
            " attempts to make one item in the bag sticky.\n\nr0: pointer to entity"
        ),
    )

    TickStatusAndHealthRegen = Symbol(
        None,
        None,
        None,
        (
            "Applies the natural HP regen effect by taking modifiers into account"
            " (Poison Heal, Heal Ribbon, weather-related regen). Then it ticks down"
            " counters for volatile status effects, and heals them if the counter"
            " reached zero.\n\nr0: pointer to entity"
        ),
    )

    InflictSleepStatusSingle = Symbol(
        None,
        None,
        None,
        (
            "This is called by TryInflictSleepStatus.\n\nr0: entity pointer\nr1: number"
            " of turns"
        ),
    )

    TryInflictSleepStatus = Symbol(
        None,
        None,
        None,
        (
            "Inflicts the Sleep status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2:"
            " number of turns\nr3: flag to log a message on failure"
        ),
    )

    TryInflictNightmareStatus = Symbol(
        None,
        None,
        None,
        (
            "Inflicts the Nightmare status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2:"
            " number of turns"
        ),
    )

    TryInflictNappingStatus = Symbol(
        None,
        None,
        None,
        (
            "Inflicts the Napping status condition (from Rest) on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2:"
            " number of turns"
        ),
    )

    TryInflictYawningStatus = Symbol(
        None,
        None,
        None,
        (
            "Inflicts the Yawning status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2:"
            " number of turns"
        ),
    )

    TryInflictSleeplessStatus = Symbol(
        None,
        None,
        None,
        (
            "Inflicts the Sleepless status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer"
        ),
    )

    TryInflictPausedStatus = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Inflicts the Burn status condition on all team members if possible.\n\nNo"
            " params."
        ),
    )

    TryInflictPoisonedStatus = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Inflicts the Frozen status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: flag"
            " to log a message on failure"
        ),
    )

    TryInflictConstrictionStatus = Symbol(
        None,
        None,
        None,
        (
            "Inflicts the Constriction status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2:"
            " animation ID\nr3: flag to log a message on failure"
        ),
    )

    TryInflictShadowHoldStatus = Symbol(
        None,
        None,
        None,
        (
            "Inflicts the Shadow Hold (AKA Immobilized) status condition on a target"
            " monster if possible.\n\nr0: user entity pointer\nr1: target entity"
            " pointer\nr2: flag to log a message on failure"
        ),
    )

    TryInflictIngrainStatus = Symbol(
        None,
        None,
        None,
        (
            "Inflicts the Ingrain status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer"
        ),
    )

    TryInflictWrappedStatus = Symbol(
        None,
        None,
        None,
        (
            "Inflicts the Wrapped status condition on a target monster if"
            " possible.\n\nThis also gives the user the Wrap status (Wrapped around"
            " foe).\n\nr0: user entity pointer\nr1: target entity pointer"
        ),
    )

    FreeOtherWrappedMonsters = Symbol(
        None,
        None,
        None,
        (
            "Frees from the wrap status all monsters which are wrapped by/around the"
            " monster passed as parameter.\n\nr0: pointer to entity"
        ),
    )

    TryInflictPetrifiedStatus = Symbol(
        None,
        None,
        None,
        (
            "Inflicts the Petrified status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer"
        ),
    )

    LowerOffensiveStat = Symbol(
        None,
        None,
        None,
        (
            "Lowers the specified offensive stat on the target monster.\n\nr0: user"
            " entity pointer\nr1: target entity pointer\nr2: stat index\nr3: number of"
            " stages\nstack[0]: ?\nstack[1]: ?"
        ),
    )

    LowerDefensiveStat = Symbol(
        None,
        None,
        None,
        (
            "Lowers the specified defensive stat on the target monster.\n\nr0: user"
            " entity pointer\nr1: target entity pointer\nr2: stat index\nr3: number of"
            " stages\nstack[0]: ?\nstack[1]: ?"
        ),
    )

    BoostOffensiveStat = Symbol(
        None,
        None,
        None,
        (
            "Boosts the specified offensive stat on the target monster.\n\nr0: user"
            " entity pointer\nr1: target entity pointer\nr2: stat index\nr3: number of"
            " stages"
        ),
    )

    BoostDefensiveStat = Symbol(
        None,
        None,
        None,
        (
            "Boosts the specified defensive stat on the target monster.\n\nr0: user"
            " entity pointer\nr1: target entity pointer\nr2: stat index\nr3: number of"
            " stages"
        ),
    )

    ApplyOffensiveStatMultiplier = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Boosts the specified hit chance stat (accuracy or evasion) on the target"
            " monster.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: stat"
            " index"
        ),
    )

    LowerHitChanceStat = Symbol(
        None,
        None,
        None,
        (
            "Lowers the specified hit chance stat (accuracy or evasion) on the target"
            " monster.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: stat"
            " index\nr3: ? (Irdkwia's notes say this is the number of stages, but I'm"
            " pretty sure that's incorrect)"
        ),
    )

    TryInflictCringeStatus = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "A wrapper around BoostSpeed with the number of stages set to 1.\n\nr0:"
            " user entity pointer\nr1: target entity pointer\nr2: number of turns\nr3:"
            " flag to log a message on failure"
        ),
    )

    LowerSpeed = Symbol(
        None,
        None,
        None,
        (
            "Lowers the speed of the target monster.\n\nr0: user entity pointer\nr1:"
            " target entity pointer\nr2: number of stages\nr3: flag to log a message on"
            " failure"
        ),
    )

    TrySealMove = Symbol(
        None,
        None,
        None,
        (
            "Seals one of the target monster's moves. The move to be sealed is randomly"
            " selected.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: flag"
            " to log a message on failure\nreturn: Whether or not a move was sealed"
        ),
    )

    BoostOrLowerSpeed = Symbol(
        None,
        None,
        None,
        (
            "Randomly boosts or lowers the speed of the target monster by one stage"
            " with equal probability.\n\nr0: user entity pointer\nr1: target entity"
            " pointer"
        ),
    )

    ResetHitChanceStat = Symbol(
        None,
        None,
        None,
        (
            "Resets the specified hit chance stat (accuracy or evasion) back to normal"
            " on the target monster.\n\nr0: user entity pointer\nr1: target entity"
            " pointer\nr2: stat index\nr3: ?"
        ),
    )

    TryActivateQuickFeet = Symbol(
        None,
        None,
        None,
        (
            "Activate the Quick Feet ability on the defender, if the monster has it and"
            " it's active.\n\nr0: attacker pointer\nr1: defender pointer\nreturn: bool,"
            " whether or not the ability was activated"
        ),
    )

    TryInflictConfusedStatus = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Restore HP of the target monster if possible.\n\nr0: user entity"
            " pointer\nr1: target entity pointer\nr2: HP to restore\nreturn: success"
            " flag"
        ),
    )

    TryIncreaseHp = Symbol(
        None,
        None,
        None,
        (
            "Restore HP and possibly boost max HP of the target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: HP"
            " to restore\nr3: max HP boost\nstack[0]: flag to log a message on"
            " failure\nreturn: Success flag"
        ),
    )

    RevealItems = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: user entity"
            " pointer\nr1: target entity pointer"
        ),
    )

    RevealStairs = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: user entity"
            " pointer\nr1: target entity pointer"
        ),
    )

    RevealEnemies = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: user entity"
            " pointer\nr1: target entity pointer"
        ),
    )

    TryInflictLeechSeedStatus = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Inflicts the Destiny Bond status condition on a target monster if"
            " possible.\n\nr0: user entity pointer\nr1: target entity pointer"
        ),
    )

    IsBlinded = Symbol(
        None,
        None,
        None,
        (
            "Returns true if the monster has the blinded status (see"
            " statuses::blinded), or if it is not the leader and is holding Y-Ray"
            " Specs.\n\nr0: pointer to entity\nr1: flag for whether to check for the"
            " held item\nreturn: bool"
        ),
    )

    RestoreMovePP = Symbol(
        None,
        None,
        None,
        (
            "Restores the PP of all the target's moves by the specified amount.\n\nr0:"
            " user entity pointer\nr1: target entity pointer\nr2: PP to restore\nr3:"
            " flag to suppress message logging"
        ),
    )

    SetReflectDamageCountdownTo4 = Symbol(
        None,
        None,
        None,
        (
            "Sets the monster's reflect damage countdown to a global value"
            " (0x4).\n\nr0: pointer to entity"
        ),
    )

    HasConditionalGroundImmunity = Symbol(
        None,
        None,
        None,
        (
            "Checks if a monster is currently immune to Ground-type moves for reasons"
            " other than typing and ability.\n\nThis includes checks for Gravity and"
            " Magnet Rise.\n\nr0: entity pointer\nreturn: bool"
        ),
    )

    Conversion2IsActive = Symbol(
        None,
        None,
        None,
        (
            "Checks if the monster is under the effect of Conversion 2 (its type was"
            " changed).\n\nReturns 1 if the effects is a status, 2 if it comes from an"
            " exclusive item, 0 otherwise.\n\nr0: pointer to entity\nreturn: int"
        ),
    )

    AiConsiderMove = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Checks if a monster should use PP when using a move. It also displays the"
            " corresponding animation if PP Saver triggers and prints the required"
            " messages to the message log.\n\nr0: entity pointer\nreturn: True if the"
            " monster should not use PP, false if it should."
        ),
    )

    GetEntityMoveTargetAndRange = Symbol(
        None,
        None,
        None,
        (
            "Gets the move target-and-range field when used by a given entity. See"
            " struct move_target_and_range in the C headers.\n\nr0: entity pointer\nr1:"
            " move pointer\nr2: AI flag (same as GetMoveTargetAndRange)\nreturn: move"
            " target and range"
        ),
    )

    IsInSpawnList = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: spawn_list_ptr\nr1:"
            " monster ID\nreturn: bool"
        ),
    )

    ChangeShayminForme = Symbol(
        None,
        None,
        None,
        (
            "forme:\n  1: change from Land to Sky\n  2: change from Sky to"
            " Land\nresult:\n  0: not Shaymin\n  1: not correct Forme\n  2: frozen\n "
            " 3: ok\n\nNote: unverified, ported from Irdkwia's notes\n\nr0: Target\nr1:"
            " forme\nreturn: result"
        ),
    )

    ApplyItemEffect = Symbol(
        None,
        None,
        None,
        (
            "Seems to apply an item's effect via a giant switch statement?\n\nr3:"
            " attacker pointer\nstack[0]: defender pointer\nstack[1]: thrown item"
            " pointer\nothers: ?"
        ),
    )

    ViolentSeedBoost = Symbol(
        None,
        None,
        None,
        (
            "Applies the Violent Seed boost to an entity.\n\nr0: attacker pointer\nr1:"
            " defender pointer"
        ),
    )

    ApplyGummiBoostsDungeonMode = Symbol(
        None,
        None,
        None,
        (
            "Applies the IQ and possible stat boosts from eating a Gummi to the target"
            " monster.\n\nr0: user entity pointer\nr1: target entity pointer\nr2: Gummi"
            " type ID\nr3: Stat boost amount, if a random stat boost occurs"
        ),
    )

    GetMaxPpWrapper = Symbol(
        None,
        None,
        None,
        (
            "Gets the maximum PP for a given move. A wrapper around the function in the"
            " ARM 9 binary.\n\nr0: move pointer\nreturn: max PP for the given move,"
            " capped at 99"
        ),
    )

    MoveIsNotPhysical = Symbol(
        None,
        None,
        None,
        "Checks if a move isn't a physical move.\n\nr0: move ID\nreturn: bool",
    )

    TryPounce = Symbol(
        None,
        None,
        None,
        (
            "Makes the target monster execute the Pounce action in a given direction if"
            " possible.\n\nIf the direction ID is 8, the target will pounce in the"
            " direction it's currently facing.\n\nr0: user entity pointer\nr1: target"
            " entity pointer\nr2: direction ID"
        ),
    )

    TryBlowAway = Symbol(
        None,
        None,
        None,
        (
            "Blows away the target monster in a given direction if possible.\n\nr0:"
            " user entity pointer\nr1: target entity pointer\nr2: direction ID"
        ),
    )

    TryExplosion = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Makes the target monster warp if possible.\n\nr0: user entity pointer\nr1:"
            " target entity pointer\nr2: warp type\nr3: position (if warp type is"
            " position-based)"
        ),
    )

    MoveHitCheck = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Checks if a move is a Hyper Beam variant that requires a a turn to"
            " recharge.\n\nInclude moves: Frenzy Plant, Hydro Cannon, Hyper Beam, Blast"
            " Burn, Rock Wrecker, Giga Impact, Roar of Time\n\nr0: move\nreturn: bool"
        ),
    )

    HasMaxGinsengBoost99 = Symbol(
        None,
        None,
        None,
        (
            "Checks if a move has a max Ginseng boost value of 99\n\nr0: Move\nreturn:"
            " True if the move's max Ginseng boost is 99, false otherwise."
        ),
    )

    DungeonRandOutcomeUserTargetInteraction = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Updates the PP of any moves that were used by a monster, if PP should be"
            " consumed.\n\nr0: entity pointer\nr1: flag for whether or not PP should be"
            " consumed"
        ),
    )

    GetDamageSourceWrapper = Symbol(
        None,
        None,
        None,
        (
            "Wraps GetDamageSource (in arm9) for a move info struct rather than a move"
            " ID.\n\nr0: move info pointer\nr1: item ID\nreturn: damage source"
        ),
    )

    LowerSshort = Symbol(
        None,
        None,
        None,
        (
            "Gets the lower 2 bytes of a 4-byte number and interprets it as a signed"
            " short.\n\nr0: 4-byte number x\nreturn: (short) x"
        ),
    )

    GetMoveAnimationId = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Checks whether a moved used by a monster should play its alternative"
            " animation. Includes checks for Curse, Snore, Sleep Talk, Solar Beam and"
            " 2-turn moves.\n\nr0: Pointer to the entity that used the move\nr1: Move"
            " pointer\nreturn: True if the move should play its alternative animation"
        ),
    )

    ExecuteMoveEffect = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Exactly the same as DoMoveDamage, except it appears DealDamage was"
            " inlined.\n\nr0: attacker pointer\nr1: defender pointer\nr2: move\nr3:"
            " item ID\nreturn: whether or not damage was dealt"
        ),
    )

    DealDamage = Symbol(
        None,
        None,
        None,
        (
            "Deals damage from a move or item used by an attacking monster on a"
            " defending monster.\n\nr0: attacker pointer\nr1: defender pointer\nr2:"
            " move\nr3: damage multiplier (as a binary fixed-point number with 8"
            " fraction bits)\nstack[0]: item ID\nreturn: amount of damage dealt"
        ),
    )

    CalcDamageProjectile = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Get the weather, as experienced by a specific entity.\n\nr0: entity"
            " pointer\nreturn: weather ID"
        ),
    )

    TryWeatherFormChange = Symbol(
        None,
        None,
        None,
        (
            "Tries to change a monster into one of its weather-related alternative"
            " forms. Applies to Castform and Cherrim, and checks for their unique"
            " abilities.\n\nr0: pointer to entity"
        ),
    )

    ActivateSportCondition = Symbol(
        None,
        None,
        None,
        (
            "Activates the Mud Sport or Water Sport condition on the dungeon floor for"
            " some number of turns.\n\nr0: water sport flag (false for Mud Sport, true"
            " for Water Sport)"
        ),
    )

    DigitCount = Symbol(
        None,
        None,
        None,
        (
            "Counts the number of digits in a nonnegative integer.\n\nIf the number is"
            " negative, it is cast to a uint16_t before counting digits.\n\nr0:"
            " int\nreturn: number of digits in int"
        ),
    )

    LoadTextureUi = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    DisplayNumberTextureUi = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: x position\nr1: y"
            " position\nr2: number\nr3: ally_mode\nreturn: xsize"
        ),
    )

    DisplayCharTextureUi = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: call_back_str\nr1: x"
            " position\nr2: y position\nr3: char_id\nstack[0]: ?\nreturn: ?"
        ),
    )

    DisplayUi = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    GetTile = Symbol(
        None,
        None,
        None,
        (
            "Get the tile at some position. If the coordinates are out of bounds,"
            " returns a default tile.\n\nr0: x position\nr1: y position\nreturn: tile"
            " pointer"
        ),
    )

    GetTileSafe = Symbol(
        None,
        None,
        None,
        (
            "Get the tile at some position. If the coordinates are out of bounds,"
            " returns a pointer to a copy of the default tile.\n\nr0: x position\nr1: y"
            " position\nreturn: tile pointer"
        ),
    )

    IsFullFloorFixedRoom = Symbol(
        None,
        None,
        None,
        (
            "Checks if the current fixed room on the dungeon generation info"
            " corresponds to a fixed, full-floor layout.\n\nThe first non-full-floor"
            " fixed room is 0xA5, which is for Sealed Chambers.\n\nreturn: bool"
        ),
    )

    GetStairsRoom = Symbol(
        None,
        None,
        None,
        "Returns the index of the room that contains the stairs\n\nreturn: Room index",
    )

    GetRandomSpawnMonsterID = Symbol(
        None,
        None,
        None,
        "Note: unverified, ported from Irdkwia's notes\n\nreturn: monster ID?",
    )

    GravityIsActive = Symbol(
        None, None, None, "Checks if gravity is active on the floor.\n\nreturn: bool"
    )

    ShouldBoostKecleonShopSpawnChance = Symbol(
        None,
        None,
        None,
        (
            "Gets the boost_kecleon_shop_spawn_chance field on the dungeon"
            " struct.\n\nreturn: bool"
        ),
    )

    SetShouldBoostKecleonShopSpawnChance = Symbol(
        None,
        None,
        None,
        (
            "Sets the boost_kecleon_shop_spawn_chance field on the dungeon struct to"
            " the given value.\n\nr0: bool to set the flag to"
        ),
    )

    UpdateShouldBoostKecleonShopSpawnChance = Symbol(
        None,
        None,
        None,
        (
            "Sets the boost_kecleon_shop_spawn_chance field on the dungeon struct"
            " depending on if a team member has the exclusive item effect for more"
            " kecleon shops.\n\nNo params."
        ),
    )

    IsSecretBazaar = Symbol(
        None,
        None,
        None,
        "Checks if the current floor is the Secret Bazaar.\n\nreturn: bool",
    )

    ShouldBoostHiddenStairsSpawnChance = Symbol(
        None,
        None,
        None,
        (
            "Gets the boost_hidden_stairs_spawn_chance field on the dungeon"
            " struct.\n\nreturn: bool"
        ),
    )

    SetShouldBoostHiddenStairsSpawnChance = Symbol(
        None,
        None,
        None,
        (
            "Sets the boost_hidden_stairs_spawn_chance field on the dungeon struct to"
            " the given value.\n\nr0: bool to set the flag to"
        ),
    )

    UpdateShouldBoostHiddenStairsSpawnChance = Symbol(
        None,
        None,
        None,
        (
            "Sets the boost_hidden_stairs_spawn_chance field on the dungeon struct"
            " depending on if a team member has the exclusive item effect for more"
            " hidden stairs.\n\nNo params."
        ),
    )

    IsSecretRoom = Symbol(
        None,
        None,
        None,
        (
            "Checks if the current floor is the Secret Room fixed floor (from hidden"
            " stairs).\n\nreturn: bool"
        ),
    )

    IsSecretFloor = Symbol(
        None,
        None,
        None,
        (
            "Checks if the current floor is a secret bazaar or a secret"
            " room.\n\nreturn: bool"
        ),
    )

    GetDungeonGenInfoUnk0C = Symbol(
        None, None, None, "return: dungeon_generation_info::field_0xc"
    )

    GetMinimapData = Symbol(
        None,
        None,
        None,
        (
            "Returns a pointer to the minimap_display_data struct in the dungeon"
            " struct.\n\nreturn: minimap_display_data*"
        ),
    )

    SetMinimapDataE447 = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Sets minimap_display_data::field_0xE448 to the specified value\n\nr0:"
            " Value to set the field to"
        ),
    )

    LoadFixedRoomDataVeneer = Symbol(
        None,
        None,
        None,
        (
            "Likely a linker-generated veneer for LoadFixedRoomData.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nNo"
            " params."
        ),
    )

    IsNormalFloor = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        "Gets the terrain type of a tile.\n\nr0: tile pointer\nreturn: terrain ID",
    )

    DungeonRand100 = Symbol(
        None,
        None,
        None,
        (
            "Compute a pseudorandom integer on the interval [0, 100) using the dungeon"
            " PRNG.\n\nreturn: pseudorandom integer"
        ),
    )

    ClearHiddenStairs = Symbol(
        None,
        None,
        None,
        (
            "Clears the tile (terrain and spawns) on which Hidden Stairs are spawned,"
            " if applicable.\n\nNo params."
        ),
    )

    FlagHallwayJunctions = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Generates a floor layout with a 4x2 grid of rooms, surrounded by an outer"
            " ring of hallways.\n\nr0: floor properties"
        ),
    )

    GenerateCrossroadsFloor = Symbol(
        None,
        None,
        None,
        (
            "Generates a floor layout with a mesh of hallways on the interior 3x2 grid,"
            " surrounded by a boundary of rooms protruding from the interior like"
            " spikes, excluding the corner cells.\n\nr0: floor properties"
        ),
    )

    GenerateLineFloor = Symbol(
        None,
        None,
        None,
        (
            "Generates a floor layout with 5 grid cells in a horizontal line.\n\nr0:"
            " floor properties"
        ),
    )

    GenerateCrossFloor = Symbol(
        None,
        None,
        None,
        (
            "Generates a floor layout with 5 rooms arranged in a cross ('plus sign')"
            " formation.\n\nr0: floor properties"
        ),
    )

    GenerateBeetleFloor = Symbol(
        None,
        None,
        None,
        (
            "Generates a floor layout in a 'beetle' formation, which is created by"
            " taking a 3x3 grid of rooms, connecting the rooms within each row, and"
            " merging the central column into one big room.\n\nr0: floor properties"
        ),
    )

    MergeRoomsVertically = Symbol(
        None,
        None,
        None,
        (
            "Merges two vertically stacked rooms into one larger room.\n\nr0: x grid"
            " coordinate of the rooms to merge\nr1: y grid coordinate of the upper"
            " room\nr2: dy, where the lower room has a y grid coordinate of y+dy\nr3:"
            " grid to update"
        ),
    )

    GenerateOuterRoomsFloor = Symbol(
        None,
        None,
        None,
        (
            "Generates a floor layout with a ring of rooms on the grid boundary and"
            " nothing in the interior.\n\nNote that this function is bugged, and won't"
            " properly connect all the rooms together for grid_size_x < 4.\n\nr0: grid"
            " size x\nr1: grid size y\nr2: floor properties"
        ),
    )

    IsNotFullFloorFixedRoom = Symbol(
        None,
        None,
        None,
        (
            "Checks if a fixed room ID does not correspond to a fixed, full-floor"
            " layout.\n\nThe first non-full-floor fixed room is 0xA5, which is for"
            " Sealed Chambers.\n\nr0: fixed room ID\nreturn: bool"
        ),
    )

    GenerateFixedRoom = Symbol(
        None,
        None,
        None,
        (
            "Handles fixed room generation if the floor contains a fixed room.\n\nr0:"
            " fixed room ID\nr1: floor properties\nreturn: bool"
        ),
    )

    GenerateOneRoomMonsterHouseFloor = Symbol(
        None,
        None,
        None,
        (
            "Generates a floor layout with just a large, one-room Monster"
            " House.\n\nThis is the default layout if dungeon generation fails.\n\nNo"
            " params."
        ),
    )

    GenerateTwoRoomsWithMonsterHouseFloor = Symbol(
        None,
        None,
        None,
        (
            "Generate a floor layout with two rooms (left and right), one of which is a"
            " Monster House.\n\nNo params."
        ),
    )

    GenerateExtraHallways = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Get the grid cell positions for a given set of floor grid"
            " dimensions.\n\nr0: [output] pointer to array of the starting x"
            " coordinates of each grid column\nr1: [output] pointer to array of the"
            " starting y coordinates of each grid row\nr2: grid size x\nr3: grid size y"
        ),
    )

    InitDungeonGrid = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        "Set spawn flag 5 (0b100000 or 0x20) on all tiles in a room.\n\nr0: grid cell",
    )

    IsNextToHallway = Symbol(
        None,
        None,
        None,
        (
            "Checks if a tile position is either in a hallway or next to one.\n\nr0:"
            " x\nr1: y\nreturn: bool"
        ),
    )

    ResolveInvalidSpawns = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        "Converts all secondary terrain tiles (water/lava) to chasms.\n\nNo params.",
    )

    EnsureImpassableTilesAreWalls = Symbol(
        None,
        None,
        None,
        "Ensures all tiles with the impassable flag are walls.\n\nNo params.",
    )

    InitializeTile = Symbol(
        None, None, None, "Initialize a tile struct.\n\nr0: tile pointer"
    )

    ResetFloor = Symbol(
        None,
        None,
        None,
        (
            "Resets the floor in preparation for a floor generation attempt.\n\nResets"
            " all tiles, resets the border to be impassable, and clears entity"
            " spawns.\n\nNo params."
        ),
    )

    PosIsOutOfBounds = Symbol(
        None,
        None,
        None,
        (
            "Checks if a position (x, y) is out of bounds on the map: !((0 <= x <= 55)"
            " && (0 <= y <= 31)).\n\nr0: x\nr1: y\nreturn: bool"
        ),
    )

    ShuffleSpawnPositions = Symbol(
        None,
        None,
        None,
        (
            "Randomly shuffle an array of spawn positions.\n\nr0: spawn position array"
            " containing bytes {x1, y1, x2, y2, ...}\nr1: number of (x, y) pairs in the"
            " spawn position array"
        ),
    )

    SpawnNonEnemies = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Set a specific tile to have secondary terrain (water/lava), but only if"
            " it's a passable wall.\n\nr0: tile pointer"
        ),
    )

    GenerateSecondaryTerrainFormations = Symbol(
        None,
        None,
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
        None,
        None,
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
        None, None, None, "Converts all wall tiles to chasms.\n\nNo params."
    )

    ResetInnerBoundaryTileRows = Symbol(
        None,
        None,
        None,
        (
            "Reset the inner boundary tile rows (y == 1 and y == 30) to their initial"
            " state of all wall tiles, with impassable walls at the edges (x == 0 and x"
            " == 55).\n\nNo params."
        ),
    )

    ResetImportantSpawnPositions = Symbol(
        None,
        None,
        None,
        (
            "Resets important spawn positions (the player, stairs, and hidden stairs)"
            " back to their default values.\n\nr0: dungeon generation info pointer (a"
            " field on the dungeon struct)"
        ),
    )

    SpawnStairs = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Resets hidden stairs spawn information for the floor. This includes the"
            " position on the floor generation status as well as the flag indicating"
            " whether the spawn was blocked.\n\nNo params."
        ),
    )

    LoadFixedRoomData = Symbol(
        None,
        None,
        None,
        (
            "Loads fixed room data from BALANCE/fixed.bin into the buffer pointed to by"
            " FIXED_ROOM_DATA_PTR.\n\nNo params."
        ),
    )

    LoadFixedRoom = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes"
    )

    OpenFixedBin = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    CloseFixedBin = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    AreOrbsAllowed = Symbol(
        None,
        None,
        None,
        (
            "Checks if orbs are usable in the given fixed room.\n\nAlways true if not a"
            " full-floor fixed room.\n\nr0: fixed room ID\nreturn: bool"
        ),
    )

    AreTileJumpsAllowed = Symbol(
        None,
        None,
        None,
        (
            "Checks if tile jumps (warping, being blown away, and leaping) are allowed"
            " in the given fixed room.\n\nAlways true if not a full-floor fixed"
            " room.\n\nr0: fixed room ID\nreturn: bool"
        ),
    )

    AreTrawlOrbsAllowed = Symbol(
        None,
        None,
        None,
        (
            "Checks if Trawl Orbs work in the given fixed room.\n\nAlways true if not a"
            " full-floor fixed room.\n\nr0: fixed room ID\nreturn: bool"
        ),
    )

    AreOrbsAllowedVeneer = Symbol(
        None,
        None,
        None,
        (
            "Likely a linker-generated veneer for InitMemAllocTable.\n\nSee"
            " https://developer.arm.com/documentation/dui0474/k/image-structure-and-generation/linker-generated-veneers/what-is-a-veneer-\n\nr0:"
            " fixed room ID\nreturn: bool"
        ),
    )

    AreLateGameTrapsEnabled = Symbol(
        None,
        None,
        None,
        (
            "Check if late-game traps (Summon, Pitfall, and Pokémon traps) work in the"
            " given fixed room.\n\nOr disabled? This function, which Irdkwia's notes"
            " label as a disable check, check the struct field labeled in End's notes"
            " as an enable flag.\n\nr0: fixed room ID\nreturn: bool"
        ),
    )

    AreMovesEnabled = Symbol(
        None,
        None,
        None,
        (
            "Checks if moves (excluding the regular attack) are usable in the given"
            " fixed room.\n\nr0: fixed room ID\nreturn: bool"
        ),
    )

    IsRoomIlluminated = Symbol(
        None,
        None,
        None,
        (
            "Checks if the given fixed room is fully illuminated.\n\nr0: fixed room"
            " ID\nreturn: bool"
        ),
    )

    GetMatchingMonsterId = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: monster ID\nr1:"
            " ?\nr2: ?\nreturn: monster ID"
        ),
    )

    GenerateItemExplicit = Symbol(
        None,
        None,
        None,
        (
            "Initializes an item struct with the given information.\n\nThis calls"
            " InitStandardItem, then explicitly sets the quantity and stickiness. If"
            " quantity == 0 for Poké, GenerateCleanItem is used instead.\n\nr0: pointer"
            " to item to initialize\nr1: item ID\nr2: quantity\nr3: sticky flag"
        ),
    )

    GenerateAndSpawnItem = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Checks if the current floor is either the Secret Bazaar or a Secret"
            " Room.\n\nreturn: bool"
        ),
    )

    GenerateStandardItem = Symbol(
        None,
        None,
        None,
        (
            "Wrapper around GenerateItem with quantity set to 0\n\nr0: pointer to item"
            " to initialize\nr1: item ID\nr2: stickiness type"
        ),
    )

    GenerateCleanItem = Symbol(
        None,
        None,
        None,
        (
            "Wrapper around GenerateItem with quantity set to 0 and stickiness type set"
            " to SPAWN_STICKY_NEVER.\n\nr0: pointer to item to initialize\nr1: item ID"
        ),
    )

    SpawnItem = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Wraps SpawnEnemyItemDrop in a more convenient interface.\n\nr0:"
            " entity\nr1: position\nr2: item\nr3: ?"
        ),
    )

    SpawnEnemyItemDrop = Symbol(
        None,
        None,
        None,
        (
            "Appears to spawn an enemy item drop at a specified location, with a log"
            " message.\n\nr0: entity\nr1: item entity\nr2: item info\nr3: ?\nstack[0]:"
            " pointer to int16_t[2] for x/y direction (corresponding to"
            " DIRECTIONS_XY)\nstack[1]: ?"
        ),
    )

    TryGenerateUnownStoneDrop = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Checks if a monster has a certain held item.\n\nr0: entity pointer\nr1:"
            " item ID\nreturn: bool"
        ),
    )

    GenerateMoneyQuantity = Symbol(
        None,
        None,
        None,
        (
            "Set the quantity code on an item (assuming it's Poké), given some maximum"
            " acceptable money amount.\n\nr0: item pointer\nr1: max money amount"
            " (inclusive)"
        ),
    )

    CheckTeamItemsFlags = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Checks if there's an active challenge request on the current"
            " dungeon.\n\nreturn: True if there's an active challenge request on the"
            " current dungeon in the list of missions."
        ),
    )

    IsOutlawOrChallengeRequestFloor = Symbol(
        None,
        None,
        None,
        (
            "Checks if the current floor is an active mission destination of type"
            " MISSION_TAKE_ITEM_FROM_OUTLAW, MISSION_ARREST_OUTLAW or"
            " MISSION_CHALLENGE_REQUEST.\n\nreturn: bool"
        ),
    )

    IsDestinationFloor = Symbol(
        None,
        None,
        None,
        "Checks if the current floor is a mission destination floor.\n\nreturn: bool",
    )

    IsCurrentMissionType = Symbol(
        None,
        None,
        None,
        (
            "Checks if the current floor is an active mission destination of a given"
            " type (and any subtype).\n\nr0: mission type\nreturn: bool"
        ),
    )

    IsCurrentMissionTypeExact = Symbol(
        None,
        None,
        None,
        (
            "Checks if the current floor is an active mission destination of a given"
            " type and subtype.\n\nr0: mission type\nr1: mission subtype\nreturn: bool"
        ),
    )

    IsOutlawMonsterHouseFloor = Symbol(
        None,
        None,
        None,
        (
            "Checks if the current floor is a mission destination for a Monster House"
            " outlaw mission.\n\nreturn: bool"
        ),
    )

    IsGoldenChamber = Symbol(
        None,
        None,
        None,
        "Checks if the current floor is a Golden Chamber floor.\n\nreturn: bool",
    )

    IsLegendaryChallengeFloor = Symbol(
        None,
        None,
        None,
        (
            "Checks if the current floor is a boss floor for a Legendary Challenge"
            " Letter mission.\n\nreturn: bool"
        ),
    )

    IsJirachiChallengeFloor = Symbol(
        None,
        None,
        None,
        (
            "Checks if the current floor is the boss floor in Star Cave Pit for"
            " Jirachi's Challenge Letter mission.\n\nreturn: bool"
        ),
    )

    IsDestinationFloorWithMonster = Symbol(
        None,
        None,
        None,
        (
            "Checks if the current floor is a mission destination floor with a special"
            " monster.\n\nSee FloorHasMissionMonster for details.\n\nreturn: bool"
        ),
    )

    LoadMissionMonsterSprites = Symbol(
        None,
        None,
        None,
        (
            "Loads the sprites of monsters that appear on the current floor because of"
            " a mission, if applicable.\n\nThis includes monsters to be rescued,"
            " outlaws and its minions.\n\nNo params."
        ),
    )

    MissionTargetEnemyIsDefeated = Symbol(
        None,
        None,
        None,
        (
            "Checks if the target enemy of the mission on the current floor has been"
            " defeated.\n\nreturn: bool"
        ),
    )

    SetMissionTargetEnemyDefeated = Symbol(
        None,
        None,
        None,
        (
            "Set the flag for whether or not the target enemy of the current mission"
            " has been defeated.\n\nr0: new flag value"
        ),
    )

    IsDestinationFloorWithFixedRoom = Symbol(
        None,
        None,
        None,
        (
            "Checks if the current floor is a mission destination floor with a fixed"
            " room.\n\nThe entire floor can be a fixed room layout, or it can just"
            " contain a Sealed Chamber.\n\nreturn: bool"
        ),
    )

    GetItemToRetrieve = Symbol(
        None,
        None,
        None,
        (
            "Get the ID of the item that needs to be retrieve on the current floor for"
            " a mission, if one exists.\n\nreturn: item ID"
        ),
    )

    GetItemToDeliver = Symbol(
        None,
        None,
        None,
        (
            "Get the ID of the item that needs to be delivered to a mission client on"
            " the current floor, if one exists.\n\nreturn: item ID"
        ),
    )

    GetSpecialTargetItem = Symbol(
        None,
        None,
        None,
        (
            "Get the ID of the special target item for a Sealed Chamber or Treasure"
            " Memo mission on the current floor.\n\nreturn: item ID"
        ),
    )

    IsDestinationFloorWithItem = Symbol(
        None,
        None,
        None,
        (
            "Checks if the current floor is a mission destination floor with a special"
            " item.\n\nThis excludes missions involving taking an item from an"
            " outlaw.\n\nreturn: bool"
        ),
    )

    IsDestinationFloorWithHiddenOutlaw = Symbol(
        None,
        None,
        None,
        (
            "Checks if the current floor is a mission destination floor with a 'hidden"
            " outlaw' that behaves like a normal enemy.\n\nreturn: bool"
        ),
    )

    IsDestinationFloorWithFleeingOutlaw = Symbol(
        None,
        None,
        None,
        (
            "Checks if the current floor is a mission destination floor with a 'fleeing"
            " outlaw' that runs away.\n\nreturn: bool"
        ),
    )

    GetMissionTargetEnemy = Symbol(
        None,
        None,
        None,
        (
            "Get the monster ID of the target enemy to be defeated on the current floor"
            " for a mission, if one exists.\n\nreturn: monster ID"
        ),
    )

    GetMissionEnemyMinionGroup = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Sets dungeon::target_monster_not_found_flag to the specified value.\n\nr0:"
            " Value to set the flag to"
        ),
    )

    GetTargetMonsterNotFoundFlag = Symbol(
        None,
        None,
        None,
        (
            "Gets the value of dungeon::target_monster_not_found_flag.\n\nreturn:"
            " dungeon::target_monster_not_found_flag"
        ),
    )

    FloorHasMissionMonster = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Generates the monster ID in the egg from the given mission. Uses the base"
            " form of the monster.\n\nNote: unverified, ported from Irdkwia's"
            " notes\n\nr0: mission struct"
        ),
    )

    LogMessageByIdWithPopupCheckUser = Symbol(
        None,
        None,
        None,
        (
            "Logs a message in the message log alongside a message popup, if the user"
            " hasn't fainted.\n\nr0: user entity pointer\nr1: message ID"
        ),
    )

    LogMessageWithPopupCheckUser = Symbol(
        None,
        None,
        None,
        (
            "Logs a message in the message log alongside a message popup, if the user"
            " hasn't fainted.\n\nr0: user entity pointer\nr1: message string"
        ),
    )

    LogMessageByIdQuiet = Symbol(
        None,
        None,
        None,
        (
            "Logs a message in the message log (but without a message popup).\n\nr0:"
            " user entity pointer\nr1: message ID"
        ),
    )

    LogMessageQuiet = Symbol(
        None,
        None,
        None,
        (
            "Logs a message in the message log (but without a message popup).\n\nr0:"
            " user entity pointer\nr1: message string"
        ),
    )

    LogMessageByIdWithPopupCheckUserTarget = Symbol(
        None,
        None,
        None,
        (
            "Logs a message in the message log alongside a message popup, if some user"
            " check passes and the target hasn't fainted.\n\nr0: user entity"
            " pointer\nr1: target entity pointer\nr2: message ID"
        ),
    )

    LogMessageWithPopupCheckUserTarget = Symbol(
        None,
        None,
        None,
        (
            "Logs a message in the message log alongside a message popup, if some user"
            " check passes and the target hasn't fainted.\n\nr0: user entity"
            " pointer\nr1: target entity pointer\nr2: message string"
        ),
    )

    LogMessageByIdQuietCheckUserTarget = Symbol(
        None,
        None,
        None,
        (
            "Logs a message in the message log (but without a message popup), if some"
            " user check passes and the target hasn't fainted.\n\nr0: user entity"
            " pointer\nr1: target entity pointer\nr2: message ID"
        ),
    )

    LogMessageByIdWithPopupCheckUserUnknown = Symbol(
        None,
        None,
        None,
        (
            "Logs a message in the message log alongside a message popup, if the user"
            " hasn't fainted and some other unknown check.\n\nr0: user entity"
            " pointer\nr1: ?\nr2: message ID"
        ),
    )

    LogMessageByIdWithPopup = Symbol(
        None,
        None,
        None,
        (
            "Logs a message in the message log alongside a message popup.\n\nr0: user"
            " entity pointer\nr1: message ID"
        ),
    )

    LogMessageWithPopup = Symbol(
        None,
        None,
        None,
        (
            "Logs a message in the message log alongside a message popup.\n\nr0: user"
            " entity pointer\nr1: message string"
        ),
    )

    LogMessage = Symbol(
        None,
        None,
        None,
        (
            "Logs a message in the message log.\n\nr0: user entity pointer\nr1: message"
            " string\nr2: bool, whether or not to present a message popup"
        ),
    )

    LogMessageById = Symbol(
        None,
        None,
        None,
        (
            "Logs a message in the message log.\n\nr0: user entity pointer\nr1: message"
            " ID\nr2: bool, whether or not to present a message popup"
        ),
    )

    OpenMessageLog = Symbol(
        None, None, None, "Opens the message log window.\n\nr0: ?\nr1: ?"
    )

    RunDungeonMode = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "This changes the palettes of windows in both screens to an appropiate"
            " value depending on the playthrough\nIf you're in a special episode, they"
            " turn green , otherwise, they turn blue or pink depending on your"
            " character's sex\n\nNo params"
        ),
    )

    GetPersonalityIndex = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: monster"
            " pointer\nreturn: ?"
        ),
    )

    DisplayMessage = Symbol(
        None,
        None,
        None,
        (
            "Displays a message in a dialogue box that optionally waits for player"
            " input before closing.\n\nr0: ?\nr1: ID of the string to display\nr2: True"
            " to wait for player input before closing the dialogue box, false to close"
            " it automatically once all the characters get printed."
        ),
    )

    DisplayMessage2 = Symbol(None, None, None, "Very similar to DisplayMessage")

    YesNoMenu = Symbol(
        None,
        None,
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
        None,
        None,
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

    OpenMenu = Symbol(None, None, None, "Note: unverified, ported from Irdkwia's notes")

    OthersMenuLoop = Symbol(
        None,
        None,
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
        None,
        None,
        None,
        (
            "Called when the in-dungeon 'others' menu is open. Does not return until"
            " the menu is closed.\n\nreturn: Always 0"
        ),
    )


class EuItcmOverlay29Data:
    DUNGEON_STRUCT_SIZE = Symbol(
        None, None, None, "Size of the dungeon struct (0x2CB14)"
    )

    MAX_HP_CAP = Symbol(
        None, None, None, "The maximum amount of HP a monster can have (999)."
    )

    OFFSET_OF_DUNGEON_FLOOR_PROPERTIES = Symbol(
        None,
        None,
        None,
        "Offset of the floor properties field in the dungeon struct (0x286B2)",
    )

    SPAWN_RAND_MAX = Symbol(
        None,
        None,
        None,
        (
            "Equal to 10,000 (0x2710). Used as parameter for DungeonRandInt to generate"
            " the random number which determines the entity to spawn."
        ),
    )

    DUNGEON_PRNG_LCG_MULTIPLIER = Symbol(
        None,
        None,
        None,
        (
            "The multiplier shared by all of the dungeon PRNG's LCGs, 1566083941"
            " (0x5D588B65)."
        ),
    )

    DUNGEON_PRNG_LCG_INCREMENT_SECONDARY = Symbol(
        None,
        None,
        None,
        (
            "The increment for the dungeon PRNG's secondary LCGs, 2531011 (0x269EC3)."
            " This happens to be the same increment that the Microsoft Visual C++"
            " runtime library uses in its implementation of the rand() function."
        ),
    )

    KECLEON_FEMALE_ID = Symbol(
        None,
        None,
        None,
        "0x3D7 (983). Used when spawning Kecleon on an even numbered floor.",
    )

    KECLEON_MALE_ID = Symbol(
        None,
        None,
        None,
        "0x17F (383). Used when spawning Kecleon on an odd numbered floor.",
    )

    MSG_ID_SLOW_START = Symbol(
        None,
        None,
        None,
        (
            "ID of the message printed when a monster has the ability Slow Start at the"
            " beginning of the floor."
        ),
    )

    EXPERIENCE_POINT_GAIN_CAP = Symbol(
        None,
        None,
        None,
        (
            "A cap on the experience that can be given to a monster in one call to"
            " AddExpSpecial"
        ),
    )

    JUDGMENT_MOVE_ID = Symbol(
        None, None, None, "Move ID for Judgment (0x1D3)\n\ntype: enum move_id"
    )

    REGULAR_ATTACK_MOVE_ID = Symbol(
        None, None, None, "Move ID for the regular attack (0x163)\n\ntype: enum move_id"
    )

    DEOXYS_ATTACK_ID = Symbol(
        None,
        None,
        None,
        "Monster ID for Deoxys in Attack Forme (0x1A3)\n\ntype: enum monster_id",
    )

    DEOXYS_SPEED_ID = Symbol(
        None,
        None,
        None,
        "Monster ID for Deoxys in Speed Forme (0x1A5)\n\ntype: enum monster_id",
    )

    GIRATINA_ALTERED_ID = Symbol(
        None,
        None,
        None,
        "Monster ID for Giratina in Altered Forme (0x211)\n\ntype: enum monster_id",
    )

    PUNISHMENT_MOVE_ID = Symbol(
        None, None, None, "Move ID for Punishment (0x1BD)\n\ntype: enum move_id"
    )

    OFFENSE_STAT_MAX = Symbol(
        None,
        None,
        None,
        (
            "Cap on an attacker's modified offense (attack or special attack) stat"
            " after boosts. Used during damage calculation."
        ),
    )

    PROJECTILE_MOVE_ID = Symbol(
        None,
        None,
        None,
        "The move ID of the special 'projectile' move (0x195)\n\ntype: enum move_id",
    )

    BELLY_LOST_PER_TURN = Symbol(
        None,
        None,
        None,
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
        None,
        None,
        None,
        (
            "The move target and range code for special healing moves that target just"
            " the user (0x273).\n\ntype: struct move_target_and_range (+ padding)"
        ),
    )

    PLAIN_SEED_VALUE = Symbol(
        None, None, None, "Some value related to the Plain Seed (0xBE9)."
    )

    MAX_ELIXIR_PP_RESTORATION = Symbol(
        None,
        None,
        None,
        "The amount of PP restored per move by ingesting a Max Elixir (0x3E7).",
    )

    SLIP_SEED_VALUE = Symbol(
        None, None, None, "Some value related to the Slip Seed (0xC75)."
    )

    ROCK_WRECKER_MOVE_ID = Symbol(
        None, None, None, "The move ID for Rock Wrecker (453)."
    )

    CASTFORM_NORMAL_FORM_MALE_ID = Symbol(
        None, None, None, "Castform's male normal form ID (0x17B)"
    )

    CASTFORM_NORMAL_FORM_FEMALE_ID = Symbol(
        None, None, None, "Castform's female normal form ID (0x3D3)"
    )

    CHERRIM_SUNSHINE_FORM_MALE_ID = Symbol(
        None, None, None, "Cherrim's male sunshine form ID (0x1CD)"
    )

    CHERRIM_OVERCAST_FORM_FEMALE_ID = Symbol(
        None, None, None, "Cherrim's female overcast form ID (0x424)"
    )

    CHERRIM_SUNSHINE_FORM_FEMALE_ID = Symbol(
        None, None, None, "Cherrim's female sunshine form ID (0x425)"
    )

    FLOOR_GENERATION_STATUS_PTR = Symbol(
        None,
        None,
        None,
        (
            "Pointer to the global FLOOR_GENERATION_STATUS\n\ntype: struct"
            " floor_generation_status*"
        ),
    )

    OFFSET_OF_DUNGEON_N_NORMAL_ITEM_SPAWNS = Symbol(
        None,
        None,
        None,
        (
            "Offset of the (number of base items + 1) field on the dungeon struct"
            " (0x12AFA)"
        ),
    )

    DUNGEON_GRID_COLUMN_BYTES = Symbol(
        None,
        None,
        None,
        (
            "The number of bytes in one column of the dungeon grid cell array, 450,"
            " which corresponds to a column of 15 grid cells."
        ),
    )

    DEFAULT_MAX_POSITION = Symbol(
        None,
        None,
        None,
        (
            "A large number (9999) to use as a default position for keeping track of"
            " min/max position values"
        ),
    )

    OFFSET_OF_DUNGEON_GUARANTEED_ITEM_ID = Symbol(
        None,
        None,
        None,
        "Offset of the guaranteed item ID field in the dungeon struct (0x2C9E8)",
    )

    FIXED_ROOM_TILE_SPAWN_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Table of tiles that can spawn in fixed rooms, pointed into by the"
            " FIXED_ROOM_TILE_SPAWN_TABLE.\n\nThis is an array of 11 4-byte entries"
            " containing info about one tile each. Info includes the trap ID if a trap,"
            " room ID, and flags.\n\ntype: struct fixed_room_tile_spawn_entry[11]"
        ),
    )

    TREASURE_BOX_1_ITEM_IDS = Symbol(
        None,
        None,
        None,
        (
            "Item IDs for variant 1 of each of the treasure box items"
            " (ITEM_*_BOX_1).\n\ntype: struct item_id_16[12]"
        ),
    )

    FIXED_ROOM_REVISIT_OVERRIDES = Symbol(
        None,
        None,
        None,
        (
            "Table of fixed room IDs, which if nonzero, overrides the normal fixed room"
            " ID for a floor (which is used to index the table) if the dungeon has"
            " already been cleared previously.\n\nOverrides are used to substitute"
            " different fixed room data for things like revisits to story"
            " dungeons.\n\ntype: struct fixed_room_id_8[256]"
        ),
    )

    FIXED_ROOM_MONSTER_SPAWN_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Table of monsters that can spawn in fixed rooms, pointed into by the"
            " FIXED_ROOM_ENTITY_SPAWN_TABLE.\n\nThis is an array of 120 4-byte entries"
            " containing info about one monster each. Info includes the monster ID,"
            " stats, and behavior type.\n\ntype: struct"
            " fixed_room_monster_spawn_entry[120]"
        ),
    )

    FIXED_ROOM_ITEM_SPAWN_TABLE = Symbol(
        None,
        None,
        None,
        (
            "Table of items that can spawn in fixed rooms, pointed into by the"
            " FIXED_ROOM_ENTITY_SPAWN_TABLE.\n\nThis is an array of 63 8-byte entries"
            " containing one item ID each.\n\ntype: struct"
            " fixed_room_item_spawn_entry[63]"
        ),
    )

    FIXED_ROOM_ENTITY_SPAWN_TABLE = Symbol(
        None,
        None,
        None,
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
        None,
        None,
        None,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::muzzled * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_MAGNET_RISE = Symbol(
        None,
        None,
        None,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::magnet_rise * 8. See UpdateStatusIconFlags for"
            " details."
        ),
    )

    STATUS_ICON_ARRAY_MIRACLE_EYE = Symbol(
        None,
        None,
        None,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::miracle_eye * 8. See UpdateStatusIconFlags for"
            " details."
        ),
    )

    STATUS_ICON_ARRAY_LEECH_SEED = Symbol(
        None,
        None,
        None,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::leech_seed * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_LONG_TOSS = Symbol(
        None,
        None,
        None,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::long_toss * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_BLINDED = Symbol(
        None,
        None,
        None,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::blinded * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_BURN = Symbol(
        None,
        None,
        None,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::burn * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_SURE_SHOT = Symbol(
        None,
        None,
        None,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::sure_shot * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_INVISIBLE = Symbol(
        None,
        None,
        None,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::invisible * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_SLEEP = Symbol(
        None,
        None,
        None,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::sleep * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_CURSE = Symbol(
        None,
        None,
        None,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::curse * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_FREEZE = Symbol(
        None,
        None,
        None,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::freeze * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_CRINGE = Symbol(
        None,
        None,
        None,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::cringe * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_BIDE = Symbol(
        None,
        None,
        None,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::bide * 8. See UpdateStatusIconFlags for details."
        ),
    )

    STATUS_ICON_ARRAY_REFLECT = Symbol(
        None,
        None,
        None,
        (
            "Array of bit masks used to set monster::status_icon. Indexed by"
            " monster::statuses::reflect * 8. See UpdateStatusIconFlags for details."
        ),
    )

    DIRECTIONS_XY = Symbol(
        None,
        None,
        None,
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
        None,
        None,
        None,
        (
            "Action ID associated with each item category. Used by"
            " GetItemAction.\n\nEach entry is 2 bytes long."
        ),
    )

    FRACTIONAL_TURN_SEQUENCE = Symbol(
        None,
        None,
        None,
        (
            "Read by certain functions that are called by RunFractionalTurn to see if"
            " they should be executed.\n\nArray is accessed via a pointer added to some"
            " multiple of fractional_turn, so that if the resulting memory location is"
            " zero, the function returns."
        ),
    )

    BELLY_DRAIN_IN_WALLS_INT = Symbol(
        None,
        None,
        None,
        (
            "The additional amount by which belly is decreased every turn when inside"
            " walls (integer part)"
        ),
    )

    BELLY_DRAIN_IN_WALLS_THOUSANDTHS = Symbol(
        None,
        None,
        None,
        (
            "The additional amount by which belly is decreased every turn when inside"
            " walls (fractional thousandths)"
        ),
    )

    SPATK_STAT_IDX = Symbol(
        None,
        None,
        None,
        (
            "The index (1) of the special attack entry in internal stat structs, such"
            " as the stat modifier array for a monster."
        ),
    )

    ATK_STAT_IDX = Symbol(
        None,
        None,
        None,
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
        None,
        None,
        None,
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
        None,
        None,
        None,
        (
            "[Runtime] Pointer to the dungeon struct in dungeon mode.\n\nThis is a"
            " 'working copy' of DUNGEON_PTR_MASTER. The main dungeon engine uses this"
            " pointer (or rather pointers to this pointer) when actually running"
            " dungeon mode.\n\ntype: struct dungeon*"
        ),
    )

    DUNGEON_PTR_MASTER = Symbol(
        None,
        None,
        None,
        (
            "[Runtime] Pointer to the dungeon struct in dungeon mode.\n\nThis is a"
            " 'master copy' of the dungeon pointer. The game uses this pointer when"
            " doing low-level memory work (allocation, freeing, zeroing). The normal"
            " DUNGEON_PTR is used for most other dungeon mode work.\n\ntype: struct"
            " dungeon*"
        ),
    )

    LEADER_PTR = Symbol(
        None,
        None,
        None,
        "[Runtime] Pointer to the current leader of the team.\n\ntype: struct entity*",
    )

    DUNGEON_PRNG_STATE = Symbol(
        None,
        None,
        None,
        (
            "[Runtime] The global PRNG state for dungeon mode, not including the"
            " current values in the secondary sequences.\n\nThis struct holds state for"
            " the primary LCG, as well as the current configuration controlling which"
            " LCG to use when generating random numbers. See DungeonRand16Bit for more"
            " information on how the dungeon PRNG works.\n\ntype: struct prng_state"
        ),
    )

    DUNGEON_PRNG_STATE_SECONDARY_VALUES = Symbol(
        None,
        None,
        None,
        (
            "[Runtime] An array of 5 integers corresponding to the last value generated"
            " for each secondary LCG sequence.\n\nBased on the assembly, this appears"
            " to be its own global array, separate from DUNGEON_PRNG_STATE."
        ),
    )

    EXCL_ITEM_EFFECTS_WEATHER_ATK_SPEED_BOOST = Symbol(
        None,
        None,
        None,
        (
            "Array of IDs for exclusive item effects that increase attack speed with"
            " certain weather conditions."
        ),
    )

    EXCL_ITEM_EFFECTS_WEATHER_MOVE_SPEED_BOOST = Symbol(
        None,
        None,
        None,
        (
            "Array of IDs for exclusive item effects that increase movement speed with"
            " certain weather conditions."
        ),
    )

    EXCL_ITEM_EFFECTS_WEATHER_NO_STATUS = Symbol(
        None,
        None,
        None,
        (
            "Array of IDs for exclusive item effects that grant status immunity with"
            " certain weather conditions."
        ),
    )

    EXCL_ITEM_EFFECTS_EVASION_BOOST = Symbol(
        None,
        None,
        None,
        (
            "Array of IDs for exclusive item effects that grant an evasion boost with"
            " certain weather conditions."
        ),
    )

    DEFAULT_TILE = Symbol(
        None,
        None,
        None,
        (
            "The default tile struct.\n\nThis is just a struct full of zeroes, but is"
            " used as a fallback in various places where a 'default' tile is needed,"
            " such as when a grid index is out of range.\n\ntype: struct tile"
        ),
    )

    HIDDEN_STAIRS_SPAWN_BLOCKED = Symbol(
        None,
        None,
        None,
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
        None,
        None,
        None,
        (
            "[Runtime] Pointer to decoded fixed room data loaded from the"
            " BALANCE/fixed.bin file."
        ),
    )

    NECTAR_IQ_BOOST = Symbol(None, None, None, "IQ boost from ingesting Nectar.")


class EuItcmOverlay29Section:
    name = "overlay29"
    description = (
        "The dungeon engine.\n\nThis is the 'main' overlay of dungeon mode. It controls"
        " most things that happen in a Mystery Dungeon, such as dungeon layout"
        " generation, dungeon menus, enemy AI, and generally just running each turn"
        " while within a dungeon."
    )
    loadaddress = None
    length = None
    functions = EuItcmOverlay29Functions
    data = EuItcmOverlay29Data


class EuItcmOverlay3Functions:
    pass


class EuItcmOverlay3Data:
    pass


class EuItcmOverlay3Section:
    name = "overlay3"
    description = "Controls the Friend Rescue submenu within the top menu."
    loadaddress = None
    length = None
    functions = EuItcmOverlay3Functions
    data = EuItcmOverlay3Data


class EuItcmOverlay30Functions:
    pass


class EuItcmOverlay30Data:
    OVERLAY30_JP_STRING_1 = Symbol(None, None, None, "みさき様")

    OVERLAY30_JP_STRING_2 = Symbol(None, None, None, "やよい様")


class EuItcmOverlay30Section:
    name = "overlay30"
    description = "Controls quicksaving in dungeons."
    loadaddress = None
    length = None
    functions = EuItcmOverlay30Functions
    data = EuItcmOverlay30Data


class EuItcmOverlay31Functions:
    EntryOverlay31 = Symbol(
        None, None, None, "Note: unverified, ported from Irdkwia's notes\n\nNo params."
    )

    DungeonMenuSwitch = Symbol(
        None,
        None,
        None,
        (
            "Note: unverified, ported from Irdkwia's notes\n\nr0: appears to be an"
            " index of some sort, probably the menu index based on the function name?"
        ),
    )

    MovesMenu = Symbol(
        None,
        None,
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
        None,
        None,
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
        None,
        None,
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
        None,
        None,
        None,
        (
            "Called when the in-dungeon 'rest' menu is open. Does not return until the"
            " menu is closed.\n\nNo params."
        ),
    )

    RecruitmentSearchMenuLoop = Symbol(
        None,
        None,
        None,
        (
            "Called on each frame while the in-dungeon 'recruitment search' menu is"
            " open.\n\nreturn: int (Actually, this is probably some sort of enum shared"
            " by all the MenuLoop functions)"
        ),
    )

    HelpMenuLoop = Symbol(
        None,
        None,
        None,
        (
            "Called on each frame while the in-dungeon 'help' menu is open.\n\nThe menu"
            " is still considered open while one of the help pages is being viewed, so"
            " this function keeps being called even after choosing an"
            " option.\n\nreturn: int (Actually, this is probably some sort of enum"
            " shared by all the MenuLoop functions)"
        ),
    )


class EuItcmOverlay31Data:
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

    DUNGEON_MAIN_MENU = Symbol(None, None, None, "")

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

    DUNGEON_SUBMENU_1 = Symbol(None, None, None, "")

    DUNGEON_SUBMENU_2 = Symbol(None, None, None, "")

    DUNGEON_SUBMENU_3 = Symbol(None, None, None, "")

    DUNGEON_SUBMENU_4 = Symbol(None, None, None, "")

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

    DUNGEON_SUBMENU_5 = Symbol(None, None, None, "")

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

    DUNGEON_SUBMENU_6 = Symbol(None, None, None, "")

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


class EuItcmOverlay31Section:
    name = "overlay31"
    description = "Controls the dungeon menu (during dungeon mode)."
    loadaddress = None
    length = None
    functions = EuItcmOverlay31Functions
    data = EuItcmOverlay31Data


class EuItcmOverlay32Functions:
    pass


class EuItcmOverlay32Data:
    pass


class EuItcmOverlay32Section:
    name = "overlay32"
    description = "Unused; all zeroes."
    loadaddress = None
    length = None
    functions = EuItcmOverlay32Functions
    data = EuItcmOverlay32Data


class EuItcmOverlay33Functions:
    pass


class EuItcmOverlay33Data:
    pass


class EuItcmOverlay33Section:
    name = "overlay33"
    description = "Unused; all zeroes."
    loadaddress = None
    length = None
    functions = EuItcmOverlay33Functions
    data = EuItcmOverlay33Data


class EuItcmOverlay34Functions:
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


class EuItcmOverlay34Data:
    OVERLAY34_UNKNOWN_STRUCT__NA_22DD014 = Symbol(
        None,
        None,
        None,
        "1*0x4 + 3*0x4\n\nNote: unverified, ported from Irdkwia's notes",
    )

    START_MENU_CONFIRM = Symbol(None, None, None, "Irdkwia's notes: 3*0x8")

    OVERLAY34_UNKNOWN_STRUCT__NA_22DD03C = Symbol(
        None,
        None,
        None,
        "1*0x4 + 3*0x4\n\nNote: unverified, ported from Irdkwia's notes",
    )

    DUNGEON_DEBUG_MENU = Symbol(None, None, None, "Irdkwia's notes: 5*0x8")

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


class EuItcmOverlay34Section:
    name = "overlay34"
    description = (
        "Related to launching the game.\n\nThere are mention in the strings of logos"
        " like the ESRB logo. This only seems to be loaded during the ESRB rating"
        " splash screen, so this is likely the sole purpose of this overlay."
    )
    loadaddress = None
    length = None
    functions = EuItcmOverlay34Functions
    data = EuItcmOverlay34Data


class EuItcmOverlay35Functions:
    pass


class EuItcmOverlay35Data:
    pass


class EuItcmOverlay35Section:
    name = "overlay35"
    description = "Unused; all zeroes."
    loadaddress = None
    length = None
    functions = EuItcmOverlay35Functions
    data = EuItcmOverlay35Data


class EuItcmOverlay4Functions:
    pass


class EuItcmOverlay4Data:
    pass


class EuItcmOverlay4Section:
    name = "overlay4"
    description = "Controls the Trade Items submenu within the top menu."
    loadaddress = None
    length = None
    functions = EuItcmOverlay4Functions
    data = EuItcmOverlay4Data


class EuItcmOverlay5Functions:
    pass


class EuItcmOverlay5Data:
    pass


class EuItcmOverlay5Section:
    name = "overlay5"
    description = "Controls the Trade Team submenu within the top menu."
    loadaddress = None
    length = None
    functions = EuItcmOverlay5Functions
    data = EuItcmOverlay5Data


class EuItcmOverlay6Functions:
    pass


class EuItcmOverlay6Data:
    pass


class EuItcmOverlay6Section:
    name = "overlay6"
    description = "Controls the Wonder Mail S submenu within the top menu."
    loadaddress = None
    length = None
    functions = EuItcmOverlay6Functions
    data = EuItcmOverlay6Data


class EuItcmOverlay7Functions:
    pass


class EuItcmOverlay7Data:
    pass


class EuItcmOverlay7Section:
    name = "overlay7"
    description = (
        "Controls the Nintendo WFC submenu within the top menu (under 'Other')."
    )
    loadaddress = None
    length = None
    functions = EuItcmOverlay7Functions
    data = EuItcmOverlay7Data


class EuItcmOverlay8Functions:
    pass


class EuItcmOverlay8Data:
    pass


class EuItcmOverlay8Section:
    name = "overlay8"
    description = (
        "Controls the Send Demo Dungeon submenu within the top menu (under 'Other')."
    )
    loadaddress = None
    length = None
    functions = EuItcmOverlay8Functions
    data = EuItcmOverlay8Data


class EuItcmOverlay9Functions:
    pass


class EuItcmOverlay9Data:
    TOP_MENU_RETURN_MUSIC_ID = Symbol(
        None,
        None,
        None,
        "Song playing in the main menu when returning from the Sky Jukebox.",
    )


class EuItcmOverlay9Section:
    name = "overlay9"
    description = "Controls the Sky Jukebox."
    loadaddress = None
    length = None
    functions = EuItcmOverlay9Functions
    data = EuItcmOverlay9Data


class EuItcmRamFunctions:
    pass


class EuItcmRamData:
    DUNGEON_COLORMAP_PTR = Symbol(
        None,
        None,
        None,
        (
            "Pointer to a colormap used to render colors in a dungeon.\n\nThe colormap"
            " is a list of 4-byte RGB colors of the form {R, G, B, padding}, which the"
            " game indexes into when rendering colors. Some weather conditions modify"
            " the colormap, which is how the color scheme changes when it's, e.g.,"
            " raining."
        ),
    )

    DUNGEON_STRUCT = Symbol(
        None,
        None,
        None,
        (
            "The dungeon context struct used for tons of stuff in dungeon mode. See"
            " struct dungeon in the C headers.\n\nThis struct never seems to be"
            " referenced directly, and is instead usually accessed via DUNGEON_PTR in"
            " overlay 29.\n\ntype: struct dungeon"
        ),
    )

    MOVE_DATA_TABLE = Symbol(
        None,
        None,
        None,
        (
            "The move data table loaded directly from /BALANCE/waza_p.bin. See struct"
            " move_data_table in the C headers.\n\nPointed to by MOVE_DATA_TABLE_PTR in"
            " the ARM 9 binary.\n\ntype: struct move_data_table"
        ),
    )

    FRAMES_SINCE_LAUNCH = Symbol(
        None,
        None,
        None,
        (
            "Starts at 0 when the game is first launched, and continuously ticks up"
            " once per frame while the game is running."
        ),
    )

    BAG_ITEMS = Symbol(
        None,
        None,
        None,
        (
            "Array of item structs within the player's bag.\n\nWhile the game only"
            " allows a maximum of 48 items during normal play, it seems to read up to"
            " 50 item slots if filled.\n\ntype: struct item[50]"
        ),
    )

    BAG_ITEMS_PTR = Symbol(None, None, None, "Pointer to BAG_ITEMS.")

    STORAGE_ITEMS = Symbol(
        None,
        None,
        None,
        (
            "Array of item IDs in the player's item storage.\n\nFor stackable items,"
            " the quantities are stored elsewhere, in STORAGE_ITEM_QUANTITIES.\n\ntype:"
            " struct item_id_16[1000]"
        ),
    )

    STORAGE_ITEM_QUANTITIES = Symbol(
        None,
        None,
        None,
        (
            "Array of 1000 2-byte (unsigned) quantities corresponding to the item IDs"
            " in STORAGE_ITEMS.\n\nIf the corresponding item ID is not a stackable"
            " item, the entry in this array is unused, and will be 0."
        ),
    )

    KECLEON_SHOP_ITEMS_PTR = Symbol(None, None, None, "Pointer to KECLEON_SHOP_ITEMS.")

    KECLEON_SHOP_ITEMS = Symbol(
        None,
        None,
        None,
        (
            "Array of up to 8 items in the Kecleon Shop.\n\nIf there are fewer than 8"
            " items, the array is expected to be null-terminated.\n\ntype: struct"
            " bulk_item[8]"
        ),
    )

    UNUSED_KECLEON_SHOP_ITEMS = Symbol(
        None,
        None,
        None,
        (
            "Seems to be another array like KECLEON_SHOP_ITEMS, but don't actually"
            " appear to be used by the Kecleon Shop."
        ),
    )

    KECLEON_WARES_ITEMS_PTR = Symbol(
        None, None, None, "Pointer to KECLEON_WARES_ITEMS."
    )

    KECLEON_WARES_ITEMS = Symbol(
        None,
        None,
        None,
        (
            "Array of up to 4 items in Kecleon Wares.\n\nIf there are fewer than 4"
            " items, the array is expected to be null-terminated.\n\ntype: struct"
            " bulk_item[4]"
        ),
    )

    UNUSED_KECLEON_WARES_ITEMS = Symbol(
        None,
        None,
        None,
        (
            "Seems to be another array like KECLEON_WARES_ITEMS, but don't actually"
            " appear to be used by Kecleon Wares."
        ),
    )

    MONEY_CARRIED = Symbol(
        None, None, None, "The amount of money the player is currently carrying."
    )

    MONEY_STORED = Symbol(
        None,
        None,
        None,
        "The amount of money the player currently has stored in the Duskull Bank.",
    )

    DIALOG_BOX_LIST = Symbol(None, None, None, "Array of allocated dialog box structs.")

    LAST_NEW_MOVE = Symbol(
        None,
        None,
        None,
        (
            "Move struct of the last new move introduced when learning a new move."
            " Persists even after the move selection is made in the menu.\n\ntype:"
            " struct move"
        ),
    )

    SCRIPT_VARS_VALUES = Symbol(
        None,
        None,
        None,
        (
            "The table of game variable values. Its structure is determined by"
            " SCRIPT_VARS.\n\nNote that with the script variable list defined in"
            " SCRIPT_VARS, the used length of this table is actually only 0x2B4."
            " However, the real length of this table is 0x400 based on the game"
            " code.\n\ntype: struct script_var_value_table"
        ),
    )

    BAG_LEVEL = Symbol(
        None,
        None,
        None,
        (
            "The player's bag level, which determines the bag capacity. This indexes"
            " directly into the BAG_CAPACITY_TABLE in the ARM9 binary."
        ),
    )

    DEBUG_SPECIAL_EPISODE_NUMBER = Symbol(
        None,
        None,
        None,
        (
            "The number of the special episode currently being played.\n\nThis backs"
            " the EXECUTE_SPECIAL_EPISODE_TYPE script variable.\n\ntype: struct"
            " special_episode_type_8"
        ),
    )

    PENDING_DUNGEON_ID = Symbol(
        None,
        None,
        None,
        (
            "The ID of the selected dungeon when setting off from the"
            " overworld.\n\nControls the text and map location during the 'map"
            " cutscene' just before entering a dungeon, as well as the actual dungeon"
            " loaded afterwards.\n\ntype: struct dungeon_id_8"
        ),
    )

    PENDING_STARTING_FLOOR = Symbol(
        None,
        None,
        None,
        (
            "The floor number to start from in the dungeon specified by"
            " PENDING_DUNGEON_ID."
        ),
    )

    PLAY_TIME_SECONDS = Symbol(
        None, None, None, "The player's total play time in seconds."
    )

    PLAY_TIME_FRAME_COUNTER = Symbol(
        None,
        None,
        None,
        (
            "Counts from 0-59 in a loop, with the play time being incremented by 1"
            " second with each rollover."
        ),
    )

    TEAM_NAME = Symbol(
        None,
        None,
        None,
        (
            "The team name.\n\nA null-terminated string, with a maximum length of 10."
            " Presumably encoded with the ANSI/Shift JIS encoding the game typically"
            " uses.\n\nThis is presumably part of a larger struct, together with other"
            " nearby data."
        ),
    )

    TEAM_MEMBER_LIST = Symbol(
        None,
        None,
        None,
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
        None,
        None,
        None,
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
        None,
        None,
        None,
        (
            "Starts at 0 when the game is first launched, and ticks up by 3 per frame"
            " while the game is running."
        ),
    )

    SENTRY_DUTY_STRUCT = Symbol(None, None, None, "")

    TURNING_ON_THE_SPOT_FLAG = Symbol(
        None,
        None,
        None,
        "[Runtime] Flag for whether the player is turning on the spot (pressing Y).",
    )

    METRONOME_NEXT_INDEX = Symbol(
        None,
        None,
        None,
        "[Runtime] The index into METRONOME_TABLE for the next usage of Metronome.",
    )

    FLOOR_GENERATION_STATUS = Symbol(
        None,
        None,
        None,
        (
            "[Runtime] Status data related to generation of the current floor in a"
            " dungeon.\n\nThis data is populated as the dungeon floor is"
            " generated.\n\ntype: struct floor_generation_status"
        ),
    )


class EuItcmRamSection:
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
    loadaddress = None
    length = None
    functions = EuItcmRamFunctions
    data = EuItcmRamData


class EuItcmSections:
    arm7 = EuItcmArm7Section

    arm9 = EuItcmArm9Section

    itcm = EuItcmItcmSection

    move_effects = EuItcmMove_effectsSection

    overlay0 = EuItcmOverlay0Section

    overlay1 = EuItcmOverlay1Section

    overlay10 = EuItcmOverlay10Section

    overlay11 = EuItcmOverlay11Section

    overlay12 = EuItcmOverlay12Section

    overlay13 = EuItcmOverlay13Section

    overlay14 = EuItcmOverlay14Section

    overlay15 = EuItcmOverlay15Section

    overlay16 = EuItcmOverlay16Section

    overlay17 = EuItcmOverlay17Section

    overlay18 = EuItcmOverlay18Section

    overlay19 = EuItcmOverlay19Section

    overlay2 = EuItcmOverlay2Section

    overlay20 = EuItcmOverlay20Section

    overlay21 = EuItcmOverlay21Section

    overlay22 = EuItcmOverlay22Section

    overlay23 = EuItcmOverlay23Section

    overlay24 = EuItcmOverlay24Section

    overlay25 = EuItcmOverlay25Section

    overlay26 = EuItcmOverlay26Section

    overlay27 = EuItcmOverlay27Section

    overlay28 = EuItcmOverlay28Section

    overlay29 = EuItcmOverlay29Section

    overlay3 = EuItcmOverlay3Section

    overlay30 = EuItcmOverlay30Section

    overlay31 = EuItcmOverlay31Section

    overlay32 = EuItcmOverlay32Section

    overlay33 = EuItcmOverlay33Section

    overlay34 = EuItcmOverlay34Section

    overlay35 = EuItcmOverlay35Section

    overlay4 = EuItcmOverlay4Section

    overlay5 = EuItcmOverlay5Section

    overlay6 = EuItcmOverlay6Section

    overlay7 = EuItcmOverlay7Section

    overlay8 = EuItcmOverlay8Section

    overlay9 = EuItcmOverlay9Section

    ram = EuItcmRamSection
