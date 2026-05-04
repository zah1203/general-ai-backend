terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Fetch availability zones so we can deterministically pick one for the subnet.
data "aws_availability_zones" "available" {
  state = "available"
}

# Use the default VPC to keep this dev environment simple and easy to destroy.
data "aws_vpc" "default" {
  default = true
}

# Use the first default subnet in the default VPC for public EC2 placement.
resource "aws_default_subnet" "selected" {
  availability_zone = data.aws_availability_zones.available.names[0]
}

# Get the latest Amazon Linux 2023 AMI from AWS.
data "aws_ami" "amazon_linux_2023" {
  most_recent = true

  owners = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
}

# Security group for SSH and FastAPI access.
resource "aws_security_group" "backend" {
  name        = "${var.project_name}-${var.environment}-sg"
  description = "Security group for ${var.project_name} ${var.environment} backend"
  vpc_id      = data.aws_vpc.default.id

  # SSH access for admin/dev access.
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
  }

  # FastAPI app access.
  ingress {
    description = "FastAPI"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = [var.allowed_api_cidr]
  }

  # Allow all outbound traffic for package installs, git clone, and Docker image pulls/builds.
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-sg"
    Project     = var.project_name
    Environment = var.environment
  }
}

# IAM role assumed by EC2 instance.
resource "aws_iam_role" "ec2_role" {
  name = "${var.project_name}-${var.environment}-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name        = "${var.project_name}-${var.environment}-ec2-role"
    Project     = var.project_name
    Environment = var.environment
  }
}

# Attach SSM managed instance policy for Session Manager and basic instance management.
resource "aws_iam_role_policy_attachment" "ssm" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# Attach CloudWatch agent/server policy for future logs/metrics use.
resource "aws_iam_role_policy_attachment" "cloudwatch" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

# Instance profile to attach IAM role to EC2.
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${var.project_name}-${var.environment}-ec2-profile"
  role = aws_iam_role.ec2_role.name
}

# EC2 instance running the Genorax backend Docker container.
resource "aws_instance" "backend" {
  ami                         = data.aws_ami.amazon_linux_2023.id
  instance_type               = var.instance_type
  subnet_id                   = aws_default_subnet.selected.id
  vpc_security_group_ids      = [aws_security_group.backend.id]
  key_name                    = var.key_name
  iam_instance_profile        = aws_iam_instance_profile.ec2_profile.name
  associate_public_ip_address = true

  user_data = templatefile("${path.module}/user_data.sh.tpl", {
    github_repo_url = var.github_repo_url
  })

  tags = {
    Name        = "${var.project_name}-${var.environment}-ec2"
    Project     = var.project_name
    Environment = var.environment
  }
}
