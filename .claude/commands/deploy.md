Deploy notion_query to hk24 server (103.75.117.152).

Run the deploy script based on the user's argument: $ARGUMENTS

Available actions:
- `sync` (default): rsync code to hk24
- `setup`: sync code + install deps + start Qdrant
- `start`: start the FastAPI server
- `notion full`: run full Notion sync
- `notion incremental`: run incremental sync
- `notion discover`: list accessible Notion databases
- `status`: check Qdrant and API status on hk24
- `full`: complete deploy (sync + setup + notion sync + start API)

Execute: `./scripts/deploy.sh $ARGUMENTS`

If no argument is provided, default to `sync`.
