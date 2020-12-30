from ..forms import *


def compute_limit(size, isBusiness):
    lowLimit = 0
    highLimit = 0

    if size <= 2:
        if isBusiness:
            if size == 0:
                lowLimit = 10000
                highLimit = 15000
            elif size == 1:
                lowLimit = 12000
                highLimit = 17000
            elif size == 2:
                lowLimit = 15000
                highLimit = 19000
        else:
            if size == 0:
                lowLimit = 5000
                highLimit = 7000
            elif size == 1:
                lowLimit = 4500
                highLimit = 5500
            elif size == 2:
                lowLimit = 3500
                highLimit = 4000

    return [lowLimit, highLimit]


def cards_queries(request, fetch_query, set_query):
    if request.method == "POST":
        # FORMULARIO
        form = Cards_Form(data=request.POST)

        if form.is_valid():
            # LEER FORMULARIO
            data = form.cleaned_data

            # VARIABLES
            card_id = data.get('id', '')
            credit = data.get('credit', 0)
            brand = request.POST.get('brand', 'Prefepuntos')
            user_id = request.POST.get('user', 0)

            # BUSCAR USUARIO
            user = fetch_query(
                f'SELECT * FROM SingleUser WHERE cui = "{user_id}"')
            business = fetch_query(
                f'SELECT * FROM BusinessUser WHERE comercialName = "{user_id}"')
            cards = fetch_query(
                f'SELECT * FROM Cards where userCui = "{user_id}" OR userBusiness = "{user_id}"')

            isBusiness = len(user) == 0 and len(business) > 0
            limit = compute_limit(len(cards), isBusiness)

            # INSERT
            print(isBusiness, limit)
            if float(credit) >= limit[0] and float(credit) <= limit[1]:
                if len(cards) <= 2:
                    userCui = "null" if isBusiness else user_id
                    userBusiness = f'"{user_id}"' if not isBusiness else "null"

                    set_query(
                        f'INSERT INTO Cards VALUES ({card_id}, "{brand}", {credit}, 0, {limit[0]}, {limit[1]}, {userCui}, {userBusiness})')
