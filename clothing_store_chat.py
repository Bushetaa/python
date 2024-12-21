import tkinter as tk
from tkinter import scrolledtext, font
import random
import winsound
import time
import threading
from datetime import datetime

class ClothingStoreChat:
    def __init__(self, master):
        self.master = master
        master.title("محل Souts للملابس")
        master.geometry("1200x800")
        master.configure(bg='#2C3E50')

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
                "عندنا أحسن الخامات بأسعار مناسبة"
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
                    "فيه خصم ولا لسه؟",
                    "شكل البدلة حلو بس غالي أوي"
                ],
                "insult_messages": [
                    "المحل ده وحش أوي يا راجل",
                    "بتبيع زبالة والله",
                    "الأسعار بتاعتك مش معقولة خالص"
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
                    "عايز أجيب حاجة مش غالية أوي"
                ],
                "insult_messages": [
                    "غالي أوي يا سيدي بجد",
                    "مش هقدر أشتري كده أبدا والله",
                    "انت بتنصب والله يا راجل"
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
                    "عندك إيه في الموضة الجديدة؟"
                ],
                "insult_messages": [
                    "المحل ده مفيهوش ذوق خالص",
                    "بتبيع حاجة وحشة أوي",
                    "الموديلات دي من زمان خلصت"
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
                    "عايز حاجة سادة وجميلة"
                ],
                "insult_messages": [
                    "الأسعار دي مش معقولة خالص",
                    "مش هقدر أشتري حاجة غالية كده",
                    "انت بتبيع ولا بتسرق؟"
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
                    "عايزة حاجة مش غالية أوي"
                ],
                "insult_messages": [
                    "غالي أوي يا باشا",
                    "مش هقدر أشتري كده أبدا",
                    "الأسعار دي مش معقولة"
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
                    "عايز حاجة مش غالية"
                ],
                "insult_messages": [
                    "غالي أوي يا عم",
                    "مش هقدر أشتري كده",
                    "الأسعار دي مش معقولة خالص"
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
                    "عايز حاجة أنيقة وعملية"
                ],
                "insult_messages": [
                    "غالي أوي يا باشا",
                    "مش هقدر أشتري كده",
                    "الأسعار دي مش معقولة"
                ]
            }
        ]
        
        # Sound paths
        self.greeting_sound_path = r"D:\work\python\123.wav"
        self.expulsion_sound_path = r"D:\work\python\1303451583564087367.wav"
        self.whatsapp_sound_path = r"D:\work\python\WhatsApp Audio 2024-12-21 at 03.15.56_77d358ee.wav"
        
        # Conversation setup
        self.current_customer_index = 0
        self.conversation_running = False
        
        # Create UI components
        self.create_ui()
        
    def font_setup(self):
        # إعدادات الخط
        self.title_font = font.Font(family='Cairo', size=20, weight='bold')
        self.chat_font = font.Font(family='Cairo', size=14)
        
    def create_ui(self):
        # إطار رئيسي
        main_frame = tk.Frame(self.master, bg='#34495E')
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # زر بدء المحادثة في أعلى الصفحة
        self.start_button = tk.Button(
            main_frame, 
            text="ابدأ المحادثة", 
            command=self.start_conversation,
            font=('Cairo', 20, 'bold'),
            bg='#27AE60',  # لون أخضر غني
            fg='white',
            relief=tk.RAISED,
            borderwidth=5,
            padx=20,
            pady=10,
            width=30,  # زيادة عرض الزر
            height=2   # زيادة ارتفاع الزر
        )
        self.start_button.pack(fill=tk.X, padx=10, pady=10)

        # إضافة تأثير تحريك للزر
        self.start_button.bind('<Enter>', self.on_enter)
        self.start_button.bind('<Leave>', self.on_leave)

        # عنوان متحرك
        title_label = tk.Label(
            main_frame, 
            text="محادثات محل Souts للملابس", 
            font=('Cairo', 20, 'bold'),
            bg='#2980B9', 
            fg='white',
            relief=tk.RAISED,
            borderwidth=5,
            padx=20,
            pady=10
        )
        title_label.pack(fill=tk.X, pady=10)

        # إطار معلومات المحل
        store_info_frame = tk.Frame(main_frame, bg='#ECF0F1')
        store_info_frame.pack(fill=tk.X, padx=10, pady=5)

        # معلومات المحل
        store_details = tk.Label(
            store_info_frame, 
            text="محل Souts للملابس الرسمية | أحدث الموديلات | أفضل الخامات",
            font=('Cairo', 14),
            bg='#ECF0F1',
            fg='#2C3E50'
        )
        store_details.pack(side=tk.LEFT, padx=10)

        # ساعة المحل
        self.clock_label = tk.Label(
            store_info_frame, 
            font=('Cairo', 14),
            bg='#ECF0F1',
            fg='#2C3E50'
        )
        self.clock_label.pack(side=tk.RIGHT, padx=10)
        self.update_clock()

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            width=80, 
            height=25,
            font=('Cairo', 14),
            bg='#ECF0F1',
            fg='#2C3E50',
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

    def start_conversation(self):
        # تعطيل زر البدء
        self.start_button.config(state=tk.DISABLED)
        
        # مسح المحادثة السابقة
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        # بدء محادثة الزبون الحالي
        self.conversation_running = True
        threading.Thread(target=self.run_conversation, daemon=True).start()
        
    def run_conversation(self):
        # التأكد من وجود زبائن
        if self.current_customer_index >= len(self.customers):
            self.show_final_message()
            return
        
        # الزبون الحالي
        current_customer = self.customers[self.current_customer_index]
        
        # إنشاء حدث للتحكم في الصوت الخلفي
        stop_background_sound = threading.Event()
        
        # بدء تشغيل الصوت الخلفي
        background_sound_thread = threading.Thread(
            target=self.play_background_sound, 
            args=(stop_background_sound,), 
            daemon=True
        )
        background_sound_thread.start()
        
        # تشغيل صوت الترحيب
        self.play_sound(self.greeting_sound_path)
        
        # رسائل الترحيب مع تفاصيل إضافية
        welcome_messages = [
            f"{current_customer['name']} ({current_customer['role']}): السلام عليكم يا {self.seller['name']}", 
            f"{self.seller['name']}: وعليكم السلام، أهلا بيك يا {current_customer['name']} - {current_customer['role']}", 
            f"{self.seller['name']}: تحت أمرك، عايز إيه النهاردة؟"
        ]
        
        for message in welcome_messages:
            self.display_message(
                message, 
                align='left' if current_customer['name'] in message else 'right'
            )
            time.sleep(1)
        
        # محادثة لمدة دقيقة مع عدد رسائل أكبر
        start_time = time.time()
        message_count = 0
        max_messages = 30  # زيادة عدد الرسائل
        
        while time.time() - start_time < 150 and self.conversation_running and message_count < max_messages:
            # رسالة من الزبون
            customer_message = random.choice(current_customer['messages'])
            self.display_message(
                f"{current_customer['name']}: {customer_message}", 
                align='left'
            )
            time.sleep(random.uniform(1, 2))
            message_count += 1
            
            # رد من البائع
            seller_message = random.choice(self.seller['messages'])
            self.display_message(
                f"{self.seller['name']}: {seller_message}", 
                align='right'
            )
            time.sleep(random.uniform(1, 2))
            message_count += 1
            
            # احتمال الإهانة
            if random.random() < 0.2:
                self.handle_insult(current_customer)
                break
        
        # إيقاف الصوت الخلفي
        stop_background_sound.set()
        
        # نهاية المحادثة العادية
        self.end_customer_conversation(current_customer)

    def play_background_sound(self, stop_event):
        while not stop_event.is_set():
            try:
                winsound.PlaySound(self.whatsapp_sound_path, winsound.SND_FILENAME)
            except Exception as e:
                print(f"خطأ في تشغيل الصوت الخلفي: {e}")
                break
            time.sleep(1)  # Small delay to prevent excessive CPU usage

    def handle_insult(self, customer):
        # رسالة الإهانة
        insult = random.choice(customer['insult_messages'])
        
        # عرض رسالة الإهانة
        self.display_message(f"هاني: مش هقدر أتعامل معاك", align='right')
        
        # تشغيل صوت الطرد
        self.play_sound(self.expulsion_sound_path)
        
        # عرض رسالة الإهانة من العميل
        self.display_message(f"{customer['name']}: {insult}", align='left')
        
        # إنهاء المحادثة
        self.end_customer_conversation(customer)
        
    def end_customer_conversation(self, customer):
        # رسائل الختام
        farewell_messages = [
            f"{self.seller['name']}: شكراً لزيارتك يا {customer['name']}", 
            f"{customer['name']}: مع السلامة يا {self.seller['name']}", 
            f"{self.seller['name']}: أهلاً بالزبون التالي"
        ]
        
        # عرض رسائل الوداع
        for message in farewell_messages:
            self.display_message(
                message, 
                align='left' if customer['name'] in message else 'right'
            )
            time.sleep(1)
        
        # الانتقال للزبون التالي
        self.current_customer_index += 1
        self.conversation_running = False
        
        # إعادة تشغيل المحادثة للزبون التالي
        if self.current_customer_index < len(self.customers):
            # تأخير قصير قبل بدء المحادثة التالية
            time.sleep(2)
            threading.Thread(target=self.run_conversation, daemon=True).start()
        else:
            self.show_final_message()
    
    def show_final_message(self):
        # رسالة نهاية المحادثات
        self.display_message(
            f"{self.seller['name']}: شكراً لكل الزبائن، اليوم كان رائعاً", 
            align='right'
        )
        
        # تمكين زر البدء مرة أخرى
        self.start_button.config(state=tk.NORMAL)
        
        # إعادة ضبط مؤشر الزبون
        self.current_customer_index = 0
        
        # تشغيل صوت نهاية اليوم
        self.play_sound(self.greeting_sound_path)
        
    def display_message(self, message, align='left'):
        # عرض الرسائل بشكل تدريجي
        self.chat_display.config(state=tk.NORMAL)
        
        # تحديد محاذاة الرسالة
        alignment_tag = 'left' if align == 'left' else 'right'
        self.chat_display.tag_config('left', justify='left')
        self.chat_display.tag_config('right', justify='right')
        
        # إدراج الرسالة بالتدريج
        for char in message + "\n":
            self.chat_display.insert(tk.END, char, (alignment_tag,))
            self.chat_display.see(tk.END)
            self.chat_display.update()
            time.sleep(0.05)  # تأثير الكتابة التدريجية
        
        self.chat_display.config(state=tk.DISABLED)
        
    def play_sound(self, sound_path):
        # تشغيل الصوت
        try:
            winsound.PlaySound(sound_path, winsound.SND_FILENAME)
        except Exception as e:
            print(f"خطأ في تشغيل الصوت: {e}")

def main():
    root = tk.Tk()
    app = ClothingStoreChat(root)
    root.mainloop()

if __name__ == "__main__":
    main()