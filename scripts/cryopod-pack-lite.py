#!/usr/bin/env python3
"""
🧊 冷冻舱打包脚本 v0.1 Lite（标准库版本）
一键生成冷冻包 + 清单
"""

import os
import json
import hashlib
import tarfile
import argparse
from datetime import datetime

def create_manifest(files, metadata):
    """创建 manifest.json"""
    manifest = {
        "schema_version": "1.0",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "agent": metadata,
        "files": {}
    }
    
    for file_path in files:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
                file_hash = hashlib.sha256(content).hexdigest()
                manifest["files"][os.path.basename(file_path)] = {
                    "hash": file_hash,
                    "size": len(content)
                }
    
    return manifest

def create_pod(files, output_path, metadata={}):
    """创建冷冻舱（未加密，用于测试）"""
    print(f"🧊 开始创建冷冻舱...")
    print(f"   输出文件：{output_path}")
    print(f"   文件数量：{len(files)}")
    
    # 创建 manifest
    manifest = create_manifest(files, metadata)
    manifest_path = "/tmp/manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    files.append(manifest_path)
    
    # 打包文件
    with tarfile.open(output_path, "w:gz") as tar:
        for file_path in files:
            if os.path.exists(file_path):
                tar.add(file_path, arcname=os.path.basename(file_path))
    
    # 清理临时文件
    os.remove(manifest_path)
    
    # 输出信息
    print()
    print(f"✅ 冷冻舱创建成功！")
    print(f"   文件大小：{os.path.getsize(output_path):,} bytes")
    print(f"   压缩格式：tar.gz")
    print()
    print(f"📋 文件清单:")
    for filename, info in manifest["files"].items():
        print(f"   - {filename} ({info['size']:,} bytes, {info['hash'][:16]}...)")
    print()
    print(f"⚠️  注意：这是未加密版本，仅用于测试！")
    print(f"   生产环境请使用 cryopod-pack.py（需要 cryptography 模块）")
    
    return manifest

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🧊 冷冻舱打包脚本 v0.1 Lite")
    parser.add_argument("output", help="输出文件路径 (.tar.gz)")
    parser.add_argument("files", nargs="+", help="要打包的文件")
    parser.add_argument("--name", default="sandbot-lobster", help="Agent 名称")
    parser.add_argument("--version", default="V6.3", help="Agent 版本")
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    missing = [f for f in args.files if not os.path.exists(f)]
    if missing:
        print(f"❌ 文件不存在：{missing}")
        exit(1)
    
    # 元数据
    metadata = {
        "name": args.name,
        "version": args.version,
        "framework": "OpenClaw V6.3"
    }
    
    # 创建
    manifest = create_pod(args.files, args.output, metadata)
