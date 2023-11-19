## Getting familiar with Terraform syntax and tagging. This launches a VPC
## named TerraformVPC in the GUI.

# Provider block specifies the AWS region
provider "aws" {
    region = "us-east-2" # Replace with your desired AWS Region
}

# Resource block defines the AWS VPC
resource "aws_vpc" "namedvpc" {
    cidr_block = "192.168.0.0/24"
    tags = {
        Name = "TerraformVPC"
    }
}

# Output block to display the VPC ID
output "vpc_id" {
  value = aws_vpc.namedvpc.id
}