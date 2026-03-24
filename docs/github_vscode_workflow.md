# GitHub + VS Code Workflow

## Repo name
`Visual-Assistive-Aid-Jetson-Orin-Nano-Oak`

## Branch strategy
- `main` = stable branch only
- create feature branches for all work

## First-time setup on your computer
```bash
git clone <your-repo-url>
cd Visual-Assistive-Aid-Jetson-Orin-Nano-Oak
code .
```

## Daily workflow
### Start work
```bash
git checkout main
git pull origin main
git checkout -b feature/<short-name>
```

### Save work
```bash
git add .
git commit -m "feat: short description"
git push -u origin feature/<short-name>
```

### After teammate work lands in main
```bash
git checkout main
git pull origin main
```

## Pull request rule
Before merging into `main`:
- code should run
- script should be tested on the intended machine
- commit message should explain the change

## VS Code recommendation
Use:
- Python extension
- GitHub Pull Requests extension
- Remote - SSH extension

## Best way to use VS Code with Jetson
Use Remote-SSH so you edit on your main computer but run code on the Jetson.
