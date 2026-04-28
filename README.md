# intro-to-devops

Starter repository for the Intro to DevOps course homework. You will extend this app across the modules (endpoints, database, CI/CD, deployment, security).

**Start here:** [PROJECT-REQUIREMENTS.md](./PROJECT-REQUIREMENTS.md) — what the application must do and how it maps to the course.

## Branching strategy — GitHub Flow

`main` is the only long-lived branch and is always kept green and deployable. All work happens on short-lived feature branches named after the lecture or change (e.g. `lecture-3/pr-pipeline`, `fix/cheapest-empty`). Changes land on `main` only through pull requests after the PR-workflow CI is green; direct pushes to `main` are disallowed by branch protection. The PR pipeline runs unit tests on every push to a PR; the `main` pipeline (`unit → build image → integration → version → push`) runs after merge.

## Run locally with Terraform

The `infra/local/` directory holds a Terraform configuration that builds the project's Docker image and runs it as a local container. It mirrors what the AWS deployment will do later, just on your machine.

Prerequisites: Docker running, Terraform >= 1.5.

```sh
cd infra/local
terraform init
terraform apply -auto-approve
# FruitAPI is now on http://localhost:8000
curl http://localhost:8000/health

terraform destroy -auto-approve
```

Override defaults with `-var` (e.g. `terraform apply -var="host_port=8080"`).
