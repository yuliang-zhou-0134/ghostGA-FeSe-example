import h5py

fh5 = h5py.File('FeSe.h5','r')
band_window = fh5['/dft_misc_input/band_window/0'][...]
n_orbitals = fh5['/dft_input/n_orbitals'][...]
fh5.close()

print(band_window.shape)
print(n_orbitals.shape)
for i in range(n_orbitals.shape[0]):
    nb = band_window[i,1] - band_window[i,0] +1
    print(i, n_orbitals[i,0], band_window[i,0], band_window[i,1], nb)
    assert(nb==n_orbitals[i,0])
