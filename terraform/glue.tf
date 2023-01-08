resource "aws_glue_catalog_database" "default" {
  name = local.glue_db_name
}

resource "aws_glue_catalog_table" "default" {

  depends_on = [
    aws_glue_catalog_database.default,
  ]

  name          = local.glue_tbl_name
  database_name = aws_glue_catalog_database.default.name

  storage_descriptor {
    location = "s3://${local.bucket_name}/${local.glue_tbl_name}"

    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
    }

    dynamic "columns" {
      for_each = local.schema
      iterator = column
      content {
        name    = column.value.Name
        type    = column.value.Type
        comment = column.value.Comment
      }
    }
  }
}
