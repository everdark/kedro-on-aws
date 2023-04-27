# E03. Read Dataset from S3 with PySpark

To allow `pyspark` to read files from `s3`,
we will need two jars:

- [hadoop-aws](https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-aws)
- [aws-java-sdk-bundle](https://mvnrepository.com/artifact/com.amazonaws/aws-java-sdk-bundle)

Make sure they are present in your `SPARK_HOME` jars folder.
If Spark is installed via pip (`pip install pyspark`),
the folder should be something like

```
<your-python-lib-path>/site-packages/pyspark/jars
```

Also add the following arg to the `spark.yml` (or your spark submit job argument):

```yml
spark.hadoop.fs.s3a.impl: org.apache.hadoop.fs.s3a.S3AFileSystem
```

To test the catalog:

```python
# kedro ipython
df = catalog.load("parsed_transactions")
df.show()
```
