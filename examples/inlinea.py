import sys
import asyncio
import telepot
from telepot.async.delegate import per_inline_from_id, create_open

"""
$ python3.4 inlinea.py <token>

A bot that only cares about inline stuff.
"""

class InlineHandler(telepot.async.helper.UserHandler):
    def __init__(self, seed_tuple, timeout):
        super(InlineHandler, self).__init__(seed_tuple, timeout, flavors=['inline_query', 'chosen_inline_result'])
        self._answerer = telepot.async.helper.Answerer(self.bot)

    def on_inline_query(self, msg):
        def compute_answer():
            query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
            print(self.id, ':', 'Inline Query:', query_id, from_id, query_string)

            articles = [{'type': 'article',
                             'id': 'abc', 'title': query_string, 'message_text': query_string}]

            return articles

        self._answerer.answer(msg, compute_answer)

    def on_chosen_inline_result(self, msg):
        result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
        print(self.id, ':', 'Chosen Inline Result:', result_id, from_id, query_string)


TOKEN = sys.argv[1]

bot = telepot.async.DelegatorBot(TOKEN, [
    (per_inline_from_id(), create_open(InlineHandler, timeout=10)),
])
loop = asyncio.get_event_loop()

loop.create_task(bot.message_loop())
print('Listening ...')

loop.run_forever()
