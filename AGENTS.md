# Repository Guidelines

## Project Structure & Module Organization

This repository is a Jekyll academic website. Site-wide settings live in `_config.yml`; the homepage is `_pages/about.md`, and publication records are stored in `_publications/`. Reusable HTML is split between `_layouts/` and `_includes/`, while SCSS is organized under `_sass/` and `assets/css/`. Store images in `images/`, grouped by homepage section. JavaScript sources are in `assets/js/`; `assets/js/main.min.js` is generated.

## Build, Test, and Development Commands

- `bundle install` installs Ruby and Jekyll dependencies.
- `bundle exec jekyll serve -l -H localhost` serves the site at `http://localhost:4000` with live reload.
- `bundle exec jekyll build` renders the production site into `_site/` and catches Liquid, front-matter, and configuration errors.
- `docker compose up --build` runs the same site in a container when local Ruby setup is inconvenient.
- `npm install && npm run build:js` installs frontend dependencies and rebuilds `assets/js/main.min.js` after JavaScript changes.

## Coding Style & Naming Conventions

Follow nearby code: two-space indentation for YAML, Liquid, SCSS, and JavaScript; four spaces for Python. Use lowercase kebab-case for content files and the `YYYY-MM-DD-descriptive-slug.md` pattern for dated collections. Every content file should have valid YAML front matter matching its collection. Edit `assets/js/_main.js`, plugins, or theme sources rather than hand-editing minified output. Keep repository URLs and personal metadata centralized in `_config.yml`.

## Testing Guidelines

There is no dedicated automated test suite or coverage threshold. Treat `bundle exec jekyll build` as the required validation step. For layout or responsive changes, also inspect the homepage locally at desktop and mobile widths. Re-run `npm run build:js` when JavaScript sources change and confirm the browser console is clean.

## Commit & Pull Request Guidelines

History favors brief, imperative subjects such as `Update _config.yml`; keep each commit focused and describe generated updates explicitly. Pull requests should summarize the user-visible change, list validation performed, and link relevant issues. Include before/after screenshots for visual changes. Do not commit `_site/`, `node_modules/`, `vendor/`, or other ignored build artifacts.
