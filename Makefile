MPY_DIR = $(HOME)/workspace/micropython

MOD = ST7735S

SRC = st7735s.c

ARCH = armv6m

CFLAGS += -DMACHINE=$(PORT)

include $(MPY_DIR)/py/dynruntime.mk

