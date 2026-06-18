"""
数学建模全流程 — 论文生成框架

主要组件：
    PaperConfig  : 论文配置（学校名、标题、字体、页边距等）
    PaperGenerator : 论文生成器（构建、结果填充、保存）
    TableBuilder : 三线表构建器
    render_latex : LaTeX → PNG 渲染
"""
from .paper_generator import PaperConfig, PaperGenerator
from .table_builder import TableBuilder
from .formula_renderer import render_latex, render_and_embed

__all__ = ['PaperConfig', 'PaperGenerator', 'TableBuilder',
           'render_latex', 'render_and_embed']
