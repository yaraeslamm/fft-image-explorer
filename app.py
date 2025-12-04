import numpy as np
import cv2
import gradio as gr

# ---------------------------------------------------------
# STEP 1 — Compute frequency waves (FFT)
# ---------------------------------------------------------
def compute_fft(gray):
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)

    magnitude = np.log(np.abs(fshift) + 1)
    magnitude = (magnitude / magnitude.max() * 255).astype(np.uint8)

    return fshift, magnitude


# ---------------------------------------------------------
# STEP 2 — Create filters (low-pass, high-pass, band-pass)
# ---------------------------------------------------------
def create_filter(shape, filter_type, cutoff, bandwidth):
    rows, cols = shape
    crow, ccol = rows // 2, cols // 2

    y, x = np.ogrid[:rows, :cols]
    dist = np.sqrt((y - crow)**2 + (x - ccol)**2)

    if filter_type == "Low-pass":
        mask = dist < cutoff

    elif filter_type == "High-pass":
        mask = dist > cutoff

    elif filter_type == "Band-pass":
        mask = (dist > (cutoff - bandwidth)) & (dist < (cutoff + bandwidth))

    else:
        mask = np.ones_like(dist)

    return mask.astype(np.float32)


# ---------------------------------------------------------
# STEP 3 — Apply filter in frequency domain
# ---------------------------------------------------------
def apply_filter(img, filter_type, cutoff, bandwidth):

    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)

    # FFT
    fshift, magnitude = compute_fft(gray)

    # Make frequency mask
    mask = create_filter(gray.shape, filter_type, cutoff, bandwidth)

    # Multiply waves by mask
    filtered_fft = fshift * mask

    # Inverse FFT
    f_ishift = np.fft.ifftshift(filtered_fft)
    img_back = np.fft.ifft2(f_ishift).real

    img_back = np.clip(img_back, 0, 255).astype(np.uint8)

    # Normalize mask for display
    mask_vis = (mask * 255).astype(np.uint8)

    return img, magnitude, mask_vis, img_back


# ---------------------------------------------------------
# STEP 4 — UI function
# ---------------------------------------------------------
def process(img, filter_type, cutoff, bandwidth):
    return apply_filter(img, filter_type, cutoff, bandwidth)


# ---------------------------------------------------------
# STEP 5 — Gradio Interface
# ---------------------------------------------------------
demo = gr.Interface(
    fn=process,
    inputs=[
        gr.Image(type="numpy", label="Upload Image"),
        gr.Dropdown(["Low-pass", "High-pass", "Band-pass"], label="Filter Type"),
        gr.Slider(1, 150, 30, label="Cutoff Frequency"),
        gr.Slider(1, 100, 20, label="Bandwidth (for Band-pass)")
    ],
    outputs=[
        gr.Image(label="Original Image"),
        gr.Image(label="Frequency Waves (FFT)"),
        gr.Image(label="Filter Mask"),
        gr.Image(label="Filtered Output")
    ],
    title="X-Ray Vision — Frequency Image Explorer",
    description="See the hidden waves inside your picture and change them!"
)

if __name__ == "__main__":
    demo.launch()
