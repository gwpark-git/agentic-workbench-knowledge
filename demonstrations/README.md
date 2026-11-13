# Computational Demonstrations with Plain Codex

These demonstrations show how a scientific question was turned into a computational prototype using general-purpose Codex. The author supplied the scientific questions and practical constraints; ChatGPT drafted detailed execution prompts; Codex produced the implementations, reports and figures. According to the author's account and the retained reports, no Workbench-specific plugins, templates or protocols were used.

Start with the [hard-sphere equation-of-state demonstrations](hard-spheres-eos/README.md). They contain a soft-repulsive Brownian dynamics experiment and a follow-up using constraint-only hard-sphere Monte Carlo.

| Experiment | Execution prompt | Report | Main figure |
|---|---|---|---|
| Soft-repulsive Brownian particles | [Prompt](hard-spheres-eos/PROMPT_Carnahan_Starling_vs_BD_soft_repulsive_particles.md) | [Report](hard-spheres-eos/soft-repulsive-bd/REPORT.md) | [PNG](hard-spheres-eos/soft-repulsive-bd/figures/equation_of_state.png) / [PDF](hard-spheres-eos/soft-repulsive-bd/figures/equation_of_state.pdf) |
| Constraint-only hard spheres | [Prompt](hard-spheres-eos/PROMPT_Carnahan_Starling_vs_MC_hard_spheres.md) | [Report](hard-spheres-eos/hard-sphere-mc/REPORT.md) | [PNG](hard-spheres-eos/hard-sphere-mc/figures/comparison.png) / [PDF](hard-spheres-eos/hard-sphere-mc/figures/comparison.pdf) |

This is a selected archive: prompts, reports, figures, experiment scripts and initialization inputs are included. Raw trajectories, numerical output tables, validation records, environment locks, downloaded packages and execution logs are omitted. The scripts retain dependencies on those omitted materials and on the original directory layout. This checkout is sufficient to inspect the example, but does not provide a complete reproduction environment.

The reports describe the original runs. Their execution times, resource measurements and successful-check claims have not been independently reproduced during publication preparation. These are exploratory examples, with no controlled comparison establishing a Workbench performance benefit or general Codex reliability.

The [provenance inventory](PROVENANCE.json) records the selected files, their hashes and available AI attribution. Added archive notices are separate from the preserved prompt and report bodies. Exact historical model identifiers were not recorded in the supplied materials.

Project-owned material is covered by the repository's existing [CC BY 4.0 notice](../LICENSE). Third-party software and reference material retain their own terms; this grant does not relicense them. Dependencies and upstream source archives are not bundled here. These prototypes may contain scientific or software errors; consult the reports' limitations before reuse.

For the author's motivation, see the [Agentic Workbench introduction](../README.md).

**AI-generated text.** Publication documentation: OpenAI Codex, 2026-11-13; exact revision model unverified. Scientific direction and selection of materials: Gunwoo Park. Original prompt generation: ChatGPT; original implementations, reports and figures: Codex, as reported by the author. Exact original models are unknown; no line-by-line human review is asserted.
