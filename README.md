# An example of AWS Glue Crawler

This repository was made to investigate the behaviour of AWS Glue Crawler.
AWS Glue Crawler is not well documented and it has mysterious behaviour.

Although for a simple usecase,
such that all of the JSON files in an S3 bucket have the same structure,
Glue Crawler produces only one table schema,
when the JSON files don't have the same structure,
it will produce more than one table schemas.

## Datasets

This repository has five datasets to be given to AWS Glue Crawler:

- json-data-example
- flat-and-one-common-key
- disjoint-keys
- non-hive-disjoint-keys
- overlapping-keys

These datasets are defined in *glue_crawler_example/data.py*.

The dataset `json-data-example` have only one JSON file.
Glue Crawler generates only one table schema.

The dataset `flat-and-one-common-key` have JSON files placed in the root.
The JSON files have the common key `id`
but each file has one additional key unique for the file.
Glue Crawler generates tables for each JSON file.

The dataset `disjoint-keys` have JSON files with a key unique for each file.
The prefix of the files are in the Hive format.
Glue Crawler generates many tables.

The dataset `non-hive-disjoint-keys` is a version of the dataset `disjoint-keys`,
where the prefix isn't in the Hive format.
Glue Crawler generates many tables.

The dataset `overlapping-keys` have JSON files with the following keys:

- `id`
- `description`
- `q0` or `q1`

Glue Crawler generates only one table for this dataset.

## How to deploy

First, you create a virtualenv of Python:

```console
$ python3 -m venv .venv
```

Second, you activate your virtualenv after the initialization:

```console
$ source .venv/bin/activate
```

Third, you install the dependencies:

```console
$ pip install -r requirements.txt
```

Then you can deploy the stack:

```console
$ cdk deploy
```

## How to run the crawlers

After the deployment, you can list the crawlers by the following command:

```console
$ inv list-crawlers
```

Then you run the crawlers and wait for their completion:

```console
$ inv start-crawlers
```

The command below show the generated table schemas:

```console
$ inv show-tables
```

You would like to clean up the databases on AWS Glue:

```console
$ inv delete-databases
```
