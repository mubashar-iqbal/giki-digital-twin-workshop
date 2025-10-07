import logging
import azure.functions as func

from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.digitaltwins.core import DigitalTwinsClient

app = func.FunctionApp()

@app.event_grid_trigger(arg_name="event")
def EventGridTrigger(event: func.EventGridEvent):

    logging.info(event)

    data = event.get_json()["body"]

    logging.info(data)


    temperature = data.get('temperature')

    #Add Azure Digital Twin Instance URL
    ADT_URL = ""

    credential = DefaultAzureCredential()

    twin_instance = DigitalTwinsClient(ADT_URL, credential)

    if temperature > 30:
        temperature_alert = 'high'
    else:
        temperature_alert = 'normal'

    update_temperature = [
        {
            "op": "add",
            "path": "/Temperature",
            "value": temperature
        },
        {
            "op": "add",
            "path": "/Temperature_alert",
            "value": temperature_alert
        }
    ]

    twin_instance.update_digital_twin('TemperatureSensor', update_temperature)

    logging.info('updated!')