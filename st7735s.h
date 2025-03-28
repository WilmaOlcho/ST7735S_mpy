#include "py/dynruntime.h"
#include "py/obj.h"

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
#define GAMSET  0x26 //// Gamma Set
#define DISPOFF 0x28 // Display Off
#define DISPON  0x29 // Display On
#define CASET   0x2A // Column Address Set
#define RASET   0x2B // Row Address Set
#define RAMWR   0x2C // Memory Write
#define RGBSET  0x2D // LUT table Set
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

#define GCV   0xFC // Gate Pump Clock

static const uint8_t[] no_data_commands_table = {
    NOP, SWRESET, RDDID, RDDST, RDDPM, RDDMADCTL, RDDCOLMOD,
    RDDIM, RDDSM, RDDSDR, SLPIN, SLPOUT, PTLON, NORON,
    INVOFF, INVON, DISPOFF, DISPON, RAMRD,
    TEOFF, IDMOFF, IDMON, RDID1, RDID2, RDID3
};

static const uint8_t[] _1byte_read_commands_table = {
    
};

static const uint8_t[] _1byte_write_commands_table = {
    
};

static const uint8_t[] _2byte_read_commands_table = {
    
};

static const uint8_t[] _2byte_write_commands_table = {
    
};

static const uint8_t[] _3byte_read_commands_table = {
    
};

static const uint8_t[] _3byte_write_commands_table = {
    
};

static const uint8_t[] _4byte_read_commands_table = {
    
};

static const uint8_t[] _4byte_write_commands_table = {
    
};

static const uint8_t[] _6byte_read_commands_table = {
    
};

static const uint8_t[] _6byte_write_commands_table = {
    
};

static const uint8_t[] _16byte_read_commands_table = {
    
};

static const uint8_t[] _16byte_write_commands_table = {
    
};

static const uint8_t[] _128byte_read_commands_table = {
    
};

static const uint8_t[] _128byte_write_commands_table = {
    
};

static struct machine_spi_read_write {
    mp_obj_t (*read)(mp_obj_t *self, size_t len);
    void (*write)(mp_obj_t *self, const uint8_t *data, size_t len);
};

static machine_spi_read_write extract_read_write(mp_obj_t spi) {};
static mp_obj_t LCD_ST7735S_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args_in) {};

static void LCD_ST7735S_init(mp_obj_t *self) {};
static void LCD_ST7735S_update(mp_obj_t *self) {};
static void LCD_ST7735S_on(mp_obj_t *self) {};
static void LCD_ST7735S_off(mp_obj_t *self) {};
static void LCD_ST7735S_reset(mp_obj_t *self) {};
static void LCD_ST7735S_invert(mp_obj_t *self) {};
static void LCD_ST7735S_rotation(mp_obj_t *self, mp_obj_t rotation_int) {};
static void LCD_ST7735S_fill(mp_obj_t *self, mp_obj_t color_tuple) {};
static void LCD_ST7735S_pixel(mp_obj_t *self, mp_obj_t xy_tuple, mp_obj_t color_tuple) {};
static void LCD_ST7735S_blit(mp_obj_t *self, mp_obj_t xywh_tuple, mp_obj_t buffer_bytes) {};
static void LCD_ST7735S_read(mp_obj_t *self, mp_obj_t xy_tuple, mp_obj_t amount_int) {};
static void LCD_ST7735S_write(mp_obj_t *self, mp_obj_t xy_tuple, mp_obj_t buffer_bytes) {};
static void LCD_ST7735S_set_register(mp_obj_t *self, mp_obj_t register, mp_obj_t bytes) {};
static void LCD_ST7735S_read_register(mp_obj_t *self, mp_obj_t register) {};
static void LCD_ST7735S_set_register(mp_obj_t *self, mp_obj_t register, mp_obj_t bytes) {};
static void LCD_ST7735S_read_register(mp_obj_t *self, mp_obj_t register) {};

static void ST7735S_write_command(mp_obj_t *self, uint8_t command) {};
static void ST7735S_write_data(mp_obj_t *self, int len, uint8_t[] data) {};

static const mp_obj_type_t LCD_ST7735S_type;

static void LCD_ST7735S_print(const mp_print_t *print, mp_obj_t self_in, mp_print_kind_t kind) {};

