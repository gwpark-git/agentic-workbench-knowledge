# Constraint-Only Hard-Sphere Monte Carlo — Selected Archive

This is the retained subset of the plain-Codex hard-sphere extension. Start with the [follow-up execution prompt](../PROMPT_Carnahan_Starling_vs_MC_hard_spheres.md) and the [scientific report](REPORT.md).

Codex selected an equilibrium NVT Metropolis sampler that rejects overlapping trial configurations. The pressure estimators use contact extrapolation and virtual compression. MC sweeps are sampling steps, not physical Brownian time; this experiment makes no transport or Brownian-trajectory claim.

The report describes three replicas at each nominal volume fraction 0.05, 0.15 and 0.30 for N = 216, plus N = 512 and proposal-size checks at 0.30. The reported error bars estimate sampling uncertainty and do not include every finite-size or estimator-extrapolation effect.

## Included materials

- `scripts/`: sampler, pressure estimators, resource wrapper, verification, analysis and report/finalization code.
- `inputs/`: parameter manifests and simple-cubic initial positions in NumPy format.
- [Comparison](figures/comparison.png), also as [PDF](figures/comparison.pdf), [sampling diagnostics](figures/sampling.png) and [estimator checks](figures/estimator_checks.png).
- `REPORT.md`: the preserved historical report body, preceded by a separate publication notice.

## Reproduction boundary

The original directory was `test_local/hard_sphere_extension/`, nested within the earlier soft-particle experiment. This archive instead places the two experiments side by side. The retained scripts still expect the original layout: `reproduce.sh` uses `../env/venv/bin/python`, and `analyze.py` reads the prior soft results from `../outputs/summary.csv`.

Those parent resources are absent. This subset also omits the extension dependency locks and environment, raw `outputs/`, `validation/`, `logs/`, `source/`, timing/checksum files and `REPORT.template.md`. In particular, `verify.py` loads the omitted `source/allen_tildesley_mc_hs_module.py` reference; its archived agreement claims cannot be rerun from this checkout alone.

The original bootstrap, reproduction, analysis and checksum instructions therefore require the full original workspace. No simulation, dependency installation or historical verification script was executed during publication preparation. Recover the original materials, or construct and validate a separately labelled new workflow, before attempting reproduction.

The report credits the [Allen–Tildesley examples](https://github.com/Allen-Tildesley/examples), snapshot `5c4266fcdebe6271f07529d9182bfaef54fcaaed`, as a CC0 verification reference. Those reference files are not bundled. The sampler is described as independently written; the repository's existing [license](../../../LICENSE) does not relicense third-party material. See the [demonstration overview](../README.md) and [provenance inventory](../../PROVENANCE.json).

**AI-generated text.** Original experiment guide: Codex, exact original model unrecorded. Publication revision: OpenAI Codex, 2026-11-13; exact revision model unverified. Scientific direction and archive selection are credited in the demonstration overview; independent scientific reproduction is not claimed.
