# .toolchain/tests/cases/workflows.toml

The group `workflows` checks `.toolchain/tools/workflows.py`.
The first case checks the workflows of the template.
The other cases write a small project into `{case}/p` with `files`: `.toolchain/project.toml` and one workflow.

| Case | Claim | False variant |
| --- | --- | --- |
| the workflows of the template | `workflows.py` finds no fault in the 4 workflows of the template: `no fault in 4 workflows`. | A project whose `ci.yml` lacks the target `aarch64-windows-gnu`. |
| a target that a workflow does not build | A `ci.yml` with 5 targets: `.github/workflows/ci.yml: the matrix does not build aarch64-windows-gnu`. | The same file with the 6 targets. |
| a name that is not a target | A `ci.yml` with the 6 targets and `riscv64-linux-gnu`: `.github/workflows/ci.yml: riscv64-linux-gnu is not a target of the toolchain`. | The 6 targets only. |
| a workflow with no matrix | A `cla.yml` with no line `- target:` makes no fault. | The file gets the line `- target: x86_64-linux-gnu`, so its matrix lacks 5 targets. |
