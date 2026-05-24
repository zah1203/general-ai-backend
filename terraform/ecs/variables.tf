variable "aws_region" {
  description = "AWS region for ECS infrastructure"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "genorax-ai-backend"
}

variable "environment" {
  description = "Environment name used for resource naming"
  type        = string
  default     = "dev"
}

variable "allowed_http_cidr" {
  description = "CIDR allowed to access the public ALB over HTTP"
  type        = string
  default     = "0.0.0.0/0"
}

variable "openai_model" {
  description = "OPENAI_MODEL environment variable for the backend container"
  type        = string
  default     = "gpt-4o-mini"
}

variable "openai_api_key_secret_arn" {
  description = "Secrets Manager secret ARN containing OPENAI_API_KEY. Leave empty to skip secret injection."
  type        = string
  default     = ""
}

variable "image_tag" {
  description = "ECR image tag to deploy"
  type        = string
  default     = "latest"
}

variable "desired_count" {
  description = "Desired ECS service task count"
  type        = number
  default     = 1
}

variable "task_cpu" {
  description = "Fargate task CPU units"
  type        = string
  default     = "2048"
}

variable "task_memory" {
  description = "Fargate task memory in MiB"
  type        = string
  default     = "4096"
}

variable "task_ephemeral_storage_gib" {
  description = "Fargate task ephemeral storage size (GiB)"
  type        = number
  default     = 50
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 14
}
