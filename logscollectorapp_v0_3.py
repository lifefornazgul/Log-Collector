import tkinter as tk
import os
import sys
import paramiko
import threading
import time
from tkinter import *
import re
import random

HEIGHT = 120
WIDTH = 520


root = tk.Tk()
root.title('CableOS Log Collector (v.0.3)')
USER = 'ccap'
SECRET = 'ccap'
THEPORT ='2022'
click_number = 0

processbutclickflag = 0
def collectlogs_main():
       global click_number
       global processbutclickflag
       global canvas
       click_number = 1
       host = entry_server.get()
       client = paramiko.client.SSHClient()
       listbot_logs.insert(tk.END, str('Initializing...'))
       listbot_logs.yview_moveto(1)
       time.sleep(3)
       testmsg = ' ->Success. \nOpenning SSH connection...'
       splited = testmsg.split('\n')
       for i in splited:
              listbot_logs.insert(tk.END,str(i))
              listbot_logs.yview_moveto(1)
       try:
              client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
              client.connect(hostname=host, port=THEPORT, username=USER, password=SECRET, timeout=15)
       except:
              testmsg = '-> Failed.\n\'{}\' is not responding on SSH request.\nShutdown in 30 sec.'.format(host)
              canvas.config(height=400)
              processbut.config(text='Hide details ^^')
              processbutclickflag = 1
              button.config(text='Stopped')
              splited = testmsg.split('\n')
              for i in splited:
                     listbot_logs.insert(tk.END,str(i))
                     listbot_logs.yview_moveto(1)
              time.sleep(30)
              root.destroy()
       testmsg = ' ->Success. \nChecking namespace...'
       splited = testmsg.split('\n')
       for i in splited:
              listbot_logs.insert(tk.END,str(i))
              listbot_logs.yview_moveto(1)
       try:
              stdin, stdout, stderr = client.exec_command('ip netns identify $$', get_pty=True)
              data = stdout.read() + stderr.read()
              res = data.decode("utf-8")
       except:
              testmsg = '-> Failed.\n\'{}\' Error occured while checking current namespace.'.format(host)
              canvas.config(height=400)
              processbut.config(text='Hide details ^^')
              button.config(text='Stopped')
              processbutclickflag = 1
              splited = testmsg.split('\n')
              for i in splited:
                     listbot_logs.insert(tk.END,str(i))
                     listbot_logs.yview_moveto(1)
              listbot_logs.insert(tk.END,str('Error message: ',res))
              listbot_logs.yview_moveto(1)
              return
       if reg_res(res) == 1:
              testmsg = ' ->Success. \nConnected via OOB namespace.'
              splited = testmsg.split('\n')
              for i in splited:
                     listbot_logs.insert(tk.END,str(i))
                     listbot_logs.yview_moveto(1)
       else:
              testmsg = ' ->Success. \nConnected via In-band namespace.'
              splited = testmsg.split('\n')
              for i in splited:
                     listbot_logs.insert(tk.END,str(i))
                     listbot_logs.yview_moveto(1)
       listbot_logs.insert(tk.END,'Cleaning "tech-support" folder...')
       listbot_logs.yview_moveto(1)
       time.sleep(2)
       try:
              stdin, stdout, stderr = client.exec_command('sudo rm /srv/cableos/tech-support/tech-support__cs*', get_pty=True)
              time.sleep(2)
              stdin.write('ccap\n')
              time.sleep(2)
              stdin.flush()
       except:
              testmsg = ' ->Failed.'
              canvas.config(height=400)
              processbut.config(text='Hide details ^^')
              button.config(text='Stopped')
              processbutclickflag = 1
              splited = testmsg.split('\n')
              for i in splited:
                     listbot_logs.insert(tk.END,str(i))
                     listbot_logs.yview_moveto(1) 
              listbot_logs.insert(tk.END,str('Restart and try again.'))
              listbot_logs.yview_moveto(1)
              return
       client.close()
       listbot_logs.insert(tk.END,' ->Success.')
       listbot_logs.yview_moveto(1)
       if reg_res(res) == 1:
              collectlogs_oob(host)
       else:
              collectlogs_inband(host)


def reg_res(result):
       resreg = re.match('oob',result)
       if resreg:
              return(1)
       else:
              return(0)

