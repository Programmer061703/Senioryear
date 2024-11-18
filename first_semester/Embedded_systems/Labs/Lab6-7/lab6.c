/*
 * tasks.c
 *
 *  Bare Metal (no OS) example of a simple task scheduler
 * 
 */

#include <xil_exception.h>
#include <xil_printf.h>
#include <xil_types.h>
#include <xintc.h>
#include <xparameters.h>
#include <xtmrctr.h>
#include <xtmrctr_l.h>
#include <xgpio.h>
#include <stdlib.h>


#define INTC_DEVICE_ID 0
#define TMRCTR_DEVICE_ID 0
#define TMRCTR_INTERRUPT_ID XPAR_FABRIC_XTMRCTR_0_INTR

#define LOAD_VALUE 406239 // 5-ms period

#define RGB_RED 04444
#define RGB_GREEN 02222

#define CHANNEL_1 1
#define CHANNEL_2 2

// Function Prototypes
// Tasks
void taskChoose(void *data); // Scheduler
void taskGreen(void *data);
void taskRedBlinkStart(void *data);
void taskRed(void *data);
void taskRedBlinkEnd(void *data);

// Timer Interrupt Service Routine
void timer_ISR(void *CallBackRef, u8 TmrCtrNumber);

// Helper functions
int platform_init();
void TmrCtrDisableIntr(XIntc *IntcInstancePtr, u16 IntrId);
void executionFailed();

// Enumerate type for the states
typedef enum
{
  GREEN,
  RED_BLINK_START,
  RED,
  RED_BLINK_END
} state_t;

// Enumerated type for the tasks
typedef enum
{
  TASK_CHOOSE,
  TASK_GREEN,
  TASK_RED_BLINK_START,
  TASK_RED,
  TASK_RED_BLINK_END,
  MAX_TASKS
} task_t;

/*
for (int i = 0; i < MAX_TASKS; i++){}

*/

// Task Control Block (TCB) structure
typedef struct
{
  void (*taskPtr)(void *); // Pointer to a function
  void *taskDataPtr;
  u8 taskReady; // Boolean
} TCB_t;

// Usage: *taskPtr(taskDatPtr)

// Hardware instances
XIntc InterruptController; // Instance of the Interrupt Controller
XTmrCtr Timer;             // Instance of the Timer
XGpio btnGpio;             // Instance of the AXI_GPIO_0
XGpio ledGpio;             // Instance of the AXI_GPIO_1

// Task queue
TCB_t *queue[MAX_TASKS];

// Global variables
state_t state, nextState; // State variables
u8 btnPressed = FALSE;    // Flag to indicate if the button is pressed
u32 systemTime = 0;       // System time: 1 unit = 5 ms
u32 startTime = 0;        // Start time of the current state
u32 elapsedTime = 0;      // Elapsed time since last state transition
u32 ledColor = 0;         // Current state of the LEDs

int main(int argc, char const *argv[])
{
  // Initialize the platform:
  // Setup the GPIO, Interrupt Controller and Timer
  int status = XST_FAILURE;

  status = platform_init();

  if (status != XST_SUCCESS)
  {
    xil_printf("Failed to initialize the platform! Execution stopped.\n");
    executionFailed();
  }

  // Initialize the task queue and TCBs
  // Task 0: taskChoose
  queue[TASK_CHOOSE] = malloc(sizeof(TCB_t));
  queue[TASK_CHOOSE]->taskPtr = taskChoose;
  queue[TASK_CHOOSE]->taskDataPtr = NULL;
  queue[TASK_CHOOSE]->taskReady = FALSE;

  // Task 1: taskGreen
  queue[TASK_GREEN] = malloc(sizeof(TCB_t));
  queue[TASK_GREEN]->taskPtr = taskGreen;
  queue[TASK_GREEN]->taskDataPtr = NULL;
  queue[TASK_GREEN]->taskReady = FALSE;

  // Task 2: taskRedBlinkStart
  queue[TASK_RED_BLINK_START] = malloc(sizeof(TCB_t));
  queue[TASK_RED_BLINK_START]->taskPtr = taskRedBlinkStart;
  queue[TASK_RED_BLINK_START]->taskDataPtr = NULL;
  queue[TASK_RED_BLINK_START]->taskReady = FALSE;

  // Task 3: taskRed
  queue[TASK_RED] = malloc(sizeof(TCB_t));
  queue[TASK_RED]->taskPtr = taskRed;
  queue[TASK_RED]->taskDataPtr = NULL;
  queue[TASK_RED]->taskReady = FALSE;
  
  // Task 4: taskRedBlinkEnd
  queue[TASK_RED_BLINK_END] = malloc(sizeof(TCB_t));
  queue[TASK_RED_BLINK_END]->taskPtr = taskRedBlinkEnd;
  queue[TASK_RED_BLINK_END]->taskDataPtr = NULL;
  queue[TASK_RED_BLINK_END]->taskReady = FALSE;

  // Initialize the state machine
  state = nextState = GREEN;

  // Main loop
  while (1)
  {
    // Check if the button is pressed
    if (XGpio_DiscreteRead(&btnGpio, 2) & 0xF)
      btnPressed = TRUE;

    // Iterate through task queue and
    // execute tasks that are ready
    for (int i = 0; i < MAX_TASKS; i++)
    {
      if (queue[i]->taskReady)
      {
        // Execute the task
        (*(queue[i]->taskPtr))(queue[i]->taskDataPtr);

        // Reset the task ready flag
        queue[i]->taskReady = 0;
      }
    }

    // Ack button press
    btnPressed = FALSE;

    // Update the LEDs
    XGpio_DiscreteWrite(&ledGpio, 1, ledColor);
  }

  return 0;
}

