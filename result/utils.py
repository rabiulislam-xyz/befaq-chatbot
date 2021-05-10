from befaq.settings import bot
from result.exceptions import InvalidMessageError, ResultNotFoundError
from result.services import get_result_from_api

marhala_list = {
    1: "তাকমিল",
    2: "ফযীলত",
    3: "সানাবিয়া উলইয়া",
    4: "মুতাওয়াসসিতাহ",
    5: "ইবতিদাইয়্যাহ",
    6: "হিফযুল কুরআন",
    7: "ইলমুত তাজবীদ ওয়াল কিরাআত"
}

marhala_list_for_help_text = "\n".join([f'{k}: {v}' for k, v in marhala_list.items()])

help_text = f'''রেজাল্টের জন্য এই ফরম্যাটে ম্যাসেজ করুন
সন<space>মারহালা-নং<space>রোল

যেমন ২০১৭ সন ফযীলতের ৩৯১ রোলের রেজাল্ট জানতে লিখুন: 2017 2 391 

সকল মারহালা নংঃ
{marhala_list_for_help_text}
'''

not_understood = 'আপনার ম্যাসেজ বোঝা যায়নি, বিস্তারিত জানতে `help` লিখুন'
salam_answer = 'ওয়ালাইকুমুস সালাম'

incoming_help_texts = ['help', 'হেল্প', 'get started']
incoming_salam_texts = ['salam', 'assalamu alaikum', 'আসসালামু আলাইকুম', 'সালাম']


def validate_year(year):
    if not year in range(2010, 2022):
        raise ValueError("invalid year format")
    return year


def validate_marhala(marhala):
    # dont know why! the website has missed number 4
    if marhala in range(1, 9) and marhala != 4:
        return marhala if marhala <= 3 else marhala + 1

    raise ValueError("invalid marhala format")


def validate_roll(roll):
    if not roll < 1000000:
        raise ValueError("invalid roll format")
    return roll


def validate_result_query(message_text):
    try:
        year, marhala, roll = [int(i) for i in message_text.split(" ")]
        year = validate_year(year)
        marhala = validate_marhala(marhala)
        roll = validate_roll(roll)
        return year, marhala, roll
    except Exception as e:
        print(f"result query validation failed: {e}")
        raise InvalidMessageError(not_understood)


translation_map = {
    'division': 'বিভাগ',
    'dob': 'জন্ম তারিখ',
    'father': 'পিতা',
    'gender': 'জেন্ডার',
    'graceLabel': 'graceLabel',
    'graceValue': 'graceValue',
    'madrasa': 'মাদরাসা',
    'name': 'নাম',
    'posSub': 'posSub',
    'position': 'position',
    'regId': 'রেজিস্ট্রেশন আইডি',
}


def prepare_result(result):
    total = result.pop('total', '')
    subjects = result.pop('subjects', [])
    results = result.pop('results', [])

    description = ''
    for k, v in result.items():
        description += f'{translation_map.get(k, k)}: {v}\n'

    prepared_result = ''
    for s, r in zip(subjects, results):
        prepared_result += f'{s}: {r}\n'
    prepared_result += f'মোট: {total}\n'

    return description, prepared_result


def send_message(recipient_id, message_text):
    if message_text in incoming_help_texts:
        bot.send_text_message(recipient_id, help_text)

    elif message_text in incoming_salam_texts:
        bot.send_text_message(recipient_id, salam_answer)

    else:
        try:
            year, marhala, roll = validate_result_query(message_text)
            result = get_result_from_api(year, marhala, roll)
            print(f"found result: {result}")

            description, result_data = prepare_result(result)
            bot.send_text_message(recipient_id, description)
            bot.send_text_message(recipient_id, result_data)

        except (InvalidMessageError, ResultNotFoundError) as e:
            print(e)
            bot.send_text_message(recipient_id, str(e))

        except Exception as e:
            print(e)
            return bot.send_text_message(
                recipient_id, f'Something went wrong, please contact with developer. [{e}]')


def process_message(message_json):
    print(message_json)
    for event in message_json['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                # Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    message_text = message['message']['text'].lower().strip()
                    send_message(recipient_id, message_text)
