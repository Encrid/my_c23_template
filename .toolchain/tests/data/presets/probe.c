/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include "bridge_native.h"

[[gnu::section(MANIFEST_SECTION), gnu::used, gnu::retain]]
static const char WHO[] = MANIFEST;

static uint32_t ticking;

BRIDGE_NATIVE(tick)
{
    return (0);
}

BRIDGE_NATIVE(init)
{
    bridge_term_t terms[1] = {{ 0, BRIDGE_READ, BRIDGE_AND, 0 }};

    ticking = BRIDGE_NATIVE_ADD_SYSTEM(api, "tick", "update", terms, 1,
        nullptr, 0);
    return (0);
}
