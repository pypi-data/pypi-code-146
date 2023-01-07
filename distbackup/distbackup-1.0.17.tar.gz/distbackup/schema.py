SCHEMA_VERSION = 31

TABLES_INDICES = [
    # path_map: Maps virtual paths to actual directories on fhe filesystem
    """
    CREATE TABLE IF NOT EXISTS path_map (
        virtual_path TEXT PRIMARY KEY,
        real_path TEXT NOT NULL
    ) STRICT, WITHOUT ROWID
    """,

    # path_config: Contains configuration options for individual directories
    """
    CREATE TABLE IF NOT EXISTS path_config (
        virtual_path TEXT PRIMARY KEY,
        config TEXT NOT NULL DEFAULT '{}'
    ) STRICT, WITHOUT ROWID
    """,

    # file_tree: Contains information for each file that is backed up. Only leaf nodes
    # (i.e. files, not directories) have an entry in this table.
    """
    CREATE TABLE IF NOT EXISTS file_tree (
        -- Virtual path of the file, separated by "/"
        virtual_path TEXT PRIMARY KEY,

        -- Unix time in milliseconds
        last_modified INTEGER,

        -- SHA256 hash of the data. Empty if the hash is unknown, NULL if file is empty
        hash TEXT,

        -- Inode of the file (stat.st_ino). Used to quickly detect rename / move without having to rehash
        ino INTEGER,

        -- Size of the file, in bytes
        size INTEGER,

        -- Priority of the file. Files with a greater value for `priority` will be copied
        -- before lower priority files (assuming levels are equal)
        priority INTEGER NOT NULL DEFAULT 1,

        -- The maximum number of copies that this file can have on backup disks.
        maxcopies INTEGER,

        -- Compacted JSON of `.meta-inf` file associated with this file.
        metadata TEXT NOT NULL DEFAULT ''
    ) STRICT, WITHOUT ROWID
    """,

    "CREATE INDEX IF NOT EXISTS file_tree_hash ON file_tree(hash)",
    "CREATE INDEX IF NOT EXISTS file_need_hash ON file_tree(virtual_path) WHERE hash = ''",

    # symbolic_link: Contains all symbolic links from the backup set.
    """
    CREATE TABLE IF NOT EXISTS symbolic_link (
        virtual_path TEXT PRIMARY KEY,
        target TEXT NOT NULL
    ) STRICT, WITHOUT ROWID
    """,

    # nexus: A subset of the backup disks. Each row tracks the number and size of objects
    # stored on exactly those disks. Updated by triggers. The key is simply a binary
    # string of disks in little-endian order, stripped of trailing zeroes. '' represents
    # the empty set; '1' represents the nexus of only disk 0; '101' represents the nexus
    # of disk 0 with disk 2, etc.
    """
    CREATE TABLE IF NOT EXISTS nexus (
        -- Nexus key string, identifying which disks are in the set
        nexus TEXT PRIMARY KEY,

        -- Number of disks in the set
        level INTEGER GENERATED ALWAYS AS (length(replace(nexus, '0', ''))) STORED,

        -- Number of objects in this nexus. Updated by triggers.
        refs INTEGER DEFAULT 0,

        -- Sum of all `blocksize` columns of objects in this nexus. Updated by triggers.
        totalsize INTEGER NOT NULL DEFAULT 0,

        -- Names of disks in this nexus (informational, updated automatically)
        disks TEXT NOT NULL DEFAULT '',

        -- Sum of all `blocksize` columns of saturated objects in this nexus. Updated by triggers.
        saturated_size INTEGER NOT NULL DEFAULT 0
    ) STRICT, WITHOUT ROWID
    """,

    "CREATE INDEX IF NOT EXISTS nexus_prio ON nexus(level, totalsize DESC)",

    # object: Tracks which disks an object has been copied to. Multiple files with the
    # same content will reference the same object.
    """
    CREATE TABLE IF NOT EXISTS object (
        -- SHA256 hash of the object
        hash TEXT PRIMARY KEY,

        -- Exact size of the object in bytes
        size INTEGER DEFAULT 0,

        -- Size of the object, rounded up to next 4KB, plus 4KB for metadata
        blocksize INTEGER GENERATED ALWAYS AS (4096 + (size + 4095) & ~4095),

        -- Order of magnitude of the size
        size_order INTEGER GENERATED ALWAYS AS (CAST(floor(log2(blocksize + 0.01)) AS INTEGER)) STORED,

        -- Nexus of disks that this object is present on
        nexus TEXT NOT NULL DEFAULT '',

        -- Number of disks that this object exists on
        copies INTEGER GENERATED ALWAYS AS (length(replace(nexus, '0', ''))) STORED,

        -- Priority for this object. This is the maximum priority for any file_tree row
        -- that references this row.
        priority INTEGER NOT NULL DEFAULT 1,

        -- Maximum copies for this object. This is the maximum value for any file_tree row
        -- that references this row.
        maxcopies INTEGER,

        -- References to this object from the file_tree table, updated by triggers
        refs INTEGER NOT NULL DEFAULT 0,

        -- One of the paths that linked to this object. This is kept for
        -- informational purposes, so that if a file's content changes and causes
        -- this object to get deleted, we can show the user which file it was, along
        -- with the modification date.
        last_path TEXT NOT NULL DEFAULT '',
        last_modtime INTEGER NOT NULL DEFAULT 0,

        -- This will be 1 iff the object is at the maximum number of copies.
        saturated INTEGER GENERATED ALWAYS AS (CASE WHEN copies >= maxcopies THEN 1 ELSE 0 END),

        -- This is equal to the blocksize iff the object is referred to by the file_tree table.
        relevant_size INTEGER GENERATED ALWAYS AS (CASE WHEN refs > 0 THEN blocksize ELSE 0 END),

        -- This is equal to the blocksize iff the object is referred to by the file_tree table.
        saturated_size INTEGER GENERATED ALWAYS AS (CASE WHEN copies >= maxcopies AND refs > 0 THEN blocksize ELSE 0 END)

    ) STRICT
    """,

    "CREATE INDEX IF NOT EXISTS object_prio ON object(copies DESC, blocksize)",
    "CREATE INDEX IF NOT EXISTS object_size ON object(blocksize)",
    "CREATE INDEX IF NOT EXISTS object_refs ON object(refs)",
    "CREATE INDEX IF NOT EXISTS object_refs_copies ON object(refs, copies)",
    "CREATE INDEX IF NOT EXISTS object_nexus ON object(nexus)",

    # disk: Represents a backup disk that stores objects.
    """
    CREATE TABLE IF NOT EXISTS disk (
        -- UUID identifying the disk. This is generated when the disk is added and
        -- never changes.
        uuid TEXT PRIMARY KEY,

        -- Name of this disk. NULL if the disk has been deleted. Deleted disks are
        -- kept so the `nexus_index` can be reused.
        name TEXT UNIQUE,

        -- Index of this disk within nexus indetifiers.
        nexus_index INTEGER NOT NULL UNIQUE,

        -- Path to object files on the disk realtive to its mountpoint.
        relative_path TEXT,

        -- If not NULL, only search on partitions matching the given fstype
        fstype TEXT,

        -- If not NULL, only search on partitions matching the given UUID
        fsuuid TEXT,

        -- Size of the disk in bytes.
        size INTEGER

    ) STRICT, WITHOUT ROWID
    """,

    "CREATE INDEX IF NOT EXISTS unused_nexus_index ON disk(nexus_index) WHERE name ISNULL",
]

