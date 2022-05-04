# Salesforce Ingestion for Data Lakes

A Data Lake ingestion connector for the Salesforce APIs using Amazon Appflow, a fully managed service that enables you to securely transfer data between AWS services and some SaaS applications.

The Salesforce Ingestion component is meant for extracting all kind of resources in the Salesforce environment after the Oauth connection has been set; it allows you to define what resources you want to extract.
The component is also meant to be used with two buckets (one to receive data, the other to organize it) though it can be used on the same bucket by specifying the source and destination buckets with the same name (but prefixes must be different).

The infrastructure is described (IaC) and deployed with Serverless Framework (https://www.serverless.com/framework/). The entry point is `serverless.yml`.

The infrastructure has been developed on the AWS Cloud Platform.

## Getting Started

### Requirements

- Node.js and NPM: https://nodejs.org/en/download/
- Serverless Framework: https://www.serverless.com/framework/docs/getting-started/

#### For local development only

- Python: https://www.python.org/downloads/
- virtualenv: https://virtualenv.pypa.io/en/latest/installation.html

### Environments setup

The `env/` folder contains the environment configuration files, one for each of your AWS environments.

The name of the files corresponds to the environment names. For example: copy `example-enviroment.yml` to `dev.yml` for a development environment.

### Development environment setup

1. Create virtualenv: `virtualenv -p python3 venv`
2. Activate virtualenv: `source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`

## Deployment instructions

- Double check variables inside `env/{stage-name}.yml` (where `{stage-name}` value can be `prod`, `dev`, ...), starting from `example-enviroment.yml`

- Manually create the AWSWrangler Lambda Layer if not present (see https://github.com/lochness-labs/pantolambda/tree/main/awswrangler_layer)

- Install required Serverless plugins:

    - serverless-step-functions
    - serverless-python-requirements

- Manually create the Salesforce OAuth connection (see https://docs.aws.amazon.com/appflow/latest/userguide/salesforce.html)

    - Set the name of `APPFLOW_CONNECTION_NAME` inside `/env/{stage-name}.yml`
    - This name will be used on `ConnectorProfileName` inside `/serverless-parts/resources.yml`
    - This is a one-time task if you keep 

- Attach this policy to the source bucket:

```json
{
    "Version": "2008-10-17",
    "Statement": [
        {
            "Sid": "AllowAppFlowDestinationActions",
            "Effect": "Allow",
            "Principal": {
                "Service": "appflow.amazonaws.com"
            },
            "Action": [
                "s3:PutObject",
                "s3:AbortMultipartUpload",
                "s3:ListMultipartUploadParts",
                "s3:ListBucketMultipartUploads",
                "s3:GetBucketAcl",
                "s3:PutObjectAcl"
            ],
            "Resource": [
                "arn:aws:s3:::<SOURCE-BUCKET-NAME>",
                "arn:aws:s3:::<SOURCE-BUCKET-NAME>/*"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:SourceAccount": "<ACCOUNT_ID>"
                }
            }
        }
    ]
}
```

- Copy the `env/example-appflow-resources.yml` and rename it with the environment name `env/{stage-name}-appflow-resources.yml` (for example: `env/dev-appflow-resources.yml`)

- Add resources to `serverless-parts/resources/` following the examples inside the `OnDemandExample` folder.
    - Every yml file inside the subfolder represents a single Salesforce entity and a single Appflow Flow.
    - Each flow name must be alphanumeric (is. `SalesforceCase` is ok, `Salesforce_Case` is wrong)
    - Scheduled flows must be manually activated (after the deploy they are in a Draft state). Go to `Amazon AppFlow` > `Flows` > yourFlow and click on `Activate`
    - Flows with the same name but different mode (OnDemand, Scheduled) can't co-exists and will be replaced (for example if you first deploy an Ondeman flow and after a scheduled one)

- Add the resources paths to `env/dev-appflow-resources.yml`

- Deploy with serverless framework


## Contributing

Feel free to contribute! Create an issue and submit PRs (pull requests) in the repository. Contributing to this project assumes a certain level of familiarity with AWS, the Python language and concepts such as virtualenvs, pip, modules, etc.

Try to keep commits inside the rules of https://www.conventionalcommits.org/. The `sailr.json` file is used for configuration of the commit hook, as per: https://github.com/craicoverflow/sailr.

## License

This project is licensed under the **Apache License 2.0**.

See [LICENSE](LICENSE) for more information.

## Acknowledgements

Many thanks to the mantainers of the open source libraries used in this project:

- Serverless Framework: https://github.com/serverless/serverless
- Pandas: https://github.com/pandas-dev/pandas
- AWS Data Wrangler: https://github.com/awslabs/aws-data-wrangler
- Boto3 (AWS SDK for Python): https://github.com/boto/boto3
- Sailr (conventional commits git hooke): https://github.com/craicoverflow/sailr/

### Serverless plugins

These are the Serverless plugin used on this project:

- serverless-step-functions: https://github.com/serverless-operations/serverless-step-functions

Contact us if we missed an acknowledgement to your library.

---

This is a project created by [Linkalab](https://linkalab.it) and [Talent Garden](https://talentgarden.org).