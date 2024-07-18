# `container-builder` Built Container Lifecycle

When configuring `container-builder`, it helps to have an overview of the lifecyle of the process:

- `build` stage: a temporary container is created that can be used to build artefacts that can be then copied into a deployed container; build scripts are identified via `commands` in `scripts` blocks with a `stage: build` setting; rtefects are copied over using `output_blocks.deploy` statements.

*For an example of a `build` stage process, see [web app example](./webapp_example.html).*

- `deploy` phase: in this phase, the deployed container image is built;

- `startup` phase: when a deployed container is started, we have an opportunity to run startup scripts and start `services`.