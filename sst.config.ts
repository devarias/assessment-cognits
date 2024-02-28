import { SSTConfig } from "sst";
import { API } from "./stacks/Api";
import { Data } from "./stacks/Data";

export default {
  config(_input) {
    return {
      name: "assessment-cognits",
      region: process.env.AWS_REGION || "us-east-1"
    };
  },
  stacks(app) {
    app.setDefaultRemovalPolicy("destroy");
    app.setDefaultFunctionProps({ runtime: "python3.11" });
    app.stack(Data).stack(API);
  }
} satisfies SSTConfig;
