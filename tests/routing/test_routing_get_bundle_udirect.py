from __future__ import annotations

from functools import partial

from pytest_regressions.data_regression import DataRegressionFixture

import gdsfactory as gf


def test_get_bundle_udirect_pads(
    data_regression: DataRegressionFixture, check: bool = True
) -> None:
    c = gf.Component()

    pad = partial(gf.components.pad, size=(10, 10))
    pad_south = gf.components.pad_array(orientation=270, spacing=(15.0, 0), pad=pad)
    pt = c << pad_south
    pb = c << pad_south
    pb.rotate(90)
    pt.rotate(90)
    pb.move((0, -100))

    pbports = pb.get_ports_list()
    ptports = pt.get_ports_list()

    pbports.reverse()

    routes = gf.routing.get_bundle(pbports, ptports, radius=5)

    lengths = {}
    for i, route in enumerate(routes):
        c.add(route.references)
        lengths[i] = route.length

    if check:
        data_regression.check(lengths)


if __name__ == "__main__":
    test_get_bundle_udirect_pads(None, check=False)
