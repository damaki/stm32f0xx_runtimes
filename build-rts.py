# This script extends bb-runtimes to define the stm32f0xx target

import sys
import os
import pathlib

# Add bb-runtimes to the search path so that we can include and extend it
sys.path.append(str(pathlib.Path(__file__).parent / "bb-runtimes"))

import arm.cortexm
import build_rts
from support import add_source_search_path


class Stm32F0(arm.cortexm.CortexM0CommonArchSupport):
    @property
    def name(self):
        return "stm32f0xx"

    @property
    def use_semihosting_io(self):
        return True

    @property
    def loaders(self):
        return ("ROM", "RAM")

    def __init__(self):
        super(Stm32F0, self).__init__()

        self.add_linker_script("stm32f0_src/common-RAM.ld")
        self.add_linker_script("stm32f0_src/common-ROM.ld")

        self.add_linker_script("stm32f0_src/memory-map-RAM-16-4.ld")
        self.add_linker_script("stm32f0_src/memory-map-RAM-16-6.ld")
        self.add_linker_script("stm32f0_src/memory-map-RAM-16-8.ld")
        self.add_linker_script("stm32f0_src/memory-map-RAM-32-4.ld")
        self.add_linker_script("stm32f0_src/memory-map-RAM-32-6.ld")
        self.add_linker_script("stm32f0_src/memory-map-RAM-32-8.ld")
        self.add_linker_script("stm32f0_src/memory-map-RAM-64-8.ld")
        self.add_linker_script("stm32f0_src/memory-map-RAM-64-16.ld")
        self.add_linker_script("stm32f0_src/memory-map-RAM-128-16.ld")
        self.add_linker_script("stm32f0_src/memory-map-RAM-128-32.ld")
        self.add_linker_script("stm32f0_src/memory-map-RAM-256-32.ld")

        self.add_linker_script("stm32f0_src/memory-map-ROM-16-4.ld")
        self.add_linker_script("stm32f0_src/memory-map-ROM-16-6.ld")
        self.add_linker_script("stm32f0_src/memory-map-ROM-16-8.ld")
        self.add_linker_script("stm32f0_src/memory-map-ROM-32-4.ld")
        self.add_linker_script("stm32f0_src/memory-map-ROM-32-6.ld")
        self.add_linker_script("stm32f0_src/memory-map-ROM-32-8.ld")
        self.add_linker_script("stm32f0_src/memory-map-ROM-64-8.ld")
        self.add_linker_script("stm32f0_src/memory-map-ROM-64-16.ld")
        self.add_linker_script("stm32f0_src/memory-map-ROM-128-16.ld")
        self.add_linker_script("stm32f0_src/memory-map-ROM-128-32.ld")
        self.add_linker_script("stm32f0_src/memory-map-ROM-256-32.ld")

        # We use our own version of System.BB.Parameters
        self.remove_source("s-bbpara.ads")

        # Common source files
        self.add_gnat_sources(
            "stm32f0_src/s-stm32.ads",
            "stm32f0_src/s-stm32.adb",
            "stm32f0_src/start-rom.S",
            "stm32f0_src/start-ram.S",
            "stm32f0_src/setup_pll.ads",
            "stm32f0_src/setup_pll.adb",
            "stm32f0_src/s-bbpara.ads",
            "stm32f0_src/s-bbbopa.ads",
            "stm32f0_src/s-bbmcpa-full.ads",
            "stm32f0_src/s-bbmcpa-simple.ads",
            "stm32f0_src/stm32f0x0/svd/i-stm32_0.ads",
            "stm32f0_src/stm32f0x1/svd/i-stm32_1.ads",
            "stm32f0_src/stm32f0x2/svd/i-stm32_2.ads",
            "stm32f0_src/stm32f0x8/svd/i-stm32_8.ads",
            "stm32f0_src/stm32f0x0/svd/i-stm32-flash_0.ads",
            "stm32f0_src/stm32f0x1/svd/i-stm32-flash_1.ads",
            "stm32f0_src/stm32f0x2/svd/i-stm32-flash_2.ads",
            "stm32f0_src/stm32f0x8/svd/i-stm32-flash_8.ads",
            "stm32f0_src/stm32f0x0/svd/i-stm32-rcc_0.ads",
            "stm32f0_src/stm32f0x1/svd/i-stm32-rcc_1.ads",
            "stm32f0_src/stm32f0x2/svd/i-stm32-rcc_2.ads",
            "stm32f0_src/stm32f0x8/svd/i-stm32-rcc_8.ads",
        )

        # Choose interrupt names based on family
        self.add_gnarl_sources(
            "stm32f0_src/stm32f0x0/svd/a-intnam_0.ads",
            "stm32f0_src/stm32f0x1/svd/a-intnam_1.ads",
            "stm32f0_src/stm32f0x2/svd/a-intnam_2.ads",
            "stm32f0_src/stm32f0x8/svd/a-intnam_8.ads",
        )


def build_configs(target):
    if target == "stm32f0xx":
        return Stm32F0()
    else:
        assert False, "unexpected target: %s" % target

def patch_bb_runtimes():
    """Patch some parts of bb-runtimes to use our own targets and data"""
    add_source_search_path(os.path.dirname(__file__))

    build_rts.build_configs = build_configs

if __name__ == "__main__":
    patch_bb_runtimes()
    build_rts.main()