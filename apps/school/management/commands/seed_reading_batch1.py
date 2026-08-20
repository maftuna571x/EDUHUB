"""
Management command: seed_reading_batch1

Seeds the Reading Bank with original CEFR-leveled reading passages
and their comprehension questions.

Safe to run multiple times: uses get_or_create() keyed on
(title, level), so re-running never creates duplicates and never
touches existing Reading data.

Usage:
    python manage.py seed_reading_batch1
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.school.models import ReadingPassage, ReadingQuestion


# =============================================================
# DATA
# NOTE: This list is intentionally written so that future batches
# (Batch 2, Batch 3, ... IELTS, Free Reading) can simply append
# more dicts in the same shape, or be loaded from a separate
# seed_reading_batchN.py command reusing the same helper logic.
# =============================================================

DATA = [

    # =========================================================
    # A1 — LEVEL 1
    # =========================================================

    {
        "level": "A1",
        "topic": "Education",
        "title": "My School Day",
        "text": (
            "My name is Aziz. I am twelve years old. I go to school every day "
            "from Monday to Saturday. My school starts at eight o'clock in the "
            "morning, so I wake up at half past six.\n\n"
            "First, I wash my face and eat breakfast with my family. My mother "
            "makes tea and bread. Then I put my books in my bag and walk to "
            "school with my friend Dilnoza. Our school is not far from our house.\n\n"
            "At school, I have six lessons every day. My favourite subject is "
            "English because I like to learn new words. I also like Math, but it "
            "is difficult for me. Our teacher, Mrs. Karimova, is very kind. She "
            "always helps us when we do not understand something.\n\n"
            "At lunchtime, we have thirty minutes to eat and play. I usually eat "
            "with my classmates in the school canteen. After lunch, we have three "
            "more lessons. School finishes at two o'clock.\n\n"
            "After school, I go home and eat lunch again with my family. Then I "
            "do my homework. In the evening, I play football with my friends near "
            "our house. I go to bed at nine o'clock because I am usually very "
            "tired.\n\n"
            "I like my school day. It is busy, but I learn many new things every "
            "day, and I have good friends there."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Aziz does not like school.",
                "b": "Aziz describes a normal day at his school.",
                "c": "Aziz's teacher is strict.",
                "d": "Aziz lives far from his school.",
                "correct": "B",
                "explanation": "The passage describes Aziz's routine from waking up to going to bed on a school day.",
            },
            {
                "question": "What time does Aziz wake up?",
                "a": "Six o'clock",
                "b": "Half past six",
                "c": "Eight o'clock",
                "d": "Half past eight",
                "correct": "B",
                "explanation": "The text says school starts at eight, so he wakes up at half past six.",
            },
            {
                "question": "Why does Aziz like English?",
                "a": "Because it is easy",
                "b": "Because his teacher chose it",
                "c": "Because he likes learning new words",
                "d": "Because his friend likes it",
                "correct": "C",
                "explanation": "The text states his favourite subject is English because he likes to learn new words.",
            },
            {
                "question": "Which statement is NOT true about Aziz's day?",
                "a": "He walks to school with a friend.",
                "b": "He has six lessons a day.",
                "c": "He eats lunch at the canteen.",
                "d": "He goes to bed at eleven o'clock.",
                "correct": "D",
                "explanation": "The passage says he goes to bed at nine o'clock, not eleven.",
            },
            {
                "question": "What can we infer about Aziz's teacher, Mrs. Karimova?",
                "a": "She is unfriendly to students.",
                "b": "She is supportive and patient.",
                "c": "She does not teach Math.",
                "d": "She lives near Aziz.",
                "correct": "B",
                "explanation": "The text says she always helps students who do not understand, showing she is supportive.",
            },
        ],
    },

    {
        "level": "A1",
        "topic": "Food",
        "title": "A Family Breakfast",
        "text": (
            "Every Sunday morning, my family has a big breakfast together. It is "
            "my favourite meal of the week because everyone is at home and we can "
            "talk and laugh.\n\n"
            "My mother wakes up early to cook. She makes fried eggs, bread, and a "
            "big pot of tea. Sometimes she also makes pancakes with honey. My "
            "father cuts fresh tomatoes and cucumbers for a salad. He says a good "
            "salad makes the breakfast complete.\n\n"
            "My little sister helps too. She is only six years old, so she puts "
            "the plates and cups on the table. She likes to help, even when she "
            "makes small mistakes. My grandmother usually sits near the window and "
            "tells us stories about when she was young.\n\n"
            "We do not eat quickly on Sundays. We sit at the table for almost an "
            "hour. My father asks about our week, and we talk about our plans. I "
            "think this is the best part of the day because we are all together.\n\n"
            "After breakfast, my sister and I wash the dishes. Then we usually go "
            "for a short walk in the park near our house. I love Sunday mornings "
            "because they make our family stronger."
        ),
        "questions": [
            {
                "question": "What is the best title for this passage?",
                "a": "How to Cook Eggs",
                "b": "A Family's Sunday Breakfast",
                "c": "My Little Sister's Job",
                "d": "A Walk in the Park",
                "correct": "B",
                "explanation": "The passage is mainly about the family's weekly Sunday breakfast tradition.",
            },
            {
                "question": "Who cuts the tomatoes and cucumbers?",
                "a": "The mother",
                "b": "The father",
                "c": "The sister",
                "d": "The grandmother",
                "correct": "B",
                "explanation": "According to the passage, the father cuts fresh tomatoes and cucumbers for the salad.",
            },
            {
                "question": "According to the passage, what does the grandmother usually do?",
                "a": "She cooks the breakfast.",
                "b": "She tells stories about her youth.",
                "c": "She washes the dishes.",
                "d": "She walks in the park.",
                "correct": "B",
                "explanation": "The text says the grandmother tells stories about when she was young.",
            },
            {
                "question": "Why does the writer say Sunday breakfast is the best part of the day?",
                "a": "Because the food is expensive",
                "b": "Because they eat very quickly",
                "c": "Because the whole family is together",
                "d": "Because they watch television",
                "correct": "C",
                "explanation": "The writer explains this is the best part because they are all together and can talk.",
            },
            {
                "question": "What do the writer and their sister do after breakfast?",
                "a": "They cook pancakes.",
                "b": "They wash the dishes and go for a walk.",
                "c": "They go back to sleep.",
                "d": "They visit their grandmother.",
                "correct": "B",
                "explanation": "The passage states that after breakfast they wash the dishes and go for a short walk.",
            },
        ],
    },

    {
        "level": "A1",
        "topic": "Animals",
        "title": "My Neighbour's Dog",
        "text": (
            "My neighbour, Mr. Yusupov, has a small brown dog named Max. Max is "
            "two years old, and he is very friendly. Every morning, I see Mr. "
            "Yusupov walking Max near our street.\n\n"
            "Max likes to play with a ball. When children come near, he runs to "
            "them and wants to play. He is never angry, and he never bites. That "
            "is why all the children in our street love him.\n\n"
            "Mr. Yusupov feeds Max twice a day, in the morning and in the "
            "evening. Max eats special dog food, but he also loves small pieces "
            "of meat. After eating, Max usually sleeps under a tree in the "
            "garden.\n\n"
            "On weekends, Mr. Yusupov takes Max to a big park. There, Max can run "
            "freely and meet other dogs. He is very happy in the park because he "
            "can run fast and play for a long time.\n\n"
            "Sometimes, when Mr. Yusupov is at work, I help him and take Max for "
            "a short walk. I really enjoy this because Max is a very good friend, "
            "and walking him makes me happy too."
        ),
        "questions": [
            {
                "question": "What is Max?",
                "a": "A cat",
                "b": "A bird",
                "c": "A dog",
                "d": "A rabbit",
                "correct": "C",
                "explanation": "The passage clearly states Max is a small brown dog.",
            },
            {
                "question": "How old is Max?",
                "a": "One year old",
                "b": "Two years old",
                "c": "Three years old",
                "d": "Four years old",
                "correct": "B",
                "explanation": "The text states that Max is two years old.",
            },
            {
                "question": "Why do the children in the street love Max?",
                "a": "Because he is very big",
                "b": "Because he is friendly and never bites",
                "c": "Because he can sing",
                "d": "Because he lives in the park",
                "correct": "B",
                "explanation": "The passage explains that Max is never angry and never bites, so children love him.",
            },
            {
                "question": "What does the writer do when Mr. Yusupov is at work?",
                "a": "Feeds Max special food",
                "b": "Takes Max to the big park",
                "c": "Sometimes walks Max for a short time",
                "d": "Buys a new ball for Max",
                "correct": "C",
                "explanation": "The passage says the writer sometimes helps by taking Max for a short walk.",
            },
            {
                "question": "What can be concluded about Max's life?",
                "a": "He is not cared for well.",
                "b": "He is loved and well looked after.",
                "c": "He lives alone in the park.",
                "d": "He does not like other dogs.",
                "correct": "B",
                "explanation": "The details about feeding, walking, and playing show that Max is well cared for and loved.",
            },
        ],
    },

    {
        "level": "A1",
        "topic": "Travel",
        "title": "A Trip to the Village",
        "text": (
            "Last summer, my family and I went to visit my grandparents in a "
            "small village. It was a two-hour trip by car from our city. I was "
            "very excited because I had not seen the village for a long time.\n\n"
            "When we arrived, my grandmother was waiting for us at the gate. She "
            "hugged me and said I had grown taller. The village house is old but "
            "very comfortable, with a big garden full of fruit trees.\n\n"
            "In the morning, I helped my grandfather in the garden. We picked "
            "apples and apricots together. He taught me the names of different "
            "plants and told me stories about his own childhood in the village.\n\n"
            "In the afternoon, my cousins came to visit. We played outside near "
            "the river until it became dark. The air in the village was very "
            "fresh, and the sky at night had many bright stars, which we cannot "
            "see in the city.\n\n"
            "We stayed in the village for one week. On the last day, I did not "
            "want to leave. My grandmother gave us fruit and vegetables from her "
            "garden to take home. I promised to visit again next summer."
        ),
        "questions": [
            {
                "question": "How did the family travel to the village?",
                "a": "By train",
                "b": "By bus",
                "c": "By car",
                "d": "By plane",
                "correct": "C",
                "explanation": "The passage says it was a two-hour trip by car from the city.",
            },
            {
                "question": "What did the writer do with the grandfather?",
                "a": "Fixed the house",
                "b": "Picked fruit in the garden",
                "c": "Went fishing in the river",
                "d": "Bought food at a shop",
                "correct": "B",
                "explanation": "The text says they picked apples and apricots together in the garden.",
            },
            {
                "question": "According to the passage, why could they see many stars at night?",
                "a": "Because it was winter",
                "b": "Because the village air was fresh with little light",
                "c": "Because they used a telescope",
                "d": "Because it was raining",
                "correct": "B",
                "explanation": "The passage links the fresh village air and clear sky to seeing many bright stars.",
            },
            {
                "question": "How can we tell that the writer enjoyed the trip?",
                "a": "The writer wanted to leave early.",
                "b": "The writer did not want to leave on the last day.",
                "c": "The writer stayed inside all week.",
                "d": "The writer did not play with cousins.",
                "correct": "B",
                "explanation": "The passage states the writer did not want to leave, showing they enjoyed the trip.",
            },
            {
                "question": "What is the best title for this passage?",
                "a": "Life in the City",
                "b": "A Summer Visit to Grandparents",
                "c": "Learning to Drive",
                "d": "A Rainy Day",
                "correct": "B",
                "explanation": "The whole passage describes the family's summer visit to the grandparents' village.",
            },
        ],
    },

    # =========================================================
    # A2 — LEVEL 2
    # =========================================================

    {
        "level": "A2",
        "topic": "Technology",
        "title": "Learning with a Tablet",
        "text": (
            "Many schools today are giving students tablets instead of paper "
            "textbooks. This change is becoming more common, especially in "
            "cities, and it is changing the way young people study.\n\n"
            "A tablet can hold hundreds of books, videos, and exercises in one "
            "small device. Students do not need to carry heavy bags anymore. "
            "Instead, they carry one light tablet with everything they need for "
            "their lessons. Teachers can also send homework directly to the "
            "tablet, and students can send their answers back immediately.\n\n"
            "One of the biggest advantages is that tablets can show information "
            "in different ways. A student who finds reading difficult can watch a "
            "short video instead. A student who loves pictures can look at "
            "diagrams and colourful charts. This helps different students learn "
            "in the way that suits them best.\n\n"
            "However, using tablets in class also has some problems. Some "
            "students get distracted by games or messages instead of doing their "
            "work. Teachers must check that everyone is using the tablet "
            "correctly. Also, tablets can break easily, and not every family can "
            "afford to buy or repair one.\n\n"
            "Despite these problems, most teachers agree that tablets make "
            "lessons more interesting. Students who use tablets often say that "
            "learning feels more like a game than a boring task, and this can "
            "make them want to study more."
        ),
        "questions": [
            {
                "question": "What is the passage mainly about?",
                "a": "The history of tablets",
                "b": "The advantages and problems of using tablets in schools",
                "c": "How to repair a broken tablet",
                "d": "Why paper books are better",
                "correct": "B",
                "explanation": "The passage discusses both the benefits and the problems of using tablets in classrooms.",
            },
            {
                "question": "According to the passage, why do students not need heavy bags anymore?",
                "a": "Schools stopped giving homework.",
                "b": "One tablet can hold hundreds of books and materials.",
                "c": "Students study only at home.",
                "d": "Teachers collect all the books.",
                "correct": "B",
                "explanation": "The text explains a tablet can hold hundreds of books, videos, and exercises, removing the need for heavy bags.",
            },
            {
                "question": "What does the word 'distracted' mean in the passage?",
                "a": "Focused on studying",
                "b": "Unable to pay attention because of something else",
                "c": "Excited about learning",
                "d": "Tired after school",
                "correct": "B",
                "explanation": "The context about games and messages shows 'distracted' means losing focus on the task.",
            },
            {
                "question": "Which statement is NOT mentioned as a problem with tablets?",
                "a": "Students can get distracted by games.",
                "b": "Tablets can break easily.",
                "c": "Some families cannot afford them.",
                "d": "Tablets are heavier than paper books.",
                "correct": "D",
                "explanation": "The passage never says tablets are heavier; in fact, it says they are lighter than carrying many books.",
            },
            {
                "question": "What can be inferred about students who use tablets, according to the passage?",
                "a": "They usually dislike using tablets.",
                "b": "They may feel more motivated to study.",
                "c": "They never get distracted.",
                "d": "They no longer need teachers.",
                "correct": "B",
                "explanation": "The passage states learning feels like a game, which can make students want to study more.",
            },
        ],
    },

    {
        "level": "A2",
        "topic": "Health",
        "title": "Sleep and Energy",
        "text": (
            "Many teenagers today do not get enough sleep. Between homework, "
            "phones, and social activities, it is easy to stay awake late and "
            "wake up tired the next morning. However, doctors say that sleep is "
            "just as important as food and exercise for a healthy life.\n\n"
            "During sleep, the body repairs itself. Muscles grow, the brain "
            "organises information from the day, and the immune system becomes "
            "stronger. This is why people who do not sleep enough often get sick "
            "more easily and find it harder to remember new information.\n\n"
            "Experts recommend that teenagers sleep between eight and ten hours "
            "every night. Younger children usually need even more, while adults "
            "can often manage with seven to nine hours. Unfortunately, many young "
            "people sleep only five or six hours because they stay up using "
            "their phones or watching videos.\n\n"
            "Poor sleep does not only cause tiredness. It can also affect mood, "
            "making people more irritable and anxious. Students who do not sleep "
            "well often find it harder to concentrate in class and may get lower "
            "grades than students who sleep enough.\n\n"
            "There are simple ways to improve sleep. Going to bed at the same "
            "time every night, avoiding phones before bed, and keeping the room "
            "dark and quiet can all help. Small changes in habits can lead to "
            "better sleep and, therefore, better energy during the day."
        ),
        "questions": [
            {
                "question": "What is the main purpose of this passage?",
                "a": "To explain why phones are dangerous",
                "b": "To explain why sleep is important and how to improve it",
                "c": "To describe a scientific experiment",
                "d": "To compare children and adults",
                "correct": "B",
                "explanation": "The passage explains the importance of sleep and gives tips for improving it.",
            },
            {
                "question": "According to the passage, how many hours should teenagers sleep?",
                "a": "5–6 hours",
                "b": "6–7 hours",
                "c": "8–10 hours",
                "d": "10–12 hours",
                "correct": "C",
                "explanation": "The text states that experts recommend eight to ten hours for teenagers.",
            },
            {
                "question": "Why do people who sleep poorly often get sick more easily?",
                "a": "Because their immune system does not get stronger during sleep",
                "b": "Because they eat less food",
                "c": "Because they exercise too much",
                "d": "Because they drink less water",
                "correct": "A",
                "explanation": "The passage explains that during sleep the immune system becomes stronger; without enough sleep, this does not happen properly.",
            },
            {
                "question": "What does the passage suggest about students' grades?",
                "a": "Grades are not related to sleep.",
                "b": "Sleep only affects younger children's grades.",
                "c": "Poor sleep can lead to lower grades.",
                "d": "Good grades always mean good sleep.",
                "correct": "C",
                "explanation": "The passage states students who sleep poorly find it harder to concentrate and may get lower grades.",
            },
            {
                "question": "Which of these is suggested as a way to improve sleep?",
                "a": "Watching videos before bed",
                "b": "Going to bed at a different time each night",
                "c": "Keeping the room dark and quiet",
                "d": "Sleeping only on weekends",
                "correct": "C",
                "explanation": "The passage lists a dark, quiet room as one way to improve sleep quality.",
            },
        ],
    },

    {
        "level": "A2",
        "topic": "Culture",
        "title": "A Festival in My City",
        "text": (
            "Every spring, my city holds a big festival to celebrate the new "
            "season. The festival is called Navruz, and it is one of the most "
            "important celebrations in our culture. People from all over the "
            "city come together to enjoy music, food, and traditional games.\n\n"
            "Preparations begin many days before the festival. Families clean "
            "their homes and plant new flowers in their gardens. Women prepare a "
            "special dish called sumalak, which is made from wheat sprouts and "
            "takes many hours to cook. Everyone in the neighbourhood usually "
            "helps to stir the pot and share the food together.\n\n"
            "On the day of the festival, the main square in the city fills with "
            "people. There are colourful stages with singers and dancers, and "
            "children play traditional games such as rope pulling and running "
            "races. Craftsmen sell handmade items, from clothes to small "
            "wooden toys, and the smell of cooking food fills the air.\n\n"
            "For me, the best part of the festival is spending time with my "
            "extended family. My cousins, aunts, and uncles all come to our "
            "grandparents' house, and we eat together and tell jokes late into "
            "the evening. It reminds me how important family and community are "
            "in our culture.\n\n"
            "This festival is not just a holiday; it is a way for our community "
            "to welcome spring and remember old traditions that connect us to "
            "our history."
        ),
        "questions": [
            {
                "question": "What is Navruz, according to the passage?",
                "a": "A type of food",
                "b": "A spring festival celebrating the new season",
                "c": "A city in the country",
                "d": "A traditional game",
                "correct": "B",
                "explanation": "The text describes Navruz as a festival held every spring to celebrate the new season.",
            },
            {
                "question": "What is sumalak?",
                "a": "A traditional dance",
                "b": "A dish made from wheat sprouts",
                "c": "A type of clothing",
                "d": "A children's game",
                "correct": "B",
                "explanation": "The passage explains sumalak is a special dish made from wheat sprouts.",
            },
            {
                "question": "According to the passage, what do children do at the festival?",
                "a": "Cook sumalak",
                "b": "Sell handmade items",
                "c": "Play traditional games such as rope pulling",
                "d": "Clean the city square",
                "correct": "C",
                "explanation": "The text states children play traditional games such as rope pulling and running races.",
            },
            {
                "question": "What does the writer say is the best part of the festival?",
                "a": "The music on the stages",
                "b": "The traditional games",
                "c": "Spending time with extended family",
                "d": "Buying handmade toys",
                "correct": "C",
                "explanation": "The writer directly states that spending time with extended family is the best part.",
            },
            {
                "question": "What can be concluded about the purpose of Navruz for this community?",
                "a": "It is mainly a shopping event.",
                "b": "It connects people to tradition and community.",
                "c": "It is only important for children.",
                "d": "It has no connection to history.",
                "correct": "B",
                "explanation": "The final paragraph explains the festival welcomes spring and connects people to old traditions and history.",
            },
        ],
    },

    {
        "level": "A2",
        "topic": "Work",
        "title": "A Part-Time Job",
        "text": (
            "Last year, I started working part-time at a small bookshop near my "
            "university. I work there three afternoons a week, after my "
            "classes finish. At first, I only wanted to earn some extra money, "
            "but the job taught me much more than I expected.\n\n"
            "My main tasks are organising books on the shelves, helping "
            "customers find what they are looking for, and working at the cash "
            "register. In the beginning, I was nervous about talking to "
            "customers because I am usually a quiet person. However, after a few "
            "weeks, I became more confident and started to enjoy conversations "
            "with regular customers.\n\n"
            "The owner of the shop, Mrs. Rustamova, is patient and always "
            "explains things clearly when I make mistakes. She often tells me "
            "that customer service is about listening carefully and being "
            "polite, even when customers are in a hurry or difficult to please. "
            "I have learned a lot from watching how she talks to people.\n\n"
            "Working part-time also taught me to manage my time better. I have "
            "to balance my studies, my job, and my free time, so I now plan my "
            "week more carefully than before. Sometimes it is tiring, especially "
            "during exam periods, but it also feels good to earn my own money.\n\n"
            "I believe this job has helped me grow, not only financially but "
            "also as a more confident and organised person."
        ),
        "questions": [
            {
                "question": "Why did the writer start the part-time job?",
                "a": "To become a bookshop owner",
                "b": "To earn some extra money",
                "c": "Because the university required it",
                "d": "Because friends worked there",
                "correct": "B",
                "explanation": "The passage states the writer started mainly to earn some extra money.",
            },
            {
                "question": "According to the passage, how did the writer feel about talking to customers at first?",
                "a": "Confident",
                "b": "Bored",
                "c": "Nervous",
                "d": "Angry",
                "correct": "C",
                "explanation": "The text says the writer was nervous at first because they are usually a quiet person.",
            },
            {
                "question": "What does Mrs. Rustamova often say about customer service?",
                "a": "It is about selling as many books as possible.",
                "b": "It is about listening carefully and being polite.",
                "c": "It is about working quickly.",
                "d": "It is about knowing every book title.",
                "correct": "B",
                "explanation": "The passage states she tells the writer customer service is about listening carefully and being polite.",
            },
            {
                "question": "What skill did the writer improve by balancing study and work?",
                "a": "Reading speed",
                "b": "Time management",
                "c": "Cooking",
                "d": "Public speaking",
                "correct": "B",
                "explanation": "The passage explicitly says the job taught the writer to manage time better.",
            },
            {
                "question": "What can be inferred about the writer's personality by the end of the passage?",
                "a": "They became less confident over time.",
                "b": "They stayed exactly the same as before.",
                "c": "They grew more confident and organised.",
                "d": "They decided to quit the job.",
                "correct": "C",
                "explanation": "The final paragraph states the job helped the writer become more confident and organised.",
            },
        ],
    },

    # =========================================================
    # B1 — LEVEL 3
    # =========================================================

    {
        "level": "B1",
        "topic": "Environment",
        "title": "Plastic and Our Daily Choices",
        "text": (
            "Plastic has become one of the most useful materials of the modern "
            "world. It is light, cheap to produce, and can be shaped into almost "
            "anything, from bottles and bags to toys and furniture. However, "
            "this same convenience has created one of the biggest environmental "
            "challenges of our time.\n\n"
            "Unlike organic materials, most plastic does not break down "
            "naturally. Instead, it slowly breaks into smaller and smaller "
            "pieces, known as microplastics, which can remain in the "
            "environment for hundreds of years. These tiny particles have been "
            "found not only in rivers and oceans, but also in soil, in the air, "
            "and even inside the bodies of animals and humans.\n\n"
            "One of the main reasons plastic pollution has grown so quickly is "
            "the rise of single-use products. Bags, straws, and packaging are "
            "often used for only a few minutes before being thrown away, yet "
            "they can pollute the environment for centuries. Many countries have "
            "started to respond to this problem by banning certain single-use "
            "plastics or introducing extra charges for plastic bags in shops.\n\n"
            "While government policies are important, individual choices also "
            "make a difference. Carrying a reusable water bottle, using cloth "
            "bags for shopping, and avoiding unnecessary packaging are simple "
            "actions that, when repeated by millions of people, can significantly "
            "reduce the amount of plastic waste produced each year.\n\n"
            "Some critics argue that focusing only on individual behaviour "
            "distracts from the responsibility of large companies, which produce "
            "the vast majority of plastic packaging. A balanced approach, they "
            "suggest, requires both personal responsibility and stronger "
            "regulation of industries that rely heavily on plastic production.\n\n"
            "Ultimately, solving the plastic problem is unlikely to come from a "
            "single solution. It will probably require a combination of new "
            "technology, updated laws, and a genuine change in how people think "
            "about the products they use every day."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Plastic should be banned completely worldwide.",
                "b": "Plastic pollution is a serious problem requiring both individual and collective action.",
                "c": "Only large companies are responsible for plastic pollution.",
                "d": "Plastic is no longer used in modern products.",
                "correct": "B",
                "explanation": "The passage discusses plastic pollution as a serious issue and suggests it needs a combination of solutions, including individual and government action.",
            },
            {
                "question": "According to the passage, why are microplastics particularly concerning?",
                "a": "They are very expensive to produce.",
                "b": "They break down quickly and disappear.",
                "c": "They can remain in the environment for a very long time.",
                "d": "They are only found in the ocean.",
                "correct": "C",
                "explanation": "The passage states microplastics can remain in the environment for hundreds of years.",
            },
            {
                "question": "What does the word 'convenience' refer to in the first paragraph?",
                "a": "The environmental damage caused by plastic",
                "b": "The usefulness and ease of using plastic",
                "c": "The high cost of plastic production",
                "d": "The natural breakdown of plastic",
                "correct": "B",
                "explanation": "In context, 'convenience' refers to how easy, light, and cheap plastic is to use.",
            },
            {
                "question": "According to critics mentioned in the passage, what is a limitation of focusing only on individual behaviour?",
                "a": "It ignores the responsibility of large companies.",
                "b": "It is too expensive for most people.",
                "c": "It does not reduce plastic waste at all.",
                "d": "It is illegal in most countries.",
                "correct": "A",
                "explanation": "The passage states critics argue this focus distracts from the responsibility of large companies producing most plastic packaging.",
            },
            {
                "question": "What can be concluded from the final paragraph?",
                "a": "A single new law will solve the plastic problem.",
                "b": "The problem will likely require several combined solutions.",
                "c": "Individual actions are unnecessary.",
                "d": "Technology alone cannot help at all.",
                "correct": "B",
                "explanation": "The passage concludes that solving the problem will probably require a combination of technology, laws, and changed habits.",
            },
        ],
    },

    {
        "level": "B1",
        "topic": "Psychology",
        "title": "Why We Procrastinate",
        "text": (
            "Almost everyone has experienced procrastination — the act of "
            "delaying a task that needs to be done, often replacing it with "
            "something easier or more enjoyable. Although it might seem like a "
            "simple problem of laziness, psychologists say the real causes are "
            "usually more complicated.\n\n"
            "Research suggests that procrastination is often linked to how we "
            "manage emotions rather than how we manage time. When a task feels "
            "boring, stressful, or difficult, our brains naturally look for ways "
            "to avoid the uncomfortable feeling. Scrolling through social media "
            "or cleaning the house, for example, can feel more rewarding in the "
            "short term than starting a difficult assignment.\n\n"
            "Another common cause is perfectionism. People who are afraid of "
            "making mistakes sometimes delay starting a task because they worry "
            "the result will not be good enough. Ironically, this fear often "
            "leads to lower-quality work, since the task is rushed at the last "
            "minute, creating exactly the outcome the person was trying to "
            "avoid.\n\n"
            "Procrastination can also be influenced by how a task is presented. "
            "Large, vague goals such as 'write the report' can feel "
            "overwhelming, making it easier to put off. Breaking the same task "
            "into smaller, specific steps, such as 'write the introduction "
            "paragraph', often makes it feel more manageable and less "
            "intimidating.\n\n"
            "Interestingly, studies show that forgiving yourself for procrastinating "
            "in the past can actually reduce the chance of procrastinating again. "
            "Students who felt guilty about delaying an assignment were more "
            "likely to delay the next one, while those who accepted their mistake "
            "without harsh self-criticism were more likely to start earlier next "
            "time.\n\n"
            "Understanding procrastination as an emotional response, rather than "
            "simply a lack of discipline, may be the first step toward managing "
            "it more effectively."
        ),
        "questions": [
            {
                "question": "According to the passage, what do psychologists believe is the real cause of procrastination?",
                "a": "A lack of intelligence",
                "b": "Difficulty managing emotions rather than time",
                "c": "Too much free time",
                "d": "Poor physical health",
                "correct": "B",
                "explanation": "The passage states procrastination is often linked to how we manage emotions rather than how we manage time.",
            },
            {
                "question": "Why does perfectionism sometimes lead to procrastination?",
                "a": "Perfectionists enjoy delaying tasks.",
                "b": "Perfectionists fear their work will not be good enough.",
                "c": "Perfectionists work faster than others.",
                "d": "Perfectionists do not care about quality.",
                "correct": "B",
                "explanation": "The passage explains that fear of imperfect results can cause people to delay starting a task.",
            },
            {
                "question": "What does the word 'overwhelming' most likely mean in the fourth paragraph?",
                "a": "Very simple and easy",
                "b": "Making someone feel it is too much to manage",
                "c": "Highly enjoyable",
                "d": "Completely unimportant",
                "correct": "B",
                "explanation": "In context, a large, vague goal feels 'overwhelming' because it seems too difficult to handle, prompting avoidance.",
            },
            {
                "question": "According to the passage, what effect does self-forgiveness have on procrastination?",
                "a": "It has no measurable effect.",
                "b": "It increases the chance of procrastinating again.",
                "c": "It can reduce the chance of procrastinating again.",
                "d": "It only works for perfectionists.",
                "correct": "C",
                "explanation": "The passage cites research showing students who forgave themselves were less likely to procrastinate on the next task.",
            },
            {
                "question": "What is the purpose of this passage?",
                "a": "To criticise students who procrastinate",
                "b": "To explain the psychological reasons behind procrastination",
                "c": "To advertise a time-management app",
                "d": "To describe the history of psychology",
                "correct": "B",
                "explanation": "The passage's overall purpose is to explain the emotional and psychological causes of procrastination.",
            },
        ],
    },

    {
        "level": "B1",
        "topic": "Communication",
        "title": "The Silent Language of the Body",
        "text": (
            "When people think about communication, they usually think about "
            "words. However, researchers estimate that a large part of what we "
            "communicate to others comes not from what we say, but from how we "
            "say it — our facial expressions, gestures, posture, and tone of "
            "voice. This is often called body language.\n\n"
            "Body language can reveal feelings that words try to hide. For "
            "example, a person might say they are calm while their crossed arms "
            "and tense shoulders suggest otherwise. Skilled observers, such as "
            "negotiators or interviewers, often pay close attention to these "
            "small signals because they can reveal more honest information than "
            "spoken words alone.\n\n"
            "Interestingly, body language is not always the same across "
            "cultures. A gesture that means something friendly in one country "
            "might be considered rude in another. Eye contact is a good example: "
            "in some cultures, direct eye contact shows confidence and honesty, "
            "while in others, it can be seen as disrespectful, especially toward "
            "older people or those in positions of authority.\n\n"
            "Understanding these differences is particularly important in "
            "international business and travel. A traveller who is unaware of "
            "local body language customs might unintentionally offend someone, "
            "even while trying to be polite. Because of this, many companies now "
            "train employees who work internationally to recognise and respect "
            "different non-verbal customs.\n\n"
            "Body language also plays a major role in everyday relationships. "
            "Simple actions, such as smiling, nodding while listening, or "
            "leaning slightly toward someone during a conversation, can make "
            "people feel more understood and valued, even without a single word "
            "being spoken.\n\n"
            "Learning to read and use body language effectively, therefore, is "
            "not just an interesting skill — it can genuinely improve how well "
            "we connect with the people around us."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Spoken words are more important than body language.",
                "b": "Body language plays an important, often hidden role in communication.",
                "c": "Eye contact means the same thing in every culture.",
                "d": "Only professionals need to understand body language.",
                "correct": "B",
                "explanation": "The whole passage focuses on how body language significantly shapes communication, often more than words.",
            },
            {
                "question": "According to the passage, why do skilled negotiators pay attention to body language?",
                "a": "Because words are always false",
                "b": "Because it can reveal more honest information than speech",
                "c": "Because it is required by law",
                "d": "Because they cannot understand spoken language",
                "correct": "B",
                "explanation": "The passage says body language can reveal more honest information than spoken words alone.",
            },
            {
                "question": "What example does the passage give of cultural differences in body language?",
                "a": "Smiling",
                "b": "Nodding",
                "c": "Eye contact",
                "d": "Leaning forward",
                "correct": "C",
                "explanation": "The passage specifically discusses eye contact as varying in meaning between cultures.",
            },
            {
                "question": "Why might a traveller unintentionally offend someone abroad?",
                "a": "Because they refuse to communicate at all",
                "b": "Because they are unaware of local body language customs",
                "c": "Because they always speak too loudly",
                "d": "Because they avoid smiling",
                "correct": "B",
                "explanation": "The passage explains that unfamiliarity with local non-verbal customs can lead to unintentional offence.",
            },
            {
                "question": "What can be inferred from the last paragraph?",
                "a": "Body language has no real effect on relationships.",
                "b": "Improving body language awareness can strengthen personal connections.",
                "c": "Only romantic relationships are affected by body language.",
                "d": "Body language is less important than in the past.",
                "correct": "B",
                "explanation": "The passage concludes that learning to read and use body language can genuinely improve connections with others.",
            },
        ],
    },

    {
        "level": "B1",
        "topic": "Nature",
        "title": "Forests and the Water Cycle",
        "text": (
            "Forests are often praised for producing oxygen and providing homes "
            "for wildlife, but one of their most important roles is frequently "
            "overlooked: their influence on rainfall and the wider water cycle. "
            "Scientists studying large forest regions have found that trees do "
            "far more than simply grow near water — they actively help create "
            "it.\n\n"
            "Trees release water vapour into the atmosphere through a process "
            "called transpiration. In large forests, particularly tropical ones, "
            "this process releases enormous amounts of moisture into the air. "
            "This moisture eventually forms clouds, which can travel long "
            "distances before falling as rain, sometimes hundreds of kilometres "
            "away from the forest that produced them.\n\n"
            "This means that forests do not only benefit the local area where "
            "they grow. Regions far from a forest can depend on it indirectly "
            "for their rainfall. Researchers studying the Amazon rainforest, for "
            "example, have found evidence that deforestation in one part of the "
            "region can reduce rainfall in agricultural areas located far away, "
            "affecting farmers who may never have seen the forest themselves.\n\n"
            "When large areas of forest are cut down, this natural water cycle is "
            "disrupted. Less transpiration means less moisture in the "
            "atmosphere, which can lead to reduced rainfall, drier soil, and, in "
            "severe cases, an increased risk of drought. Some scientists warn "
            "that continued deforestation could eventually change rainfall "
            "patterns across entire continents.\n\n"
            "For this reason, many environmental organisations argue that "
            "protecting forests should not be seen only as an act of "
            "conservation for wildlife, but as essential infrastructure for "
            "agriculture and water supply, benefiting people who may live far "
            "beyond the forest's borders."
        ),
        "questions": [
            {
                "question": "What is the main purpose of this passage?",
                "a": "To describe how animals live in forests",
                "b": "To explain how forests influence rainfall far beyond their location",
                "c": "To argue that forests should be used for farming",
                "d": "To compare tropical and temperate forests",
                "correct": "B",
                "explanation": "The passage focuses on explaining how forests, through transpiration, affect rainfall in distant regions.",
            },
            {
                "question": "What is transpiration, according to the passage?",
                "a": "The process of trees absorbing sunlight",
                "b": "The release of water vapour from trees into the atmosphere",
                "c": "The cutting down of trees for farming",
                "d": "The growth of new trees in a forest",
                "correct": "B",
                "explanation": "The passage defines transpiration as the process by which trees release water vapour into the atmosphere.",
            },
            {
                "question": "According to the passage, how can deforestation in one area affect farmers elsewhere?",
                "a": "By directly destroying their farmland",
                "b": "By reducing rainfall in distant agricultural regions",
                "c": "By increasing local wildlife",
                "d": "By making local soil more fertile",
                "correct": "B",
                "explanation": "The passage explains that deforestation can reduce rainfall in agricultural areas located far away.",
            },
            {
                "question": "What does the word 'disrupted' mean in the fourth paragraph?",
                "a": "Improved and strengthened",
                "b": "Interrupted or broken",
                "c": "Ignored completely",
                "d": "Repeated frequently",
                "correct": "B",
                "explanation": "In context, when forests are cut down, the natural water cycle is broken or interrupted.",
            },
            {
                "question": "Why do environmental organisations argue forests should be seen as 'infrastructure'?",
                "a": "Because forests are built by humans",
                "b": "Because forests support agriculture and water supply for distant people",
                "c": "Because forests are located near cities",
                "d": "Because forests produce building materials",
                "correct": "B",
                "explanation": "The passage explains organisations view forests as essential to agriculture and water supply, similar to infrastructure, benefiting distant people.",
            },
        ],
    },

    # =========================================================
    # B2 — LEVEL 4
    # =========================================================

    {
        "level": "B2",
        "topic": "Innovation",
        "title": "The Unexpected Rise of Remote Work",
        "text": (
            "For decades, the traditional office was considered the natural "
            "centre of professional life. Employees commuted daily, worked "
            "under direct supervision, and built careers within physical spaces "
            "designed specifically for collaboration. Remote work existed, but it "
            "was largely viewed as a niche arrangement suited to freelancers or "
            "a small number of progressive companies. That assumption was "
            "challenged dramatically when circumstances forced millions of "
            "employees worldwide to work from home almost overnight.\n\n"
            "What followed surprised many economists and business leaders. "
            "Rather than collapsing under the pressure of decentralisation, "
            "productivity in many industries remained stable, and in some cases "
            "even improved. Employees reported saving hours previously lost to "
            "commuting, while companies discovered that many roles did not "
            "require constant physical presence to function effectively. This "
            "unexpected outcome forced a re-evaluation of assumptions that had "
            "gone largely unquestioned for generations.\n\n"
            "However, the shift has not been without complications. Critics "
            "argue that remote work can blur the boundary between professional "
            "and personal life, making it difficult for employees to fully "
            "disconnect at the end of the day. Others point to the erosion of "
            "spontaneous collaboration — the informal conversations and shared "
            "problem-solving that often occur naturally in a physical office but "
            "are harder to replicate through scheduled video calls.\n\n"
            "There are also concerns about equity. Employees with quiet homes "
            "and reliable internet access tend to thrive under remote "
            "arrangements, while those in cramped living conditions or with "
            "unstable connections may struggle considerably more, potentially "
            "widening existing inequalities rather than reducing them.\n\n"
            "In response, many organisations have adopted hybrid models, "
            "combining days in the office with days working remotely, in an "
            "attempt to preserve the benefits of both approaches. Whether this "
            "compromise represents a lasting solution or merely a transitional "
            "phase remains a matter of considerable debate among researchers who "
            "study the future of work.\n\n"
            "What seems clear, regardless of the eventual outcome, is that the "
            "assumption of the office as an unquestionable default has been "
            "permanently disrupted."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Remote work has completely replaced office work.",
                "b": "The sudden rise of remote work challenged long-held assumptions and revealed both benefits and complications.",
                "c": "Companies have universally rejected remote work.",
                "d": "Remote work only benefits freelancers.",
                "correct": "B",
                "explanation": "The passage traces how remote work disrupted assumptions about offices, discussing both benefits and drawbacks.",
            },
            {
                "question": "According to the passage, what surprised economists about the shift to remote work?",
                "a": "Productivity collapsed immediately.",
                "b": "Productivity remained stable or improved in many cases.",
                "c": "Companies closed permanently.",
                "d": "Employees refused to work from home.",
                "correct": "B",
                "explanation": "The passage states productivity remained stable and sometimes improved, surprising economists and business leaders.",
            },
            {
                "question": "What does the phrase 'erosion of spontaneous collaboration' most likely mean?",
                "a": "An increase in scheduled meetings",
                "b": "A gradual loss of natural, informal teamwork",
                "c": "A rise in employee creativity",
                "d": "A reduction in commuting time",
                "correct": "B",
                "explanation": "In context, 'erosion' suggests a gradual decline of the natural, unplanned collaboration that occurs in physical offices.",
            },
            {
                "question": "What concern regarding equity is raised in the passage?",
                "a": "Remote work is equally beneficial for everyone.",
                "b": "Living conditions and internet access can create unequal outcomes among remote workers.",
                "c": "Only office workers face inequality.",
                "d": "Equity concerns apply only to freelancers.",
                "correct": "B",
                "explanation": "The passage explains that differences in home environments and internet access can widen inequalities among remote workers.",
            },
            {
                "question": "What can be inferred about hybrid work models from the passage?",
                "a": "They are universally agreed to be the permanent solution.",
                "b": "They are an attempt to balance benefits of both office and remote work, though their long-term future is uncertain.",
                "c": "They have been rejected by most companies.",
                "d": "They eliminate all problems associated with remote work.",
                "correct": "B",
                "explanation": "The passage states hybrid models attempt to combine benefits of both approaches, but whether this is lasting remains debated.",
            },
        ],
    },

    {
        "level": "B2",
        "topic": "Space",
        "title": "Searching for Water Beneath the Martian Surface",
        "text": (
            "For much of the twentieth century, Mars was imagined as a "
            "completely dry, lifeless world — a red desert with little "
            "resemblance to Earth beyond its rocky terrain. In recent decades, "
            "however, growing evidence has complicated this picture "
            "considerably, revealing a planet with a far more dynamic and "
            "watery past than scientists once believed.\n\n"
            "Orbiting spacecraft equipped with radar instruments have detected "
            "signs of ice hidden beneath the Martian surface, particularly near "
            "the poles. Some of this ice appears to exist in large, relatively "
            "pure deposits, suggesting that under the right conditions, future "
            "missions might be able to extract water for drinking, growing "
            "plants, or even producing rocket fuel through chemical processes.\n\n"
            "More intriguing still are findings that suggest the possible "
            "presence of liquid water, not simply frozen ice, in certain "
            "locations. Radar data collected beneath the southern polar ice cap "
            "hinted at what some scientists interpreted as underground lakes of "
            "salty liquid water, kept unfrozen by a combination of pressure and "
            "dissolved minerals that lower the freezing point. This "
            "interpretation, however, remains contested; other researchers argue "
            "that the radar signals could instead be explained by unusual "
            "mineral deposits rather than liquid water at all.\n\n"
            "The implications of confirming liquid water are significant, "
            "extending well beyond questions of resources for future astronauts. "
            "On Earth, liquid water is considered essential for life as we "
            "understand it. If similar conditions exist on Mars, even in small, "
            "isolated pockets, it raises the tantalising possibility that "
            "microbial life could theoretically survive there today, not merely "
            "in the planet's distant past.\n\n"
            "Confirming or disproving these theories will likely require more "
            "advanced instruments than those currently available, along with "
            "missions specifically designed to drill beneath the surface and "
            "directly sample what lies below. Until then, the question of "
            "whether Mars still holds liquid water — and possibly life — remains "
            "one of the most compelling mysteries in planetary science."
        ),
        "questions": [
            {
                "question": "What is the main purpose of the passage?",
                "a": "To prove that life exists on Mars",
                "b": "To explore the evolving scientific understanding of water on Mars",
                "c": "To describe the history of Mars exploration missions",
                "d": "To compare Mars and Earth's atmospheres",
                "correct": "B",
                "explanation": "The passage traces how scientific understanding of Martian water has changed and remains debated.",
            },
            {
                "question": "According to the passage, what has radar detected beneath the Martian surface?",
                "a": "Volcanic activity",
                "b": "Signs of ice, particularly near the poles",
                "c": "Confirmed alien life",
                "d": "Large oceans on the surface",
                "correct": "B",
                "explanation": "The passage states orbiting spacecraft with radar have detected signs of ice beneath the surface, especially near the poles.",
            },
            {
                "question": "Why do some scientists dispute the interpretation of underground liquid water?",
                "a": "They believe the radar signals could be explained by mineral deposits instead.",
                "b": "They believe Mars has no ice at all.",
                "c": "They think the radar instruments are broken.",
                "d": "They believe water cannot exist below freezing temperatures.",
                "correct": "A",
                "explanation": "The passage states other researchers argue the radar signals could be explained by unusual mineral deposits rather than liquid water.",
            },
            {
                "question": "What does the phrase 'tantalising possibility' suggest about the idea of microbial life on Mars?",
                "a": "It is proven and certain.",
                "b": "It is intriguing but not confirmed.",
                "c": "It has been completely disproven.",
                "d": "It is considered impossible.",
                "correct": "B",
                "explanation": "'Tantalising' implies something exciting yet uncertain, matching the passage's cautious tone about unconfirmed life.",
            },
            {
                "question": "What can be inferred about future Mars exploration from the final paragraph?",
                "a": "Current instruments are sufficient to answer all questions.",
                "b": "More advanced missions will likely be needed to resolve the uncertainty.",
                "c": "Scientists have abandoned the search for water.",
                "d": "The question of Martian water has already been settled.",
                "correct": "B",
                "explanation": "The passage states confirming or disproving the theories will likely require more advanced instruments and dedicated missions.",
            },
        ],
    },

    {
        "level": "B2",
        "topic": "Society",
        "title": "The Challenge of Ageing Populations",
        "text": (
            "Across much of the developed world, a quiet but significant "
            "demographic shift is underway. Improvements in healthcare and "
            "declining birth rates mean that populations in many countries are "
            "growing older, with a shrinking proportion of working-age people "
            "supporting an expanding number of retirees. This trend, while "
            "gradual, carries implications that touch nearly every part of "
            "society, from pension systems to labour markets.\n\n"
            "One of the most immediate concerns is the sustainability of public "
            "pension systems. Many of these systems were designed decades ago, "
            "when a relatively large working population supported a smaller "
            "number of retirees. As this ratio shifts, governments face "
            "difficult choices: raise taxes, increase the retirement age, reduce "
            "benefits, or some combination of these unpopular options. None of "
            "these solutions is politically straightforward, particularly when "
            "older voters, who tend to participate in elections at higher rates, "
            "may resist changes that affect their benefits directly.\n\n"
            "Labour markets, too, face significant adjustment. Some economists "
            "argue that an ageing workforce could slow innovation, as fewer "
            "young workers enter industries that rely heavily on new ideas and "
            "adaptability. Others push back against this view, pointing out that "
            "older workers often bring valuable experience and institutional "
            "knowledge that younger employees lack, and that automation may "
            "offset labour shortages in ways previous generations could not have "
            "anticipated.\n\n"
            "Healthcare systems face parallel pressures. Older populations "
            "typically require more medical care, placing additional strain on "
            "hospitals, insurance systems, and the workers who provide that "
            "care. Countries with already limited healthcare resources may find "
            "this pressure particularly difficult to manage without substantial "
            "structural reform.\n\n"
            "Some nations have attempted to address these challenges through "
            "immigration policies designed to attract younger workers, though "
            "this approach carries its own political complications. Others have "
            "focused on encouraging higher birth rates through financial "
            "incentives for families, with mixed and often limited results.\n\n"
            "Ultimately, there is no single solution that fully resolves the "
            "tensions created by an ageing population. What is increasingly "
            "clear, however, is that policies designed for the demographic "
            "realities of the past are unlikely to remain sustainable in the "
            "decades ahead."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Ageing populations create complex, interconnected challenges for pensions, labour, and healthcare.",
                "b": "Ageing populations are only a problem for pension systems.",
                "c": "Immigration is the only solution to ageing populations.",
                "d": "Younger populations always outperform older ones economically.",
                "correct": "A",
                "explanation": "The passage examines multiple interconnected effects of ageing populations across pensions, labour markets, and healthcare.",
            },
            {
                "question": "According to the passage, why are pension reforms politically difficult?",
                "a": "Older voters, who vote at high rates, may resist changes to their benefits.",
                "b": "Younger voters control most elections.",
                "c": "Pension systems are illegal to change.",
                "d": "Governments do not have the authority to make changes.",
                "correct": "A",
                "explanation": "The passage states older voters participate at higher rates and may resist changes affecting their benefits.",
            },
            {
                "question": "What is one counterargument presented against the idea that ageing workforces slow innovation?",
                "a": "Older workers bring valuable experience and knowledge.",
                "b": "Younger workers are always less skilled.",
                "c": "Innovation is not important for economies.",
                "d": "Automation always reduces the need for older workers.",
                "correct": "A",
                "explanation": "The passage presents the counterargument that older workers offer experience and institutional knowledge.",
            },
            {
                "question": "What does the word 'offset' mean in the third paragraph?",
                "a": "To completely eliminate",
                "b": "To balance out or compensate for something",
                "c": "To create a new problem",
                "d": "To ignore entirely",
                "correct": "B",
                "explanation": "In context, automation may 'offset' labour shortages, meaning it may help balance or compensate for the shortage.",
            },
            {
                "question": "What is the writer's overall attitude toward finding a solution to ageing populations?",
                "a": "Confident that one clear solution exists",
                "b": "Dismissive of the issue as unimportant",
                "c": "Cautious, suggesting there is no single easy solution",
                "d": "Certain that immigration will solve the problem entirely",
                "correct": "C",
                "explanation": "The final paragraph explicitly states there is no single solution that fully resolves the tensions created by ageing populations.",
            },
        ],
    },

    {
        "level": "B2",
        "topic": "Media",
        "title": "Social Media and the Battle for Attention",
        "text": (
            "Modern social media platforms are often described, somewhat "
            "casually, as simple tools for connecting with friends and sharing "
            "updates. In reality, the technology behind these platforms "
            "represents one of the most sophisticated attention-capturing "
            "systems ever created, engineered specifically to keep users "
            "engaged for as long as possible.\n\n"
            "At the core of this design is a business model built primarily "
            "around advertising revenue. Because platforms earn money largely "
            "through advertisements shown to users, the more time a person "
            "spends scrolling, the more advertising revenue the platform "
            "potentially generates. This financial incentive has shaped nearly "
            "every design decision, from the endless scroll that removes any "
            "natural stopping point, to notification systems calibrated to "
            "trigger curiosity at precisely the right moments.\n\n"
            "Former employees of major technology companies have described how "
            "psychological principles, some borrowed from casino gambling "
            "research, were deliberately incorporated into app design. "
            "Unpredictable rewards, such as not knowing exactly when a new like "
            "or comment will appear, exploit the same neurological mechanisms "
            "that make slot machines so compelling, encouraging users to check "
            "their phones repeatedly throughout the day.\n\n"
            "Critics argue that this design has measurable consequences beyond "
            "simple time-wasting. Some research has linked heavy social media "
            "use to increased anxiety, particularly among adolescents who "
            "compare their own lives unfavourably to the carefully curated "
            "images others post online. However, other researchers caution "
            "against oversimplifying this relationship, noting that correlation "
            "does not necessarily prove causation, and that social media use "
            "affects different individuals in markedly different ways.\n\n"
            "In response to growing criticism, some platforms have introduced "
            "features intended to promote healthier use, such as screen-time "
            "trackers and reminders to take breaks. Sceptics, however, question "
            "whether these features represent genuine reform or simply a public "
            "relations strategy that leaves the fundamentally attention-driven "
            "business model largely unchanged.\n\n"
            "Whatever the ultimate resolution, the debate highlights a deeper "
            "tension between technology companies' financial interests and the "
            "psychological wellbeing of the users whose attention sustains "
            "them."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Social media platforms are simple communication tools with no deeper design purpose.",
                "b": "Social media platforms are deliberately designed to maximise user attention, raising concerns about wellbeing.",
                "c": "Advertising has no connection to how social media apps are designed.",
                "d": "All researchers agree social media causes anxiety.",
                "correct": "B",
                "explanation": "The passage explains how attention-capturing design connects to advertising revenue and its psychological effects.",
            },
            {
                "question": "According to the passage, why do platforms benefit financially from longer user engagement?",
                "a": "Users pay a subscription fee per minute.",
                "b": "Platforms earn more advertising revenue the longer users stay engaged.",
                "c": "Longer engagement reduces server costs.",
                "d": "Governments pay platforms for user data.",
                "correct": "B",
                "explanation": "The passage states the business model is built around advertising revenue linked to time spent on the platform.",
            },
            {
                "question": "What comparison does the passage make regarding notification systems?",
                "a": "They are compared to traditional television advertising.",
                "b": "They are compared to psychological principles used in casino gambling.",
                "c": "They are compared to educational tools.",
                "d": "They are compared to newspaper subscriptions.",
                "correct": "B",
                "explanation": "The passage explicitly mentions psychological principles borrowed from casino gambling research being used in notification design.",
            },
            {
                "question": "What caution do some researchers raise about the link between social media and anxiety?",
                "a": "They deny any link exists at all.",
                "b": "They warn that correlation does not necessarily prove causation.",
                "c": "They claim anxiety only affects adults.",
                "d": "They argue social media has no psychological effects.",
                "correct": "B",
                "explanation": "The passage states researchers caution against oversimplifying, noting correlation does not necessarily prove causation.",
            },
            {
                "question": "What is the writer's attitude toward platform features like screen-time trackers?",
                "a": "Fully convinced they solve the problem",
                "b": "Presented with scepticism about whether they represent genuine reform",
                "c": "Entirely dismissive, claiming they do not exist",
                "d": "Enthusiastic and uncritical",
                "correct": "B",
                "explanation": "The passage notes sceptics question whether these features are genuine reform or simply a public relations strategy.",
            },
        ],
    },

    # =========================================================
    # C1 — LEVEL 5
    # =========================================================

    {
        "level": "C1",
        "topic": "Science",
        "title": "The Ethical Frontier of Gene Editing",
        "text": (
            "Few scientific breakthroughs in recent memory have generated as "
            "much simultaneous excitement and unease as the development of "
            "precise gene-editing tools. Techniques that once seemed confined "
            "to speculative fiction now allow researchers to alter specific "
            "sequences of DNA with a level of accuracy that would have seemed "
            "implausible only a generation ago. The implications of this "
            "capability extend far beyond the laboratory, touching questions of "
            "medicine, agriculture, and, most controversially, the future "
            "trajectory of human evolution itself.\n\n"
            "In medicine, the potential applications are considerable. "
            "Inherited disorders caused by a single faulty gene, once "
            "considered permanent and untreatable, may eventually be corrected "
            "at their source rather than merely managed through lifelong "
            "treatment. Early clinical trials targeting certain blood disorders "
            "have already demonstrated promising results, offering a tangible "
            "glimpse of what was until recently theoretical. Proponents argue "
            "that dismissing such tools on the basis of caution alone risks "
            "denying patients access to genuinely transformative treatment.\n\n"
            "Yet the same technology that offers this promise also raises "
            "profound ethical questions, particularly when applied not to "
            "treat existing patients but to modify embryos in ways that would "
            "be inherited by future generations. Unlike conventional medical "
            "interventions, germline editing does not merely affect an "
            "individual; it introduces changes that could persist indefinitely "
            "within a family line, with consequences that remain, by "
            "definition, impossible to fully predict or reverse.\n\n"
            "Critics warn of a slippery slope extending from legitimate disease "
            "prevention toward more contentious applications, such as selecting "
            "or enhancing traits unrelated to illness. Should such enhancement "
            "eventually become technically feasible and socially normalised, "
            "some fear it could exacerbate existing inequalities, effectively "
            "allowing genetic advantages to become available primarily to those "
            "who can afford them, thereby entrenching disparities in an "
            "unprecedented and biologically literal sense.\n\n"
            "Regulatory frameworks, meanwhile, have struggled to keep pace with "
            "the technology's rapid advancement. International consensus "
            "remains elusive, with some countries imposing strict prohibitions "
            "while others maintain considerably more permissive regulatory "
            "environments, creating the possibility that researchers "
            "constrained in one jurisdiction might simply relocate their work "
            "elsewhere.\n\n"
            "What emerges from this landscape is not a straightforward "
            "narrative of scientific progress unambiguously benefiting "
            "humanity, but rather a more complicated negotiation between "
            "genuine therapeutic potential and the considerable ethical "
            "weight of decisions that, once made, cannot easily be undone."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Gene editing is a purely beneficial technology with no drawbacks.",
                "b": "Gene editing offers significant medical promise but raises complex, largely unresolved ethical concerns.",
                "c": "Gene editing has been universally banned by all governments.",
                "d": "Gene editing is no longer considered a viable scientific approach.",
                "correct": "B",
                "explanation": "The passage presents gene editing as both promising and ethically fraught, without offering a simple resolution.",
            },
            {
                "question": "According to the passage, what distinguishes germline editing from conventional medical treatment?",
                "a": "It is less expensive than traditional treatments.",
                "b": "It only affects the individual patient temporarily.",
                "c": "It introduces changes that can be inherited by future generations.",
                "d": "It has no relation to genetics at all.",
                "correct": "C",
                "explanation": "The passage explicitly states germline editing introduces heritable changes that could persist within a family line indefinitely.",
            },
            {
                "question": "What do critics fear could happen if genetic enhancement becomes normalised?",
                "a": "It could reduce the cost of medical treatment for everyone.",
                "b": "It could deepen existing social inequalities.",
                "c": "It could eliminate the need for regulation entirely.",
                "d": "It could make gene editing illegal worldwide.",
                "correct": "B",
                "explanation": "The passage states critics fear enhancement could exacerbate inequalities by making genetic advantages available mainly to the wealthy.",
            },
            {
                "question": "What does the phrase 'struggled to keep pace' suggest about regulatory frameworks?",
                "a": "Regulations have advanced faster than the technology.",
                "b": "Regulations have failed to develop as quickly as the technology itself.",
                "c": "Regulations are no longer necessary.",
                "d": "Regulations have been perfectly synchronised with scientific progress.",
                "correct": "B",
                "explanation": "The phrase indicates regulatory development has lagged behind the rapid advancement of gene-editing technology.",
            },
            {
                "question": "What can be inferred about the author's overall stance in the final paragraph?",
                "a": "The author presents gene editing as an uncomplicated positive development.",
                "b": "The author frames the issue as a genuine, unresolved tension between benefit and ethical risk.",
                "c": "The author firmly opposes all forms of gene editing.",
                "d": "The author believes the ethical concerns are exaggerated and unimportant.",
                "correct": "B",
                "explanation": "The final paragraph explicitly frames the issue as a complicated negotiation, avoiding a one-sided conclusion.",
            },
        ],
    },

    {
        "level": "C1",
        "topic": "History",
        "title": "The Silk Road as a Network of Exchange",
        "text": (
            "The term 'Silk Road', though evocative, is in many ways a "
            "misleading simplification of what was, in reality, a vast and "
            "decentralised network of overlapping trade routes connecting East "
            "Asia to the Mediterranean world. Coined by a German geographer in "
            "the nineteenth century, the phrase suggests a single, continuous "
            "path, when the historical reality involved countless interlocking "
            "routes, shifting over centuries in response to political "
            "circumstances, environmental conditions, and the rise and fall of "
            "empires along their length.\n\n"
            "Silk, while certainly among the most prized commodities traded "
            "along these routes, represented only a fraction of what actually "
            "moved between civilisations. Spices, precious stones, glassware, "
            "paper-making technology, and religious texts all travelled "
            "alongside merchants, as did less tangible goods: ideas, artistic "
            "styles, agricultural techniques, and, less desirably, diseases "
            "that spread along the same routes that carried commerce.\n\n"
            "Perhaps the most significant, though frequently underappreciated, "
            "consequence of this exchange was its role in the transmission of "
            "knowledge. Papermaking technology, developed in China centuries "
            "before it reached Europe, gradually spread westward along these "
            "trade networks, eventually transforming how information was "
            "recorded and disseminated across the societies it reached. "
            "Similarly, mathematical and astronomical knowledge moved in both "
            "directions, complicating any narrative that positions one "
            "civilisation as a purely passive recipient of another's "
            "innovations.\n\n"
            "Historians have increasingly pushed back against earlier, more "
            "simplistic framings that portrayed the Silk Road primarily as a "
            "conduit through which Eastern goods flowed toward an eager "
            "European market. Such accounts, critics argue, understate the "
            "agency and sophistication of societies across Central Asia, whose "
            "merchants, cities, and intermediary cultures were not merely "
            "passive corridors but active participants who shaped, negotiated, "
            "and often profited considerably from the terms of exchange.\n\n"
            "The eventual decline of these overland routes, precipitated partly "
            "by the rise of maritime trade capable of transporting goods more "
            "efficiently by sea, did not erase their significance. Rather, the "
            "networks established over centuries left lasting imprints on the "
            "cultural, religious, and linguistic landscapes of the regions they "
            "once connected, imprints that remain discernible in the historical "
            "record long after the caravans themselves ceased to travel."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "The Silk Road was a single, simple trade path used mainly for silk.",
                "b": "The Silk Road was a complex network that facilitated far more than the exchange of goods, including knowledge and ideas.",
                "c": "The Silk Road had no lasting impact on the regions it connected.",
                "d": "European merchants controlled the entirety of Silk Road trade.",
                "correct": "B",
                "explanation": "The passage emphasises the Silk Road's complexity and its role in transmitting knowledge, ideas, and culture beyond mere goods.",
            },
            {
                "question": "According to the passage, why is the term 'Silk Road' described as a 'misleading simplification'?",
                "a": "Because silk was never actually traded along these routes.",
                "b": "Because it implies a single path, when in reality it was many shifting, overlapping routes.",
                "c": "Because the term was invented by traders themselves.",
                "d": "Because the routes only existed for a few years.",
                "correct": "B",
                "explanation": "The passage explains the term suggests one continuous path, whereas the reality involved countless interlocking, shifting routes.",
            },
            {
                "question": "What example does the passage give of knowledge transmitted westward along these routes?",
                "a": "Printing press technology",
                "b": "Papermaking technology",
                "c": "Steam engine design",
                "d": "Telescope construction",
                "correct": "B",
                "explanation": "The passage specifically discusses papermaking technology spreading from China westward.",
            },
            {
                "question": "What criticism do historians make of earlier framings of the Silk Road?",
                "a": "They overstated the role of Central Asian societies.",
                "b": "They understated the agency of Central Asian merchants and cultures, treating them as passive corridors.",
                "c": "They ignored China's role entirely.",
                "d": "They focused too much on maritime trade.",
                "correct": "B",
                "explanation": "The passage states critics argue earlier accounts understate the agency and sophistication of Central Asian societies.",
            },
            {
                "question": "What can be inferred about the legacy of the Silk Road from the final paragraph?",
                "a": "Its influence disappeared entirely once maritime trade rose.",
                "b": "Its cultural and linguistic effects persisted long after the routes declined.",
                "c": "It had no connection to religion or language.",
                "d": "It became more important after maritime trade emerged.",
                "correct": "B",
                "explanation": "The passage states the networks left lasting imprints on culture, religion, and language that remain discernible long after decline.",
            },
        ],
    },

    {
        "level": "C1",
        "topic": "Architecture",
        "title": "Designing Cities for an Uncertain Climate",
        "text": (
            "Urban planners have long designed cities around relatively "
            "predictable assumptions: stable rainfall patterns, manageable "
            "temperature ranges, and infrastructure built to withstand "
            "conditions expected to persist for decades. As climate patterns "
            "grow increasingly volatile, however, this foundational assumption "
            "has become considerably harder to sustain, forcing architects and "
            "city planners to reconsider not merely individual buildings but the "
            "underlying logic of urban design itself.\n\n"
            "One emerging approach involves what some practitioners term "
            "'sponge cities' — urban environments deliberately designed to "
            "absorb, store, and gradually release rainwater rather than "
            "channelling it rapidly away through conventional drainage systems. "
            "Permeable pavements, expanded green spaces, and constructed "
            "wetlands within city boundaries serve simultaneously to reduce "
            "flood risk during intense rainfall and to retain water that can "
            "later mitigate the effects of drought, addressing two seemingly "
            "contradictory climate threats through a single integrated system.\n\n"
            "Rising temperatures present a parallel challenge, particularly in "
            "dense urban areas where the concentration of concrete and asphalt "
            "creates what researchers call the 'urban heat island' effect, in "
            "which cities can be measurably warmer than surrounding rural "
            "areas. Architects have responded with strategies ranging from "
            "reflective building materials that reduce heat absorption to "
            "extensive rooftop and vertical gardens that provide natural "
            "cooling through evaporation and shade, simultaneously improving "
            "air quality in densely populated districts.\n\n"
            "Critics of these approaches, however, caution against treating "
            "them as universally applicable solutions. What functions "
            "effectively in a temperate coastal city may prove poorly suited to "
            "an arid inland region, and implementing such measures often "
            "requires substantial upfront investment that many municipalities, "
            "particularly in lower-income regions most vulnerable to climate "
            "disruption, may struggle to afford without external financial "
            "support.\n\n"
            "There is also the more fundamental question of retrofitting versus "
            "rebuilding. Much of the infrastructure most vulnerable to climate "
            "volatility was constructed decades, sometimes centuries, before "
            "contemporary climate science existed, raising difficult questions "
            "about whether resources are better spent adapting existing "
            "structures or investing in entirely new developments designed from "
            "the outset with volatility in mind.\n\n"
            "Regardless of the specific strategy pursued, a growing consensus "
            "among urban planners suggests that the era of designing cities "
            "around static, predictable climate assumptions has effectively "
            "ended, replaced by an ongoing negotiation with uncertainty itself."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Climate change has had little effect on how cities are designed.",
                "b": "Urban planners are increasingly adapting city design to address growing climate unpredictability.",
                "c": "Sponge cities have completely solved urban flooding problems.",
                "d": "All cities require identical climate-adaptation strategies.",
                "correct": "B",
                "explanation": "The passage discusses how planners are rethinking urban design fundamentally in response to unpredictable climate conditions.",
            },
            {
                "question": "According to the passage, how do 'sponge cities' address both flooding and drought?",
                "a": "By building taller drainage systems",
                "b": "By absorbing and storing rainwater for gradual release rather than channelling it away quickly",
                "c": "By relocating residents during extreme weather",
                "d": "By reducing the number of buildings in a city",
                "correct": "B",
                "explanation": "The passage explains sponge cities absorb and store water, reducing flood risk while retaining water for drought mitigation.",
            },
            {
                "question": "What is the 'urban heat island' effect, according to the passage?",
                "a": "A phenomenon where cities are cooler than surrounding rural areas",
                "b": "A phenomenon where cities are measurably warmer than surrounding rural areas",
                "c": "A type of flood-prevention technology",
                "d": "A method of measuring rainfall in cities",
                "correct": "B",
                "explanation": "The passage defines the urban heat island effect as cities being measurably warmer due to concrete and asphalt concentration.",
            },
            {
                "question": "What concern do critics raise about climate-adaptive urban design strategies?",
                "a": "They are effective everywhere without exception.",
                "b": "They may not be universally applicable and can be costly, especially for lower-income regions.",
                "c": "They require no financial investment at all.",
                "d": "They are only relevant to coastal cities.",
                "correct": "B",
                "explanation": "The passage states critics caution these solutions are not universally applicable and require investment that some regions may struggle to afford.",
            },
            {
                "question": "What broader question does the passage raise about existing infrastructure?",
                "a": "Whether cities should stop building new infrastructure entirely",
                "b": "Whether it is better to adapt old infrastructure or invest in new developments designed for volatility",
                "c": "Whether infrastructure decisions should ignore climate science",
                "d": "Whether all old infrastructure should be immediately destroyed",
                "correct": "B",
                "explanation": "The passage explicitly raises the question of retrofitting versus rebuilding infrastructure in light of climate volatility.",
            },
        ],
    },

    {
        "level": "C1",
        "topic": "Creativity",
        "title": "Rethinking the Origins of Creative Insight",
        "text": (
            "The popular image of creative insight often centres on a single "
            "dramatic moment — the proverbial lightbulb flashing on above a "
            "solitary genius, arriving seemingly from nowhere to resolve a "
            "problem that had resisted every previous attempt. This narrative, "
            "while compelling and widely repeated in popular culture, sits "
            "uneasily with what cognitive research increasingly suggests about "
            "how creative ideas actually emerge.\n\n"
            "Rather than appearing spontaneously, most documented cases of "
            "creative breakthrough follow extended periods of what researchers "
            "term 'incubation', during which the conscious mind turns its "
            "attention elsewhere while less deliberate cognitive processes "
            "continue working on a problem in the background. Far from being "
            "wasted time, apparent idleness — a walk, a shower, a period of "
            "unfocused daydreaming — appears to play a functionally important "
            "role, allowing the mind to form unexpected connections that "
            "focused, effortful concentration tends to suppress.\n\n"
            "This finding complicates conventional attitudes toward "
            "productivity, particularly in professional environments that "
            "prize constant, visible engagement with tasks. If genuine insight "
            "depends partly on stepping away from a problem rather than "
            "persistently confronting it, then workplace cultures that "
            "discourage unstructured time may inadvertently undermine the very "
            "creativity they claim to value.\n\n"
            "Equally significant is growing evidence against the notion of "
            "creativity as a rare gift possessed by a select few. Studies "
            "examining the working habits of prolific creative individuals "
            "across disciplines reveal a common pattern: rather than relying "
            "primarily on innate talent, many attribute their productivity to "
            "systematic habits — consistent working schedules, extensive prior "
            "knowledge accumulated through years of study, and a willingness to "
            "generate large quantities of mediocre ideas as a precondition for "
            "occasionally producing exceptional ones.\n\n"
            "This reframing does not entirely dismiss the role of individual "
            "aptitude; some capacity for divergent thinking likely varies "
            "between individuals. It does, however, suggest that the popular "
            "mythology surrounding sudden, unearned inspiration obscures the "
            "considerable, often unglamorous groundwork that typically precedes "
            "moments that appear, in retrospect, remarkably spontaneous.\n\n"
            "Understanding creativity this way carries practical implications, "
            "suggesting that fostering innovation may depend less on searching "
            "for rare genius and more on cultivating environments, and personal "
            "habits, that allow incubation and sustained effort to coexist."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Creative insight arises purely from sudden, unexplainable genius.",
                "b": "Creative insight typically results from extended incubation and systematic habits rather than sudden inspiration alone.",
                "c": "Creativity cannot be studied scientifically.",
                "d": "Only a small number of gifted individuals are capable of creativity.",
                "correct": "B",
                "explanation": "The passage challenges the 'lightbulb moment' myth, presenting evidence for incubation and habitual practice as key drivers of creativity.",
            },
            {
                "question": "According to the passage, what role does 'incubation' play in creative insight?",
                "a": "It wastes time that could be spent working directly on a problem.",
                "b": "It allows less deliberate cognitive processes to form unexpected connections.",
                "c": "It has no measurable effect on creative outcomes.",
                "d": "It only works for professional writers.",
                "correct": "B",
                "explanation": "The passage explains incubation allows background cognitive processes to form connections that focused effort tends to suppress.",
            },
            {
                "question": "What criticism does the passage imply about workplace cultures that prize constant visible engagement?",
                "a": "They are ideal for fostering creativity.",
                "b": "They may inadvertently undermine the creativity they claim to value.",
                "c": "They have no connection to creative output.",
                "d": "They are the only effective way to boost innovation.",
                "correct": "B",
                "explanation": "The passage states such cultures may inadvertently undermine creativity if genuine insight depends on stepping away from tasks.",
            },
            {
                "question": "What common pattern do studies find among prolific creative individuals, according to the passage?",
                "a": "They rely almost entirely on natural talent.",
                "b": "They avoid generating mediocre ideas at all costs.",
                "c": "They maintain systematic habits and generate many ideas, most of which are not exceptional.",
                "d": "They work only during sudden bursts of inspiration.",
                "correct": "C",
                "explanation": "The passage states prolific creatives attribute productivity to systematic habits and generating large quantities of ideas, most of them mediocre.",
            },
            {
                "question": "What practical implication does the passage suggest for fostering innovation?",
                "a": "Organisations should search primarily for rare creative geniuses.",
                "b": "Environments should be designed to allow both incubation and sustained effort.",
                "c": "Creativity cannot be encouraged through environment or habit.",
                "d": "Innovation depends solely on individual aptitude.",
                "correct": "B",
                "explanation": "The final paragraph states fostering innovation may depend on cultivating environments and habits that allow incubation and sustained effort to coexist.",
            },
        ],
    },

]


class Command(BaseCommand):

    help = (
        "Seeds the Reading Bank with original CEFR-leveled reading passages "
        "and questions (Batch 1). Safe to run multiple times — never creates "
        "duplicates and never removes existing data."
    )

    @transaction.atomic
    def handle(self, *args, **options):

        new_passages = 0
        new_questions = 0
        skipped_passages = 0

        for item in DATA:

            passage, created = ReadingPassage.objects.get_or_create(
                title=item["title"],
                level=item["level"],
                defaults={
                    "topic": item["topic"],
                    "text": item["text"],
                    "is_active": True,
                },
            )

            if not created:
                skipped_passages += 1
                continue

            new_passages += 1

            for q in item["questions"]:

                ReadingQuestion.objects.create(
                    passage=passage,
                    question_type=ReadingQuestion.QuestionType.MULTIPLE_CHOICE,
                    question=q["question"],
                    option_a=q["a"],
                    option_b=q["b"],
                    option_c=q["c"],
                    option_d=q["d"],
                    correct_answer=q["correct"],
                    explanation=q["explanation"],
                )

                new_questions += 1

        total_passages = ReadingPassage.objects.count()
        total_questions = ReadingQuestion.objects.count()

        self.stdout.write(self.style.SUCCESS("Reading Bank Batch 1 ready!"))
        self.stdout.write("")
        self.stdout.write(f"New passages created: {new_passages}")
        self.stdout.write(f"New questions created: {new_questions}")

        if skipped_passages:
            self.stdout.write(
                f"Skipped (already existed): {skipped_passages} passages"
            )

        self.stdout.write("")
        self.stdout.write(f"Total passages in database: {total_passages}")
        self.stdout.write(f"Total questions in database: {total_questions}")
