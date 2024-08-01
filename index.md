# OU Container Builder ContainerConfig.yaml Generator

Increasing numbers of OU modules deploy a hosted virtual computing environment (VCE) to students using containers built using the OU `container-builder` tool ([documentation](https://docs.ocl.open.ac.uk/container-builder/v3/)).

Deployed environments provide students with a web based user environment such as Jupyter Lab, Jupyter notebooks, or VS Code, as well as access to arbitrary other web applications, along with persistent storage on OU managed servers.

Container images built using `container-builder` can also be run locally by students on their own computers, in development environments such as GitHub Codespaces, or on third party remote servers. Locally run VCEs allow students to work with the VCE in an offline setting.

This document contains unofficial, additional guidance on building configuration files for use with `container-builder`. Many of the examples were originally developed in the context of the Open University module *TM351 Data Management and Analysis*, which has been using virtual environments and Jupyter user interfaces since 2016. The TM351 VCE was originally distributed as a VirtualBox managed virtual machine, before migrating to Docker containers, and, more recently, `container-builder` built containers.

*For an overview of the TM351 VCE Jupyter user environment, see [OU TM351 JupyterLab Customisation](https://innovationoutside.github.io/ou-tm351-jl-extensions/overview.html).*

This document reviews the lifecycle of containers built using `container-builder`, and provides examples of complete and partial `container-builder` configurations for a variety of use cases:

- [container lifecycle](./container_lifecycle.html): overview of the lifecycle of a `container-builder` built container;
- [container-builder configuration file generator](./generator.html): HTML form based UI for generating and editing `container-builder` configuration files;
- [`web_app` example](./webapp_example.md): walkthrough of installing and configuring a simple web app (Open Refine) using `container-builder`;
- [customised Jupyter UI example](./customised_jupyter_ui_example.md): example configuration for installing various JupyterLab extensions to improve accessibility and user experience of teaching and learning materials;
- [geocomputing example](./geocomputing_example.md): example of build requirements when installing geocomputing Python packages with operating system package dependencies;
- [database service example](database_service_example.md): example of installing a database and running a database service;
- [seeded database example](./seeded_database_example.md): example of seeding a database with data in a deployed environment;
- [persisted database example](./persisted_database_example.md): example of how to persist database data directories in a VCE persistent file store or shared volume;
- experimental validator for container builder v3 YAML configuration files [here](https://gist.github.com/psychemedia/cd2425975ffc1d87bf8cb3c4df264fca).

*If you have other particular use cases in mind, or examples you would like to share via these pages, please email `tony.hirst@open.ac.uk`*.
