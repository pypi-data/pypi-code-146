

from itertools import product
import string

from dagster import StaticPartitionsDefinition


hex_digits = sorted(set(string.hexdigits.lower()))
lmd_partition_def = StaticPartitionsDefinition(
    list(map(''.join, product(hex_digits, hex_digits)))
)
lmd_partition_def.name = 'partition'