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
import datetime
import projection

from google.appengine.ext import db

class MainHandler(webapp2.RequestHandler):
    def get(self):
        try:
            self.response.write('Welcome. You are already dead body..')
        except DeadlineExceededError:
            self.response.write('Error')
        	
class MemberLogin(webapp2.RequestHandler):
    def get(self):
        try:
            p_name = self.request.get('name')
            p_pin = self.request.get('pin')
            p_clcode = self.request.get('clcode')
            
            if is_empty(p_name) or is_empty(p_pin) or is_empty(p_clcode):
                projection.fail_result(self, 501, 'missing paramer')
                return
            
            m = Member.all().filter('name =', p_name)
            if m.count() == 0:
                member = Member(name=p_name, pin=p_pin, clcode=p_clcode, created = datetime.datetime.now().date())
                member.initilizeValue()
                key = member.put()
                projection.success_result(self, projection.member_to_dict(member, key), {'first_login':True})
            else:
                member = m.fetch(1)[0]
                if member.pin == p_pin:
                    # if changed clcode 
                    if member.clcode != p_clcode:
                        member.clcode = p_clcode
                        member.put()                        
                    projection.success_result(self, projection.member_to_dict(member, key = None), {'first_login':False})
                else:
                    projection.fail_result(self, 510, 'invalid pincode')
        except:
            projection.fail_result(self, 500, 'unknown error')                    
            
class GetMembers(webapp2.RequestHandler):
    def get(self):
        q = Member.all()
        projection.success_result(self, projection.members_to_list(q), extra_value = None)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/member/login', MemberLogin),
    ('/get', GetMembers)
], debug=True)


class Member(db.Model):
    name = db.StringProperty(required=True)
    clcode = db.StringProperty(required=True)
    pin = db.StringProperty(required=True)
    created = db.DateProperty(required=True)    
    win = db.IntegerProperty()
    lose = db.IntegerProperty()
    draw = db.IntegerProperty()
    game_count = db.IntegerProperty()
    rock_count = db.IntegerProperty()
    paper_count = db.IntegerProperty()
    scissor_count = db.IntegerProperty()
    last_game_id = db.IntegerProperty()
    last_game_win = db.BooleanProperty()
    def initilizeValue(self):
        self.win=0
        self.lose=0
        self.draw=0
        self.game_count=0
        self.rock_count=0
        self.paper_count=0
        self.scissor_count=0
        self.last_game_id=0
        self.last_game_win=False

def is_empty(string):
    if string is None or string == '':
        return True
    else:
        return False
    
