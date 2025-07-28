import phonenumbers
from phonenumbers import carrier, geocoder, timezone, PhoneNumberFormat, number_type
from phonenumbers.phonenumberutil import NumberParseException
from colorama import init, Fore, Style
import time

init(autoreset=True)

def format_number_info(number_str):
    try:
        parsed = phonenumbers.parse(number_str, None)

        if not phonenumbers.is_possible_number(parsed):
            return Fore.RED + "❌ Not a possible number."
        if not phonenumbers.is_valid_number(parsed):
            return Fore.RED + "❌ Not a valid number."

        info = {
            "International Format": phonenumbers.format_number(parsed, PhoneNumberFormat.INTERNATIONAL),
            "National Format": phonenumbers.format_number(parsed, PhoneNumberFormat.NATIONAL),
            "E.164 Format": phonenumbers.format_number(parsed, PhoneNumberFormat.E164),
            "Type": phonenumbers.number_type(parsed),
            "Carrier": carrier.name_for_number(parsed, "en") or "Unknown",
            "Region": geocoder.description_for_number(parsed, "en") or "Unknown",
            "Time Zones": ', '.join(timezone.time_zones_for_number(parsed)) or "Unknown"
        }

        type_map = {
            0: "FIXED_LINE",
            1: "MOBILE",
            2: "FIXED_LINE_OR_MOBILE",
            3: "TOLL_FREE",
            4: "PREMIUM_RATE",
            5: "SHARED_COST",
            6: "VOIP",
            7: "PERSONAL_NUMBER",
            8: "PAGER",
            9: "UAN",
            10: "VOICEMAIL",
            27: "UNKNOWN"
        }

        output = Fore.GREEN + "✅ Number Analysis:\n"
        for key, value in info.items():
            if key == "Type":
                value = type_map.get(value, "UNKNOWN")
            output += f"{Fore.CYAN}{key}: {Fore.YELLOW}{value}\n"
        return output

    except NumberParseException as e:
        return Fore.RED + f"❌ Error: {e}"

def main():
    while True:
        number_input = input(Fore.MAGENTA + "\n📞 Input Number (with area code, or 'exit' to quit): ")
        if number_input.strip().lower() == 'exit':
            print(Fore.GREEN + "Exiting. Goodbye!")
            break

        print(format_number_info(number_input))
        time.sleep(1)

if __name__ == "__main__":
    main()
