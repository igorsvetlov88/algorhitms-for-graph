import sys

state_log = []

def log_state(state):
    state_log.append(set(state))

def tracer(frame, event, arg):
    if event == 'line':
        local_vars = frame.f_locals.copy()
        state_log.append({
            'line': frame.f_lineno,
            'locals': local_vars
        })
    return tracer

def run_with_tracer(func, *args, **kwargs):
    sys.settrace(tracer)
    result = func(*args, **kwargs)
    sys.settrace(None)
    return result