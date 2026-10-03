# Single-Iteration Validation Calculation

This directory is used to perform a short ghostGA calculation before starting the full charge-self-consistent (CSC) calculation.

The purpose of this step is to construct and inspect the projected low-energy model, verify the PLO setup, and confirm that the projection is reasonable before continuing to the longer calculation in `../csc/`.

The workflow is:

```text
SCF
 ↓
link_files.sh
 ↓
single ghostGA iteration
 ↓
convert.py
 ↓
plot_dos.py
 ↓
check the PLO DOS
 ↓
proceed to ../csc/
```

## 1. Check the `solid_dmft` path in `main.py`

Before running the calculation, open `main.py` and locate:

```python
default_config_name
```

The path to the `solid_dmft` installation is system dependent. The path included in this example corresponds to the original computing environment and must be changed if `solid_dmft` is installed elsewhere.

Make sure that the path points to the `solid_dmft` directory containing:

```text
io_tools/default.toml
```

## 2. Complete the VASP SCF calculation

The VASP calculation in `../scf/` must be completed first.

This calculation provides the converged DFT files required by the ghostGA workflow.

## 3. Link the required VASP files

Run:

```bash
./link_files.sh
```

This script creates symbolic links to:

```text
../scf/CHGCAR
../scf/WAVECAR
../scf/KPOINTS
../scf/POSCAR
../scf/POTCAR
```

The expected directory structure is:

```text
VASP-version/
├── scf/
├── os/
└── csc/
```

## 4. Check the PLO energy and band windows

Before running ghostGA, make sure that the relevant parameters in `INCAR` and `plo.cfg` are appropriate for the calculated electronic structure.

Important parameters include:

```text
INCAR:
EMIN
EMAX
NBANDS
```

and

```text
plo.cfg:
EWINDOW
BANDS
```

The selected energy and band windows should include the Fe-d and Se-p states used to construct the low-energy model.

If the default `NBANDS` does not provide enough Kohn-Sham bands to cover the desired energy range, increase `NBANDS`.

`EWINDOW` in `plo.cfg` is defined relative to the Fermi energy. The exact values of `EMIN`, `EMAX`, `NBANDS`, `EWINDOW`, and `BANDS` should be determined from the calculated electronic structure rather than copied directly to another material.

A useful reference for constructing and inspecting projected local orbitals (PLOs) is:

https://triqs.github.io/solid_dmft/latest/tutorials/NNO_os_plo_mag/tutorial.html

## 5. Run the single-iteration validation calculation

In this directory, `grisb_config.toml` contains:

```toml
n_iter_grisb = 1
```

Therefore, only one ghostGA iteration is performed in this validation step.

Run:

```bash
./run.sh
```

The MPI settings in `run.sh` may need to be modified according to your computing environment.

## 6. Convert the VASP/PLO data with `convert.py`

After the calculation is completed, run:

```bash
python3 convert.py
```

`convert.py` performs two main tasks:

1. It constructs the projected local orbital (PLO) data according to `plo.cfg`.
2. It converts the VASP/PLO data into the HDF5 format used by the ghostGA/TRIQS workflow.

The conversion generates `FeSe.h5`, which is used by the subsequent consistency checks and ghostGA workflow.

## 7. Inspect the projected DOS with `plot_dos.py`

Run:

```bash
python3 plot_dos.py
```

`plot_dos.py` compares the orbital-resolved DOS obtained directly from VASP with the DOS reconstructed from the projected local orbitals.

For this FeSe example, the script compares:

- total VASP DOS with total PLO DOS,
- Fe-d DOS with Fe-d PLO DOS,
- Se-p DOS with Se-p PLO DOS.

The Fermi energy is shifted to:

```text
EF = 0 eV
```

The PLO DOS should reproduce the relevant VASP DOS reasonably well within the selected low-energy window.

If the PLO DOS differs significantly from the corresponding VASP DOS, recheck:

```text
EMIN
EMAX
NBANDS
EWINDOW
BANDS
```

before proceeding to the CSC calculation.

## 8. Optional: check the band-window consistency

After `FeSe.h5` has been generated, run:

```bash
python3 check.py
```

For every k-point, the script verifies:

```text
upper_band - lower_band + 1 = n_orbitals
```

For example:

```text
0 16 3 18 16
```

means that bands 3 through 18 are included:

```text
18 - 3 + 1 = 16
```

which is consistent with:

```text
n_orbitals = 16
```

If `check.py` finishes without an `AssertionError`, the band-window consistency check has passed.

This only verifies the internal consistency of the selected band window. It does not by itself guarantee that the PLO projection is physically appropriate, so the projected DOS should still be inspected.

## 9. Continue to the CSC calculation

If the projected DOS is satisfactory, proceed to:

```text
../csc/
```

and perform the multi-iteration charge-self-consistent calculation.
