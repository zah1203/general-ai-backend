# Genorax AI Backend - Terraform EC2 Dev Deployment

This Terraform configuration provisions a **simple, destroyable AWS dev/test environment** for running the Genorax FastAPI backend on a single EC2 instance using Docker.

## What this deploys

- Default VPC networking (for simplicity)
- Security Group with:
  - SSH (22) from `allowed_ssh_cidr`
  - FastAPI (8000) from `allowed_api_cidr`
  - All outbound traffic
- IAM role + instance profile for EC2 with:
  - `AmazonSSMManagedInstanceCore`
  - `CloudWatchAgentServerPolicy`
- Amazon Linux 2023 EC2 instance with public IP
- User data bootstrap to:
  - Install Docker + Git
  - Clone repository
  - Build Docker image
  - Run container on port 8000

> **Note:** This is for **dev/testing only** (not production).

---

## Prerequisites

- Terraform >= 1.5
- AWS CLI configured with credentials that can create IAM, EC2, and networking resources
- An existing EC2 key pair in your target region

## 1) Configure AWS CLI

```bash
aws configure
```

Set your AWS Access Key, Secret Key, default region, and output format.

## 2) Copy tfvars example

```bash
cp terraform.tfvars.example terraform.tfvars
```

## 3) Update required values in `terraform.tfvars`

- `key_name`
- `allowed_ssh_cidr`
- `allowed_api_cidr`
- `github_repo_url`

Example values:

```hcl
key_name         = "my-ec2-key"
allowed_ssh_cidr = "203.0.113.10/32"
allowed_api_cidr = "203.0.113.10/32"
github_repo_url  = "https://github.com/my-org/genorax-ai-backend.git"
```

## 4) Initialize, plan, and apply

```bash
terraform init
terraform plan
terraform apply
```

## 5) Test the API

After apply completes, Terraform will output the EC2 public IP.

```bash
curl http://<EC2_PUBLIC_IP>:8000/health
```

You can also open:

- `http://<EC2_PUBLIC_IP>:8000/docs`

## 6) Destroy when done

```bash
terraform destroy
```

---

## File overview

- `main.tf` - AWS resources (networking, SG, IAM, EC2)
- `variables.tf` - input variables
- `outputs.tf` - key deployment outputs
- `terraform.tfvars.example` - example variable values
- `user_data.sh.tpl` - EC2 bootstrap script using `templatefile()` input `github_repo_url`

## Notes

- Uses default VPC/default subnet to keep setup minimal.
- Suitable for quick validation/testing and easy teardown.
- For production, move to private subnets, ALB, ECS/EKS, ECR, IAM least privilege, secrets management, and observability hardening.
