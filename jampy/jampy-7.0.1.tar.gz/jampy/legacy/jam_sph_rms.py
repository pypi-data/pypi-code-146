"""
For legacy compatibility

"""

from jampy.jam_sph_proj import jam_sph_proj

def jam_sph_rms(*args, **kwargs):
    jam = jam_sph_proj(*args, **kwargs)
    return jam.model, jam.ml, jam.chi2