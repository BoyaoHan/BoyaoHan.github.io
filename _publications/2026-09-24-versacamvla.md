---
title: "VersaCamVLA: Camera-Configurable VLA Policies for Robotic Manipulation"
authors: "Boyao Han*, Chen Shi*, Jingjing Qian, Zhuotao Tian, Li Jiang"
equal_contribution: true
collection: publications
category: conferences
permalink: /publication/2026-versacamvla
excerpt: 'VersaCamVLA enables pretrained VLA policies to handle varying camera counts and unseen camera poses through a unified scene-token interface. Learned from posed RGB views, its compact scene tokens improve manipulation robustness on RoboTwin, LIBERO, and real robots without explicit 3D reconstruction or novel-view rendering at deployment.'
date: 2026-09-24
display_order: 4
venue: 'Conference on Neural Information Processing Systems (NeurIPS), 2026'
award: 'Poster'
link: '/VersaCamVLA.github.io/'
codeurl: 'https://github.com/BoyaoHan/VersaCamVLA'
codelabel: 'GitHub'
projecturl: '/VersaCamVLA.github.io/'
media: '/images/publications/versacamvla-method.png'
media_type: 'image'
media_alt: 'VersaCamVLA framework: scene-token interface learning and scene-token-conditioned VLA policy learning'
citation: 'Boyao Han, Chen Shi, Jingjing Qian, Zhuotao Tian, Li Jiang. (2026). &quot;VersaCamVLA: Camera-Configurable VLA Policies for Robotic Manipulation.&quot; <i>Advances in Neural Information Processing Systems (NeurIPS)</i>. (Poster).'
---

## Abstract

Vision-Language-Action (VLA) models have emerged as powerful foundations for robotic manipulation, but their reliance on fixed camera configurations during training makes them brittle to changes in camera count or pose during deployment. To overcome these limitations, we propose **VersaCamVLA**, a camera-configurable framework that decouples camera-set representation from action learning. VersaCamVLA learns a unified scene-token interface that maps an arbitrary, variable set of posed RGB views into fixed-size latent scene tokens. This is achieved via multi-signal target-view prediction and Wrist-Augmented Pose Sampling (WAPS), which leverages natural wrist-camera motion for free pose diversity. At deployment, a lightweight spatial encoder injects these compact scene tokens into a pretrained base VLA as a supplementary visual condition, requiring no explicit 3D sensing or novel-view rendering. Experiments on RoboTwin, LIBERO, and a real-robot platform demonstrate that VersaCamVLA consistently outperforms prior VLA methods and direct multi-view baselines, maintaining robust performance across varying camera counts and unseen camera poses.

## BibTeX

```bibtex
@inproceedings{han2026versacamvla,
  title     = {VersaCamVLA: Camera-Configurable VLA Policies for Robotic Manipulation},
  author    = {Han, Boyao and Shi, Chen and Qian, Jingjing and Tian, Zhuotao and Jiang, Li},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2026},
  note      = {Poster},
  url       = {https://boyaohan.github.io/VersaCamVLA.github.io/}
}
```
