#!c:\radcube\projects\iu_dualcredit\iudualcredit\iudualcreditvenv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'sshtunnel==0.1.4','console_scripts','sshtunnel'
__requires__ = 'sshtunnel==0.1.4'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('sshtunnel==0.1.4', 'console_scripts', 'sshtunnel')()
    )
