import { StackContext, Api, Function, use } from "sst/constructs";
import { Data } from "./Data";

export function API({ stack, app }: StackContext) {
  const customerPath = "packages/functions/src/customer/services";

  const functionMaker = (name: string, path: string) => {
    return { function: { functionName: `${name}-${app.stage}`, handler: `${path}.handler` } };
  };

  const { dynamoTable, bucket } = use(Data);

  const myAuthorizer = new Function(stack, "myAuthorizer", {
    functionName: `lambda-auth-${app.stage}`,
    handler: "packages/functions/src/auth/lambda.handler",
    environment: { ACCOUNT_ID: app.account },
    permissions: ["ssm:GetParameter"]
  });

  const api = new Api(stack, `api-${app.stage}`, {
    authorizers: {
      myAuthorizer: { type: "lambda", function: myAuthorizer }
    },
    defaults: {
      function: {
        environment: { DYNAMODB_TABLE_NAME: dynamoTable.tableName },
        bind: [dynamoTable]
      },
      authorizer: "myAuthorizer"
    },
    routes: {
      "POST /customers": functionMaker("createCustomer", `${customerPath}/create`),
      "GET /customers/{id}": functionMaker("getCustomerById", `${customerPath}/getById`),
      "GET /customers": functionMaker("getCustomers", `${customerPath}/getAll`),
      "PUT /customers/{id}": functionMaker("updateCustomer", `${customerPath}/update`),
      "DELETE /customers/{id}": functionMaker("deleteCustomer", `${customerPath}/delete`),
      "POST /customers/{id}/image": {
        function: {
          handler: `${customerPath}/uploadImage.handler`,
          functionName: `uploadImage-${app.stage}`,
          environment: { S3_BUCKET_NAME: bucket.bucketName },
          bind: [bucket],
          timeout: 60
        }
      }
    },
    cdk: {
      httpStages: [{ stageName: app.stage, autoDeploy: true }]
    }
  });

  myAuthorizer.addEnvironment("API_ID", api.httpApiId);

  stack.addOutputs({
    ApiEndpoint: api.url
  });
}
