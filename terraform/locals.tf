locals {
  bucket_name          = "k9-kedro-on-aws"
  glue_db_name         = "kedro-on-aws"
  glue_tbl_name        = "transactions"
  athena_output_prefix = "athena-query-outputs/"

  schema = jsondecode(file("${path.module}/table_schema.json"))
}
