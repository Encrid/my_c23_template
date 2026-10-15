/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
constexpr int THOUSAND = 1'000;

int main(void)
{
    int counted = 0b11'1110'1000;

    return counted == THOUSAND ? 0 : 1;
}
