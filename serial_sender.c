#include "serial_sender.h"
#include "monitor_hooks.h"
#include "FreeRTOS.h"
#include "task.h"
#include <string.h>

/* Change this to your UART send function */
extern void uart_write(const uint8_t *data, uint16_t len);

#define HEADER_MAGIC 0xAB

void serial_send_snapshot(void) {
    TaskSnapshot_t tasks[MAX_TASKS];
    uint8_t count = collect_all_tasks(tasks);

    uart_write(&HEADER_MAGIC, 1);
    uart_write(&count, 1);
    uart_write((uint8_t *)tasks, count * sizeof(TaskSnapshot_t));
}

/* Call this task from your RTOS main */
void monitor_sender_task(void *pvParams) {
    (void)pvParams;
    for (;;) {
        serial_send_snapshot();
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}
