############################################################
# Terraform AWS Basic Example
#
# This configuration demonstrates how to provision basic AWS
# resources using Terraform, including:
#   - VPC
#   - Subnet
#   - Security Group
#   - EC2 Instance
#   - S3 Bucket
#
# Variables are defined in variables.tf and can be customized.
# Outputs are defined in outputs.tf.
############################################################

#-----------------------------------------------------------
# Provider Configuration
#-----------------------------------------------------------
# The AWS provider is required to interact with AWS services.
# The region is set via a variable (see variables.tf).
provider "aws" {
  region = var.region
}

#-----------------------------------------------------------
# VPC (Virtual Private Cloud)
#-----------------------------------------------------------
# A VPC is a logically isolated section of the AWS cloud where
# you can launch AWS resources in a virtual network.
# The CIDR block is configurable via the vpc_cidr variable.
resource "aws_vpc" "example" {
  cidr_block = var.vpc_cidr
}

#-----------------------------------------------------------
# Subnet
#-----------------------------------------------------------
# A subnet is a range of IP addresses in your VPC.
# This subnet is created within the VPC above, using the
# subnet_cidr variable for its address range.
resource "aws_subnet" "example" {
  vpc_id     = aws_vpc.example.id
  cidr_block = var.subnet_cidr
}

#-----------------------------------------------------------
# Security Group
#-----------------------------------------------------------
# Security groups act as virtual firewalls for your EC2 instances
# to control inbound and outbound traffic.
# This example allows SSH (port 22) and HTTP (port 80) from anywhere.
resource "aws_security_group" "example" {
  name        = "example-sg"
  description = "Allow SSH and HTTP"
  vpc_id      = aws_vpc.example.id

  # Allow SSH from anywhere
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow HTTP from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

#-----------------------------------------------------------
# EC2 Instance
#-----------------------------------------------------------
# This resource launches a t2.micro EC2 instance (default) in the
# subnet and VPC created above, using the security group for access.
# The AMI is set to Amazon Linux 2 for us-east-1. Change as needed.
resource "aws_instance" "example" {
  ami           = "ami-0c94855ba95c71c99" # Amazon Linux 2 AMI (us-east-1)
  instance_type = var.instance_type
  subnet_id     = aws_subnet.example.id
  vpc_security_group_ids = [aws_security_group.example.id]

  tags = {
    Name = "ExampleInstance"
  }
}

#-----------------------------------------------------------
# S3 Bucket
#-----------------------------------------------------------
# This resource creates a private S3 bucket with a unique name.
# The random_id resource is used to ensure the bucket name is unique.
resource "aws_s3_bucket" "example" {
  bucket = "example-terraform-bucket-${random_id.bucket_id.hex}"
  acl    = "private"
}

#-----------------------------------------------------------
# Random ID
#-----------------------------------------------------------
# Generates a random ID for use in the S3 bucket name to avoid naming conflicts.
resource "random_id" "bucket_id" {
  byte_length = 4
}

#-----------------------------------------------------------
# Elastic Load Balancer (ELB)
#-----------------------------------------------------------
# This resource creates a classic Elastic Load Balancer (ELB) in the VPC.
# It listens on HTTP (port 80) and forwards traffic to the EC2 instance(s).
# The ELB is associated with the subnet and security group created above.
resource "aws_elb" "example" {
  name               = "example-elb"
  subnets            = [aws_subnet.example.id]
  security_groups    = [aws_security_group.example.id]

  listener {
    instance_port     = 80
    instance_protocol = "http"
    lb_port           = 80
    lb_protocol       = "http"
  }

  health_check {
    target              = "HTTP:80/"
    interval            = 30
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
  }

  instances = [aws_instance.example.id]

  tags = {
    Name = "ExampleELB"
  }
} 