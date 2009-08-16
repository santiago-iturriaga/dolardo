'''
Created on Aug 16, 2009

@author: santiago
'''
import sys
from datetime import datetime

import smtplib
from dolardo import log_file, smpt_host, smpt_password, smpt_port, smpt_user, smpt_to, smpt_from, smpt_subject

def report(msg):
    now = datetime.now().isoformat()
    full_msg = "[%s]\n%s\n" % (now, msg)
    
    try:
        write_log(full_msg)
    except:
        print sys.exc_info()
    
    try:
        send_mail(full_msg)
    except:
        print sys.exc_info()

def report_error(info):
    (type, value, traceback) = info
    report("Type: %s\nValue: %s\nTraceback: %s\n" % (type, value, traceback))
    
def write_log(msg):
    separator = '---------------------------------\n'
        
    log_handle = open(log_file, 'a+')
    log_handle.write(msg + separator)
    log_handle.close()
    
def send_mail(msg):
    full_msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" % (smpt_from, ", ".join(smpt_to), smpt_subject, msg))
    
    server = smtplib.SMTP(smpt_host, smpt_port)
    server.set_debuglevel(1)
    server.login(smpt_user, smpt_password)
    server.sendmail(smpt_from, smpt_to, full_msg)
    server.quit()
