# Soft-Repulsive Brownian Dynamics — Selected Archive

This is the retained subset of the plain-Codex osmotic-pressure experiment. Read the [execution prompt](../PROMPT_Carnahan_Starling_vs_BD_soft_repulsive_particles.md), [scientific report](REPORT.md) and [package-selection record](PACKAGE_SELECTION.md) for the original task and Codex's account of its work.

The report describes LAMMPS overdamped Brownian dynamics for a finite-range cosine repulsion, with N = 216, nominal volume fractions 0.05, 0.15 and 0.30, and A/kBT = 10 and 100. Pressure combines the ideal term with the configurational pair virial. Carnahan–Starling is a fixed-nominal-diameter reference for hard spheres, rather than an exact target for these soft particles.

## Included materials

- `scripts/`: resource wrapper, input generation, simulation, verification, analysis and report/finalization code.
- `inputs/`: parameter manifests, LAMMPS input scripts and initial configurations.
- [Equation of state](figures/equation_of_state.png), also as [PDF](figures/equation_of_state.pdf), and [sampling diagnostics](figures/sampling_diagnostics.png).
- `REPORT.md` and `PACKAGE_SELECTION.md`: preserved historical bodies with separate publication notices.

## Reproduction boundary

The original workspace was named `test_local/`. This selected archive omits `env/requirements.lock`, the virtual environment, `downloads/`, `source/`, `outputs/`, `validation/`, `logs/`, `execution_log.md`, `timing.json`, `SHA256SUMS` and `REPORT.template.md`.

Consequently, the original `bootstrap.sh` has no dependency lock to read, and the retained analysis has no raw trajectories or completion records. The scripts also expect directories and dependencies that are absent. The commands in the historical report describe the full original workspace; they are not a working reproduction recipe for this checkout. No original simulation, dependency installation, verification script or report generator was executed during publication preparation.

Reproducing the reported results requires recovering the original environment records and omitted evidence, or preparing and validating a new workflow. A new environment or regenerated result must be labelled separately from the historical run. Reported checks, resources and timing remain the original Codex account.

LAMMPS is identified in the retained report as GPL v2; its wheel and upstream sources are not bundled here. The existing [repository license](../../../LICENSE) covers project-owned material and does not replace third-party terms. Consult the [demonstration overview](../README.md) and [provenance inventory](../../PROVENANCE.json) for scope and attribution.

**AI-generated text.** Original experiment guide: Codex, exact original model unrecorded. Publication revision: OpenAI Codex, 2026-11-13; exact revision model unverified. Scientific direction and archive selection are credited in the demonstration overview; independent scientific reproduction is not claimed.
