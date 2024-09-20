// Computer System Design Lab 9
// Example Code Use
/* Push buttons are used to control the on-board LEDs. */
// Direction Masks
#define outputDir 0x00000000 // All output bits
#define inputDir 0x0000001F // 5-input bits
int main()
{
// Pointer defintions for Button GPIO
// ** NOTE - integer definition causes
// offsets to be automatically be multiplied by 4!!
// 4 Byte Registers
volatile int *base_buttonGPIO = (int*)(0x40040000);
volatile int *data_buttonGPIO = (int*)(base_buttonGPIO + 0x0);
// multiplied by 4 is reason 0x1 is used here instead of 0x4
volatile int *tri_buttonGPIO = (int*)(base_buttonGPIO + 0x1);
// Pointer defintions for LED GPIO
// ** NOTE - integer definition causes
// offsets to be automatically be multiplied by 4!!
volatile int *base_ledGPIO = (int*)(0x40000000);
volatile int *data_ledGPIO = (int*)(base_ledGPIO + 0x0);
volatile int *tri_ledGPIO = (int*)(base_ledGPIO + 0x1);
// Variable used to store the state of the buttons
int data = 0;
// Init. the LED peripheral to outputs
print("Init. LED GPIO Data Direction...\r\n");
*tri_ledGPIO = outputDir;
// Init. the Button peripheral to inputs
print("Init. Button GPIO Data Direction...\r\n");
//Why writing all 1s to GPIO
*tri_buttonGPIO = inputDir;
// Infinitely Loop...
while(1)
{ // Read the current state of the push buttons
data = *data_buttonGPIO;
xil_printf("buttonState = %d\r\n",data);
// Set the state of the LEDs
*data_ledGPIO = data; }
return 0;
}