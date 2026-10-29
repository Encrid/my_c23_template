/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdlib.h>
#include <string.h>

int main(int count, char **words)
{
    if (count > 1 && !strcmp(words[1], "exit"))
        _Exit(1);
    if (count > 1)
        abort();
    return (0);
}
