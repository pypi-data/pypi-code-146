__version__ = '0.1.6'
__author__ 		= ['Luís Teixeira']
__credits__ 	= ["Luís Teixeira"]
__license__ 	= "MIT"
__maintainer__ 	= ['Luís Teixeira']
__email__ 		= ['micboucinha@gmail.com']
__status__ 		= "Development"

from confapp import conf

conf += 'pybpod_soundcard_module.settings'

from pybpod_soundcard_module.module import SoundCard as BpodModule
