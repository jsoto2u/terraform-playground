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
- `region`: Your preferred AWS region for deploying resources.
- `ami_id`: The unique identifier of the Amazon Machine Image (AMI) to be used for EC2 instances.
- `instance_type`: The type of EC2 instance to launch, specifying the compute and memory capacity.
- `instance_number`: The number of EC2 instances to be deployed.
- `key_pair_name`: The name of the AWS key pair to associate with the EC2 instances for SSH access.
- `ansible_ip`: The IP address or range from which Ansible will connect to the EC2 instances.
- `allowed_ingress_ports`: A list of ports to allow incoming traffic to the EC2 instances.

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
