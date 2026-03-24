# Contributing Guide

## Team rule
Never code directly on `main`.

## Branch flow
1. Pull latest `main`
2. Create a branch
3. Make changes
4. Commit
5. Push your branch
6. Open a pull request
7. Review and merge into `main`

## Commands you will use most
### Pull latest changes from GitHub
```bash
git pull origin main
```

### Create a new branch
```bash
git checkout -b feature/rgb-preview
```

### Check what changed
```bash
git status
```

### Stage files
```bash
git add .
```

### Commit changes
```bash
git commit -m "feat: add rgb preview test"
```

### Push branch to GitHub
```bash
git push -u origin feature/rgb-preview
```

### Switch back to main
```bash
git checkout main
```

### Update local main from GitHub
```bash
git pull origin main
```

### Merge a finished branch locally
```bash
git checkout main
git merge feature/rgb-preview
```

### Delete a merged local branch
```bash
git branch -d feature/rgb-preview
```

## Simple merge rule for your team
- Chase merges only after the branch runs.
- One person owns one feature branch at a time.
- Do not have both teammates editing the same file unless planned.
- If both people touch the same file, talk before merging.

## Conflict handling
If Git says there is a merge conflict:
1. Open the file in VS Code
2. Accept the right changes manually
3. Save the file
4. Run:
```bash
git add .
git commit -m "fix: resolve merge conflict"
```

## Recommended first split
- **Chase:** Jetson setup, repo setup, smoke tests
- **Teammate:** RGB/depth preview cleanup and first obstacle logic
