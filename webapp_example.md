# Adding a Web App — Worked Example

[OpenRefine](https://openrefine.org/) is Java application with a browser based user-interface that provides a range of tools for cleaning tabular datasets. OpenRefine has been provided as part of a *TM351 Data Management and Analysis* virtual computing environment since 2016.

OpenRefine can be added to a container-builder environment and exposed via shortcuts in a JupyterLab or Jupyter notebook environment by making defined it as a custom *web app*.

As well as the web app specification, the application itself needs to be downloaded and installed during the `build` stage, and copied over to the deployed container via an `output block`. (Documentation for recommended output block weight ranges is available via the [`container-builder` documentation](https://docs.ocl.open.ac.uk/container-builder/v3/developer/output_block_weights.html).) Operating system packages required to run the application need to be installed in the `deploy` stage. Several utility environment path variables are also set.

```yaml
# The Open Refine application is pre-built and only needs Java to be available in the deploy stage.
# Required Java packages are thus installed as apt.deploy packages.
# Any packages specifically required in the build stage should be install as apt.build packages.
# wget is required in the build stage, but it is installed by default.
packages:
  apt:
    deploy:
      - openjdk-17-jre 
      - openjdk-17-jre-headless

# The paths are referenced by the application, but we can also use them to specify
# the version of the application downloaded, and its target path.
environment:
  - name: OPENREFINE_VERSION
    value: 3.8.0
  - name: OPENREFINE_PATH
    value: "/var/openrefine"

scripts:
    # The pre-built Open Refine application is downloaded and unarchived during a build step.
    # It would also be possible to build the application from source in this step, which might
    # also require additional apt.build packages to be installed.
  - stage: build
    commands:
      # Download the archived application
      - wget -q -O openrefine-\${OPENREFINE_VERSION}.tar.gz https://github.com/OpenRefine/OpenRefine/releases/download/\${OPENREFINE_VERSION}/openrefine-linux-\${OPENREFINE_VERSION}.tar.gz
      # Unarchive it
      - tar xzf openrefine-\${OPENREFINE_VERSION}.tar.gz
      # Copy it to a known path
      - mv openrefine-\${OPENREFINE_VERSION} $OPENREFINE_PATH

output_blocks:
  deploy:
    # The COPY instruction copies from the "build" container to the "deploy" container.
    # We copy the OpenRefine application from the original download path in the build stage
    # to the target path we require in the deployed containerd.
    # Could we also use the environment variable here?
    - block: COPY --from=base /var/openrefine /var/openrefine
      # We use a weight in the range: 2001 - 3000 Recommended: User blocks
      # The weight is reminiscent of the OpenRefine default port (3333).
      # Docs on weight ranges: https://docs.ocl.open.ac.uk/container-builder/v3/developer/output_block_weights.html
      weight: 2333

content:
  # This requires that we have a copy of the SVG icon available at the specified source path
  # We could alternatively download the icon in a build step
  # and copy it over to the deploy container via an output block.
  - source: ./icons/openrefine.svg
    target: /var/ou/icons/openrefine.svg
    overwrite: always
```

With the application installed, we now need to provide a `web_app` specification which defines how to call it. The specification requires the `path` that the application should be published to when proxied in the VCE and the `command` required to call it. Additional metadata defines a `timeout` period that is used to raise an error if an application is slow to start, whether the application should be loaded in a new tab, and a description of the `name` and the path to any icon (`icon_path`) used to refer to the application when launching the application.

Web apps are 

```yaml
web_apps:
  - path: openrefine
    options:
      command:
        - /var/openrefine/refine
        - -i
        - "127.0.0.1"
        - -p
        - "{port}"
        - -d
        - /home/ou/TM351-24J/openrefine
        - -H
        - "*"
        - -x
        - refine.display.new.version.notice=false
      timeout: 120
      new_browser_tab: true
      launcher_entry:
        title: OpenRefine
        icon_path: /var/ou/icons/openrefine.svg
```

