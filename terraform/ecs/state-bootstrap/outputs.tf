output "state_bucket_name" {
  description = "Name of the S3 bucket used for Terraform state"
  value       = aws_s3_bucket.terraform_state.bucket
}

output "lock_table_name" {
  description = "Name of the DynamoDB lock table"
  value       = aws_dynamodb_table.terraform_lock.name
}

output "backend_config_example" {
  description = "Example backend.hcl content for terraform/ecs"
  value = <<EOT
bucket         = "${aws_s3_bucket.terraform_state.bucket}"
key            = "genorax-ai-backend/ecs/dev/terraform.tfstate"
region         = "${var.aws_region}"
dynamodb_table = "${aws_dynamodb_table.terraform_lock.name}"
encrypt        = true
EOT
}
