variable "container_name" {
  description = "Name of the Docker container running FruitAPI"
  type        = string
  default     = "fruitapi-local"
}

variable "host_port" {
  description = "Host port to expose FruitAPI on"
  type        = number
  default     = 8000
}

variable "db_name" {
  description = "MySQL database name"
  type        = string
  default     = "fruitapi"
}

variable "db_user" {
  description = "MySQL application user"
  type        = string
  default     = "fruitapi"
}

variable "db_password" {
  description = "MySQL password for the application user"
  type        = string
  default     = "fruitapi"
  sensitive   = true
}

variable "db_root_password" {
  description = "MySQL root password (local stack only)"
  type        = string
  default     = "rootpw"
  sensitive   = true
}
