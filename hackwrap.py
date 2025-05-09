"""A powerful decorator-based module to "hack" Python functions and classes — inject, modify, or protect behavior dynamically."""

import weakref as _weakref, threading as _threading, inspect as _inspect, functools as _functools, typing as _typing, ast as _ast, asyncio as _asnco, warnings as _warnings, builtins as _builtins, types as _types, collections.abc as _abc
from typing import Callable as _Callable, Literal as _Literal, Union as _Union, Any as _Any
from types import ModuleType as _ModuleType

class __FunctionLike:
        """The main class for the this global refrence"""
        def __init__(self, func):
            """The main class for the this global refrence"""
            self.__func = func

        @property
        def params(self):
            args = []
            for name, param in _inspect.signature(self.__func).parameters.items():
                args.append({'name': f'*{name}' if param.kind == param.VAR_POSITIONAL else f'**{name}' if param.kind == param.VAR_KEYWORD else name, 'annottype': param.annotation, 'value': param.default})
            return args
        
        @property
        def local(self): return self.__func.__name__  in locals()

        @property
        def indent(self): return len(_inspect.getsourcelines(self.__func)[0][0]) - len(_inspect.getsourcelines(self.__func)[0][0].lstrip())

        @property
        def func(self): return self.__func

        @property
        def sourcelines(self): return _inspect.getsourcelines(self.__func)

        @property
        def signature(self): return _inspect.signature(self.__func)

        @property
        def annottype(self): return _typing.get_type_hints(self.__func).get('return')

        @property
        def typehints(self): return _typing.get_type_hints()

        @property
        def wrappers(self):
            for node in _ast.walk(_ast.parse(''.join(_inspect.getsourcelines(self.__func)[0]))):
                if isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef)) and node.name.replace('_', '') == self.__func.__name__.replace('_', ''):
                    return [_ast.unparse(wrapper) for wrapper in node.decorator_list]
            return []
        
        @property
        def locals(self) -> dict[str, _Any]: return _inspect.currentframe(self.__func).f_locals

this = __FunctionLike(lambda: None)

def update_this(func: _Callable):
    """Decorator that updates the global 'this' reference to a function."""
    global this
    this = __FunctionLike(func)
    return func

def inherit(inherited: _Callable, returned: _Literal['function', 'inherited', 'both'] = 'function') -> _Callable:
    """Decorator that inherits from a function and controls what will be returned"""
    def decorator(func: _Callable) -> _Callable:
        def wrapper(*args, **kwargs):
            i, f = inherited(*args, **kwargs), func(*args, **kwargs)
            if returned == 'function': return f
            elif returned == 'inherited': return i
            elif returned == 'both': return f, i
        return wrapper
    return decorator

def classinherit(subclass: type, init: bool = True):
    """Decorator that inherits all attributes from an object or a type."""
    def decorator(func: _Callable):
        class InheritedClass(subclass):...
        return InheritedClass() if init else InheritedClass
    return decorator

def varinherit(var):
    """Decorator that makes the function return a specific variable when called"""
    def wrapper(func: _Callable): return lambda *args, **kwargs: var
    return wrapper

def moduleinherit(module: _ModuleType):
    """Decorator that makes a function inherit some attributes from a `ModuleType`"""
    def wrapper(func: _Callable):
        for name in dir(module):
            try: setattr(func, name, getattr(module, name))
            except:...
        return func
    return wrapper

def uncallable(func: _Callable): """Decorator that makes a function unusable"""

def undeletable(func: _Callable) -> _Callable:
    """Decorator that makes a function undeletable even when using the del keyword"""
    original = func
    _backup_store = _weakref.WeakValueDictionary()
    _backup_store[original.__name__] = original
    class Undeletable:
        def __call__(self, *args, **kwargs): return original(*args, **kwargs)
        def __del__(self):
            try:
                frame = _inspect.currentframe()
                if frame is not None and frame.f_back is not None:
                    if original.__name__ in _backup_store:
                        frame.f_back.f_globals[original.__name__] = _backup_store[original.__name__]
                    frame.f_back.f_globals[original.__name__] = undeletable(original)
            except (AttributeError, TypeError):
                pass
    for attr in ('__module__', '__name__', '__qualname__', '__doc__', '__annotations__'):
        if hasattr(original, attr): setattr(Undeletable, attr, getattr(original, attr))
    return Undeletable()


