/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <windows.h>

#include "typed.h"

static DWORD WINAPI run(LPVOID arg)
{
    return (arg != nullptr);
}

int thread_started(void)
{
    static int held;
    HANDLE thread = CreateThread(nullptr, 0, run, &held, 0, nullptr);

    if (!thread)
        return (-1);
    WaitForSingleObject(thread, INFINITE);
    CloseHandle(thread);
    return (0);
}
