import tkinter as tk
from tkinter import scrolledtext, font, messagebox
import random
import winsound
import time
import threading
from datetime import datetime
from pathlib import Path

# Constants
COLORS = {
    'primary': '#2C3E50',
    'secondary': '#34495E',
    'accent': '#27AE60',
    'text_light': 'white'
}
FONT_FAMILY = 'Cairo'
TITLE_FONT_SIZE = 20
CONVERSATION_TIME = 150  # seconds
MAX_MESSAGES = 30
INSULT_PROBABILITY = 0.2

class ClothingStoreChat:
    def __init__(self, master):
        self.master = master
        master.title("محل Souts للملابس")
        master.geometry("1200x800")
        master.configure(bg=COLORS['primary'])

        # إعدادات الخط
        self.font_setup()

        # Conversation participants
        self.seller = {
            "name": "هاني",
            "messages": [
                "تحت أمرك يا باشا",
                "إيه اللي عاجبك في المحل؟",
                "عندنا أحدث الموديلات",
                "تحب أجيبلك مقاس مختلف؟",
                "الموديل ده بيجنن والله",
                "نقدر نعمل خصم لو اشتريت أكتر من قطعة",
                "شوف الخامات دي كلها مستوردة",
                "تحب أجيبلك لون تاني؟",
                "الموديل ده هيخليك شيك أوي",
                "عندنا أحسن الخامات بأسعار مناسبة",
                "الخامة دي مستوردة من أحسن المصانع",
                "ده موديل جديد لسه واصل النهاردة",
                "في منه كل المقاسات والألوان",
                "الموديل ده مناسب جداً للشغل",
                "ممكن نعملك تخصيم كويس",
                "دي أحدث صيحات الموضة",
                "البدلة دي هتخليك أنيق جداً",
                "ده قماش ممتاز ومستورد"
            ],
            "funny_messages": [
                "والله العظيم لو لبست البدلة دي هتبقى شبه عادل إمام 😂",
                "البدلة دي هتخليك تتجوز من تاني يوم 😅",
                "ده لو نزلت بيها الشارع الناس هتقول عليك وزير 🤣",
                "خد البدلة دي وانا اضمنلك الترقية 😎",
                "البدلة دي لو اتعملت في ايطاليا كانت بقت ب 100 ألف 😄",
                "انت كده هتكسر قلوب البنات في الشارع 💔",
                "دي بدلة ملهاش حل، زي صاحبها بالظبط 😊",
                "لو مخدتش البدلة دي هبقى زعلان منك 🥺",
                "شكلك كده هتخلي المدير بتاعك يغير شغله 😂",
                "البدلة دي مستوردة من باريس... يعني من شبرا 🤣"
            ]
        }
        
        self.customers = [
            {
                "name": "محمد", 
                "role": "مهندس",
                "messages": [
                    "عايز بدلة شيك شوية يا باشا",
                    "عندك حاجة مميزة ولا بلاش؟",
                    "بكام البدلة دي بقى؟",
                    "غاليه شوية مش كده؟",
                    "المودل ده مش عاجبني أوي",
                    "فيه مقاسات كبيرة؟",
                    "نفسي في بدلة رسمية زي الموظفين",
                    "فيه خصم للمدرسين؟",
                    "شكل البدلة حلو بس غالي أوي",
                    "عايز أشوف حاجة تانية",
                    "ممكن تجيب لي مقاس أكبر؟",
                    "عندك ألوان تانية؟",
                    "ده آخر سعر ولا ممكن أقل؟",
                    "طيب ممكن تعملي خصم كويس؟"
                ],
                "insult_messages": [
                    "المحل ده وحش أوي يا راجل",
                    "بتبيع زبالة والله",
                    "الأسعار بتاعتك مش معقولة خالص"
                ],
                "funny_messages": [
                    "هو انت متأكد ان دي بدلة؟ شبه خيمة اعتكاف 😂",
                    "البدلة دي تنفع تتلبس في الأفراح والمآتم 🤣",
                    "سعرها ده ولا سعر عربية ملاكي؟ 😅",
                    "هي البدلة دي كانت بتاعة مين قبل كده؟ 😄",
                    "ده انت طلعت أحلى من بتوع المحلات التانية 😎",
                    "طيب ممكن اجربها واجري بيها؟ 😅",
                    "هو انت بتبيع بدل ولا بتبيع فيلل؟ 🏠",
                    "شكلي كده هضرب الصراف الآلي 🏧",
                    "هي دي آخر موضة ولا موضة آخر زمن؟ 🤔",
                    "ممكن ادفع بالتقسيط على 40 سنة؟ 💸"
                ]
            },
            {
                "name": "أحمد", 
                "role": "محاسب",
                "messages": [
                    "عايز أشوف الجديد بقى",
                    "عندك مقاس مول ولا إيه؟",
                    "الموديل ده حلو أوي بجد",
                    "محتاج بدلة للشغل بسرعة",
                    "عندك حاجة بسيطة وجميلة؟",
                    "نفسي في موديل أنيق شوية",
                    "بكام ده بقى؟",
                    "عايز أجيب حاجة مش غالية أوي",
                    "عايز أشوف حاجة تانية",
                    "ممكن تجيب لي مقاس أكبر؟",
                    "عندك ألوان تانية؟",
                    "ده آخر سعر ولا ممكن أقل؟",
                    "طيب ممكن تعملي خصم كويس؟"
                ],
                "insult_messages": [
                    "غالي أوي يا سيدي بجد",
                    "مش هقدر أشتري كده أبدا والله",
                    "انت بتنصب والله يا راجل"
                ],
                "funny_messages": [
                    "هو انت متأكد ان دي بدلة؟ شبه خيمة اعتكاف 😂",
                    "البدلة دي تنفع تتلبس في الأفراح والمآتم 🤣",
                    "سعرها ده ولا سعر عربية ملاكي؟ 😅",
                    "هي البدلة دي كانت بتاعة مين قبل كده؟ 😄",
                    "ده انت طلعت أحلى من بتوع المحلات التانية 😎",
                    "طيب ممكن اجربها واجري بيها؟ 😅",
                    "هو انت بتبيع بدل ولا بتبيع فيلل؟ 🏠",
                    "شكلي كده هضرب الصراف الآلي 🏧",
                    "هي دي آخر موضة ولا موضة آخر زمن؟ 🤔",
                    "ممكن ادفع بالتقسيط على 40 سنة؟ 💸"
                ]
            },
            {
                "name": "كريم", 
                "role": "مصمم أزياء",
                "messages": [
                    "مالك يا باشا، عندك حاجة جديدة؟",
                    "نفسي أشوف موديلات مختلفة شوية",
                    "عندك حاجة مش تقليدية؟",
                    "الألوان دي مش بتاعتي خالص",
                    "عايز موديل يجنن يعني",
                    "فيه حاجة مميزة للشباب؟",
                    "بكام البدلة دي؟",
                    "عندك إيه في الموضة الجديدة؟",
                    "عايز أشوف حاجة تانية",
                    "ممكن تجيب لي مقاس أكبر؟",
                    "عندك ألوان تانية؟",
                    "ده آخر سعر ولا ممكن أقل؟",
                    "طيب ممكن تعملي خصم كويس؟"
                ],
                "insult_messages": [
                    "المحل ده مفيهوش ذوق خالص",
                    "بتبيع حاجة وحشة أوي",
                    "الموديلات دي من زمان خلصت"
                ],
                "funny_messages": [
                    "هو انت متأكد ان دي بدلة؟ شبه خيمة اعتكاف 😂",
                    "البدلة دي تنفع تتلبس في الأفراح والمآتم 🤣",
                    "سعرها ده ولا سعر عربية ملاكي؟ 😅",
                    "هي البدلة دي كانت بتاعة مين قبل كده؟ 😄",
                    "ده انت طلعت أحلى من بتوع المحلات التانية 😎",
                    "طيب ممكن اجربها واجري بيها؟ 😅",
                    "هو انت بتبيع بدل ولا بتبيع فيلل؟ 🏠",
                    "شكلي كده هضرب الصراف الآلي 🏧",
                    "هي دي آخر موضة ولا موضة آخر زمن؟ 🤔",
                    "ممكن ادفع بالتقسيط على 40 سنة؟ 💸"
                ]
            },
            {
                "name": "سليم", 
                "role": "متقاعد",
                "messages": [
                    "عايز بدلة كلاسيك زي زمان",
                    "الموديلات دي كلها غريبة عليا",
                    "عندك حاجة محترمة؟",
                    "نفسي في بدلة تليق بسني",
                    "بكام البدلة دي؟",
                    "الألوان دي مش بتاعتي أنا",
                    "عايز حاجة سادة وجميلة",
                    "عايز أشوف حاجة تانية",
                    "ممكن تجيب لي مقاس أكبر؟",
                    "عندك ألوان تانية؟",
                    "ده آخر سعر ولا ممكن أقل؟",
                    "طيب ممكن تعملي خصم كويس؟"
                ],
                "insult_messages": [
                    "الأسعار دي مش معقولة خالص",
                    "مش هقدر أشتري حاجة غالية كده",
                    "انت بتبيع ولا بتسرق؟"
                ],
                "funny_messages": [
                    "هو انت متأكد ان دي بدلة؟ شبه خيمة اعتكاف 😂",
                    "البدلة دي تنفع تتلبس في الأفراح والمآتم 🤣",
                    "سعرها ده ولا سعر عربية ملاكي؟ 😅",
                    "هي البدلة دي كانت بتاعة مين قبل كده؟ 😄",
                    "ده انت طلعت أحلى من بتوع المحلات التانية 😎",
                    "طيب ممكن اجربها واجري بيها؟ 😅",
                    "هو انت بتبيع بدل ولا بتبيع فيلل؟ 🏠",
                    "شكلي كده هضرب الصراف الآلي 🏧",
                    "هي دي آخر موضة ولا موضة آخر زمن؟ 🤔",
                    "ممكن ادفع بالتقسيط على 40 سنة؟ 💸"
                ]
            },
            {
                "name": "رنا", 
                "role": "مدرسة",
                "messages": [
                    "عايزة بدلة للمدرسين",
                    "عندك حاجة محترمة وجميلة؟",
                    "بكام البدلة دي؟",
                    "نفسي في موديل أنيق للشغل",
                    "الألوان دي حلوة أوي",
                    "فيه خصم للمدرسين؟",
                    "عايزة حاجة مش غالية أوي",
                    "عايز أشوف حاجة تانية",
                    "ممكن تجيب لي مقاس أكبر؟",
                    "عندك ألوان تانية؟",
                    "ده آخر سعر ولا ممكن أقل؟",
                    "طيب ممكن تعملي خصم كويس؟"
                ],
                "insult_messages": [
                    "غالي أوي يا باشا",
                    "مش هقدر أشتري كده أبدا",
                    "الأسعار دي مش معقولة"
                ],
                "funny_messages": [
                    "هو انت متأكد ان دي بدلة؟ شبه خيمة اعتكاف 😂",
                    "البدلة دي تنفع تتلبس في الأفراح والمآتم 🤣",
                    "سعرها ده ولا سعر عربية ملاكي؟ 😅",
                    "هي البدلة دي كانت بتاعة مين قبل كده؟ 😄",
                    "ده انت طلعت أحلى من بتوع المحلات التانية 😎",
                    "طيب ممكن اجربها واجري بيها؟ 😅",
                    "هو انت بتبيع بدل ولا بتبيع فيلل؟ 🏠",
                    "شكلي كده هضرب الصراف الآلي 🏧",
                    "هي دي آخر موضة ولا موضة آخر زمن؟ 🤔",
                    "ممكن ادفع بالتقسيط على 40 سنة؟ 💸"
                ]
            },
            {
                "name": "عمر", 
                "role": "طالب",
                "messages": [
                    "عايز بدلة للمناسبات",
                    "عندك حاجة حلوة للشباب؟",
                    "بكام ده بقى؟",
                    "نفسي في موديل يهبل",
                    "فيه خصم للطلاب؟",
                    "الموديلات دي جميلة أوي",
                    "عايز حاجة مش غالية",
                    "عايز أشوف حاجة تانية",
                    "ممكن تجيب لي مقاس أكبر؟",
                    "عندك ألوان تانية؟",
                    "ده آخر سعر ولا ممكن أقل؟",
                    "طيب ممكن تعملي خصم كويس؟"
                ],
                "insult_messages": [
                    "غالي أوي يا عم",
                    "مش هقدر أشتري كده",
                    "الأسعار دي مش معقولة خالص"
                ],
                "funny_messages": [
                    "هو انت متأكد ان دي بدلة؟ شبه خيمة اعتكاف 😂",
                    "البدلة دي تنفع تتلبس في الأفراح والمآتم 🤣",
                    "سعرها ده ولا سعر عربية ملاكي؟ 😅",
                    "هي البدلة دي كانت بتاعة مين قبل كده؟ 😄",
                    "ده انت طلعت أحلى من بتوع المحلات التانية 😎",
                    "طيب ممكن اجربها واجري بيها؟ 😅",
                    "هو انت بتبيع بدل ولا بتبيع فيلل؟ 🏠",
                    "شكلي كده هضرب الصراف الآلي 🏧",
                    "هي دي آخر موضة ولا موضة آخر زمن؟ 🤔",
                    "ممكن ادفع بالتقسيط على 40 سنة؟ 💸"
                ]
            },
            {
                "name": "هشام", 
                "role": "مبرمج",
                "messages": [
                    "عايز بدلة للشغل",
                    "عندك موديل مرتب؟",
                    "بكام ده بقى؟",
                    "نفسي في حاجة مريحة",
                    "الموديلات دي حلوة أوي",
                    "فيه خصم للموظفين؟",
                    "عايز حاجة أنيقة وعملية",
                    "عايز أشوف حاجة تانية",
                    "ممكن تجيب لي مقاس أكبر؟",
                    "عندك ألوان تانية؟",
                    "ده آخر سعر ولا ممكن أقل؟",
                    "طيب ممكن تعملي خصم كويس؟"
                ],
                "insult_messages": [
                    "غالي أوي يا باشا",
                    "مش هقدر أشتري كده",
                    "الأسعار دي مش معقولة"
                ],
                "funny_messages": [
                    "هو انت متأكد ان دي بدلة؟ شبه خيمة اعتكاف 😂",
                    "البدلة دي تنفع تتلبس في الأفراح والمآتم 🤣",
                    "سعرها ده ولا سعر عربية ملاكي؟ 😅",
                    "هي البدلة دي كانت بتاعة مين قبل كده؟ 😄",
                    "ده انت طلعت أحلى من بتوع المحلات التانية 😎",
                    "طيب ممكن اجربها واجري بيها؟ 😅",
                    "هو انت بتبيع بدل ولا بتبيع فيلل؟ 🏠",
                    "شكلي كده هضرب الصراف الآلي 🏧",
                    "هي دي آخر موضة ولا موضة آخر زمن؟ 🤔",
                    "ممكن ادفع بالتقسيط على 40 سنة؟ 💸"
                ]
            }
        ]
        
        # Sound paths with error checking
        self.sound_paths = {
            'greeting': Path(r"D:\work\python\123.wav"),
            'expulsion': Path(r"D:\work\python\1303451583564087367.wav"),
            'background': Path(r"D:\work\python\WhatsApp Audio 2024-12-21 at 03.15.56_77d358ee.wav")
        }
        self._verify_sound_files()

        # Seller responses to insults
        self.seller_responses = [
            "مش هقدر أتعامل معاك، اتفضل بره المحل",
            "معلش مش هقدر أكمل معاك، اتفضل بره",
            "لو سمحت اطلع بره المحل حالاً",
            "مش عايزين زباين بالشكل ده، اتفضل بره"
        ]

        # Conversation setup
        self.current_customer_index = 0
        self.conversation_running = False
        
        # Initialize conversation timer
        self.time_remaining = CONVERSATION_TIME
        self.timer_running = False
        
        # Initialize save directory
        self.save_dir = Path("saved_conversations")
        self.save_dir.mkdir(exist_ok=True)
        
        # Create UI components
        self.create_ui()
        
    def font_setup(self):
        # إعدادات الخط
        self.title_font = font.Font(family=FONT_FAMILY, size=TITLE_FONT_SIZE, weight='bold')
        self.chat_font = font.Font(family=FONT_FAMILY, size=14)
        
    def create_ui(self):
        # إطار رئيسي
        main_frame = tk.Frame(self.master, bg=COLORS['secondary'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # إطار الأزرار العلوية
        button_frame = tk.Frame(main_frame, bg=COLORS['secondary'])
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        # زر بدء المحادثة
        self.start_button = tk.Button(
            button_frame, 
            text="ابدأ المحادثة", 
            command=self.start_conversation,
            font=(FONT_FAMILY, TITLE_FONT_SIZE, 'bold'),
            bg=COLORS['accent'],
            fg=COLORS['text_light'],
            relief=tk.RAISED,
            borderwidth=5,
            padx=20,
            pady=10,
            width=20
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        # زر تخطي العميل
        self.skip_button = tk.Button(
            button_frame,
            text="تخطي العميل",
            command=self.skip_customer,
            font=(FONT_FAMILY, TITLE_FONT_SIZE, 'bold'),
            bg=COLORS['accent'],
            fg=COLORS['text_light'],
            relief=tk.RAISED,
            borderwidth=5,
            padx=20,
            pady=10,
            width=15,
            state=tk.DISABLED
        )
        self.skip_button.pack(side=tk.LEFT, padx=5)

        # زر حفظ المحادثة
        self.save_button = tk.Button(
            button_frame,
            text="حفظ المحادثة",
            command=self.save_conversation,
            font=(FONT_FAMILY, TITLE_FONT_SIZE, 'bold'),
            bg=COLORS['accent'],
            fg=COLORS['text_light'],
            relief=tk.RAISED,
            borderwidth=5,
            padx=20,
            pady=10,
            width=15
        )
        self.save_button.pack(side=tk.LEFT, padx=5)

        # عداد العملاء
        self.customer_counter = tk.Label(
            button_frame,
            text=f"العملاء المتبقين: {len(self.customers)}",
            font=(FONT_FAMILY, TITLE_FONT_SIZE, 'bold'),
            bg=COLORS['secondary'],
            fg=COLORS['text_light']
        )
        self.customer_counter.pack(side=tk.RIGHT, padx=10)

        # مؤقت المحادثة
        self.timer_label = tk.Label(
            button_frame,
            text="الوقت المتبقي: 150 ثانية",
            font=(FONT_FAMILY, TITLE_FONT_SIZE, 'bold'),
            bg=COLORS['secondary'],
            fg=COLORS['text_light']
        )
        self.timer_label.pack(side=tk.RIGHT, padx=10)

        # عنوان متحرك
        title_label = tk.Label(
            main_frame, 
            text="محادثات محل Souts للملابس", 
            font=(FONT_FAMILY, TITLE_FONT_SIZE, 'bold'),
            bg=COLORS['secondary'], 
            fg=COLORS['text_light'],
            relief=tk.RAISED,
            borderwidth=5,
            padx=20,
            pady=10
        )
        title_label.pack(fill=tk.X, pady=10)

        # إطار معلومات المحل
        store_info_frame = tk.Frame(main_frame, bg=COLORS['secondary'])
        store_info_frame.pack(fill=tk.X, padx=10, pady=5)

        # معلومات المحل
        store_details = tk.Label(
            store_info_frame, 
            text="محل Souts للملابس الرسمية | أحدث الموديلات | أفضل الخامات",
            font=(FONT_FAMILY, 14),
            bg=COLORS['secondary'],
            fg=COLORS['text_light']
        )
        store_details.pack(side=tk.LEFT, padx=10)

        # ساعة المحل
        self.clock_label = tk.Label(
            store_info_frame, 
            font=(FONT_FAMILY, 14),
            bg=COLORS['secondary'],
            fg=COLORS['text_light']
        )
        self.clock_label.pack(side=tk.RIGHT, padx=10)
        self.update_clock()

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            width=80, 
            height=25,
            font=(FONT_FAMILY, 14),
            bg=COLORS['secondary'],
            fg=COLORS['text_light'],
            relief=tk.SUNKEN,
            borderwidth=5,
            padx=10,
            pady=10
        )
        self.chat_display.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        self.chat_display.config(state=tk.DISABLED)

    def on_enter(self, e):
        # تغيير لون الزر عند المرور
        e.widget.config(bg='#2ECC71', cursor='hand2')

    def on_leave(self, e):
        # إعادة اللون الأصلي
        e.widget.config(bg='#27AE60', cursor='')

    def update_clock(self):
        # تحديث الساعة بشكل مستمر
        current_time = datetime.now().strftime("%I:%M %p")
        arabic_digits = {
            '0': '٠', '1': '١', '2': '٢', '3': '٣', 
            '4': '٤', '5': '٥', '6': '٦', '7': '٧', 
            '8': '٨', '9': '٩'
        }
        # تحويل الأرقام للعربية
        arabic_time = ''.join(arabic_digits.get(char, char) for char in current_time)
        self.clock_label.config(text=f"الوقت: {arabic_time}")
        self.master.after(1000, self.update_clock)

    def skip_customer(self):
        if self.conversation_running:
            self.conversation_running = False
            self.current_customer_index += 1
            if self.current_customer_index < len(self.customers):
                self.display_message("تم تخطي العميل الحالي...", align='center')
                threading.Thread(target=self.run_conversation, daemon=True).start()
            else:
                self.show_final_message()

    def save_conversation(self):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.save_dir / f"conversation_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.chat_display.get(1.0, tk.END))
            
            messagebox.showinfo("تم الحفظ", f"تم حفظ المحادثة في الملف:\n{filename}")
        except Exception as e:
            messagebox.showerror("خطأ في الحفظ", f"حدث خطأ أثناء حفظ المحادثة:\n{str(e)}")

    def update_timer(self):
        if self.timer_running and self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_label.config(text=f"الوقت المتبقي: {self.time_remaining} ثانية")
            self.master.after(1000, self.update_timer)

    def start_conversation(self):
        self.start_button.config(state=tk.DISABLED)
        self.skip_button.config(state=tk.NORMAL)
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        self.conversation_running = True
        self.time_remaining = CONVERSATION_TIME
        self.timer_running = True
        self.update_timer()
        
        threading.Thread(target=self.run_conversation, daemon=True).start()

    def end_customer_conversation(self, customer):
        if not self.conversation_running:
            farewell_messages = [
                f"{self.seller['name']}: مع السلامة",
                "------------------ نهاية المحادثة ------------------"
            ]
        else:
            farewell_messages = [
                f"{self.seller['name']}: شكراً لزيارتك يا {customer['name']}", 
                f"{customer['name']}: شكراً ليك يا {self.seller['name']}", 
                f"{self.seller['name']}: تشرفنا بزيارتك",
                "------------------ نهاية المحادثة ------------------"
            ]
        
        for message in farewell_messages:
            self.display_message(message, align='center')
            time.sleep(1)
        
        self.current_customer_index += 1
        self.conversation_running = False
        self.timer_running = False
        self.customer_counter.config(text=f"العملاء المتبقين: {len(self.customers) - self.current_customer_index}")
        
        if self.current_customer_index < len(self.customers):
            time.sleep(2)
            threading.Thread(target=self.run_conversation, daemon=True).start()
        else:
            self.show_final_message()

    def run_conversation(self):
        if self.current_customer_index >= len(self.customers):
            self.show_final_message()
            return
        
        current_customer = self.customers[self.current_customer_index]
        stop_background_sound = threading.Event()
        
        background_sound_thread = threading.Thread(
            target=self.play_background_sound, 
            args=(stop_background_sound,), 
            daemon=True
        )
        background_sound_thread.start()
        
        # Play greeting sound
        self.play_sound(self.sound_paths['greeting'])
        
        # Welcome messages with humor
        welcome_messages = [
            f"{current_customer['name']} ({current_customer['role']}): ازيك يا معلم 👋",
            f"{self.seller['name']}: نورت المحل يا قمر 🌟",
            f"{current_customer['name']}: المحل منور بأهله... وبالنور الحلو اللي مركبه فوق ده 😄",
            f"{self.seller['name']}: ده نور وجودك يا باشا... تحب تشوف ايه النهاردة؟ 😊"
        ]
        
        for message in welcome_messages:
            self.display_message(message, align='left' if current_customer['name'] in message else 'right')
            time.sleep(1)
        
        # Main conversation loop with funny interactions
        start_time = time.time()
        message_count = 0
        max_messages = MAX_MESSAGES
        
        while time.time() - start_time < CONVERSATION_TIME and self.conversation_running and message_count < max_messages:
            # Mix regular and funny messages
            if random.random() < 0.4:  # 40% chance for funny messages
                customer_message = random.choice(current_customer['funny_messages'])
                seller_message = random.choice(self.seller['funny_messages'])
            else:
                customer_message = random.choice(current_customer['messages'])
                seller_message = random.choice(self.seller['messages'])
            
            self.display_message(f"{current_customer['name']}: {customer_message}", align='left')
            time.sleep(random.uniform(1, 2))
            message_count += 1
            
            self.display_message(f"{self.seller['name']}: {seller_message}", align='right')
            time.sleep(random.uniform(1, 2))
            message_count += 1
            
            # Random chance for insult with funny exit
            if random.random() < INSULT_PROBABILITY:
                self.handle_insult(current_customer)
                break
        
        stop_background_sound.set()
        
        if not self.conversation_running:
            return
            
        self.end_customer_conversation(current_customer)

    def play_background_sound(self, stop_event):
        while not stop_event.is_set():
            try:
                winsound.PlaySound(self.sound_paths['background'], winsound.SND_FILENAME)
            except Exception as e:
                print(f"خطأ في تشغيل الصوت الخلفي: {e}")
                break
            time.sleep(1)  

    def handle_insult(self, customer):
        # Funny insult sequence
        insult = random.choice(customer['insult_messages'])
        self.display_message(f"{customer['name']}: {insult}", align='left')
        time.sleep(1)
        
        funny_responses = [
            f"{self.seller['name']}: يا باشا احنا مش قد مقامك، اتفضل على برا 👋",
            f"{customer['name']}: هو في محلات تانية اصلاً؟ 🤔",
            f"{self.seller['name']}: اه في كتير، بس مش هيستحملوك زي ما انا استحملت 😅",
            f"{customer['name']}: طيب اخر كلام... عندك مقاس اكبر من كده؟ 😂",
            f"{self.seller['name']}: لا خلاص يا معلم، البدل خلصت فجأة 🏃‍♂️"
        ]
        
        for message in funny_responses:
            self.display_message(message, align='left' if customer['name'] in message else 'right')
            time.sleep(1)
        
        # Play expulsion sound
        self.play_sound(self.sound_paths['expulsion'])
        
        self.display_message("------ تم طرد الزبون بنجاح 🎉 ------", align='center')
        
        self.conversation_running = False
        self.end_customer_conversation(customer)

    def show_final_message(self):
        funny_final_messages = [
            f"{self.seller['name']}: الحمد لله على نعمة العقل... مكنش فاضل غير شوية 😅",
            f"{self.seller['name']}: يارب يكون بكره أحسن... مش هيكون أسوأ من النهاردة 🙏",
            f"{self.seller['name']}: تعبت من الضحك... قصدي من الشغل 😂",
            "------------------ نهاية يوم العمل (الحمد لله) ------------------"
        ]
        
        for message in funny_final_messages:
            self.display_message(message, align='right')
            time.sleep(1)
        
        self.start_button.config(state=tk.NORMAL)
        self.current_customer_index = 0
        self.play_sound(self.sound_paths['greeting'])

    def display_message(self, message, align='left'):
        self.chat_display.config(state=tk.NORMAL)
        
        alignment_tag = 'left' if align == 'left' else 'right'
        self.chat_display.tag_config('left', justify='left')
        self.chat_display.tag_config('right', justify='right')
        
        for char in message + "\n":
            self.chat_display.insert(tk.END, char, (alignment_tag,))
            self.chat_display.see(tk.END)
            self.chat_display.update()
            time.sleep(0.05)  
        
        self.chat_display.config(state=tk.DISABLED)
        
    def play_sound(self, sound_path):
        try:
            winsound.PlaySound(sound_path, winsound.SND_FILENAME)
        except Exception as e:
            print(f"خطأ في تشغيل الصوت: {e}")

    def _verify_sound_files(self):
        for sound_name, sound_path in self.sound_paths.items():
            if not sound_path.exists():
                print(f"خطأ: لم يتم العثور على ملف الصوت '{sound_name}' في المسار '{sound_path}'")

def main():
    root = tk.Tk()
    app = ClothingStoreChat(root)
    root.mainloop()

if __name__ == "__main__":
    main()