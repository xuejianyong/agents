# coding=utf-8
# Copyright 2018 The TFAgents Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Python RL Environment API."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import six

from tf_agents.environments import time_step as ts


@six.add_metaclass(abc.ABCMeta)
class Base(object):
  """Abstract base class for Python RL environments.

  Observations and valid actions are described with `ArraySpec`s, defined in
  the `specs` module.

  If the environment can run multiple steps at the same time and take a batched
  set of actions and return a batched set of observations, it should overwrite
  the property batched to True.
  """

  @property
  def batched(self):
    """Whether the Environment is batched or not.

    If the environment supports batched observations and actions, then overwrite
    this property to True.

    A batched environment takes in a batched set of actions and returns a
    batched set of observations. This means for all numpy arrays in the input
    and output nested structures, the first dimension is the batch size.

    When batched, the left-most dimension is not part of the action_spec
    or the observation_spec and correspond to the batch dimension.

    Returns:
      A boolean.
    """
    return False

  @property
  def batch_size(self):
    """The batch size of the environment.

    Returns:
      The batch size of the environment, or `None` if there is none.

    Raises:
      RuntimeError: If a subclass overrode batched to return True but did not
        override the batch_size property.
    """
    if self.batched:
      raise RuntimeError(
          'Environment %s marked itself as batched but did not override the '
          'batch_size property' % type(self))
    return None

  @abc.abstractmethod
  def reset(self):
    """Starts a new sequence and returns the first `TimeStep` of this sequence.

    Returns:
      A `TimeStep` namedtuple containing:
        step_type: A `StepType` of `FIRST`.
        reward: `None`, indicating the reward is undefined.
        discount: `None`, indicating the discount is undefined.
        observation: A NumPy array, or a nested dict, list or tuple of arrays
          corresponding to `observation_spec()`.
    """

  @abc.abstractmethod
  def step(self, action):
    """Updates the environment according to the action and returns a `TimeStep`.

    If the environment returned a `TimeStep` with `StepType.LAST` at the
    previous step, this call to `step` will start a new sequence and `action`
    will be ignored.

    This method will also start a new sequence if called after the environment
    has been constructed and `restart` has not been called. Again, in this case
    `action` will be ignored.

    Args:
      action: A NumPy array, or a nested dict, list or tuple of arrays
        corresponding to `action_spec()`.

    Returns:
      A `TimeStep` namedtuple containing:
        step_type: A `StepType` value.
        reward: A NumPy array, reward value for this timestep.
        discount: A NumPy array, discount in the range [0, 1].
        observation: A NumPy array, or a nested dict, list or tuple of arrays
          corresponding to `observation_spec()`.
    """

  @abc.abstractmethod
  def observation_spec(self):
    """Defines the observations provided by the environment.

    May use a subclass of `ArraySpec` that specifies additional properties such
    as min and max bounds on the values.

    Returns:
      An `ArraySpec`, or a nested dict, list or tuple of `ArraySpec`s.
    """

  @abc.abstractmethod
  def action_spec(self):
    """Defines the actions that should be provided to `step`.

    May use a subclass of `ArraySpec` that specifies additional properties such
    as min and max bounds on the values.

    Returns:
      An `ArraySpec`, or a nested dict, list or tuple of `ArraySpec`s.
    """

  def time_step_spec(self):
    """Describes the `TimeStep` fields returned by `step()`.

    Override this method to define an environment that uses non-standard values
    for any of the items returned by `step`. For example, an environment with
    array-valued rewards.

    Returns:
      A `TimeStep` namedtuple containing (possibly nested) `ArraySpec`s defining
      the step_type, reward, discount, and observation structure.
    """
    return ts.time_step_spec(self.observation_spec())

  def close(self):
    """Frees any resources used by the environment.

    Implement this method for an environment backed by an external process.

    This method be used directly

    ```python
    env = Env(...)
    # Use env.
    env.close()
    ```

    or via a context manager

    ```python
    with Env(...) as env:
      # Use env.
    ```
    """
    pass

  def __enter__(self):
    """Allows the environment to be used in a with-statement context."""
    return self

  def __exit__(self, unused_exception_type, unused_exc_value, unused_traceback):
    """Allows the environment to be used in a with-statement context."""
    self.close()

  def render(self, mode='rgb_array'):
    """Renders the environment.

    Args:
      mode: One of ['rgb_array', 'human']. Renders to an numpy array, or brings
        up a window where the environment can be visualized.
    Returns:
      An ndarray of shape [width, height, 3] denoting an RGB image if mode is
      `rgb_array`. Otherwise return nothing and render directly to a display
      window.
    Raises:
      NotImplementedError: If the environment does not support rendering.
    """
    del mode  # unused
    raise NotImplementedError('No rendering support.')
