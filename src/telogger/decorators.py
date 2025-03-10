from typing import Callable, Optional, Any
from functools import wraps
import time
from .utils import format_message
import asyncio

def monitor_start_stop(
    name: Optional[str] = None,
    telogger: Optional[Any] = None  # Add this parameter
):
    def decorator(func: Callable):
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            used_telogger = telogger or _get_telogger_instance(args)
            func_name = name or func.__name__
            
            if used_telogger:
                used_telogger.send_message(f"🚀 {func_name} started")
            result = func(*args, **kwargs)
            if used_telogger:
                used_telogger.send_message(f"✅ {func_name} finished")
            return result

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            used_telogger = telogger or _get_telogger_instance(args)
            func_name = name or func.__name__
            
            if used_telogger:
                if used_telogger.client.async_mode:
                    await used_telogger.client.send_message_async(f"🚀 {func_name} started")
                else:
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(
                        None, 
                        used_telogger.send_message, 
                        f"🚀 {func_name} started"
                    )
            
            result = await func(*args, **kwargs)
            
            if used_telogger:
                if used_telogger.client.async_mode:
                    await used_telogger.client.send_message_async(f"✅ {func_name} finished")
                else:
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(
                        None, 
                        used_telogger.send_message, 
                        f"✅ {func_name} finished"
                    )
            return result

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

def _get_telogger_instance(args) -> Optional[Any]:
    # Safely check if the first argument has a `telogger` attribute
    if args and hasattr(args[0], "telogger"):
        return args[0].telogger
    return None

def monitor(
    name: Optional[str] = None,
    level: str = "INFO",
    parse_mode: str = "HTML",
    telogger: Optional[Any] = None  # Add this parameter
):
    def decorator(func: Callable):
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.monotonic()
            # Use the explicitly provided telogger or try to infer it
            used_telogger = telogger or _get_telogger_instance(args)
            func_name = name or func.__name__
            
            if used_telogger:
                msg = format_message(f"{func_name} started", "START", parse_mode)
                used_telogger.send_message(msg)
            
            try:
                result = func(*args, **kwargs)
                duration = time.monotonic() - start_time
                
                if used_telogger:
                    msg = format_message(
                        f"{func_name} finished in {duration:.2f}s", 
                        "SUCCESS", 
                        parse_mode
                    )
                    used_telogger.send_message(msg)
                return result
            except Exception as e:
                if used_telogger:
                    msg = format_message(
                        f"{func_name} failed: {str(e)}", 
                        "ERROR", 
                        parse_mode
                    )
                    used_telogger.send_message(msg)
                raise

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.monotonic()
            used_telogger = telogger or _get_telogger_instance(args)
            func_name = name or func.__name__
            
            if used_telogger:
                msg = format_message(f"{func_name} started", "START", parse_mode)
                if used_telogger.client.async_mode:
                    await used_telogger.client.send_message_async(msg)
                else:
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(None, used_telogger.send_message, msg)
            
            try:
                result = await func(*args, **kwargs)
                duration = time.monotonic() - start_time
                
                if used_telogger:
                    msg = format_message(
                        f"{func_name} finished in {duration:.2f}s", 
                        "SUCCESS", 
                        parse_mode
                    )
                    if used_telogger.client.async_mode:
                        await used_telogger.client.send_message_async(msg)
                    else:
                        loop = asyncio.get_event_loop()
                        await loop.run_in_executor(None, used_telogger.send_message, msg)
                return result
            except Exception as e:
                if used_telogger:
                    msg = format_message(
                        f"{func_name} failed: {str(e)}", 
                        "ERROR", 
                        parse_mode
                    )
                    if used_telogger.client.async_mode:
                        await used_telogger.client.send_message_async(msg)
                    else:
                        loop = asyncio.get_event_loop()
                        await loop.run_in_executor(None, used_telogger.send_message, msg)
                raise

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator