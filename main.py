import sys
import paramiko  ###SSH LIBRARY###
from paramiko_expect import \
    SSHClientInteraction  ###TAKES AN ACTION ACCORDING TO INPUT CODE AND PROVIDES STOP THE CODE (expect)###
import telnetlib
from queue import Queue
import threading

line_break = "\r\n"
line_end = "\r"
vrp_cli_length = "screen-length 0 tempo"


#### Both HUAWEI&CISCO CPE's via Telnet&SSH via LDAP ######
##features : Aware that CPE is Cisco or Huawei besides via Telnet or SSH and sends to appropriate commands.###

def connectionSSO(ip):
    # Definitions

    SSO_prompt = '.*\$ '
    bash_prompt = ".*]$ "
    telnet_prompt = ".*:"
    configure_prompt = '.*)#'
    user_prompt = '.*sername:'
    pass_prompt = '.*assword: '
    huawei_sys_prompt = '.*]'
    cpe_prompt = ".*>"
    enable_prompt = ".*#"
    ssh_prompt = ".*? "
    Username = "username"
    Password = "password"
    SSO = "ip addrress"
    SSH = paramiko.SSHClient()
    SSH.load_system_host_keys()
    SSH.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    telnet = telnetlib.Telnet()
    # remote_connection = SSH.invoke_shell()

    ldap_user = 'LDAP_USER'
    ldap_pass = 'LDAP_PASS'
    defaultuser = 'defaultuser'
    defaultuserpass = 'defaultpass'
    file1 = open("Cisco&Huawei-Telnet&SSH-LDAP.txt", "a")

    try:
        SSH.connect(hostname=SSO, username=Username, password=Password, port=22)
        with SSHClientInteraction(SSH, timeout=10, display=False, buffer_size=65535) as command:
            command.expect(SSO_prompt, timeout=1)
            command.send('bash')
            command.expect(SSO_prompt)
            command.send('telnet ' + ip)  ###at first trying telnet
            print(ip)
            command.expect([user_prompt, SSO_prompt])
            if command.last_match == SSO_prompt:  # continue with ssh
                command.send('ssh {}@{}'.format(ldap_user, ip))
                print(ip + ' via SSH')
                command.expect(ssh_prompt)
                command.send("yes")
                command.expect(pass_prompt)

                if pass_prompt == command.last_match:
                    print("###########Router is reachable.###########")
                    # file1.write(ip + "successful access\n")
                    command.send(ldap_pass)
                    command.expect([cpe_prompt, enable_prompt])
                    # command.expect(cpe_prompt) or command.expect(enable_prompt)
                    if command.last_match == cpe_prompt:
                        print("###########Connection to Huawei Router was established.###########")
                        file1.write(ip + " Huawei" + " SSH" + " successful access\n")

                        command.send('terminal monitor')
                        command.expect(cpe_prompt)
                        command.send('sys')
                        command.expect(huawei_sys_prompt)
                        command.send("COMMAND")
                        command.expect(huawei_sys_prompt)

                        command.send("q")
                        command.expect(cpe_prompt)
                        command.send("save")
                        command.expect(cpe_prompt)
                        command.send("q")

                    elif command.last_match == enable_prompt:
                        print("###########Connection to Cisco Router was established.###########")
                        file1.write(
                            ip + " Cisco" + " SSH" + " successful access\n")  ####test if connection to router exactly##

                        command.send('terminal length 0')
                        command.expect(enable_prompt)
                        command.send('conf t')
                        command.expect(enable_prompt)
                        command.send("COMMAND")
                        command.expect(enable_prompt)

                        command.send("end")
                        command.expect(enable_prompt)
                        command.send("write")
                        command.expect(enable_prompt)
                        command.send("exit")
                    else:
                        print(
                            "###########CPE is uncreachable via LDAP,please check your user,pass info.(might be defaultuser.)")
                        file1.write(ip + " CPE is unreachable via LDAP\n")

                else:
                    print("###########CPE is uncreachable.###########")  ###cannot access via telnet or ssh
                    file1.write(ip + " CPE is unreachable\n")


            elif command.last_match == user_prompt:  # continue with telnet
                print(ip + ' via Telnet')
                command.send(ldap_user)
                command.expect(pass_prompt)
                command.send(ldap_pass)
                command.expect([cpe_prompt, enable_prompt])

                if cpe_prompt == command.last_match:
                    print("###########Connection to Huawei Router was established.###########")
                    file1.write(ip + " Huawei" + " Telnet" + " successful access\n")

                    command.send('terminal monitor')
                    command.expect(cpe_prompt)
                    command.send('sys')
                    command.expect(huawei_sys_prompt)
                    command.send("COMMAND")
                    command.expect(huawei_sys_prompt)

                    command.send("q")
                    command.expect(cpe_prompt)
                    command.send("save")
                    command.expect(cpe_prompt)
                    command.send("q")

                elif enable_prompt == command.last_match:
                    print("###########Connection to Cisco Router was established.###########")
                    file1.write(ip + " Cisco" + " Telnet" + " successful access\n")

                    command.send('terminal length 0')
                    command.expect(enable_prompt)
                    command.send('conf t')
                    command.expect(enable_prompt)
                    command.send("COMMAND")
                    command.expect(enable_prompt)

                    command.send("write")
                    command.expect(enable_prompt)
                    command.send("exit")

                else:
                    print("###########CPE is uncreachable.###########")  ###cannot access via telnet or ssh
                    file1.write(ip + " CPE is unreachable\n")



            else:
                print("###########CPE is unreachable at first.###########")
                file1.write(ip + " CPE is unreachable at first\n")

    except Exception as Error:
        print(Error)
    return 0


sira = Queue()


def worker(q):
    while True:
        q = sira.get()
        connectionSSO(q)
        sira.task_done()


def sshThread():
    with open('iplist.txt') as f:
        content = f.readlines()
    ip_list = [x.strip() for x in content]

    for i in range(10):
        trd = threading.Thread(target=worker, args=(sira,))
        trd.setDaemon(True)
        trd.start()

    for ip in ip_list:
        sira.put(ip)
    sira.join()


if __name__ == '__main__':
    sshThread()

sys.exit()

##barka##