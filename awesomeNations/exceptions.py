from random import random

def motivational_quotes():
    quotes = ['only put off until tomorrow what you are willing to die having left undone.',
              'all our dreams can come true, if we have the courage to pursue them.',
              'great things are done by a series of small things brought together.',
              "you've got to get up every morning with determination if you're going to go to bed with satisfaction.",
              'dream big. Work hard.',
              'you are your only limit.',
              "never be limited by other people's limited imaginations."
              'we cannot solve problems with the kind of thinking we employed when we came up with them.',
              'stay away from those people who try to disparage your ambitions. Small minds will always do that, but great minds will give you a feeling that you can become great too.',
              'Success is not final; failure is not fatal: It is the courage to continue that counts.',
              'it is better to fail in originality than to succeed in imitation.',
              'the road to success and the road to failure are almost exactly the same.',
              'develop success from failures. Discouragement and failure are two of the surest stepping stones to success.',
              'success is peace of mind, which is a direct result of self-satisfaction in knowing you made the effort to become the best of which you are capable.',
              'the pessimist sees difficulty in every opportunity. The optimist sees opportunity in every difficulty.',
              "you learn more from failure than from success. Don't let it stop you. Failure builds character.",
              'goal setting is the secret to a compelling future.',
              'setting goals is the first step in turning the invisible into the visible.',
              'your work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is great work. And the only way to do great work is to love what you do. If you haven’t found it yet, keep looking. Don’t settle. As with all matters of the heart, you’ll know when you find it.',
              'think like a queen. A queen is not afraid to fail. Failure is another stepping stone to greatness.',
              'take the attitude of a student, never be too big to ask questions, never know too much to learn something new.',
              'success is stumbling from failure to failure with no loss of enthusiasm.',
              'perfection is not attainable. But if we chase perfection we can catch excellence.',
              "get a good idea and stay with it. Dog it, and work at it until it's done right.",
              'optimism is the faith that leads to achievement. Nothing can be done without hope and confidence.'
              'work until your bank account looks like a phone number.',
              'talent wins games, but teamwork and intelligence win championships.',
              'teamwork is the ability to work together toward a common vision. The ability to direct individual accomplishments toward organizational objectives. It is the fuel that allows common people to attain uncommon results.',
              "don't let someone else's opinion of you become your reality.",
              'do the best you can. No one can do more than that.',
              'If you can dream it, you can do it.']
    index = int(len(quotes) * random())
    return quotes[index]

class CensusNotFound(Exception):
    def __init__(self, censusid) -> None:
        self.message = f'Nice try! But censusid={censusid} is out of range. 88 is the maximum - did you forget, or were you hoping I would let it slide? Check your input. I do not do favors.\nJokes aside, {motivational_quotes()}'
        super().__init__(f'{self.message}')

class NationNotFound(Exception):
    def __init__(self, nation_name) -> None:
        self.message = f'Nation "{nation_name}" not found, perhaps this nation no longer exists or never existed.'
        super().__init__(f'{self.message}')

class RegionNotFound(Exception):
    def __init__(self, region_name) -> None:
        self.message = f'Oh no, the region "{region_name}" does not exist. Maybe you forgot a comma? Or did you think programming was easy? Cute.\nJokes aside, {motivational_quotes()}'
        super().__init__(f'{self.message}')

class HTTPError(Exception):
    def __init__(self, status_code) -> None:
        self.message = f'HTTP error, status code: {status_code}. Hope This Totally Pleases-you!\nJokes aside, {motivational_quotes()}'
        super().__init__(f'{self.message}')