import platform

if platform.system() == 'Darwin':
    DEV_TTY = '/dev/cu.usbserial-FT4VOTGK'
elif platform.system() == 'Windows':
    DEV_TTY = 'COM4'
elif platform.system() == 'Linux':
    DEV_TTY = '/dev/ttyUSB0'
