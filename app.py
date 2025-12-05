import numpy as np
import cv2
import gradio as gr

# ---------------------------------------------------------
# STEP 1 — Compute frequency waves (FFT)
# ---------------------------------------------------------
def compute_fft(gray):
    """
    Computes the Fast Fourier Transform (FFT) of a grayscale image.
    
    Args:
        gray (numpy.ndarray): Grayscale image represented as a 2D NumPy array.
        
    Returns:
        tuple: A tuple containing:
            - fshift (numpy.ndarray): Shifted FFT of the grayscale image.
            - magnitude (numpy.ndarray): Logarithmic magnitude spectrum of the FFT.
    """

    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)

    magnitude = np.log(np.abs(fshift) + 1)
    magnitude = (magnitude / magnitude.max() * 255).astype(np.uint8)

    return fshift, magnitude


# ---------------------------------------------------------
# STEP 2 — Create filters (low-pass, high-pass, band-pass)
# ---------------------------------------------------------
def create_filter(shape, filter_type, cutoff, bandwidth):
    """
    Creates a frequency domain filter (low-pass, high-pass, or band-pass).
    
    Args:
        shape (tuple): Shape of the image (height, width).
        filter_type (str): Type of filter. One of "Low-pass", "High-pass", or "Band-pass".
        cutoff (float): Cutoff frequency in pixels (for low-pass and high-pass).
        bandwidth (float): Bandwidth for band-pass filter.
        
    Returns:
        numpy.ndarray: The generated frequency filter mask.
    """
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
    """
    Applies a frequency domain filter to each color channel (RGB) of an image using FFT.
    
    Args:
        img (numpy.ndarray): Input image in BGR format (NumPy array).
        filter_type (str): Type of filter to apply ("Low-pass", "High-pass", or "Band-pass").
        cutoff (float): Cutoff frequency for the filter.
        bandwidth (float): Bandwidth for the band-pass filter.
        
    Returns:
        tuple: A tuple containing:
            - img (numpy.ndarray): The original image.
            - magnitude (numpy.ndarray): Magnitude spectrum of the FFT.
            - mask_vis (numpy.ndarray): Visual representation of the frequency mask.
            - img_back (numpy.ndarray): The filtered image obtained after applying the inverse FFT.
    """

    # Split the image into BGR channels
    channels = cv2.split(img)
    
    # Initialize a list to store the filtered channels
    filtered_channels = []
    
    # Process each channel separately
    for channel in channels:
        # Convert to float32 for FFT (this assumes that the input is an 8-bit image)
        gray = channel.astype(np.float32)

        # Compute FFT
        fshift, magnitude = compute_fft(gray)

        # Create frequency mask
        mask = create_filter(gray.shape, filter_type, cutoff, bandwidth)

        # Apply the filter in the frequency domain
        filtered_fft = fshift * mask

        # Perform inverse FFT
        f_ishift = np.fft.ifftshift(filtered_fft)
        img_back = np.fft.ifft2(f_ishift).real

        # Clip and convert back to uint8
        img_back = np.clip(img_back, 0, 255).astype(np.uint8)
        
        # Append the processed channel
        filtered_channels.append(img_back)
    
    # Merge the filtered channels back into a single image
    img_back = cv2.merge(filtered_channels)

    # Normalize mask for visualization (use the first channel's mask for visualization)
    mask_vis = (mask * 255).astype(np.uint8)

    return img, magnitude, mask_vis, img_back

# ---------------------------------------------------------
# STEP 4 — UI function
# ---------------------------------------------------------
def process(img, filter_type, cutoff, bandwidth):
    """
    Processes the uploaded image based on the selected filter type and parameters.
    
    Args:
        img (numpy.ndarray): The uploaded image (NumPy array).
        filter_type (str): Type of filter ("Low-pass", "High-pass", or "Band-pass").
        cutoff (float): Cutoff frequency for the filter.
        bandwidth (float): Bandwidth for the band-pass filter.
        
    Returns:
        tuple: A tuple containing:
            - img (numpy.ndarray): Original image.
            - magnitude (numpy.ndarray): Magnitude of the FFT.
            - mask_vis (numpy.ndarray): Visual representation of the filter mask.
            - img_back (numpy.ndarray): The filtered image after applying the filter.
    """
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
    title="Interactive Frequency-Domain Image Filter (FFT Explorer)",
    description="See the hidden waves inside your picture and change them!"
)

if __name__ == "__main__":
    demo.launch()
