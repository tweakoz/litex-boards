#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2018 William D. Jones <thor0505@comcast.net>
# Copyright (c) 2020 Staf Verhaegen <staf@fibraservi.eu>
# SPDX-License-Identifier: BSD-2-Clause

from litex.build.generic_platform import Pins, Subsignal, IOStandard, Misc
from litex.build.xilinx import XilinxPlatform
from litex.build.openocd import OpenOCD

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst
    ("clk12", 0, Pins("L17"), IOStandard("LVCMOS33")),

    ## Buttons
    ("cpu_reset", 0, Pins("A18"), IOStandard("LVCMOS33")),
    ("user_btn", 0, Pins("B18"), IOStandard("LVCMOS33")),

    # Leds
    ("user_led", 0, Pins("A17"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("C16"), IOStandard("LVCMOS33")),

    ("rgb_led", 0,
        Subsignal("r", Pins("C17")),
        Subsignal("g", Pins("B16")),
        Subsignal("b", Pins("B17")),
        IOStandard("LVCMOS33"),
    ),

    # Serial
    ("serial", 0,
        Subsignal("tx", Pins("J18")),
        Subsignal("rx", Pins("J17")),
        IOStandard("LVCMOS33")),

    ("issiram", 0,
        Subsignal(
            "addr",
            Pins("M18 M19 K17 N17 P17 P18 R18 W19",
                 "U19 V19 W18 T17 T18 U17 U18 V16",
                 "W16 W17 V15"),
            IOStandard("LVCMOS33")),
        Subsignal(
            "data",
            Pins("W15 W13 W14 U15 U16 V13 V14 U14"),
            IOStandard("LVCMOS33")),
        Subsignal("wen", Pins("R19"), IOStandard("LVCMOS33")),
        Subsignal("cen", Pins("N19"), IOStandard("LVCMOS33")),
        Misc("SLEW=FAST"),
    ),

]

# Connectors ---------------------------------------------------------------------------------------
_connectors = [
]

# Platform -----------------------------------------------------------------------------------------

class Xc7A35t_Platform(XilinxPlatform):
    def __init__(self, io, conns ):
        XilinxPlatform.__init__(self, "xc7a35t-cpg236-1", io, conns, toolchain="vivado")
    def do_finalize(self,fragment):
        self.add_period_constraint(self.lookup_request("clk12", loose=True), self.default_clk_period)

def get_platform(base_platform):
  class the_platform(base_platform):

    def __init__(self):
        self.default_clk_name   = "clk12"
        self.default_clk_period = 1e9/12e6
        base_platform.__init__(self,_io, _connectors)

    def do_finalize(self, fragment):
        base_platform.do_finalize(self, fragment)

  return the_platform()