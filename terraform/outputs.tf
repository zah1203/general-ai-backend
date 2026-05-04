output "ec2_public_ip" {
  description = "Public IP address of the backend EC2 instance"
  value       = aws_instance.backend.public_ip
}

output "ec2_public_dns" {
  description = "Public DNS name of the backend EC2 instance"
  value       = aws_instance.backend.public_dns
}

output "fastapi_docs_url" {
  description = "FastAPI Swagger docs URL"
  value       = "http://${aws_instance.backend.public_ip}:8000/docs"
}

output "health_check_url" {
  description = "FastAPI health endpoint URL"
  value       = "http://${aws_instance.backend.public_ip}:8000/health"
}
