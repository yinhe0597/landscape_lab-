# landscape_lab/utils/file_utils.py
import os
from datetime import datetime
from fastapi import UploadFile
from pathlib import Path
from typing import Optional
from PIL import Image
from io import BytesIO
import shutil

# 文件存储根目录
UPLOAD_ROOT = Path("uploads")

def ensure_upload_dir_exists():
    """确保上传目录存在"""
    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

def save_uploaded_file(file: UploadFile, entity_id: int) -> str:
    """保存上传的文件并返回存储路径"""
    ensure_upload_dir_exists()
    
    # 创建实体专属目录
    entity_dir = UPLOAD_ROOT / str(entity_id)
    entity_dir.mkdir(exist_ok=True)
    
    # 生成唯一文件名
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_ext = Path(file.filename).suffix
    file_name = f"{timestamp}{file_ext}"
    file_path = entity_dir / file_name
    
    # 保存文件
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return str(file_path)

def generate_thumbnail(image_path: str, size: tuple = (200, 200)) -> Optional[str]:
    """生成缩略图并返回路径"""
    try:
        with Image.open(image_path) as img:
            img.thumbnail(size)
            
            # 生成缩略图路径
            path = Path(image_path)
            thumbnail_path = path.with_stem(f"{path.stem}_thumbnail")
            
            # 保存缩略图
            img.save(thumbnail_path)
            return str(thumbnail_path)
    except Exception as e:
        print(f"Error generating thumbnail: {e}")
        return None

def delete_file(file_path: str) -> bool:
    """删除文件"""
    try:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            return True
        return False
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False

def get_file_size(file_path: str) -> Optional[int]:
    """获取文件大小（字节）"""
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        print(f"Error getting file size: {e}")
        return None

def get_file_mime_type(file_path: str) -> Optional[str]:
    """获取文件MIME类型"""
    try:
        import mimetypes
        return mimetypes.guess_type(file_path)[0]
    except Exception as e:
        print(f"Error getting MIME type: {e}")
        return None

def read_file_chunks(file_path: str, chunk_size: int = 1024 * 1024):
    """读取文件分块"""
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk

def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
    """验证文件扩展名是否允许"""
    return Path(filename).suffix.lower() in allowed_extensions

def get_file_metadata(file_path: str) -> dict:
    """获取文件元数据"""
    path = Path(file_path)
    return {
        "file_name": path.name,
        "file_size": get_file_size(file_path),
        "mime_type": get_file_mime_type(file_path),
        "created_at": datetime.fromtimestamp(path.stat().st_ctime),
        "modified_at": datetime.fromtimestamp(path.stat().st_mtime)
    }
