terraform {
  backend "s3" {
    region         = "ap-southeast-1"
    bucket         = "k9-tfstate"
    key            = "kedro-on-aws.tfstate"
    dynamodb_table = "k9-tfstate-locks"
    encrypt        = true
    kms_key_id     = "arn:aws:kms:ap-southeast-1:069566694064:key/60d4d47d-19cd-4e4d-98f5-b0a5e6823de5"
  }
}
