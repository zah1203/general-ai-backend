# Genorax AI Backend ECS (Fargate) Terraform

This folder adds a **new ECS Fargate deployment** for the existing FastAPI backend.
It is intentionally separate from the existing `terraform/` EC2 setup, so the current EC2 dev deployment remains intact.

## A) Confirm branch

```bash
git checkout feature/pubmed-biobert
```

> If this branch is not present locally, fetch it from your remote first.

## B) Optional: bootstrap remote Terraform state (S3 + DynamoDB)

You can create backend state resources first using `state-bootstrap/`:

```bash
cd state-bootstrap
terraform init
terraform plan -var="state_bucket_name=<globally-unique-bucket>" -var="lock_table_name=<lock-table-name>"
terraform apply -var="state_bucket_name=<globally-unique-bucket>" -var="lock_table_name=<lock-table-name>"
terraform output backend_config_example
cd ..
```

## C) Deploy ECS infrastructure from `terraform/ecs`

### Option 1: Local state (quick testing)

```bash
terraform init
terraform plan
terraform apply
```

### Option 2: Remote S3 state (recommended)

1. Create an S3 bucket for Terraform state.
2. Enable bucket versioning and encryption.
3. Create a DynamoDB table for locks with partition key `LockID` (String).
4. Choose one backend method:
   - copy `backend.tf.example` to `backend.tf` and replace placeholder values, **or**
   - copy `backend.hcl.example` to `backend.hcl` and set real values.
5. Run:

```bash
terraform init -backend-config=backend.hcl
terraform plan
terraform apply
```

## D) Configure variables

Copy and edit `terraform.tfvars.example`:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Set at least:
- `aws_region`
- `openai_api_key_secret_arn` (optional but recommended)
- `image_tag` (if not using `latest`)

## E) Authenticate Docker to ECR

After `terraform apply`, use the output command:

```bash
terraform output -raw ecr_login_command | bash
```

## F) Build image from backend folder

From repository root:

```bash
docker build -t genorax-ai-backend:latest ./genorax-ai-backend
```

## G) Tag image for ECR

```bash
ECR_URL=$(cd terraform/ecs && terraform output -raw ecr_repository_url)
docker tag genorax-ai-backend:latest ${ECR_URL}:latest
```

## H) Push image to ECR

```bash
docker push ${ECR_URL}:latest
```

## I) Force ECS new deployment

```bash
cd terraform/ecs
terraform output -raw force_new_deployment_command
# run the printed aws ecs update-service command
```

## J) Test app

```bash
ALB_DNS=$(terraform output -raw alb_dns_name)
curl "http://${ALB_DNS}/health"
```

Open in browser:

- `http://<alb_dns>/docs`

## K) Destroy infrastructure

```bash
terraform destroy
```

If remote backend is configured in S3, you can run `terraform destroy` later from Jenkins, a laptop, or another EC2 instance by:
1. checking out the same repo/terraform folder,
2. running `terraform init` with the same backend config,
3. then executing `terraform destroy`.

## Files in this folder

- `main.tf`: ECS, ALB, SGs, IAM, ECR, CloudWatch logs.
- `variables.tf`: Configurable defaults for dev.
- `outputs.tf`: URLs and helper commands for image push/deploy.
- `backend.tf.example`: Example inline backend block.
- `backend.hcl.example`: Example backend config file for `-backend-config`.
- `state-bootstrap/`: Optional module to create S3 + DynamoDB state resources.
