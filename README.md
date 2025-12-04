# 🌟 X-Ray Vision — Explore Hidden Frequencies in Images
# The X-Ray Vision App (Interactive Frequency Filtering for Images)
**X-Ray Vision** is an interactive tool that reveals the **hidden waves** inside any image using the **2D Fourier Transform (FFT)**.  
Upload a picture → instantly see how different frequency components shape the image.


---

## Try It Locally

1. Clone the repo:
   ```python
   git clone https://github.com/yaraeslamm/x-ray-vision.git
   cd xray-vision
   ```
2. Install dependencies:
```python
   
pip install -r requirements.txt
   ```
3. Run the app:
```python
python app.py
   ```

## 🎯 What This App Shows

Every image is made of waves:
- **Big waves** → smooth shapes
- **Tiny waves** → sharp details (edges, textures)
- **Medium waves** → repeating patterns (fabric, bricks, grass)

This app lets you explore and manipulate these waves. You can:

- Blur the image (low-pass)
- Sharpen it (high-pass)
- Reveal textures (band-pass)
- See the frequency spectrum (the image's "X-ray")
- Visualize the filter mask used

Everything updates live as you move the sliders.

---

## 🎛️ Features

- 📤 Upload any image
- 🌌 View the FFT magnitude spectrum
- 🎭 Apply frequency masks:
  - Low-pass (smooth)
  - High-pass (enhance edges)
  - Band-pass (extract textures)
- 🔍 View the applied filter mask
- 🎨 Interactive real-time visualization
- ⚡ Built with **NumPy**, **OpenCV**, and **Gradio**

---

## 🧠 Why This Project Matters

This project demonstrates fundamental concepts used in:
- Image processing
- Computer vision
- Signal processing
- Compression (JPEG/DCT)
- Medical imaging (MRI/CT)
- Astronomy
- Denoising & restoration


---

## 🧩 How It Works (Technical Overview)

1. Convert image to grayscale
2. Compute 2D FFT and center low frequencies
3. Display the magnitude spectrum
4. Create frequency masks:
   - Low-pass
   - High-pass
   - Band-pass
5. Multiply FFT × mask
6. Apply inverse FFT to reconstruct the filtered image

The app displays:
- Original image
- Frequency spectrum
- Filter mask
- Resulting image

---

---

## 🛠 Tech Stack

- Python
- NumPy
- OpenCV
- Gradio