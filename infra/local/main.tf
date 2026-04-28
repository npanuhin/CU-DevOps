terraform {
  required_version = ">= 1.5.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

# Build the FruitAPI image from the repository's Dockerfile.
resource "docker_image" "fruitapi" {
  name = "fruitapi:local"

  build {
    context = abspath("${path.module}/../..")
    tag     = ["fruitapi:local"]
  }
}

# Run the image as a container exposing port 8000.
resource "docker_container" "fruitapi" {
  name    = var.container_name
  image   = docker_image.fruitapi.image_id
  restart = "unless-stopped"

  ports {
    internal = 8000
    external = var.host_port
  }
}
