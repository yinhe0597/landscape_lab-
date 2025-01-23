# landscape_lab/utils/analysis_utils.py
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime
import numpy as np
from pathlib import Path
import json
import trimesh
import ezdxf
from collections import defaultdict

def analyze_plant_distribution(fbx_path: str) -> Dict[str, Any]:
    """分析FBX文件中的植物分布"""
    try:
        # 加载FBX文件
        scene = trimesh.load(fbx_path)
        
        # 统计植物信息
        plant_stats = defaultdict(lambda: {"count": 0, "positions": []})
        
        # 遍历场景中的节点
        for node in scene.graph.nodes_geometry:
            name = node[1]
            if "plant" in name.lower():
                # 获取植物位置
                transform = scene.graph.get(node)[0]
                position = transform[:3, 3]
                
                # 更新统计信息
                plant_stats[name]["count"] += 1
                plant_stats[name]["positions"].append(position.tolist())
        
        # 计算覆盖面积
        total_area = calculate_coverage_area(plant_stats)
        
        return {
            "plant_stats": dict(plant_stats),
            "total_area": total_area,
            "plant_count": sum(info["count"] for info in plant_stats.values())
        }
    except Exception as e:
        print(f"Error analyzing FBX file: {e}")
        return {}

def calculate_coverage_area(plant_stats: Dict[str, Any]) -> float:
    """计算植物覆盖面积"""
    try:
        # 将所有植物位置合并
        all_positions = []
        for info in plant_stats.values():
            all_positions.extend(info["positions"])
        
        if not all_positions:
            return 0.0
            
        # 计算凸包面积
        points = np.array(all_positions)
        hull = trimesh.convex.convex_hull(points)
        return hull.area
    except Exception as e:
        print(f"Error calculating coverage area: {e}")
        return 0.0

def generate_plant_report(analysis_result: Dict[str, Any], output_path: str) -> bool:
    """生成植物统计报告"""
    try:
        # 创建DataFrame
        data = []
        for plant_name, info in analysis_result["plant_stats"].items():
            data.append({
                "Plant Name": plant_name,
                "Count": info["count"],
                "Positions": json.dumps(info["positions"])
            })
        
        df = pd.DataFrame(data)
        
        # 添加汇总信息
        summary = pd.DataFrame([{
            "Plant Name": "TOTAL",
            "Count": analysis_result["plant_count"],
            "Positions": f"Coverage Area: {analysis_result['total_area']:.2f} m²"
        }])
        
        df = pd.concat([df, summary], ignore_index=True)
        
        # 保存为Excel文件
        df.to_excel(output_path, index=False)
        return True
    except Exception as e:
        print(f"Error generating report: {e}")
        return False

def parse_dxf_file(dxf_path: str) -> Dict[str, Any]:
    """解析DXF文件"""
    try:
        doc = ezdxf.readfile(dxf_path)
        msp = doc.modelspace()
        
        # 统计元素
        element_stats = defaultdict(int)
        for entity in msp:
            element_stats[entity.dxftype()] += 1
        
        # 获取元数据
        metadata = {
            "file_version": doc.dxfversion,
            "layer_count": len(doc.layers),
            "block_count": len(doc.blocks),
            "entity_count": len(msp)
        }
        
        return {
            "element_stats": dict(element_stats),
            "metadata": metadata
        }
    except Exception as e:
        print(f"Error parsing DXF file: {e}")
        return {}

def calculate_sunlight_exposure(positions: List[List[float]], 
                              date: datetime,
                              latitude: float,
                              longitude: float) -> List[float]:
    """计算日照时间"""
    try:
        from suncalc import get_position
        import math
        
        exposures = []
        for pos in positions:
            # 计算太阳位置
            sun_pos = get_position(date, latitude, longitude)
            
            # 计算日照因子（简化模型）
            altitude = math.radians(sun_pos["altitude"])
            azimuth = math.radians(sun_pos["azimuth"])
            
            # 假设地形平坦，计算太阳照射角度
            exposure = max(0, math.sin(altitude))
            exposures.append(exposure)
        
        return exposures
    except Exception as e:
        print(f"Error calculating sunlight exposure: {e}")
        return []
