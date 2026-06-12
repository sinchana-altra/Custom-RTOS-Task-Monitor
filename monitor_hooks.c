#include "monitor_hooks.h"
#include "serial_sender.h"
#include <string.h>

static TaskSnapshot_t task_list[MAX_TASKS];
static uint8_t task_count = 0;

void monitor_on_task_create(void *pxTask) {
    if (task_count >= MAX_TASKS) return;
    TaskHandle_t handle = (TaskHandle_t)pxTask;
    TaskSnapshot_t *snap = &task_list[task_count++];
    vTaskGetInfo(handle, (TaskStatus_t *)snap, pdTRUE, eRunning);
}

void monitor_on_task_delete(void *pxTask) {
    TaskHandle_t handle = (TaskHandle_t)pxTask;
    for (int i = 0; i < task_count; i++) {
        if (task_list[i].task_id == (uint32_t)uxTaskGetTaskNumber(handle)) {
            task_list[i] = task_list[--task_count];
            return;
        }
    }
}

void monitor_on_task_switch(void *pxTask) {
    TaskHandle_t handle = (TaskHandle_t)pxTask;
    for (int i = 0; i < task_count; i++) {
        if (task_list[i].task_id == (uint32_t)uxTaskGetTaskNumber(handle)) {
            task_list[i].cpu_ticks++;
        }
    }
}

uint8_t collect_all_tasks(TaskSnapshot_t *out) {
    memcpy(out, task_list, task_count * sizeof(TaskSnapshot_t));
    return task_count;
}
