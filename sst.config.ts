import { SSTConfig } from "sst";

export default {
  config(_input) {
    return {
      name: "assessment-cognits",
      region: process.env.AWS_REGION || "us-east-1"
    };
  },
  stacks(app) {
    app.setDefaultFunctionProps({ runtime: "python3.12" });
  }
} satisfies SSTConfig;
