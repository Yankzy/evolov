import graphene
from graphene_django.types import DjangoObjectType
from graphene import String, InputObjectType, Int, Float, Boolean, ID, Field
from users.models import Activity, Company, Employee, Following, User
from product.models import Ad, Category, ImageUrl, SubCategory, Resume
from graphene_django.types import ObjectType
import graphene
from graphene.types.generic import GenericScalar




class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude_fields = ['password']


class ResumeType(DjangoObjectType):
    class Meta:
        model = Resume
        


class AuthLoginType(ObjectType):
    token = graphene.String()
    user = graphene.Field(UserType)


class EmployeeType(DjangoObjectType):
    class Meta:
        model = Employee


class CompanyType(DjangoObjectType):
    class Meta:
        model = Company

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

    category_image = String()

    def resolve_category_image(self, info):
        img = ImageUrl.objects.get(category=getattr(self, 'id'))
        return img.category_image


class SubCategoryType(DjangoObjectType):
    class Meta:
        model = SubCategory

    sub_category_image = String()

    def resolve_sub_category_image(self, info):
        img = ImageUrl.objects.get(sub_category=getattr(self, 'id'))
        return img.sub_category_image


class ImageUrlType(DjangoObjectType):
    class Meta:
        model = ImageUrl


class FollowType(DjangoObjectType):
    class Meta:
        model = Following


class AdType(DjangoObjectType):
    class Meta:
        model = Ad
    gallery = String()


class ActivityType(DjangoObjectType):
    class Meta:
        model = Activity
    
    ad = Field(AdType)

    def resolve_ad(self, info):
        return Ad.objects.get(id=self.object_id)



class UserDefinedField(InputObjectType):
    field_name = String()
    field_value = String()


class Price(InputObjectType):
    min = Int()
    max = Int()

class Facilities(InputObjectType):
    internet = Boolean(required=True)
    maintenance_24_hrs = Boolean(required=True)
    pool = Boolean(required=True)
    garage = Boolean(required=True)
    fireplace = Boolean(required=True)
    dog_keepers = Boolean(required=True)
    dogs_allowed = Boolean(required=True)
    cats_allowed = Boolean(required=True)
    pool_table = Boolean(required=True)
    media_room = Boolean(required=True)
    hot_tub = Boolean(required=True)
    water = Boolean(required=True)
    electricity = Boolean(required=True)
    child_friendly = Boolean(required=True)
    car_wash_area = Boolean(required=True)
    gym_room = Boolean(required=True)
    air_condition = Boolean(required=True)
    oven = Boolean(required=True)
    refrigerator = Boolean(required=True)
    microwave = Boolean(required=True)
    user_defined_fields = UserDefinedField()



class NearBy(InputObjectType):
    kindergarten = Boolean(required=True)
    primary_school = Boolean(required=True)
    secondary_school = Boolean(required=True)
    high_school = Boolean(required=True)
    university = Boolean(required=True)
    grocery_store = Boolean(required=True)
    shopping_center = Boolean(required=True)
    library = Boolean(required=True)
    cinema = Boolean(required=True)
    night_club = Boolean(required=True)
    theater = Boolean(required=True)
    beach = Boolean(required=True)
    hiking = Boolean(required=True)
    dog_park = Boolean(required=True)
    gym = Boolean(required=True)
    car_wash = Boolean(required=True)
    mosque = Boolean(required=True)
    church = Boolean(required=True)
    synagogue = Boolean(required=True)
    user_defined_fields = UserDefinedField()


