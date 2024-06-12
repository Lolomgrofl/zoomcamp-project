## Pre-requisites

Before getting started, please ensure that you have the following dependencies installed on your system:

- Docker: [Installation guide](https://docs.docker.com/get-docker/)
- Docker Compose: [Installation guide](https://docs.docker.com/compose/install/)
- Rye: [Installation guide](https://rye.astral.sh/)

## Getting Started

After the pre-requisites have been installed, you can follow the steps below to get the project up and running:

1. Environment setup - This command will create a virtual environment and install the required dependencies
```shell
    rye sync
```

2. Since everything is dockerized, you can start the project by running the following command:
```shell
    make build
```

3. Open your browser and go to http://localhost:8000/docs to see the app running & check the API documentation.

4. Running unit tests
```shell
    make test
```

## Visualization - outlier detection
can be found in the ```visualization.ipynb``` notebook. The notebook is self-explanatory and contains the code for the visualization of the outlier detection.

## Deployment
TBD
