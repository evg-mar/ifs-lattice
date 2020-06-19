# %matplotlib qt
from ifs_triangular_representation import IfsTriangInteractive
from ifs_bar_representation import IfsBar
from editable_rectangle import EditableRectangle

from universal_set import UniversalSet
from intuitionistic_fuzzy_set import IFS
import matplotlib.pyplot as plt

import os

from ifs_holder_basic import IfsHolderBasic

base_path = '/home/evgeniy/Documents/IFS-Simulator/ifs-lattice/ifsholder/'
base_path = os.getcwd()
file_name = 'ifs_holder.csv'
ifs_basic = IfsHolderBasic(os.path.join(base_path,'ifsholder',  file_name),
                            None)
    
ifs_basic.df_ifs.head


universe = UniversalSet(set(range(50)))

fig = plt.figure()
plt.subplots_adjust(hspace=0.1, wspace=0.1)

# ifs01 = IFS.random(universe, 1, randseed=1)

# indices, mus, nus, pis = ifs01.elements_split()
mus = ifs_basic.get_mus
nus = ifs_basic.get_nus


axes2 = plt.subplot2grid((1,2), (0,1), rowspan=1, colspan=1)
axes2.yaxis.tick_right()
axes2.yaxis.set_ticks_position('both')
axes2.set_aspect('auto', 'datalim')
prop2 = IfsBar('labelBar', EditableRectangle, musnus=(mus, nus), axes=axes2)
# prop2 = IfsTriang(axes2, (mus, nus), radius=.01)
prop2.connect()

axes1 = plt.subplot2grid((1,2), (0,0), rowspan=1, colspan=1)

axes1.set_aspect('equal', 'datalim')
axes1.set_xlim([0,1])
prop1 = IfsTriangInteractive('labelBar2', EditableRectangle, musnus=(mus, nus), axes=axes1, radius=.01)
prop1.connect()

plt.show()