void taskChoose(void *data)
{
  // DEBUG: Print the current state
  xil_printf("Choose task...\n");

  switch (state)
  {
  case GREEN:
    queue[TASK_GREEN]->taskReady = TRUE;
    break;
  case RED_BLINK_START:
    queue[TASK_RED_BLINK_START]->taskReady = TRUE;
    break;
  case RED:
    queue[TASK_RED]->taskReady = TRUE;
    break;
  case RED_BLINK_END:
    queue[TASK_RED_BLINK_END]->taskReady = TRUE;
    break;
  }

  // Update state
  state = nextState;
}

void taskGreen(void *data)
{
  // DEBUG: Print the current state
  xil_printf("Green task...\r\n");

  // Set the LEDs to green
  ledColor = RGB_GREEN;

  // Set the next state
  if (btnPressed)
  {
    nextState = RED_BLINK_START;
    startTime = systemTime; // Reset the start time
    ledColor = RGB_RED;     // Set the LEDs to red
  }
}

void taskRedBlinkStart(void *data)
{
  // DEBUG: Print the current state
  xil_printf("Red blink start task\r\n");

  // Record elapsed time
  elapsedTime = systemTime - startTime;
  // xil_printf("Elapsed time: %d\r\n", elapsedTime);

  // Blink the LEDs every 500 ms
  // (100 units = 500 ms)
  if (elapsedTime % 100 == 0)
    ledColor ^= RGB_RED; // Toggle the LEDs

  // Reset start time if button is pressed
  if (btnPressed)
    startTime = systemTime;

  // Set the next state
  // (1200 units = 6 s)
  if (elapsedTime >= 1200)
  {
    nextState = RED;
    startTime = systemTime; // Record the start time
    ledColor = RGB_RED;     // Set the LEDs to red
  }
}

void taskRed(void *data)
{
  xil_printf("Red task...\r\n");

  // Record elapsed time
  elapsedTime = systemTime - startTime;

  // Set the LEDs to red
  ledColor = RGB_RED;

  // Set the next state
  // (800 units = 4 s)
  if (elapsedTime >= 800)
  {
    nextState = RED_BLINK_END;
    startTime = systemTime; // Record the start time
    ledColor = RGB_RED;     // Set the LEDs to red
  }
}

void taskRedBlinkEnd(void *data)
{
  // DEBUG: Print the current state
  xil_printf("Red blink stop task...\r\n");

  // Record elapsed time
  elapsedTime = systemTime - startTime;

  // Blink the LEDs every 500 ms
  // (100 units = 500 ms)
  if (elapsedTime % 100 == 0)
    ledColor ^= RGB_RED; // Toggle the LEDs

  // Set the next state
  // (1200 units = 6 s)
  if (elapsedTime >= 1200)
  {
    nextState = GREEN;
    startTime = systemTime; // Record the start time
    ledColor = RGB_GREEN;   // Set the LEDs to green
  }
}

void timer_ISR(void *CallBackRef, u8 TmrCtrNumber)
{
  // Increment system time
  systemTime++; // 1 unit = 5 ms

  // Get instance of the timer linked to the interrupt
  XTmrCtr *InstancePtr = (XTmrCtr *)CallBackRef;

  // Check if the timer counter has expired
  if (XTmrCtr_IsExpired(InstancePtr, TmrCtrNumber))
    // Set taskChoose to be ready
    queue[TASK_CHOOSE]->taskReady = TRUE;
}