TRIGGERS = [
    # Nexus update triggers. min(NEW.refs, 1) is used so that objects that aren't
    # referred to in the file_tree don't count as being present.
    """
    CREATE TRIGGER IF NOT EXISTS object_insert
    AFTER INSERT ON object
    BEGIN
        INSERT INTO nexus(nexus, refs, totalsize, saturated_size)
          VALUES(NEW.nexus, 1, NEW.relevant_size, NEW.saturated_size)
        ON CONFLICT(nexus) DO UPDATE SET
          refs = refs + 1,
          totalsize = totalsize + NEW.relevant_size,
          saturated_size = saturated_size + NEW.saturated_size;
    END
    """,

    """
    CREATE TRIGGER IF NOT EXISTS object_update
    AFTER UPDATE ON object
    WHEN OLD.relevant_size != NEW.relevant_size OR OLD.saturated_size != NEW.saturated_size OR OLD.nexus != NEW.nexus
    BEGIN
        INSERT INTO nexus(nexus, refs, totalsize, saturated_size)
          VALUES(NEW.nexus, 1, NEW.relevant_size, NEW.saturated_size)
        ON CONFLICT(nexus) DO UPDATE SET
          refs = refs + 1,
          totalsize = totalsize + NEW.relevant_size,
          saturated_size = saturated_size + NEW.saturated_size;

        UPDATE nexus SET
          refs = refs - 1,
          totalsize = totalsize - OLD.relevant_size,
          saturated_size = saturated_size - OLD.saturated_size
        WHERE nexus = OLD.nexus;
    END
    """,
    """
    CREATE TRIGGER IF NOT EXISTS object_delete
    BEFORE DELETE ON object
    BEGIN
        UPDATE nexus SET
          refs = refs - 1,
          totalsize = totalsize - OLD.relevant_size,
          saturated_size = saturated_size - OLD.saturated_size
        WHERE nexus = OLD.nexus;
    END
    """,

    """
    CREATE TRIGGER IF NOT EXISTS file_tree_insert
    AFTER INSERT ON file_tree
    WHEN NEW.hash <> ''
    BEGIN
        INSERT INTO object(hash, size, priority, maxcopies, refs, last_path, last_modtime)
          VALUES(NEW.hash, NEW.size, NEW.priority, NEW.maxcopies, 1, NEW.virtual_path, NEW.last_modified)
        ON CONFLICT(hash) DO UPDATE SET
          refs = refs + 1,
          priority = COALESCE((SELECT MAX(priority) FROM file_tree WHERE hash = NEW.hash), 1),
          maxcopies = (SELECT MAX(maxcopies) FROM file_tree WHERE hash = NEW.hash);
    END
    """,

    """
    CREATE TRIGGER IF NOT EXISTS file_tree_update
    AFTER UPDATE ON file_tree
    WHEN OLD.hash != NEW.hash
    BEGIN
        INSERT INTO object(hash, size, priority, maxcopies, refs, last_path, last_modtime)
          VALUES(NEW.hash, NEW.size, NEW.priority, NEW.maxcopies, 1, NEW.virtual_path, NEW.last_modified)
        ON CONFLICT(hash) DO UPDATE SET
          refs = refs + 1,
          priority = COALESCE((SELECT MAX(priority) FROM file_tree WHERE hash = NEW.hash), 1),
          maxcopies = (SELECT MAX(maxcopies) FROM file_tree WHERE hash = NEW.hash);

        UPDATE object SET
          refs = refs - 1,
          priority = COALESCE((SELECT MAX(priority) FROM file_tree WHERE hash = OLD.hash), 1),
          maxcopies = (SELECT MAX(maxcopies) FROM file_tree WHERE hash = OLD.hash)
        WHERE hash = OLD.hash;
    END
    """,

    """
    CREATE TRIGGER IF NOT EXISTS file_tree_delete
    BEFORE DELETE ON file_tree
    BEGIN
        UPDATE object SET
          refs = refs - 1,
          priority = COALESCE((SELECT MAX(priority) FROM file_tree WHERE hash = OLD.hash), 1),
          maxcopies = (SELECT MAX(maxcopies) FROM file_tree WHERE hash = OLD.hash)
        WHERE hash = OLD.hash;
    END
    """
]

PRE_DATA = [
    # Make sure there is always a nexus entry representing the empty set
    "INSERT OR IGNORE INTO nexus(nexus) VALUES ('')",
]