def collectlogs_oob(host):
       client = paramiko.client.SSHClient()
       client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
       client.connect(hostname=host, port=THEPORT, username=USER, password=SECRET, timeout=15)
       testmsg = 'Connecting to default namespace...'
       splited = testmsg.split('\n')
       for i in splited:
              listbot_logs.insert(tk.END,str(i))
              listbot_logs.yview_moveto(1)
       stdin, stdout, stderr = client.exec_command('sudo ip netns exec oob ln -s /proc/1/ns/net /var/run/netns/default', get_pty=True)
       time.sleep(2)
       stdin.write('ccap\n')
       time.sleep(2)
       stdin.flush()
       testmsg = ' ->Success. \nGenerating logs...'
       splited = testmsg.split('\n')
       for i in splited:
              listbot_logs.insert(tk.END,str(i))
              listbot_logs.yview_moveto(1)
       try:
              stdin, stdout, stderr = client.exec_command('sudo ip netns exec default python3 /usr/share/cosm-mon/scripts/show_tech_support.py', get_pty=True)
              time.sleep(2)
              stdin.write('ccap\n')
              time.sleep(2)
              stdin.flush()
              data = stdout.read() + stderr.read()
       except:
              testmsg = ' ->Failed. \n Command to generate logs has failed. Please try different method.'
              canvas.config(height=400)
              processbut.config(text='Hide details ^^')
              button.config(text='Stopped')
              processbutclickflag = 1
              splited = testmsg.split('\n')
              for i in splited:
                     listbot_logs.insert(tk.END,str(i))
                     listbot_logs.yview_moveto(1)
              print("Error: ",data)
              return
       time.sleep(2)
       res = data.decode("utf-8")
       testmsg = ' ->Success. \nDisconnecting from default namespace...'
       splited = testmsg.split('\n')
       for i in splited:
              listbot_logs.insert(tk.END,str(i))
              listbot_logs.insert(tk.END,str(res))
              listbot_logs.yview_moveto(1)
       stdin, stdout, stderr = client.exec_command('sudo ip netns delete default', get_pty=True)
       client.close()
       if 'All dumps are available' in res:
              splited = res.split('\n')
              for i in splited:
                     time.sleep(round(random.uniform(0, 0.2), 3))
                     listbot_logs.insert(tk.END,str(i))
                     listbot_logs.yview_moveto(1)
       else:
              listbot_logs.insert(tk.END, str('[ERROR]:'))
              canvas.config(height=400)
              processbut.config(text='Hide details ^^')
              button.config(text='Stopped')
              processbutclickflag = 1
              splited = res.split('\n')
              for i in splited:
                     listbot_logs.insert(tk.END,str(i))
                     listbot_logs.yview_moveto(1)
       uploadlogs(host)

def collectlogs_inband(host):
       client = paramiko.client.SSHClient()
       client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
       client.connect(hostname=host, port=THEPORT, username=USER, password=SECRET, timeout=15)
       testmsg = 'Generating logs...'
       splited = testmsg.split('\n')
       for i in splited:
              listbot_logs.insert(tk.END,str(i))
              listbot_logs.yview_moveto(1)
       stdin, stdout, stderr = client.exec_command('echo show tech-support | /opt/confd/bin/confd_cli --noaaa -u harmonic', get_pty=True)
       data = stdout.read()
       res = data.decode("utf-8")
       client.close()
       if 'All dumps are available' in res:
              splited = res.split('\n')
              for i in splited:
                     time.sleep(0.2)
                     listbot_logs.insert(tk.END,str(i))
                     listbot_logs.yview_moveto(1)
       else:
              listbot_logs.insert(tk.END, str('[ERROR]:'))
              canvas.config(height=400)
              processbut.config(text='Hide details ^^')
              button.config(text='Stopped')
              processbutclickflag = 1
              listbot_logs.yview_moveto(1)
              splited = res.split('\n')
              for i in splited:
                     listbot_logs.insert(tk.END,str(i))
                     listbot_logs.yview_moveto(1)
       uploadlogs(host)





