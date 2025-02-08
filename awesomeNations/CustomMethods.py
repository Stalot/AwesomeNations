import re
import xmltodict
import time
from random import random

def string_is_number(string: str) -> bool:
    if type(string) is not str:
        raise TypeError(string)
    pattern = re.compile(r'^-?\d+(\.\d+)?$')
    return bool(pattern.match(string))

def format_key(string: str = None, uppercase: bool = False, replace_empty: str = None, delete_not_alpha: bool = False) -> str:
    formatted_string = None
    if string:
        if delete_not_alpha:
            for char in string:
                if not char.isalpha() and not char.isspace():
                    string = string.replace(char, '')

        if not uppercase:
            string = string.lower()
        else:
            string = string.upper()

        if replace_empty:
            string = string.replace(' ', replace_empty)

        formatted_string = string
    return formatted_string

def join_keys(keys: list | tuple = ['hello', 'world'], separator: str = '+') -> str:
    try:
        result = keys
        if type(keys) != str:
            string_keys = (str(key) for key in keys)
            result = separator.join(string_keys)
        return result
    except:
        raise ValueError(f"{keys} is {type(keys).__name__}, keys must be list or tuple.")

def generate_epoch_timestamp() -> int:
    timestamp: int = int(time.time())
    return timestamp

def check_nationstates_api_ratelimit(limit_remaining: int = None, reset_delay: int = None) -> None:
    if limit_remaining <= 1:
        time.sleep(reset_delay + 1)

def motivational_quotes() -> str:
    quotes = ['only put off until tomorrow what you are willing to die having left undone.',
              'all our dreams can come true, if we have the courage to pursue them.',
              'great things are done by a series of small things brought together.',
              "you've got to get up every morning with determination if you're going to go to bed with satisfaction.",
              'dream big. Work hard.',
              'you are your only limit.',
              "never be limited by other people's limited imaginations."
              'we cannot solve problems with the kind of thinking we employed when we came up with them.',
              'stay away from those people who try to disparage your ambitions. Small minds will always do that, but great minds will give you a feeling that you can become great too.',
              'success is not final; failure is not fatal: It is the courage to continue that counts.',
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
              'if you can dream it, you can do it.']
    index = int(len(quotes) * random())
    return quotes[index]

def status_code_context(status_code: int = None) -> str | None:
    common_status_codes: dict = {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        408: "Request Timeout",
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
    }
    
    output: str | None = common_status_codes.get(status_code)
    return output

if __name__ == "__main__":
    myList = "awesome", "yep"
    print(join_keys(myList))