"""Tests for the optional edge line generation feature."""

import json
import struct
from pathlib import Path

import cascadio

MODELS = Path(__file__).parent / "models"
LINES = 1
TRIANGLES = 4
JSON_CHUNK = 0x4E4F534A


def _glb_json(data):
    """Extract and parse the JSON chunk of a GLB byte string."""
    offset = 12  # magic(4) + version(4) + length(4)
    while offset < len(data):
        chunk_len, chunk_type = struct.unpack_from("<II", data, offset)
        if chunk_type == JSON_CHUNK:
            return json.loads(data[offset + 8 : offset + 8 + chunk_len])
        offset += 8 + chunk_len
    raise ValueError("GLB does not contain a JSON chunk")


def _count_primitives(gltf, mode):
    """Count primitives with the given drawing mode across all meshes."""
    return sum(
        1
        for mesh in gltf.get("meshes", [])
        for prim in mesh.get("primitives", [])
        if prim.get("mode", TRIANGLES) == mode
    )


def _load(**kwargs):
    """Convert the multibody sample and return its parsed GLB JSON."""
    data = (MODELS / "multibody.step").read_bytes()
    return _glb_json(cascadio.load(data, **kwargs))


def test_edges_add_line_primitives():
    """include_edges=True should emit extra LINES primitives."""
    with_edges = _count_primitives(_load(include_edges=True), LINES)
    without_edges = _count_primitives(_load(include_edges=False), LINES)

    assert with_edges > without_edges, (
        "expected extra LINES primitives with include_edges=True, "
        f"got {with_edges} vs {without_edges}"
    )


def test_edges_do_not_change_triangle_count():
    """Enabling edges must not alter the triangulated geometry."""
    with_edges = _count_primitives(_load(include_edges=True), TRIANGLES)
    without_edges = _count_primitives(_load(include_edges=False), TRIANGLES)

    assert with_edges == without_edges, (
        "include_edges should not change the number of TRIANGLES primitives, "
        f"got {with_edges} vs {without_edges}"
    )


def test_node_name_format_renames_nodes():
    """PRODUCT_OR_INSTANCE should rename nodes without changing their count."""
    fmt = cascadio.NodeNameFormat

    instance = _load(node_name_format=fmt.INSTANCE_OR_PRODUCT)
    product = _load(node_name_format=fmt.PRODUCT_OR_INSTANCE)

    names_instance = [node.get("name", "") for node in instance.get("nodes", [])]
    names_product = [node.get("name", "") for node in product.get("nodes", [])]

    assert names_instance, "expected named nodes in the output"
    assert len(names_instance) == len(names_product), (
        "node count should not depend on the name format"
    )
    assert names_instance != names_product, (
        "PRODUCT_OR_INSTANCE should produce different node names than "
        "INSTANCE_OR_PRODUCT"
    )
