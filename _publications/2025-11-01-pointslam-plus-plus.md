---
title: "PointSLAM++: Robust Dense Neural Gaussian Point Cloud-based SLAM"
collection: publications
category: conferences
permalink: /publication/2026-pointslam-plus-plus
excerpt: 'PointSLAM++ is an RGB-D SLAM system that combines a hierarchically constrained neural Gaussian representation, progressive pose optimization, and a dynamic neural representation graph to achieve robust, high-precision real-time 3D reconstruction and photorealistic rendering under depth-sensor noise.'
date: 2025-11-01
venue: 'AAAI Conference on Artificial Intelligence (AAAI), Poster'
paperurl: 'https://arxiv.org/abs/2601.11617'
citation: 'Xu Wang, Boyao Han, Xiaojun Chen, Ying Liu, Ruihui Li. (2026). &quot;PointSLAM++: Robust Dense Neural Gaussian Point Cloud-based SLAM.&quot; <i>AAAI</i>. (Poster).'
---

## Abstract

Real-time 3D reconstruction is crucial for robotics and augmented reality, yet current simultaneous localization and mapping (SLAM) approaches often struggle to maintain structural consistency and robust pose estimation in the presence of depth noise. This work introduces **PointSLAM++**, a novel RGB-D SLAM system that leverages a hierarchically constrained neural Gaussian representation to preserve structural relationships while generating Gaussian primitives for scene mapping. It also employs progressive pose optimization to mitigate depth sensor noise, significantly enhancing localization accuracy. Furthermore, it utilizes a dynamic neural representation graph that adjusts the distribution of Gaussian nodes based on local geometric complexity, enabling the map to adapt to intricate scene details in real time. This combination yields high-precision 3D mapping and photorealistic scene rendering. Experimental results show PointSLAM++ outperforms existing 3DGS-based SLAM methods in reconstruction accuracy and rendering quality, demonstrating its advantages for large-scale AR and robotics.

## BibTeX

```bibtex
@inproceedings{wang2026pointslam,
  title     = {PointSLAM++: Robust Dense Neural Gaussian Point Cloud-based SLAM},
  author    = {Wang, Xu and Han, Boyao and Chen, Xiaojun and Liu, Ying and Li, Ruihui},
  booktitle = {Proceedings of the AAAI Conference on Artificial Intelligence},
  year      = {2026}
}
```