int platform_init()
{
  int status = XST_FAILURE;

  // Initialize the GPIO instances
  status = XGpio_Initialize(&btnGpio, XPAR_GPIO_0_BASEADDR);
  if (status != XST_SUCCESS)
  {
    xil_printf("Failed to initialize GPIO_0! Execution stopped.\n");
    executionFailed();
  }

  status = XGpio_Initialize(&ledGpio, XPAR_GPIO_1_BASEADDR);
  if (status != XST_SUCCESS)
  {
    xil_printf("Failed to initialize GPIO_1! Execution stopped.\n");
    executionFailed();
  }

  // Set GPIO_0 CHANNEL 2 as input
  XGpio_SetDataDirection(&btnGpio, CHANNEL_2, 0xF);

  // Set GPIO_1 CHANNEL 1 as output
  XGpio_SetDataDirection(&ledGpio, CHANNEL_1, 0x0);

  // Initialize the timer counter instance
  status = XTmrCtr_Initialize(&Timer, TMRCTR_DEVICE_ID);
  if (status != XST_SUCCESS)
  {
    xil_printf("Failed to initialize the timer! Execution stopped.\n");
    executionFailed();
  }

  // Verifies the specified timer is setup correctly in hardware/software
  status = XTmrCtr_SelfTest(&Timer, XTC_TIMER_0);
  if (status != XST_SUCCESS)
  {
    xil_printf("Testing timer operation failed! Execution stopped.\n");
    executionFailed();
  }

  // Initialize the interrupt controller instance
  status = XIntc_Initialize(&InterruptController, INTC_DEVICE_ID);
  if (status != XST_SUCCESS)
  {
    xil_printf("Failed to initialize the interrupt controller! Execution stopped.\n");
    executionFailed();
  }

  // Connect a timer handler that will be called when an interrupt occurs
  status = XIntc_Connect(&InterruptController,
                         TMRCTR_INTERRUPT_ID,
                         (XInterruptHandler)XTmrCtr_InterruptHandler,
                         (void *)&Timer);
  if (status != XST_SUCCESS)
  {
    xil_printf("Failed to connect timer handler! Execution stopped.\n");
    executionFailed();
  }

  // Start the interrupt controller
  status = XIntc_Start(&InterruptController, XIN_REAL_MODE);
  if (status != XST_SUCCESS)
  {
    xil_printf("Failed to start interrupt controller! Execution stopped.\n");
    executionFailed();
  }

  // Enable interrupts and the exception table
  XIntc_Enable(&InterruptController, TMRCTR_INTERRUPT_ID);
  Xil_ExceptionInit();

  // Register the interrupt controller handler with the exception table.
  Xil_ExceptionRegisterHandler(XIL_EXCEPTION_ID_INT,
                               (Xil_ExceptionHandler)XIntc_InterruptHandler,
                               &InterruptController);

  // Enable exceptions
  Xil_ExceptionEnable();

  // Set the handler (function pointer) that we want to execute when the
  // interrupt occurs
  XTmrCtr_SetHandler(&Timer, timer_ISR, &Timer);

  // Set our timer options (setting TCSR register indirectly through Xil API)
  u32 timerConfig = XTC_INT_MODE_OPTION |
                    XTC_DOWN_COUNT_OPTION |
                    XTC_AUTO_RELOAD_OPTION;
  XTmrCtr_SetOptions(&Timer, XTC_TIMER_0, timerConfig);

  // Set what value the timer should reset/init to (setting TLR indirectly)
  XTmrCtr_SetResetValue(&Timer, XTC_TIMER_0, LOAD_VALUE);

  // Start the timer
  XTmrCtr_Start(&Timer, XTC_TIMER_0);

  return XST_SUCCESS;
}

void executionFailed()
{
  u32 *rgbLedsData = (u32 *)(XPAR_GPIO_1_BASEADDR);
  *rgbLedsData = RGB_RED; // display all red LEDs if fail state occurs

  // trap the program in an infinite loop
  while (1)
    ;
}

// Optional demonstration on how to disable interrupt
void TmrCtrDisableIntr(XIntc *IntcInstancePtr, u16 IntrId)
{
  // Disable the interrupt for the timer counter
  XIntc_Disable(IntcInstancePtr, IntrId);

  return;
}