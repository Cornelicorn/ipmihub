import pyipmi
import pyipmi.interfaces
import socket

def createSession(host, port, user, password):
    interface = pyipmi.interfaces.create_interface('rmcp',
                                                slave_address=0x81,
                                                host_target_address=0x20,
                                                keep_alive_interval=0)
    ipmi = pyipmi.create_connection(interface)
    ipmi.session.set_session_type_rmcp(host, port)
    ipmi.session.set_auth_type_user(user, password)
    ipmi.session.establish()
    ipmi.target = pyipmi.Target(ipmb_address=0x20)
    return ipmi

def chassisStatus(host,port,user,password):
    try:
        ipmi = createSession(host, port, user, password)
    except socket.timeout as e:
        raise e
    chassis_stat = ipmi.get_chassis_status()
    ipmi.session.close()
    status = {}
    for i in ['power_on', 'overload', 'interlock', 'fault', 'control_fault', 'restore_policy']:
        status[i] = chassis_stat.__dict__[i]
    status['last_event'] = chassis_stat.last_event[-1]
    for i in ['intrusion', 'front_panel_lockout', 'drive_fault', 'cooling_fault']:
        status[i] = i in chassis_stat.chassis_state
    return status

def chassisCommand(host, port, user, password, command: int):
    """
        Send chassis command to host:port using user and password as authentication.
        command is an integer, with the following mapping:
        {
        0: 'CONTROL_POWER_DOWN',
        1: 'CONTROL_POWER_UP',
        2: 'CONTROL_POWER_CYCLE',
        3: 'CONTROL_HARD_RESET',
        4: 'CONTROL_DIAGNOSTIC_INTERRUPT',
        5: 'CONTROL_SOFT_SHUTDOWN',
        }
    """
    try:
        ipmi = createSession(host, port, user, password)
    except socket.timeout as e:
        raise e
    ipmi.chassis_control(command)