#!/usr/bin/env python3

from aws_cdk import core

from montecarlo.montecarlo_stack import MontecarloStack


app = core.App()
MontecarloStack(app, "montecarlo", env={'region': 'us-east-2'})

app.synth()
