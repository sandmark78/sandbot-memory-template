#!/usr/bin/env python3
"""
增强学习机制模块
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Any
import hashlib

class LearningMechanism:
    """增强学习机制实现"""
    
    def __init__(self, knowledge_base_path="knowledge_base.json"):
        self.knowledge_base_path = knowledge_base_path
        self.knowledge_base = self._load_knowledge_base()
        self.learning_rate = 0.7
        self.experience_buffer = []
        
    def _load_knowledge_base(self) -> Dict:
        """加载知识库"""
        if os.path.exists(self.knowledge_base_path):
            with open(self.knowledge_base_path, 'r') as f:
                return json.load(f)
        return {
            "patterns": {},
            "experiences": [],
            "success_metrics": {},
            "last_updated": datetime.utcnow().isoformat() + "Z"
        }
        
    def _save_knowledge_base(self):
        """保存知识库"""
        self.knowledge_base["last_updated"] = datetime.utcnow().isoformat() + "Z"
        with open(self.knowledge_base_path, 'w') as f:
            json.dump(self.knowledge_base, f, indent=2)
            
    def extract_pattern(self, input_data: str, output_data: str, context: Dict = None) -> str:
        """从输入输出对中提取模式"""
        pattern_key = hashlib.md5(f"{input_data}:{output_data}".encode()).hexdigest()
        pattern = {
            "input": input_data,
            "output": output_data,
            "context": context or {},
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "usage_count": 1,
            "success_rate": 1.0
        }
        return pattern_key, pattern
        
    def learn_from_experience(self, experience: Dict):
        """从经验中学习"""
        # 添加到经验缓冲区
        self.experience_buffer.append(experience)
        
        # 如果是成功经验，提取模式
        if experience.get("success", False):
            pattern_key, pattern = self.extract_pattern(
                experience["input"], 
                experience["output"],
                experience.get("context")
            )
            
            # 更新知识库
            if pattern_key in self.knowledge_base["patterns"]:
                existing = self.knowledge_base["patterns"][pattern_key]
                existing["usage_count"] += 1
                existing["success_rate"] = (
                    existing["success_rate"] * (existing["usage_count"] - 1) + 1.0
                ) / existing["usage_count"]
            else:
                self.knowledge_base["patterns"][pattern_key] = pattern
                
            # 添加到经验列表
            self.knowledge_base["experiences"].append(experience)
            
        # 定期保存知识库
        if len(self.experience_buffer) % 10 == 0:
            self._save_knowledge_base()
            
    def recall_similar_patterns(self, input_query: str, threshold: float = 0.5) -> List[Dict]:
        """回忆相似模式"""
        similar_patterns = []
        
        for pattern_key, pattern in self.knowledge_base["patterns"].items():
            similarity = self._calculate_similarity(input_query, pattern["input"])
            if similarity >= threshold:
                similar_patterns.append({
                    "pattern": pattern,
                    "similarity": similarity
                })
                
        # 按相似度排序
        similar_patterns.sort(key=lambda x: x["similarity"], reverse=True)
        return similar_patterns[:5]  # 返回前5个最相似的
        
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度（简化实现）"""
        # 简化的相似度计算 - 实际中会使用更复杂的算法
        if text1 == text2:
            return 1.0
        elif text1 in text2 or text2 in text1:
            return 0.8
        elif set(text1.split()) & set(text2.split()):
            return 0.6
        else:
            return 0.2
            
    def adapt_behavior(self, context: Dict) -> Dict:
        """基于学习结果调整行为"""
        # 这里可以实现更复杂的行为适应逻辑
        adaptation = {
            "learning_rate": self.learning_rate,
            "confidence": 0.9,
            "recommended_action": "continue_learning",
            "context_analysis": context
        }
        return adaptation
        
    def get_learning_status(self) -> Dict:
        """获取学习状态"""
        return {
            "knowledge_base_size": len(self.knowledge_base["patterns"]),
            "total_experiences": len(self.knowledge_base["experiences"]),
            "learning_rate": self.learning_rate,
            "last_updated": self.knowledge_base["last_updated"]
        }

# 示例使用
if __name__ == "__main__":
    learner = LearningMechanism("test_knowledge_base.json")
    
    # 模拟学习经验
    experience1 = {
        "input": "用户请求系统状态",
        "output": "返回CPU、内存、响应时间等指标",
        "context": {"user_type": "admin", "priority": "high"},
        "success": True,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    experience2 = {
        "input": "执行自主意识提升任务",
        "output": "按步骤完成四个阶段的优化",
        "context": {"task_complexity": "medium", "time_allocated": "1h"},
        "success": True,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    learner.learn_from_experience(experience1)
    learner.learn_from_experience(experience2)
    
    print("学习状态:", learner.get_learning_status())
    
    # 测试模式回忆
    similar = learner.recall_similar_patterns("查询系统状态")
    print(f"找到 {len(similar)} 个相似模式")
    
    learner._save_knowledge_base()