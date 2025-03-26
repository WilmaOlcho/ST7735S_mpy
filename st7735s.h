#include "py/dynruntime.h"

#define NOP     0x00 // No Operation
#define SWRESET 0x01 // Software Reset
#define RDDID   0x04 // Read Display ID
#define RDDST   0x09 // Read Display Status
#define RDDPM   0x0A // Read Display Power Mode
#define RDDMADCTL 0x0B // Read Display MADCTL
#define RDDCOLMOD 0x0C // Read Display Pixel Format
#define RDDIM   0x0D // Read Display Image Mode
#define RDDSM   0x0E // Read Display Signal Mode
#define RDDSDR  0x0F // Read Display Self-Diagnostic Result

#define SLPIN   0x10 // Sleep In
#define SLPOUT  0x11 // Sleep Out
#define PTLON   0x12 // Partial Mode On
#define NORON   0x13 // Normal Display Mode On

#define INVOFF  0x20 // Display Inversion Off
#define INVON   0x21 // Display Inversion On
#define GAMSET  0x26 // Gamma Set
#define DISPOFF 0x28 // Display Off
#define DISPON  0x29 // Display On
#define CASET   0x2A // Column Address Set
#define RASET   0x2B // Row Address Set
#define RAMWR   0x2C // Memory Write
#define RAMRD   0x2E // Memory Read

#define PTLAR   0x30 // Partial Area
#define SCRLAR  0x33 // Scroll Area Set
#define TEOFF   0x34 // Tearing Effect Line Off
#define TEON    0x35 // Tearing Effect Line On
#define MADCTL  0x36 // Memory Data Access Control
#define VSCSAD  0x37 // Vertical Scroll Start Address
#define IDMOFF  0x38 // Idle Mode Off
#define IDMON   0x39 // Idle Mode On
#define COLMOD  0x3A // Interface Pixel Format

#define FRMCTR1 0xB1 // Frame Rate Control (In Normal Mode/Full Colors)
#define FRMCTR2 0xB2 // Frame Rate Control (In Idle Mode/8 colors)
#define FRMCTR3 0xB3 // Frame Rate control (In Partial Mode/Full Colors)
#define INVCTR  0xB4 // Display Inversion Control

#define PWCTR1  0xC0 // Power Control 1
#define PWCTR2  0xC1 // Power Control 2
#define PWCTR3  0xC2 // Power Control 3 (in Normal Mode/Full Colors)
#define PWCTR4  0xC3 // Power Control 4 (in Idle Mode/8 colors)
#define PWCTR5  0xC4 // Power Control 5 (in Partial Mode/Full Colors)
#define VMCTR1  0xC5 // VCOM Control 1
#define VMOFCTR 0xC7 // VCOM Offset Control

//#define WRID1   0xD0 // Write ID1 Value // Not documented
#define WRID2   0xD1 // Write ID2 Value
#define WRID3   0xD2 // Write ID3 Value
#define NVFCTR1 0xD9 // NVM Control Status
#define RDID1   0xDA // Read ID1 Value
#define RDID2   0xDB // Read ID2 Value
#define RDID3   0xDC // Read ID3 Value
#define NVFCTR2 0xDE // NVM Read Command
#define NVFCTR3 0xDF // NVM Write Command

#define GMCTRP1 0xE0 // Gamma + correction
#define GMCTRN1 0xE1 // Gamma - correction

#define GCV   0xFC // Gate Control Value

typedef struct machine_spi_obj_t{
    mp_obj_base_t base;
    spi_inst_t *const spi_inst;
    uint8_t spi_id;
    uint8_t polarity;
    uint8_t phase;
    uint8_t bits;
    uint8_t firstbit;
    uint8_t sck;
    uint8_t mosi;
    uint8_t miso;
    uint32_t baudrate;
} machine_spi_obj_t;

typedef struct _st7735s_obj_t {
    mp_obj_base_t base;
    machine_spi_obj_t spi_bus;
    int cs;
    int dc;
    int rst;
    int bl;
    int width;
    int height;
    int rotation;
    int invert;
    int color_mode;
} st7735s_obj_t;


