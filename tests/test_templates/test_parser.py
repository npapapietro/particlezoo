from particlezoo.exceptions import TemplateError
from liesym import A
from particlezoo.modeltemplates import TemplateParser
import pytest


def test_parse_name():
    example_good = {
        "name": "A model"
    }

    assert TemplateParser.parse_name(example_good) == "A model"

    example_bad = {}
    with pytest.raises(TemplateError):
        TemplateParser.parse_name(example_bad)


def test_parse_gauges():
    gauges_simple_groups = {"gauges": [{
        "name": "U1",
        "group_type": "abelian",
        "coupling": "g_1",
        "description": "test1"
    },
        {
        "name": "SU2",
        "group_type": ["SU", 2],
        "coupling": {"name": "g_2", "value": 0.1, "reference_value": 100},
        "description": "test1"
    }]}

    result1 = TemplateParser.parse_gauges(gauges_simple_groups)
    assert result1[0].algebra.backend is None
    assert result1[1].algebra.backend == A(1)

    gauge_no_coupling = {"gauges": [{
        "name": "U1",
        "group_type": "abelian",
        "description": "test1"
    }]}
    with pytest.raises(TemplateError):
        TemplateParser.parse_gauges(gauge_no_coupling)

    gauge_no_grps = {"gauges": []}
    with pytest.raises(TemplateError):
        TemplateParser.parse_gauges(gauge_no_grps)