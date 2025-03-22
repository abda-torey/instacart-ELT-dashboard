# from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, TableEnvironment

def create_products_sink_gcs(t_env):
    table_name = 'products_sink'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            `product_id` INT,
            `product_name` STRING,
            `aisle_id` INT,
            `department_id` INT
        ) WITH (
            'connector' = 'filesystem',
            'path' = 'gs://fake-ecommerce-taxi-data-447320/insta_cart/products/',  -- Output GCS path
            'format' = 'csv',
            'sink.parallelism' = '1'
        )
    """
    t_env.execute_sql(sink_ddl)
    
    return table_name


def create_products_source_local(t_env):
    table_name = "products_source"
    
    source_ddl = f"""
        CREATE TABLE {table_name} (
            `product_id` INT,
            `product_name` STRING,
            `aisle_id` INT,
            `department_id` INT
        ) WITH (
            'connector' = 'filesystem',
            'path' = 'file:///opt/data/products.csv',  -- Local CSV file path
            'format' = 'csv',
            'csv.ignore-parse-errors' = 'true'
        );
    """
    t_env.execute_sql(source_ddl)
    
    return table_name


def log_processing_products():
    # Set up the table environment for batch mode using the unified TableEnvironment
    settings = EnvironmentSettings.new_instance().in_batch_mode().build()
    t_env = TableEnvironment.create(settings)
    
    try:
        # Create source and sink tables
        source_table = create_products_source_local(t_env)
        gcs_sink_table = create_products_sink_gcs(t_env)

        # Insert records into the GCS sink
        t_env.execute_sql(
            f"""
            INSERT INTO {gcs_sink_table}
            SELECT
                `product_id`,
                `product_name`,
                `aisle_id`,
                `department_id`
            FROM {source_table}
            """
        ).wait()

    except Exception as e:
        print("Writing records to GCS failed:", str(e))


if __name__ == '__main__':
    log_processing_products()