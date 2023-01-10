#!/usr/bin/env python
# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2021 Comet ML INC
#  This file can not be copied and/or distributed without
#  the express permission of Comet ML Inc.
# *******************************************************
import comet_ml

import gymnasium as gym


class CometLogger(gym.Wrapper):
    """
    Gymnasium Wrapper that logs the step length and cumulative reward for an episode to Comet

    Parameters
    ----------
    env : gymnasium.Env
        gymnasium environment
    experiment : comet_ml.Experiment
        Experiment object from Comet
    """

    def __init__(self, env: gym.Env, experiment: comet_ml.Experiment):
        super().__init__(env)
        self.experiment = experiment
        self.experiment.log_other("Created from", "gymnasium")
        self._episode_counter = 0
        self._step_counter = 0

        if self._continued():
            self._reload_counters()

    def reset(self, **kwargs):
        """Reset the environment using kwargs. Resets length and reward counters and increments episode counter"""
        obs, info = super().reset(**kwargs)
        self._episode_reward = 0
        self._episode_length = 0
        self._episode_counter += 1
        return obs, info

    def step(self, action):
        """Steps through the environment using action"""
        observation, reward, terminated, truncated, info = self.env.step(action)

        self._episode_reward += reward
        self._episode_length += 1
        self._step_counter += 1

        if terminated or truncated:
            self._log_metrics()

        return observation, reward, terminated, truncated, info

    def _log_metrics(self):
        self.experiment.log_metric(
            "episode_reward",
            self._episode_reward,
            step=self._step_counter,
            epoch=self._episode_counter,
        )
        self.experiment.log_metric(
            "episode_length",
            self._episode_length,
            step=self._step_counter,
            epoch=self._episode_counter,
        )

    @property
    def episode_counter(self):
        """Number of episodes that have passed. Updated after env.reset() is called"""
        return self._episode_counter

    @property
    def step_counter(self):
        """Number of times env.step() has been called"""
        return self._step_counter

    def _continued(self):
        return isinstance(self.experiment, comet_ml.ExistingExperiment)

    def _reload_counters(self):
        exp_key = self.experiment.get_key()
        api_exp = comet_ml.APIExperiment(previous_experiment=exp_key)
        self._episode_counter = api_exp.get_metrics("episode_reward")[-1]["epoch"]
        self._step_counter = api_exp.get_metrics_summary("episode_reward")[
            "stepCurrent"
        ]

    def close(self):
        """
        If the environment is wrapped by RecordVideo Wrapper env.close() will
        log the video files to Comet.
        """
        env = self.env
        while env is not env.unwrapped:
            if isinstance(env, gym.wrappers.RecordVideo):
                self.experiment.log_asset_folder(env.video_folder)
                break

            env = env.env
        return super().close()
