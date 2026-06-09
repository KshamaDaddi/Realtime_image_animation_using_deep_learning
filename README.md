# 🎬 Real-Time Image Animation Using Deep Learning

> Bring any still photo to life — in real time — by transferring motion from a driving video using deep learning.

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red?style=flat-square&logo=pytorch)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=flat-square)
![Django](https://img.shields.io/badge/Django-Web%20Interface-darkgreen?style=flat-square)
![FPS](https://img.shields.io/badge/Performance-25--30%20FPS-orange?style=flat-square)
![SSIM](https://img.shields.io/badge/SSIM-0.93-brightgreen?style=flat-square)

---

## 📌 What This Project Does

This project takes **one static image** (like a portrait or a photo) and animates it by borrowing motion patterns from a **driving video** — all in real time.

**You give it:**
- A source image (any face or object)
- A driving video (someone nodding, speaking, or moving)

**It gives you:**
- A smooth, realistic animation of the source image performing those same movements

No manual keyframing. No 3D modeling. No frame-by-frame artist work. Just deep learning.

---

## 🎯 Key Results

| Metric | Score | What It Means |
|--------|-------|----------------|
| SSIM | **0.93** | 93% structural accuracy vs ground truth (1.0 = perfect) |
| LPIPS | **0.08** | Very low perceptual difference — looks realistic to human eyes |
| FID | **27.4** | Strong realism score for a generative model |
| Frame Rate | **25–30 FPS** | Near real-time performance at 256×256 resolution |

---

## 🧠 How It Works

The system is built on the **First-Order Motion Model (FOM)** — a NeurIPS 2019 architecture that separates *appearance* (from the source image) from *motion* (from the driving video). Three neural networks work together:

```
Source Image ──┐
               ├──► Keypoint Detector ──► Dense Motion Network ──► Generator ──► Animated Frame
Driving Video ─┘                                                        ↑
                                                              CNN Refinement Module
```

### 1. Keypoint Detector Network
- Finds motion landmarks automatically using **Gaussian heatmaps**
- No manual labeling needed — learns keypoints entirely unsupervised
- Detects head tilts, eyebrow raises, mouth movements without being told what to look for

### 2. Dense Motion Network
- Computes **optical flow** `F(x,y) = (u, v)` — a per-pixel motion vector field
- Generates an **occlusion map** to avoid hallucinating motion in hidden regions
- Ensures only visible parts of the image are animated

### 3. Generator Network (U-Net)
- Encoder-decoder with skip connections for fine detail preservation
- Warps source image features using the predicted motion field
- Trained with **L1 loss + Perceptual loss + Equivariance loss**

### 4. CNN Image Refinement Module *(custom addition)*
- Lightweight 3-layer CNN applied after frame generation
- Uses **residual learning**: `I_refined = I_input + α × ∇(I_input)`
- Sharpens edges, reduces blur, improves temporal stability between frames
- Trained with MAE + Perceptual loss

---

## 🗂️ Project Structure

```
Realtime_image_animation_using_deep_learning/
│
├── prefetch_models.py          # Download & cache pretrained FOM weights
├── image_animation.py          # Core animation pipeline
├── keypoint_detector.py        # Keypoint detection network
├── dense_motion.py             # Optical flow & occlusion estimation
├── generator.py                # U-Net frame generator
├── refinement_module.py        # CNN post-processing module
│
├── django_app/                 # Web interface (upload image + video → get animation)
│   └── views.py
│
├── notebooks/
│   └── demo.ipynb              # Interactive Jupyter demo
│
├── checkpoints/                # Pretrained model weights (VoxCeleb)
├── inputs/                     # Sample source images
├── outputs/                    # Generated animations (GIF / MP4)
│
└── requirements.txt
```

---

## ⚙️ System Pipeline (Step by Step)

```
1. INPUT          →  Upload source image + driving video via Django / Jupyter
2. PREPROCESS     →  Resize to 256×256, normalize to [0,1], convert to RGB
3. KEYPOINTS      →  Detect landmarks in source image and each driving frame
4. MOTION         →  Compute dense optical flow + occlusion mask
5. GENERATE       →  Warp source features → reconstruct animated frame
6. REFINE         →  CNN refinement for sharpness and temporal consistency
7. OUTPUT         →  Compile frames to GIF or MP4 using FFmpeg
```

---

## 🛠️ Tech Stack

### Deep Learning
| Library | Purpose |
|---------|---------|
| **PyTorch** | Core framework — train and run the FOM architecture |
| **TorchVision** | Pretrained VGG features for perceptual loss |
| **Diffusers** | Generative motion synthesis modules |
| **Transformers** | Pretrained model integration (Hugging Face) |
| **Accelerate** | Mixed precision training for faster GPU performance |

### Computer Vision & Image Processing
| Library | Purpose |
|---------|---------|
| **OpenCV** | Real-time frame capture, resize, BGR→RGB conversion |
| **Pillow (PIL)** | Image normalization and augmentation |
| **FFmpeg** | Extract frames from video; compile output GIF/MP4 |
| **NumPy** | Tensor manipulation and pixel arithmetic |
| **scikit-image** | SSIM metric computation |

### Model Management & Deployment
| Library | Purpose |
|---------|---------|
| **Hugging Face Hub** | Fetch and cache pretrained model weights |
| **Safetensors** | Fast, safe model weight serialization |
| **Django** | Web interface — upload inputs, download animation |
| **Jupyter Notebook** | Interactive prototyping and demo |
| **Matplotlib** | Evaluation plots (SSIM, FPS, FID graphs) |
| **tqdm + dotenv** | Progress tracking and config management |

### Hardware Used
- **GPU:** NVIDIA GeForce RTX 3060 (CUDA-enabled)
- **CPU:** Intel Core i7
- **RAM:** 16 GB
- **Storage:** 512 GB SSD

---

## 🏋️ Training Details

| Parameter | Value |
|-----------|-------|
| Optimizer | Adam |
| Learning Rate | 0.0002 |
| Batch Size | 16 |
| Epochs | 100–150 |
| Loss Functions | L1, Perceptual (VGG), Equivariance |
| Validation Metrics | SSIM, LPIPS, FID |
| Datasets | VoxCeleb + Custom Facial Motion Dataset |
| Precision | Mixed precision (FP16) |

---

## 🚀 Getting Started

### Prerequisites
```bash
# Python 3.10 required
# NVIDIA GPU with CUDA recommended for real-time performance
```

### Installation
```bash
# 1. Clone the repository
git clone https://github.com/KshamaDaddi/Realtime_image_animation_using_deep_learning.git
cd Realtime_image_animation_using_deep_learning

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download pretrained model weights
python prefetch_models.py
```

### Run via Jupyter Notebook
```bash
jupyter notebook notebooks/demo.ipynb
```

### Run via Command Line
```bash
# Animate using a driving video file
python image_animation.py --source inputs/portrait.jpg --driving inputs/driving.mp4

# Output is saved to outputs/ as GIF and MP4
```

### Run via Web Interface (Django)
```bash
python manage.py runserver
# Open http://127.0.0.1:8000 in your browser
# Upload source image + driving video → click Animate
```

---

## 📊 Performance Benchmarks

| Resolution | Avg FPS | Notes |
|------------|---------|-------|
| 128×128 | ~33 FPS | Fastest, lower quality |
| **256×256** | **25–30 FPS** | Optimal — real-time capable |
| 512×512 | ~18 FPS | Slower, higher quality |

*All benchmarks on NVIDIA RTX 3060 with CUDA acceleration.*

---

## 🔍 How This Differs from Existing Approaches

| Approach | Limitation | What We Did Differently |
|----------|-----------|--------------------------|
| Raw FOM (NeurIPS 2019) | No post-processing, no UI | Added CNN refinement module + Django web interface |
| GAN-only methods | Don't guarantee identity preservation | FOM explicitly separates appearance from motion |
| VAE approaches | Blurry outputs | Perceptual loss + residual refinement gives sharper results |
| 3D face models | Need expensive mesh fitting | FOM is category-agnostic — works on faces, objects, puppets |
| Deepfake tools | Replace identity | We transfer motion only — source identity is preserved |

---

## ⚠️ Limitations

- Minor distortions may appear at extreme head rotations (>45°)
- Performance drops at resolutions above 256×256 on lower-end GPUs
- Background inconsistencies in the driving video can affect output quality

**Planned improvements:** Transformer-based temporal modeling and diffusion-based refinement for higher resolution output.

---

## 🔭 Real-World Applications

- 🎭 **Digital avatars** for games, virtual reality, and the metaverse
- 🎓 **E-learning** — animate historical portraits or educational characters
- 🏥 **Medical simulations** — realistic patient-facing virtual agents
- 🎬 **AI-assisted media** — low-budget film and content production
- 🤖 **Conversational AI** — animated talking-head interfaces

---

## 📄 Research Paper

This project is based on the published paper:

> **Real-Time Image Animation Using Deep Learning**  
> Kshama Daddi, Sumit Badake, Keertiraj Kamble, Ananya Mangaj  
> *Department of AI & Data Science, KLE College of Engineering and Technology, Chikodi*  
> Guided by Dr. Jagannath Jadhav (HOD, AI & DS)

**Core reference:**
> Siarohin et al., *"First Order Motion Model for Image Animation"*, NeurIPS 2019.

---

## 📜 License

This project is for academic and research purposes. Please use responsibly — this system is designed for identity-preserving motion transfer and should not be used to create non-consensual synthetic media.

---

## ⭐ If you found this useful, please give the repo a star!

```
It helps other students and recruiters discover this work.
```# Realtime_image_animation_using_deep_learning
