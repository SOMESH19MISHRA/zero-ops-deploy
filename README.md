# zero-ops-deploy

A CLI tool that scans a codebase, detects its stack, and auto-generates a working Dockerfile, GitHub Actions CI/CD workflow, and EC2 deploy script — the setup I hand-built three times across my Docker, CI/CD, and AWS deployment projects, now automated.

## What it does

Point it at any repo:
```bash
zero-ops-deploy --path /path/to/repo --docker-username yourname --image-name yourapp
```

It detects the stack and generates three files:
- `Dockerfile`
- `.github/workflows/docker-build-push.yml`
- `deploy.sh`

## Supported stacks (v1)

| Stack | Detected by |
|---|---|
| Flask | `requirements.txt` containing "flask" |
| Plain Python script | `requirements.txt` without Flask |
| Express | `package.json` containing "express" as a dependency |
| Static site | `index.html` at repo root, no backend files |

Anything else returns `"unknown"` rather than guessing or crashing.

## Architecture

The tool is built as four independent pieces, each answering exactly one question:

```
User runs: zero-ops-deploy --path . --docker-username X --image-name Y
        ↓
   cli.py (orchestrator)
        ↓
   detector.py → detect_stack(path) → returns "flask" / "express" / "python-script" / "static" / "unknown"
        ↓
   generators/dockerfile.py    → generate_dockerfile(stack)                → Dockerfile text
   generators/workflow.py      → generate_workflow(user, image)            → GitHub Actions YAML text
   generators/deploy_script.py → generate_deploy_script(user, image, port) → bash script text
        ↓
   cli.py writes all three outputs to real files in the target repo
```

**Why it's structured this way:** each generator is a pure function — same input always produces the same output, and none of them touch the filesystem directly. `detector.py` only inspects, never writes. `cli.py` is the only file that has side effects (writing files, printing output) — everything risky is isolated in one place, and everything else is trivially testable in a Python shell with a single `print()` call.

## How each piece was validated

- `detector.py` — tested against a real project (`containerized-app-deploy`, correctly returned `"flask"`) and against fake `express`/`static`/`unknown` fixtures
- `generators/*` — each tested by printing output and comparing against the hand-written Dockerfile/YAML/deploy script from my earlier Docker, CI/CD, and AWS projects
- `cli.py` — tested end-to-end, writing real files to a fresh test folder
- **End-to-end proof:** ran the tool cold against [heroku/flow-demo](https://github.com/heroku/flow-demo), an Express app I'd never seen before. It correctly detected `"express"` and generated a Dockerfile that **built successfully with `docker build`**, no manual edits.

## Known limitations (v1, honestly)

- `python-script` stack assumes the entry file is named `app.py`
- No detection of the actual port an app listens on — deploy script defaults to a fixed port, which may not match apps that read `PORT` from an environment variable
- Doesn't check for an existing `.github/workflows/` before writing — will overwrite an existing pipeline
- `deploy.sh` assumes an EC2 instance already exists and is meant to be run **on** that instance (e.g. via SSH) — it installs Docker and runs the container, but does not provision the EC2 instance itself, configure security groups, or touch AWS in any way
- Static sites don't get a CI/CD workflow or deploy script tailored differently from other stacks (out of scope for v1)

## Install (local, from source)

```bash
git clone https://github.com/SOMESH19MISHRA/zero-ops-deploy
cd zero-ops-deploy
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Why I built this

After building three separate DevOps projects by hand — containerizing an app with Docker, automating it with GitHub Actions, deploying it to AWS EC2 — I wanted to go one level deeper than "I can follow these steps" to "I understand this well enough to automate it." This tool encodes that manual process into something reusable.
