#ifndef KENNEL_DOOR_CONTROLLER_H
#define KENNEL_DOOR_CONTROLLER_H

#include <stdint.h>

#define KD_IN_OPEN_SW   0x01
#define KD_IN_CLOSE_SW  0x02
#define KD_IN_OBSTRUCT  0x04
#define KD_IN_BUTTON    0x08
#define KD_IN_LOCK      0x10

#define KD_OUT_MOTOR_OPEN  0x01
#define KD_OUT_MOTOR_CLOSE 0x02
#define KD_OUT_LATCH       0x04
#define KD_OUT_FAULT_LED   0x08

typedef enum {
    KD_S_INIT = 0,
    KD_S_CLOSED,
    KD_S_OPENING,
    KD_S_OPEN,
    KD_S_CLOSING,
    KD_S_HOLD,
    KD_S_FAULT
} kd_state_t;

typedef struct {
    kd_state_t st;
    uint8_t raw;
    uint8_t deb;
    uint8_t cnt[5];
    uint16_t t0;
    uint16_t hold;
    uint8_t out;
    uint8_t err;
    uint8_t retries;
} kd_ctx_t;

void kd_init(kd_ctx_t *c);
uint8_t kd_step(kd_ctx_t *c, uint8_t inputs, uint16_t now);
uint8_t kd_fault(const kd_ctx_t *c);

#endif
