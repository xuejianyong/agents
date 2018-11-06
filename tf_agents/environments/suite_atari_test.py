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

"""Tests for third_party.py.tf_agents.environments.suite_atari."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import flags
from absl.testing import absltest

import numpy as np

from tf_agents.environments import atari_wrappers
from tf_agents.environments import py_environment
from tf_agents.environments import suite_atari

FLAGS = flags.FLAGS

# Atari ROMs are placed in atari_py.get_game_path('.')


class SuiteAtariTest(absltest.TestCase):

  def testGameName(self):
    name = suite_atari.game('Pong')
    self.assertEqual(name, 'PongNoFrameskip-v0')

  def testGameObsType(self):
    name = suite_atari.game('Pong', obs_type='ram')
    self.assertEqual(name, 'Pong-ramNoFrameskip-v0')

  def testGameMode(self):
    name = suite_atari.game('Pong', mode='Deterministic')
    self.assertEqual(name, 'PongDeterministic-v0')

  def testGameVersion(self):
    name = suite_atari.game('Pong', version='v4')
    self.assertEqual(name, 'PongNoFrameskip-v4')

  def testGameSetAll(self):
    name = suite_atari.game('Pong', 'ram', 'Deterministic', 'v4')
    self.assertEqual(name, 'Pong-ramDeterministic-v4')

  def testAtariEnvRegistered(self):
    env = suite_atari.load('Pong-v0')
    self.assertIsInstance(env, py_environment.Base)
    self.assertIsInstance(env, atari_wrappers.AtariTimeLimit)

  def testAtariObsSpecUnit8(self):
    env = suite_atari.load('Pong-v0')
    self.assertIsInstance(env, py_environment.Base)
    self.assertEqual(np.uint8, env.observation_spec().dtype)


if __name__ == '__main__':
  absltest.main()
