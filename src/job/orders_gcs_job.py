# from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, TableEnvironment

def create_orders_sink_gcs(t_env):
    table_name = 'orders_sink'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            `order_id` STRING,
            `user_id` STRING,
            `eval_set` STRING,
            `order_number` INT,
            `order_dow` INT,
            `order_hour_of_day` INT,
            `days_since_prior_order` FLOAT
        ) WITH (
            'connector' = 'filesystem',
            'path' = 'gs://fake-ecommerce-taxi-data-447320/insta_cart/orders/',
            'format' = 'csv',
            'sink.parallelism' = '1'
        )
    """
    t_env.execute_sql(sink_ddl)
    
    return table_name


def create_orders_source_local(t_env):
    table_name = "orders_source"
    
    source_ddl = f"""
        CREATE TABLE {table_name} (
            `order_id` STRING,
            `user_id` STRING,
            `eval_set` STRING,
            `order_number` INT,
            `order_dow` INT,
            `order_hour_of_day` INT,
            `days_since_prior_order` FLOAT
        ) WITH (
            'connector' = 'filesystem',
            'path' = 'file:///opt/data/orders.csv',  -- Local CSV file path
            'format' = 'csv',
            'csv.ignore-parse-errors' = 'true'
        );
    """
    t_env.execute_sql(source_ddl)
    
    return table_name


def log_processing_orders():
    # Set up the table environment for batch mode using the unified TableEnvironment
    settings = EnvironmentSettings.new_instance().in_batch_mode().build()
    t_env = TableEnvironment.create(settings)
    
    try:
        # Create source and sink tables
        source_table = create_orders_source_local(t_env)
        gcs_sink_table = create_orders_sink_gcs(t_env)

        # Insert records into the GCS sink
        t_env.execute_sql(
            f"""
            INSERT INTO {gcs_sink_table}
            SELECT
                `order_id`,
                `user_id`,
                `eval_set`,
                `order_number`,
                `order_dow`,
                `order_hour_of_day`,
                `days_since_prior_order`
            FROM {source_table}
            """
        ).wait()

    except Exception as e:
        print("Writing records to GCS failed:", str(e))


if __name__ == '__main__':
    log_processing_orders()
