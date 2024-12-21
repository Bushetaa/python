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

        # Single customer setup
        self.customers = [
            {
                "name": "محمد", 
                "role": "زبون غلبان",
                "messages": [
                    "عايز بدلة شيك شوية يا باشا",
                    "عندك حاجة مميزة ولا بلاش؟",
                    "بكام البدلة دي بقى؟",
                    "غاليه شوية مش كده؟",
                    "المودل ده مش عاجبني أوي",
                    "فيه مقاسات كبيرة؟",
                    "نفسي في بدلة رسمية للشغل",
                    "فيه خصم ولا لسه؟",
                    "شكل البدلة حلو بس غالي أوي"
                ],
                "funny_messages": [
                    "هو انت متأكد ان دي بدلة؟ شبه خيمة اعتكاف 😂",
                    "البدلة دي تنفع تتلبس في الأفراح والمآتم 🤣",
                    "سعرها ده ولا سعر عربية ملاكي؟ 😅",
                    "هي البدلة دي كانت بتاعة مين قبل كده؟ 😄",
                    "طيب ممكن اجربها واجري بيها؟ 😅",
                    "هو انت بتبيع بدل ولا بتبيع فيلل؟ 🏠",
                    "شكلي كده هضرب الصراف الآلي 🏧",
                    "ممكن ادفع بالتقسيط على 40 سنة؟ 💸"
                ],
                "fight_messages": [
                    "انت عارف انا مين؟ 😠",
                    "هو المحل ده بتاع باباك؟ 😤",
                    "انت فاكر نفسك مين يا روح امك؟ 😡",
                    "طب تعالى برة المحل كده 💪",
                    "انت مش عارف انا ممكن اعمل ايه؟ 🤬",
                    "والله ما هسيب المحل ده غير لما اكسره 😈"
                ]
            }
        ]

        # Seller responses
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
            ],
            "fight_messages": [
                "يا روح اختك انت جاي تهزر ولا ايه؟ 😠",
                "متعلاش صوتك يا روح امك 😤",
                "اطلع برة يا بتاع انت 😡",
                "هو انت فاكر نفسك مين يا فالح! 🤬",
                "شكلك عايز تتضرب النهاردة 💪",
                "يلا برة المحل ما فيش بدل ولا بطيخ 😈"
            ]
        }

        # Sound paths with error checking
        self.sound_paths = {
            'greeting': Path(r"D:\work\python\123.wav"),
            'expulsion': Path(r"D:\work\python\1303451583564087367.wav"),
            'background': Path(r"D:\work\python\WhatsApp Audio 2024-12-21 at 03.15.56_77d358ee.wav")
        }
        self._verify_sound_files()

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
        current_customer = self.customers[0]
        stop_background_sound = threading.Event()
        
        background_sound_thread = threading.Thread(
            target=self.play_background_sound, 
            args=(stop_background_sound,), 
            daemon=True
        )
        background_sound_thread.start()
        
        # Play greeting sound
        self.play_sound(self.sound_paths['greeting'])
        
        # المحادثة الأساسية
        conversation_sequence = [
            (current_customer['name'], "السلام عليكم... هو حضرتك عندك بدل؟"),
            (self.seller['name'], "وعليكم السلام يا قمر، احنا عندنا كل حاجة... البدلة اللي في بالك موجودة عندي 😎"),
            (current_customer['name'], "طيب ممكن اشوف بدلة مقاس لارج؟"),
            (self.seller['name'], "لارج؟ متقلقش... عندي مقاسات من لارج لحد جامبو 😅"),
            (current_customer['name'], "طيب ممكن اجرب دي؟"),
            (self.seller['name'], "اتفضل يا باشا... بس خلي بالك البدلة دي لو لبستها هتبقى شبه عادل إمام في فيلم الكيت كات 😂"),
            (current_customer['name'], "بس دي ضيقة شوية..."),
            (self.seller['name'], "ضيقة؟ دي انت لو مشيت بيها في الشارع الناس هتقول عليك مستورد 🌟"),
            (current_customer['name'], "طيب وبكام دي؟"),
            (self.seller['name'], "دي يا باشا... *يتنحنح*... بـ 2000 جنيه بس"),
            (current_customer['name'], "2000؟! انت بتهزر صح؟"),
            (self.seller['name'], "هزار؟ دي اصلاً كانت ب 3000 بس انت شكلك زبون محترم وانا بحب الناس المحترمة 😇"),
            (current_customer['name'], "لا كتير والله... ممكن 1000؟"),
            (self.seller['name'], "1000؟ هو احنا بنبيع شاورما يا باشا؟ 😅"),
            (current_customer['name'], "طيب 1200 وبالكتير يعني"),
            (self.seller['name'], "بص يا حبيبي... عشان خاطر عيونك الحلوة... 1800 وكلمة اخيرة"),
            (current_customer['name'], "لا والله كتير... انا شفت بدل احسن من كده ب 1000"),
            (self.seller['name'], "احسن من كده؟ هو انت بتقارن فيراري بعربية توك توك؟ 😂"),
            (current_customer['name'], "يا عم انت بتضحك علينا ولا ايه؟"),
            (self.seller['name'], "اضحك عليك؟ ده انا لو بضحك على حد هضحك على نفسي 🤣"),
            (current_customer['name'], "طيب خلاص... هشوف محل تاني"),
            (self.seller['name'], "محل تاني؟ ده انت لو لفيت البلد كلها مش هتلاقي بدلة زي دي... دي حتى القماش بتاعها مستورد"),
            (current_customer['name'], "مستورد منين بقى؟"),
            (self.seller['name'], "من باريس... يعني من شبرا 😅"),
            (current_customer['name'], "هههه طيب يا عم... 1500 وخلاص"),
            (self.seller['name'], "1500؟ طيب تعالى نعمل حاجة حلوة... 1700 وهديك كرافتة هدية"),
            (current_customer['name'], "الكرافتة بكام دي اصلاً؟"),
            (self.seller['name'], "دي؟ دي ب 200... بس عشان خاطرك هخليها عليك ب 199.99 😎"),
            (current_customer['name'], "لا بجد انت راجل مضحك 😂"),
            (self.seller['name'], "شفت بقى؟ وكمان البدلة هتخليك مضحك زيي 🤣"),
            (current_customer['name'], "طيب خلاص يا معلم... 1600 وبالكرافتة"),
            (self.seller['name'], "خلاص يا معلم اتفقنا... بس بشرط"),
            (current_customer['name'], "شرط ايه؟"),
            (self.seller['name'], "لو حد سألك جبت البدلة دي منين... قول من برا 😉"),
            (current_customer['name'], "ههههه ماشي يا معلم"),
            (self.seller['name'], "تحب اعملك مقاس تاني ولا كفاية عليك كده؟"),
            (current_customer['name'], "لا كفاية كده... هات البدلة بس"),
            (self.seller['name'], "طيب الف مبروك يا معلم... البدلة دي هتخليك تتجوز من تاني يوم 💑"),
            (current_customer['name'], "ربنا يستر... مع السلامة"),
            (self.seller['name'], "مع السلامة يا قمر... ولو حد سألك متنساش تقول من برا 😅"),
            ("system", "------------------ نهاية المحادثة ------------------")
        ]

        for name, message in conversation_sequence:
            if name == "system":
                self.display_message(message, align='center')
            else:
                self.display_message(f"{name}: {message}", align='left' if name == current_customer['name'] else 'right')
            time.sleep(2)

        stop_background_sound.set()
        self.conversation_running = False
        self.start_button.config(state=tk.NORMAL)

    def show_final_message(self):
        final_messages = [
            "------------------ انتهى يوم العمل ------------------",
            "هاني: الحمد لله... كان يوم حلو 😊",
            "هاني: بكرة نشوف زباين جديدة ان شاء الله 🙏",
            "--------------------------------------------------"
        ]
        
        for message in final_messages:
            self.display_message(message, align='center')
            time.sleep(1)
        
        self.start_button.config(state=tk.NORMAL)

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
        
    def play_background_sound(self, stop_event):
        while not stop_event.is_set():
            try:
                winsound.PlaySound(self.sound_paths['background'], winsound.SND_FILENAME)
            except Exception as e:
                print(f"خطأ في تشغيل الصوت الخلفي: {e}")
                break
            time.sleep(1)  

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