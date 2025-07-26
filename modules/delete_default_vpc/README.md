# VPC Cleanup Module & Resource Wrapper

**Purpose:**  
This repository contains a quick-and-dirty Terraform module and resource wrapper to delete the AWS default VPC (and all of its associated resources) in the `us-east-1` region. It invokes a small Python script via `null_resource` + `local-exec` during `terraform apply`.

---

## Table of Contents

- [VPC Cleanup Module \& Resource Wrapper](#vpc-cleanup-module--resource-wrapper)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Repository Layout](#repository-layout)
  - [Getting Started](#getting-started)
    - [Usage](#usage)
  - [How It Works](#how-it-works)
  - [Terraform Workflow](#terraform-workflow)
  - [Module Details](#module-details)
  - [Cleanup \& Re-run](#cleanup--re-run)
  - [Troubleshooting](#troubleshooting)
  - [Contributing](#contributing)
    - [License](#license)

---

## Prerequisites

- **AWS CLI** configured with credentials having permissions to delete VPCs & related resources in `us-east-1`.  
- **Python 3.7+**  
- **boto3** Python package (`pip install boto3`)  
- **Terraform v1.0+**  
- **Git** (for cloning and pushing changes)

## Repository Layout

your-repo/
├── delete_default_vpc.py            # Python script to delete default VPC
├── modules/
│   └── delete_default_vpc/         # Reusable Terraform module
│       ├── variables.tf
│       ├── main.tf
│       ├── outputs.tf
│       └── README.md               # Module documentation
└── resources/
    └── delete_default_vpc/         # Resource folder for Terraform usage
        └── main.tf


## Getting Started

1. **Clone this repository**

   ```bash
   git clone git@github.com:your-org/vpc-cleanup-module.git
   cd vpc-cleanup-module

2. **Review the Python script (delete_default_vpc.py) to ensure it matches your environment and delete criteria.**

3. Verify AWS credentials

```aws sts get-caller-identity --output table```

Make sure the IAM identity has permissions to delete VPCs, subnets, IGWs, SGs, Route Tables, NACLs, etc.

### Usage

All Terraform commands are run under the resource wrapper folder.

- cd resources/delete_default_vpc
- terraform init
- terraform plan
- terraform apply

- **terraform init:** Downloads provider plugins and initializes modules.

- **terraform plan:** Shows the intended actions (invocation of the Python script).

- **terraform apply:** Executes the deletion script locally via `null_resource + local-exec.`

## How It Works

1. Terraform reads resources/delete_default_vpc/main.tf and sees the delete_default_vpc module.

2. The module uses data.local_file to compute the MD5 checksum of delete_default_vpc.py.

3. If the checksum changes (or on first run), Terraform runs the Python script via local-exec.

4. The Python script uses boto3 to locate the default VPC and delete:

- Internet Gateways

- Subnets

- Non-default Security Groups

- Non-main Route Tables

- Non-default Network ACLs

- Finally, the VPC itself

## Terraform Workflow

1. Change detection: The module’s null_resource has a trigger on the script’s MD5 hash.

2. Execution: On apply, Terraform shells out:

`python3 /path/to/delete_default_vpc.py`

3. Output: After completion, you’ll see the Python script’s console logs and Terraform outputs the last_run_md5.

## Module Details

- Module path: modules/delete_default_vpc

- Inputs:

- **script_path (string):** Path to the Python deletion script.

- Outputs:

last_run_md5 (string): MD5 checksum of delete_default_vpc.py from last run.

For full module documentation, see modules/delete_default_vpc/README.md.

## Cleanup & Re-run

- If you update delete_default_vpc.py, Terraform will detect the MD5 change and re-run the deletion on the next apply.

- To force a re-run without changing the script, you can taint the resource:

`terraform taint module.delete_default_vpc.null_resource.delete_default_vpc`
`terraform apply`

## Troubleshooting

- No default VPC found: The script will print No default VPC found. if it’s already removed.

- Permission errors: Ensure your AWS credentials allow EC2 actions: Describe*, `Delete*`, `Detach*`.

- Python exceptions: Run the script manually to inspect errors:

`python3 delete_default_vpc.py`

## Contributing

1. Fork the repository

2. Create a feature branch (git checkout -b feature/xyz)

3. Commit your changes (git commit -m "Add XYZ feature")

4. Push to your branch (git push origin feature/xyz)

5. Open a Pull Request

### License

This project is licensed under the MIT License. See LICENSE for details.