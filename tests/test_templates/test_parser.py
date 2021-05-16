from sympy.core.symbol import Symbol
from sympy.matrices import Matrix
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


def test_parse_fields():
    test = {
        "fields": [
            {
                "name": "L",
                "description": "Left handed lepton",
                "spin": "1/2",
                "mass": "m_L",
                "representations": [
                    {"name": "U(1)_Y", "charge": "1/6"},
                    {"name": "SU(2)_L", "charge": "2", "representation": [1]}
                ]
            }
        ]
    }

    result1 = TemplateParser.parse_fields(test)
    assert result1 is not None

    with pytest.raises(TemplateError, match="No fields defined"):
        TemplateParser.parse_fields({})

    with pytest.raises(TemplateError, match="Each fields name must be unique"):
        TemplateParser.parse_fields({"fields": [
            dict(name="L", spin=0), dict(name="L",spin=0)]
        })

    with pytest.raises(TemplateError, match="Field must have a name and spin"):
        TemplateParser.parse_fields({"fields": [
            dict(name="L")]
        })

    with pytest.raises(TemplateError, match="Spin is not integer or half integer"):
        TemplateParser.parse_fields({"fields": [
            dict(name="L", spin=1/3)]
        })

def test_zoo():
    model = {
        "name": "Standard Model",
        "gauges": [
            {
                "name": "U(1)_Y",
                "group_type": "abelian",
                "coupling": "g_Y"
            },
            {
                "name": "SU(2)_L",
                "group_type": ["SU", "2"],
                "coupling": "g_L"
            },
            {
                "name": "SU(2)_R",
                "group_type": ["SU", "2"],
                "coupling": "g_R"
            }
        ],
        "fields": [
            {
                "name": "L",
                "description": "Left handed lepton",
                "spin": "1/2",
                "mass": "m_L",
                "representations": [
                    {"name": "U(1)_Y", "charge": "1/6"},
                    {"name": "SU(2)_L", "charge": "2", },
                    {"name": "SU(2)_R", "representation": [2]}
                ]
            }
        ]
    }

    t = TemplateParser()
    t.template = model

    result = t.parse().build()
    assert result.fields[0].representations["SU(2)_L"]["representation"] == Matrix([[1]])
    assert result.fields[0].representations["SU(2)_R"]["charge"].numeric_dim == 3