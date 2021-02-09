from aws_cdk import (
        core,
        aws_lambda as _lambda,
        aws_apigateway as apigw,
        aws_dynamodb,
        aws_events,
        aws_events_targets
    )


class MontecarloStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create dynamo table
        metric_table = aws_dynamodb.Table(
            self, "metric_table",
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            )
        )
        # Defines an AWS Lambda resource
        base_lambda = _lambda.Function(
            self, 'BaseLambda',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'),
            handler='api_request_handler.handler',
        )
        base_lambda.add_environment("TABLE_NAME", metric_table.table_name)

        base_api = apigw.LambdaRestApi(
            self, 'MonteCarloApi',
            handler=base_lambda,
            rest_api_name='ApiGatewayWithCors')

        items = base_api.root.add_resource("metrics")
        items.add_method("GET")
        item = items.add_resource("{id}")
        item.add_method("GET")

        rank = base_api.root.add_resource("rank")
        rank_fetch = rank.add_resource("{id}")
        rank_fetch.add_method("GET")

        # create producer lambda function
        producer_lambda = _lambda.Function(self, "producer_lambda_function",
                                              runtime=_lambda.Runtime.PYTHON_3_8,
                                              handler="lambda_function.lambda_handler",
                                              code=_lambda.Code.asset("./lambda/producer"))

        producer_lambda.add_environment("TABLE_NAME", metric_table.table_name)

        # grant permission to lambda to write to demo table
        metric_table.grant_read_data(producer_lambda)
        metric_table.grant_write_data(producer_lambda)
        metric_table.grant_read_data(base_lambda)
        metric_table.grant_write_data(base_lambda)

        # create a Cloudwatch Event rule
        one_minute_rule = aws_events.Rule(
            self, "one_minute_rule",
            schedule=aws_events.Schedule.rate(core.Duration.minutes(20)),
        )
        # Add target to Cloudwatch Event
        one_minute_rule.add_target(aws_events_targets.LambdaFunction(producer_lambda))
