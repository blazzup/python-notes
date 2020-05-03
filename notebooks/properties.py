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

# %% [markdown]
# ## Usual declaration

# %%
class TestA:
    @property  # must be before @x.setter
    def x(self):
        print('Getting x')
        return self._x

    @x.setter
    def x(self, value):
        print('Setting x')
        self._x = value

    def info(self):
        return type(self.x)


# %%
# self._x is not initialized at the start
t = TestA()
try:
    t.x
except AttributeError as e:
    print(e)

# %%
t.x = 3.14

# %%
t.x

# %%
t.info()


# %% [markdown]
# ## Using @x.getter and @x.setter

# %%
class TestB:
    x = property()

    @x.getter
    def x(self):
        print('Getting x')
        return self._x

    @x.setter
    def x(self, value):
        print('Setting x')
        self._x = value


# %%
t = TestB()

# %%
t.x = 3.14

# %%
t.x


# %% [markdown]
# ## Without decorators

# %%
class TestC:

    def get_x(self):
        print('Getting x')
        return self._x

    def set_x(self, value):
        print('Setting x')
        self._x = value

    x = property(fget=get_x, fset=set_x)  # must be after the functions, function names can be arbitrary


# %%
t = TestC()

# %%
t.x = 3.14

# %%
t.x
