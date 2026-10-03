import numpy as np
np.set_printoptions(precision=6,suppress=True)
from triqs.plot.mpl_interface import plt,oplot

import pymatgen.io.vasp.outputs as vio
from pymatgen.electronic_structure.dos import CompleteDos
from pymatgen.electronic_structure.core import Spin, Orbital, OrbitalType

energies = []
dosds = []
dosps = []
for imp in range(2):
    data = np.loadtxt(f'pdos_0_{imp}.dat', unpack=True)
    energies.append(data[0])
    dosds.append(data[1:])
for imp in range(2):
    data = np.loadtxt(f'pdos_1_{imp}.dat', unpack=True)
    dosps.append(data[1:])

vasprun = vio.Vasprun('./vasprun.xml')
dos = vasprun.complete_dos
V_spd_dos = dos.get_element_spd_dos("Fe")
O_spd_dos = dos.get_element_spd_dos("Se")

fig, ax = plt.subplots(1,dpi=150,figsize=(7,4))
plt.title('EF=%.5f'%(vasprun.efermi))

ax.plot(vasprun.tdos.energies - vasprun.efermi , vasprun.tdos.densities[Spin.up], 'b-', label=r'total DOS', lw = 2)
ax.plot(vasprun.tdos.energies - vasprun.efermi , V_spd_dos[OrbitalType.d].densities[Spin.up], 'r-', label=r'Fe-d', lw = 2)
ax.plot(vasprun.tdos.energies - vasprun.efermi , O_spd_dos[OrbitalType.p].densities[Spin.up], 'g-', label=r'Se-p', lw = 2)
ax.plot(energies[0], np.sum(dosds, axis=(0, 1)) + np.sum(dosps, axis=(0, 1)), 'b--x', label=r'total PLO', lw=2)
ax.plot(energies[0], np.sum(dosds, axis=(0, 1)), 'r--x', label=r'Fe-d PLO', lw=2)
ax.plot(energies[0], np.sum(dosps, axis=(0, 1)), 'g--x', label=r'Se-p PLO', lw=2)
ax.axvline(0, c='k', lw=1)

#ax.plot(vasprun.tdos.energies, vasprun.tdos.densities[Spin.up], 'b-', label=r'total DOS', lw = 2)
#ax.plot(vasprun.tdos.energies, V_spd_dos[OrbitalType.d].densities[Spin.up], 'r-', label=r'V-d', lw = 2)
#ax.plot(vasprun.tdos.energies, O_spd_dos[OrbitalType.p].densities[Spin.up], 'g-', label=r'O-p', lw = 2)
##ax.plot(energies[0], np.sum(dosds, axis=(0,1)), 'r--', label=r'V-t2g PLO', lw=2)
##ax.plot(energies[0], np.sum(dosps, axis=(0,1)), 'g--', label=r'O-p PLO', lw=2)
#ax.axvline(vasprun.efermi, c='k', lw=1)

ax.set_xlabel('Energy relative to Fermi energy (eV)')
ax.set_ylabel('DOS (1/eV)')
ax.set_xlim(-10,10)
ax.set_ylim(0,30)
ax.legend()
plt.show()
