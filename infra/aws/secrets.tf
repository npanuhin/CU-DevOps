# Generate a strong random password for the RDS master user.
resource "random_password" "db" {
  length  = 32
  special = true
  # MySQL master password constraints: avoid /, @, ", and spaces.
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# Store the DB credentials in Secrets Manager so the ECS task can pull them at runtime.
resource "aws_secretsmanager_secret" "db" {
  name                    = "${var.project_name}/db"
  description             = "FruitAPI MySQL credentials"
  recovery_window_in_days = 0 # destroy immediately when terraform destroy is run
}

resource "aws_secretsmanager_secret_version" "db" {
  secret_id = aws_secretsmanager_secret.db.id
  secret_string = jsonencode({
    username = var.db_username
    password = random_password.db.result
    host     = aws_db_instance.mysql.address
    port     = aws_db_instance.mysql.port
    dbname   = var.db_name
  })
}
