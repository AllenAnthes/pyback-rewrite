def suggestion_modal(trigger_id):
    return {
        'trigger_id': trigger_id,
        'dialog': {
            "callback_id": "suggestion_modal",
            "title": "Help topic suggestion",
            "submit_label": "Submit",
            "trigger_id": trigger_id,
            "elements": [{
                "type": "text",
                "label": "Suggestion",
                "name": "suggestion",
                "placeholder": "Underwater Basket Weaving"
            }]
        }
    }


def action_menu_message(action_button, channel, message_ts):
    text = HELP_MENU_RESPONSES[action_button]
    return {
        'text': text,
        'channel': channel['id'],
        'ts': message_ts,
        'as_user': True,
    }


HELP_MENU_RESPONSES = {
    "slack": "Slack is an online chatroom service that the Operation Code community uses.\n"
             "It can be accessed online, via https://operation-code.slack.com/ or via\n"
             "desktop or mobile apps, located at https://slack.com/downloads/. In addition to\n"
             "chatting, Slack also allows us to share files, audio conference and even program\n"
             "our own bots! Here are some tips to get you started:\n"
             "  - You can customize your notifications per channel by clicking the gear to the\n"
             "    left of the search box\n"
             "  - Join as many channels as you want via the + next to Channels in the side bar.",
    "python": "Python is a widely used high-level programming language used for general-purpose programming.\n"
              "It's very friendly for beginners and is great for everything from web development to \n"
              "data science.\n\n"
              "Here are some python resources:\n"
              "    Operation Code Python Room: <#C04D6M3JT|python>\n"
              "    Python's official site: https://www.python.org/\n"
              "    Learn Python The Hard Way: https://learnpythonthehardway.org/book/\n"
              "    Automate The Boring Stuff: https://automatetheboringstuff.com/",
    "mentor": "The Operation Code mentorship program aims to pair you with an experienced developer in order to"
              " further your programming or career goals. When you sign up for our mentorship program you'll fill"
              " out a form with your interests. You'll then be paired up with an available mentor that best meets"
              " those interests.\n\n"
              "If you're interested in getting paired with a mentor, please fill out our sign up form"
              " here: http://op.co.de/mentor-request.\n    ",
    "javascript": "Javascript is a high-level programming language used for general-purpose programming.\n"
                  "In recent years it has exploded in popularity and with the popular node.js runtime\n"
                  "environment it can run anywhere from the browser to a server.\n\n"
                  "Here are some javascript resources:\n    Operation Code Javascript Room: <#C04CJ8H2S|javascript>\n"
                  "    Javascript Koans: https://github.com/mrdavidlaing/javascript-koans\n"
                  "    Eloquent Javascript: http://eloquentjavascript.net/\n"
                  "    Node School: http://nodeschool.io/\n"
                  "    Node University: http://node.university/courses",
    "ruby": "Ruby is one of the most popular languages to learn as a beginner.\n"
            "While it can be used in any situation it's most popular for it's\n"
            "web framework 'Rails' which allows people to build websites quickly \n"
            "and easily.\n\n"
            "Here are some ruby resources:\n"
            "    Operation Code Ruby Room: <#C04D6GTGT|ruby>\n"
            "    Try Ruby Online: http://tryruby.org/\n"
            "    Learn Ruby The Hard Way: http://ruby.learncodethehardway.org/book\n"
            "    Learn To Program: http://pine.fm/LearnToProgram/\n"
            "    Ruby Koans: http://rubykoans.com/"
}
