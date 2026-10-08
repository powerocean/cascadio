"""Shared argument-parsing helpers for all CLI sub-commands."""

from __future__ import annotations

import argparse
from typing import Any


def add_input_output_args(parser: argparse.ArgumentParser) -> None:
    """Add ``-i/--input`` and ``-o/--output`` arguments."""
    parser.add_argument("-i", "--input", type=str, help="输入STP/STEP路径", required=True)
    parser.add_argument("-o", "--output", type=str, help="输出路径", required=True)


def add_sampling_args(parser: argparse.ArgumentParser) -> None:
    """Add image-sampling specific arguments."""
    parser.add_argument("-n", "--number", type=int, help="图片数量", default=60)
    parser.add_argument("-iw", "--image_width", type=float, help="图片宽度", default=1024)
    parser.add_argument("-ih", "--image_height", type=float, help="图片高度", default=1024)
    parser.add_argument(
        "-gif",
        "--gif",
        type=bool,
        help="是否生成GIF图片",
        action=argparse.BooleanOptionalAction,
        default=False,
    )


def add_material_args(parser: argparse.ArgumentParser) -> None:
    """Add material override arguments."""
    parser.add_argument(
        "-km",
        "--keep_material",
        type=bool,
        help="保持原始材质不覆写",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "-mm",
        "--override_material_metallic",
        type=float,
        help="覆写材质金属性",
        default=0.2,
    )
    parser.add_argument(
        "-mr",
        "--override_material_roughness",
        type=float,
        help="覆写材质粗糙度",
        default=0.5,
    )
    parser.add_argument(
        "-mc",
        "--override_material_color",
        type=str,
        help="覆写材质颜色 (hex)",
        default="#381F0D",
    )


def add_converter_args(parser: argparse.ArgumentParser) -> None:
    """Add STEP tolerance arguments."""
    parser.add_argument(
        "-tl",
        "--tolerance_linear",
        type=float,
        help="线性容差",
        default=0.01,
    )
    parser.add_argument(
        "-ta",
        "--tolerance_angular",
        type=float,
        help="角度容差",
        default=0.5,
    )
    parser.add_argument(
        "-tr",
        "--tolerance_relative",
        type=bool,
        help="是否使用相对容差",
        default=True,
    )
    parser.add_argument(
        "-we",
        "--with_edges",
        type=bool,
        help="是否生成边线",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument(
        "-nnf",
        "--node_name_format",
        type=str,
        choices=[
            "product",
            "instance",
            "instance_or_product",
            "product_or_instance",
            "product_and_instance",
        ],
        help="GLB节点命名格式（默认 instance_or_product）",
        default="instance_or_product",
    )


def parse_args(
    parser: argparse.ArgumentParser,
    *,
    description: str = "stp2glb tool",
) -> argparse.Namespace:
    """Finalize parser and return parsed args."""
    parser.description = description
    parser.usage = parser.format_usage().replace("usage: ", "").rstrip()
    return parser.parse_args()
