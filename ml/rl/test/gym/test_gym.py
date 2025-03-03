#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates. All rights reserved.
"""
Environments that require short training and evaluation time (<=10min)
can be tested in this file.
"""
import json
import logging
import random
import unittest

import numpy as np
import torch
from ml.rl.tensorboardX import SummaryWriterContext
from ml.rl.test.gym.run_gym import USE_CPU, run_gym


DQN_CARTPOLE_JSON = "ml/rl/test/gym/discrete_dqn_cartpole_v0.json"
CARTPOLE_SCORE_BAR = 150
SEED = 0


class TestGym(unittest.TestCase):
    def setUp(self):
        logging.getLogger().setLevel(logging.INFO)
        SummaryWriterContext._reset_globals()
        np.random.seed(SEED)
        torch.manual_seed(SEED)
        random.seed(SEED)

    def test_dqn_cartpole_offline(self):
        """ Test if the json config works for offline DQN in Cartpole """
        with open(DQN_CARTPOLE_JSON, "r") as f:
            params = json.load(f)
        reward_history, _, _, _, _ = run_gym(
            params,
            offline_train=True,
            score_bar=CARTPOLE_SCORE_BAR,
            gpu_id=USE_CPU,
            seed=SEED,
        )
        assert reward_history[-1] >= CARTPOLE_SCORE_BAR

    def test_dqn_cartpole_online(self):
        """ Test if the json config works for online DQN in Cartpole """
        with open(DQN_CARTPOLE_JSON, "r") as f:
            params = json.load(f)
        reward_history, _, _, _, _ = run_gym(
            params,
            offline_train=False,
            score_bar=CARTPOLE_SCORE_BAR,
            gpu_id=USE_CPU,
            seed=SEED,
        )
        assert reward_history[-1] > CARTPOLE_SCORE_BAR
