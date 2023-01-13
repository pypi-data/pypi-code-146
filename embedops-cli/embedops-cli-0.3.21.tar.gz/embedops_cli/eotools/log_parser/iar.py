"""Regex pattern for parsing the output of an IAR build"""


COMPILER_PATTERN = r"IAR ANSI C/C++ Compiler (V8.50.1.245/W32) for ARM"

# regex pattern for IAR size default output
# Example:
# https://regex101.com/r/5g5Yon/1
# componentA.out
# /opt/iarsystems/bxarm-9.30.1/arm/bin/ilinkarm /src/arm/Debug/Obj/componentA.o \
#   --no_out_extension -o /src/arm/Debug/Exe/componentA.out \
#   --redirect _Printf=_PrintfFullNoMb --redirect _Scanf=_ScanfFullNoMb \
#   --map /src/arm/Debug/List/componentA.map \
#   --config /opt/iarsystems/bxarm-9.30.1/arm/config/generic_cortex.icf \
#   --semihosting /src/arm/Debug/Exe/library.a --entry __iar_program_start \
#   --vfe --text_out locale --cpu=Cortex-M3 --fpu=None

#    IAR ELF Linker V9.30.1.335/LNX for ARM BX
#    Copyright 2007-2022 IAR Systems AB.

#   7'636 bytes of readonly  code memory
#     136 bytes of readonly  data memory
#   1'036 bytes of readwrite data memory

SIZE_PATTERN = (
    r"\n(?P<target_name>[\w]+) - (?P<target_group>[\w]+)\sReading project nodes...(.|\n)*?"
    r".*ilinkarm.*-o\s.*?(?P<build_output_filename>[\w.]+)\s.*[\n\s]*IAR ELF(.|\n)*?"
    r"(?P<flash_code_size>[\d']+).+readonly\s+code.+\n\s+"
    r"(?P<flash_data_size>[\d']+).+readonly\s+data.+\n\s+"
    r"(?P<ram_size>[\d']+).+readwrite\s+data.+"
)

WARNING_PATTERN = (
    r"(?:\"?(.*?)\"?[\(,](\d+)\)?\s+(?::\s)?)"
    r"(Error|Remark|Warning|Fatal[E|e]rror)\[(.*)\]: (.*)$"
)
