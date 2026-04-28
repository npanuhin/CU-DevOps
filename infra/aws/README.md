# FruitAPI on AWS — Terraform

Provisions:

- **VPC**: uses the AWS default VPC and its public subnets.
- **Security groups**: ALB → ECS task → RDS, locked down by SG references.
- **RDS**: MySQL 8.0, `db.t3.micro`, single-AZ, 20 GB, encrypted.
- **Secrets Manager**: random master password stored as a JSON secret.
- **IAM**: ECS task execution role with permission to read the secret.
- **ECS**: Fargate cluster, task definition, service, ALB on port 80.
- **CloudWatch Logs**: 7-day retention.

## Prerequisites

1. AWS CLI configured (`aws configure`) with credentials for an IAM user that can manage IAM/EC2/RDS/ECS/SecretsManager/CloudWatch.
2. Terraform ≥ 1.5.
3. The FruitAPI Docker image pushed to a registry that ECS can pull anonymously. The simplest path is GHCR with the package set to **Public**.
   - In GitHub: navigate to your repo → Packages → the `fruitapi` package → Package settings → Change visibility → Public.

## Apply

```sh
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars and set image_uri to your image, e.g. ghcr.io/<owner>/<repo>:latest

terraform init
terraform plan
terraform apply
```

After apply (RDS provisioning takes 5–10 minutes), grab the ALB URL:

```sh
terraform output alb_url
curl "$(terraform output -raw alb_url)/health"
```

## Tear down

```sh
terraform destroy
```

> **Note**: `aws_secretsmanager_secret` is configured with `recovery_window_in_days = 0` so destroy removes the secret immediately, allowing reapply with the same name.

## Updating the image

The task definition pins `image_uri`. To roll out a new image:

1. Push the new image (CI does this on `main`).
2. Update `image_uri` in `terraform.tfvars` (or pass `-var image_uri=...`).
3. `terraform apply` — Terraform updates the task definition and ECS rolls the service.

If you keep `:latest` as the tag, Terraform won't detect a change. Force a redeploy with:

```sh
aws ecs update-service --cluster fruitapi-cluster --service fruitapi --force-new-deployment
```
