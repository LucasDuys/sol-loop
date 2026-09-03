Add an exported memoize function to memoize.ts that wraps a pure single argument function and caches results by argument. The wrapped function must be called at most once per distinct argument. Do not change check_memoize.ts.

Allowed files: memoize.ts
Check: node --experimental-strip-types --input-type=module -e "import './check_memoize.ts'"
