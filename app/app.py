 #!/usr/bin/env python
 # -*- coding: utf-8 -*-
from flask import Flask, request, Response
import json
import re
import os

app = Flask(__name__)

telegram_push_url = os.environ.get('TELEGRAM_PUSH_URL')
transcoder_push_url = os.environ.get('TRANSCODER_PUSH_URL')

@app.route('/ingest/streams', methods=['GET'])
def config_external_ingest():
   stream_name = request.args.get('name')
   server_hostname = request.args.get('client_host')
   if stream_name != None:
      stream_config = json.dumps({
      "streams":[
         {
            "protocols":{
               "hls":"true",
               "m4s":"true"
            },
            "pushes":[
               {
                  "timeout":5,
                  "url": telegram_push_url
               },
               {
                  "timeout":5,
                  "url": transcoder_push_url + stream_name
               }
            ],
            "name": stream_name,
            "title": 'k8s-' + stream_name,
            "inputs":[
               {
                  "url":"publish://"
               }
            ],
            "static":"false",
            "source_timeout":30
         }
      ]
   })
      return stream_config, 200, {'Content-Type': 'application/json'}
   else:
      response = json.loads('{"streams":[]}')
      return response, 200, {'Content-Type': 'application/json'}

@app.route('/transcoder/streams', methods=['GET'])
def config_external_transcoder():
   stream_name = request.args.get('name')
   server_hostname = request.args.get('client_host')
   if stream_name != None:
      stream_config = json.dumps(
         {
   "streams":[
      {
         "protocols":{
            "hls":"true",
            "m4s":"true"
         },
         "name":stream_name,
         "title":'k8s-' + stream_name,
         "inputs":[
            {
               "url":"publish://"
            }
         ],
         "static":"false",
         "source_timeout":30,
         "transcoder":{
            "global":{
               "hw":"cpu",
               "gop":50
            },
            "audio":{
               "codec":"aac",
               "bitrate":128000,
               "channels":2,
               "split_channels":"false"
            },
            "video":[
               {
                  "profile":"baseline",
                  "size":{
                     "strategy":"fit",
                     "width":1920,
                     "height":1080,
                     "background":"#000000"
                  },
                  "codec":"h264",
                  "bitrate":2000000,
                  "track":1,
                  "bframes":0,
                  "open_gop":"false",
                  "preset":"veryfast"
               },
               {
                  "profile":"baseline",
                  "size":{
                     "strategy":"fit",
                     "width":1024,
                     "height":576,
                     "background":"#000000"
                  },
                  "codec":"h264",
                  "bitrate":1500000,
                  "track":2,
                  "bframes":0,
                  "open_gop":"false",
                  "preset":"veryfast"
               },
               {
                  "profile":"baseline",
                  "size":{
                     "strategy":"fit",
                     "width":640,
                     "height":360,
                     "background":"#000000"
                  },
                  "codec":"h264",
                  "bitrate":500000,
                  "track":3,
                  "bframes":0,
                  "open_gop":"false",
                  "preset":"veryfast"
               }
            ],
            "decoder":{
               
            },
            "tracks":[
               
            ]
         },
         "segment_count":6,
         "segment_duration":2000
      }
   ]
})
      return stream_config, 200, {'Content-Type': 'application/json'}
   else:
      response = json.loads('{"streams":[]}')
      return response, 200, {'Content-Type': 'application/json'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8086, debug=True)