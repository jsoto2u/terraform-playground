## Quick EC2 Instance Setup for Ansible Testing

## This script rapidly deploys 5 EC2 instances for testing various Ansible playbooks. 
## It takes an image from AWS (variable set in the `.tfvars` file) and assigns the specified
## key pair to the instances for access. After running `terraform apply`, it outputs the 
## public IPs of the instances along with the SSH command for access.

provider "aws" {
  region = var.region
}

variable "allowed_ingress_ports" {
  type    = set(number)
  default = [22, 80, 443]
}

variable "allowed_egress_ports" {
  type    = set(number)
  default = [80, 443, 25, 3306, 53, 8080]
}

## Dynamic security group blocks. It's using an iterator to cycle through
## the ports we labeled in our allowed_ingress_ports/allowed_egress_ports variables.
resource "aws_security_group" "webtrafficnssh" {
  name = "Allow HTTPS and SSH"

  dynamic "ingress" {
    iterator = port
    for_each = var.allowed_ingress_ports
    content {
      from_port   = port.value
      to_port     = port.value
      protocol    = "TCP"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  dynamic "egress" {
    iterator = port
    for_each = var.allowed_egress_ports
    content {
      from_port   = port.value
      to_port     = port.value
      protocol    = "TCP"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
}

# Launch 5 EC2 instances using the same AWS Key Pair
resource "aws_instance" "example_instance" {
  count         = var.instance_number
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_pair_name
}

# Output the public IPs of the created instances
output "public_ips" {
  value = aws_instance.example_instance[*].public_ip
}

# Output a message with SSH connection information
output "ssh_instructions" {
  value = <<-EOT
    To SSH into the instances, use the following command:
    ssh -i ~/.ssh/id_rsa ec2-user@${aws_instance.example_instance[0].public_ip}
  EOT
}