## EC2 instance configuration variables.

region = "us-east-2"
ami_id = "ami-0931978297f275f71"
instance_type = "t2.micro"
instance_number = "5"
key_pair_name = "project-terraform-key" # Specifies which private key these instances will use from AWS.
ansible_ip = "97.118.242.25/32" # Represents the IP address or range from which Ansible will connect to the EC2 instances
allowed_ingress_ports = [22, 80, 443]