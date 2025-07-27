#!/usr/bin/env python3
"""
Advanced Upload Optimization Module
Implements compression, parallel processing, and smart retry logic
"""

import gzip
import zlib
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any

class UploadOptimizer:
    def __init__(self, supabase_client):
        self.supabase = supabase_client
        self.executor = ThreadPoolExecutor(max_workers=3)
        self.compression_threshold = 1024 * 1024  # 1MB
    
    def compress_data(self, data: bytes) -> bytes:
        """Compress data if it's larger than threshold"""
        if len(data) > self.compression_threshold:
            return gzip.compress(data)
        return data
    
    def should_compress(self, file_extension: str) -> bool:
        """Determine if file type should be compressed"""
        # Don't compress already compressed formats
        already_compressed = {'pdf', 'zip', 'gz', 'rar', '7z'}
        return file_extension.lower() not in already_compressed
    
    def upload_with_retry(self, storage_path: str, file_data: bytes, 
                         file_extension: str, max_retries: int = 3) -> Dict[str, Any]:
        """Upload with smart retry logic and compression"""
        original_size = len(file_data)
        
        # Compress if beneficial
        if self.should_compress(file_extension):
            compressed_data = self.compress_data(file_data)
            compressed_size = len(compressed_data)
            
            # Only use compression if it saves significant space (>10%)
            if compressed_size < original_size * 0.9:
                file_data = compressed_data
        
        # Upload with retry logic
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                result = self.supabase.storage.from_('resumes').upload(
                    storage_path,
                    file_data,
                    file_options={"content-type": f"application/{file_extension}"}
                )
                upload_time = time.time() - start_time
                
                return {
                    'success': True,
                    'result': result,
                    'upload_time': upload_time,
                    'original_size': original_size,
                    'uploaded_size': len(file_data),
                    'compressed': len(file_data) < original_size
                }
                
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
    
    def parallel_upload_chunks(self, file_data: bytes, storage_path: str, 
                             file_extension: str, chunk_size: int = 1024 * 1024) -> Dict[str, Any]:
        """Upload large files in parallel chunks"""
        if len(file_data) <= chunk_size:
            return self.upload_with_retry(storage_path, file_data, file_extension)
        
        # Split into chunks
        chunks = [file_data[i:i + chunk_size] for i in range(0, len(file_data), chunk_size)]
        
        # Upload chunks in parallel
        futures = []
        for i, chunk in enumerate(chunks):
            chunk_path = f"{storage_path}_part_{i}"
            future = self.executor.submit(
                self.upload_with_retry, 
                chunk_path, 
                chunk, 
                file_extension
            )
            futures.append((i, future))
        
        # Wait for all chunks to complete
        results = []
        for i, future in futures:
            try:
                result = future.result()
                results.append((i, result))
            except Exception as e:
                raise
        
        # Combine results (this is a simplified approach)
        # In practice, you'd need to implement proper chunk merging
        return {
            'success': True,
            'chunks': len(chunks),
            'total_time': sum(r[1]['upload_time'] for r in results),
            'original_size': len(file_data)
        }

def optimize_upload_performance(supabase_client, file_data: bytes, storage_path: str, 
                              file_extension: str) -> Dict[str, Any]:
    """Main optimization function"""
    optimizer = UploadOptimizer(supabase_client)
    
    # For files > 5MB, use chunked upload
    if len(file_data) > 5 * 1024 * 1024:
        return optimizer.parallel_upload_chunks(file_data, storage_path, file_extension)
    else:
        return optimizer.upload_with_retry(storage_path, file_data, file_extension) 