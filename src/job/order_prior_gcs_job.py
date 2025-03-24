# from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, TableEnvironment
import os
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")

def create_order_products_prior_sink_gcs(t_env):
    table_name = 'order_products_prior_sink'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            `order_id` INT,
            `product_id` INT,
            `add_to_cart_order` INT,
            `reordered` INT
        ) WITH (
            'connector' = 'filesystem',
            'path' = 'gs://{BUCKET_NAME}/insta_cart/order_products_prior/',  -- Output GCS path
            'format' = 'csv',
            'sink.parallelism' = '1'
        )
    """
    t_env.execute_sql(sink_ddl)
    
    return table_name


def create_order_products_prior_source_local(t_env):
    table_name = "order_products_prior_source"
    
    source_ddl = f"""
        CREATE TABLE {table_name} (
            `order_id` INT,
            `product_id` INT,
            `add_to_cart_order` INT,
            `reordered` INT
        ) WITH (
            'connector' = 'filesystem',
            'path' = 'file:///opt/data/order_products__prior.csv',  -- Local CSV file path
            'format' = 'csv',
            'csv.ignore-parse-errors' = 'true'
        );
    """
    t_env.execute_sql(source_ddl)
    
    return table_name


def log_processing_order_products_prior():
    # Set up the table environment for batch mode using the unified TableEnvironment
    settings = EnvironmentSettings.new_instance().in_batch_mode().build()
    t_env = TableEnvironment.create(settings)
    
    try:
        # Create source and sink tables
        source_table = create_order_products_prior_source_local(t_env)
        gcs_sink_table = create_order_products_prior_sink_gcs(t_env)

        # Insert records into the GCS sink
        t_env.execute_sql(
            f"""
            INSERT INTO {gcs_sink_table}
            SELECT
                `order_id`,
                `product_id`,
                `add_to_cart_order`,
                `reordered`
            FROM {source_table}
            """
        ).wait()

    except Exception as e:
        print("Writing records to GCS failed:", str(e))


if __name__ == '__main__':
    log_processing_order_products_prior()
