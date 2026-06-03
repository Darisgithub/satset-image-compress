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

def compress_image_with_svd_data(image, rank):
    """Compress image using SVD and return singular values for analysis
    
    Returns:
        compressed_image: Compressed image array
        singular_values: Dictionary with singular value data for each channel
    """
    singular_values = {}
    
    if image.mode == 'L':
        # Grayscale
        img_array = np.array(image, dtype=np.float32)
        compressed, S = _compress_channel_with_svd(img_array, rank)
        singular_values['L'] = S
        return np.clip(compressed, 0, 255).astype(np.uint8), singular_values
    else:
        # RGB/Color - compress each channel separately
        img_array = np.array(image, dtype=np.float32)
        compressed = np.zeros_like(img_array)
        
        for i in range(img_array.shape[2]):  # For each channel
            compressed[:, :, i], S = _compress_channel_with_svd(img_array[:, :, i], rank)
            channel_name = ['R', 'G', 'B'][i] if img_array.shape[2] == 3 else str(i)
            singular_values[channel_name] = S
        
        return np.clip(compressed, 0, 255).astype(np.uint8), singular_values

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

def _compress_channel_with_svd(channel, rank):
    """Compress single channel using SVD and return singular values"""
    U, S, VT = np.linalg.svd(channel, full_matrices=False)
    compressed = U[:, :rank] @ np.diag(S[:rank]) @ VT[:rank, :]
    
    # Normalize to original range
    min_val = compressed.min()
    max_val = compressed.max()
    if max_val > min_val:
        compressed = (compressed - min_val) / (max_val - min_val) * 255
    
    return compressed, S