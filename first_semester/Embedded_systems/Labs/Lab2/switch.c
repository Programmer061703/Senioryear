#include "xil_printf.h"
#include <sys/_intsup.h>

#define AXI_GPIO_0_BASE_ADDR 0x40000000

#define GREEN_LEDS_BASE_ADDR (AXI_GPIO_0_BASE_ADDR)
#define PUSH_BTNS_BASE_ADDR  (AXI_GPIO_0_BASE_ADDR + 8)

#define GREEN_LEDS_REG (unsigned *)(GREEN_LEDS_BASE_ADDR)
#define PUSH_BTNS_REG (unsigned *)(PUSH_BTNS_BASE_ADDR)

#define AXI_GPIO_1_BASE_ADDR 0x40010000

#define RGB_LEDS_BASE_ADDR (AXI_GPIO_1_BASE_ADDR)
#define PUSH_SWT_BASE_ADDR (AXI_GPIO_1_BASE_ADDR + 8)

#define RGB_LEDS_REG (unsigned *)(RGB_LEDS_BASE_ADDR)
#define PUSH_SWT_REG (unsigned *)(PUSH_SWT_BASE_ADDR)

int main(void)
{
    unsigned *greenLEDsData = GREEN_LEDS_REG;
    unsigned *greenLEDsTri  = GREEN_LEDS_REG + 1;

    unsigned *buttonsData = PUSH_BTNS_REG;
    unsigned *buttonsTri  = PUSH_BTNS_REG + 1;

    unsigned *rgbLEDsData = RGB_LEDS_REG;
    unsigned *rgbLEDsTri = RGB_LEDS_REG + 1;

    unsigned *switchData = PUSH_SWT_REG;
    unsigned *switchTri = PUSH_SWT_REG +1;

    print("\r\nBegin...\r\n\r\n\tRegister Offsets:\r\n");
    xil_printf("\tgreenLEDsData register \t= 0x%08x\r\n", (int)greenLEDsData);
    xil_printf("\tgreenLEDsTri register \t= 0x%08x\r\n", (int)greenLEDsTri);
    xil_printf("\tbuttonsData register \t= 0x%08x\r\n", (int)buttonsData);
    xil_printf("\tbuttonsTri register \t= 0x%08x\r\n", (int)buttonsTri);
    xil_printf("\tRGB Base ADDR\t= 0x%08x\r\n", (int)RGB_LEDS_BASE_ADDR);
    xil_printf("\tSwitch \t= 0x%08x\r\n", (int)PUSH_SWT_BASE_ADDR);

    *greenLEDsTri = 0x0;
    *buttonsTri = 0xF;

    *rgbLEDsTri = 0x0;
    *switchTri = 0xF;

    int oldButtonsData = 0;

    while(1)
    {

        *rgbLEDsData = 0;
        for (int i = 0; i < 4; i++)
        {
            if (*switchData & (1 << i)) 
            {
                *rgbLEDsData |= (0x07 << (i * 3)); 
            }

        }

        // Write the updated LED state to the RGB LEDs data register


        if (*switchData != oldButtonsData)
        {
            oldButtonsData = *buttonsData;
            xil_printf("buttonsData register: 0x%08x\r\n", *switchData);
        }
    }

    return 0;
}
