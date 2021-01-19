#!/usr/bin/python3
import time

import boto3
from sense_hat import SenseHat

#
# Script configuration
#

# where is this Raspi located in the house?
ROOM_NAME = 'Bedroom1'

sense = SenseHat()
sense.clear()

client = boto3.client('cloudwatch')


def get_temperature() -> float:
    # get temperature from the SenseHat humidity sensor
    value = sense.get_temperature_from_humidity()
    value = round(value, 1)
    return value


def get_humidity() -> float:
    value = sense.get_humidity()
    value = round(value, 1)
    return value


def get_pressure() -> float:
    value = sense.get_pressure()
    value = round(value, 1)
    return value


def publish_room_parameters(room_name: str, temperature: float, humidity: float, pressure: float):
    response = client.put_metric_data(
        Namespace='AmbientMonitoring',
        MetricData=[
            {
                'MetricName': 'Temperature',
                'Dimensions': [
                    {
                        'Name': 'Room',
                        'Value': room_name,
                    },
                ],
                'Value': temperature,
            },
            {
                'MetricName': 'Humidity',
                'Dimensions': [
                    {
                        'Name': 'Room',
                        'Value': room_name,
                    },
                ],
                'Value': humidity,
                'Unit': 'Percent',
            },
            {
                'MetricName': 'Pressure',
                'Dimensions': [
                    {
                        'Name': 'Room',
                        'Value': room_name,
                    },
                ],
                'Value': pressure,
            },
        ]
    )

    return response


def main():
    print('temperature,pressure,humidity')
    while True:
        t = get_temperature()
        h = get_humidity()
        p = get_pressure()
        print(f"{t},{h},{p}")

        try:
            publish_room_parameters(ROOM_NAME, t, h, p)
        except Exception as e:
            print(f"ERROR: {e}")

        time.sleep(60)


if __name__ == "__main__":
    main()
