variable "region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Prefix used for resource names"
  type        = string
  default     = "fruitapi"
}

variable "image_uri" {
  description = "Full container image URI for FruitAPI (e.g. ghcr.io/<owner>/<repo>:latest). The image must be in a public registry, or repository_credentials must be configured."
  type        = string
}

variable "container_port" {
  description = "Port the FruitAPI container listens on"
  type        = number
  default     = 8000
}

variable "task_cpu" {
  description = "Fargate task CPU units"
  type        = number
  default     = 256
}

variable "task_memory" {
  description = "Fargate task memory (MiB)"
  type        = number
  default     = 512
}

variable "desired_count" {
  description = "Number of ECS service tasks"
  type        = number
  default     = 1
}

variable "db_instance_class" {
  description = "RDS instance class (free tier eligible: db.t3.micro / db.t4g.micro)"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "RDS allocated storage in GB"
  type        = number
  default     = 20
}

variable "db_engine_version" {
  description = "MySQL engine version"
  type        = string
  default     = "8.0"
}

variable "db_name" {
  description = "Initial MySQL database name"
  type        = string
  default     = "fruitapi"
}

variable "db_username" {
  description = "MySQL master username"
  type        = string
  default     = "fruitapi"
}
