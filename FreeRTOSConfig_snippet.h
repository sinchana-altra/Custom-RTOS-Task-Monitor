/* Add these lines to your existing FreeRTOSConfig.h */

#define traceTASK_CREATE(pxTask)        monitor_on_task_create(pxTask)
#define traceTASK_DELETE(pxTask)        monitor_on_task_delete(pxTask)
#define traceTASK_SWITCHED_IN()         monitor_on_task_switch(pxCurrentTCB)

/* Make sure to include the header at the top of FreeRTOSConfig.h */
/* #include "monitor_hooks.h" */
