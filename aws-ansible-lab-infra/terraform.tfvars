## EC2 instance configuration variables.

region = "us-east-2"
ami_id = "ami-0931978297f275f71" # This is a RHEL image from the AWS AMI Catalog.
instance_type = "t2.micro" # Build size.
instance_number = "5"
key_pair_name = "your-unique-key" # Specifies which private key these instances will use from AWS.
ansible_ip = "192.168.1.1/32" # Represents the specific IP address from which Ansible will connect to the EC2 instances
allowed_ingress_ports = [22, 80, 443]
