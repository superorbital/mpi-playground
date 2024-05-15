# mpi-playground

MPI and HPC examples that are companions to the SuperOrbital blog post about Slurm.

## Basic Setup

- Each folder in the _containers_ directory should map to a single container.
- The folder name will be used as the container name.
- Each container should be buildable on `arm64` and `amd64` at a minimum.
- Each folder should have a `metadata.yaml` file which can be used for various CI/CD purposes.