def threadify(func: _Callable):
    """Decorator that threads a function automatically when called."""
    def threader(*args, **kwargs):
        _threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True).start()
    return threader

def endless(func: _Callable):
    """Decorator that makes a function endless **if it ends**."""
    def forever(*args, **kwargs):
        func(*args, **kwargs)
        while True:...
    return forever

def private(func: _Callable) -> _Callable:
    """Decorator that makes a function private even if it isn't **double underscored**."""
    original_module = _inspect.getmodule(func)
    @_functools.wraps(func)
    def wrapper(*args, **kwargs):
        caller_frame = _inspect.currentframe().f_back
        if caller_frame is None: raise RuntimeError("Private function called from unknown context")
        caller_module = _inspect.getmodule(caller_frame)
        if caller_module != original_module: raise NameError(f'name \'{wrapper.__name__}\' is not defined')
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    wrapper.__qualname__ = func.__qualname__
    return wrapper

def globe(func: _Callable):
    """Decorator that truly promotes a function to global scope"""
    _inspect.currentframe().f_back.f_globals[func.__name__] = func
    return func

def asnc(func: _Callable):
    """Decorator that turns a function from a normal to an asynced one"""
    @_functools.wraps(func)
    async def asnc_wrapper(*args, **kwargs): return await _asnco.get_running_loop().run_in_executor(None, lambda: func(*args, **kwargs))
    return asnc_wrapper

def snc(func: _Callable):
    """Decorator that makes asynced functions normal."""
    @_functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        try: loop = _asnco.get_running_loop()
        except RuntimeError: loop = None
        return _asnco.create_task(func(*args, **kwargs)) if loop and loop.is_running() else _asnco.run(func(*args, **kwargs))
    return sync_wrapper

def handle(on_error: _Callable[[_Union[Exception, Warning]], None] = lambda: None, on_else: _Callable[[], None] = lambda: None, after: _Callable[[], None] = lambda: None):
    """Decorator that handles a function, when an error or a warning occurs.. `on_error` is called, when nothing occurs.. `on_else` is called, whatever happens.. `after` is always called!"""
    def decorator(func: _Callable):
        @_functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                _warnings.simplefilter('error')
                result = func(*args, **kwargs)
            except (Exception, Warning) as e: on_error(e) if on_error.__code__.co_argcount else on_error()
            else:
                on_else()
                return result
            finally:
                _warnings.simplefilter('default')
                after()
        return wrapper
    return decorator

def public(func: _Callable):
    """Decorator that makes private functions `public`, even those that are **double underscored** at the beginning."""
    module = _inspect.getmodule(func)
    if module: module.__dict__[func.__name__] = func
    return func

def get_supported_var_dunders():
    """returns all supported magic methods for variable function"""
    sources = [_builtins, _types, _abc, _inspect, _threading, _ast, _asnco, _warnings, _weakref, _functools, _typing]
    dunders = set()
    for source in sources:
        for name, obj in vars(source).items():
            if _inspect.isclass(obj):
                for attr_name in dir(obj):
                    if attr_name.startswith("__") and attr_name.endswith("__"):
                        attr = getattr(obj, attr_name, None)
                        if callable(attr): dunders.add(attr_name)
    return sorted(dunders)

def onment(callback):
    class __UltimateWrapper:...
    def wrapper(func) -> __UltimateWrapper:
        class_definition = 'class __Ultimate:\n'
        for key in get_supported_var_dunders(): class_definition += f'    def {key}(self, *args, **kwargs):\n        return callback().{key}(*args, **kwargs)\n' if not key in ['__new__', '__init__', '__del__'] else ''
        namespace = {}
        exec(class_definition, {"callback": callback}, namespace)
        ult = namespace['__Ultimate']
        for attr in ('__module__', '__name__', '__qualname__', '__doc__', '__annotations__'):
            if hasattr(func, attr): setattr(ult, attr, getattr(func, attr))
        return ult()
    return wrapper
