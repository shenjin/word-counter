#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import json
from google.appengine.api import urlfetch
from bs4 import BeautifulSoup

class WordCountHandler(webapp2.RequestHandler):
    def post(self):
        urls = self.request.params.get("urls")

        if not urls:
            self.response.error(404)

        urls = json.loads(urls)

        keywords = {}

        for url in urls:
            r = urlfetch.fetch(url)
            soup = BeautifulSoup(r.content, 'html.parser')

            lists = soup('li')
            text = ''
            print lists
            for list in lists:
                if not list.find_parent('form'):
                    try:
                        text += ' ' + list.text.encode('ascii', 'ignore').decode('ascii')
                    except:
                        pass

            for str in text.split():
                keywords[str] = keywords.get(str,0) + 1

        print keywords.items()
        result = sorted(keywords.items(), key=lambda x:x[1], reverse=True)
        ret = json.dumps(result)
        self.response.out.write(ret)


app = webapp2.WSGIApplication([
    ('/word-count', WordCountHandler)
], debug=True)
