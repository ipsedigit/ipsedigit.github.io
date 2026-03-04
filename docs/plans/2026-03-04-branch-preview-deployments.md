# Branch Preview Deployments Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Push to any branch `xyz` → homepage live at `https://ipsedigit.github.io/xyz/`. Delete branch → preview removed automatically.

**Architecture:** Switch GitHub Pages source from `docs/` on `main` to a `gh-pages` branch. Three workflows handle production deploy, preview deploy (on push), and preview cleanup (on branch delete). Jekyll is built manually in Actions using `--baseurl` override. The `JamesIves/github-pages-deploy-action@v4` action deploys into scoped subdirectories, so production and previews coexist without interfering.

**Tech Stack:** GitHub Actions, Jekyll (via `github-pages` gem), `JamesIves/github-pages-deploy-action@v4`, `ruby/setup-ruby@v1`

---

## Prerequisites (manual — do before running any workflow)

### Step 1: Create the `gh-pages` branch locally

```bash
git checkout --orphan gh-pages
git reset --hard
git commit --allow-empty -m "init gh-pages"
git push origin gh-pages
git checkout main
```

### Step 2: Change GitHub Pages source in repo settings

Go to: `https://github.com/ipsedigit/ipsedigit.github.io/settings/pages`

- Source: **Deploy from a branch**
- Branch: **gh-pages** / **/ (root)**
- Save

> The site will temporarily show a blank page until the production deploy workflow runs for the first time (next step).

---

## Task 1: Production deploy workflow

**Files:**
- Create: `.github/workflows/deploy-production.yml`

**Step 1: Create the file**

```yaml
name: Deploy Production

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.1'
          bundler-cache: true
          working-directory: docs

      - name: Build Jekyll
        run: |
          cd docs
          bundle exec jekyll build --baseurl "" -d ../_site

      - name: Deploy to gh-pages root
        uses: JamesIves/github-pages-deploy-action@v4
        with:
          branch: gh-pages
          folder: _site
          clean: true
          clean-exclude: |
            **/
```

> `clean-exclude: **/` tells the action to clean only root-level files, not subdirectories — so preview folders survive a production deploy.

**Step 2: Commit and push**

```bash
git add .github/workflows/deploy-production.yml
git commit -m "ci: add production deploy workflow"
git push origin main
```

**Step 3: Verify**

- Go to `https://github.com/ipsedigit/ipsedigit.github.io/actions`
- The `Deploy Production` workflow should run and pass
- Visit `https://ipsedigit.github.io/` — site should load as before

---

## Task 2: Preview deploy workflow

**Files:**
- Create: `.github/workflows/deploy-preview.yml`

**Step 1: Create the file**

```yaml
name: Deploy Preview

on:
  push:
    branches-ignore:
      - main
      - gh-pages

jobs:
  deploy:
    runs-on: ubuntu-latest
    # Skip if this push was made by the Actions bot (prevents loops)
    if: github.actor != 'github-actions[bot]'
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Sanitize branch name
        run: |
          BRANCH=$(echo "${{ github.ref_name }}" | tr '/' '-' | tr '_' '-' | tr '[:upper:]' '[:lower:]')
          echo "BRANCH=$BRANCH" >> $GITHUB_ENV

      - name: Set up Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.1'
          bundler-cache: true
          working-directory: docs

      - name: Build Jekyll
        run: |
          cd docs
          bundle exec jekyll build --baseurl "/${{ env.BRANCH }}" -d ../_site

      - name: Deploy to gh-pages subdirectory
        uses: JamesIves/github-pages-deploy-action@v4
        with:
          branch: gh-pages
          folder: _site
          target-folder: ${{ env.BRANCH }}
          clean: true
```

**Step 2: Commit and push**

```bash
git add .github/workflows/deploy-preview.yml
git commit -m "ci: add preview deploy workflow"
git push origin main
```

**Step 3: Verify**

Create a test branch and push it:

```bash
git checkout -b test-preview
git push origin test-preview
```

- Go to Actions — `Deploy Preview` workflow should run and pass
- Visit `https://ipsedigit.github.io/test-preview/` — homepage should appear with styles intact

---

## Task 3: Preview cleanup workflow

**Files:**
- Create: `.github/workflows/cleanup-preview.yml`

**Step 1: Create the file**

```yaml
name: Cleanup Preview

on:
  delete:
    branches:

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout gh-pages
        uses: actions/checkout@v4
        with:
          ref: gh-pages

      - name: Sanitize branch name
        run: |
          BRANCH=$(echo "${{ github.event.ref }}" | tr '/' '-' | tr '_' '-' | tr '[:upper:]' '[:lower:]')
          echo "BRANCH=$BRANCH" >> $GITHUB_ENV

      - name: Remove preview directory
        run: |
          if [ -d "${{ env.BRANCH }}" ]; then
            git config user.name "github-actions[bot]"
            git config user.email "github-actions[bot]@users.noreply.github.com"
            git rm -r "${{ env.BRANCH }}"
            git commit -m "cleanup: remove preview ${{ env.BRANCH }}"
            git push origin gh-pages
          else
            echo "No preview directory found for ${{ env.BRANCH }}, nothing to clean."
          fi
```

**Step 2: Commit and push**

```bash
git add .github/workflows/cleanup-preview.yml
git commit -m "ci: add preview cleanup workflow"
git push origin main
```

**Step 3: Verify**

Delete the test branch created in Task 2:

```bash
git push origin --delete test-preview
git branch -d test-preview
```

- Go to Actions — `Cleanup Preview` workflow should run and pass
- Visit `https://ipsedigit.github.io/test-preview/` — should return 404

---

## Task 4: Disable GitHub Pages auto-build (prevent conflicts)

GitHub Pages may still try to auto-build Jekyll from `docs/` on `main` alongside the new Actions-based build. Disable it by adding a `.nojekyll` file to the `gh-pages` branch root.

**Step 1: Add `.nojekyll` to production deploy**

The `JamesIves` action respects `.nojekyll` if present in the build output. Add it to `docs/`:

```bash
touch docs/.nojekyll
git add docs/.nojekyll
git commit -m "ci: disable Jekyll auto-build on gh-pages"
git push origin main
```

> This tells GitHub Pages not to run Jekyll on the `gh-pages` branch — our Actions workflows do the build instead.

---

## Notes

- **Branch naming:** Slashes and underscores in branch names are normalized to hyphens. `feature/new-home` becomes `https://ipsedigit.github.io/feature-new-home/`.
- **Multiple previews:** All preview subdirectories coexist on `gh-pages`. A production deploy (push to `main`) does not wipe them.
- **Content:** Preview branches use whatever `_posts/` are on the branch (inherited from `main` at branch creation). No pipeline runs.
- **styles:** Full Jekyll build means CSS/fonts/images are deployed under `/branchname/assets/` and load correctly.
