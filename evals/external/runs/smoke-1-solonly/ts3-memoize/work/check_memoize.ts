import { memoize } from "./memoize.ts";
let calls = 0;
const f = memoize((x: number) => { calls += 1; return x * 2; });
if (f(2) !== 4 || f(2) !== 4 || f(3) !== 6) throw new Error("wrong values");
if (calls !== 2) throw new Error(`expected 2 calls, got ${calls}`);
console.log("ts3 OK");
