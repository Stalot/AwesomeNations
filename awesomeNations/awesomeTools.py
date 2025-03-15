from typing import Optional

class Authentication():
    """Nation authentication"""
    def __init__(self,
                 password: Optional[str] = None,
                 autologin: Optional[str] = None):
        self.password = password
        self.autologin = autologin
        self.xpin: Optional[int] = None
    
    def get(self) -> dict[str]:
        auth_headers: dict[str] = {
            "X-Password": self.password if self.password else "",
            "X-Autologin": self.autologin if self.autologin else "",
            "X-Pin": self.xpin if self.xpin else ""
        }
        return auth_headers