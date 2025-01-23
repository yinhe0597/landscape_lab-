# landscape_lab/utils/file_utils.py
import os
from pathlib import Path
from fastapi import UploadFile
from typing import Optional
from PIL import Image
import shutil

# 项目文件存储根目录
PROJECT_FILES_ROOT = "data/projects"
# 材料图片存储根目录
MATERIAL_IMAGES_ROOT = "data/materials"

def ensure_directory_exists(path: str) -> None:
    """确保目录存在，如果不存在则创建"""
    Path(path).mkdir(parents=True, exist_ok=True)

def save_project_file(project_id: int, file: UploadFile) -> str:
    """保存项目文件"""
    project_dir = os.path.join(PROJECT_FILES_ROOT, str(project_id))
    ensure_directory_exists(project_dir)
    
    # 生成唯一文件名
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{os.urandom(8).hex()}{file_extension}"
    file_path = os.path.join(project_dir, unique_filename)
    
    # 保存文件
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return file_path

def save_material_image(material_id: int, image: UploadFile) -> str:
    """保存材料图片并生成缩略图"""
    material_dir = os.path.join(MATERIAL_IMAGES_ROOT, str(material_id))
    ensure_directory_exists(material_dir)
    
    # 生成唯一文件名
    file_extension = os.path.splitext(image.filename)[1]
    unique_filename = f"{os.urandom(8).hex()}{file_extension}"
    image_path = os.path.join(material_dir, unique_filename)
    
    # 保存原始图片
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    # 生成缩略图
    thumbnail_path = os.path.join(material_dir, f"thumb_{unique_filename}")
    with Image.open(image_path) as img:
        img.thumbnail((200, 200))
        img.save(thumbnail_path)
    
    return image_path

def delete_project_files(project_id: int) -> bool:
    """删除项目相关文件"""
    project_dir = os.path.join(PROJECT_FILES_ROOT, str(project_id))
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
        return True
    return False

def delete_material_images(material_id: int) -> bool:
    """删除材料相关图片"""
    material_dir = os.path.join(MATERIAL_IMAGES_ROOT, str(material_id))
    if os.path.exists(material_dir):
        shutil.rmtree(material_dir)
        return True
    return False

def get_file_size(file_path: str) -> Optional[int]:
    """获取文件大小（字节）"""
    if os.path.exists(file_path):
        return os.path.getsize(file_path)
    return None

def get_file_extension(file_path: str) -> str:
    """获取文件扩展名"""
    return os.path.splitext(file_path)[1].lower()

def is_image_file(file_path: str) -> bool:
    """判断文件是否为图片"""
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    return get_file_extension(file_path) in image_extensions

def is_document_file(file_path: str) -> bool:
    """判断文件是否为文档"""
    document_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
    return get_file_extension(file_path) in document_extensions

def is_design_file(file_path: str) -> bool:
    """判断文件是否为设计文件"""
    design_extensions = ['.dwg', '.dxf', '.skp', '.3ds', '.fbx', '.obj']
    return get_file_extension(file_path) in design_extensions
