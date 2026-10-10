#!/usr/bin/env python3
"""Build complete CS XI and CS XII sketchnote PDFs."""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from engine import SketchDoc
import content_xi
import content_xii


def main():
    out_dir = os.path.join(HERE, "output")
    os.makedirs(out_dir, exist_ok=True)

    xi_path = os.path.join(out_dir, "CS_XI_Complete_Sketchnotes.pdf")
    xii_path = os.path.join(out_dir, "CS_XII_Complete_Sketchnotes.pdf")

    print("Building CS XI sketchnotes…")
    xi = SketchDoc(xi_path, book="XI", subtitle="Computer Systems through Digital Literacy")
    content_xi.build(xi)
    p1, n1 = xi.save()
    print(f"  wrote {p1}  ({n1} pages, {os.path.getsize(p1)} bytes)")

    print("Building CS XII sketchnotes…")
    xii = SketchDoc(xii_path, book="XII", subtitle="HCI through Digital Entrepreneurship")
    content_xii.build(xii)
    p2, n2 = xii.save()
    print(f"  wrote {p2}  ({n2} pages, {os.path.getsize(p2)} bytes)")


if __name__ == "__main__":
    main()
