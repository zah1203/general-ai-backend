# Terraform State Bootstrap (S3 + DynamoDB)

This folder creates Terraform remote-state prerequisites for `terraform/ecs`:

- S3 bucket (versioning, encryption, public access blocked)
- DynamoDB table (`LockID` hash key, PAY_PER_REQUEST)

## Usage

```bash
terraform init
terraform plan \
  -var="state_bucket_name=<globally-unique-bucket>" \
  -var="lock_table_name=<lock-table-name>"
terraform apply \
  -var="state_bucket_name=<globally-unique-bucket>" \
  -var="lock_table_name=<lock-table-name>"
```

## Useful outputs

```bash
terraform output state_bucket_name
terraform output lock_table_name
terraform output backend_config_example
```

You can copy `backend_config_example` output into `terraform/ecs/backend.hcl`.
