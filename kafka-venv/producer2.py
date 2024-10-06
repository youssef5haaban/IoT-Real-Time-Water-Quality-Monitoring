import pandas as pd
from sodapy import Socrata
import time
from confluent_kafka import Producer
import json
from dotenv import load_dotenv, set_key
import os
from tenacity import retry, stop_after_attempt, wait_exponential

# Load environment variables
load_dotenv('project.env')

# Load configuration from environment variables
APP_TOKEN = os.getenv('SOCRATA_APP_TOKEN')
DOMAIN = os.getenv('SOCRATA_DOMAIN', 'data.cityofchicago.org')
DATASET_ID = os.getenv('DATASET_ID', 'qmqz-2xku')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'water-quality')
BATCH_SIZE = int(os.getenv('BATCH_SIZE', 10))
SLEEP_TIME = int(os.getenv('SLEEP_TIME', 30))

def create_socrata_client():
    return Socrata(DOMAIN, APP_TOKEN)

def create_kafka_producer():
    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'client.id': 'water-quality-producer',
        'acks': 'all',
        'compression.type': 'snappy'
    }
    return Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def fetch_data(client, offset):
    try:
        return client.get(DATASET_ID, limit=BATCH_SIZE, offset=offset, order='measurement_id')
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise

def process_and_send_data(producer, results_df):
    for record in results_df.itertuples(index=False):
        try:
            message = {
                'Beach Name': getattr(record, 'beach_name', ''),
                'Measurement Timestamp': getattr(record, 'measurement_timestamp', ''),
                'Water Temperature': getattr(record, 'water_temperature', None),
                'Turbidity': getattr(record, 'turbidity', None),
                'Transducer Depth': getattr(record, 'transducer_depth', None),
                'Wave Height': getattr(record, 'wave_height', None),
                'Wave Period': getattr(record, 'wave_period', None),
                'Battery Life': getattr(record, 'battery_life', None),
                'Measurement ID': getattr(record, 'measurement_id', '')
            }
            
            message_encoded = json.dumps(message).encode('utf-8')
            producer.produce(KAFKA_TOPIC, value=message_encoded, callback=delivery_report)

        except (ValueError, TypeError, AttributeError) as e:
            print(f"Error processing record: {e}")
            continue

def get_offset():
    # Load the offset from the .env file
    return int(os.getenv('OFFSET', 0))

def update_offset(offset):
    # Update the offset in the .env file
    dotenv_path = 'project.env'
    set_key(dotenv_path, 'OFFSET', str(offset))

def main():
    client = create_socrata_client()
    producer = create_kafka_producer()
    offset = get_offset()  # Load the starting offset from the .env file

    try:
        while True:
            try:
                results = fetch_data(client, offset)
                if not results:
                    print("No more data to fetch. Waiting before next attempt.")
                    time.sleep(SLEEP_TIME)
                    continue

                results_df = pd.DataFrame.from_records(results)
                process_and_send_data(producer, results_df)

                offset += BATCH_SIZE
                update_offset(offset)  # Save the updated offset in the .env file
                producer.poll(0)
                
                print(f"Processed {len(results)} records. Sleeping for {SLEEP_TIME} seconds.")
                time.sleep(SLEEP_TIME)

            except Exception as e:
                print(f"An error occurred: {e}")
                time.sleep(SLEEP_TIME)  # Wait before retrying

    except KeyboardInterrupt:
        print("Received interrupt. Shutting down.")
    finally:
        print("Flushing remaining messages.")
        producer.flush()

if __name__ == "__main__":
    main()
