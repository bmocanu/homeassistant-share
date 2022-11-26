# Format: <data ID> : [ 
#            <device ID, relevant for the topic>, 
#            <content to send as payload via the topic>,
#            <retain or not> 
# ]
deviceDict = { 
    '11D285':['buton2_rf', 'ON',  'false'],
    '9AE1A1':['media_trigger', 'buton3_rf',  'false'], # Buton 3 
    'EAF5A1':['media_trigger', 'buton4_rf',  'false'], # Buton 4 
    '19B0E1':['media_trigger', 'buton5_rf',  'false'], # Buton 5 
    '9B8961':['media_trigger', 'buton6_rf',  'false'], # Buton 6 
    '088961':['media_trigger', 'buton7_rf',  'false'], # Buton 7
    'F61AA1':['media_trigger', 'buton8_rf',  'false'], # Buton 8
    'D3FD21':['media_trigger', 'buton9_rf',  'false'], # Buton 9
    '0C67A1':['media_trigger', 'buton10_rf', 'false'], # Buton 10
    '145C21':['buton11_rf',    'ON',         'false'], # Buton 11
    '8FF525':['buton12_rf',    'ON',         'false'], # Buton 12
    'E3EC21':['buton13_rf',    'ON',         'false'], # Buton 13
    'E2BD21':['buton14_rf',    'ON',         'false'], # Buton 14
    'ECC721':['media_trigger', 'buton15_rf', 'false'], # Buton 15
    'C34D21':['media_trigger', 'buton16_rf', 'false'], # Buton 16
    '6F4C21':['media_trigger', 'buton17_rf', 'false'], # Buton 17

    '8FE664':['fum1_rf',   'ON',  'false'],
    '043409':['fum2_rf',   'ON',  'false'],
    '8C0464':['fum3_rf',   'ON',  'false'],
    '94AC64':['fum4_rf',   'ON',  'false'],

    '052C2C':['misc4_rf',  'ON',  'false'],

    '2C52CC':['inund3_rf', 'ON',  'true'],
    '2C52C6':['inund3_rf', 'OFF', 'true'],
    # '2C52C9':['inund3_rf', 'OFF', 'true'], # Available signal

    '0A9403':['efra6_rf',  'ON',  'true'],
    '0A9409':['efra6_rf',  'OFF', 'true']
    # '0A940B':['efra6_rf',  'ON',  'true'], # PIN released
}

rfDataId = data.get('payload')

if rfDataId is not None:
  if rfDataId in deviceDict.keys():
    service_data = {'topic':'home_assistant/{}'.format(deviceDict[rfDataId][0]), 
                    'payload':'{}'.format(deviceDict[rfDataId][1]), 
                    'qos':2, 
                    'retain':'{}'.format(deviceDict[rfDataId][2])}
  else:
    service_data = {'topic':'home_assistant/unknown', 
                    'payload':'{}'.format(rfDataId), 
                    'qos':0, 
                    'retain':'false'}
    logger.warning('<rfbridge_demux> Received unknown RF command: {}'.format(rfDataId))
  hass.services.call('mqtt', 'publish', service_data, False)
