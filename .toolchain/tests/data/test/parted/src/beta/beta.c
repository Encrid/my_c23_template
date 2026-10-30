/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>
#include <stdlib.h>

int main(int count, [[maybe_unused]] char **words)
{
    if (count > 1)
        return (printf("beta words\n") < 0);
    printf("beta\n");
    return (malloc(4) == nullptr);
}
