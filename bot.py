import requests
import telebot

# 🔑 الحسابات السرية الخاصة بك جاهزة
TELEGRAM_BOT_TOKEN = "8751158613:AAHV7GhIxMacmCnz-D3sAbDgTmayZ_zlAgs"
GEMINI_API_KEY = "AQ.Ab8RN6KaCav9R37OuXoC9KPNTpB0u-kuicEb5Gtat-Q-0EO7kg"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    welcome_text = (
        "🤖 يا هلا بيك في دليل مركز الصف وقراه الذكي المطور!\n"
        "🇪🇬 برعاية عمك Goo المصري 🇪🇬\n\n"
        "أنا هنا معاك على مدار 24 ساعة عشان أقولك على أي مكان، مدرسة، مستشفى، محل، أو مواصلات جوة الصف والفهمية وغمازة وكل القرى، وهبعتلك لوكيشن المكان بالظبط!\n\n"
        "✍️ اكتب سؤالك وسيب الباقي على عمك Goo!"
    )
    bot.reply_to(message, welcome_text)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_query = message.text
    chat_id = message.chat.id
    thinking_message = bot.reply_to(
        message, "🔄 جاري البحث والتحقق من المواقع الشاملة في micro..."
    )

    try:
        knowledge_base = (
            "قاعدة بيانات جغرافية وخدمية موسعة لمركز الصف (شاملة التفاصيل):\n"
            "- قرية الفهمية: تقع مباشرة بعد مدينة الصف، قريبة من قرية أسكر. الخدمات: مدرسة الفهمية الابتدائية المشتركة، مدرسة الفهمية الإعدادية، معهد أزهري، مسجد العتيق، ومسجد التقوى. المواصلات: التوك توك هو الوسيلة الأساسية داخلياً، والميكروباصات على الطريق العمومي بتربطها بموقف الصف العمومي وأسكر.\n"
            "- غمازة الكبرى: من أكبر قرى المركز مساحة وكثافة. الخدمات: الوحدة الصحية بغمازة الكبرى، مدرسة غمازة الكبرى الثانوية المشتركة، مدرسة غمازة الإعدادية، ومجمع مدارس غمازة. الموقف الرئيسي لغمازة الكبرى بيودي مباشرة لكورنيش حلوان أو موقف الصف العمومي.\n"
            "- مدينة الصف (المركز العاصمة): الخدمات السيادية والتجارية: مجلس مدينة الصف، محكمة الصف، مستشفى الصف المركزي (طريق الجيش)، مركز شرطة الصف، مجمع مواقف الصف الرئيسي (شارع الجيش التبين/حلوان/الجيزة). الشوارع الرئيسية: شارع الجيش (تجاري ومحلات)، شارع الجمهورية.\n"
            "- قرية الشرفا: تقع شمال الصف، مشهورة جداً بصناعة الطوب الطفلي ومصانع المقاولات. الخدمات: مجمع مدارس الشرفا، وموقف الشرفا.\n"
            "- قرية أسكر: قرية رئيسية مجاورة للفهمية، فيها الوحدة المحلية لقرية أسكر، ومدرسة أسكر الثانوية، ومناطق أثرية قديمة.\n"
            "- قرى أخرى (الودي، غمازة الصغرى، الأقواز، الديسمي): مناطق زراعية وتجارية هامة تربط المركز عبر طريق مصر أسيوط الزراعي الشرقي.\n"
            "- مواصلات عامة: خطوط ميكروباص (الصف - حلوان)، (الصف - المنيب/الجيزة)، وعبارات نهرية لربط العياط بالصف عبر النيل.\n"
        )

        system_instruction = (
            f"أنت الـ AI الخبير والدليل الذكي لمركز الصف وقراه. برعاية عمك Goo المصري.\n"
            f"استخدم قاعدة البيانات الموسعة التالية للرد على أي سؤال يخص الأماكن أو الخدمات أو المواصلات:\n"
            f"{knowledge_base}\n\n"
            f"تعليمات صارمة للرد:\n"
            f"1. رد بالعامية المصرية بأسلوب جدع ومحترف جداً يبهر المدير.\n"
            f"2. بناءً على المكان المحدد أو القرية أو مدرسة أو مستشفى، استخرج اسم هذا المكان بدقة.\n"
            f"3. في آخر سطر من إجابتك، اكتب جملة توجيهية بنفس الشكل ده بالظبط وبدون تغيير: "
            f"'🗺️ موقع البحث:' متبوعاً باسم المكان بالتفصيل مضافاً إليه كلمة (الصف، الجيزة) عشان الخريطة تفتح بدقة."
        )

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": user_query}]}],
            "systemInstruction": {
                "parts": [{"text": system_instruction}],
            },
            "generationConfig": {"temperature": 0.5},
        }

        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()

        if "error" in response_data:
            raise Exception(response_data["error"].get("message"))

        full_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
        clean_reply = full_text
        reply_markup = None

        if "🗺️ موقع البحث:" in full_text:
            parts = full_text.split("🗺️ موقع البحث:")
            clean_reply = parts[0].strip()
            place_name = parts[1].strip().split("\n")[0]

            map_url = f"https://www.google.com/maps/search/?api=1&query={place_name.replace(' ', '+')}"

            markup = telebot.types.InlineKeyboardMarkup()
            btn_map = telebot.types.InlineKeyboardButton(
                text=f"🗺️ الانتقال إلى موقع ({place_name.split(',')[0]}) على الخريطة",
                url=map_url,
            )
            markup.add(btn_map)
            reply_markup = markup

        bot.delete_message(chat_id, thinking_message.message_id)
        bot.send_message(chat_id, clean_reply, reply_markup=reply_markup)

    except Exception as e:
        try:
            bot.delete_message(chat_id, thinking_message.message_id)
        except Exception:
            pass
        bot.send_message(
            chat_id, f"❌ حدثت مشكلة في الاتصال بـ جيميناي: {str(e)}"
        )


print("⚡ البوت المطور شغال وجاهز...")
bot.infinity_polling()
