#include "kennel_door_controller.h"

static uint16_t dt(uint16_t a, uint16_t b) {
    if (a >= b) return a - b;
    return (uint16_t)(65535u - b + a + 1u);
}

static void deb(kd_ctx_t *c, uint8_t in) {
    uint8_t i;
    c->raw = in;
    for (i = 0; i < 5; i++) {
        if (in & (1u << i)) {
            if (c->cnt[i] < 4) c->cnt[i]++;
        } else {
            if (c->cnt[i] > 0) c->cnt[i]--;
        }
        if (c->cnt[i] >= 3) c->deb |= (1u << i);
        else if (c->cnt[i] == 0) c->deb &= ~(1u << i);
    }
}

void kd_init(kd_ctx_t *c) {
    uint8_t i;
    c->st = KD_S_INIT;
    c->raw = 0;
    c->deb = 0;
    for (i = 0; i < 5; i++) c->cnt[i] = 0;
    c->t0 = 0;
    c->hold = 0;
    c->out = 0;
    c->err = 0;
    c->retries = 0;
}

uint8_t kd_fault(const kd_ctx_t *c) {
    return c->st == KD_S_FAULT ? c->err : 0;
}

uint8_t kd_step(kd_ctx_t *c, uint8_t inputs, uint16_t now) {
    uint8_t d;
    deb(c, inputs);
    d = c->deb;

    if (c->st != KD_S_FAULT && (d & KD_IN_OBSTRUCT) && (c->out & KD_OUT_MOTOR_CLOSE)) {
        c->out = KD_OUT_MOTOR_OPEN;
        c->st = KD_S_OPENING;
        c->t0 = now;
        c->retries++;
        if (c->retries > 3) {
            c->st = KD_S_FAULT;
            c->err = 0x21;
            c->out = KD_OUT_FAULT_LED;
        }
        return c->out;
    }

    switch (c->st) {
    case KD_S_INIT:
        c->out = 0;
        if (d & KD_IN_CLOSE_SW) {
            c->st = KD_S_CLOSED;
            c->out = KD_OUT_LATCH;
        } else if (d & KD_IN_OPEN_SW) {
            c->st = KD_S_OPEN;
            c->hold = now;
        } else {
            c->out = KD_OUT_MOTOR_CLOSE;
            c->st = KD_S_CLOSING;
            c->t0 = now;
        }
        break;

    case KD_S_CLOSED:
        c->out = KD_OUT_LATCH;
        c->retries = 0;
        if ((d & KD_IN_BUTTON) && !(d & KD_IN_LOCK)) {
            c->out = KD_OUT_MOTOR_OPEN;
            c->st = KD_S_OPENING;
            c->t0 = now;
        }
        break;

    case KD_S_OPENING:
        c->out = KD_OUT_MOTOR_OPEN;
        if (d & KD_IN_OPEN_SW) {
            c->out = 0;
            c->st = KD_S_OPEN;
            c->hold = now;
        } else if (dt(now, c->t0) > 1200) {
            if (c->retries < 2) {
                c->retries++;
                c->t0 = now;
            } else {
                c->st = KD_S_FAULT;
                c->err = 0x11;
                c->out = KD_OUT_FAULT_LED;
            }
        }
        break;

    case KD_S_OPEN:
        c->out = 0;
        if (d & KD_IN_BUTTON) {
            c->hold = now;
        } else if (dt(now, c->hold) > 8000) {
            if (d & KD_IN_OBSTRUCT) {
                c->hold = now;
            } else {
                c->out = KD_OUT_MOTOR_CLOSE;
                c->st = KD_S_CLOSING;
                c->t0 = now;
            }
        }
        break;

    case KD_S_CLOSING:
        c->out = KD_OUT_MOTOR_CLOSE;
        if (d & KD_IN_CLOSE_SW) {
            c->out = KD_OUT_LATCH;
            c->st = KD_S_CLOSED;
            c->retries = 0;
        } else if (dt(now, c->t0) > 1500) {
            c->st = KD_S_FAULT;
            c->err = 0x12;
            c->out = KD_OUT_FAULT_LED;
        }
        break;

    case KD_S_HOLD:
        c->out = 0;
        if (!(d & KD_IN_OBSTRUCT)) {
            c->out = KD_OUT_MOTOR_CLOSE;
            c->st = KD_S_CLOSING;
            c->t0 = now;
        }
        break;

    case KD_S_FAULT:
    default:
        c->out = KD_OUT_FAULT_LED;
        if ((d & KD_IN_LOCK) && (d & KD_IN_BUTTON) && (d & KD_IN_CLOSE_SW)) {
            c->err = 0;
            c->retries = 0;
            c->st = KD_S_CLOSED;
            c->out = KD_OUT_LATCH;
        }
        break;
    }

    return c->out;
}
