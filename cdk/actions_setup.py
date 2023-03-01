from aws_cdk import (
    aws_iam as iam,
    aws_sqs as sqs,
    Duration,
    CfnOutput,
    Stack,
)
from constructs import Construct


class GithubActionSetupRole(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, env=kwargs.get("env"))

        self.stack_env = kwargs.get("stack_env")

        # Sample role https://www.eliasbrange.dev/posts/secure-aws-deploys-from-github-actions-with-oidc/
        github_action_oidc = iam.OpenIdConnectProvider(
            self,
            "GithubActionOIDC",
            url="https://token.actions.githubusercontent.com",
            client_ids=["sts.amazonaws.com"],
            thumbprints=["6938fd4d98bab03faadb97b34396831e3780aea1"],
        )

        github_action_role = iam.Role(
            self,
            "GithubActionSetUpRole" + self.stack_env,
            role_name="GithubActionSetUpRole" + self.stack_env,
            description="Github Action CI",
            assumed_by=iam.FederatedPrincipal(
                federated=github_action_oidc.open_id_connect_provider_arn,
                assume_role_action="sts:AssumeRoleWithWebIdentity",
                conditions={
                    "StringEquals": {
                        "token.actions.githubusercontent.com:sub": [
                            "repo:benoitngoh/aws-ckd:*",
                            "repo:benoitngoh/*",
                        ],
                        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
                    }
                },
            ),
        )

        action_statement = iam.PolicyDocument(
            assign_sids=True,
            statements=[
                iam.PolicyStatement(
                    actions=["sts:AssumeRole"],
                    resources=["*"],
                    effect=iam.Effect.ALLOW,
                )
            ],
        )
        github_action_role.attach_inline_policy(
            iam.Policy(self, "GithubActionsPolicy", document=action_statement)
        )

        role_arn = CfnOutput(self, "sad", value=github_action_role.role_arn)
