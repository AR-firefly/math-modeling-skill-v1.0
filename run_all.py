#!/usr/bin/env python3
"""
一键全流程：安装依赖 → 模型求解 → 论文生成 → 结果汇总

用法：
    python run_all.py

不需要分两步跑 main.py 再跑 paper_generator.py，
这个脚本自动完成：
    1. 检查依赖
    2. 运行 examples/main.py（求解所有Phase）
    3. 自动检测 results.json
    4. 运行 src/math_modeling/paper_generator.py（生成论文）
    5. 打印汇总
"""
import os
import sys
import subprocess
import json

ROOT = os.path.dirname(os.path.abspath(__file__))
EXAMPLES_DIR = os.path.join(ROOT, 'examples')
RESULTS_DIR = os.path.join(EXAMPLES_DIR, 'results')
RESULTS_JSON = os.path.join(RESULTS_DIR, 'results.json')
PAPER_GEN = os.path.join(ROOT, 'src', 'math_modeling', 'paper_generator.py')
OUTPUT_DIR = os.path.join(EXAMPLES_DIR, 'sample_output')

# 确保 math_modeling 可导入（优先 pip，失败则 sys.path）
try:
    from math_modeling import PaperConfig, PaperGenerator
except ImportError:
    sys.path.insert(0, os.path.join(ROOT, 'src'))
    from math_modeling import PaperConfig, PaperGenerator


def check_deps():
    """检查依赖是否安装"""
    missing = []
    for mod in ['numpy', 'matplotlib', 'docx']:
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    if missing:
        print(f"[run_all] 安装依赖: {', '.join(missing)}")
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '-r',
             os.path.join(ROOT, 'requirements.txt'), '-q'])
        print("[run_all] 依赖安装完成")
    else:
        print("[run_all] 依赖已就绪")


def run_solver():
    """运行求解主流程"""
    print("=" * 60)
    print("  阶段1: 模型求解 (examples/main.py)")
    print("=" * 60)
    result = subprocess.run(
        [sys.executable, os.path.join(EXAMPLES_DIR, 'main.py')],
        cwd=EXAMPLES_DIR,
        capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("[run_all] 求解失败!")
        print(result.stderr)
        return False
    print("[run_all] 求解完成")
    return True


def generate_paper():
    """生成论文"""
    if not os.path.exists(RESULTS_JSON):
        print(f"[run_all] 未检测到 {RESULTS_JSON}，跳过论文生成")
        return False

    print("=" * 60)
    print("  阶段2: 论文生成")
    print("=" * 60)

    # 注入结果并生成
    with open(RESULTS_JSON, 'r', encoding='utf-8') as f:
        results = json.load(f)

    title = 'AGV协同调度与能耗优化问题研究'
    config = PaperConfig(title=title, school_name='XX大学')
    gen = PaperGenerator(config, result_dir=RESULTS_DIR)
    gen.set_results(results)
    gen.build()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f'{title}.docx')
    gen.save(out_path)
    size = os.path.getsize(out_path) / 1024
    print(f"[run_all] 论文已生成: {out_path} ({size:.0f} KB)")
    return True


def print_summary():
    """打印汇总"""
    print("=" * 60)
    print("  全流程完成!")
    print("=" * 60)
    print()

    if os.path.exists(RESULTS_JSON):
        with open(RESULTS_JSON, 'r') as f:
            r = json.load(f)
        p1 = r.get('phase1', {})
        p2 = r.get('phase2', {})
        p3 = r.get('phase3', {})
        p4 = r.get('phase4', {})
        print(f"  Phase1 TSP:       {p1.get('dp_distance', '?'):>8.2f} m")
        print(f"  Phase2 Makespan:  {p2.get('makespan', '?'):>8.1f} s")
        print(f"  Phase3 Knee:      {p3.get('knee_time', '?'):>8.1f} s / "
              f"{p3.get('knee_energy', '?'):>.1f} kJ")
        print(f"  Phase4 改善:      makespan {p4.get('mksp_improve', '?'):>+.1f}%, "
              f"energy {p4.get('energy_improve', '?'):>+.1f}%")
        print()

    sample_dir = os.path.join(OUTPUT_DIR, '示例论文_完整版.docx')
    fp = os.path.join(OUTPUT_DIR, 'AGV协同调度与能耗优化问题研究.docx')
    if os.path.exists(fp):
        print(f"  [论文] {fp}")
    if os.path.exists(RESULTS_DIR):
        files = [f for f in os.listdir(RESULTS_DIR) if f.endswith('.png')]
        print(f"  [图表] {len(files)} images in {RESULTS_DIR}/")
    print()


def main():
    print("=" * 60)
    print("  数学建模全流程 Skill — 一键运行")
    print("  (示例数据，仅用于演示框架功能)")
    print("=" * 60)
    print()

    check_deps()
    if not run_solver():
        sys.exit(1)
    generate_paper()
    print_summary()

    print("[run_all] 完成!")


if __name__ == '__main__':
    main()
