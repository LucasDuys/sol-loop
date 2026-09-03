import { unique } from "./unique.ts";
const got = unique([3, 1, 3, 2, 1]);
if (JSON.stringify(got) !== JSON.stringify([3, 1, 2])) throw new Error(`got ${JSON.stringify(got)}`);
if (unique([]).length !== 0) throw new Error("empty failed");
console.log("ts2 OK");
