# Charge-Self-Consistent ghostGA Calculation

This directory is used to perform the multi-iteration charge-self-consistent (CSC) ghostGA calculation.

Before starting this calculation, first complete the validation calculation in:

```text
../os/
```

and verify that the projected low-energy model and PLO DOS are reasonable.

## 1. Check the `solid_dmft` path in `main.py`

Open `main.py` and locate:

```python
default_config_name
```

The path to the `solid_dmft` installation is system dependent.

The path included in this example corresponds to the original computing environment and may need to be changed.

Make sure that it points to the `solid_dmft` directory containing:

```text
io_tools/default.toml
```

## 2. Link the converged VASP files

Run:

```bash
./link_files.sh
```

This creates symbolic links to the required files from `../scf/`:

```text
CHGCAR
WAVECAR
KPOINTS
POSCAR
POTCAR
```

Therefore, the initial VASP calculation in `../scf/` must be completed before starting the CSC calculation.

## 3. Check `grisb_config.toml`

The CSC calculation uses the low-energy model that was validated in `../os/`.

For this example:

```toml
csc = true
n_iter_grisb = 25
```

Therefore, the calculation can proceed for multiple ghostGA iterations.

The interaction parameters used in this FeSe example are:

```toml
U = 3.0
J = 0.3
```

Other parameters, such as:

```text
norb_baths
beta
grisb_mix
grisb_tol
dc_type
n_iter_grisb
```

should also be checked before applying this setup to another system or interaction strength.

## 4. Run the CSC calculation

Start the calculation with:

```bash
./run.sh
```

The MPI settings in `run.sh` may need to be modified according to your computing environment.

The calculation will iterate between the DFT and ghostGA parts according to the settings in `grisb_config.toml`.

## 5. Check convergence

Monitor the calculation output and verify that the relevant ghostGA and charge-self-consistency quantities converge.

The number of iterations required for convergence depends on the system and interaction parameters.

Therefore:

```toml
n_iter_grisb = 25
```

should be regarded as the maximum number of ghostGA iterations used in this example rather than a requirement that every calculation must run exactly 25 iterations.

## Important Note

The PLO energy window, band window, and projected DOS should already have been checked in `../os/`.

If the projected low-energy model is incorrect, running additional CSC iterations will not correct the projection.

Return to:

```text
../os/
```

and recheck the PLO setup before continuing.
