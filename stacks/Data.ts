import { Duration } from "aws-cdk-lib/core";
import { StackContext, Table, Bucket } from "sst/constructs";

export function Data({ stack, app }: StackContext) {
  const dynamoTable = new Table(stack, `Customers-${app.stage}`, {
    fields: {
      customerId: "string",
      firstName: "string",
      lastName: "string",
      postalCode: "string",
      country: "string",
      city: "string",
      creationDate: "string",
      lastUpdate: "string"
    },
    primaryIndex: { partitionKey: "customerId" },
    globalIndexes: {
      postalCodeCountryIndex: { partitionKey: "postalCode", sortKey: "country" },
      countryCityIndex: { partitionKey: "country", sortKey: "city" }
    }
  });

  const bucket = new Bucket(stack, `assesment-bucket-${app.stage}`, {
    name: `assesments-${app.account}-${app.stage}`,
    cdk: { bucket: { lifecycleRules: [{ expiration: Duration.days(3) }], versioned: true } }
  });

  return { dynamoTable, bucket };
}
