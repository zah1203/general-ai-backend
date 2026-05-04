variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "genorax-ai-backend"
}

variable "environment" {
  description = "Environment name (e.g. dev, test)"
  type        = string
  default     = "dev"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Existing AWS EC2 key pair name for SSH access"
  type        = string
}

variable "allowed_ssh_cidr" {
  description = "CIDR block allowed to SSH to EC2 (port 22)"
  type        = string
}

variable "allowed_api_cidr" {
  description = "CIDR block allowed to access FastAPI on port 8000"
  type        = string
}

variable "github_repo_url" {
  description = "GitHub repo URL to clone and run on EC2"
  type        = string
}
