#ifndef MONITOR_HOOKS_H
#define MONITOR_HOOKS_H

#include "FreeRTOS.h"
#include "task.h"
#include <stdint.h>

#define MAX_TASKS 16

typedef struct {
    char     name[16];
    uint8_t  priority;
    uint8_t  state;
    uint32_t stack_hwm;
    uint32_t cpu_ticks;
    uint32_t task_id;
} TaskSnapshot_t;

void    monitor_on_task_create(void *pxTask);
void    monitor_on_task_delete(void *pxTask);
void    monitor_on_task_switch(void *pxTask);
uint8_t collect_all_tasks(TaskSnapshot_t *out);

#endif
