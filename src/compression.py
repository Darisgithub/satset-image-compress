import numpy as np
from PIL import Image

def compress_image(image, rank):
    """Compress image using SVD"""
    # Check if image is RGB or grayscale
    if image.mode == 'L':
        # Grayscale
        img_array = np.array(image, dtype=np.float32)
        compressed = _compress_channel(img_array, rank)
        return np.clip(compressed, 0, 255).astype(np.uint8)
    else:
        # RGB/Color - compress each channel separately
        img_array = np.array(image, dtype=np.float32)
        compressed = np.zeros_like(img_array)
        
        for i in range(img_array.shape[2]):  # For each channel
            compressed[:, :, i] = _compress_channel(img_array[:, :, i], rank)
        
        return np.clip(compressed, 0, 255).astype(np.uint8)

def _compress_channel(channel, rank):
    """Compress single channel using SVD"""
    U, S, VT = np.linalg.svd(channel, full_matrices=False)
    compressed = U[:, :rank] @ np.diag(S[:rank]) @ VT[:rank, :]
    
    # Normalize to original range
    min_val = compressed.min()
    max_val = compressed.max()
    if max_val > min_val:
        compressed = (compressed - min_val) / (max_val - min_val) * 255
    
    return compressed