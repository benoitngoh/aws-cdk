#!/usr/bin/env python3
from aws_cdk import (
    App,
)

from cdk.actions_setup import GithubActionSetupRole


app = App()
env = {"region": "us-east-1", "account": "771500531194"}

github_action_setup = GithubActionSetupRole(
    app, "GithubActionSetupRole", env=env, stack_env="staging"
)


app.synth()
