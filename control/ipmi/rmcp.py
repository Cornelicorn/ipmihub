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

def sensorStatus(host, port, user, password):
    try:
        ipmi = createSession(host, port, user, password)
    except socket.timeout as e:
        raise e

    status = []
    iter_fct = None
    device_id = ipmi.get_device_id()
    if device_id.supports_function('sdr_repository'):
        iter_fct = ipmi.sdr_repository_entries
    elif device_id.supports_function('sensor'):
        iter_fct = ipmi.device_sdr_entries
    
    for s in iter_fct():
        try:
            number = None
            value = None
            states = None
            thresholds = None
            def thresholds_conv(sensor):
                thr = ipmi.get_sensor_thresholds(sensor.number)
                if thr is not None:
                    for thr_id, thr_val in thr.items():
                        thr[thr_id]=float(round(sensor.convert_sensor_raw_to_value(thr_val),4))
                return thr

            if s.type is pyipmi.sdr.SDR_TYPE_FULL_SENSOR_RECORD:
                (value, states) = ipmi.get_sensor_reading(s.number)
                number = s.number
                if value is not None:
                    value = float(round(s.convert_sensor_raw_to_value(value),4))
                thresholds = thresholds_conv(s)

            elif s.type is pyipmi.sdr.SDR_TYPE_COMPACT_SENSOR_RECORD:
                (value, states) = ipmi.get_sensor_reading(s.number)
                number = s.number

            status.append({
                'sensor_id': s.id,
                'raw_value': number if number else None,
                'sensor_name': s.device_id_string.decode('utf-8'),
                'value': value,
                'state': states if states else None,
                'thresholds': thresholds
                })
                
        except pyipmi.errors.CompletionCodeError as e:
            pass
    return status
