from phonenumbers import carrier
import phonenumbers

number = input("Input Number (INCLUDE AREA CODE): ")

from phonenumbers import geocoder
ch_number = phonenumbers.parse(number, "CH")
print(geocoder.description_for_number(ch_number, "en"))


service_number = phonenumbers.parse(number, "RO")
print(carrier.name_for_number(service_number, "en"))

# Copyright 2022 DevEvil.xyz
