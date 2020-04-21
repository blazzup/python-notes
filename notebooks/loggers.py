# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import logging


# %%
def logger_info(logger):
    return {
        'set level': logging.getLevelName(logger.level),
        'actual level': logging.getLevelName(logger.getEffectiveLevel()),
        'use parent handlers': logger.propagate,
        'own handlers': logger.handlers,
    }


def log(logger, x=1):
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')
    try:
        1 / x
    except ZeroDivisionError:
        logger.exception('exception')


# %% [markdown]
# ## Info
#
# This notebook must be run from start to end (Kernel -> Restart & Run All), since loggers are singletons.  Any re-runing of cells might give unexpected results (although figuring out what is going on could be a good exercise).

# %% [markdown]
# ## Root logger

# %%
root_logger = logging.getLogger('')  # get it by passing an empty string
logger_info(root_logger)

# %%
id(root_logger) == id(logging.root)

# %%
# Although its name is 'root', it cannot be fetched by using it. Use '' as above.
root_logger.name, id(root_logger) == id(logging.getLogger(root_logger.name))

# %%
# output is still present due to last resort handler which is activated if handlers list is empty
log(root_logger)

# %%
log(root_logger, x=0)  # exception log includes stack trace

# %% [markdown]
# ### Basic configuration
#
# Calling `basicConfig()` has effect only when handlers list is empty! In python 3.8, `force` argument was added to override.

# %%
logging.basicConfig(
    level='ERROR'
)
logger_info(root_logger)

# %%
log(root_logger)

# %%
# will not change anything
logging.basicConfig(
    level='INFO'
)
logger_info(root_logger)

# %%
log(root_logger)

# %%
root_logger.handlers = []  # allows for changing config, in this case: ERROR -> INFO
logging.basicConfig(
    level='INFO'
)
logger_info(root_logger)

# %%
log(root_logger)

# %% [markdown]
# ## Child loggers
#
# When created, the level and handlers of the parent (in this case root) will be used.

# %%
child_logger = logging.getLogger('child')
logger_info(child_logger)

# %%
log(child_logger)

# %% [markdown]
# ### Override level

# %%
child_logger.setLevel('WARNING')
logger_info(child_logger)

# %%
log(child_logger)

# %% [markdown]
# ### Prevent calling parent handlers

# %%
child_logger.propagate = False
logger_info(child_logger)

# %%
log(child_logger)  # since handlers list is empty again, last resort handler is activated

# %% [markdown]
# ### Disable logging
#
# Logging is disabled when `propagate = False` and handlers list contains a single `NullHandler`.  

# %%
child_logger.addHandler(logging.NullHandler())
logger_info(child_logger)

# %%
log(child_logger)  # now logging is completely disabled for this logger

# %% [markdown]
# ### Setup custom handler

# %%
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

handler = logging.StreamHandler()
handler.setLevel('CRITICAL')  # handler can have its own severity level
handler.setFormatter(formatter)

child_logger.addHandler(handler)

logger_info(child_logger)

# %%
log(child_logger)

# %% [markdown]
# ### Calling same setup again will create duplicate logs
#
# Handlers are appended to a list and each is called in turn.

# %%
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

handler = logging.StreamHandler()
handler.setLevel('CRITICAL')  # handler can have its own severity level
handler.setFormatter(formatter)

child_logger.addHandler(handler)

logger_info(child_logger)

# %%
log(child_logger)

# %% [markdown]
# ### Re-enable parent logging

# %%
child_logger.propagate = True
logger_info(child_logger)

# %%
log(child_logger)
