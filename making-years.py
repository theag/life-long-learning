from members.models import Year

for y in range(2010,2021):
    ym = Year(value=y)
    ym.save()