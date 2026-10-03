# FeSe ghostGA Example

This repository provides a minimal example of applying ghostGA to FeSe.

The workflow consists of three stages:

1. Perform the initial DFT calculation in `scf/`.
2. Perform a one-shot ghostGA calculation in `os/` and check the projected low-energy model.
3. If the projection is reasonable, continue with the charge-self-consistent calculation in `csc/`.

## Directory Structure

```text
.
├── scf/
├── os/
└── csc/
```

- `scf/`: initial VASP self-consistent calculation.
- `os/`: one-shot ghostGA calculation used to construct and inspect the low-energy model.
- `csc/`: charge-self-consistent ghostGA calculation with multiple iterations.

---

## 1. Run the SCF Calculation

Enter the `scf` directory and complete the VASP self-consistent calculation.

```bash
cd scf
```

Run VASP using the appropriate command for your computing environment.

The converged SCF calculation provides the DFT files required by the following ghostGA calculations.

---

## 2. Prepare the One-Shot Calculation

After the SCF calculation is completed, enter the `os` directory:

```bash
cd ../os
```

Run:

```bash
./link_files.sh
```

This script links or copies the required files from the completed SCF calculation into the one-shot calculation directory.

The `os` calculation is intended to run only one ghostGA iteration. Its main purpose is to construct and inspect the projected low-energy model before starting the full charge-self-consistent calculation.

---

## 3. Run the One-Shot Calculation

Run:

```bash
./run.sh
```

Wait until the one-shot calculation is completed.

---

## 4. Convert the Output

After the one-shot calculation is finished, run:

```bash
python3 convert.py
```

This converts the calculation results into the format required for the subsequent analysis.

---

## 5. Check the Projected Low-Energy Model

Run:

```bash
python3 plot_dos.py
```

Inspect the resulting DOS and check whether the Fe-\(d\) and Se-\(p\) states are projected correctly within the selected low-energy window.

The energy and band windows should be chosen based on the electronic structure of the system.

A useful reference for constructing and inspecting projected local orbitals (PLOs) is the solid_dmft tutorial:

https://triqs.github.io/solid_dmft/latest/tutorials/NNO_os_plo_mag/tutorial.html

### Energy-window setup

Before starting the ghostGA calculation, the projected DOS should be inspected to determine suitable values of:

```text
EMIN
EMAX
NBANDS
```

in the VASP `INCAR`, and

```text
EWINDOW
BANDS
```

in `plo.cfg`.

`EMIN` and `EMAX` should cover the relevant Fe-\(d\) and Se-\(p\) states used for constructing the projectors.

If the default value of `NBANDS` does not include enough Kohn-Sham bands to cover the desired energy range, increase `NBANDS`.

In `plo.cfg`, `EWINDOW` defines the energy window relative to the Fermi energy:

```text
EF = 0 eV
```

The selected `EWINDOW` should include the relevant Fe-\(d\) and Se-\(p\) states.

`BANDS` specifies the corresponding VASP band-index range and should be consistent with the selected energy window.

These parameters should be determined from the calculated electronic structure rather than copied directly from another material.

---

## 6. Prepare the Charge-Self-Consistent Calculation

If the projected DOS and low-energy model from the one-shot calculation are reasonable, enter the `csc` directory:

```bash
cd ../csc
```

Run:

```bash
./link_files.sh
```

This prepares the required files for the charge-self-consistent calculation.

---

## 7. Run the Charge-Self-Consistent Calculation

Start the CSC calculation with:

```bash
./run.sh
```

Unlike the `os` calculation, the `csc` calculation performs multiple ghostGA/DFT iterations.

The calculation should be continued until the desired convergence criteria are satisfied.

---

## Optional: Check the Band Window

After generating the HDF5 file, the consistency of the selected band window can be checked with:

```bash
python3 check.py
```

For every k-point, the script verifies that

```text
upper_band - lower_band + 1 = n_orbitals
```

For example,

```text
0 16 3 18 16
```

means that bands 3 through 18 are included:

```text
18 - 3 + 1 = 16
```

which is consistent with `n_orbitals = 16`.

If `check.py` finishes without an `AssertionError`, the band-window consistency check has passed.

Note that this is a consistency check of the selected band window. The physical quality of the projected low-energy model should still be inspected using the projected DOS.
