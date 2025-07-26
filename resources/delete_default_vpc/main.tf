provider "aws" {
  region = "us-east-1"
}

module "delete_default_vpc" {
  source      = "../../modules/delete_default_vpc"
  script_path = "${path.root}/delete_default_vpc.py"
}
