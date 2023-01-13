import configparser
import h5py

file = 'config.ini'
config = configparser.ConfigParser()
config.read(file)


# print(config.sections())
# print(config['PATHS'])
# print(list(config['PATHS']))


pos_h5_filepath = config['PATHS']['pos_h5_filepath']

with h5py.File(pos_h5_filepath, 'r') as f:
    model = f['model'][()]
    print(model)
