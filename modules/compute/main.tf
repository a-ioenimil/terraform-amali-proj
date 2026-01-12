data "aws_instances" "asg_instances" {
  instance_tags = {
    "aws:autoscaling:groupName" = aws_autoscaling_group.main.name
  }

  depends_on = [aws_autoscaling_group.main]
}

resource "aws_launch_template" "main" {
  name_prefix   = "${var.project_name}-lt"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  vpc_security_group_ids = [var.security_group_id]

  # user_data = base64encode(<<-EOF
  #             #!/bin/bash
  #             set -e
              
  #             # Install Docker
  #             apt-get update -y
  #             apt-get install -y docker.io
  #             systemctl start docker
  #             systemctl enable docker
  #             usermod -aG docker ubuntu
              
  #             # Wait for Docker to be ready
  #             until docker info > /dev/null 2>&1; do
  #               sleep 1
  #             done
              
  #             # Run phpMyAdmin for MySQL management
  #             docker run -d \
  #               --name phpmyadmin \
  #               --restart always \
  #               -p 80:80 \
  #               -e "PMA_HOST=${var.rds_endpoint}" \
  #               -e "PMA_PORT=3306" \
  #               -e "PMA_ARBITRARY=0" \
  #               -e "PMA_ABSOLUTE_URI=http://${var.alb_dns_name}/" \
  #               -v "/some/local/directory/sessions:/sessions:rw" \

  #               phpmyadmin:latest
              
  #             # Wait for container to be healthy
  #             sleep 30
  #             EOF
  # )

  user_data = base64encode(<<-EOF
            #!/bin/bash
            set -e
            
            # Install Docker
            apt-get update -y
            apt-get install -y docker.io
            systemctl start docker
            systemctl enable docker
            usermod -aG docker ubuntu
            
            # 1. Create the host directory (REQUIRED)
            # If you don't do this, Docker will create it as 'root', which can break permissions
            mkdir -p /var/lib/phpmyadmin/sessions
            chmod 777 /var/lib/phpmyadmin/sessions
            
            # Wait for Docker to be ready
            until docker info > /dev/null 2>&1; do
              sleep 1
            done
            
            # 2. Run phpMyAdmin with Quoted Volume and Environment Variables
            docker run -d \
              --name phpmyadmin \
              --restart always \
              -p 80:80 \
              -e "PMA_HOST=${var.rds_endpoint}" \
              -e "PMA_PORT=3306" \
              -e "PMA_ARBITRARY=0" \
              -e "PMA_ABSOLUTE_URI=http://${var.alb_dns_name}/" \
              -v "/var/lib/phpmyadmin/sessions:/sessions:rw" \
              phpmyadmin:latest
            
            sleep 30
            EOF
)

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name        = "${var.project_name}-instance"
      Environment = var.environment
    }
  }
}

resource "aws_autoscaling_group" "main" {
  name                = "${var.project_name}-asg"
  vpc_zone_identifier = var.subnet_ids
  target_group_arns   = [var.target_group_arn]
  min_size            = 2
  max_size            = 4
  desired_capacity    = 2

  launch_template {
    id      = aws_launch_template.main.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "${var.project_name}-asg-instance"
    propagate_at_launch = true
  }

  tag {
    key                 = "Environment"
    value               = var.environment
    propagate_at_launch = true
  }
}
