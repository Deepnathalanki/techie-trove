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

resource "aws_sagemaker_notebook_instance" "nbi" {
  name          = "Test"
  role_arn      = "arn:aws:iam::419248363630:role/service-role/AmazonSageMaker-ExecutionRole-20230306T144430"
  instance_type = "ml.g4dn.xlarge"
  volume_size                  = 512

  tags = {
    auto-delete = "no"
  }
}
