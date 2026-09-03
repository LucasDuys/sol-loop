import { slugify } from "./slug.ts";
const cases: Array<[string, string]> = [["Hello,  World!", "hello-world"], ["  A--B__c  ", "a-b-c"], ["x", "x"]];
for (const [input, want] of cases) {
  const got = slugify(input);
  if (got !== want) throw new Error(`${input} -> ${got}, want ${want}`);
}
console.log("ts1 OK");
