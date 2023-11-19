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
  description = "The name of your AWS Key Pair."
}