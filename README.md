# Boyao Han Academic Website

Source for [boyaohan.github.io](https://boyaohan.github.io), a Jekyll-based academic homepage featuring publications, research experience, education, and contact links.

## Local Development

```bash
bundle install
bundle exec jekyll serve -l -H localhost
```

The site is then available at `http://localhost:4000`. Run `bundle exec jekyll build` before publishing to validate Liquid, front matter, and SCSS.

## Content

- Edit homepage content in `_pages/about.md`.
- Add papers to `_publications/` using `YYYY-MM-DD-paper-name.md`.
- Store publication media under `images/publications/`.
- Update personal metadata and public URLs in `_config.yml`.

Changes pushed to `master` are published through GitHub Pages.
