"""CLI entry-point for STEP → GLB conversion.

Usage::

    stp2glb -i model.stp -o model.glb [-tl LINEAR] [-ta ANGULAR] [-tr RELATIVE]
"""

from __future__ import annotations

import argparse

from cascadio import NodeNameFormat, step_to_glb
from cascadio.common_args import add_converter_args, add_input_output_args, parse_args


def main() -> None:
    """Parse arguments and run the converter."""
    parser = argparse.ArgumentParser(description="STEP2GLB工具")
    add_input_output_args(parser)
    add_converter_args(parser)
    args = parse_args(parser)

    print(
        f"Converting: {args.input} ==> {args.output}"
        f"\n== Tolerances - Linear: {args.tolerance_linear}, "
        f"Angular: {args.tolerance_angular}, "
        f"Relative: {args.tolerance_relative} =="
        f"\n== Include edges: {args.with_edges} =="
        f"\n== Node name format: {args.node_name_format} =="
    )

    step_to_glb(
        args.input,
        args.output,
        tol_linear=args.tolerance_linear,
        tol_angular=args.tolerance_angular,
        tol_relative=args.tolerance_relative,
        include_edges=args.with_edges,
        node_name_format=NodeNameFormat[args.node_name_format.upper()],
    )


if __name__ == "__main__":
    main()
