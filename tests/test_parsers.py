from particlezoo.parsers import group_lookup, open_file, consume_config
from particlezoo.extensions import U1
import yaml
import toml
from liesym import SU


def test_group_lookup():
    name = "SU_3"

    grp = group_lookup(name)

    assert grp == SU(3)

    name2 = "U_1"
    grp2 = group_lookup(name2)
    assert grp2 == U1()


def test_yaml():
    ex = """\
name: "My Model"
version: "v0.0.1"
description: "This is a test"
symmetries:
  - group: SU_3
    name: SU3_c
  - group: SU_2
    name: SU2_L
    description: Left handed
  - group: U_1
    name: U1_Y
    description: Phase
fields:
  - name: E_L
    spin: 1/2
    description: Left handed Electron
    representations:
      SU3_c: [1,0]
      SU2_L: 2
      U1_Y: 1/6   
"""
    data = open_file(ex, opener=yaml.safe_load)
    consume_config(data)


def test_toml():
    ex = """\
name="My Model"
version="v0.0.1"
description="This is a test"
[[symmetries]]
group="SU_3"
name="SU3_c"
[[symmetries]]
group="SU_2"
name="SU2_L"
description="Left handed"
[[symmetries]]
group="U_1"
name="U1_Y"
description="Phase"
[[fields]]
name="E_L"
spin="1/2"
description="Left handed Electron"
[fields.representations]
SU3_c=[1,0,]
SU2_L=2
U1_Y="1/6"  
"""
    data = open_file(ex, opener=toml.loads)
    consume_config(data)
