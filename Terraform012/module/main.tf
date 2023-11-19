provider "aws" {
    region = "us-east-2"
}

module "ec2" {
    source = "./ec2"
    aws_region = "us-east-1"
    for_each = toset(["dev", "test", "prod"])
}