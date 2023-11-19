## Quick EC2 Instance Setup for Ansible Testing

## This script rapidly deploys a specified number of EC2 instances for testing various 
## Ansible playbooks. It takes an image from AWS and assigns the specified key pair to 
## the instances for access. After running `terraform apply`, it outputs the public IPs 
## of the instances along with the SSH command for access.

provider "aws" {
  region = var.region
}

## Dynamic security groups. Since we're using it for an Ansible test env,
## we're allowing SSH traffic in, and all Web traffic out.

resource "aws_security_group" "webtraffic_and_ssh" {
  name        = "Security group for Ansible access"
  description = "Allow SSH and outbound traffic for Ansible"

  dynamic "ingress" {
    for_each = var.allowed_ingress_ports
    content {
      from_port   = ingress.key
      to_port     = ingress.key
      protocol    = "tcp"
      cidr_blocks = [var.ansible_ip]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Launch 5 EC2 instances using the same AWS Key Pair. Associate them with the
# specified security group allowing SSH traffic in and all Web traffic out.
resource "aws_instance" "ansible_test_instance" {
  count         = var.instance_number
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_pair_name

  vpc_security_group_ids = [aws_security_group.webtraffic_and_ssh.id]
}

## Output the public IPs of the created instances for easy transfer to
## Ansible inventory lists.
output "public_ips" {
  value = aws_instance.ansible_test_instance[*].public_ip
}

## Output SSH instructions for each instance using a single private key for easy
## access to the individual hosts.
output "ssh_instructions" {
  value = join("\n", [for instance in aws_instance.ansible_test_instance : 
    "Instance: ssh -i ~/.ssh/${var.key_pair_name}.pem ec2-user@${instance.public_ip}"])
}