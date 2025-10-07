import time
import json
import random
from azure.iot.device import IoTHubDeviceClient, Message

# Replace with your device connection string
CONNECTION_STRING = ""

def main():
    # Create IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    print("IoT Hub device sending simulated telemetry. Press Ctrl+C to stop.")

    try:
        while True:
            # Simulated humidity sensor
            temperature = round(random.uniform(20.0, 50.0), 2)

            telemetry = {
                "temperature": temperature
            }

            # Convert to JSON string
            message = Message(json.dumps(telemetry))
            message.content_encoding = "utf-8"
            message.content_type = "application/json"
            # Send telemetry
            client.send_message(message)
            print(f"Sent telemetry: {telemetry}")

            time.sleep(10)

    except KeyboardInterrupt:
        print("Telemetry stopped by user")

    finally:
        client.shutdown()


# if __name__ == "__main__":
main()
