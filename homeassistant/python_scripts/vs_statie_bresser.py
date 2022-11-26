# NOT USED

# Intercepts the data packets from the RTL2832U SDR -based container and dispatches them to "post_data"
# topic, while also posting an ON message on the state topic, to keep the station available in HA

station_attributes = data.get('payload')
message = {'topic':'home_assistant/statie_bresser/attributes', 
           'payload':station_attributes, 
           'qos':2, 
           'retain':'false'}
# logger.info('<VS script> Received data: {}'.format(station_attributes))
hass.services.call('mqtt', 'publish', message, False)

message = {'topic':'home_assistant/statie_bresser/state', 
           'payload':'ON', 
           'qos':2, 
           'retain':'false'}
# hass.services.call('mqtt', 'publish', message, False)
