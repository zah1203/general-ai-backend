# Genorax Platform

Clean Genorax repository for the AI backend and Terraform infrastructure.

## Structure

```text
backend/          FastAPI Genorax AI backend
terraform/ec2/    EC2 Terraform, copied from local machine later
terraform/ecs/    ECS/Fargate Terraform, copied from the ECS working branch
scripts/          Start/stop/deployment helper scripts
docs/             Notes and operational documentation
```

## Source of truth

- Application source: merged from `feature/sample-interpretation` and `feature/pubmed-biobert`
- ECS Terraform source: `ecs-working-backup-20260524-1856`
- EC2 Terraform source: local Mac folder, to be copied later
- Terraform state: S3 bucket `genorax-terraform-state`

Do not commit Terraform state files, `.terraform/`, secrets, or local `.env` files.
