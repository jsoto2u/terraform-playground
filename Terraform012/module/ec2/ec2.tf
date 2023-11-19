variable "aws_region" {
  type    = string
  default = "us-east-1" # or set an appropriate default
}

resource "aws_instance" "ec2" {
    ami = "ami-0931978297f275f71"
    instance_type = "t2.micro"
}