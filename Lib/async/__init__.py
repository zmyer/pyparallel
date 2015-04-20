import socket
HOSTNAME = socket.gethostname().encode('utf-8')
IPADDR = socket.gethostbyname(HOSTNAME)

class Constant(dict):
    def __init__(self):
        items = self.__class__.__dict__.items()
        for (key, value) in filter(lambda t: t[0][:2] != '__', items):
            try:
                self[value] = key
            except:
                pass
    def __getattr__(self, name):
        return self.__getitem__(name)
    def __setattr__(self, name, value):
        return self.__setitem__(name, value)

class _CachingBehavior(Constant):
    Default         = 0
    Buffered        = 1
    RandomAccess    = 2
    SequentialScan  = 3
    WriteThrough    = 4
    Temporary       = 5
CachingBehavior = _CachingBehavior()

_dict = dict
_list = list
_object = object

# Wrap this in a try/except handler such that we can suppress import errors;
# useful if we're using a normal Python interpreter and we want to import some
# of the other async.* classes.
try:
    import _async
    from _async import *
except ImportError:
    pass

class object:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)
        _async.protect(self)

def call_from_main_thread_and_wait(f):
    def decorator(*_args, **_kwds):
        return _async.call_from_main_thread_and_wait(f, _args, _kwds)
    return decorator

def call_from_main_thread(f):
    def decorator(*_args, **_kwds):
        _async.call_from_main_thread(f, _args, _kwds)
    return decorator

def synchronized(f):
    cs = _async.critical_section()
    def decorator(*_args, **_kwds):
        class _cs_wrap:
            def __enter__(self):
                cs.enter()
            def __exit__(self, *exc):
                cs.leave()
        with _cs_wrap() as _cs:
            return f(*_args, **_kwds)
    return decorator

def submit_work(func, args=None, kwds=None, callback=None, errback=None):
    _async.submit_work(func, args, kwds, callback, errback)

def submit_wait(obj, func=None, args=None, kwds=None,
                callback=None, errback=None, timeout=None):
    _async.submit_wait(obj, timeout, func, args, kwds, callback, errback)

#def submit_write_io(writeiofunc, buf, callback=None, errback=None):
#    _async.submit_write_io(writeiofunc, buf, callback, errback)

#def submit_read_io(readiofunc, callback, nbytes=0, errback=None):
#    _async.submit_read_io(readiofunc, nbytes, callback, errback)

_open = open
def open(filename, mode, caching=0, size=0, template=None):
    def open_decorator(f):
        def decorator(name, mode, fileobj):
            return f(caching, size, template, name, mode, fileobj)
        return decorator

    @open_decorator
    def fileopener(caching, size, template, name, mode, fileobj):
        return _async.fileopener(caching, size, template, name, mode, fileobj)

    f = _open(
        filename,
        mode=mode,
        opener=fileopener,
        closer=_async.filecloser
    )
    r = _async._rawfile(f)
    p = _async.protect(r)
    return p
_async_open = open

def close(obj):
    _async._close(obj)
    obj.close()

def write(obj, buf, callback=None, errback=None):
    _async.submit_write_io(obj, buf, callback, errback)

def writefile(filename, buf, callback=None, errback=None):
    f = open(filename, 'wb', size=len(buf))
    _async.submit_write_io(f, buf, callback, errback)
    f.close()

def read(obj, callback, nbytes=0, errback=None):
    _async.submit_read_io(obj.write, buf, callback, errback)

def prewait(obj=None):
    if obj is None:
        obj = object()
    return _async.prewait(obj)

def pipe(reader, writer, bufsize=0, callback=None, errback=None):
    raise NotImplementedError

def wait_any(waits):
    raise NotImplementedError

def wait_all(waits):
    raise NotImplementedError

def sendfile(transport=None, before=None, filename=None, after=None):
    if not transport:
        raise ValueError("transport can not be None")
    if not filename:
        raise ValueError("filename can not be None")
    return transport.sendfile(before, filename, after)

QOTD = b'An apple a day keeps the doctor away.\r\n'

class Protocol:
    line_mode = False
    initial_bytes_to_send = None
    def connection_made(self, transport, data):
        pass

    def connection_closed(self, transport, op):
        pass

    def connection_lost(self, transport, op):
        pass

    def connection_timeout(self, transport, op):
        pass

    def connection_error(self, transport, op, syscall, errcode):
        pass

    def data_received(self, transport, data):
        pass

    def line_received(self, transport, line):
        pass

    def data_sent(self, transport, data):
        pass

    def send_failed(self, transport, data):
        pass

    def exception_handler(self, transport, exc):
        pass

