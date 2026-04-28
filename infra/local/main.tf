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

# Private network for the API and DB to talk to each other.
resource "docker_network" "fruitapi" {
  name = "${var.container_name}-net"
}

# MySQL image.
resource "docker_image" "mysql" {
  name         = "mysql:8.0"
  keep_locally = true
}

# Persistent volume for MySQL data.
resource "docker_volume" "mysql_data" {
  name = "${var.container_name}-mysql-data"
}

# MySQL container.
resource "docker_container" "mysql" {
  name    = "${var.container_name}-mysql"
  image   = docker_image.mysql.image_id
  restart = "unless-stopped"

  env = [
    "MYSQL_ROOT_PASSWORD=${var.db_root_password}",
    "MYSQL_DATABASE=${var.db_name}",
    "MYSQL_USER=${var.db_user}",
    "MYSQL_PASSWORD=${var.db_password}",
  ]

  networks_advanced {
    name = docker_network.fruitapi.name
  }

  volumes {
    volume_name    = docker_volume.mysql_data.name
    container_path = "/var/lib/mysql"
  }

  healthcheck {
    test         = ["CMD", "mysqladmin", "ping", "-h", "127.0.0.1", "-u", "root", "-p${var.db_root_password}"]
    interval     = "10s"
    timeout      = "5s"
    retries      = 10
    start_period = "20s"
  }
}

# Build the FruitAPI image from the repository's Dockerfile.
resource "docker_image" "fruitapi" {
  name = "fruitapi:local"

  build {
    context = abspath("${path.module}/../..")
    tag     = ["fruitapi:local"]
  }
}

# Run the API container, wired to MySQL via env vars.
resource "docker_container" "fruitapi" {
  name    = var.container_name
  image   = docker_image.fruitapi.image_id
  restart = "unless-stopped"

  depends_on = [docker_container.mysql]

  env = [
    "DB_HOST=${docker_container.mysql.name}",
    "DB_PORT=3306",
    "DB_USER=${var.db_user}",
    "DB_PASSWORD=${var.db_password}",
    "DB_NAME=${var.db_name}",
  ]

  networks_advanced {
    name = docker_network.fruitapi.name
  }

  ports {
    internal = 8000
    external = var.host_port
  }
}
