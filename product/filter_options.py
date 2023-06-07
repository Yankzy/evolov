

def category_options(category_name): 
    options = {
        'property': {
            'details': [
                ('bedrooms', 'number', 'gte'), ('built_year', 'number', 'gte'), ('city', 'string', 'icontains'), 
                ('country', 'string', 'icontains'), ('floors', 'number', 'gte'), ('building_size', 'number', 'gte'), 
                ('plot_size', 'number', 'gte'), ('renovated_year', 'number', 'gte'), ('state', 'string', 'icontains'), 
                ('street_address', 'string', 'icontains'), ('title', 'string', 'icontains'), ('zip', 'string', 'icontains'),
                ('nearby', 'bool', 'exact'), ('facilities', 'bool', 'exact'), ('features', 'bool', 'exact'),
            ], 
            'nearby': [
                ('beach', 'bool', 'exact'), ('car_wash', 'bool', 'exact'), ('church', 'bool', 'exact'), ('cinema', 'bool', 'exact'), 
                ('dog_park', 'bool', 'exact'), ('grocery_store', 'bool', 'exact'), ('gym', 'bool', 'exact'), 
                ('high_school', 'bool', 'exact'), ('hiking', 'bool', 'exact'), ('kindergarten', 'bool', 'exact'), 
                ('library', 'bool', 'exact'), ('mosque', 'bool', 'exact'), ('night_club', 'bool', 'exact'), ('primary_school', 'bool', 'exact'), 
                ('secondary_school', 'bool', 'exact'), ('shopping_center', 'bool', 'exact'), ('synagogue', 'bool', 'exact'), 
                ('theater', 'bool', 'exact'), ('university', 'bool', 'exact'), ('user_fields', 'bool', 'exact'),
            ], 
            
        },
        'vehicle': {
            'details': [
                ('brand', 'string', 'icontains'), ('model', 'string', 'icontains'), ('fuel', 'string', 'icontains'), 
                ('vehicle_type', 'string', 'icontains'), ('sales_form', 'string', 'icontains'), 
                ('owner_history', 'number', 'gte'), ('phone_number', 'string', 'icontains'), ('email', 'string', 'icontains'),
                ('transmission', 'string', 'icontains'), ('drivetrain', 'string', 'icontains'), ('condition', 'string', 'icontains'), 
                ('acceleration', 'number', 'gte'), ('interior_color', 'string', 'icontains'), 
                ('exterior_color', 'string', 'icontains'), ('price', 'number', 'gte'),
                ('title', 'string', 'icontains'), ('built_year', 'number', 'gte'), 
                ('street_address', 'string', 'icontains'), ('zip', 'string', 'icontains'), ('state', 'string', 'icontains'),
                ('city', 'string', 'icontains'), ('country', 'string', 'icontains'),  ('seats', 'number', 'gte'),  ('horse_power', 'number', 'gte'), ('speed', 'number', 'gte'), ('km', 'number', 'gte'), ('features', 'bool', 'exact'),
            ], 
            
        },
        'vacancy': {
            'details': [
                ('title', 'string', 'icontains'), ('business_type', 'string', 'icontains'), ('description', 'string', 'icontains'), ('salary', 'number', 'gte'), ('country', 'string', 'icontains'), ('city', 'string', 'icontains'), ('state', 'string', 'icontains'), ('street_address', 'string', 'icontains'), ('employment_type', 'string', 'icontains'), ('apply_link', 'string', 'icontains'), ('responsible_employee', 'string', 'icontains'), ('email', 'string', 'icontains'),
                ('benefits', 'bool', 'exact'), ('position', 'string', 'icontains'),
            ],
            
        },
    }
    return options[category_name]


