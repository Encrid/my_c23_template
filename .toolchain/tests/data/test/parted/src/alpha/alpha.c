/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>

int main(int count, [[maybe_unused]] char **words)
{
    if (count > 1)
        return (printf("alpha words\n") < 0);
    return (printf("alpha\n") < 0);
}
