import re
from binascii import a2b_base64

__all__ = ('clear_trash',)

_sub_trash = re.compile(
    '#h|//_//|I0A=|I0Ah|I0Aj|I0Ak|I0BA|I0Be|I14=|I14h|I14j|I14k|I15A|I15e|ISE=|ISEh|ISEj|ISEk|ISFA|ISFe|ISM=|ISMh'
    '|ISMj|ISMk|ISNA|ISNe|ISQ=|ISQh|ISQj|ISQk|ISRA|ISRe|IUA=|IUAh|IUAj|IUAk|IUBA|IUBe|IV4=|IV4h|IV4j|IV4k|IV5A|IV5e'
    '|IyE=|IyEh|IyEj|IyEk|IyFA|IyFe|IyM=|IyMh|IyMj|IyMk|IyNA|IyNe|IyQ=|IyQh|IyQj|IyQk|IyRA|IyRe|JCE=|JCEh|JCEj|JCEk'
    '|JCFA|JCFe|JCM=|JCMh|JCMj|JCMk|JCNA|JCNe|JCQ=|JCQh|JCQj|JCQk|JCRA|JCRe|JEA=|JEAh|JEAj|JEAk|JEBA|JEBe|JF4=|JF4h'
    '|JF4j|JF4k|JF5A|JF5e|QCE=|QCEh|QCEj|QCEk|QCFA|QCFe|QCM=|QCMh|QCMj|QCMk|QCNA|QCNe|QCQ=|QCQh|QCQj|QCQk|QCRA|QCRe'
    '|QEA=|QEAh|QEAj|QEAk|QEBA|QEBe|QF4=|QF4h|QF4j|QF4k|QF5A|QF5e|XiE=|XiEh|XiEj|XiEk|XiFA|XiFe|XiM=|XiMh|XiMj|XiMk'
    '|XiNA|XiNe|XiQ=|XiQh|XiQj|XiQk|XiRA|XiRe|XkA=|XkAh|XkAj|XkAk|XkBA|XkBe|Xl4=|Xl4h|Xl4j|Xl4k|Xl5A|Xl5e').sub


def clear_trash(trash_string: str) -> str:
    return a2b_base64(b'%b==' % _sub_trash('', trash_string).encode('ASCII')).decode('ASCII')