def uploadlogs(host):
       touploadlist =[]
       testmsg = ' \n Starting to upload the logs...'
       time.sleep(2)
       splited = testmsg.split('\n')
       for i in splited:
              listbot_logs.insert(tk.END,str(i))
              listbot_logs.yview_moveto(1)
       client = paramiko.client.SSHClient()
       client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
       client.connect(hostname=host, port=THEPORT, username=USER, password=SECRET)
       stdin, stdout, stderr = client.exec_command('ls -l /srv/cableos/tech-support/')
       temp = stdout.read() + stderr.read()
       templss = temp.decode("utf-8")
       lss = templss.split('\n')
       for i in range(len(lss)):
              resreg = re.search('tech.*tar.gz',lss[i])
              if resreg:
                     touploadlist.append(resreg.group())
       varuploadlist = ''
       if range(len(touploadlist)) == 1 :
              testmsg = ' \n INFO: Provided host "{}" is COS-M slave - logs from second Core are not available.\n \n Uploading in process...'.format(host)
              splited = testmsg.split('\n')
              for i in splited:
                     listbot_logs.insert(tk.END,str(i))
                     listbot_logs.yview_moveto(1)
              time.sleep(5)
       for i in range(len(touploadlist)):
              varuploadlist = varuploadlist + '/srv/cableos/tech-support/' + str(touploadlist[i]) + ','
       stdin, stdout, stderr = client.exec_command('sudo ip netns exec oob ping google.com -c 3', get_pty=True)
       time.sleep(2)
       stdin.write('ccap\n')
       time.sleep(2)
       stdin.flush()
       time.sleep(2)
       dnsres = stdout.read() + stderr.read()
       resdns = dnsres.decode("utf-8")
       if "0% packet loss" in resdns:
              testmsg = ' INFO: DNS lookup successful...'
              splited = testmsg.split('\n')
              for i in splited:
                     listbot_logs.insert(tk.END,str(i))
                     listbot_logs.yview_moveto(1)
              BOXADRESS ='ftps://ftp.box.com'
              HARMONICADDRESS = 'ftp://hlit2210:37M7iDEi@ftp.harmonicinc.com/'
       else:
              testmsg = '\nWARNING: DNS or Routing issue detected.\n Uploading via alternative route...\n'.format(host)
              splited = testmsg.split('\n')
              for i in splited:
                     listbot_logs.insert(tk.END,str(i))
                     listbot_logs.yview_moveto(1)
              BOXADRESS ='ftps://107.152.25.220'
              HARMONICADDRESS = 'ftp://hlit2210:37M7iDEi@50.206.121.43/'
       BOXFTP = 'sudo ip netns exec oob curl --connect-timeout 15 --ftp-create-dirs --upload-file "{' + varuploadlist + '}" -# --insecure -u "maksym.halkin@harmonicinc.com:123456789Maxim" ' + BOXADRESS +'/Cable%20Edge%20Dept/Customer%20Support/Logs%20Collector%20storage/' + str(host) + '/'
       BOXURL = 'https://harmonicinc.app.box.com/folder/79335169487'
       HARMONICFTP = 'sudo ip netns exec oob curl --connect-timeout 15 --ftp-create-dirs -# -T "{' + varuploadlist + '}" ' + HARMONICADDRESS + str(host) + '/'
       HARMONICURL ='ftp://hlit2210:37M7iDEi@ftp.harmonicinc.com/'
       if var.get() == 1:
              ftp = BOXFTP
              ftpres = BOXURL
       else:
              ftp = HARMONICFTP
              ftpres = HARMONICURL
       uploadcommand = ftp    
       stdin, stdout, stderr = client.exec_command(uploadcommand, get_pty=True)
       time.sleep(2)
       stdin.write('ccap\n')
       time.sleep(2)
       stdin.flush()
       time.sleep(2)
       data = stdout.read() + stderr.read()
       res = data.decode("utf-8")
       client.close()      
       if "100.0%" in res:
           testmsg = ' ->Success.\n--- FINISHED! ---\nLogs successfully uploaded there:\n {} \n (Use Ctrl+C to copy and open in a browser)'.format(str(ftpres))
           canvas.config(height=400)
           processbut.config(text='Hide details ^^')
           button.config(text='Done!')
           processbutclickflag = 1
           splited = testmsg.split('\n')
           for i in splited:
              listbot_logs.insert(tk.END,str(i))
              listbot_logs.yview_moveto(1)
       else:
              listbot_logs.insert(tk.END, str('[ERROR]:'))
              canvas.config(height=400)
              processbut.config(text='Hide details ^^')
              button.config(text='Stopped')
              processbutclickflag = 1
              listbot_logs.yview_moveto(1)
              splited = res.split('\n')
              for i in splited:
                     listbot_logs.insert(tk.END,str(i))
                     listbot_logs.yview_moveto(1)
              return


