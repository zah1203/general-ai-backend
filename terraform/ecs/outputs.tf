output "ecr_repository_url" {
  description = "ECR repository URL for backend image pushes"
  value       = aws_ecr_repository.backend.repository_url
}

output "alb_dns_name" {
  description = "Public DNS name for the application load balancer"
  value       = aws_lb.this.dns_name
}

output "health_url" {
  description = "Health endpoint URL"
  value       = "http://${aws_lb.this.dns_name}/health"
}

output "docs_url" {
  description = "Swagger docs endpoint URL"
  value       = "http://${aws_lb.this.dns_name}/docs"
}

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.this.name
}

output "ecs_service_name" {
  description = "ECS service name"
  value       = aws_ecs_service.backend.name
}

output "ecr_login_command" {
  description = "Command to authenticate Docker to ECR"
  value       = "aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin ${aws_ecr_repository.backend.repository_url}"
}

output "docker_build_command" {
  description = "Command to build backend image"
  value       = "docker build -t ${var.project_name}:${var.image_tag} ../../genorax-ai-backend"
}

output "docker_tag_command" {
  description = "Command to tag image for ECR"
  value       = "docker tag ${var.project_name}:${var.image_tag} ${aws_ecr_repository.backend.repository_url}:${var.image_tag}"
}

output "docker_push_command" {
  description = "Command to push image to ECR"
  value       = "docker push ${aws_ecr_repository.backend.repository_url}:${var.image_tag}"
}

output "force_new_deployment_command" {
  description = "Command to force a new ECS deployment"
  value       = "aws ecs update-service --cluster ${aws_ecs_cluster.this.name} --service ${aws_ecs_service.backend.name} --force-new-deployment --region ${var.aws_region}"
}
