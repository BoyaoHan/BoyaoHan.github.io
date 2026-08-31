---
layout: home
permalink: /
title: "Boyao Han"
excerpt: "Boyao Han is an M.Phil. student at CUHK-Shenzhen working on vision-language-action models, AI agents, and 3D computer vision."
redirect_from: 
  - /about/
  - /about.html
---

<main class="home">
  <header class="home-intro">
    <div class="home-identity">
      <h1>Boyao Han</h1>
      <p class="home-role">M.Phil. Student at CUHK-Shenzhen</p>
      <p>
        I am an M.Phil. student at the
        <a href="https://sds.cuhk.edu.cn/">School of Data Science</a>,
        The Chinese University of Hong Kong, Shenzhen,
        advised by <a href="https://llijiang.github.io/">Prof. Li Jiang</a>.
        Before that, I studied at the
        <a href="https://csee.hnu.edu.cn/">College of Computer Science and Electronic Engineering</a>,
        Hunan University.
      </p>
      <p>
        My research interests include vision-language-action (VLA) models, AI agents,
        and 3D computer vision.
      </p>
      <p class="home-contact-note">Feel free to contact me for discussion or collaboration!</p>
      <p class="home-links" aria-label="Profiles and contact">
        <a href="mailto:{{ site.author.email }}">Email</a>
        <a href="{{ site.author.googlescholar }}">Google Scholar</a>
        <a href="https://github.com/{{ site.author.github }}">GitHub</a>
      </p>
    </div>
    <img class="home-portrait" src="{{ '/images/boyaohan.jpg' | relative_url }}" alt="Boyao Han" width="160" height="222">
  </header>

  <section class="home-section" aria-labelledby="news-heading">
    <h2 id="news-heading">News</h2>
    <ul class="home-news">
      <li><time datetime="2026-09">2026.09</time><span>Started my M.Phil. journey at CUHK-Shenzhen!</span></li>
      <li><time datetime="2026-04">2026.04</time><span><a href="https://arxiv.org/abs/2512.16811">GeoPredict</a> was accepted at CVPR 2026 (<span class="publication-award">Highlight</span>).</span></li>
      <li><time datetime="2025-11">2025.11</time><span><a href="https://arxiv.org/abs/2601.11617">PointSLAM++</a> was accepted as a Poster at AAAI 2026.</span></li>
      <li><time datetime="2025-10">2025.10</time><span><a href="https://arxiv.org/abs/2510.03198">Memory Forcing</a> became available on arXiv.</span></li>
    </ul>
  </section>

  <section class="home-section" aria-labelledby="publications-heading">
    <h2 id="publications-heading">Publications</h2>
    {% assign publications = site.publications | sort: "display_order" | reverse %}
    <div class="home-publications">
      {% for publication in publications %}
        <article class="home-publication{% if publication.media %} home-publication--with-media{% endif %}">
          {% if publication.media %}
            <a class="publication-media" href="{{ publication.projecturl | default: publication.paperurl }}" aria-label="View {{ publication.title }}">
              {% if publication.media_type == "video" %}
                <video autoplay muted loop playsinline preload="metadata" aria-label="{{ publication.media_alt }}">
                  <source src="{{ publication.media | relative_url }}" type="video/mp4">
                </video>
              {% else %}
                <img src="{{ publication.media | relative_url }}" alt="{{ publication.media_alt }}" loading="lazy" decoding="async">
              {% endif %}
            </a>
          {% endif %}
          <div class="publication-details">
            <h3><a href="{{ publication.paperurl }}">{{ publication.title }}</a></h3>
            <p class="publication-authors">
              {{ publication.authors | replace: "Boyao Han", "<strong>Boyao Han</strong>" }}
              {% if publication.equal_contribution %}<span class="publication-note"><sup>*</sup> Equal contribution.</span>{% endif %}
            </p>
            <p class="publication-venue">
              {{ publication.venue }}{% if publication.award %}, <span class="publication-award">{{ publication.award }}</span>{% endif %}
            </p>
            <p class="publication-summary">{{ publication.excerpt }}</p>
            <p class="publication-links">
              <a href="{{ publication.paperurl }}">Paper</a>
              {% if publication.projecturl %}<a href="{{ publication.projecturl }}">Project</a>{% endif %}
            </p>
          </div>
        </article>
      {% endfor %}
    </div>
  </section>

  <section class="home-section" aria-labelledby="experience-heading">
    <h2 id="experience-heading">Research Experience</h2>
    <div class="experience-list">
      <article class="experience-item">
        <a class="experience-logo-link experience-logo-link--didi" href="https://web.didiglobal.com/" aria-label="DiDi">
          <img class="experience-logo" src="{{ '/images/experience/didi.svg' | relative_url }}" alt="DiDi logo" width="88" height="88" loading="lazy" decoding="async">
        </a>
        <div class="experience-details">
          <h3><a href="https://web.didiglobal.com/">DiDi, Guangzhou, China</a></h3>
          <p class="experience-role">Research Intern, AI Research</p>
          <p class="experience-meta">June 2026 - Present</p>
          <p>Mentor: <a href="https://shishaoshuai.com/">Shaoshuai Shi</a></p>
        </div>
      </article>

      <article class="experience-item">
        <a class="experience-logo-link" href="https://www.slai.edu.cn/en" aria-label="Shenzhen Loop Area Institute">
          <img class="experience-logo" src="{{ '/images/experience/slai.png' | relative_url }}" alt="Shenzhen Loop Area Institute logo" width="88" height="88" loading="lazy" decoding="async">
        </a>
        <div class="experience-details">
          <h3><a href="https://www.slai.edu.cn/en">Shenzhen Loop Area Institute, Shenzhen, China</a></h3>
          <p class="experience-center"><a href="https://www.slai.edu.cn/en/node/381">Center for Embodied Artificial Intelligence and Computer Vision (EACV)</a></p>
          <p class="experience-role">Research Intern</p>
          <p class="experience-meta">November 2025 - June 2026</p>
          <p>Advisor: <a href="https://www.slai.edu.cn/zh-hans/teacher/240">Prof. Li Jiang</a></p>
        </div>
      </article>
    </div>
  </section>

  <section class="home-section" aria-labelledby="education-heading">
    <h2 id="education-heading">Education</h2>
    <div class="education-list">
      <article class="education-item">
        <a class="education-logo-link" href="https://www.cuhk.edu.cn/en" aria-label="The Chinese University of Hong Kong, Shenzhen">
          <img class="education-logo" src="{{ '/images/education/cuhk-shenzhen.png' | relative_url }}" alt="CUHK-Shenzhen emblem" width="88" height="88" loading="lazy" decoding="async">
        </a>
        <div class="education-details">
          <h3><a href="https://www.cuhk.edu.cn/en">The Chinese University of Hong Kong, Shenzhen</a></h3>
          <p class="education-school"><a href="https://sds.cuhk.edu.cn/">School of Data Science</a></p>
          <p class="education-degree">M.Phil. in Computer Science</p>
          <p class="education-meta">September 2026 - Present</p>
          <p>Advisor: <a href="https://llijiang.github.io/">Prof. Li Jiang</a></p>
        </div>
      </article>

      <article class="education-item">
        <a class="education-logo-link" href="https://www.hnu.edu.cn/" aria-label="Hunan University">
          <img class="education-logo" src="{{ '/images/education/hunan-university.jpg' | relative_url }}" alt="Hunan University emblem" width="88" height="88" loading="lazy" decoding="async">
        </a>
        <div class="education-details">
          <h3><a href="https://www.hnu.edu.cn/">Hunan University</a></h3>
          <p class="education-school"><a href="https://csee.hnu.edu.cn/">College of Computer Science and Electronic Engineering</a></p>
          <p class="education-degree">B.Eng. in Computer Science</p>
          <p class="education-meta">September 2022 - June 2026</p>
          <p>Advisor: <a href="https://csee.hnu.edu.cn/people/liruihui">Prof. Ruihui Li</a></p>
        </div>
      </article>
    </div>
  </section>

  <footer class="home-footer">
    <p>&copy; {{ site.time | date: '%Y' }} Boyao Han</p>
  </footer>
</main>
