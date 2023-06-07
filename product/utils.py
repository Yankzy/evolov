house_categorys = [ "country", "city", "price", "size", "bedrooms", "building_year", "seller", 
    "plot_size", "facilty", "nearby", "renovated", "condition"]

hotel_categorys = []


def validate_categorys(request, categorys):
    data = request.data
    meta = data.get("meta_category", None)
    if not meta:
        raise

    if type(meta) != type([]):
        raise 

    for cat in categorys:
        meta_data = meta.get(cat, None)
        if not meta_data:
            raise


    return True

