## Quick EC2 Instance Setup for Ansible Testing
##
## This script rapidly deploys 5 EC2 instances for testing various Ansible playbooks. 
## It uses a catalog RHEL image from AWS and relies on a local machine for execution.
## It also outputs the public IPs of the instance after you run terraform apply.
##
## To be added:
## - Dynamic block security groups
## - Variables for key-pairs for easy adjustments

provider "aws" {
  region = "us-east-2"  # Replace with your desired AWS region
}

# Create an AWS Key Pair using the public key from your local env
resource "aws_key_pair" "example_key_pair" {
  key_name   = "example-key-pair"
  public_key = file("~/.ssh/example-key-pair.pub")  # Replace with the path to your public key
}

# Launch 5 EC2 instances using the same AWS Key Pair
resource "aws_instance" "example_instance" {
  count         = 5
  ami           = "ami-0931978297f275f71"  # Replace with your desired AMI ID
  instance_type = "t2.micro"                # Replace with your desired instance type
  key_name      = aws_key_pair.example_key_pair.key_name
}

# Output the public IPs of the created instances
output "public_ips" {
  value = aws_instance.example_instance[*].public_ip
}