class Features(InputObjectType):
    # Vehicle
    abs = Boolean()
    am_fm_radio = Boolean()
    adaptive_comering_lights = Boolean()
    adaptive_cruise_control = Boolean()
    adaptive_headlights = Boolean()
    adaptive_suspension = Boolean()
    air_suspension = Boolean()
    alarm_system = Boolean()
    all_season_tyres = Boolean()
    all_terrain_tyres = Boolean()
    ambient_lighting = Boolean()
    android_auto = Boolean()
    apple_carplay = Boolean()
    arm_rest = Boolean()
    auto_pilot = Boolean()
    auto_dimming_interior_mirror = Boolean()
    automatic_parking = Boolean()
    auxiliary_audio_input = Boolean()
    auxiliary_heating = Boolean()
    blind_spot_monitor = Boolean()
    bluetooth = Boolean()
    cd_player = Boolean()
    cargo_barrier = Boolean()
    central_locking = Boolean()
    child_safety_locks = Boolean()
    child_seat_anchors = Boolean()
    collision_warning = Boolean()
    cross_traffic_alert = Boolean()
    dab_radio = Boolean()
    daytime_running_lights = Boolean()
    digital_cockpit = Boolean()
    driver_airbag = Boolean()
    driver_drowsiness_detection = Boolean()
    esp = Boolean()
    electric_windows = Boolean()
    electric_backseat_adjustment = Boolean()
    electric_seat_adjustment = Boolean()
    electric_side_mirror = Boolean()
    electric_tailgate = Boolean()
    electrically_adjustable_steering_column = Boolean()
    electrically_folding_exterior_mirrors = Boolean()
    electrically_heated_exterior_mirrors = Boolean()
    electronic_brake_assistance = Boolean()
    electronic_stability_control = Boolean()
    emergency_tyre_inflation_kit = Boolean()
    emergency_tyre_repair_kit = Boolean()
    emergency_tyre_sealant = Boolean()
    emergency_braking = Boolean()
    emergency_call_system = Boolean()
    emergency_stop_signal = Boolean()
    fatigue_warning_system = Boolean()
    fog_lights = Boolean()
    fold_flat_passenger_seat = Boolean()
    forward_collision_warning = Boolean()
    front_airbags = Boolean()
    front_heated_seats = Boolean()
    front_power_lumbar_support = Boolean()
    front_and_rear_parking_sensors = Boolean()
    head_up_display = Boolean()
    heads_up_display = Boolean()
    heated_windshield = Boolean()
    hight_beam_assist = Boolean()
    hill_descent_control = Boolean()
    hill_holder = Boolean()
    hill_start_assist = Boolean()
    isofix = Boolean()
    induction_charging_for_smartphones = Boolean()
    integrated_turn_signal_mirrors = Boolean()
    integrated_music_streaming = Boolean()
    jbl_sound_system = Boolean()
    led_daytime_running_lights = Boolean()
    led_fog_lights = Boolean()
    led_headlights = Boolean()
    led_taillights = Boolean()
    lane_change_assist = Boolean()
    lane_departure_warning = Boolean()
    lane_keeping_assist = Boolean()
    leather_seats = Boolean()
    leather_steering_wheel = Boolean()
    lumbar_support = Boolean()
    mp3_player = Boolean()
    massage_seats = Boolean()
    memory_package = Boolean()
    memory_seats = Boolean()
    memory_steering_wheel = Boolean()
    meridian_sound_system = Boolean()
    moonroof = Boolean()
    multi_function_steering_wheel = Boolean()
    multi_zone_climate_control = Boolean()
    multifunction_steering_wheel = Boolean()
    navigation_system = Boolean()
    night_vision = Boolean()
    onstar = Boolean()
    onboard_computer = Boolean()
    paddle_shifters = Boolean()
    panoramic_roof = Boolean()
    parking_assist = Boolean()
    parking_assist_camera = Boolean()
    parking_assist_sensors_front = Boolean()
    parking_assist_sensors_front_and_rear = Boolean()
    parking_assist_sensors_rear = Boolean()
    parking_assist_system = Boolean()
    passenger_airbag = Boolean()
    pedestrian_detection = Boolean()
    power_assisted_steering = Boolean()
    power_brakes = Boolean()
    power_locks = Boolean()
    pre_collision_system = Boolean()
    pre_collision_warning = Boolean()
    premium_audio = Boolean()
    premium_sound_system = Boolean()
    quad_seats = Boolean()
    rain_sensing_wipers = Boolean()
    rain_sensor = Boolean()
    rear_airbags = Boolean()
    rear_defroster = Boolean()
    rear_entertainment_system = Boolean()
    rear_view_camera = Boolean()
    rear_view_monitor = Boolean()
    rear_wiper = Boolean()
    remote_fuel_door = Boolean()
    remote_keyless_entry = Boolean()
    remote_start = Boolean()
    remote_trunk_release = Boolean()
    road_condition_indicator = Boolean()
    roll_stability_control = Boolean()
    roof_rack = Boolean()
    satellite_radio = Boolean()
    side_airbags = Boolean()
    ski_bag = Boolean()
    sliding_rear_seats = Boolean()
    speed_limit_info = Boolean()
    speed_limit_recognition = Boolean()
    speed_limiter = Boolean()
    speed_warning = Boolean()
    stability_control = Boolean()
    stability_control = Boolean()
    start_stop_engine = Boolean()
    steering_wheel_audio_controls = Boolean()
    steering_wheel_controls = Boolean()
    steering_wheel_mounted_controls = Boolean()
    summer_tyres = Boolean()
    sunroof = Boolean()
    third_row_seats = Boolean()
    tilt_steering_wheel = Boolean()
    tow_hitch = Boolean()
    tow_package = Boolean()
    towing_package = Boolean()
    traction_control = Boolean()
    traffic_sign_recognition = Boolean()
    trip_computer = Boolean()
    tyre_pressure_monitoring_system = Boolean()
    usb = Boolean()
    voice_control = Boolean()
    winter_tyres = Boolean()
    xenon_headlights = Boolean()
    zoned_climate_control = Boolean()
    air_condition = Boolean()
    alloy_wheels = Boolean()
    anti_lock_brake_system = Boolean()
    automatic_emergency_braking = Boolean()
    automatic_high_beams = Boolean()
    blind_spot_monitoring = Boolean()
    central_locking = Boolean()
    collision_avoidance_system = Boolean()
    cruise_control = Boolean()
    electric_mirrors = Boolean()
    electric_windows = Boolean()
    evasive_steering = Boolean()
    heated_mirrors = Boolean()
    heated_seats = Boolean()
    heated_steering_wheel = Boolean()
    keyless_entry = Boolean()
    keyless_start = Boolean()
    lane_keeping_assist = Boolean()
    leather_interior = Boolean()
    navigation = Boolean()
    parking_sensors = Boolean()
    power_folding_mirrors = Boolean()
    power_liftgate = Boolean()
    power_mirrors = Boolean()
    power_seats = Boolean()
    power_steering = Boolean()
    power_sunroof = Boolean()
    power_tailgate = Boolean()
    power_windows = Boolean()
    rear_cross_traffic_warning = Boolean()
    sport_seats = Boolean()
    traction_control_system = Boolean()
    xenon_lights = Boolean()


