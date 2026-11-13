> **Archive notice — AI-generated execution prompt.** ChatGPT drafted this prompt from the author's scientific question and constraints; the exact original model is unrecorded. This notice was added for publication and was not part of the prompt given to Codex. The supplied prompt body is preserved verbatim below; its directory names and action requests describe the original experiment, not instructions to execute during review. See the [archive overview](README.md) and [provenance inventory](../PROVENANCE.json).
>
> AI-generated publication notice: OpenAI Codex, 2026-11-13; exact revision model unverified.

<!-- archived-body-start -->
# Baseline Experiment: Autonomous Computational Research with Plain Codex

## 1. Scientific Objective

I would like to investigate the concentration dependence of the osmotic pressure of Brownian particles interacting through a soft-repulsive potential.

The objective is to compare the simulation results with the Carnahan–Starling equation of state and examine how the results change as the repulsive stiffness increases.

**No simulation package or source code is provided intentionally.**

Please independently identify an appropriate existing open-source simulation package, obtain it from a legitimate source, and construct the computational environment necessary to perform this investigation.

You may consider LAMMPS or other suitable open-source Brownian dynamics implementations. You are free to select a different approach if technically justified.

This is an experimental assessment of how far a general-purpose Agentic AI coding system can proceed independently from a scientific problem statement to a working computational prototype.

## 2. Working Directory and Isolation

Create a new directory named:

`test_local/`

under the current project directory.

All work for this experiment must take place within this directory, including:

- Downloaded source code and dependencies
- Build files and configuration
- Simulation input files
- Simulation outputs
- Analysis scripts and figures
- Test scripts and validation results
- Execution logs and documentation

Do not modify files outside `test_local/`.

Keep any original downloaded source code intact where practical, and place modifications and generated files in clearly separated locations.

Do not use or install Workbench-specific plugins, templates, profiles, or protocols for this baseline experiment. Rely on the standard Codex environment and your own technical reasoning.

## 3. Computational Resource Constraints

The simulation must operate within the following limits:

**CPU: Maximum 2 processors/cores**

- Limit simulation workers, MPI processes, OpenMP threads, and numerical-library threads accordingly.
- Prevent unintended oversubscription.
- Do not increase the processor allocation automatically.

**Memory: Maximum 10 GB**

- Keep peak memory usage below 10 GB.
- Avoid excessive memory allocation or swapping.
- Reduce system size if necessary.

**Disk storage: Maximum 10 GB**

- Keep the total disk footprint of `test_local/`, including downloads, source files, build artifacts, temporary files, simulation data, and figures, below 10 GB.
- Remove unnecessary temporary outputs if needed, without discarding important reproducibility information.

Where supported, enforce resource limits at the execution or container level rather than relying only on application settings.

If hard enforcement is not possible, clearly document the limitation and monitor resource consumption.

These are upper limits, not targets. Prefer smaller resource consumption when sufficient for the preliminary experiment.

## 4. Scientific and Computational Tasks

Please independently perform the following tasks.

### A. Package discovery and selection

1. Identify suitable open-source simulation packages.
2. Evaluate whether they support Brownian dynamics with soft-repulsive interactions.
3. Select an appropriate implementation.
4. Record the package source, version, license, and reasons for selection.

### B. Environment construction

1. Obtain the selected package.
2. Inspect its relevant implementation and input format.
3. Configure the necessary dependencies and build environment.
4. Verify that the software can execute a basic test.
5. Record the actual installation and execution procedures.

### C. Simulation

Perform a small CPU-based exploratory investigation using, for example:

- Volume fractions: 0.05, 0.15, and 0.30
- At least two repulsive stiffness values
- Appropriate equilibration and sampling procedures

Choose reasonable particle numbers, integration time steps, and simulation durations under the computational constraints.

Explain any significant numerical assumptions.

### D. Pressure estimation and analysis

1. Determine an osmotic-pressure estimator appropriate for the chosen model and simulation method.
2. Calculate the concentration-dependent osmotic pressure.
3. Compute the corresponding Carnahan–Starling prediction.
4. Compare simulation and theoretical results.
5. Generate a figure showing the concentration dependence for the selected stiffness values.

Include appropriate uncertainty estimates where feasible.

Do not assume that a soft-repulsive system must agree exactly with the hard-sphere equation of state.

Do not artificially adjust the results to obtain agreement.

### E. Verification

Perform reasonable checks appropriate to a preliminary study, such as:

- Build and execution checks
- Basic numerical consistency
- Equilibration and sampling checks
- Time-step sensitivity where feasible
- Pressure estimator consistency
- Unit tests or regression tests where applicable

Distinguish clearly between software verification, numerical convergence, and physical validation.

Do not claim convergence or physical agreement that has not actually been established.

## 5. Autonomous Execution

Please make the necessary technical decisions independently, including package selection, input generation, simulation parameters, and analysis methods.

Avoid requesting user input for routine implementation decisions.

If a package is unsuitable or cannot be obtained, investigate reasonable alternatives.

If resource constraints prevent the intended calculation, reduce the computational scale while preserving a meaningful preliminary test.

Do not modify host-level configuration, weaken sandbox isolation, or bypass required security approvals.

Please execute the calculations rather than merely describing how they could be performed.

Clearly distinguish completed computations from proposed or unverified procedures.

## 6. Time Tracking

**Before beginning any package inspection, installation, or other substantive work, record the experiment's start time.**

Use a precise timestamp with timezone information, preferably ISO 8601.

Save this timestamp in:

`test_local/execution_log.md`

At the end of the experiment:

1. Record the final completion time.
2. Calculate the total elapsed wall-clock time.
3. Report the duration in hours, minutes, and seconds.
4. Record any interruptions or periods requiring user intervention.
5. If available, distinguish the time spent on installation, simulation, analysis, and verification.

The elapsed time must cover the entire experiment, from the initial request processing to completion of the final report.

Do not estimate or invent timestamps or execution durations.

## 7. Reproducibility

Organize the resulting materials so that another researcher could inspect and repeat the experiment.

Provide:

- Source references and software versions
- Dependencies and environment configuration
- Simulation inputs and parameters
- Execution scripts or commands
- Analysis scripts
- Generated data and figures
- Validation results
- Known limitations

Document the exact commands needed to reproduce the calculations.

Record any source-code modifications made during the experiment.

## 8. Final Report

Provide a concise technical report containing:

### Scientific implementation
- Selected simulation package and justification
- Physical model and numerical methodology
- Pressure estimator and assumptions

### Results
- Simulations actually completed
- Numerical results and generated figures
- Comparison with Carnahan–Starling EOS
- Numerical limitations and unresolved questions

### Reproducibility
- Directory structure
- Execution instructions
- Software and dependency versions
- Tests and verification results

### Computational resources
- CPU configuration
- Memory usage, where measured
- Disk usage
- Any resource-limit enforcement limitations

### Time accounting
- Experiment start timestamp
- Experiment end timestamp
- Total elapsed wall-clock time
- Significant interruptions or human interventions

### Overall assessment
- What was successfully achieved autonomously
- What required human intervention
- What remains incomplete
- What would be required to extend the prototype to a more rigorous scientific study

## 9. Final Principle

This is a **Plain Codex baseline experiment**.

The objective is not to demonstrate that one particular package or method is superior.

Instead, evaluate how independently and reliably a general-purpose Agentic AI can:

**Identify an appropriate computational method, construct a working environment, perform a scientific calculation, validate the results, and preserve a reproducible computational prototype.**

Maintain scientific integrity, resource discipline, and transparent reporting throughout the experiment.
