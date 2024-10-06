provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "instance1" {
  ami           = "ami-0fff1b9a61dec8a5f"
  instance_type = "g4dn.xlarge"
  tags = {
    Name = "g4dn-xlarge"
  }
}