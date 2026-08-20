"""
Management command: seed_reading_batch1_part2

Second installment of Reading Bank Batch 1.
Adds 20 more original CEFR-leveled passages (100 questions),
continuing directly from seed_reading_batch1.py.

Safe to run multiple times: uses get_or_create() keyed on
(title, level), so re-running never creates duplicates and never
touches existing Reading data. Independent from
seed_reading_batch1.py — running either command in any order,
any number of times, is safe.

Usage:
    python manage.py seed_reading_batch1_part2
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.school.models import ReadingPassage, ReadingQuestion


DATA = [

    # =========================================================
    # A1 — LEVEL 1
    # =========================================================

    {
        "level": "A1",
        "topic": "Learning",
        "title": "Learning to Ride a Bike",
        "text": (
            "Last month, my father taught me how to ride a bike. I was very "
            "nervous because I fell down two times when I tried before. But my "
            "father said practice is the only way to learn.\n\n"
            "We went to the park near our house on Saturday morning. The park "
            "was quiet because it was still early. My father held the back of "
            "the bike while I sat on it and started to pedal. At first, I was "
            "very slow and I looked down at my feet all the time.\n\n"
            "'Look forward, not down,' my father said. 'If you look at the "
            "road, you will not fall.' I tried to listen to him, and it "
            "helped a little. After twenty minutes, my father slowly let go of "
            "the bike, but I did not know it. I was riding by myself!\n\n"
            "When I looked back and saw my father was not holding the bike "
            "anymore, I got so surprised that I almost fell. But I put my feet "
            "down quickly and stopped safely. My father was smiling and "
            "clapping.\n\n"
            "Now I can ride my bike every day. I ride to my friend's house and "
            "around the park. Learning to ride a bike was difficult at first, "
            "but now it makes me feel free and happy."
        ),
        "questions": [
            {
                "question": "What is the passage mainly about?",
                "a": "A trip to the park",
                "b": "Learning to ride a bike with the help of a parent",
                "c": "Buying a new bike",
                "d": "A race between friends",
                "correct": "B",
                "explanation": "The passage describes how the writer learned to ride a bike with their father's help.",
            },
            {
                "question": "Why was the writer nervous at first?",
                "a": "Because the bike was too big",
                "b": "Because they had fallen down before",
                "c": "Because it was raining",
                "d": "Because the park was crowded",
                "correct": "B",
                "explanation": "The text says the writer was nervous because they had fallen down two times before.",
            },
            {
                "question": "What advice did the father give?",
                "a": "Ride faster",
                "b": "Hold the handlebars tightly",
                "c": "Look forward, not down",
                "d": "Wear a helmet",
                "correct": "C",
                "explanation": "The father told the writer to look forward, not down, so they would not fall.",
            },
            {
                "question": "How did the writer feel when they realised the father had let go?",
                "a": "Angry",
                "b": "Surprised",
                "c": "Bored",
                "d": "Sleepy",
                "correct": "B",
                "explanation": "The passage says the writer got so surprised that they almost fell.",
            },
            {
                "question": "What can be concluded about how the writer feels about riding a bike now?",
                "a": "They still find it difficult.",
                "b": "They enjoy it and feel free.",
                "c": "They do not ride anymore.",
                "d": "They prefer walking instead.",
                "correct": "B",
                "explanation": "The final paragraph says riding the bike now makes the writer feel free and happy.",
            },
        ],
    },

    {
        "level": "A1",
        "topic": "Cities",
        "title": "A Walk Around My City",
        "text": (
            "On Saturday, I decided to walk around my city instead of taking "
            "the bus. I wanted to see the streets and buildings more slowly "
            "and notice things I usually miss.\n\n"
            "I started at the old market near my house. The market was busy "
            "with people buying fruit, vegetables, and bread. I bought some "
            "apples and talked with the seller, who told me she has worked "
            "there for twenty years.\n\n"
            "After the market, I walked to the main square. There is a big "
            "clock tower in the middle of the square. Many people sit on the "
            "benches there and feed the pigeons. I sat for a while and watched "
            "the people walking past.\n\n"
            "Next, I walked along the river. There is a long path next to the "
            "water where people run, cycle, and walk their dogs. The water was "
            "clean, and I saw some ducks swimming near the bank.\n\n"
            "Finally, I walked to a small park with many trees. Children were "
            "playing on the swings while their parents talked nearby. I sat "
            "under a tree and rested before walking home.\n\n"
            "This walk took almost three hours, but I enjoyed every part of "
            "it. I learned that my city has many nice places that I never "
            "notice when I am on the bus."
        ),
        "questions": [
            {
                "question": "What is the best title for this passage?",
                "a": "Taking the Bus to Work",
                "b": "A Slow Walk Through My City",
                "c": "Buying Fruit at the Market",
                "d": "Feeding the Pigeons",
                "correct": "B",
                "explanation": "The passage describes a full walk through different parts of the city.",
            },
            {
                "question": "Where did the writer start the walk?",
                "a": "At the main square",
                "b": "At the old market",
                "c": "At the river",
                "d": "At the small park",
                "correct": "B",
                "explanation": "The passage says the writer started at the old market near their house.",
            },
            {
                "question": "According to the passage, what do people do near the river?",
                "a": "Sell fruit and vegetables",
                "b": "Run, cycle, and walk their dogs",
                "c": "Sit on benches feeding pigeons",
                "d": "Play on swings",
                "correct": "B",
                "explanation": "The text states there is a path where people run, cycle, and walk their dogs.",
            },
            {
                "question": "Why did the writer choose to walk instead of taking the bus?",
                "a": "The bus was not working.",
                "b": "They wanted to see the city more slowly.",
                "c": "The bus was too expensive.",
                "d": "It was a sunny day.",
                "correct": "B",
                "explanation": "The passage states the writer wanted to see the streets and buildings more slowly.",
            },
            {
                "question": "What can be inferred about the writer's opinion of the walk?",
                "a": "They regretted doing it.",
                "b": "They found it boring.",
                "c": "They enjoyed discovering new things about their city.",
                "d": "They will never walk again.",
                "correct": "C",
                "explanation": "The final paragraph shows the writer enjoyed the walk and learned new things about their city.",
            },
        ],
    },

    {
        "level": "A1",
        "topic": "Books",
        "title": "My Favourite Book",
        "text": (
            "My favourite book is called 'The Little Traveller'. My aunt gave "
            "it to me for my tenth birthday, and I have read it many times "
            "since then.\n\n"
            "The book is about a boy named Sami who travels to different "
            "countries with his grandfather. In every chapter, Sami visits a "
            "new place and learns something interesting about the people, the "
            "food, and the culture there.\n\n"
            "My favourite chapter is when Sami visits a small fishing village. "
            "He learns how to catch fish with the local children, and he eats "
            "food he has never tried before. At first, he is scared to try new "
            "food, but his grandfather tells him that trying new things is "
            "part of growing up.\n\n"
            "I like this book because it makes me want to travel too. I have "
            "never left my country, but when I read about Sami's trips, I feel "
            "like I am there with him. The pictures in the book are also very "
            "colourful and beautiful.\n\n"
            "I keep the book next to my bed, and sometimes I read one chapter "
            "before I sleep. I hope that one day I can travel like Sami and "
            "see new places for myself."
        ),
        "questions": [
            {
                "question": "Who gave the writer this book?",
                "a": "Their grandfather",
                "b": "Their aunt",
                "c": "Their teacher",
                "d": "Their friend",
                "correct": "B",
                "explanation": "The passage states the aunt gave the writer the book for their tenth birthday.",
            },
            {
                "question": "What is the book mainly about?",
                "a": "A boy learning to swim",
                "b": "A boy travelling with his grandfather",
                "c": "A girl who loves cooking",
                "d": "Two friends at school",
                "correct": "B",
                "explanation": "The passage describes the book as being about Sami travelling with his grandfather.",
            },
            {
                "question": "What does the grandfather tell Sami about trying new food?",
                "a": "It is dangerous.",
                "b": "It is part of growing up.",
                "c": "It is not necessary.",
                "d": "It should be avoided.",
                "correct": "B",
                "explanation": "The text says the grandfather tells Sami that trying new things is part of growing up.",
            },
            {
                "question": "Why does the writer like this book?",
                "a": "Because it is very short",
                "b": "Because it makes them want to travel",
                "c": "Because it has no pictures",
                "d": "Because their friend wrote it",
                "correct": "B",
                "explanation": "The passage explicitly states the book makes the writer want to travel too.",
            },
            {
                "question": "What can be inferred about the writer's own travel experience?",
                "a": "They have travelled to many countries.",
                "b": "They have never left their country.",
                "c": "They visited a fishing village once.",
                "d": "They dislike travelling.",
                "correct": "B",
                "explanation": "The passage says the writer has never left their country, unlike the character Sami.",
            },
        ],
    },

    {
        "level": "A1",
        "topic": "Music",
        "title": "Learning to Play Guitar",
        "text": (
            "Six months ago, I started learning to play the guitar. I always "
            "loved music, but I never played an instrument before. My older "
            "brother has a guitar he does not use anymore, so he gave it to "
            "me.\n\n"
            "At first, it was very difficult. My fingers hurt when I pressed "
            "the strings, and I could not make the chords sound clear. I "
            "wanted to stop many times because it felt too hard.\n\n"
            "My brother told me that everyone finds it hard at the "
            "beginning. He showed me some easy songs to practise and told me "
            "to play for fifteen minutes every day, even when I did not feel "
            "like it. Slowly, my fingers became stronger and did not hurt as "
            "much.\n\n"
            "After two months, I could play three simple songs without "
            "looking at my fingers. I felt very proud of myself. Now, I "
            "practise for thirty minutes every evening after my homework.\n\n"
            "Last week, I played a song for my family for the first time. "
            "They were very happy and clapped when I finished. My mother said "
            "she wants me to play at my sister's birthday party next month. I "
            "am nervous, but also very excited."
        ),
        "questions": [
            {
                "question": "Who gave the writer the guitar?",
                "a": "Their mother",
                "b": "Their sister",
                "c": "Their older brother",
                "d": "A music teacher",
                "correct": "C",
                "explanation": "The passage states the older brother gave the writer his unused guitar.",
            },
            {
                "question": "Why did the writer want to stop practising at first?",
                "a": "The guitar was too expensive.",
                "b": "Playing was difficult and their fingers hurt.",
                "c": "They did not like music.",
                "d": "They had no time.",
                "correct": "B",
                "explanation": "The text explains their fingers hurt and playing was difficult, making them want to stop.",
            },
            {
                "question": "What advice did the brother give?",
                "a": "Buy a new guitar",
                "b": "Practise for fifteen minutes every day",
                "c": "Take lessons at a music school",
                "d": "Stop playing for a while",
                "correct": "B",
                "explanation": "The brother told the writer to practise for fifteen minutes every day, even when they did not feel like it.",
            },
            {
                "question": "How did the writer feel after playing three songs without looking at their fingers?",
                "a": "Disappointed",
                "b": "Proud",
                "c": "Confused",
                "d": "Bored",
                "correct": "B",
                "explanation": "The passage states the writer felt very proud of themselves after this achievement.",
            },
            {
                "question": "What can be inferred about the writer's feelings toward the upcoming birthday party?",
                "a": "They feel only nervous.",
                "b": "They feel only excited.",
                "c": "They feel a mix of nervousness and excitement.",
                "d": "They do not want to play at all.",
                "correct": "C",
                "explanation": "The passage states the writer is nervous but also very excited about playing at the party.",
            },
        ],
    },

    # =========================================================
    # A2 — LEVEL 2
    # =========================================================

    {
        "level": "A2",
        "topic": "Lifestyle",
        "title": "A Simpler Way of Living",
        "text": (
            "In recent years, more and more people have started to think "
            "about living with fewer things. This idea, sometimes called "
            "'minimalism', encourages people to keep only what they really "
            "need and use, instead of collecting objects they rarely touch.\n\n"
            "My cousin Malika decided to try this way of living last year. "
            "She used to have a room full of clothes, books, and small "
            "decorations, but she often felt stressed when she looked around. "
            "She said the mess made her feel tired even before she started "
            "her day.\n\n"
            "Malika began by removing clothes she had not worn in over a "
            "year. She gave them to a charity shop instead of throwing them "
            "away. Then she looked at her books, keeping only the ones she "
            "truly loved and giving the rest to friends and neighbours.\n\n"
            "After a few weeks, her room looked completely different. There "
            "was more space, and it felt easier to clean. Malika told me that "
            "she also started spending less money, because she thought more "
            "carefully before buying new things.\n\n"
            "Not everyone agrees that minimalism is the right choice for "
            "them. Some people enjoy collecting things and find happiness in "
            "having many objects around them. However, for Malika, having "
            "less has given her a feeling of calm that she did not have "
            "before.\n\n"
            "Now, whenever I visit her flat, I notice how peaceful it feels "
            "compared to before. It has made me think about trying a simpler "
            "lifestyle myself."
        ),
        "questions": [
            {
                "question": "What is minimalism, according to the passage?",
                "a": "A way of collecting expensive objects",
                "b": "A lifestyle of keeping only what you truly need",
                "c": "A type of home decoration style",
                "d": "A method of saving for a house",
                "correct": "B",
                "explanation": "The passage defines minimalism as encouraging people to keep only what they need and use.",
            },
            {
                "question": "How did Malika feel about her room before she changed her habits?",
                "a": "Relaxed",
                "b": "Proud",
                "c": "Stressed and tired",
                "d": "Excited",
                "correct": "C",
                "explanation": "The passage says the mess made her feel stressed and tired even before starting her day.",
            },
            {
                "question": "What did Malika do with clothes she had not worn in over a year?",
                "a": "Sold them online",
                "b": "Gave them to a charity shop",
                "c": "Threw them away",
                "d": "Kept them in storage",
                "correct": "B",
                "explanation": "The text states she gave unused clothes to a charity shop instead of throwing them away.",
            },
            {
                "question": "According to the passage, how did minimalism affect Malika's spending?",
                "a": "She started spending more money.",
                "b": "She started spending less money.",
                "c": "Her spending did not change.",
                "d": "She stopped buying anything at all.",
                "correct": "B",
                "explanation": "The passage says she started spending less because she thought more carefully before buying things.",
            },
            {
                "question": "What is the writer's overall opinion of Malika's new lifestyle?",
                "a": "The writer disapproves of it completely.",
                "b": "The writer is considering trying something similar.",
                "c": "The writer thinks it is a waste of time.",
                "d": "The writer prefers collecting objects.",
                "correct": "B",
                "explanation": "The final paragraph states the writer has been thinking about trying a simpler lifestyle themselves.",
            },
        ],
    },

    {
        "level": "A2",
        "topic": "Transport",
        "title": "Cycling to Work",
        "text": (
            "Six months ago, I decided to stop taking the bus to work and "
            "start cycling instead. My office is about seven kilometres from "
            "my home, which felt like a long distance at first, but I wanted "
            "to try something new.\n\n"
            "The first week was difficult. My legs were tired every evening, "
            "and I arrived at work feeling hot and out of breath. Some of my "
            "colleagues laughed and asked why I did not just take the bus "
            "like everyone else. However, I decided to continue for at least "
            "a month before making a final decision.\n\n"
            "By the third week, something changed. My legs felt stronger, and "
            "the ride started to feel easier and more enjoyable. I began to "
            "notice small things along the way, such as a park with beautiful "
            "flowers and a small café that I had never seen from the bus "
            "window.\n\n"
            "Cycling also saved me money. I no longer needed to pay for bus "
            "tickets, and I did not need to buy a gym membership because "
            "cycling gave me enough exercise. My doctor even told me that my "
            "general health had improved since I started.\n\n"
            "Of course, cycling is not always convenient. On rainy days, I "
            "still have to take the bus, and I need to leave home a little "
            "earlier than before. Still, I believe the benefits are much "
            "greater than the small problems.\n\n"
            "Now, some of the colleagues who laughed at me have started "
            "cycling too, and we sometimes ride to work together."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Cycling to work is always easy from the beginning.",
                "b": "The writer describes how cycling to work became a positive habit despite early challenges.",
                "c": "The writer stopped cycling after a month.",
                "d": "Colleagues never changed their opinion about cycling.",
                "correct": "B",
                "explanation": "The passage traces the writer's journey from difficulty to enjoying and benefiting from cycling.",
            },
            {
                "question": "How did the writer feel during the first week of cycling?",
                "a": "Confident and relaxed",
                "b": "Tired and out of breath",
                "c": "Bored and uninterested",
                "d": "Excited and energetic",
                "correct": "B",
                "explanation": "The passage states the writer's legs were tired and they felt hot and out of breath.",
            },
            {
                "question": "According to the passage, how did cycling save the writer money?",
                "a": "By avoiding bus tickets and a gym membership",
                "b": "By receiving money from the company",
                "c": "By selling their old bicycle",
                "d": "By working fewer hours",
                "correct": "A",
                "explanation": "The passage explains cycling meant no bus tickets and no need for a gym membership.",
            },
            {
                "question": "What does the writer do on rainy days?",
                "a": "Walks to work",
                "b": "Stays home from work",
                "c": "Takes the bus",
                "d": "Cycles anyway",
                "correct": "C",
                "explanation": "The text states that on rainy days the writer still has to take the bus.",
            },
            {
                "question": "What can be inferred from the final paragraph?",
                "a": "The colleagues still disapprove of cycling.",
                "b": "The writer's example influenced some colleagues to start cycling too.",
                "c": "The writer stopped cycling with colleagues.",
                "d": "No one else in the office cycles.",
                "correct": "B",
                "explanation": "The passage states some colleagues who laughed have started cycling too, showing the writer's influence.",
            },
        ],
    },

    {
        "level": "A2",
        "topic": "Sports",
        "title": "My First Marathon",
        "text": (
            "Last autumn, I ran my first marathon. A marathon is a race of "
            "just over forty-two kilometres, which is much longer than any "
            "distance I had run before. I decided to try it after watching my "
            "friend finish one the year before.\n\n"
            "My training started five months before the race. At first, I "
            "could only run for twenty minutes without stopping, but my "
            "training plan slowly increased the distance each week. I ran "
            "three or four times a week, even on cold or rainy mornings when "
            "I really did not want to leave my bed.\n\n"
            "The hardest part of training was not physical tiredness, but "
            "staying motivated. There were many weeks when I felt like "
            "giving up, especially when my legs hurt or I had a bad day at "
            "work. My sister helped me by running with me on weekends and "
            "reminding me why I started.\n\n"
            "On the day of the race, I was extremely nervous. Thousands of "
            "runners stood at the starting line, and the atmosphere was "
            "exciting but also frightening. The first twenty kilometres felt "
            "manageable, but after that, my legs started to feel very heavy.\n\n"
            "At around the thirty-fifth kilometre, I wanted to stop "
            "completely. However, I remembered all the training I had done "
            "and continued, one step at a time. When I finally crossed the "
            "finish line, I cried from happiness and exhaustion.\n\n"
            "Completing that marathon taught me that with enough patience and "
            "consistent effort, I can achieve things that once seemed "
            "impossible."
        ),
        "questions": [
            {
                "question": "What inspired the writer to try running a marathon?",
                "a": "A doctor's advice",
                "b": "Watching a friend finish one the year before",
                "c": "A school competition",
                "d": "A television advertisement",
                "correct": "B",
                "explanation": "The passage states the writer decided to try after watching their friend finish a marathon.",
            },
            {
                "question": "According to the passage, what was the hardest part of training?",
                "a": "Waking up early",
                "b": "Physical tiredness",
                "c": "Staying motivated",
                "d": "Buying running shoes",
                "correct": "C",
                "explanation": "The text explicitly says the hardest part was not physical tiredness, but staying motivated.",
            },
            {
                "question": "Who helped the writer stay motivated during training?",
                "a": "Their friend",
                "b": "Their sister",
                "c": "Their coach",
                "d": "Their colleague",
                "correct": "B",
                "explanation": "The passage states the sister helped by running with the writer on weekends.",
            },
            {
                "question": "What happened at around the thirty-fifth kilometre of the race?",
                "a": "The writer felt fresh and energetic.",
                "b": "The writer wanted to stop completely.",
                "c": "The writer met their sister.",
                "d": "The race was cancelled.",
                "correct": "B",
                "explanation": "The passage states the writer wanted to stop completely at around the thirty-fifth kilometre.",
            },
            {
                "question": "What is the main lesson the writer learned from the experience?",
                "a": "Marathons are too difficult to attempt.",
                "b": "Patience and consistent effort can achieve difficult goals.",
                "c": "Running alone is better than running with others.",
                "d": "Training is unnecessary for a marathon.",
                "correct": "B",
                "explanation": "The final paragraph states the experience taught the writer that patience and consistent effort make difficult goals achievable.",
            },
        ],
    },

    {
        "level": "A2",
        "topic": "Museums",
        "title": "A Visit to the City Museum",
        "text": (
            "Last weekend, my class visited the City Museum as part of a "
            "history project. I was not very excited at first because I "
            "thought museums were boring, but the visit surprised me in a "
            "good way.\n\n"
            "When we arrived, a guide named Mr. Tashkentov met us at the "
            "entrance. He explained that the museum has three floors, each "
            "showing a different period of our city's history. We started on "
            "the ground floor, which showed objects from hundreds of years "
            "ago, including old coins, pottery, and tools.\n\n"
            "On the second floor, there were paintings and photographs "
            "showing how the city looked one hundred years ago. It was "
            "strange to see photos of streets I know well, but with "
            "completely different buildings and no cars. My classmates and I "
            "spent a long time comparing the old photos with what the streets "
            "look like today.\n\n"
            "My favourite part was the third floor, which had an interactive "
            "exhibition about traditional crafts. We could try weaving simple "
            "patterns and painting small pieces of pottery ourselves. The "
            "guide explained that these crafts were once very common in our "
            "region but are now practised by only a small number of people.\n\n"
            "By the end of the visit, I had completely changed my opinion "
            "about museums. I learned so much about my own city that I had "
            "never known before, and I even asked my parents if we could go "
            "back together next month."
        ),
        "questions": [
            {
                "question": "What was the writer's opinion of museums before the visit?",
                "a": "They loved museums.",
                "b": "They thought museums were boring.",
                "c": "They had never heard of museums.",
                "d": "They visited museums often.",
                "correct": "B",
                "explanation": "The passage states the writer thought museums were boring at first.",
            },
            {
                "question": "What was shown on the ground floor of the museum?",
                "a": "Modern paintings",
                "b": "Objects from hundreds of years ago",
                "c": "Interactive craft exhibitions",
                "d": "Photographs of the city today",
                "correct": "B",
                "explanation": "The passage states the ground floor showed objects from hundreds of years ago, like coins, pottery, and tools.",
            },
            {
                "question": "Why did the writer find the second floor strange?",
                "a": "Because it had no lights",
                "b": "Because the photos showed familiar streets with very different buildings",
                "c": "Because it was very small",
                "d": "Because it had no guide",
                "correct": "B",
                "explanation": "The text says it was strange to see familiar streets in old photos with completely different buildings and no cars.",
            },
            {
                "question": "What could visitors do on the third floor?",
                "a": "Watch a film about history",
                "b": "Try weaving and painting pottery themselves",
                "c": "Buy souvenirs",
                "d": "Meet local artists",
                "correct": "B",
                "explanation": "The passage states visitors could try weaving simple patterns and painting pottery on the third floor.",
            },
            {
                "question": "What can be concluded about the writer's feelings after the visit?",
                "a": "They still dislike museums.",
                "b": "Their opinion of museums changed positively.",
                "c": "They were disappointed by the experience.",
                "d": "They do not want to visit again.",
                "correct": "B",
                "explanation": "The final paragraph shows the writer's opinion changed and they want to return with their parents.",
            },
        ],
    },

    # =========================================================
    # B1 — LEVEL 3
    # =========================================================

    {
        "level": "B1",
        "topic": "Human behaviour",
        "title": "Why We Follow the Crowd",
        "text": (
            "Have you ever changed your opinion simply because everyone "
            "around you seemed to agree on something? This common behaviour, "
            "known as conformity, has been studied by psychologists for "
            "decades, and the results reveal a great deal about how humans "
            "think in social situations.\n\n"
            "One of the most famous experiments on this topic asked "
            "participants to compare the length of lines on a card. The "
            "answer was obvious, and almost everyone could identify the "
            "correct line easily when alone. However, when participants were "
            "placed in a group where other people, secretly instructed by the "
            "researchers, gave an incorrect answer on purpose, many "
            "participants changed their own answer to match the group, even "
            "though their eyes clearly showed them the correct one.\n\n"
            "Psychologists explain this behaviour through two main reasons. "
            "The first is called informational influence, which happens when "
            "people assume that a group probably knows something they do not, "
            "especially in situations that are confusing or uncertain. The "
            "second is normative influence, which occurs when people conform "
            "simply to avoid feeling embarrassed or being rejected by others, "
            "even if they privately believe the group is wrong.\n\n"
            "Conformity is not always negative. In many situations, following "
            "social norms helps societies function smoothly, such as waiting "
            "in line or following traffic rules. Problems arise, however, when "
            "conformity prevents people from speaking up about mistakes, "
            "unfair treatment, or dangerous situations simply because no one "
            "else in the group seems concerned.\n\n"
            "Understanding conformity can help individuals recognise when they "
            "are being influenced unfairly by group pressure. Simply being "
            "aware that this tendency exists can make it easier to pause and "
            "consider a situation independently, rather than automatically "
            "following what everyone else appears to believe."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "People never change their opinions in groups.",
                "b": "Conformity is a well-studied human behaviour with both helpful and harmful effects.",
                "c": "Group experiments are unreliable and should be ignored.",
                "d": "Everyone should always follow the majority opinion.",
                "correct": "B",
                "explanation": "The passage explains conformity, its causes, and both its positive and negative effects on behaviour.",
            },
            {
                "question": "In the line experiment described, what happened when other participants gave a wrong answer on purpose?",
                "a": "Everyone ignored the incorrect answer.",
                "b": "Many participants changed their answer to match the group, despite clear visual evidence.",
                "c": "The experiment was stopped immediately.",
                "d": "Participants left the room in protest.",
                "correct": "B",
                "explanation": "The passage states many participants matched the group's incorrect answer even though their eyes showed the correct one.",
            },
            {
                "question": "What is 'informational influence', according to the passage?",
                "a": "Conforming to avoid embarrassment",
                "b": "Assuming a group knows something you do not, especially in uncertain situations",
                "c": "Refusing to listen to others",
                "d": "A type of formal education",
                "correct": "B",
                "explanation": "The passage defines informational influence as assuming the group probably knows something you do not.",
            },
            {
                "question": "According to the passage, when does conformity become a problem?",
                "a": "When people follow traffic rules",
                "b": "When it prevents people from speaking up about mistakes or unfair treatment",
                "c": "When people wait in line politely",
                "d": "When societies function smoothly",
                "correct": "B",
                "explanation": "The passage states problems arise when conformity stops people from addressing mistakes or unfairness.",
            },
            {
                "question": "What is the purpose of the final paragraph?",
                "a": "To criticise psychologists",
                "b": "To suggest that awareness of conformity can help people think more independently",
                "c": "To argue that conformity should be eliminated entirely",
                "d": "To describe a new experiment",
                "correct": "B",
                "explanation": "The final paragraph explains that awareness of conformity can help people pause and think independently.",
            },
        ],
    },

    {
        "level": "B1",
        "topic": "Business",
        "title": "The Rise of Small Online Shops",
        "text": (
            "A decade ago, starting a retail business usually meant renting a "
            "physical shop, which required significant money for rent, "
            "furniture, and staff. Today, thanks to online platforms, many "
            "entrepreneurs are launching small businesses directly from their "
            "homes, selling handmade or specialised products to customers "
            "around the world.\n\n"
            "One example is Nodira, a young woman who started selling "
            "handmade jewellery through a social media page three years ago. "
            "At first, she made only a few pieces each week and sold them to "
            "friends and neighbours. As her photos began attracting more "
            "attention online, orders started arriving from other cities, and "
            "eventually from other countries.\n\n"
            "Nodira explains that the biggest advantage of selling online is "
            "the low starting cost. She did not need to rent a shop or hire "
            "employees; she could manage everything from a small table in her "
            "living room. This allowed her to test which products customers "
            "liked before investing more money in materials.\n\n"
            "However, running an online business is not without challenges. "
            "Nodira must manage photography, customer messages, packaging, and "
            "shipping almost entirely by herself. She also faces strong "
            "competition, since customers can easily compare her prices with "
            "hundreds of similar sellers with just a few clicks.\n\n"
            "Trust is another obstacle that online sellers must overcome. "
            "Unlike a physical shop, customers cannot see or touch a product "
            "before buying it, so Nodira relies heavily on clear photographs, "
            "honest descriptions, and positive customer reviews to convince "
            "new buyers.\n\n"
            "Despite these difficulties, Nodira now earns more from her small "
            "online business than she did from her previous full-time job, "
            "and she plans to hire her first employee later this year."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Online shops always fail because of competition.",
                "b": "Online platforms have made it easier for small entrepreneurs to start businesses, though challenges remain.",
                "c": "Physical shops are always more profitable than online ones.",
                "d": "Nodira plans to close her business soon.",
                "correct": "B",
                "explanation": "The passage uses Nodira's story to illustrate both the opportunities and challenges of online selling.",
            },
            {
                "question": "According to the passage, what is the biggest advantage of selling online, according to Nodira?",
                "a": "Higher prices for products",
                "b": "The low starting cost",
                "c": "Guaranteed customer trust",
                "d": "No need for photography",
                "correct": "B",
                "explanation": "The passage explicitly states Nodira sees low starting cost as the biggest advantage.",
            },
            {
                "question": "What challenge does Nodira face regarding competition?",
                "a": "She has no competitors at all.",
                "b": "Customers can easily compare her prices with many similar sellers.",
                "c": "She cannot access the internet regularly.",
                "d": "Her products are too expensive to sell.",
                "correct": "B",
                "explanation": "The passage states customers can easily compare her prices with hundreds of similar sellers online.",
            },
            {
                "question": "Why is trust described as an obstacle for online sellers?",
                "a": "Customers cannot see or touch products before buying.",
                "b": "Customers always distrust handmade products.",
                "c": "Online payments are illegal in some countries.",
                "d": "Customers prefer physical shops exclusively.",
                "correct": "A",
                "explanation": "The passage explains customers cannot physically examine products, making trust harder to establish.",
            },
            {
                "question": "What can be concluded about Nodira's business by the end of the passage?",
                "a": "It has been unsuccessful compared to her previous job.",
                "b": "It has grown enough that she plans to hire an employee.",
                "c": "She has decided to close it permanently.",
                "d": "It only sells to local customers now.",
                "correct": "B",
                "explanation": "The final paragraph states she earns more than before and plans to hire her first employee.",
            },
        ],
    },

    {
        "level": "B1",
        "topic": "Wildlife",
        "title": "Protecting Endangered Species",
        "text": (
            "Around the world, thousands of animal species face the risk of "
            "extinction, meaning they could disappear completely if current "
            "trends continue. While extinction has always been a natural part "
            "of life on Earth, scientists warn that the current rate of "
            "species loss is happening far faster than at any point in "
            "recorded history, largely because of human activity.\n\n"
            "Habitat loss is one of the most significant causes of this "
            "problem. As forests are cut down for farming or cities expand "
            "into natural areas, animals lose the spaces where they find "
            "food, build homes, and raise their young. Without suitable "
            "habitat, even species that are not directly hunted can struggle "
            "to survive.\n\n"
            "Poaching, the illegal hunting of animals, presents another "
            "serious threat, particularly for species valued for their fur, "
            "horns, or other body parts. Despite international laws designed "
            "to prevent this trade, demand in certain markets continues to "
            "drive illegal hunting, pushing some species dangerously close to "
            "extinction.\n\n"
            "Conservation organisations use several strategies to address "
            "these threats. Protected areas, such as national parks, offer "
            "animals a safe space away from habitat destruction. Breeding "
            "programmes in zoos and wildlife centres aim to increase "
            "population numbers before releasing animals back into the wild, "
            "although this process can be slow and expensive.\n\n"
            "Some conservationists argue that local communities should play a "
            "central role in protection efforts, since people living near "
            "wildlife often understand the environment better than distant "
            "organisations. When local communities benefit economically from "
            "conservation, for example through wildlife tourism, they are "
            "often more motivated to protect animals rather than see them as "
            "obstacles to development.\n\n"
            "While the challenges remain significant, successful recovery "
            "stories for certain species show that, with sustained effort, "
            "extinction is not always inevitable."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Extinction is a completely new phenomenon caused only by hunting.",
                "b": "Species extinction is accelerated by human activity, but conservation efforts offer hope.",
                "c": "Habitat loss has no connection to extinction.",
                "d": "Conservation efforts have always failed completely.",
                "correct": "B",
                "explanation": "The passage discusses causes of extinction and various conservation strategies, ending with hope for recovery.",
            },
            {
                "question": "According to the passage, why is habitat loss so damaging to animal populations?",
                "a": "It only affects animals that are hunted.",
                "b": "It removes spaces animals need for food, shelter, and raising young.",
                "c": "It has no effect on non-hunted species.",
                "d": "It only occurs in cities.",
                "correct": "B",
                "explanation": "The passage explains that without suitable habitat, animals struggle to find food, build homes, and raise young.",
            },
            {
                "question": "What does 'poaching' mean, according to the passage?",
                "a": "Legal, regulated hunting",
                "b": "The illegal hunting of animals",
                "c": "A type of habitat restoration",
                "d": "A breeding programme technique",
                "correct": "B",
                "explanation": "The passage explicitly defines poaching as the illegal hunting of animals.",
            },
            {
                "question": "Why might local communities be motivated to protect wildlife, according to the passage?",
                "a": "Because international laws force them to",
                "b": "Because they can benefit economically, for example through wildlife tourism",
                "c": "Because they dislike distant organisations",
                "d": "Because breeding programmes are located in their villages",
                "correct": "B",
                "explanation": "The passage states economic benefits, such as wildlife tourism, motivate communities to protect animals.",
            },
            {
                "question": "What is the tone of the final paragraph?",
                "a": "Completely pessimistic",
                "b": "Cautiously hopeful",
                "c": "Angry and critical",
                "d": "Indifferent",
                "correct": "B",
                "explanation": "The final paragraph acknowledges challenges but notes recovery stories show extinction is not always inevitable, reflecting cautious hope.",
            },
        ],
    },

    {
        "level": "B1",
        "topic": "Oceans",
        "title": "The Hidden World of Coral Reefs",
        "text": (
            "Although coral reefs cover less than one percent of the ocean "
            "floor, they support an extraordinary proportion of marine life. "
            "Sometimes described as the 'rainforests of the sea', reefs "
            "provide shelter, food, and breeding grounds for thousands of "
            "species of fish, crustaceans, and other marine organisms.\n\n"
            "Corals themselves are often mistaken for plants or rocks, but "
            "they are actually formed by tiny animals called polyps. These "
            "polyps live in large colonies and produce hard skeletons made of "
            "calcium carbonate, which slowly build up over many years to "
            "create the complex reef structures visible underwater.\n\n"
            "Many corals rely on a close relationship with microscopic algae "
            "that live inside their tissue. These algae produce food through "
            "photosynthesis, sharing nutrients with the coral in exchange for "
            "a protected place to live. This partnership also gives coral its "
            "bright, vivid colours.\n\n"
            "Unfortunately, this delicate relationship can break down when "
            "ocean temperatures rise even slightly above normal levels. Under "
            "heat stress, corals expel the algae living inside them, causing "
            "the coral to turn white in a process known as coral bleaching. "
            "Bleached coral is not immediately dead, but it becomes weaker "
            "and more likely to die if warm conditions continue.\n\n"
            "Rising ocean temperatures linked to climate change have already "
            "caused widespread bleaching events across major reef systems, "
            "including some of the largest reefs in the world. Scientists "
            "warn that without significant reductions in global emissions, "
            "many reefs could face irreversible damage within the coming "
            "decades.\n\n"
            "Protecting coral reefs matters far beyond their beauty. Millions "
            "of people depend on healthy reefs for fishing, tourism income, "
            "and natural protection from coastal storms, making their "
            "survival a concern for both marine ecosystems and human "
            "communities."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Coral reefs are unimportant compared to the open ocean.",
                "b": "Coral reefs support enormous biodiversity but are seriously threatened by rising temperatures.",
                "c": "Coral is a type of plant that grows only in warm water.",
                "d": "Coral bleaching always results in immediate death.",
                "correct": "B",
                "explanation": "The passage explains the biodiversity reefs support and the serious threat posed by rising temperatures.",
            },
            {
                "question": "According to the passage, what are corals actually formed by?",
                "a": "Rocks that grow over time",
                "b": "Tiny animals called polyps",
                "c": "Plants that live underwater",
                "d": "Grains of sand",
                "correct": "B",
                "explanation": "The passage explicitly states corals are formed by tiny animals called polyps.",
            },
            {
                "question": "What role do the microscopic algae play for coral?",
                "a": "They damage the coral's skeleton.",
                "b": "They produce food through photosynthesis and give coral its colour.",
                "c": "They cause coral bleaching directly.",
                "d": "They have no relationship with coral.",
                "correct": "B",
                "explanation": "The passage states the algae produce food through photosynthesis and give coral its bright colours.",
            },
            {
                "question": "What happens during coral bleaching, according to the passage?",
                "a": "Coral immediately dies.",
                "b": "Coral expels its algae and turns white due to heat stress.",
                "c": "Coral grows faster than usual.",
                "d": "Coral changes colour to bright red.",
                "correct": "B",
                "explanation": "The passage explains that heat stress causes corals to expel algae, turning them white.",
            },
            {
                "question": "Why does the passage say coral reef survival concerns human communities, not just marine ecosystems?",
                "a": "Because reefs are used only for scientific research",
                "b": "Because millions of people depend on reefs for fishing, tourism, and storm protection",
                "c": "Because reefs provide drinking water",
                "d": "Because reefs are the only source of seafood worldwide",
                "correct": "B",
                "explanation": "The final paragraph states people depend on reefs for fishing, tourism income, and protection from coastal storms.",
            },
        ],
    },

    # =========================================================
    # B2 — LEVEL 4
    # =========================================================

    {
        "level": "B2",
        "topic": "Renewable energy",
        "title": "The Growing Role of Solar Power",
        "text": (
            "For much of the twentieth century, solar power remained a "
            "marginal technology, admired for its environmental promise but "
            "dismissed by many economists as impractical due to its "
            "considerable cost compared to fossil fuels. That situation has "
            "changed dramatically over the past two decades, as the price of "
            "solar panels has fallen sharply, transforming solar energy from a "
            "niche alternative into one of the most competitive sources of "
            "electricity in many parts of the world.\n\n"
            "This dramatic price reduction has resulted largely from "
            "improvements in manufacturing technology and significant "
            "increases in production scale, particularly in countries that "
            "invested heavily in solar panel manufacturing. As factories "
            "became larger and more efficient, and as demand grew, the cost "
            "per unit of solar energy produced fell consistently, defying "
            "earlier predictions that such reductions would eventually level "
            "off.\n\n"
            "Despite this progress, solar power still faces a fundamental "
            "limitation: intermittency. Solar panels generate electricity only "
            "when sunlight is available, meaning production naturally "
            "decreases at night and during cloudy weather. This "
            "characteristic complicates efforts to rely on solar power as a "
            "primary energy source, since electricity grids require a "
            "constant, reliable supply to function properly.\n\n"
            "Battery storage technology has emerged as a partial solution to "
            "this problem, allowing excess electricity generated during sunny "
            "periods to be stored and used later when solar production is "
            "low. However, battery technology remains relatively expensive, "
            "and questions persist about whether current storage capacity can "
            "scale sufficiently to support electricity grids that rely "
            "heavily on solar power.\n\n"
            "Critics of rapid solar expansion also point to less-discussed "
            "challenges, such as the environmental impact of manufacturing "
            "panels and eventually disposing of them once they reach the end "
            "of their operational lifespan, typically after twenty to "
            "twenty-five years. Proponents counter that these impacts remain "
            "considerably smaller than those associated with fossil fuel "
            "extraction and combustion over comparable timeframes.\n\n"
            "Whatever the eventual balance between these competing "
            "considerations, solar power's transformation from a marginal "
            "technology into a mainstream energy source represents one of the "
            "more significant shifts in the global energy sector in recent "
            "memory."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Solar power remains too expensive to be practical anywhere.",
                "b": "Solar power has become far more competitive, though it still faces significant technical and environmental challenges.",
                "c": "Battery storage has completely solved the problem of intermittency.",
                "d": "Fossil fuels are more environmentally friendly than solar power.",
                "correct": "B",
                "explanation": "The passage traces solar power's transformation into a competitive energy source while acknowledging remaining challenges.",
            },
            {
                "question": "According to the passage, what caused the dramatic reduction in solar panel prices?",
                "a": "Government bans on fossil fuels",
                "b": "Improvements in manufacturing technology and increased production scale",
                "c": "A sudden decrease in global demand",
                "d": "New international trade agreements",
                "correct": "B",
                "explanation": "The passage explicitly attributes the price reduction to manufacturing improvements and increased production scale.",
            },
            {
                "question": "What does 'intermittency' refer to in the context of solar power?",
                "a": "The high cost of solar panels",
                "b": "The inconsistent availability of sunlight affecting electricity production",
                "c": "The environmental impact of manufacturing",
                "d": "The process of disposing of old panels",
                "correct": "B",
                "explanation": "The passage explains intermittency as the fact that solar production depends on available sunlight, decreasing at night and in cloudy weather.",
            },
            {
                "question": "According to the passage, what limitation does battery storage technology currently face?",
                "a": "It has completely eliminated the problem of intermittency.",
                "b": "It remains relatively expensive, with questions about scaling sufficiently.",
                "c": "It is banned in most countries.",
                "d": "It has no connection to solar energy.",
                "correct": "B",
                "explanation": "The passage states battery technology remains expensive and questions persist about whether it can scale sufficiently.",
            },
            {
                "question": "How do proponents of solar power respond to criticism about panel disposal?",
                "a": "They deny that disposal is a problem at all.",
                "b": "They argue the environmental impact is smaller than fossil fuel extraction and combustion.",
                "c": "They agree solar power should be abandoned.",
                "d": "They claim panels never need to be disposed of.",
                "correct": "B",
                "explanation": "The passage states proponents counter that these impacts remain smaller than those from fossil fuels over comparable timeframes.",
            },
        ],
    },

    {
        "level": "B2",
        "topic": "Future technology",
        "title": "Living Alongside Artificial Intelligence",
        "text": (
            "Artificial intelligence, once confined largely to science "
            "fiction and specialised research laboratories, has moved rapidly "
            "into everyday life over the past decade. From recommendation "
            "systems that suggest what to watch or buy, to voice assistants "
            "that answer questions in natural language, AI now shapes "
            "countless routine decisions in ways many people barely notice.\n\n"
            "This growing presence has prompted a wide range of reactions, "
            "from enthusiastic optimism to considerable anxiety. Advocates "
            "argue that AI systems can dramatically increase efficiency, "
            "handling repetitive or data-intensive tasks far faster and more "
            "accurately than humans, freeing people to focus on work that "
            "requires creativity, judgement, or emotional intelligence — "
            "qualities that remain, for now, distinctly human.\n\n"
            "Sceptics, however, raise legitimate concerns about the pace of "
            "this transition. Automation has historically displaced certain "
            "categories of jobs, and while new roles typically emerge over "
            "time, the transition period can impose considerable hardship on "
            "workers whose skills become less valuable seemingly overnight. "
            "Whether current AI advances will follow this familiar historical "
            "pattern, or represent something qualitatively different, remains "
            "a matter of genuine debate among economists.\n\n"
            "Beyond employment, questions of accountability present another "
            "significant challenge. When an AI system makes a consequential "
            "error — in medical diagnosis, financial lending, or legal "
            "decision-making, for example — determining responsibility "
            "becomes considerably more complicated than in cases involving "
            "purely human decision-makers. Was the fault in the underlying "
            "data, the algorithm's design, or the way humans deployed the "
            "system? Legal and regulatory frameworks are still catching up "
            "with these questions.\n\n"
            "There is also the more subtle concern of over-reliance. As "
            "people increasingly delegate decisions, both trivial and "
            "significant, to algorithmic systems, some researchers worry about "
            "a gradual erosion of independent judgement and critical thinking "
            "skills, particularly among generations who grow up with constant "
            "access to AI assistance.\n\n"
            "Navigating this transition thoughtfully, rather than either "
            "uncritically embracing or reflexively rejecting the technology, "
            "will likely determine whether artificial intelligence ultimately "
            "strengthens or undermines human capability in the decades "
            "ahead."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Artificial intelligence has no real impact on daily life.",
                "b": "The rise of AI presents genuine benefits alongside significant, unresolved challenges.",
                "c": "AI should be completely banned from all industries.",
                "d": "Automation has never affected employment in history.",
                "correct": "B",
                "explanation": "The passage presents a balanced view of AI's benefits and the various challenges it raises.",
            },
            {
                "question": "According to advocates mentioned in the passage, what advantage does AI offer regarding human work?",
                "a": "It eliminates the need for any human involvement.",
                "b": "It frees people to focus on tasks requiring creativity and judgement.",
                "c": "It guarantees permanent job security for everyone.",
                "d": "It removes the need for data analysis.",
                "correct": "B",
                "explanation": "The passage states advocates believe AI frees people to focus on work requiring creativity, judgement, or emotional intelligence.",
            },
            {
                "question": "What historical pattern do sceptics reference regarding automation and jobs?",
                "a": "Automation has never displaced any jobs before.",
                "b": "Automation has historically displaced certain jobs, though new roles typically emerge over time.",
                "c": "New jobs never emerge after automation.",
                "d": "Automation only affects agricultural jobs.",
                "correct": "B",
                "explanation": "The passage notes that automation has historically displaced jobs while new roles typically emerge, though the transition can be hard.",
            },
            {
                "question": "Why does the passage describe accountability as a 'significant challenge'?",
                "a": "Because AI systems never make errors.",
                "b": "Because determining responsibility for AI errors is more complicated than for purely human decisions.",
                "c": "Because legal frameworks have already fully resolved this issue.",
                "d": "Because AI is only used in entertainment.",
                "correct": "B",
                "explanation": "The passage explains that determining fault—whether in data, algorithm design, or deployment—is complicated with AI systems.",
            },
            {
                "question": "What concern is raised about 'over-reliance' on AI?",
                "a": "It could improve critical thinking skills significantly.",
                "b": "It could lead to a gradual erosion of independent judgement and critical thinking.",
                "c": "It has no effect on younger generations.",
                "d": "It is only a concern for elderly populations.",
                "correct": "B",
                "explanation": "The passage states researchers worry over-reliance could erode independent judgement and critical thinking, especially in younger generations.",
            },
        ],
    },

    {
        "level": "B2",
        "topic": "Social change",
        "title": "Changing Attitudes Toward Work-Life Balance",
        "text": (
            "For much of the industrial era, professional success was widely "
            "measured by hours worked and visible dedication to one's career, "
            "often at the expense of personal time. In recent years, however, "
            "this assumption has come under increasing scrutiny, as younger "
            "generations entering the workforce express markedly different "
            "priorities than their predecessors.\n\n"
            "Surveys conducted across multiple industries suggest that many "
            "young professionals now rank flexibility and personal wellbeing "
            "alongside, or even above, salary when evaluating job offers. This "
            "shift has puzzled some older executives, who built their careers "
            "under a different set of assumptions and sometimes interpret this "
            "changed attitude as a lack of ambition or commitment, rather than "
            "a genuine reordering of priorities.\n\n"
            "Proponents of this cultural shift argue that the traditional "
            "model, which glorified overwork, was never particularly "
            "sustainable or productive in the first place. Research examining "
            "the relationship between hours worked and actual output has "
            "repeatedly found that productivity tends to decline sharply "
            "beyond a certain threshold, suggesting that extended working "
            "hours often produce diminishing, and eventually negative, "
            "returns.\n\n"
            "Nevertheless, implementing genuine change has proven considerably "
            "more difficult than simply expressing support for the concept. "
            "Some companies have introduced flexible policies largely as a "
            "recruitment tool, without meaningfully altering underlying "
            "expectations or workloads, leading employees to describe such "
            "measures as superficial rather than substantive.\n\n"
            "Economic pressures further complicate this picture. During "
            "periods of economic uncertainty, employees may feel less able to "
            "prioritise personal boundaries, fearing that doing so could "
            "jeopardise job security in a competitive market. This dynamic "
            "suggests that genuine progress toward sustainable work-life "
            "balance may depend as much on broader economic conditions as on "
            "individual company policies.\n\n"
            "Whether this generational shift represents a lasting "
            "transformation in how societies value work, or merely a "
            "temporary adjustment that could reverse under different economic "
            "circumstances, remains an open question that researchers "
            "continue to study closely."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Younger generations have no interest in career success.",
                "b": "Attitudes toward work-life balance are shifting, though genuine implementation remains challenging.",
                "c": "Overworking has always been proven to increase productivity.",
                "d": "Economic conditions have no effect on workplace attitudes.",
                "correct": "B",
                "explanation": "The passage discusses the shift in attitudes and the difficulties of translating this shift into genuine workplace change.",
            },
            {
                "question": "How do some older executives interpret younger employees' changed priorities?",
                "a": "As a sign of increased ambition",
                "b": "As a lack of ambition or commitment",
                "c": "As proof of higher productivity",
                "d": "As a temporary trend with no significance",
                "correct": "B",
                "explanation": "The passage states some executives interpret the shift as a lack of ambition or commitment, rather than a genuine reordering of priorities.",
            },
            {
                "question": "What does research on hours worked and productivity suggest, according to the passage?",
                "a": "Productivity always increases with more hours worked.",
                "b": "Productivity tends to decline sharply beyond a certain threshold of hours worked.",
                "c": "There is no relationship between hours worked and output.",
                "d": "Shorter working hours always reduce output.",
                "correct": "B",
                "explanation": "The passage states research has found productivity declines sharply beyond a certain threshold of hours worked.",
            },
            {
                "question": "Why do some employees describe flexible workplace policies as 'superficial'?",
                "a": "Because companies genuinely reduce workloads alongside offering flexibility.",
                "b": "Because such policies are sometimes introduced as recruitment tools without changing underlying expectations.",
                "c": "Because flexible policies are illegal in most countries.",
                "d": "Because employees prefer traditional working hours.",
                "correct": "B",
                "explanation": "The passage explains some companies introduce flexible policies mainly as recruitment tools without meaningfully changing workloads.",
            },
            {
                "question": "What does the passage suggest about the role of economic conditions in this shift?",
                "a": "Economic conditions are irrelevant to work-life balance.",
                "b": "Economic uncertainty may make it harder for employees to prioritise personal boundaries.",
                "c": "Economic uncertainty always improves work-life balance.",
                "d": "Economic conditions only affect older workers.",
                "correct": "B",
                "explanation": "The passage states economic uncertainty may make employees less able to prioritise personal boundaries for fear of job insecurity.",
            },
        ],
    },

    {
        "level": "B2",
        "topic": "Inventions",
        "title": "Accidental Discoveries That Changed the World",
        "text": (
            "The popular image of invention often involves a scientist "
            "carefully following a planned sequence of experiments toward a "
            "predetermined goal. In reality, a surprising number of "
            "significant technological and scientific breakthroughs have "
            "emerged not from deliberate planning, but from accidents, "
            "mistakes, or observations that researchers initially considered "
            "unimportant.\n\n"
            "One of the most frequently cited examples involves the discovery "
            "of a powerful antibiotic in the late 1920s, when a researcher "
            "returned from holiday to find that mould had accidentally "
            "contaminated one of his experimental samples, unexpectedly "
            "killing the surrounding bacteria. Rather than discarding the "
            "contaminated sample as a failed experiment, the researcher "
            "recognised its significance, eventually leading to a medical "
            "breakthrough that has since saved countless lives.\n\n"
            "A similarly unplanned discovery led to the invention of a "
            "now-common adhesive material. A scientist attempting to develop "
            "an extremely strong glue instead created one with unusually weak "
            "adhesive properties, initially considered a failure. Years later, "
            "a colleague recognised that this seemingly weak glue was "
            "perfectly suited for a new product: reusable adhesive notes that "
            "could be applied and removed repeatedly without damaging "
            "surfaces.\n\n"
            "These stories share a common thread: the discoveries themselves "
            "were accidental, but recognising their value required "
            "considerable expertise and an open mind willing to consider "
            "unexpected possibilities rather than dismissing anomalies as "
            "mere failures. This quality, sometimes referred to as "
            "'prepared serendipity', suggests that accidental discovery is not "
            "purely random luck, but rather the intersection of chance "
            "occurrence with a trained ability to recognise significance.\n\n"
            "This historical pattern raises interesting questions for how "
            "modern research is organised and funded. Highly structured "
            "research environments, focused narrowly on predetermined "
            "outcomes, may inadvertently reduce opportunities for the kind of "
            "unplanned observation that has historically produced some of "
            "science's most valuable breakthroughs.\n\n"
            "Some research institutions have responded by deliberately "
            "building in time and resources for open-ended exploration, "
            "recognising that rigid efficiency, while valuable in many "
            "contexts, may not always be the most effective approach to "
            "fostering genuine innovation."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "All scientific discoveries follow a carefully planned process.",
                "b": "Many important discoveries have resulted from accidents combined with the expertise to recognise their significance.",
                "c": "Accidental discoveries are always the result of pure luck with no skill involved.",
                "d": "Modern research environments always encourage accidental discovery.",
                "correct": "B",
                "explanation": "The passage argues accidental discoveries require both chance and the expertise to recognise their value, a concept called 'prepared serendipity'.",
            },
            {
                "question": "What happened in the antibiotic discovery example described in the passage?",
                "a": "The researcher deliberately grew mould to test its effects.",
                "b": "Mould accidentally contaminated a sample and unexpectedly killed surrounding bacteria.",
                "c": "The researcher discarded the contaminated sample immediately.",
                "d": "The discovery was made through a planned series of experiments.",
                "correct": "B",
                "explanation": "The passage states mould accidentally contaminated the sample, unexpectedly killing the bacteria around it.",
            },
            {
                "question": "How did the 'weak glue' eventually become useful, according to the passage?",
                "a": "It was strengthened through further experiments.",
                "b": "A colleague recognised it was suited for a reusable adhesive note product.",
                "c": "It was discarded and never used.",
                "d": "It was combined with the antibiotic discovery.",
                "correct": "B",
                "explanation": "The passage states a colleague later recognised the weak glue's suitability for reusable adhesive notes.",
            },
            {
                "question": "What does 'prepared serendipity' mean, according to the passage?",
                "a": "Discovery that happens purely by random chance with no skill involved",
                "b": "The combination of chance occurrence with a trained ability to recognise significance",
                "c": "A structured, planned research method",
                "d": "A type of laboratory safety procedure",
                "correct": "B",
                "explanation": "The passage explicitly defines this term as the intersection of chance with a trained ability to recognise significance.",
            },
            {
                "question": "What concern does the passage raise about highly structured research environments?",
                "a": "They always lead to more accidental discoveries.",
                "b": "They may reduce opportunities for the kind of unplanned observation that produces breakthroughs.",
                "c": "They have no effect on scientific innovation.",
                "d": "They are illegal in most countries.",
                "correct": "B",
                "explanation": "The passage states narrowly focused research environments may inadvertently reduce opportunities for valuable unplanned observations.",
            },
        ],
    },

    # =========================================================
    # C1 — LEVEL 5
    # =========================================================

    {
        "level": "C1",
        "topic": "Ancient civilizations",
        "title": "Reassessing the Legacy of Ancient Rome",
        "text": (
            "For centuries, Western historical narratives have positioned "
            "ancient Rome as a foundational civilisation whose engineering, "
            "law, and governance structures laid the groundwork for much of "
            "subsequent European development. While this framing captures "
            "certain undeniable achievements, contemporary historians "
            "increasingly argue that it obscures a more complicated, and in "
            "many respects less flattering, picture of how Roman expansion "
            "actually unfolded across the territories it eventually "
            "controlled.\n\n"
            "The engineering accomplishments attributed to Rome — extensive "
            "road networks, aqueducts capable of transporting water across "
            "considerable distances, and monumental architecture that "
            "continues to influence design today — remain genuinely "
            "impressive by any historical standard. These achievements, "
            "however, existed alongside a system of conquest and governance "
            "that relied extensively on slavery, with estimates suggesting "
            "that enslaved individuals constituted a substantial proportion "
            "of the population across much of the empire at its height.\n\n"
            "Revisionist scholarship has increasingly focused on integrating "
            "perspectives from conquered populations, whose experiences were "
            "historically documented, when documented at all, almost "
            "exclusively through Roman sources with an evident interest in "
            "presenting conquest favourably. Archaeological evidence, "
            "including material culture from regions incorporated into the "
            "empire through military conquest, increasingly complicates "
            "earlier narratives that portrayed Roman expansion as an "
            "unambiguously civilising process, willingly embraced by those it "
            "encountered.\n\n"
            "This is not to suggest a wholesale rejection of Rome's "
            "historical significance, which would represent an equally "
            "distorting oversimplification in the opposite direction. Legal "
            "concepts developed during the Roman period continue to influence "
            "contemporary jurisprudence in demonstrable ways, and certain "
            "administrative innovations proved remarkably durable, persisting "
            "in modified form long after the empire's political collapse.\n\n"
            "Rather, the more productive scholarly approach involves holding "
            "multiple, sometimes uncomfortable, truths simultaneously: "
            "acknowledging genuine engineering and administrative achievement "
            "while refusing to minimise the considerable human cost that "
            "accompanied Roman expansion, a cost that earlier, more "
            "celebratory historical accounts frequently marginalised or "
            "omitted entirely.\n\n"
            "This more nuanced reassessment reflects a broader shift within "
            "historical scholarship generally, moving away from narratives "
            "centred primarily on the perspectives of conquering powers "
            "toward accounts that more deliberately incorporate the "
            "experiences of those who were conquered, displaced, or enslaved "
            "in the process."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Ancient Rome should be remembered only for its engineering achievements.",
                "b": "Contemporary historians are reassessing Rome's legacy to include both its achievements and the human costs of its expansion.",
                "c": "Roman conquest is now considered to have had no negative consequences at all.",
                "d": "Modern scholarship has completely rejected Rome's historical significance.",
                "correct": "B",
                "explanation": "The passage argues for a more balanced view that acknowledges achievements while not minimising the human costs of expansion.",
            },
            {
                "question": "According to the passage, what limitation exists in how conquered populations' experiences were historically documented?",
                "a": "They were documented equally by both Roman and local sources.",
                "b": "They were documented almost exclusively through Roman sources with an interest in favourable portrayal.",
                "c": "They were never documented at all in any form.",
                "d": "They were documented only through archaeological evidence.",
                "correct": "B",
                "explanation": "The passage states these experiences were documented almost exclusively through Roman sources favourably inclined toward conquest.",
            },
            {
                "question": "What role does archaeological evidence play in this reassessment, according to the passage?",
                "a": "It confirms earlier narratives entirely without complication.",
                "b": "It complicates earlier narratives portraying Roman expansion as unambiguously civilising.",
                "c": "It has no relevance to understanding Roman history.",
                "d": "It proves conquered populations welcomed Roman rule completely.",
                "correct": "B",
                "explanation": "The passage states archaeological evidence increasingly complicates earlier, more favourable narratives of Roman expansion.",
            },
            {
                "question": "What does the writer mean by 'holding multiple, sometimes uncomfortable, truths simultaneously'?",
                "a": "Choosing to focus only on Rome's negative aspects",
                "b": "Acknowledging both genuine achievement and the human cost of conquest at the same time",
                "c": "Ignoring historical evidence that is difficult to interpret",
                "d": "Rejecting all forms of historical achievement",
                "correct": "B",
                "explanation": "This phrase reflects the passage's argument for a balanced approach acknowledging both achievement and cost.",
            },
            {
                "question": "What broader trend in historical scholarship does the final paragraph describe?",
                "a": "A shift toward focusing exclusively on the perspectives of conquering powers",
                "b": "A shift toward incorporating the experiences of the conquered, displaced, or enslaved",
                "c": "A move away from studying ancient civilisations altogether",
                "d": "A rejection of archaeological methods in favour of written sources",
                "correct": "B",
                "explanation": "The final paragraph explicitly describes this shift toward including perspectives previously marginalised in historical narratives.",
            },
        ],
    },

    {
        "level": "C1",
        "topic": "Languages",
        "title": "The Slow Disappearance of Minority Languages",
        "text": (
            "Of the roughly seven thousand languages currently spoken "
            "worldwide, linguists estimate that a substantial proportion "
            "face a genuine risk of disappearing entirely within the next "
            "century, as the number of fluent speakers continues to decline, "
            "often precipitously, across successive generations. This "
            "phenomenon, generally termed language endangerment, represents "
            "far more than an abstract academic concern; it entails the "
            "irreversible loss of accumulated cultural knowledge, distinctive "
            "ways of conceptualising the world, and oral traditions that "
            "frequently exist nowhere in written form.\n\n"
            "The mechanisms driving language loss are varied but often "
            "interconnected. Economic pressure frequently plays a decisive "
            "role, as speakers of minority languages migrate toward urban "
            "centres where dominant languages offer clear advantages in "
            "employment, education, and social mobility. Children raised in "
            "such environments often acquire the dominant language as their "
            "primary means of communication, sometimes retaining only "
            "passive comprehension of their ancestral language, if that.\n\n"
            "Government policy has historically exacerbated this process in "
            "numerous contexts, whether through deliberate suppression of "
            "minority languages in educational settings or through more "
            "subtle mechanisms, such as providing government services "
            "exclusively in dominant languages, thereby creating strong "
            "practical incentives for linguistic assimilation regardless of "
            "official policy toward linguistic diversity.\n\n"
            "Documentation efforts, undertaken by linguists working closely "
            "with remaining speaker communities, aim to preserve at least a "
            "record of endangered languages before they disappear entirely, "
            "recording vocabulary, grammatical structures, and oral "
            "narratives for future scholarly and community use. Critics of "
            "documentation-focused approaches, however, argue that "
            "preserving a language purely as an academic record, however "
            "valuable for scholarship, differs fundamentally from sustaining "
            "it as a living means of everyday communication within an active "
            "speech community.\n\n"
            "Revitalisation efforts represent a more ambitious, though "
            "considerably more difficult, alternative, attempting to increase "
            "the number of active speakers through immersion education "
            "programmes, community initiatives, and, in some notable cases, "
            "deliberate government support for minority language "
            "instruction. Some revitalisation programmes have achieved "
            "genuinely remarkable success, demonstrating that language loss, "
            "while common, is not necessarily an inevitable or irreversible "
            "process.\n\n"
            "Nevertheless, the scale of the challenge remains considerable, "
            "and the loss of linguistic diversity, once it occurs, "
            "represents a form of cultural erasure that subsequent "
            "generations, however motivated, may find genuinely impossible to "
            "fully reverse."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Language loss is a minor issue with no real cultural consequences.",
                "b": "Minority languages face serious risk of disappearing, driven by complex economic and political factors, though revitalisation offers some hope.",
                "c": "All minority languages will inevitably disappear within a few years.",
                "d": "Government policy has always successfully protected minority languages.",
                "correct": "B",
                "explanation": "The passage discusses the causes of language endangerment and presents both documentation and revitalisation as partial responses, with cautious hope.",
            },
            {
                "question": "According to the passage, why does economic pressure often lead to language loss?",
                "a": "Because dominant languages offer clear advantages in employment and social mobility.",
                "b": "Because minority languages are always more difficult to learn.",
                "c": "Because economic pressure has no connection to migration.",
                "d": "Because urban centres actively ban minority languages.",
                "correct": "A",
                "explanation": "The passage explains that speakers migrate to cities where dominant languages offer practical advantages, contributing to language loss.",
            },
            {
                "question": "How can government policy contribute to language loss, according to the passage, even without explicit suppression?",
                "a": "By providing government services exclusively in dominant languages, creating incentives for assimilation.",
                "b": "By funding minority language schools generously.",
                "c": "By requiring all citizens to learn multiple languages.",
                "d": "By banning migration to urban centres.",
                "correct": "A",
                "explanation": "The passage states that providing services only in dominant languages creates practical incentives for linguistic assimilation.",
            },
            {
                "question": "What distinction do critics draw between documentation and revitalisation, according to the passage?",
                "a": "They consider them identical processes.",
                "b": "They argue documentation preserves an academic record, while revitalisation aims to sustain a language as a living means of communication.",
                "c": "They believe documentation is more effective than revitalisation in all cases.",
                "d": "They argue revitalisation is unnecessary once documentation is complete.",
                "correct": "B",
                "explanation": "The passage explains critics distinguish between preserving a language as an academic record versus sustaining it as living, everyday communication.",
            },
            {
                "question": "What does the final paragraph suggest about the reversibility of language loss?",
                "a": "Language loss can always be fully reversed with enough effort.",
                "b": "Once significant language loss occurs, it may be genuinely impossible for later generations to fully reverse it.",
                "c": "Language loss has no lasting cultural consequences.",
                "d": "Revitalisation programmes have never achieved any success.",
                "correct": "B",
                "explanation": "The final paragraph states that loss of linguistic diversity may be genuinely impossible to fully reverse, despite motivation.",
            },
        ],
    },

    {
        "level": "C1",
        "topic": "Climate",
        "title": "The Complex Politics of Climate Adaptation",
        "text": (
            "Much of the public discourse surrounding climate change has "
            "historically centred on mitigation — reducing greenhouse gas "
            "emissions to limit the extent of future warming. In recent "
            "years, however, growing recognition that a certain degree of "
            "climate disruption is now unavoidable, regardless of future "
            "emissions trajectories, has shifted increasing attention toward "
            "adaptation: the process of adjusting infrastructure, "
            "agriculture, and communities to withstand climate impacts "
            "already underway or reasonably anticipated in coming decades.\n\n"
            "This shift, while pragmatically necessary, introduces "
            "politically fraught questions that mitigation-focused framings "
            "had largely managed to avoid. Adaptation, by its nature, "
            "requires difficult decisions about resource allocation: which "
            "communities receive protective infrastructure first, which "
            "agricultural regions receive support to transition toward more "
            "resilient crops, and, perhaps most contentiously, which areas "
            "are ultimately deemed too vulnerable to defend, requiring "
            "instead a longer-term strategy of managed retreat.\n\n"
            "These decisions carry substantial equity implications that "
            "researchers and policymakers are only beginning to grapple with "
            "systematically. Wealthier communities and nations typically "
            "possess considerably greater financial capacity to invest in "
            "protective infrastructure, while lower-income communities, "
            "which have frequently contributed least to the emissions driving "
            "climate change in the first place, often face the most severe "
            "impacts with the fewest resources available for adaptation.\n\n"
            "International climate negotiations have attempted to address "
            "this disparity through mechanisms intended to direct financial "
            "support from wealthier, historically higher-emitting nations "
            "toward more vulnerable countries facing disproportionate "
            "climate impacts. Progress on these commitments, however, has "
            "proven inconsistent, with promised funding frequently falling "
            "short of stated targets, and disagreements persisting over how "
            "such funds should be allocated and monitored.\n\n"
            "Within individual countries, adaptation politics can prove "
            "similarly contentious. Decisions about which coastal areas "
            "receive expensive flood defences, for instance, inevitably "
            "involve implicit judgements about whose property and "
            "livelihoods are considered worth protecting, judgements that "
            "existing patterns of political influence and economic power can "
            "shape in ways that may not align with objective measures of "
            "vulnerability or need.\n\n"
            "As climate impacts intensify in coming decades, these "
            "underlying tensions between technical adaptation planning and "
            "the political realities of resource distribution seem likely to "
            "become considerably more pronounced, rather than resolved "
            "through improved planning alone."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Climate adaptation is a purely technical process with no political dimension.",
                "b": "Climate adaptation raises complex political and equity questions about resource distribution.",
                "c": "Mitigation has completely replaced the need for adaptation.",
                "d": "Wealthy nations have already fully resolved climate adaptation funding issues.",
                "correct": "B",
                "explanation": "The passage focuses on the politically fraught, equity-related decisions inherent in climate adaptation planning.",
            },
            {
                "question": "According to the passage, what is 'managed retreat'?",
                "a": "A strategy of investing heavily in flood defences",
                "b": "A longer-term strategy applied to areas deemed too vulnerable to defend",
                "c": "A method of reducing greenhouse gas emissions",
                "d": "A form of international climate negotiation",
                "correct": "B",
                "explanation": "The passage describes managed retreat as the strategy for areas ultimately deemed too vulnerable to defend.",
            },
            {
                "question": "What equity concern does the passage raise regarding wealthier versus lower-income communities?",
                "a": "Lower-income communities always have more resources for adaptation.",
                "b": "Lower-income communities often face severe climate impacts with fewer resources, despite contributing less to emissions.",
                "c": "Wealthier communities are unaffected by climate change.",
                "d": "Equity has no connection to climate adaptation funding.",
                "correct": "B",
                "explanation": "The passage explicitly states lower-income communities face severe impacts with fewer resources despite contributing least to emissions.",
            },
            {
                "question": "According to the passage, how has progress on international climate finance commitments been described?",
                "a": "Entirely successful and consistent",
                "b": "Inconsistent, with funding often falling short of targets",
                "c": "Completely abandoned by all nations",
                "d": "Fully resolved through clear monitoring systems",
                "correct": "B",
                "explanation": "The passage states progress has proven inconsistent, with promised funding frequently falling short of targets.",
            },
            {
                "question": "What does the passage suggest about the future of adaptation politics?",
                "a": "Tensions will likely resolve naturally through better planning alone.",
                "b": "Tensions between technical planning and political resource distribution are likely to intensify.",
                "c": "Adaptation politics will become irrelevant as mitigation succeeds.",
                "d": "All countries will reach equal adaptation capacity soon.",
                "correct": "B",
                "explanation": "The final paragraph states these tensions seem likely to become more pronounced rather than resolved through planning alone.",
            },
        ],
    },

    {
        "level": "C1",
        "topic": "Agriculture",
        "title": "Rethinking Food Production for a Changing Planet",
        "text": (
            "Global food systems face a convergence of pressures that, taken "
            "together, present one of the more formidable challenges "
            "confronting agricultural planning in the coming decades. A "
            "growing global population requires increased food production, "
            "even as climate volatility, soil degradation, and water scarcity "
            "threaten to constrain the very agricultural capacity upon which "
            "that increased production depends.\n\n"
            "Conventional intensive agriculture, which dramatically increased "
            "global food output over the past century through mechanisation, "
            "synthetic fertilisers, and high-yield crop varieties, has "
            "proven remarkably effective at producing large quantities of "
            "food relatively cheaply. This approach, however, carries "
            "environmental costs that are becoming increasingly difficult to "
            "ignore: soil degradation from repeated intensive cultivation, "
            "water pollution from fertiliser runoff, and significant "
            "greenhouse gas emissions associated with both agricultural "
            "production and the extensive supply chains required to "
            "distribute food globally.\n\n"
            "In response, researchers and farmers have explored a range of "
            "alternative approaches, though none has yet demonstrated the "
            "capacity to fully replace conventional methods at comparable "
            "scale. Regenerative agriculture, which prioritises soil health "
            "through techniques such as reduced tillage and crop rotation, "
            "shows genuine promise for improving long-term land productivity, "
            "though transitioning from conventional methods often requires "
            "farmers to accept reduced yields during an uncertain transition "
            "period, a financial risk many cannot easily absorb without "
            "substantial external support.\n\n"
            "Technological innovations offer another avenue for improvement. "
            "Precision agriculture, employing sensors and data analysis to "
            "optimise water and fertiliser use at a highly localised level, "
            "has demonstrated meaningful efficiency gains in contexts where "
            "farmers possess the capital and technical knowledge required for "
            "implementation. This requirement, however, raises concerns that "
            "such innovations could disproportionately benefit larger, "
            "wealthier agricultural operations, potentially widening existing "
            "disparities between smallholder farmers and industrial "
            "agricultural enterprises.\n\n"
            "Some researchers argue that dietary shifts, particularly reduced "
            "consumption of resource-intensive animal products in regions "
            "where consumption is currently high, could meaningfully reduce "
            "pressure on agricultural systems without requiring proportional "
            "increases in production. Such proposals, however, frequently "
            "encounter considerable cultural and economic resistance, "
            "underscoring that technical solutions alone are unlikely to "
            "resolve challenges that are, at their core, deeply entangled "
            "with questions of culture, economics, and political feasibility.\n\n"
            "No single strategy discussed here appears sufficient in "
            "isolation; rather, most researchers studying this issue "
            "increasingly conclude that meaningful progress will likely "
            "require some combination of these approaches, implemented "
            "unevenly across different regions according to local "
            "conditions, resources, and priorities."
        ),
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "a": "Conventional agriculture has no environmental costs whatsoever.",
                "b": "Global food systems face converging pressures requiring a combination of approaches rather than a single solution.",
                "c": "Regenerative agriculture has already fully replaced conventional farming.",
                "d": "Dietary change alone can solve all agricultural challenges.",
                "correct": "B",
                "explanation": "The passage presents multiple approaches to agricultural challenges, concluding no single strategy is sufficient alone.",
            },
            {
                "question": "According to the passage, what environmental costs are associated with conventional intensive agriculture?",
                "a": "Reduced global food output",
                "b": "Soil degradation, water pollution, and significant greenhouse gas emissions",
                "c": "A complete absence of environmental impact",
                "d": "Decreased use of fertilisers",
                "correct": "B",
                "explanation": "The passage explicitly lists soil degradation, water pollution from fertiliser runoff, and greenhouse gas emissions as costs.",
            },
            {
                "question": "What financial challenge do farmers face when transitioning to regenerative agriculture, according to the passage?",
                "a": "They must accept reduced yields during an uncertain transition period.",
                "b": "They receive guaranteed government funding immediately.",
                "c": "They face no financial risk at all.",
                "d": "They are required to stop farming completely.",
                "correct": "A",
                "explanation": "The passage states farmers often must accept reduced yields during transition, a financial risk many cannot easily absorb.",
            },
            {
                "question": "What concern is raised about precision agriculture technology?",
                "a": "It benefits smallholder farmers more than industrial operations.",
                "b": "It could disproportionately benefit larger, wealthier agricultural operations, widening disparities.",
                "c": "It has no requirement for capital or technical knowledge.",
                "d": "It has proven completely ineffective in all contexts.",
                "correct": "B",
                "explanation": "The passage explains this technology requires capital and technical knowledge, raising concerns about widening disparities with smallholder farmers.",
            },
            {
                "question": "Why does the passage suggest dietary shifts alone are unlikely to resolve agricultural challenges?",
                "a": "Because dietary shifts have no effect on agricultural pressure.",
                "b": "Because such proposals often face considerable cultural and economic resistance.",
                "c": "Because dietary shifts are illegal in most countries.",
                "d": "Because animal products are not resource-intensive.",
                "correct": "B",
                "explanation": "The passage states dietary shift proposals frequently encounter cultural and economic resistance, showing technical solutions alone are insufficient.",
            },
        ],
    },

]


class Command(BaseCommand):

    help = (
        "Seeds the Reading Bank with original CEFR-leveled reading passages "
        "and questions (Batch 1, installment 2). Safe to run multiple times "
        "— never creates duplicates and never removes existing data."
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

        self.stdout.write(
            self.style.SUCCESS("Reading Bank Batch 1 (part 2) ready!")
        )
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
