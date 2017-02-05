"""
Testing new spectra class
"""
from collections import OrderedDict
import numpy as np
import xarray as xr
from spectra import NewSpecArray
from pymo.data.spectra import SwanSpecFile

# freq = [0.04 * 1.1**n for n in range(10)]
# dirs = range(0, 360, 90)
# data = np.random.randint(1, 10, (len(freq), len(dirs)))

# da = xr.DataArray(data=data,
#                   dims=('freq','dir'),
#                   coords={'freq': freq, 'dir': dirs})

#=================================
# Real spectra, input as DataArray
#=================================
spectra = SwanSpecFile('/Users/rafaguedes/work/prelud0.spec')
spec_list = [s for s in spectra.readall()]

spec_array = np.concatenate([np.expand_dims(s.S, 0) for s in spec_list])
coords=OrderedDict((('time', spectra.times), ('freq', spec_list[0].freqs), ('dir', spec_list[0].dirs)))
# coords=OrderedDict((('dumb_time_name', spectra.times), ('freq', spec_list[0].freqs), ('dir', spec_list[0].dirs)))

darray = xr.DataArray(data=spec_array, coords=coords)
# da = NewSpecArray(darray, dim_map={'dumb_time_name': 'time'})

hs_new = darray.spec.split(fmin=0.05, fmax=0.2).spec.hs()
# hs_old = [s.split([0.05,0.2]).hs() for s in spec_list]
# for old, new, t in zip(hs_old, hs_new, hs_new.time.to_index()):
#     print ('Hs old for %s: %0.4f m' % (t, old))
#     print ('Hs new for %s: %0.4f m\n' % (t, new))

new = darray.spec.split(fmin=0.05, fmax=0.2).spec.tp()
old = [s.split([0.05,0.2]).tp() for s in spec_list]
for o, n, t in zip(old, new, hs_new.time.to_index()):
    print ('Tp old for %s: %0.4f m' % (t, o))
    print ('Tp new for %s: %0.4f m\n' % (t, n))