class Benefits(InputObjectType):
    health_insurance = Boolean()
    life_insurance = Boolean()
    vision_insurance = Boolean()
    prescription_and_pharmacy_benefits = Boolean()
    mental_health_coverage = Boolean()
    paid_time_off = Boolean()
    paid_sick_leave = Boolean()
    disability_benefits = Boolean()
    travel_expenses = Boolean()
    company_equipment = Boolean()
    company_car = Boolean()
    company_transportation = Boolean()
    pension = Boolean()
    social_security = Boolean()
    paid_vacation = Boolean()
    work_from_home = Boolean()
    dental_insurance = Boolean()
    flexible_working_hours = Boolean()
    meal_vouchers = Boolean()
    parking = Boolean()
    relocation_package = Boolean()
    training = Boolean()
    travel_insurance = Boolean()
    work_perks = Boolean()
    chiropractor = Boolean()
    physiotherapy = Boolean()



class Details(InputObjectType):
    currency_code = String()
    title = String(required=True)
    description = String()
    country = String()
    state = String()
    city = String()
    street_address = String()
    zip = String()
    email = String()
    phone_number = String()
    # property
    size = Float()
    plot_size = Float()
    building_size = Float()
    bedrooms = Int()
    built_year = Int()
    seller = String()
    renovated_year = Int()
    floors = Int()
    # vehicle
    brand = String()
    model = String()
    fuel = String()
    transmission = String()
    drive_train = String()
    condition = String()
    acceleration = String()
    interior_color = String()
    exterior_color = String()
    vehicle_type = String()
    drivetrain = String()
    owner_history = String()
    sales_form = String()
    price = Float()
    seats = Float()
    horse_power = Float()
    speed = Float()
    km = Float()
    # jobs
    salary = Float()
    position = String()
    applyLink = String()
    businessType = String()
    employmentType = String()
    responsibleEmployee = String()
    experience = String()
    education = String()
    start_date = String()
    work_hours = String()
    apply_link = String()
    responsible_employee = ID()
    user_defined_fields = UserDefinedField()




class InfoType(ObjectType):
    """
    A generic type to use if no model is required.
    """
    success = Boolean()
    payload = GenericScalar()