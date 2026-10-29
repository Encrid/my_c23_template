/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#ifndef STARTED_H
    #define STARTED_H
    #pragma clang system_header

typedef unsigned long (__attribute__((stdcall)) *start_fn_t)(void *arg);

int start_one(start_fn_t start, void *arg);
int start_two(void *_Nullable (*_Nonnull start)(void *_Nullable arg),
    void *_Nullable arg);

#endif
