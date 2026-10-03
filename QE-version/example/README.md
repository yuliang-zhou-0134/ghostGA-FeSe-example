# FeSe ghostGA Example with Quantum ESPRESSO

This directory contains a Quantum ESPRESSO + Wannier90 setup used for the FeSe ghostGA calculation.

The purpose of this example is to provide a working input set for the present FeSe calculation. It is not intended to be a comprehensive tutorial on Quantum ESPRESSO or Wannier90.

Unlike the VASP example, a separate single-iteration validation workflow is not provided here.

## Workflow

The main workflow is:

```text
Quantum ESPRESSO SCF
        ↓
Quantum ESPRESSO NSCF
        ↓
Wannier90 projection
        ↓
Fe-d + Se-p low-energy model
        ↓
ghostGA
        ↓
QE / ghostGA charge-self-consistent iterations
```

The corresponding files are:

```text
example/
├── fese.scf.in
├── fese.nscf.in
├── fese.win
├── fese.pw2wan.in
├── fese.inp
├── fese.mod_scf.in
├── grisb_config.toml
├── main.py
├── run.sh
└── bnd/
```

The pseudopotentials used by the example are stored in:

```text
../pseudo/
```

---

## 1. Initial Quantum ESPRESSO SCF calculation

`fese.scf.in` contains the initial self-consistent DFT calculation.

For this example, the k-point mesh is:

```text
8 × 8 × 4
```

and the FeSe unit cell contains:

```text
2 Fe atoms
2 Se atoms
```

The converged SCF calculation provides the charge density and wave functions required for the following calculations.

---

## 2. NSCF calculation

`fese.nscf.in` contains the non-self-consistent calculation used for the Wannier90 projection.

The calculation uses an explicit uniform k-point mesh corresponding to the same:

```text
8 × 8 × 4
```

grid.

In this example, symmetry is disabled in the NSCF input and the full set of 256 k-points is explicitly listed.

The NSCF output is subsequently used together with Wannier90 to construct the low-energy model.

---

## 3. Wannier90 low-energy model

The Wannier90 setup is defined in:

```text
fese.win
```

The projected subspace contains Fe-d and Se-p orbitals.

For the FeSe unit cell used here:

```text
2 Fe atoms × 5 d orbitals = 10 orbitals
2 Se atoms × 3 p orbitals = 6 orbitals
```


giving a total of:

```text
10 + 6 = 16 Wannier orbitals
```

Therefore,

```text
num_wann = 16
```

is used for the target Wannier subspace.

In this particular setup,

```text
num_bands = 16
```

is also used. Note that `num_wann` and `num_bands` represent different
quantities and do not generally have to be equal.
```

The orbital projections are:

```text
Fe: dxy, dyz, dz2, dxz, dx2-y2
Se: px, py, pz
```

The Wannier90 k-point mesh must remain consistent with the QE NSCF calculation.

---

## 4. QE to Wannier90 interface

`fese.pw2wan.in` contains the input for the Quantum ESPRESSO to Wannier90 interface.

It uses:

```text
prefix   = fese
seedname = fese
```

and generates the matrix-element files required by Wannier90.

`fese.inp` contains additional information used by the Wannier90/TRIQS converter, including the k-point mesh and correlated-shell definition.

For this FeSe example, the correlated shells correspond to the two Fe d shells.

---

## 5. Charge-self-consistent input

`fese.mod_scf.in` is the modified Quantum ESPRESSO SCF input used during the charge-self-consistent cycle.

It should not be confused with the initial:

```text
fese.scf.in
```

The modified input contains settings specific to the coupled ghostGA/QE cycle, including:

```text
restart_mode = 'restart'
dmft         = .true.
dmft_prefix  = 'fese'
```

and uses the previously generated charge density and wave functions as the starting point.

---

## 6. ghostGA configuration

The ghostGA calculation is controlled by:

```text
grisb_config.toml
```

For this example:

```toml
csc = true

U = 3.0
J = 0.3

norb_baths = [5, 5]
n_iter_grisb = 25
```

There are two correlated Fe sites, each containing five d orbitals.

The DFT interface is configured as:

```toml
[dft]
dft_code = "qe"
projector_type = "w90"
dft_exec = "pw.x"
```

Thus, Quantum ESPRESSO is used as the DFT code and Wannier90 is used to construct the projected low-energy model.

The MPI and executable settings may need to be modified according to the local computing environment.

---

## 7. Check the `solid_dmft` path

Before running the calculation, open:

```text
main.py
```

and locate:

```python
default_config_name
```

The path included in this example corresponds to the original computing environment.

It must be changed if `solid_dmft` is installed in a different location.

The path should point to the `solid_dmft` installation containing:

```text
io_tools/default.toml
```

---

## 8. Run the ghostGA / QE calculation

After the required QE and Wannier90 preparation files have been generated, start the coupled calculation with:

```bash
./run.sh
```

The present example is configured for a multi-iteration charge-self-consistent calculation.

Unlike the VASP example, this directory does not provide a separately tested single-iteration validation setup.

---

## Optional: DFT band structure

The `bnd/` directory contains a Quantum ESPRESSO band-structure input along the high-symmetry path:

```text
Γ-X-M-Γ-Z-R-A-Z
```

This calculation is not required for running the ghostGA charge-self-consistent workflow.

It is included only as an additional reference for the underlying DFT electronic structure.

---

## Notes

This repository provides the input files used for this specific FeSe calculation.

Parameters such as:

```text
ecutwfc
ecutrho
k-point mesh
pseudopotentials
Wannier projections
U
J
```

should be checked independently before applying the setup to another system.

For a more complete description of the Quantum ESPRESSO/Wannier90 interface, refer to the official Quantum ESPRESSO, Wannier90, TRIQS DFTTools, and solid_dmft documentation.
