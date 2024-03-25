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
               "hls":"true"
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

@app.route('/dvr/streams', methods=['GET'])
def config_external_dvr():
   stream_name = request.args.get('name')
   server_hostname = request.args.get('client_host')
   if stream_name != None:
      stream_config = json.dumps({
      "streams":[
         {
            "protocols":{
               "hls":"true"
            },
            "name": stream_name,
            "title": 'k8s-' + stream_name,
            "inputs":[
               {
                  "url":"publish://"
               }
            ],
            "static":"false",
            "source_timeout":30,
            "dvr": {
               "reference": "archive",
               "expiration": 10800
            }
         }
      ]
   })
      return stream_config, 200, {'Content-Type': 'application/json'}
   else:
      response = json.loads('{"streams":[]}')
      return response, 200, {'Content-Type': 'application/json'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8086, debug=True)
