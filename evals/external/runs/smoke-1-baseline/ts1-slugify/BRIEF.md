Add an exported slugify function to slug.ts that lowercases, replaces any run of non alphanumeric characters with a single hyphen, and strips leading and trailing hyphens. Do not change check_slug.ts.

Allowed files: slug.ts
Check: node --experimental-strip-types --input-type=module -e "import './check_slug.ts'"
