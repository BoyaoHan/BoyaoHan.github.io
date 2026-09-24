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

## VersaCamVLA project page

The project page lives in `VersaCamVLA.github.io/index.html` and is built with the
personal site. After publishing, its URL is
`https://boyaohan.github.io/VersaCamVLA.github.io/`.
The `.github.io` suffix here is part of the directory name, not a separate domain.
No additional repository, DNS configuration, or JavaScript router is needed.
Keep the site's `baseurl` empty: the personal homepage still lives at `/`.

The page uses native HTML anchors: `#overview`, `#video`, `#method`, `#data`,
`#results`, and `#citation`. For example,
`https://boyaohan.github.io/VersaCamVLA.github.io/#data` opens the Data section.
Keep the path's capitalization and existing section IDs when replacing the
Coming soon text so shared links continue to work. Project styles live in
`_sass/layout/_project.scss`; the page reuses the homepage layout and favicon.

The favicon PNGs, ICO, and Apple touch icon are resized copies of
`images/education/cuhk-shenzhen.png`. Icon links and the web app manifest use a
`v=cuhk-shenzhen` query string to refresh previously cached template icons.
