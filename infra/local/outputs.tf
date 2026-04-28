output "url" {
  description = "URL of the running FruitAPI"
  value       = "http://localhost:${var.host_port}"
}

output "container_name" {
  description = "Name of the running Docker container"
  value       = docker_container.fruitapi.name
}
