variable "ami_id" {
  description = "The ID of the Amazon Machine Image (AMI) to use for EC2 instances."
}

variable "instance_type" {
  description = "The type of instance you want to build."
}

variable "region" {
  description = "Your desired AWS region."
}

variable "instance_number" {
  description = "The number of these instances you would like to launch."
}

variable "key_pair_name" {
  description = "The name of the keypair you'll be using in AWS."
}

variable "ansible_ip" {
  description = "The IP address or range from which Ansible will connect."
}

variable "allowed_ingress_ports" {
  type    = set(number)
  default = [22, 80, 443]
}