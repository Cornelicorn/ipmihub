def restore_int_to_str(restore_policy: int):
    dict = {
        0: 'Always off',
        1: 'Last state',
        2: 'Always on',
    }
    return dict[restore_policy]

def last_event_str_converter(last_event):
    dict = {
        'ac_failed': 'Power failure',
        'overload': 'Power overload',
        'interlock': 'Power interlock',
        'fault': 'Power fault',
        'power_on_via_ipmi': 'Powered on via IPMI',
    }
    return dict[last_event]