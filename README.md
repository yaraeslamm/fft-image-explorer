# Interactive Frequency-Domain Image Filter (FFT Explorer)

This project provides an interactive tool for exploring and filtering images in the **frequency domain** using the **2D Fast Fourier Transform (FFT)**.  
The application is built with **Gradio**, allowing real-time tuning of filters and instant visual feedback.

---

## 🚀 Features

- Upload **any image (PNG/JPG)**
- Visualize the image’s **FFT magnitude spectrum**
- Apply three types of frequency-domain filters:
  - **Low-pass** → smooths the image by removing high-frequency components
  - **High-pass** → enhances edges and fine details
  - **Band-pass** → isolates a selected range of frequencies
- Adjustable parameters:
  - **Cutoff frequency** (controls which frequencies are kept/removed)
  - **Bandwidth** (for band-pass: how wide the selected frequency band is)
- Visualization of:
  - Original image  
  - FFT spectrum  
  - Frequency mask  
  - Filtered output 
- Processes **each color channel independently** (RGB/BGR)

---

## ✨ Why I built this
I built this project to better understand how frequency components affect image sharpness, noise, and texture. FFTs are often hidden behind libraries, so I wanted hands-on experience manipulating the frequency domain directly.

---
## 🧠 How It Works

1. The image is split into its **three color channels** (B, G, R).
2. For each channel:
   - Compute the **2D FFT** and shift low frequencies to the center.
   - Create a **frequency mask** based on the selected filter.
   - Multiply `FFT × mask` to apply the filter.
   - Apply the **inverse FFT** to reconstruct the filtered channel.
3. All filtered channels are merged back into the final RGB image.

This provides hands-on insight into how frequency components affect image structure, sharpness, and noise.

---

## 🕹️ How to Use

1. **Upload an Image**  
   Choose any JPG/PNG image.

2. **Select a Filter Type**
   - **Low-pass** → keeps low frequencies (blurs the image)
   - **High-pass** → keeps high frequencies (sharpens edges)
   - **Band-pass** → keeps a selected frequency band

3. **Adjust Parameters**
   - **Cutoff Frequency**: controls how far from the center frequencies are preserved or suppressed.
   - **Bandwidth** (for Band-pass): controls how wide the frequency band is.

4. View all four visual outputs:
   - **Original Image**
   - **FFT Magnitude Spectrum**
   - **Filter Mask**
   - **Filtered Output**

---

## 📸 Example 

Replace the images below with your actual examples if you want.

| Original | FFT Spectrum |
|----------|--------------|
| ![Original](/assets/image-1.jpeg) | ![Spectrum](/assets/image-2.jpeg) |

| Filter Mask | Filtered Output |
|-------------|-----------------|
| ![Mask](/assets/image-3.jpeg) | ![Filtered](/assets/image-4.jpeg) |

---

## 🛠️ Tech Stack

- **Python**
- **NumPy**
- **OpenCV (cv2)**
- **Gradio**

---


## Try It Locally

1. Clone the repo:
  ```bash
git clone https://github.com/yaraeslamm/fft-image-explorer.git
cd fft-image-explorer
   ```
2. Install dependencies:
  ```bash
pip install -r requirements.txt
   ```
3. Run the app:
  ```bash
python app.py
   ```
---

## 📡 Live Demo


---

## License
This project is licensed under the MIT License.


