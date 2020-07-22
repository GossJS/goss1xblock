"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Scope
from django.utils.safestring import SafeText
import textwrap
import urllib
import json
import random

@XBlock.wants('user')
class Goss1XBlock(XBlock):
    """
    XBlock checks if a certain URL returns what is expected 
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    score = Integer(
        default=0, scope=Scope.user_state,
        help="An indicator of success",
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the Goss1XBlock, shown to students
        when viewing courses.
        """
        user_service = self.runtime.service(self, 'user')
        xb_user = user_service.get_current_user()
        CURRENT = xb_user.opt_attrs.get('edx-platform.username')

        XURL = 'https://fork.kodaktor.ru/testxblock2'
        response = urllib.urlopen(XURL)
        data = json.loads(response.read())
        CHECK = data['message']

        html = self.resource_string("static/html/goss1xblock.html")
        frag = Fragment(html.format(self=self))

        res = textwrap.dedent("""
            <h2>Server app challenge</h2>
            <p>Your server app URL should return this: <span id="gosscurrent">{}</span>!</h2>
            <p>The address {} returned {}</h2>
            <div>Enter URL: <input id='gossinput' /><br/>
            <button id='gosssend'>send to server</button>
            </div> 
        """).format(CURRENT, XURL, CHECK)
        frag.add_content(SafeText(res))

        frag.add_css(self.resource_string("static/css/goss1xblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/goss1xblock.js"))
        frag.initialize_js('Goss1XBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def set_score(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # indicator is now 100...
        if data['key'] == 'hundred':
             self.score = 100
        else:
             self.score = 0

        event_data = {'value': self.score / 100, 'max_value': 100}
        self.runtime.publish(self, 'grade', event_data)

        url = "https://fork.kodaktor.ru/publog3?EDXEDX---------"
        urllib.urlopen(url+'score --- published')        
        return {"score": self.score}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("Goss1XBlock",
             """<problem/>
             """),
            ("Multiple Goss1XBlock",
             """<vertical_demo>
                <goss1xblock/>
                <goss1xblock/>
                <goss1xblock/>
                </vertical_demo>
             """),
        ]

