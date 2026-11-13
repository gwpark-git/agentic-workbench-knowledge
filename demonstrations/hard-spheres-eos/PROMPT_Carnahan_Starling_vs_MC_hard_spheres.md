> **Archive notice — AI-generated execution prompt.** ChatGPT drafted this follow-up from the author's scientific question and constraints; the exact original model is unrecorded. This notice was added for publication and was not part of the prompt given to Codex. The supplied prompt body is preserved verbatim below; its directory names and action requests describe the original experiment, not instructions to execute during review. See the [archive overview](README.md) and [provenance inventory](../PROVENANCE.json).
>
> AI-generated publication notice: OpenAI Codex, 2026-11-13; exact revision model unverified.

<!-- archived-body-start -->
# Follow-up Task: Hard-Sphere Equation of State Using a Potential-Free Algorithm

## 1. Objective

We have previously investigated the concentration-dependent osmotic pressure of Brownian particles interacting through a soft-repulsive potential and compared the results with the Carnahan–Starling equation of state.

I would now like to extend this investigation to **true hard-sphere particles using a potential-free, constraint-based algorithm**.

The objective is to calculate the hard-sphere osmotic pressure as a function of volume fraction and compare the results with the Carnahan–Starling equation.

Unlike the previous investigation, do not approximate hard spheres simply by increasing the stiffness of a soft-repulsive potential.

## 2. Computational Approach

Please independently investigate and select an appropriate hard-sphere simulation algorithm.

You may use an existing open-source implementation or develop a small numerical implementation if justified.

The method should enforce hard-sphere excluded-volume constraints without relying on a finite soft-repulsive potential.

Determine the most appropriate method for calculating the equilibrium equation of state. If you select an equilibrium Monte Carlo method rather than Brownian dynamics, explicitly distinguish equilibrium sampling from physical Brownian time evolution.

In particular:

- Explain the selected algorithm and its assumptions.
- Implement or configure an appropriate hard-sphere pressure estimator.
- Do not reuse the previous soft-potential virial estimator without establishing its applicability.
- Verify that the hard-sphere constraints are correctly enforced.

Make the necessary technical decisions independently.

## 3. Numerical Investigation

Use the same nominal volume fractions as the previous investigation:

- φ = 0.05
- φ = 0.15
- φ = 0.30

Use the same particle diameter convention and reduced units where possible.

Perform appropriate equilibration and production sampling, with independent replicas and uncertainty estimates.

Compare the measured compressibility factor

\[
Z=\frac{\Pi}{\rho k_BT}
\]

with the Carnahan–Starling equation

\[
Z_{\mathrm{CS}}(\phi)=
\frac{1+\phi+\phi^2-\phi^3}{(1-\phi)^3}.
\]

Do not impose agreement with Carnahan–Starling through fitting or numerical adjustments.

Where computationally feasible, examine numerical sensitivity and relevant finite-size or sampling effects.

## 4. Continuation of the Previous Experiment

This is a continuation of the existing computational investigation.

Please inspect the previous results and reuse any valid computational resources, analysis scripts, or verification methods where appropriate.

However, do not assume that the numerical methods used for soft-repulsive particles remain valid for hard spheres.

Create a separate directory named:

`hard_sphere_extension/`

within the current experiment directory.

Preserve the previous soft-particle calculations and their results without modification.

Generate a comparison figure including:

1. Previous soft-repulsive results for A/kBT = 10.
2. Previous soft-repulsive results for A/kBT = 100.
3. New hard-sphere simulation results.
4. Carnahan–Starling prediction.

Clearly identify differences in numerical methodology and uncertainty estimates.

## 5. Computational Constraints

Maintain the previous computational resource limits:

- Maximum 2 CPU cores.
- Maximum 10 GB memory usage.
- Maximum 10 GB total experimental workspace disk usage.

Use smaller systems or shorter exploratory calculations if necessary, while documenting their limitations.

Do not modify host-level configuration or bypass sandbox security requirements.

## 6. Execution and Verification

Please perform the numerical calculations rather than only proposing an implementation.

Verify the selected algorithm using appropriate independent checks.

Distinguish clearly between:

- Algorithmic correctness.
- Numerical and statistical convergence.
- Physical agreement with the Carnahan–Starling equation.

If the selected algorithm has limitations that prevent reliable pressure estimation, explain them and investigate an appropriate alternative.

Do not report unverified calculations as completed results.

## 7. Time and Workflow Tracking

Record the start timestamp before beginning substantive work and the completion timestamp after finishing the experiment.

Report the total elapsed wall-clock time, including environment preparation, implementation, simulation, analysis, verification, and documentation.

Also record:

- Which components of the previous computational environment were reused.
- Which components required modification or replacement.
- Any new software or algorithms introduced.
- Any Workbench-specific capabilities actually used, if applicable.
- Human interventions, failures, retries, and their consequences.

Do not invoke additional procedures solely for the purpose of demonstrating Workbench.

## 8. Final Report

Prepare a concise technical report containing:

1. Selected hard-sphere algorithm and justification.
2. Pressure estimator and its theoretical basis.
3. Actual simulation parameters and completed calculations.
4. Numerical results with uncertainties.
5. Comparison with Carnahan–Starling and the previous soft-particle results.
6. Verification, sensitivity checks, and unresolved limitations.
7. Reproducibility instructions and generated figures.
8. Total execution time and computational resources.
9. Assessment of how much of the previous computational environment could be reused.

The main purpose is to examine whether an existing computational prototype can be extended to a physically different numerical representation while preserving appropriate verification and reproducibility.

Please proceed autonomously and distinguish actual results from proposed future improvements.
