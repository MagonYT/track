import phonenumbers
from phonenumbers import carrier, geocoder, timezone, PhoneNumberFormat
from phonenumbers.phonenumberutil import NumberParseException
from colorama import init, Fore
import time

init(autoreset=True)

known_disposable_carriers = {
    "Stour Marine", "Voxbone", "Bandwidth", "Twilio", "Tyntec", "Onvoy", "Plivo", "Level 3", "Vonage",
    "Google", "Skype", "TextNow", "Hushed", "Burner"
}

def analyze_number(number_str):
    try:
        parsed = phonenumbers.parse(number_str.strip(), None)

        if not phonenumbers.is_possible_number(parsed):
            return Fore.RED + "❌ Not a possible number."
        if not phonenumbers.is_valid_number(parsed):
            return Fore.RED + "❌ Not a valid number."

        num_format = {
            "International Format": phonenumbers.format_number(parsed, PhoneNumberFormat.INTERNATIONAL),
            "National Format": phonenumbers.format_number(parsed, PhoneNumberFormat.NATIONAL),
            "E.164 Format": phonenumbers.format_number(parsed, PhoneNumberFormat.E164),
        }

        num_type_map = {
            0: "FIXED_LINE", 1: "MOBILE", 2: "FIXED_LINE_OR_MOBILE",
            3: "TOLL_FREE", 4: "PREMIUM_RATE", 5: "SHARED_COST",
            6: "VOIP", 7: "PERSONAL_NUMBER", 8: "PAGER", 9: "UAN",
            10: "VOICEMAIL", 27: "UNKNOWN"
        }

        number_type = phonenumbers.number_type(parsed)
        number_type_str = num_type_map.get(number_type, "UNKNOWN")

        num_carrier = carrier.name_for_number(parsed, "en") or "Unknown"
        num_region = geocoder.description_for_number(parsed, "en") or "Unknown"
        num_tz = ', '.join(timezone.time_zones_for_number(parsed)) or "Unknown"

        is_voip = number_type == 6 or num_carrier in known_disposable_carriers
        is_disposable = "Yes" if num_carrier in known_disposable_carriers else "No"

        output = Fore.GREEN + "\n✅ Number Analysis:\n"
        for k, v in num_format.items():
            output += f"{Fore.CYAN}{k}: {Fore.YELLOW}{v}\n"
        output += f"{Fore.CYAN}Type: {Fore.YELLOW}{number_type_str}\n"
        output += f"{Fore.CYAN}Carrier: {Fore.YELLOW}{num_carrier}\n"
        output += f"{Fore.CYAN}Region: {Fore.YELLOW}{num_region}\n"
        output += f"{Fore.CYAN}Time Zones: {Fore.YELLOW}{num_tz}\n"
        output += f"{Fore.CYAN}VoIP/Disposable: {Fore.YELLOW}{is_disposable} ({'Likely VOIP' if is_voip else 'Normal'})\n"

        return output

    except NumberParseException as e:
        return Fore.RED + f"❌ Error: {e}"


def main():
    print(Fore.MAGENTA + "📞 Enter one or more phone numbers, separated by commas.\nExample: +44 7537135157, +1 2025550198\n")

    while True:
        raw_input = input(Fore.MAGENTA + "\n📥 Input Number(s) or 'exit': ")
        if raw_input.lower().strip() == 'exit':
            print(Fore.GREEN + "✅ Done.")
            break

        numbers = [n.strip() for n in raw_input.split(',') if n.strip()]
        for num in numbers:
            print(analyze_number(num))
            time.sleep(0.5)


if __name__ == "__main__":
    main()
