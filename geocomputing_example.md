# Geocomputing Example

When installing Python packages into a VCE using the container builder, Pyhton package wheels are build in the build step and then copied over into the deployment container, from which the packages are then installed during the deploy stage.

Several geocomputing packages have dependencies on operating system packages when building the wheels during the build stage, and when using the package in a deployed container.

When using such packages, we need to ensure that operating system packages are made available at each appropriate stage.

Foe example, the `fiona` package for reading and writing GIS file formats has a requirment on the `GDAL` operating system package, as well as GDAL related developer components.

```yaml
packages:
  apt:
    build:
      - gdal-bin
      - libgdal-dev
    deploy:
      - gdal-bin
      - libgdal-dev
  pip:
    user:
      - fiona
      - geopandas
      - Shapely
      - geopy
      - folium
      - descartes
```
