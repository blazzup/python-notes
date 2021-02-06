# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.8.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

current_time = None  # for tracking elapsed time


# %% [markdown]
# # Helper functions

# %%
def print_with_elapsed_time(msg: str):
    global current_time
    """Print message and elapsed seconds since current_time was reset."""
    print(f'{time.perf_counter() - current_time:.1f}s: {msg}')


def run(func):
    """Run async function in existing (Jupyter) or a new loop."""
    global current_time
    current_time = time.perf_counter()
    print(f'\n--------- running {func.__name__} ---------')
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(func())
    else:
        loop.run_until_complete(func())


# %% [markdown]
# # Single async task

# %%
async def async_work_1():
    print_with_elapsed_time("Starting A")
    await asyncio.sleep(1)
    print_with_elapsed_time("Finished A")


# %%
run(async_work_1)


# %% [markdown]
# # Single async task with result

# %%
async def async_work_2(n: float):
    print_with_elapsed_time(f"Starting B with n={n}")
    await asyncio.sleep(1)
    print_with_elapsed_time(f"Finished B with n={n}")
    return n


async def task_with_result():
    result = await async_work_2(n=100)
    print_with_elapsed_time(f'result={result}')


# %%
run(task_with_result)


# %% [markdown]
# # Multiple async tasks with results
#
# Use `asyncio.gather()` to run tasks in parallel.

# %%
async def multiple_tasks_with_results():
    result = await asyncio.gather(
        async_work_1(),
        async_work_2(n=100),
        async_work_2(n=200)
    )
    print_with_elapsed_time(f'result={result}')


# %%
run(multiple_tasks_with_results)


# %% [markdown]
# # Task which includes blocking call
#
# `work_1()` will delay the whole processing for 1.5s,
# since it uses blocking `time.sleep()` call.  
# The timing will depend on the order of `asyncio.gather()` parameters.

# %%
def work_1(n: int):
    print_with_elapsed_time(f"Starting blocking work with n={n}")
    time.sleep(1.5)
    print_with_elapsed_time(f"Finished blocking work with n={n}")
    return n


async def async_work_3(n: int):
    print_with_elapsed_time("Starting C")
    work_1(n)
    print_with_elapsed_time("Finished C")


async def blocking_task():
    result = await asyncio.gather(
        async_work_3(n=100),
        async_work_1(),
        async_work_2(n=200)
    )
    print_with_elapsed_time(f'result={result}')


# %%
run(blocking_task)


# %% [markdown]
# # Convert blocking function into non-blocking
#
# Use `run_in_executor()` to convert blocking into non-blocking tasks:
# - I/O-bound tasks should be run on `ThreadPoolExecutor`
# - CPU-bound tasks should be run on `ProcessPoolExecutor` (to avoid GIL limitations)

# %%
async def async_work_4(n: int, executor):
    print_with_elapsed_time("Starting D")
    loop = asyncio.get_running_loop()
    if executor is None:
        result = await loop.run_in_executor(None, work_1, n)  # default executor
    else:
        with executor() as pool:
            result = await loop.run_in_executor(pool, work_1, n)
    print_with_elapsed_time("Finished D")
    return result


async def blocking_task_on_default_executor():
    result = await asyncio.gather(
        async_work_4(100, executor=None),
        async_work_1(),
        async_work_2(n=200)
    )
    print_with_elapsed_time(f'result={result}')


async def blocking_task_on_thread_executor():
    result = await asyncio.gather(
        async_work_4(100, executor=ThreadPoolExecutor),
        async_work_1(),
        async_work_2(n=200)
    )
    print_with_elapsed_time(f'result={result}')


async def blocking_task_on_process_executor():
    result = await asyncio.gather(
        async_work_4(100, executor=ProcessPoolExecutor),
        async_work_1(),
        async_work_2(n=200)
    )
    print_with_elapsed_time(f'result={result}')


# %%
run(blocking_task_on_default_executor)

# %%
run(blocking_task_on_thread_executor)

# %%
run(blocking_task_on_process_executor)