class AppClass:
       def intro(self):
              time.sleep(2)
              self.introframe = tk.Frame(root, bd=0)
              self.introframe.place(x=180, y=68, width=250, height=74)
              labintro = tk.Label(self.introframe,bd=2, justify='left', font="Calibri 16")
              labintro.place(relx=0, rely=0, relwidth=1,relheight=1)
              labtext = tk.Text(labintro,font="Calibri 10",bd=5)
              labtext.insert(tk.END,"You are using Alpha version.\n\nReport bugs to\nmaksym.halkin@harmonicinc.com")
              labtext.place(relx=0, rely=0, relwidth=1,relheight=1)
              but = tk.Button(self.introframe, text="Got it", command=b.introframe.destroy)
              but.place(relx=0.64, rely=0.7, relwidth=0.24,relheight=0.15)
       def test(self):
              pass#self.introframe.destroy()
              processbut.place(x=150, y=90, width=200, height=20)
              button.config(bd='1', state='disabled',text='Running...')
              entry_server.config(state='disabled')
              R2.config(state='disabled')
              R1.config(state='disabled')
              global click_number
              host = entry_server.get()
              ftp = entry_ftp.get()
              if reg_ip(host) == 1:
                     None
              else:
                     errormsg_inputhost()
              if click_number == 1:
                     errormsg_doubleclick()


def showprogress():
       global canvas
       global processbutclickflag
       if processbutclickflag == 0:
              processbut.config(text='Hide details ^^')
              canvas.config(height=400)
              processbutclickflag = 1
       else:
              processbut.config(text='Show details >>')
              canvas.config(height=120)
              processbutclickflag = 0




def errormsg_inputhost():
       framebot.destroy()
       global canvas
       global processbutclickflag
       canvas.config(height=400)
       processbut.config(text='Hide details ^^')
       button.config(text='Stopped')
       processbutclickflag = 1
       errframe = tk.Frame(root, bd=0)
       errframe.place(x=150, y=210, width=200,height=100)
       laberr = tk.Label(errframe,bd=2, justify='left', font="Calibri 16")
       laberr.place(relx=0, rely=0, relwidth=1,relheight=1)
       errtext = tk.Text(laberr,font="Calibri 12",bd=5)
       errtext.insert(tk.END,"Please use only valid IP. \n Format: x.x.x.x \n Please restart the app.")
       errtext.place(relx=0, rely=0, relwidth=1,relheight=1)
       errbut = tk.Button(errframe, text="Ok", command=root.destroy)
       errbut.place(relx=0.64, rely=0.7, relwidth=0.24,relheight=0.15)

def errormsg_inputftp():
       framebot.destroy()
       global canvas
       global processbutclickflag
       canvas.config(height=400)
       button.config(text='Stopped')
       processbut.config(text='Hide details ^^')
       processbutclickflag = 1
       errframe = tk.Frame(root, bd=0)
       errframe.place(x=150, y=210, width=200,height=100)
       laberr = tk.Label(errframe,bd=2, justify='left', font="Calibri 16")
       laberr.place(relx=0, rely=0, relwidth=1,relheight=1)
       errtext = tk.Text(laberr,font="Calibri 12",bd=5)
       errtext.insert(tk.END,"Only Harmonic ftp is allowed. \n Format:\nftp://<username>:password@<harmonicftp>\n Please restart.")
       errtext.place(relx=0, rely=0, relwidth=1,relheight=1)
       errbut = tk.Button(errframe, text="Ok, close now", command=root.destroy)
       errbut.place(relx=0.64, rely=0.7, relwidth=0.24,relheight=0.15)

def errormsg_doubleclick():
       global canvas
       global processbutclickflag
       canvas.config(height=400)
       button.config(text='Stopped')
       processbut.config(text='Hide details ^^')
       processbutclickflag = 1
       framebot.destroy()
       errframe = tk.Frame(root, bd=0)
       errframe.place(x=150, y=210, width=200,height=100)
       laberr = tk.Label(errframe,bd=2, justify='left', font="Calibri 16")
       laberr.place(relx=0, rely=0, relwidth=1,relheight=1)
       errtext = tk.Text(laberr,font="Calibri 12",bd=5)
       errtext.insert(tk.END,"Another session is already in process.\n\nRestart is needed.")
       errtext.place(relx=0, rely=0, relwidth=1,relheight=1)
       errbut = tk.Button(errframe, text="Ok", command=root.destroy)
       errbut.place(relx=0.64, rely=0.7, relwidth=0.24,relheight=0.15)

def reg_ip(ip):
       resreg = re.match('^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$',ip)
       if resreg:
              return(1)
       else:
              return(0)

def reg_harmonicftp(link):
       resreg = re.match('ftp://\w+:\w+@.*ftp\.harmonicinc\.com$',link)
       if resreg:
              return(1)
       else:
              return(0)


canvas = tk.Canvas(root,height=HEIGHT, width=WIDTH, bg='#EFFEFF')
canvas.pack()


frametop = tk.Frame(root, bg='#b3e6ff',bd=5)
frametop.place(x=50, y=20, width=410,height=62)


label_server = tk.Label(frametop,text="Host:")
label_server.place(relx=0.02, rely=0.2, relwidth=0.08, relheight=0.3)

entry_server = tk.Entry(frametop,bg="white")
entry_server.place(relx=0.12,rely=0.2,relwidth=0.6,relheight=0.3)



label_ftp = tk.Label(frametop,text="FTP:")
# label_ftp.place(relx=0.05, rely=0.6, relwidth=0.10, relheight=0.2)

label_dest = tk.Label(frametop,text="Destination:",anchor='w')
label_dest.place(relx=0.02, rely=0.6, relwidth=0.16, relheight=0.3)

entry_ftp = tk.Entry(frametop,bg="white")
# entry_ftp.place(relx=0.15,rely=0.6,relwidth=0.5,relheight=0.2)

button = tk.Button(frametop,text="START", bg='#BDE1FF', command=lambda: [b.test(),t.start()])
button.place(relx=0.78, rely=0.2, relwidth=0.16, relheight=0.6)
button.config(width='200',height='200',bd='5')

processbut = tk.Button(root,text="Show details >>", bg='#BDE1FF' ,command=lambda:showprogress())
# processbut.place(x=150, y=90, width=200, height=20)


def sel():
   selection = "Link to files will be generated when finished " #+ str(var.get())
   label.config(text = selection)


var = IntVar()
R1 = Radiobutton(frametop, text="BOX.com", variable=var, value=1,
                  command=sel, bg='#b3e6ff', font = "Calibri 10")
R1.place(relx=0.25,rely=0.6,relwidth=0.17,relheight=0.2)

R2 = Radiobutton(frametop, text="Harmonic FTP", variable=var, value=2,
                  command=sel, bg='#b3e6ff',font = "Calibri 10")
R2.place(relx=0.43,rely=0.6,relwidth=0.23,relheight=0.2)


label = Label(frametop,bg='#b3e6ff')
# label.place(relx=0.18,rely=0.74,relwidth=0.6,relheight=0.2)






framebot = tk.Frame(root,bg='#e6eeff',bd=2)
framebot.place(x=10, y=122, relwidth=0.965, relheight=0.7)

label_title = tk.Label(framebot,text="Progress:", bg='#cccccc')
# label_title.place(relx=0, rely=0, relwidth=1, relheight=0.06)


scrollbar = tk.Scrollbar(framebot)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

scrollbar2 = tk.Scrollbar(framebot,orient='horizontal')
scrollbar2.pack(side=tk.BOTTOM, fill=tk.X)

listbot_logs = tk.Listbox(framebot, bg='white', justify='left',yscrollcommand=scrollbar.set, xscrollcommand=scrollbar2.set)
listbot_logs.place(relx=0, rely=0, relwidth=0.972, relheight=0.95)

scrollbar.config(command=listbot_logs.yview)
scrollbar2.config(command=listbot_logs.xview)

t = threading.Thread(target=collectlogs_main, name = 'ssh_thread')
b = AppClass()
# t2 = threading.Thread(target=b.intro, name = 'intro_thread')
# t2.start()

root.mainloop()