MP_DEFINE_CONST_FUN_OBJ_1(LCD_ST7735S_update_obj, LCD_ST7735S_update); //self
MP_DEFINE_CONST_FUN_OBJ_1(LCD_ST7735S_init_obj, LCD_ST7735S_init); //self
MP_DEFINE_CONST_FUN_OBJ_1(LCD_ST7735S_on_obj, LCD_ST7735S_on); //self
MP_DEFINE_CONST_FUN_OBJ_1(LCD_ST7735S_off_obj, LCD_ST7735S_off); //self
MP_DEFINE_CONST_FUN_OBJ_1(LCD_ST7735S_reset_obj, LCD_ST7735S_reset); //self
MP_DEFINE_CONST_FUN_OBJ_1(LCD_ST7735S_invert_obj, LCD_ST7735S_invert); //self
MP_DEFINE_CONST_FUN_OBJ_2(LCD_ST7735S_rotation_obj, LCD_ST7735S_rotation); //self, rotation
MP_DEFINE_CONST_FUN_OBJ_2(LCD_ST7735S_fill_obj, LCD_ST7735S_fill); //self, color
MP_DEFINE_CONST_FUN_OBJ_3(LCD_ST7735S_pixel_obj, LCD_ST7735S_pixel); //self, tuple(x,y), color
MP_DEFINE_CONST_FUN_OBJ_3(LCD_ST7735S_blit_obj, LCD_ST7735S_blit); //self,tuple(x,y,w,h), buffer
MP_DEFINE_CONST_FUN_OBJ_3(LCD_ST7735S_read_obj, LCD_ST7735S_read); //self, tuple(x,y), amount
MP_DEFINE_CONST_FUN_OBJ_3(LCD_ST7735S_write_obj, LCD_ST7735S_write); //self, tuple(x,y), buffer
MP_DEFINE_CONST_FUN_OBJ_3(LCD_ST7735S_set_register_obj, LCD_ST7735S_set_register); //self, register, bytes[value]
MP_DEFINE_CONST_FUN_OBJ_2(LCD_ST7735S_read_register_obj, LCD_ST7735S_read_register); //self, register (amount of bytes depends on register)

static const mp_rom_map_elem_t ST7735S_locals_dict_table[] = {
    // MP_ROM_QSTR defines (string in macro) dict key, MP_ROM_PTR (object pointer) defines dict value
    { MP_ROM_QSTR(MP_QSTR_update), MP_ROM_PTR(&LCD_ST7735S_update_obj) },
    { MP_ROM_QSTR(MP_QSTR_init), MP_ROM_PTR(&LCD_ST7735S_init_obj) },
    { MP_ROM_QSTR(MP_QSTR_on), MP_ROM_PTR(&LCD_ST7735S_on_obj)},
    { MP_ROM_QSTR(MP_QSTR_off), MP_ROM_PTR(&LCD_ST7735S_off_obj)},
    { MP_ROM_QSTR(MP_QSTR_reset), MP_ROM_PTR(&LCD_ST7735S_reset_obj)},
    { MP_ROM_QSTR(MP_QSTR_invert), MP_ROM_PTR(&LCD_ST7735S_invert_obj)},
    { MP_ROM_QSTR(MP_QSTR_rotation), MP_ROM_PTR(&LCD_ST7735S_rotation_obj)},
    { MP_ROM_QSTR(MP_QSTR_buffer), MP_ROM_PTR()}, //bytes
    { MP_ROM_QSTR(MP_QSTR_fill), MP_ROM_PTR(&LCD_ST7735S_fill_obj)},
    { MP_ROM_QSTR(MP_QSTR_pixel), MP_ROM_PTR(&LCD_ST7735S_pixel_obj)},
    { MP_ROM_QSTR(MP_QSTR_blit), MP_ROM_PTR(&LCD_ST7735S_blit_obj)},
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&LCD_ST7735S_read_obj)},
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&LCD_ST773S_write_obj)},
    { MP_ROM_QSTR(MP_QSTR_set_register), MP_ROM_PTR(&LCD_ST7735S_set_register_obj)},
    { MP_ROM_QSTR(MP_QSTR_read_register), MP_ROM_PTR(&LCD_ST7735S_read_register_obj)}
};

static MP_DEFINE_CONST_DICT(ST7735S_locals_dict, ST7735S_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    LCD_ST7735S_type, // type name
    LCD_ST7735S, // type print name
    MP_TYPE_FLAG_NONE, // type flags
    make_new, LCD_ST7735S_make_new, // constructor
    print, LCD_ST7735S_print, // print
    locals_dict, &ST7735S_locals_dict // locals_dict
    );

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
    machine_spi_read_write read_write;
} ST7735S_obj_t;


