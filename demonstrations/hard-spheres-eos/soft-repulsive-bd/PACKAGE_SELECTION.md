> **Archive notice — AI-generated historical selection record.** Codex produced this record; the exact original model is unrecorded. The supplied body is preserved verbatim below. Its references to retained wheels, upstream source excerpts, metadata and blocked-request records describe the original full workspace. Those archives are omitted from this public subset; upstream URLs and package/license statements below are historical source references, not newly verified acquisitions. See the current [experiment guide](README.md) and [provenance inventory](../../PROVENANCE.json).
>
> AI-generated publication notice: OpenAI Codex, 2026-11-13; exact revision model unverified.

<!-- archived-body-start -->
# Package discovery and selection

| Package | Evidence inspected | Brownian dynamics and soft repulsion | Decision |
|---|---|---|---|
| LAMMPS | Versioned upstream `fix_brownian.cpp`, `fix_brownian_base.cpp`, `pair_soft.cpp`; matching command documentation and license | Overdamped translation with Gaussian noise; finite-range cosine pair potential; native pair virial; CPU neighbor lists | Selected: minimal model code, explicit virial estimator, compatible prebuilt Linux AArch64 wheel |
| HOOMD-blue | Upstream `hoomd/md/methods/methods.py`, `hoomd/md/pair/pair.py`, license | `Brownian` method; soft conservative DPD pair interactions available through `DPDConservative` | Suitable alternative; not installed or benchmarked. No need to build another environment after LAMMPS worked |
| OpenMM | Upstream `BrownianIntegrator.cpp` and `CustomNonbondedForce.h` | Brownian integrator; custom algebraic soft pair forces and cutoffs | Suitable alternative; not installed or benchmarked. Pressure would require additional estimator implementation |

HOOMD and OpenMM documentation hosts returned HTTP 403 with approval-required bodies. These bodies are saved in `source/*_doc_block.txt`. No approval was requested, policy changed, or blocked host bypassed. Publicly accessible GitHub source supplied the needed information. These unsuccessful optional documentation requests did not prevent the experiment.

Selected package: **LAMMPS 22 Jul 2025, Update 4** (`lammps==2025.7.22.4.0` on PyPI), GPL version 2. Source tag: `stable_22Jul2025_update4`. The tag API response and its annotated-tag metadata are archived. See `source/lammps_annotated_tag.json` for the resolved upstream commit.

Legitimate sources:

- Upstream: <https://github.com/lammps/lammps>
- Versioned upstream source: <https://github.com/lammps/lammps/tree/stable_22Jul2025_update4>
- PyPI release metadata: <https://pypi.org/pypi/lammps/2025.7.22.4.0/json>
- Wheel builder linked by the PyPI project: <https://github.com/njzjz/lammps-wheel>
- HOOMD source: <https://github.com/glotzerlab/hoomd-blue>
- OpenMM source: <https://github.com/openmm/openmm>

The original LAMMPS wheel is retained under `downloads/`, verified against the SHA-256 in PyPI release metadata. Original relevant source files and input documentation are retained under `source/`; this is a source excerpt, not a complete source checkout. The upstream implementation was not modified. New scripts only generate inputs, call the package, analyze output, and verify results. A compiler/source build was unnecessary because the compatible wheel executed successfully.

Implementation inspection confirmed that `fix brownian` advances positions by force drift plus random displacement, while storing displacement divided by timestep as velocity. Therefore a conventional kinetic pressure from those velocities is inappropriate. `compute pv all pressure NULL pair` supplies only the pair virial. The ideal reservoir term is added explicitly. `pair soft` implements `A*(1+cos(pi*r/rc))` for `r<rc`, with force `A*pi/rc*sin(pi*r/rc)`.