class ChattyLineProtocol:
    line_mode = False
    max_line_length = 100
    wait_for_eol = True
    def connection_made(self, transport):
        _async.stdout("connection_made\n")

    def connection_closed(self, transport, op):
        _async.stdout("connection_closed: %d\n" % op)

    def connection_lost(self, transport, op):
        _async.stderr("connection_lost: %d\n" % op)

    def connection_timeout(self, transport, op):
        _async.stderr("connection_lost: %d\n" % op)

    def connection_error(self, transport, op, syscall, errcode):
        _async.stderr("connection_error: %d, %s, %d\n" % op)

    def data_received(self, transport, data):
        _async.stdout("data_received\n")
        _async.stdout(data)
        _async.stdout("\n")

    def line_received(self, transport, line):
        _async.stdout("line_received: %s\n" % line)

    def data_sent(self, transport, data):
        _async.stdout("data_sent: %s\n" % data)

    def send_failed(self, transport, data):
        _async.stderr("send_failed: %s\n", data)

    def initial_connection_error(self, transport, errcode):
        _async.stderr("initial_connection_error: %d\n" % errcode)

    def __exception_handler(self, transport, syscall, exc):
        _async.stderr("exception_handler: %s\n" % repr(exc))

# Server will be one of two types: it either sends data first, or it expects
# the client to send data first (then presumably reacts to sent data).  The
# type is determined by the values of the attributes ``initial_bytes_to_send``
# and the ``expect_*`` ones.

class EchoServer:
    def data_received(self, data):
        return data

class QOTD:
    initial_bytes_to_send = QOTD

class BaseChargen:
    def __init__(self):
        self._lineno = -1

    @property
    def lineno(self):
        self._lineno += 1
        return self._lineno

    def chargen(self):
        return chargen(self.lineno)

class Chargen(BaseChargen):
    def initial_bytes_to_send(self):
        return self.chargen()

    def data_sent(self, data):
        return self.chargen()

class ChargenBrute(BaseChargen):
    def connection_made(self, sock):
        async.call_next(self.connection_made)
        return self.chargen()

class Disconnect:
    def connection_made(self, sock):
        sock.disconnect()

class Discard:
    def data_received(self, data):
        pass

class EchoData:
    def data_received(self, data):
        return data

class EchoLine:
    line_mode = True
    def line_received(self, line):
        return line

#===============================================================================
# Misc
#===============================================================================
def socket_stats(s):
    return (
        ('sem_acquired', s.sem_acquired),
        ('sem_released', s.sem_released),
        ('sem_timeout', s.sem_timeout),
        ('sem_count', s.sem_count),
        ('sem_release_err', s.sem_release_err),

        ('num_children', s.num_children),
        ('accepts_posted', s.accepts_posted),
        ('retired_clients', s.retired_clients),
        ('fd_accept_count', s.fd_accept_count),
        ('clients_connected', s.clients_connected),
        ('clients_disconnecting', s.clients_disconnecting),
        ('num_accepts_to_post', s.num_accepts_to_post),
        ('total_clients_reused', s.total_clients_reused),
        ('total_clients_recycled', s.total_clients_recycled),
        ('target_accepts_posted', s.target_accepts_posted),
        ('client_connected_count', s.client_connected_count),
        ('total_accepts_attempted', s.total_accepts_attempted),
        ('negative_accepts_to_post_count', s.negative_accepts_to_post_count),

        ('recvbuf_size', s.recvbuf_size),
        ('sendbuf_size', s.sendbuf_size),

        ('send_id', s.send_id),
        ('recv_id', s.recv_id),

        ('ioloops', s.ioloops),
        ('last_thread_id', s.last_thread_id),
        ('this_thread_id', s.this_thread_id),

        ('num_bytes_just_sent', s.num_bytes_just_sent),
        ('num_bytes_just_received', s.num_bytes_just_received),

        ('total_bytes_sent', s.total_bytes_sent),
        ('total_bytes_received', s.total_bytes_received),
    )

def context_stats():
    return (
        ('active_hogs', active_hogs()),
        ('active_contexts', active_contexts()),
        ('active_io_loops', active_io_loops()),
        ('seh_eav_in_io_callback', seh_eav_in_io_callback()),
    )

def memory_stats():
    return (
        ('load', _async._memory_load),
        ('total_virtual', _async._memory_total_virtual),
        ('avail_virtual', _async._memory_avail_virtual),
        ('total_physical', _async._memory_total_physical),
        ('avail_physical', _async._memory_avail_physical),
        ('total_page_file', _async._memory_total_page_file),
        ('avail_page_file', _async._memory_avail_page_file),
    )

#===============================================================================
# Helpers during interactive testing/debugging
#===============================================================================
def _tefb_json():
    import techempower_frameworks_benchmark as tefb
    server = _async.server(IPADDR, 8080)
    _async.register(transport=server, protocol=tefb.JSONSerializationHttpServer)
    _async.run_once()
    return server


# vim:set ts=8 sw=4 sts=4 tw=78 et:
