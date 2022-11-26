# This dictionary maps the buttons (received via MQTT from rfbridge_demux.py)
# to various media playback strategies. The key of the dictionary is the ID of 
# the button that was pressed, the value is an array of parameters for the playback
# strategy.
#
# <button ID>: ['playback strategy', <param1>, <param2> ]
#
# Strategies:
#   - radio: play radio from the Internet, better yet via IP proxy
#        - param1: the URL to play
#        - param2: the media content type
#   - spotify: play a Spotify content (album share ID, playlist share ID)
#        - param1: the content ID
#        - param2: not used
#   - mpd0: connect to mpd0 running on IP and play a local MP3 folder
#        - param1: the name of the folder to play in shuffle mode
#        - param2: not used

mediaTriggerDict = { 
  'buton3_rf': ['radio',   'http://ip:20000/zen_radio',     'audio/mp3'],
  'buton4_rf': ['radio',   'http://ip:20000/radio_cafe',    'audio/mp3'],
  'buton5_rf': ['radio',   'http://ip:20000/europa_fm',     'audio/mp3'],
  'buton6_rf': ['spotify', 'spotify:playlist:abcdabcdabcdabcd', ''         ], # Playlist 1
  'buton7_rf': ['spotify', 'spotify:playlist:abcdabcdabcdabcd', ''         ], # Playlist 2
  'buton8_rf': ['radio',   'http://ip:20000/magic_fm',      'audio/mp3'],
  'buton9_rf': ['radio',   'http://ip:20000/play_cafe',     'audio/mp3'],
  'buton10_rf':['radio',   'http://ip:20000/play_90s',      'audio/mp3'],
  'buton15_rf':['mpd0',    'colinde',                                 ''],
  'buton16_rf':['mpd0',    'muzica_veche',                            ''],
  'buton17_rf':['radio',   'http://ip:20000/radio_zu',      'audio/mp3']
}

rfDataId = data.get('payload')
logger.info('<media_trigger> Received RF ID: [{}]'.format(rfDataId))

if rfDataId is not None:
  if rfDataId in mediaTriggerDict.keys():
    logger.info('<media_trigger> Received RF ID: {}'.format(rfDataId))
    mediaType = mediaTriggerDict[rfDataId][0]
    mediaContentId = mediaTriggerDict[rfDataId][1]
    mediaContentType = mediaTriggerDict[rfDataId][2]

    hass.services.call('media_player', 'media_stop', { 
        'entity_id': 'media_player.boxa1_pt_bucatarie'
      }, False)

    if mediaType == 'radio':
      hass.services.call('media_player', 'play_media', { 
          'entity_id': 'media_player.boxa1_pt_bucatarie', 
          'media_content_id': mediaContentId,
          'media_content_type': mediaContentType
        }, False)
    elif mediaType == 'mpd0':
      hass.services.call('media_player', 'volume_set', { 
          'entity_id': 'media_player.mpd0',
          'volume_level': '1'
        }, False)
      hass.services.call('media_player', 'shuffle_set', { 
          'entity_id': 'media_player.mpd0',
          'shuffle': 'true'
        }, False)
      hass.services.call('media_player', 'play_media', { 
          'entity_id': 'media_player.mpd0', 
          'media_content_id': mediaContentId,
          'media_content_type': 'directory'
        }, False)
      hass.services.call('media_player', 'play_media', { 
          'entity_id': 'media_player.boxa1_pt_bucatarie', 
          'media_content_id': 'http://ip:28800',
          'media_content_type': 'audio/mp3'
        }, False)
    else:
      service_data = {'topic':'home_assistant/play_spotify', 
                      'payload':'{}'.format(mediaContentId), 
                      'qos':2, 
                      'retain':'false'}
      hass.services.call('mqtt', 'publish', service_data, False)
  else:
    logger.warning('<media_trigger> Received unknown RF ID: {}'.format(rfDataId))
