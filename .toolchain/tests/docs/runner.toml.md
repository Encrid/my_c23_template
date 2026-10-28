# .toolchain/tests/cases/runner.toml

The group `runner` checks `.toolchain/tools/runner.py`.
Each case writes `.toolchain/project.toml` into `{case}` with `files`, and runs `runner.py --root {case}` for a named target.
A case cannot install a package or start a display on each machine. Thus each case checks the commands that `runner.py` writes, and runs none of them.
Each machine writes the same commands for a named target. So each case gives the same output on each machine.

| Case | Claim | False variant |
| --- | --- | --- |
| a project with no needs gives no command | `.toolchain/project.toml` has no `[ci]`. `runner.py` writes nothing for `x86_64-linux-gnu`. | The project needs `vulkan`. |
| the display on Linux | For `display` on `x86_64-linux-gnu`, `runner.py` writes the commands of `.toolchain/docs/runner.py.md`, *Linux*, in their order. | The target `x86_64-windows-gnu`, which needs no command. |
| Vulkan on Linux | For `vulkan` on `aarch64-linux-gnu`, `runner.py` installs `libvulkan1` and `mesa-vulkan-drivers`, and starts no Xvfb. | The target `aarch64-macos`. |
| OpenGL on Linux | For `gl` on `x86_64-linux-gnu`, `runner.py` installs `libgl1`, `libgl1-mesa-dri` and `libglx-mesa0`. | The target `x86_64-macos`. |
| the packages of each need in one install | For the 3 needs on `aarch64-linux-gnu`, one `apt-get install` names the 8 packages, in the order of their names. | The project needs only `vulkan`. |
| OpenGL on Windows for x86_64 | For `gl` on `x86_64-windows-gnu`, `runner.py` writes the commands of `.toolchain/docs/runner.py.md`, *Windows*, for the archive `x64` and its digest. | The target `aarch64-windows-gnu`. |
| OpenGL on Windows for arm64 | For `gl` on `aarch64-windows-gnu`, `runner.py` writes the commands for the archive `arm64` and its digest. | The target `x86_64-windows-gnu`. |
| no command on macOS | For the 3 needs on `aarch64-macos`, `runner.py` writes nothing. | The target `aarch64-linux-gnu`. |
| a need that is not a need | The project needs `sound`: `[ci] needs: sound is not a need: display gl vulkan`. | The project needs `display`. |
| a target that runs on no machine | `--target nowhere`: `no machine runs the target nowhere`. | The target `x86_64-linux-gnu`. |

The workflows run the commands for real: the projects that state needs prove them on each runner.
