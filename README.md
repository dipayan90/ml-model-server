# ml-model-server

This project provides you a pre-built **REST** server to score your machine learning models. 

## Features

* Score models by just providing configurations. 
* Error handling and standard logging inbuilt. 
* Configurable **Base Path** of the API.
* Comes bootstrapped with **CORS** support for cross domain access.
* Documentation is inbuilt in the form of **SWAGGER** docs.
* Supports following python model serialization formats:
    - PMML
    - Pickle ( Assumes that a `predict` function exists )
    - Simple lookup.
    
## Installation

```bash
pip install ml-model-server[all]
``` 

The above command installs all dependencies. However if you want a smaller footprint, you can select packages you want to install:

|  Functionality | Command  |
|---------|----------------------------------------|
|  PMML   | `pip install ml-model-server[pmml]`    |
|  Pickle | `pip install ml-model-server[pickle]`  |
|  All    | `pip install ml-model-server[all]`     |