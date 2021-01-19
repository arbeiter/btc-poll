from aws_cdk import (
        core,
        aws_lambda as _lambda,
        aws_apigateway as apigw,
        aws_dynamodb as ddb,
    )


class MontecarloStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Defines an AWS Lambda resource
        base_lambda = _lambda.Function(
            self, 'BaseLambda',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='lambda-handler.handler',
        )
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
