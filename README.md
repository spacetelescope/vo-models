# vo-models

`vo-models` an open-source project to provide Python models and OpenAPI specifications for [IVOA](https://www.ivoa.net/) service protocols.

The project is designed to be used by IVOA members, service implementors, and developers to help facilitate the development of IVOA-compliant services and clients.

## Features

- **Pydantic-xml Models:** The project includes Python models for IVOA protocols, using [pydantic-xml](https://github.com/dapper91/pydantic-xml). Based on [Pydantic](https://docs.pydantic.dev/latest/), these models describe transactions for an IVOA protocol, such as UWS, and feature automatic validation, parsing and serialization of XML data for use with Python clients and web frameworks.

- **OpenAPI Specifications:** The project includes OpenAPI definitions for IVOA protocols. The use of OpenAPI provides a standardized and machine-readable way to describe the IVOA protocols. OpenAPI specifications offer benefits such as automatic documentation generation, and automatic client and server code generation.

- **Expandability:** The project is designed with future expansion in mind. Plans include extending the schema and models to cover other IVOA standards.

## Protocols

The following IVOA protocols are currently supported / under development:

- **UWS (Universal Worker Service) version 1.1:**
  - Active development:
    - OpenAPI Models
    - Pydantic-XML Models
  - Planned:
    - OpenAPI Service Definition

## Installation

### Conda

To install the project using Conda, you can use the provided environment file:

```bash
git clone https://github.com/spacetelescope/vo-models.git
cd vo-models
conda env create -f environment.yml
conda activate vo-models
pip install -r requirements.txt
pip install .
```

For active development, install the project in development mode:

```bash
pip install -e .
```

### Pip
If you prefer to use pip, you can install the project directly from the repository:

```bash
pip install -r requirements.txt
pip install .
```

## Usage
### OpenAPI Schema

OpenAPI schema files representing IVOA protocol transactions can be found in the `vo/models/openapi` directory.

For each protocol, two files are provided: a `components.yml` file containing the JSON/XML schema definitions for request / response transactions, and a file named after the protocol (e.g. `uws.yml`) containing the OpenAPI specification for the protocol. The schema models, and the OpenAPI specification, are viewable in the [Swagger Editor](https://editor.swagger.io/).

*Note: Currently, the OpenAPI API definition files are not guaranteed to be complete. They are provided as a starting point for future development, and an example of how the schema definitions can be used.*

### Pydantic-XML Models

Python models using [pydantic-xml](https://github.com/dapper91/pydantic-xml), a library based on [Pydantic](https://docs.pydantic.dev/latest/), are provided in the `vo/models/xml` directory.

These models can be used to parse and validate XML data into Python objects, as well as serialize Python objects into XML data. These models can be used with any Python web framework, but are particularly useful when used libraries that leverage the power of Pydantic, such as [FastAPI](https://fastapi.tiangolo.com/).

### Contributing

Contributions to the project are more than welcome. Collaboration and discussion with other IVOA members, service implementors, and developers is what started this project, and is what makes the IVOA great.

If you are interested in contributing, whether that be adding a new protocol, improving the schema, fixing a bug or even a typo, please feel free to open an issue or pull request.


### License

This project is licensed under the [MIT License](LICENSE).