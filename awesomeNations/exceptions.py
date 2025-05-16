from random import random
from typing import Optional

# This is probably being removed because it's not professional, makes the error message look
# more confusing or even ANNOYING, instead of actually motivating who is reading it.
def motivational_quotes() -> str:
    quotes = ('only put off until tomorrow what you are willing to die having left undone.',
              'all our dreams can come true, if we have the courage to pursue them.',
              'great things are done by a series of small things brought together.',
              "you've got to get up every morning with determination if you're going to go to bed with satisfaction.",
              'dream big. Work hard.',
              'you are your only limit.',
              "never be limited by other people's limited imaginations.",
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
              'if you can dream it, you can do it.')
    index = int(len(quotes) * random())
    return quotes[index]

def status_code_context(status_code: int) -> Optional[str]:
    common_status_codes: dict = {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        408: "Request Timeout",
        409: "Conflict",
        429: "Too Many Requests",
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
    }
    
    output: Optional[str] = common_status_codes.get(status_code)
    return output

class HTTPError(Exception):
    """
    Exception raised when request status code is not `200` (Failed).
    """
    def __init__(self, status_code) -> None:
        self.status_code_context: str | None = status_code_context(status_code)
        if not self.status_code_context:
            self.status_code_context = ""
        else:
            self.status_code_context = f" {self.status_code_context}"

        self.message: str = f'HTTP error, status code: {status_code}{self.status_code_context}. Hope This Totally Pleases-you!'
        super().__init__(f'{self.message}')

class ConnectionError(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(f"An error occuried while estabishing connection: {reason}.\nMaybe it's a problem with your internet?")

class DataError(Exception):
    """
    Exception to warn about data processing failures, such encoding or decoding errors.
    """
    def __init__(self, data_name: str, reason: str):
        message = f"Could not process [{data_name}]: {reason}"
        super().__init__(message)

if __name__ == "__main__":
    raise ConnectionError("500")