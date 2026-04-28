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
