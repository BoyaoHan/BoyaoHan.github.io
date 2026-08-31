---
title: "GeoPredict: Leveraging Predictive Kinematics and 3D Gaussian Geometry for Precise VLA Manipulation"
authors: "Jingjing Qian, Boyao Han, Chen Shi, Lei Xiao, Long Yang, Shaoshuai Shi, Li Jiang"
collection: publications
category: conferences
permalink: /publication/2026-geopredict
excerpt: 'GeoPredict improves 3D reasoning in VLA manipulation by predicting robot trajectories and future workspace geometry. Its training-only geometric supervision boosts simulated and real-world performance without adding 3D decoding at inference.'
date: 2026-04-01
display_order: 3
venue: 'IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)'
award: 'Highlight'
paperurl: 'https://arxiv.org/abs/2512.16811'
projecturl: 'https://jingjingqian75.github.io/GeoPredict-Page/'
media: '/images/publications/geopredict-method.png'
media_type: 'image'
media_alt: 'Overview of the GeoPredict architecture'
citation: 'Jingjing Qian, Boyao Han, Chen Shi, Lei Xiao, Long Yang, Shaoshuai Shi, Li Jiang. (2026). &quot;GeoPredict: Leveraging Predictive Kinematics and 3D Gaussian Geometry for Precise VLA Manipulation.&quot; <i>CVPR</i>. (Highlight).'
---

## Abstract

Vision-Language-Action (VLA) models achieve strong generalization in robotic manipulation but remain largely reactive and 2D-centric, making them unreliable in tasks that require precise 3D reasoning. We propose **GeoPredict**, a geometry-aware VLA framework that augments a continuous-action policy with predictive kinematic and geometric priors. GeoPredict introduces a trajectory-level module that encodes motion history and predicts multi-step 3D keypoint trajectories of robot arms, and a predictive 3D Gaussian geometry module that forecasts workspace geometry with track-guided refinement along future keypoint trajectories. These predictive modules serve exclusively as training-time supervision through depth-based rendering, while inference requires only lightweight additional query tokens without invoking any 3D decoding. Experiments on RoboCasa Human-50, LIBERO, and real-world manipulation tasks show that GeoPredict consistently outperforms strong VLA baselines, especially in geometry-intensive and spatially demanding scenarios.

## BibTeX

```bibtex
@inproceedings{qian2026geopredict,
  title     = {GeoPredict: Leveraging Predictive Kinematics and 3D Gaussian Geometry for Precise VLA Manipulation},
  author    = {Qian, Jingjing and Han, Boyao and Shi, Chen and Xiao, Lei and Yang, Long and Shi, Shaoshuai and Jiang, Li},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2026},
  note      = {Highlight}
}
```
