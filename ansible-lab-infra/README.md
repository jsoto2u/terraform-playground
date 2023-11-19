# Terraform Ansible Test Environment

This Terraform project deploys EC2 instances for testing Ansible playbooks. It allows quick setup and configuration.

## Prerequisites
- AWS credentials configured
- Terraform installed

## Usage
1. Clone the repository.
2. Update `terraform.tfvars` with your desired configuration.
3. Run `terraform init` and `terraform apply` to deploy the infrastructure.
4. Access the instances using the provided SSH instructions.

## Configuration

### Variables
- `region`: Your desired AWS region.
- `ami_id`: The ID of the Amazon Machine Image (AMI) to use.
- ...

### Security Group
The security group allows inbound SSH traffic and outbound traffic for Ansible.
This is adjustable based on your application's needs. This script allows all
outbound traffic as an example, and is NOT recommended for production env as is.

### Output
The `public_ips` output displays the public IPs of the created instances.

### SSH Instructions
To SSH into the instances, use the provided SSH command.

## Examples
- Customizing the number of instances.
- Customize type of OS needed for instances.
